from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
DATA = ROOT
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)


def load_data():
    raw = pd.read_csv(DATA / "atmosync_raw.csv")
    df = raw.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.drop_duplicates().sort_values("timestamp")
    for col, lo, hi in [
        ("temperature_c", -20, 55),
        ("humidity_pct", 0, 100),
        ("wind_speed_kmh", 0, 200),
        ("precipitation_mm", 0, 1000),
    ]:
        bad = ~df[col].between(lo, hi)
        df.loc[bad, col] = np.nan
    df["humidity_pct"] = df.groupby("location_id")["humidity_pct"].transform(
        lambda s: s.interpolate(limit_direction="both")
    )
    df["hour"] = df["timestamp"].dt.hour
    df["date"] = df["timestamp"].dt.date
    df["comfort_score"] = 100 - (
        np.abs(df["temperature_c"] - 27) * 5
        + np.abs(df["humidity_pct"] - 55) * 0.55
    )
    df["comfort_score"] = df["comfort_score"].clip(0, 100).round(2)
    df["rain_risk"] = np.select(
        [df["precipitation_mm"] >= 1, df["precipitation_mm"] >= 0.3],
        ["High", "Medium"], default="Low"
    )
    df["wind_risk"] = np.select(
        [df["wind_speed_kmh"] >= 12, df["wind_speed_kmh"] >= 8],
        ["High", "Medium"], default="Low"
    )
    return df


def build_kpis(df):
    kpi = df.groupby("location_id").agg(
        observations=("location_id", "size"),
        avg_temperature_c=("temperature_c", "mean"),
        avg_humidity_pct=("humidity_pct", "mean"),
        avg_wind_speed_kmh=("wind_speed_kmh", "mean"),
        total_precipitation_mm=("precipitation_mm", "sum"),
        avg_comfort_score=("comfort_score", "mean"),
        high_rain_observations=("rain_risk", lambda s: (s == "High").sum()),
        high_wind_observations=("wind_risk", lambda s: (s == "High").sum()),
    ).reset_index()
    return kpi.round(2)


def make_charts(df, kpi):
    plt.figure(figsize=(11, 5))
    daily = df.groupby("date")["temperature_c"].mean()
    plt.plot(pd.to_datetime(daily.index), daily.values)
    plt.title("AtmoSync — Daily Average Temperature")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.tight_layout()
    plt.savefig(OUT / "daily_trend.png", dpi=160)
    plt.close()

    plt.figure(figsize=(9, 5))
    plt.bar(kpi["location_id"], kpi["avg_comfort_score"])
    plt.title("Average Comfort Score by Location")
    plt.xlabel("Location")
    plt.ylabel("Comfort Score (0–100)")
    plt.tight_layout()
    plt.savefig(OUT / "location_comparison.png", dpi=160)
    plt.close()

    corr_cols = ["temperature_c", "humidity_pct", "wind_speed_kmh", "precipitation_mm", "pressure_hpa", "solar_wm2", "comfort_score"]
    corr = df[corr_cols].corr()
    plt.figure(figsize=(9, 7))
    plt.imshow(corr, aspect="auto")
    plt.colorbar(label="Correlation")
    plt.xticks(range(len(corr_cols)), corr_cols, rotation=45, ha="right")
    plt.yticks(range(len(corr_cols)), corr_cols)
    plt.title("Environmental Variable Correlation")
    plt.tight_layout()
    plt.savefig(OUT / "correlation_heatmap.png", dpi=160)
    plt.close()

    hourly = df.groupby("hour")["comfort_score"].mean()
    plt.figure(figsize=(10, 5))
    plt.plot(hourly.index, hourly.values, marker="o")
    plt.title("Average Comfort Score by Hour")
    plt.xlabel("Hour of Day")
    plt.ylabel("Comfort Score")
    plt.xticks(range(24))
    plt.grid(alpha=0.25)
    plt.tight_layout()
    plt.savefig(OUT / "comfort_by_hour.png", dpi=160)
    plt.close()

    hourly.to_csv(OUT / "hourly_profile.csv", header=["avg_comfort_score"])


def main():
    df = load_data()
    kpi = build_kpis(df)
    df.to_csv(DATA / "atmosync_clean.csv", index=False)
    kpi.to_csv(OUT / "location_kpis.csv", index=False)
    make_charts(df, kpi)
    print("AtmoSync analysis complete")
    print(kpi.to_string(index=False))


if __name__ == "__main__":
    main()
