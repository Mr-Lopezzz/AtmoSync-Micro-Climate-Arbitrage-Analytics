from pathlib import Path
import pandas as pd
import streamlit as st

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "atmosync_clean.csv"

st.set_page_config(
    page_title="AtmoSync | Climate Intelligence",
    page_icon="🌦️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# CUSTOM UI STYLING
# --------------------------------------------------

st.markdown("""
<style>
    .stApp {
        background-color: #0b1120;
        color: #e5e7eb;
    }

    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #263449;
    }

    .main-title {
        font-size: 32px;
        font-weight: 800;
        color: #f8fafc;
        letter-spacing: -1px;
    }

    .subtitle {
        color: #94a3b8;
        font-size: 14px;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 20px;
        font-weight: 700;
        color: #f1f5f9;
        margin-top: 15px;
        margin-bottom: 12px;
    }

    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, #17243a, #111c2e);
        border: 1px solid #263b57;
        padding: 20px 18px;
        border-radius: 12px;
    }

    div[data-testid="stMetricLabel"] {
        color: #94a3b8;
    }

    div[data-testid="stMetricValue"] {
        color: #7dd3fc;
        font-weight: 750;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #263449;
        border-radius: 10px;
    }

    div.stDownloadButton > button {
        background: #0879d1;
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        width: 100%;
    }

    div.stDownloadButton > button:hover {
        background: #0ea5e9;
        color: white;
    }

    hr {
        border-color: #263449;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">🌦️ AtmoSync</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'MICRO-CLIMATE INTELLIGENCE & ENVIRONMENTAL MONITORING'
    '</div>',
    unsafe_allow_html=True
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

if not DATA.exists():
    st.error(f"Dataset not found: {DATA}")
    st.stop()

df = pd.read_csv(DATA, parse_dates=["timestamp"])

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.markdown("## ⚙️ Dashboard Controls")
st.sidebar.caption("Customize your analytics view")

all_locations = sorted(df["location_id"].dropna().unique())

locations = st.sidebar.multiselect(
    "Select Monitoring Locations",
    all_locations,
    default=all_locations
)

metric_options = {
    "Temperature": "temperature_c",
    "Humidity": "humidity_pct",
    "Wind Speed": "wind_speed_kmh",
    "Comfort Score": "comfort_score"
}

selected_metric = st.sidebar.selectbox(
    "Select Trend Metric",
    list(metric_options.keys())
)

metric = metric_options[selected_metric]

st.sidebar.divider()
st.sidebar.caption("AtmoSync | Climate Analytics")
st.sidebar.caption("Portfolio Demonstration")

# --------------------------------------------------
# FILTER DATA
# --------------------------------------------------

view = df[df["location_id"].isin(locations)].copy()

if view.empty:
    st.warning("No data available. Please select at least one location.")
    st.stop()

# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

st.markdown(
    '<div class="section-title">Executive Overview</div>',
    unsafe_allow_html=True
)

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Total Observations",
    f"{len(view):,}"
)

c2.metric(
    "Average Temperature",
    f"{view['temperature_c'].mean():.1f} °C"
)

c3.metric(
    "Average Humidity",
    f"{view['humidity_pct'].mean():.1f}%"
)

c4.metric(
    "Comfort Index",
    f"{view['comfort_score'].mean():.1f}/100"
)

st.divider()

# --------------------------------------------------

# CLIMATE TREND
# --------------------------------------------------

st.markdown(
    '<div class="section-title">📈 Climate Trends</div>',
    unsafe_allow_html=True
)

trend = (
    view.set_index("timestamp")[metric]
    .resample("D")
    .mean()
    .dropna()
)

st.caption(f"Daily average — {selected_metric}")

# Format dates for a clearer X-axis
trend_chart = (
    trend.rename_axis("Date")
    .rename("Value")
    .reset_index()
)

trend_chart["Date"] = pd.to_datetime(
    trend_chart["Date"]
).dt.strftime("%d %b")

st.line_chart(
    trend_chart,
    x="Date",
    y="Value",
    x_label="Date",
    y_label=selected_metric,
    use_container_width=True
)

st.divider()

# --------------------------------------------------
# ANALYTICS SUMMARY
# --------------------------------------------------

st.markdown(
    '<div class="section-title">📊 Analytics Summary</div>',
    unsafe_allow_html=True
)

summary_rain = (view["rain_risk"] == "High").sum()
summary_wind = (view["wind_risk"] == "High").sum()

s1, s2 = st.columns(2)

with s1:
    st.info(
        f"""
        **Monitoring Summary**

        - Total observations: {len(view):,}
        - Locations monitored: {view['location_id'].nunique()}
        - Average temperature: {view['temperature_c'].mean():.1f} °C
        - Average humidity: {view['humidity_pct'].mean():.1f}%
        """
    )

with s2:
    st.warning(
        f"""
        **Environmental Risk Summary**

        - High rain-risk observations: {summary_rain}
        - High wind-risk observations: {summary_wind}
        """
    )

# --------------------------------------------------

# --------------------------------------------------
# DYNAMIC EXECUTIVE INSIGHTS
# --------------------------------------------------

st.divider()

st.markdown(
    '<div class="section-title">🧠 Executive Climate Insights</div>',
    unsafe_allow_html=True
)

if not view.empty:

    location_insights = view.groupby("location_id").agg(
        temperature=("temperature_c", "mean"),
        humidity=("humidity_pct", "mean"),
        comfort=("comfort_score", "mean"),
        rain_alerts=("rain_risk", lambda s: (s == "High").sum()),
        wind_alerts=("wind_risk", lambda s: (s == "High").sum())
    )

    hottest = location_insights["temperature"].idxmax()
    humidest = location_insights["humidity"].idxmax()
    lowest_comfort = location_insights["comfort"].idxmin()

    highest_rain = location_insights["rain_alerts"].idxmax()
    highest_wind = location_insights["wind_alerts"].idxmax()

    st.markdown("### Key Findings")

    c1, c2 = st.columns(2)

    with c1:
        st.info(
            f"🌡️ **Highest Average Temperature**\n\n"
            f"{hottest}: "
            f"{location_insights.loc[hottest, 'temperature']:.2f} °C"
        )

        st.info(
            f"💧 **Highest Average Humidity**\n\n"
            f"{humidest}: "
            f"{location_insights.loc[humidest, 'humidity']:.2f}%"
        )

        st.warning(
            f"🌧️ **Most High-Rain Alerts**\n\n"
            f"{highest_rain}: "
            f"{int(location_insights.loc[highest_rain, 'rain_alerts'])} observations"
        )

    with c2:
        st.warning(
            f"🌤️ **Lowest Average Comfort**\n\n"
            f"{lowest_comfort}: "
            f"{location_insights.loc[lowest_comfort, 'comfort']:.2f}/100"
        )

        st.info(
            f"💨 **Most High-Wind Alerts**\n\n"
            f"{highest_wind}: "
            f"{int(location_insights.loc[highest_wind, 'wind_alerts'])} observations"
        )

    st.caption(
        "Insights are calculated dynamically using your selected locations and filters."
    )

else:
    st.info("No observations available for executive insights.")


# --------------------------------------------------
# CLIMATE ANOMALY DETECTION
# --------------------------------------------------

st.divider()

st.markdown(
    '<div class="section-title">🔍 Climate Anomaly Detection</div>',
    unsafe_allow_html=True
)

if not view.empty:

    anomaly_data = view.copy()

    anomaly_data["temp_mean"] = (
        anomaly_data.groupby("location_id")["temperature_c"]
        .transform("mean")
    )

    anomaly_data["temp_std"] = (
        anomaly_data.groupby("location_id")["temperature_c"]
        .transform("std")
    )

    anomaly_data["humidity_mean"] = (
        anomaly_data.groupby("location_id")["humidity_pct"]
        .transform("mean")
    )

    anomaly_data["humidity_std"] = (
        anomaly_data.groupby("location_id")["humidity_pct"]
        .transform("std")
    )

    anomaly_data["Temperature_Anomaly"] = (
        (anomaly_data["temperature_c"] - anomaly_data["temp_mean"]).abs()
        > (2 * anomaly_data["temp_std"])
    )

    anomaly_data["Humidity_Anomaly"] = (
        (anomaly_data["humidity_pct"] - anomaly_data["humidity_mean"]).abs()
        > (2 * anomaly_data["humidity_std"])
    )

    anomaly_data["Anomaly_Detected"] = (
        anomaly_data["Temperature_Anomaly"]
        | anomaly_data["Humidity_Anomaly"]
    )

    total_anomalies = int(
        anomaly_data["Anomaly_Detected"].sum()
    )

    temp_anomalies = int(
        anomaly_data["Temperature_Anomaly"].sum()
    )

    humidity_anomalies = int(
        anomaly_data["Humidity_Anomaly"].sum()
    )

    a1, a2, a3 = st.columns(3)

    a1.metric("Total Anomalies", f"{total_anomalies:,}")
    a2.metric("Temperature Anomalies", f"{temp_anomalies:,}")
    a3.metric("Humidity Anomalies", f"{humidity_anomalies:,}")

    st.caption(
        "Anomalies are observations more than two standard deviations "
        "from their location's average."
    )

    anomaly_results = anomaly_data[
        anomaly_data["Anomaly_Detected"]
    ].copy()

    st.markdown("#### Detected Unusual Observations")

    if not anomaly_results.empty:

        display_columns = [
            "timestamp",
            "location_id",
            "temperature_c",
            "humidity_pct",
            "Temperature_Anomaly",
            "Humidity_Anomaly"
        ]

        st.dataframe(
            anomaly_results[display_columns],
            hide_index=True,
            use_container_width=True
        )

    else:
        st.success("No unusual observations detected.")

else:
    st.info("No data available for anomaly detection.")

# --------------------------------------------------
# ADVANCED WEATHER RISK INTELLIGENCE
# --------------------------------------------------

st.divider()

st.markdown(
    '<div class="section-title">🎯 Advanced Weather Risk Intelligence</div>',
    unsafe_allow_html=True
)

if not view.empty:

    risk_data = view.copy()

    risk_data["Rain_Alert"] = (
        risk_data["rain_risk"] == "High"
    ).astype(int)

    risk_data["Wind_Alert"] = (
        risk_data["wind_risk"] == "High"
    ).astype(int)

    risk_data["Temp_Deviation"] = (
        risk_data["temperature_c"]
        - risk_data.groupby("location_id")["temperature_c"]
        .transform("mean")
    ).abs()

    risk_data["Humidity_Deviation"] = (
        risk_data["humidity_pct"]
        - risk_data.groupby("location_id")["humidity_pct"]
        .transform("mean")
    ).abs()

    risk_summary = risk_data.groupby("location_id").agg(
        Rain_Alerts=("Rain_Alert", "sum"),
        Wind_Alerts=("Wind_Alert", "sum"),
        Avg_Temp_Deviation=("Temp_Deviation", "mean"),
        Avg_Humidity_Deviation=("Humidity_Deviation", "mean")
    )

    risk_summary["Risk_Score"] = (
        risk_summary["Rain_Alerts"] * 2
        + risk_summary["Wind_Alerts"] * 2
        + risk_summary["Avg_Temp_Deviation"] * 3
        + risk_summary["Avg_Humidity_Deviation"] * 0.5
    ).round(2)

    risk_summary["Risk_Level"] = risk_summary[
        "Risk_Score"
    ].apply(
        lambda score:
        "High" if score >= 150
        else "Moderate" if score >= 75
        else "Low"
    )

    st.markdown("#### Location Risk Scores")

    risk_display = risk_summary.reset_index().rename(
        columns={
            "location_id": "Location",
            "Rain_Alerts": "Rain Alerts",
            "Wind_Alerts": "Wind Alerts",
            "Avg_Temp_Deviation": "Avg Temperature Deviation",
            "Avg_Humidity_Deviation": "Avg Humidity Deviation",
            "Risk_Score": "Risk Score",
            "Risk_Level": "Risk Level"
        }
    )

    st.dataframe(
        risk_display,
        hide_index=True,
        use_container_width=True
    )

    st.markdown("#### Risk Score Comparison")

    st.bar_chart(
        risk_summary[["Risk_Score"]],
        y_label="Relative Risk Score",
        x_label="Monitoring Location",
        use_container_width=True
    )

    st.caption(
        "Experimental portfolio indicator using weighted alert counts "
        "and average climate deviations. Thresholds are illustrative, "
        "not validated meteorological warning levels."
    )

else:
    st.info("No data available for risk intelligence.")

# LOCATION PERFORMANCE
# --------------------------------------------------

st.markdown(
    '<div class="section-title">📍 Location Performance</div>',
    unsafe_allow_html=True
)

kpi = view.groupby("location_id").agg(
    Avg_Temperature_C=("temperature_c", "mean"),
    Avg_Humidity_pct=("humidity_pct", "mean"),
    Avg_Wind_kmh=("wind_speed_kmh", "mean"),
    Avg_Comfort=("comfort_score", "mean"),
    High_Rain_Count=("rain_risk", lambda s: (s == "High").sum()),
    High_Wind_Count=("wind_risk", lambda s: (s == "High").sum())
).round(2)

# Create cleaner display names
kpi = kpi.rename(columns={
    "Avg_Temperature_C": "Temperature (°C)",
    "Avg_Humidity_pct": "Humidity (%)",
    "Avg_Wind_kmh": "Wind Speed (km/h)",
    "Avg_Comfort": "Comfort Index",
    "High_Rain_Count": "High Rain Alerts",
    "High_Wind_Count": "High Wind Alerts"
})

st.dataframe(
    kpi,
    use_container_width=True,
    hide_index=False,
    height=300,
    column_config={
        "Temperature (°C)": st.column_config.NumberColumn(
            format="%.2f °C"
        ),
        "Humidity (%)": st.column_config.NumberColumn(
            format="%.2f%%"
        ),
        "Wind Speed (km/h)": st.column_config.NumberColumn(
            format="%.2f km/h"
        ),
        "Comfort Index": st.column_config.NumberColumn(
            format="%.2f"
        ),
        "High Rain Alerts": st.column_config.NumberColumn(
            format="%d"
        ),
        "High Wind Alerts": st.column_config.NumberColumn(
            format="%d"
        )
    }
)

# --------------------------------------------------
# HOURLY ANALYSIS
# --------------------------------------------------

st.markdown(
    f'<div class="section-title">🕒 {selected_metric} by Hour</div>',
    unsafe_allow_html=True
)

hourly = (
    view.groupby("hour")[metric]
    .mean()
    .reindex(range(24))
)

st.line_chart(
    hourly,
    use_container_width=True
)

# --------------------------------------------------

# WEATHER RISK ANALYSIS
# --------------------------------------------------

st.divider()

st.markdown(
    '<div class="section-title">⚠️ Weather Risk Monitoring</div>',
    unsafe_allow_html=True
)

risk_by_location = view.groupby("location_id").agg(
    High_Rain_Risk=("rain_risk", lambda s: (s == "High").sum()),
    High_Wind_Risk=("wind_risk", lambda s: (s == "High").sum())
).reset_index()

# Risk summary cards
r1, r2 = st.columns(2)

with r1:
    st.metric(
        "🌧️ High Rain-Risk Records",
        f"{summary_rain:,}",
        help="Total observations classified as high rain risk."
    )

with r2:
    st.metric(
        "💨 High Wind-Risk Records",
        f"{summary_wind:,}",
        help="Total observations classified as high wind risk."
    )

st.markdown("#### 📍 Location-wise Risk Analysis")

risk_display = risk_by_location.rename(columns={
    "location_id": "Location",
    "High_Rain_Risk": "High Rain Alerts",
    "High_Wind_Risk": "High Wind Alerts"
})

st.dataframe(
    risk_display,
    hide_index=True,
    use_container_width=True,
    column_config={
        "Location": st.column_config.TextColumn("Location"),
        "High Rain Alerts": st.column_config.ProgressColumn(
            "High Rain Alerts",
            format="%d",
            min_value=0,
            max_value=max(1, int(risk_by_location["High_Rain_Risk"].max()))
        ),
        "High Wind Alerts": st.column_config.ProgressColumn(
            "High Wind Alerts",
            format="%d",
            min_value=0,
            max_value=max(1, int(risk_by_location["High_Wind_Risk"].max()))
        )
    }
)

st.markdown("#### 📊 Location Risk Comparison")

chart_data = risk_by_location.set_index("location_id")

st.bar_chart(
    chart_data,
    use_container_width=True,
    y_label="Number of High-Risk Observations",
    x_label="Monitoring Location"
)

st.caption(
    "Risk counts reflect high-risk observations within the selected filters."
)

# --------------------------------------------------
# RISK DISTRIBUTION
# --------------------------------------------------

st.markdown(
    '<div class="section-title">Risk Distribution</div>',
    unsafe_allow_html=True
)

rc1, rc2 = st.columns(2)

with rc1:
    st.markdown("#### Rain Risk")
    st.bar_chart(
        view["rain_risk"].value_counts().reindex(
            ["Low", "Medium", "High"], fill_value=0
        )
    )

with rc2:
    st.markdown("#### Wind Risk")
    st.bar_chart(
        view["wind_risk"].value_counts().reindex(
            ["Low", "Medium", "High"], fill_value=0
        )
    )

# --------------------------------------------------

# DOWNLOAD REPORTS
# --------------------------------------------------

st.divider()

st.markdown(
    '<div class="section-title">📥 Download Centre</div>',
    unsafe_allow_html=True
)

st.caption(
    "Export your climate observations and location-wise weather risk analysis."
)

d1, d2 = st.columns(2)

with d1:
    st.markdown("#### 📊 Filtered Climate Dataset")
    st.caption(
        f"{len(view):,} observations | CSV format"
    )

    st.download_button(
        label="⬇️ Download Climate Dataset",
        data=view.to_csv(index=False).encode("utf-8"),
        file_name="atmosync_filtered_data.csv",
        mime="text/csv",
        use_container_width=True
    )

with d2:
    st.markdown("#### ⚠️ Location Risk Report")
    st.caption(
        f"{len(risk_by_location):,} locations | CSV format"
    )

    st.download_button(
        label="⬇️ Download Risk Report",
        data=risk_by_location.to_csv(index=False).encode("utf-8"),
        file_name="atmosync_location_risk_report.csv",
        mime="text/csv",
        use_container_width=True
    )

st.caption(
    "Reports are generated using your currently selected dashboard filters."
)
