# Uganda Food Price Prediction

A machine learning project that predicts next month's Maize price at Owino market, Kampala, using 16 years of historical WFP data.

Built as a learning project to understand core ML concepts hands-on.

## What it does

Trains a Random Forest model on historical price data to predict the next month's Maize price (UGX/kg) at Owino market, Kampala.

**Results:** Test MAE of 193 UGX/kg (~20% of average price) on 2020–2022 data. The test period covers COVID-era price shocks which the model had never seen during training — a realistic challenge for any classical ML model.

## Project structure

```
01_exploration.ipynb          # Data exploration and seasonality analysis
02_feature_engineering.ipynb  # Feature engineering — lag, rolling mean, calendar features
03_model_training.ipynb       # Model training, evaluation, and visualization
data/maize_owino_features.csv # Engineered dataset
wfp_food_prices_uga.csv       # Raw WFP Uganda food prices data
price_prediction_results.png  # Predicted vs actual chart + feature importance
```

## ML concepts covered

- Supervised regression
- Feature engineering (lag features, rolling means, calendar features)
- Time-based train/test split
- Random Forest ensemble model
- MAE evaluation
- Overfitting
- Feature importance

## Setup

```bash
uv sync
jupyter lab
```

Then run the notebooks in order: `01` → `02` → `03`.

## Data

Source: [WFP Food Prices](https://data.humdata.org/dataset/wfp-food-prices-for-uganda) — 25,526 rows of food price observations across Uganda markets from 2006 to 2022.

## Key findings

- `price_lag_1` (last month's price) is the strongest predictor
- Seasonality (harvest cycles) is a real signal the model picks up
- COVID-era disruptions (2020–2022) are hard to predict from pre-COVID training data
