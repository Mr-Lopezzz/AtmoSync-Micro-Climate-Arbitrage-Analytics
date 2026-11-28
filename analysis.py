from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
DATA = ROOT
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)



def load_data():
    input_file = DATA / "atmosync_raw.csv"

    if not input_file.exists():
        raise FileNotFoundError(
            f"Raw dataset not found: {input_file}"
        )

    raw = pd.read_csv(input_file)

    required_columns = [
        "timestamp",
        "location_id",
        "temperature_c",
        "humidity_pct",
        "wind_speed_kmh",
        "precipitation_mm",
        "pressure_hpa",
        "solar_wm2",
    ]

    missing_columns = [
        col for col in required_columns if col not in raw.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Dataset is missing required columns: {missing_columns}"
        )

    if raw.empty:
        raise ValueError("The raw dataset is empty.")

    total_input_records = len(raw)
    
    df = raw.copy()

    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        format="%d-%m-%y %H:%M",
        errors="coerce"
    )

    invalid_timestamps = df["timestamp"].isna().sum()

    df = df.dropna(subset=["timestamp"])

    print(f"Invalid timestamps removed: {invalid_timestamps}")

    duplicate_records = df.duplicated().sum()
    df = df.drop_duplicates().sort_values("timestamp")

    for col, lo, hi in [
        ("temperature_c", -20, 55),
        ("humidity_pct", 0, 100),
        ("wind_speed_kmh", 0, 200),
        ("precipitation_mm", 0, 1000),
    ]:
        bad = ~df[col].between(lo, hi)
        df.loc[bad, col] = np.nan
    
    missing_values_before_imputation = df.isna().sum()

    df["humidity_pct"] = df.groupby("location_id")["humidity_pct"].transform(
        lambda s: s.interpolate(limit_direction="both")
    )

    df["temperature_c"] = df.groupby("location_id")["temperature_c"].transform(
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
        [
            df["precipitation_mm"].isna(),
            df["precipitation_mm"] >= 1,
            df["precipitation_mm"] >= 0.3,
        ],
        ["Unknown", "High", "Medium"],
        default="Low"
    )

    df["wind_risk"] = np.select(
        [
            df["wind_speed_kmh"].isna(),
            df["wind_speed_kmh"] >= 12,
            df["wind_speed_kmh"] >= 8,
        ],
        ["Unknown", "High", "Medium"],
        default="Low"
    )

    final_cleaned_records = len(df)

    missing_values_after_imputation = df.isna().sum()

    create_data_quality_report(
        total_input_records,
        invalid_timestamps,
        duplicate_records,
        final_cleaned_records,
        missing_values_before_imputation,
        missing_values_after_imputation
    )

    return df

def create_data_quality_report(
    total_input_records,
    invalid_timestamps,
    duplicate_records,
    final_cleaned_records,
    missing_values_before_imputation,
    missing_values_after_imputation
):
    total_values_imputed = (
        missing_values_before_imputation
        - missing_values_after_imputation.reindex(
            missing_values_before_imputation.index
        )
    ).clip(lower=0).sum()

    total_missing_before = missing_values_before_imputation.sum()

    cleaning_efficiency = (
        (total_values_imputed / total_missing_before) * 100
        if total_missing_before > 0
        else 0
    )

    cleaning_efficiency = round(cleaning_efficiency, 2)

    quality_report = pd.DataFrame({
        "Metric": [
            "Total Input Records",
            "Invalid Timestamps Removed",
            "Duplicate Records Removed",
            "Final Cleaned Records",
            "Total Values Imputed",
            "Data Cleaning Efficiency (%)",
        ],
        "Value": [
            total_input_records,
            invalid_timestamps,
            duplicate_records,
            final_cleaned_records,
            total_values_imputed,
            cleaning_efficiency,
        ]
    })

    quality_report.to_csv(
        OUT / "data_quality_report.csv",
        index=False
    )

    missing_report = pd.DataFrame({
        "Column": missing_values_before_imputation.index,
        "Missing Before Imputation": missing_values_before_imputation.values,
        "Missing After Imputation": missing_values_after_imputation.reindex(
            missing_values_before_imputation.index
        ).values
    })

    missing_report.to_csv(
        OUT / "missing_values_report.csv",
        index=False
    )

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
    plt.title("AtmoSync - Daily Average Temperature")
    plt.xlabel("Date")
    plt.ylabel("Temperature (deg C)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(OUT / "daily_trend.png", dpi=160)
    plt.close()

    plt.figure(figsize=(9, 5))
    bars = plt.bar(kpi["location_id"], kpi["avg_comfort_score"])
    plt.bar_label(bars, fmt="%.2f", padding=3)
    plt.title("Average Comfort Score by Location")
    plt.xlabel("Location")
    plt.ylabel("Comfort Score (0-100)")
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
