# AtmoSync — Micro-Climate Analytics

### Environmental Intelligence & Weather Risk Monitoring Platform

## Project Overview

AtmoSync is a data analytics platform designed to process, analyze, and visualize micro-climate observations across multiple monitoring locations.

The platform transforms climate telemetry into meaningful insights through interactive dashboards, location-level comparisons, statistical anomaly detection, and experimental weather risk scoring.

## Key Features

- **Interactive Climate Dashboard:** Explore environmental observations using location and metric filters.
- **Executive Overview:** Monitor total observations, average temperature, humidity, and comfort index.
- **Climate Trend Analysis:** Visualize daily climate patterns.
- **Location Performance:** Compare temperature, humidity, wind speed, and comfort across locations.
- **Weather Risk Monitoring:** Identify high rain-risk and wind-risk observations.
- **Executive Climate Insights:** Automatically identify significant location-level climate patterns.
- **Climate Anomaly Detection:** Flag unusual temperature and humidity observations using a statistical threshold.
- **Advanced Risk Intelligence:** Calculate experimental location-level risk scores.
- **Data Export:** Download filtered climate datasets and risk reports.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Data processing and application logic |
| Pandas | Data cleaning and analysis |
| NumPy | Numerical operations |
| Matplotlib | Data visualization |
| Streamlit | Interactive dashboard |
| CSV | Dataset storage and exchange |

## Project Architecture

1. Raw climate observations are collected in CSV format.
2. Python processes and cleans the observations.
3. Processed data is stored in a cleaned CSV dataset.
4. Analytics scripts generate summary statistics and visual outputs.
5. Streamlit presents interactive climate analytics.
6. Statistical models identify unusual observations and calculate experimental risk scores.

## Analytical Methodology

### Climate Trends
Daily averages are calculated using timestamp-based resampling.

### Anomaly Detection
Observations more than two standard deviations from their location-specific mean are flagged for further investigation.

### Experimental Risk Intelligence
A weighted scoring method combines high rain-risk observations, high wind-risk observations, and average climate deviations.

These scores are exploratory portfolio indicators, not official meteorological warnings.

## Running the Application

Activate the Linux virtual environment:

```bash
source .venv-linux/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the analysis:

```bash
python analysis.py
```

Launch the dashboard:

```bash
python -m streamlit run dashboard.py
```

Open:

```text
http://localhost:8501
```

## Project Purpose

AtmoSync demonstrates practical skills in:

- Data cleaning and transformation
- Exploratory data analysis
- Statistical analysis
- Interactive dashboard development
- Time-series analytics
- Anomaly detection
- Risk-oriented data visualization
- Python application development

## Disclaimer
This project is a portfolio demonstration using synthetic or public-safe climate telemetry. Its anomaly and risk indicators are experimental and are not intended for operational weather forecasting or emergency decisions.
