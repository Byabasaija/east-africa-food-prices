# East Africa Food Price Prediction

An end-to-end ML project predicting maize prices at Owino market, Kampala, Uganda — from raw WFP data to a production FastAPI deployed on HuggingFace.

**The honest finding:** A 3-month rolling average (MAE 196 UGX/kg) beats every ML model we tried. This README documents why, and what we built along the way.

---

## Results

| Model | Train Rows | MAE (UGX/kg) | Notes |
|-------|-----------|-------------|-------|
| Naive baseline (rolling mean 3) | — | **196** | Hard to beat |
| RF v6 — EA prices + feature eng. | 143 | **216** | Best honest ML · deployed |
| RF v4 — global maize + FX | 155 | 223 | No CPI dependency |
| RF v3 — maize CPI (leaky) | 65 | 224 | Uses same-month CPI — invalid in production |
| RF v3 — CPI lag-1 (honest) | 65 | 268 | What v3 actually does in production |
| RF v5 — real prices (deflated) | 65 | 263 | Deflation approach |
| Prophet | — | 1,169 | Trend extrapolation fails on 2024 correction |

Test set: January 2024 – April 2025 (16 months). See [MODEL_BENCHMARKS.md](MODEL_BENCHMARKS.md) for full details.

---

## Structure

```
food_prices_model/
  01_exploration.ipynb        # EDA — price distributions, seasonality
  02_feature_engineering.ipynb
  03_model_training.ipynb     # v1 baseline
  04_cpi_feature.ipynb        # broad food CPI experiment
  05_retrain_full.ipynb       # v3 — maize-specific CPI + leakage test
  06_prophet.ipynb            # Prophet experiment (MAE 1,169)
  07_cpi_backfill.ipynb       # Attempted UBOS CPI backfill to 2006
  08_retrain_v4.ipynb         # v4 — World Bank global maize + FX
  09_retrain_v5.ipynb         # v5 — real prices (CPI deflation)
  10_retrain_v6.ipynb         # v6 — EA regional prices + feature engineering

food_prices_api/
  main.py                     # FastAPI — loads v6, fetches EA/global maize + FX
  features.py                 # Feature computation (12-month window)
  models.py                   # Pydantic request/response models
```

---

## Data

All datasets published to HuggingFace:

- **Prices:** [`byabasaija/uganda-maize-prices`](https://huggingface.co/datasets/byabasaija/uganda-maize-prices) — WFP monthly retail prices, Owino market, 2010–2025
- **CPI:** [`byabasaija/uganda-food-cpi`](https://huggingface.co/datasets/byabasaija/uganda-food-cpi) — UBOS maize-specific CPI, July 2017–present
- **Model:** [`byabasaija/uganda-food-prices-model`](https://huggingface.co/byabasaija/uganda-food-prices-model) — v6 Random Forest

External sources fetched at runtime:
- World Bank Pink Sheet — global maize price (USD/tonne, monthly, 1960–present)
- WFP HDX — Kenya (Nairobi) and Tanzania (Dar es Salaam) maize prices
- World Bank API — UGX/USD annual exchange rate

---

## API

```bash
POST /predict
{
  "prices": [1800, 1750, 1900, 2000, 1850, 1700, 1650, 1800, 1900, 2100, 2000, 1950],
  "month": 7,
  "year": 2025
}
```

Requires **12 months** of historical prices (for lag_6 and lag_12 features).

Returns:
```json
{
  "predicted_price": 1923.45,
  "currency": "UGX",
  "unit": "per kg",
  "commodity": "Maize",
  "market": "Owino, Kampala"
}
```

---

## Key Learnings

**1. Data leakage is subtle.**
v3 used the same month's CPI it was predicting (MAE 224). Fixed to CPI lag-1, MAE jumped to 268. The 224 was never real. Always ask: at prediction time, is this feature actually available?

**2. Random Forest cannot extrapolate.**
The 2022–2023 price spike followed by a sharp 2024 correction is the core challenge. RF trained on "high prices" keeps predicting high when prices have already fallen. No amount of feature engineering fixes this — it's structural.

**3. Prophet extrapolates the wrong direction.**
It fit an upward trend to 2017–2023 and projected it forward. MAE 1,169 — six times worse than a rolling average.

**4. 177 monthly rows is not enough for ML to win.**
The naive baseline wins because last month's price is the best predictor of next month's price on this dataset. This mirrors the Makridakis M-competition findings: on short time series with high autocorrelation, simple baselines beat ML.

**5. The CPI backfill problem.**
UBOS rebased their CPI in 2016–2017 and introduced maize-specific commodity codes then. No maize CPI exists before July 2017, capping CPI-dependent models to 65 training rows.

---

## What's Next

This project is concluded. The next project in this domain: an **agricultural AI extension worker** — a RAG system trained on MAAIF Uganda crop guides and FAO extension manuals, wrapped in FastAPI. Better data characteristics (text, abundant), genuinely useful to the same audience (farmers, NGOs, planners).

---

## Full Writeup

→ [I Built 6 ML Models to Predict Uganda Maize Prices. A Rolling Average Beat All of Them.](https://vcard-portfolio-8xncnqjyj-byabasaijas-projects.vercel.app/post/i-built-6-ml-models-to-predict-uganda-maize-prices)
