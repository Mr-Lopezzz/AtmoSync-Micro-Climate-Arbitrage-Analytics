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
    /* Main application */
    .stApp {
        background: #0B1220;
        color: #E5E7EB;
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #111B2E;
        border-right: 1px solid #26364D;
    }

    [data-testid="stSidebar"] h2 {
        color: #F8FAFC;
        font-size: 20px;
    }

    [data-testid="stSidebar"] label {
        color: #CBD5E1 !important;
    }

    /* Main branding */
    .main-title {
        font-size: 38px;
        font-weight: 800;
        color: #F8FAFC;
        letter-spacing: -1.5px;
        margin-bottom: 2px;
    }

    .subtitle {
        color: #38BDF8;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 2px;
        margin-bottom: 30px;
    }

    /* Section headings */
    .section-title {
        font-size: 21px;
        font-weight: 750;
        color: #F1F5F9;
        margin-top: 22px;
        margin-bottom: 16px;
    }

    /* KPI cards */
    div[data-testid="stMetric"] {
        background: linear-gradient(
            145deg, #172942, #111C30
        );
        border: 1px solid #29415D;
        border-radius: 14px;
        padding: 20px;
        min-height: 115px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.15);
    }

    div[data-testid="stMetricLabel"] {
        color: #A8B9CE;
        font-size: 13px;
        font-weight: 600;
    }

    div[data-testid="stMetricValue"] {
        color: #38BDF8;
        font-size: 28px;
        font-weight: 800;
    }

    /* Charts and tables */
    [data-testid="stDataFrame"] {
        border: 1px solid #263B55;
        border-radius: 12px;
        overflow: hidden;
    }

    [data-testid="stPlotlyChart"],
    [data-testid="stVegaLiteChart"] {
        border-radius: 12px;
    }

    /* Download buttons */
    div.stDownloadButton > button {
        background: linear-gradient(
            90deg, #0879D1, #0891B2
        );
        color: white;
        border: none;
        border-radius: 9px;
        min-height: 44px;
        font-weight: 700;
        transition: 0.2s ease;
    }

    div.stDownloadButton > button:hover {
        background: #0EA5E9;
        color: white;
        border: none;
    }

    /* General buttons */
    .stButton > button {
        border-radius: 9px;
        font-weight: 600;
    }

    /* Dividers */
    hr {
        border-color: #26364D;
        margin-top: 25px;
        margin-bottom: 25px;
    }

    /* Captions */
    [data-testid="stCaptionContainer"] {
        color: #94A3B8;
    }

    /* Select boxes and multiselects */
    [data-baseweb="select"] > div {
        background-color: #17243A;
        border-color: #344861;
        border-radius: 8px;
    }

    /* Responsive spacing */
    @media (max-width: 768px) {
        .main-title {
            font-size: 30px;
        }

        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)



# --------------------------------------------------
# PROFESSIONAL HEADER
# --------------------------------------------------

st.markdown("""
<div class="header-card">
    <div style="display:flex; justify-content:space-between;
                align-items:center; flex-wrap:wrap; gap:12px;">
        <div>
            <div class="main-title">🌦️ AtmoSync</div>
            <div class="subtitle">
                MICRO-CLIMATE INTELLIGENCE PLATFORM
            </div>
        </div>
        <div class="status-label">
            ● ANALYTICS SYSTEM ACTIVE
        </div>
    </div>
    <div class="header-description">
        Environmental monitoring, climate analytics,
        anomaly detection and location-based weather risk intelligence.
    </div>
</div>
""", unsafe_allow_html=True)

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
# EXECUTIVE KPI CARDS — ATMOSYNC 2.0
# --------------------------------------------------

st.markdown(
    '<div class="section-title">Executive Overview</div>',
    unsafe_allow_html=True
)

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

kpi1.metric(
    "Total Observations",
    f"{len(view):,}",
    help="Total climate observations in the selected locations."
)

kpi2.metric(
    "Monitoring Locations",
    f"{view['location_id'].nunique():,}",
    help="Number of selected monitoring locations."
)

kpi3.metric(
    "Average Temperature",
    f"{view['temperature_c'].mean():.1f} °C",
    help="Average recorded temperature."
)

kpi4.metric(
    "Average Humidity",
    f"{view['humidity_pct'].mean():.1f}%",
    help="Average relative humidity."
)

kpi5.metric(
    "Comfort Index",
    f"{view['comfort_score'].mean():.1f}/100",
    help="Average calculated environmental comfort score."
)

st.divider()


# --------------------------------------------------
# PROFESSIONAL CLIMATE TREND
# --------------------------------------------------

trend = (
    view.set_index("timestamp")[metric]
    .resample("D")
    .mean()
    .dropna()
)

trend_chart = trend.rename("Value").reset_index()

st.caption(
    f"Daily average {selected_metric.lower()} across selected monitoring locations"
)

st.line_chart(
    trend_chart,
    x="timestamp",
    y="Value",
    x_label="Monitoring Date",
    y_label=selected_metric,
    color="#38BDF8",
    height=380,
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
   
        # Rank locations by weather risk
    risk_summary = risk_summary.sort_values(
        by="Risk_Score",
        ascending=False
    )

    risk_summary.insert(
        0,
        "Risk Rank",
        range(1, len(risk_summary) + 1)
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
# Rank locations by average comfort score
kpi = kpi.sort_values(
    by="Comfort Index",
    ascending=False
)

kpi.insert(
    0,
    "Performance Rank",
    range(1, len(kpi) + 1)
)

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

# Comfort Index Comparison Chart
st.markdown("### 🏆 Comfort Index by Location")

st.bar_chart(
    kpi["Comfort Index"],
    horizontal=True,
    use_container_width=True
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
    '<div class="section-title">Weather Risk Monitoring</div>',
    unsafe_allow_html=True
)

st.caption(
    "Location-wise monitoring of high rainfall and wind risk alerts."
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

st.caption("Alert counts by monitoring location. Higher values indicate more frequent weather-risk events.")

st.dataframe(
    risk_display,
    hide_index=True,
    use_container_width=True,
    column_config={
        "Location": st.column_config.TextColumn(
            "Monitoring Location"
        ),
        "High Rain Alerts": st.column_config.ProgressColumn(
            "High Rain Alerts",
            format="%d",
            min_value=0,
            max_value=max(
                1, int(risk_display["High Rain Alerts"].max())
            )
        ),
        "High Wind Alerts": st.column_config.ProgressColumn(
            "High Wind Alerts",
            format="%d",
            min_value=0,
            max_value=max(
                1, int(risk_display["High Wind Alerts"].max())
            )
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

st.caption(
    "Distribution of weather-risk events across monitoring locations."
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
    '<div class="section-title">Download Centre</div>',
    unsafe_allow_html=True
)

st.caption(
    "Export cleaned climate data and analytical outputs for further analysis."
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
st.divider()

st.markdown(
    """
    <div style="text-align:center; padding:15px; color:#94A3B8;">
        <strong>AtmoSync</strong> | Micro-Climate Intelligence Platform
        <br>
        <small>Built with Python, Pandas and Streamlit | Portfolio Analytics Project</small>
    </div>
    """,
    unsafe_allow_html=True
)
