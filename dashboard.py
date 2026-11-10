from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
DATA = "atmosync_clean.csv"

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

c1.metric(
    "Total Observations",
    f"{len(view):,}",
    help="Total number of selected weather observations"
)

c2.metric(
    "Average Temperature",
    f"{view.temperature_c.mean():.1f} °C"
)

c3.metric(
    "Average Humidity",
    f"{view.humidity_pct.mean():.1f}%"
)

c4.metric(
    "Average Comfort",
    f"{view.comfort_score.mean():.1f}/100"
)

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


metric_labels = {
    "temperature_c": "Temperature (°C)",
    "humidity_pct": "Humidity (%)",
    "wind_speed_kmh": "Wind Speed (km/h)",
    "comfort_score": "Comfort Score"
}

st.subheader(f"{metric_labels[metric]} by Hour")
hourly = view.groupby("hour")[metric].mean().sort_index()
st.line_chart(hourly)


st.subheader("Weather Risk Alerts")

st.subheader("Location-wise Risk Analysis")

risk_by_location = view.groupby("location_id").agg(
    High_Rain_Risk=("rain_risk", lambda s: (s == "High").sum()),
    High_Wind_Risk=("wind_risk", lambda s: (s == "High").sum())
).reset_index()

st.write("High-risk observations by location:")

st.dataframe(
    risk_by_location,
    hide_index=True,
    use_container_width=True
)

st.subheader("Location Risk Comparison")

chart_data = risk_by_location.set_index("location_id")[
    ["High_Rain_Risk", "High_Wind_Risk"]
]

st.bar_chart(chart_data)

st.subheader("Download Analytics Report")

col1, col2 = st.columns(2)

with col1:
    st.download_button(
        label="Download Filtered Data (CSV)",
        data=view.to_csv(index=False).encode("utf-8"),
        file_name="atmosync_filtered_data.csv",
        mime="text/csv"
    )

with col2:
    st.download_button(
        label="Download Location Risk Report (CSV)",
        data=risk_by_location.to_csv(index=False).encode("utf-8"),
        file_name="atmosync_location_risk_report.csv",
        mime="text/csv"
    )

high_rain = (view["rain_risk"] == "High").sum()
high_wind = (view["wind_risk"] == "High").sum()

alert1, alert2 = st.columns(2)

with alert1:
    if high_rain > 0:
        st.warning(f"Rain Risk Alert: {high_rain} high-risk observations detected.")
    else:
        st.success("No high rain-risk observations detected.")

with alert2:
    if high_wind > 0:
        st.warning(f"Wind Risk Alert: {high_wind} high-risk observations detected.")
    else:
        st.success("No high wind-risk observations detected.")

st.subheader("Risk Distribution")
rc1, rc2 = st.columns(2)
with rc1:
    st.write("Rain Risk")
    st.bar_chart(view["rain_risk"].value_counts())
with rc2:
    st.write("Wind Risk")
    st.bar_chart(view["wind_risk"].value_counts())
