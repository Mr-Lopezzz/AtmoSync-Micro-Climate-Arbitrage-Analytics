from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "atmosync_clean.csv"

st.set_page_config(page_title="AtmoSync Analytics", layout="wide")
st.title("AtmoSync — Micro-Climate Analytics")
st.caption("Synthetic/public-safe telemetry dataset for portfolio demonstration")

df = pd.read_csv(DATA, parse_dates=["timestamp"])

locations = st.sidebar.multiselect(
    "Locations", sorted(df["location_id"].unique()),
    default=sorted(df["location_id"].unique())
)
metric = st.sidebar.selectbox(
    "Trend metric", ["temperature_c", "humidity_pct", "wind_speed_kmh", "comfort_score"]
)

view = df[df["location_id"].isin(locations)].copy()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Observations", f"{len(view):,}")
c2.metric("Avg Temperature", f"{view.temperature_c.mean():.1f} °C")
c3.metric("Avg Humidity", f"{view.humidity_pct.mean():.1f}%")
c4.metric("Avg Comfort", f"{view.comfort_score.mean():.1f}")

st.subheader("Trend")
trend = view.groupby("timestamp")[metric].mean().sort_index()
st.line_chart(trend)

st.subheader("Location KPIs")
kpi = view.groupby("location_id").agg(
    Avg_Temperature_C=("temperature_c", "mean"),
    Avg_Humidity_pct=("humidity_pct", "mean"),
    Avg_Wind_kmh=("wind_speed_kmh", "mean"),
    Avg_Comfort=("comfort_score", "mean"),
    High_Rain_Count=("rain_risk", lambda s: (s == "High").sum()),
    High_Wind_Count=("wind_risk", lambda s: (s == "High").sum()),
).round(2)
st.dataframe(kpi, use_container_width=True)

st.subheader("Comfort by Hour")
hourly = view.groupby("hour")["comfort_score"].mean().sort_index()
st.line_chart(hourly)

st.subheader("Risk Distribution")
rc1, rc2 = st.columns(2)
with rc1:
    st.write("Rain Risk")
    st.bar_chart(view["rain_risk"].value_counts())
with rc2:
    st.write("Wind Risk")
    st.bar_chart(view["wind_risk"].value_counts())
