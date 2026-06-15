# Model Benchmarks

All models use the same test set: **January 2024 to April 2025 (16 months)**.

| Model | Train Period | Train Rows | MAE (UGX/kg) | R² | Notes |
|---|---|---|---|---|---|
| Naive baseline (rolling mean 3) | N/A | N/A | **196** | -0.10 | Average of last 3 months — hard to beat |
| **RF v6 — EA prices + feature eng. (deployed)** | **2010–2023** | **143** | **216** | -1.13 | **Current production model** |
| RF v4 — global maize + FX | 2010–2023 | 155 | 223 | -1.36 | No CPI dependency |
| RF v3 — maize CPI (leaky) | 2017–2023 | 65 | 224 | -0.35 | Uses same-month CPI — not valid in production |
| RF v3 — maize CPI lag-1 (honest) | 2017–2023 | 65 | 268 | — | What v3 actually does in production |
| RF v5 — real prices (deflated) | 2017–2023 | 65 | 263 | — | Deflation approach — worse than nominal |
| RF v1 — no CPI | 2006–2023 | — | 282 | -0.91 | More data but no economic features |
| RF v2 — broad food CPI (old deployed) | 2017–2019 | — | 658 | 0.05 | Wrong CPI signal — replaced |
| Prophet — time series (no CPI) | 2006–2023 | — | 900–1169 | -13 to -24 | Trend extrapolation failure on 2024 correction |

## Key findings

1. **The naive baseline wins.** Rolling mean of the last 3 months (MAE 196) beats every ML model. This is consistent with Makridakis M-competition findings: on short time series with high autocorrelation, simple baselines outperform ML.

2. **v3's 224 MAE was leaky.** It used the same month's CPI that it was predicting — unavailable at prediction time. The honest v3 (CPI lag-1) scores 268. v6 (216) is the best *honest* ML model.

3. **The 2024 structural break is the core challenge.** Prices corrected sharply after the 2022–2023 spike. Random Forest cannot extrapolate below its training range. Prophet extrapolated the upward trend further. The naive baseline survived by adjusting month-by-month.

4. **177 monthly rows is not enough for ML to consistently win.** The gap to the naive baseline (20 UGX/kg for v6) requires either daily price data or years more collection.

5. **East African regional prices + feature engineering (v6) helped.** Replacing Chicago CME price with Kenya/Tanzania WFP prices + adding lag_6, lag_12, momentum, and cyclical month encoding improved MAE from 223 → 216. The EA data ends March 2022, so the test period fell back to global price.

## v6 Feature Set (current production)

| Feature | Description |
|---|---|
| price_lag_1/2/3 | Last 1, 2, 3 months price |
| price_lag_6 | 6 months ago (captures bi-annual harvest cycle) |
| price_lag_12 | 12 months ago (same month last year) |
| rolling_mean_3/6 | Average of last 3 and 6 months |
| price_momentum | price_lag_1 - price_lag_2 (direction of movement) |
| sin_month, cos_month | Cyclical month encoding |
| year | Long-term trend |
| regional_maize_usd | EA maize price (Kenya/Tanzania) — global fallback when unavailable |
| fx_ugx_usd | Annual UGX/USD exchange rate (World Bank) |
