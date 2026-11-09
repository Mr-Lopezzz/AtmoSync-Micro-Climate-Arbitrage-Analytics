# AtmoSync Data Dictionary

| Column | Meaning | Unit |
|---|---|---|
| timestamp | Observation timestamp | datetime |
| location_id | Sensor/location identifier | text |
| latitude | Location latitude | degrees |
| longitude | Location longitude | degrees |
| temperature_c | Air temperature | °C |
| humidity_pct | Relative humidity | % |
| wind_speed_kmh | Wind speed | km/h |
| precipitation_mm | Precipitation amount | mm |
| pressure_hpa | Atmospheric pressure | hPa |
| solar_wm2 | Solar radiation proxy | W/m² |
| hour | Hour extracted from timestamp | 0–23 |
| date | Calendar date | date |
| comfort_score | Engineered environmental suitability indicator | 0–100 |
| rain_risk | Rain category derived from precipitation | Low/Medium/High |
| wind_risk | Wind category derived from wind speed | Low/Medium/High |
