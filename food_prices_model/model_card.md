---
license: mit
language:
- en
tags:
- food-prices
- uganda
- forecasting
- agriculture
---

# Uganda Maize Price Prediction Model

Predicts next month's maize retail price at Owino market, Kampala, Uganda.

## Model Details

- **Algorithm**: Random Forest (200 trees)
- **Version**: v3
- **Train period**: July 2017 – December 2023
- **Test period**: January 2024 – April 2025
- **MAE**: 224 UGX/kg on test set

## Features

| Feature | Description |
|---|---|
| price_lag_1 | Retail price last month |
| price_lag_2 | Retail price 2 months ago |
| price_lag_3 | Retail price 3 months ago |
| rolling_mean_3 | Average price over last 3 months |
| rolling_mean_6 | Average price over last 6 months |
| month | Calendar month (seasonality) |
| year | Calendar year (trend) |
| food_cpi | Uganda maize-specific CPI (UBOS) |
## Training Data

- **Prices**: [byabasaija/uganda-maize-prices](https://huggingface.co/datasets/byabasaija/uganda-maize-prices) — WFP food price data, Owino market, retail prices averaged per month
- **CPI**: [byabasaija/uganda-food-cpi](https://huggingface.co/datasets/byabasaija/uganda-food-cpi) — Uganda maize-specific CPI from UBOS (whole grain maize + maize flour index)

## Performance

| Model | MAE (UGX/kg) |
|---|---|
| Naive baseline (rolling mean 3) | 196 |
| **This model (v3, maize CPI)** | **224** |
| V1 (no CPI) | 282 |
| V2 (broad food CPI) | 658 |

## Usage

```python
import joblib
import pandas as pd
from huggingface_hub import hf_hub_download

model_path = hf_hub_download(repo_id="byabasaija/uganda-food-prices-model", filename="maize_price_model_v3.pkl")
model = joblib.load(model_path)
```

## Limitations

- Trained on Owino market (Kampala) retail prices only
- CPI data available from July 2017 — training window limited
- Does not account for rainfall, fuel prices, or exchange rates (planned)
- Predicts one month ahead only

## Built By

Pascal Byabasaija
