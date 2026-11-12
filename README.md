AtmoSync — Micro-Climate Analytics

Environmental Intelligence & Weather Risk Monitoring Platform

## Dashboard Screenshots

### 1. Dashboard Overview
![Dashboard Overview](screenshots/dashboard-overview.png)

### 2. Climate Trends
![Climate Trends](screenshots/climate-trends.png)

### 3. Location Analysis
![Location Analysis](screenshots/location-analysis.png)

### 4. Weather Risk Monitoring
![Weather Risk](screenshots/weather-risk.png)


Project Overview

AtmoSync is a Python-based data analytics platform designed to process, analyze, and visualize micro-climate observations across multiple monitoring locations.

The platform transforms climate telemetry into meaningful insights through interactive dashboards, location-level comparisons, statistical anomaly detection, and experimental weather risk scoring.

Key Features

Interactive Climate Dashboard: Explore environmental observations using location and metric filters.

Executive Overview: Monitor total observations, average temperature, humidity, and comfort index.

Climate Trend Analysis: Visualize daily climate patterns.

Location Performance: Compare temperature, humidity, wind speed, and comfort across locations.

Weather Risk Monitoring: Identify high rain-risk and wind-risk observations.

Executive Climate Insights: Identify significant location-level climate patterns.

Climate Anomaly Detection: Flag unusual temperature and humidity observations using statistical thresholds.

Advanced Risk Intelligence: Calculate experimental location-level risk scores.

Data Export: Download filtered climate datasets and risk reports.

Technology Stack

Technology

Purpose

Python

Data processing and application logic

Pandas

Data cleaning and analysis

NumPy

Numerical operations

Matplotlib

Data visualization

Streamlit

Interactive dashboard

CSV

Dataset storage and exchange

AtmoSync/
├── analysis.py
├── dashboard.py
├── atmosync_raw.csv
├── atmosync_clean.csv
├── requirements.txt
├── README.md
├── screenshots/
│   ├── dashboard-overview.png
│   ├── climate-trends.png
│   ├── location-analysis.png
│   ├── weather-risk.png
│   └── anomaly-detection.png
└── outputs/

Analytical Methodology

Climate Trends

Daily averages are calculated using timestamp-based resampling.

Anomaly Detection

Observations more than two standard deviations from their location-specific mean are flagged for investigation.

Experimental Risk Intelligence

A weighted scoring method combines high rain-risk observations, high wind-risk observations, and average climate deviations.

These scores are exploratory portfolio indicators, not official meteorological warnings.

Installation and Setup

Clone the repository:

git clone https://github.com/Mr-Lopezzz/AtmoSync-Micro-Climate-Arbitrage-Analytics.git
cd AtmoSync-Micro-Climate-Arbitrage-Analytics

Create and activate a Linux virtual environment:

python3 -m venv .venv-linux
source .venv-linux/bin/activate

Install dependencies:

python -m pip install -r requirements.txt

Run the analysis:

python analysis.py

Launch the dashboard:

python -m streamlit run dashboard.py

Open the dashboard in your browser:

http://localhost:8501

Project Skills Demonstrated

Data cleaning and transformation

Exploratory data analysis

Statistical analysis

Interactive dashboard development

Time-series analytics

Anomaly detection

Risk-oriented data visualization

Python application development

Project Purpose

AtmoSync is an independent portfolio project demonstrating the application of Python-based analytics and interactive visualization to environmental telemetry.

Disclaimer

This project is a portfolio demonstration using synthetic or public-safe climate telemetry. Its anomaly detection and risk indicators are experimental and are not intended for operational weather forecasting or emergency decisions.
