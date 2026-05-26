# Model Benchmarks

| Model | Train Period | Test Period | MAE (UGX/kg) | R² | Notes |
|---|---|---|---|---|---|
| Original RF (7 features, no CPI) | 2006–2019 | 2020–2022 | 193 | N/A | Looked good — but test period was pre-spike |
| Original RF (7 features, no CPI) | 2006–2019 | 2020–2025 | 1,112 | -2.34 | Breaks down badly on spike + correction |
| Naive baseline (rolling mean 3) | N/A | 2024–2025 | 196 | -0.10 | Best performer on recent data |
| RF v2 (8 features, with CPI) | 2017–2019 | 2024–2025 | 658 | 0.05 | Currently deployed — best ML model on recent data |
| RF v3 (8 features, clean retail) | 2017–2023 | 2024–2025 | 700 | -8.81 | Clean data but still worse than naive |
| Prophet (trend, with CPI) | 2017–2023 | 2024–2025 | 1,169 | -24.18 | Aggressively extrapolates upward trend |
| Prophet (flat trend, with CPI) | 2017–2023 | 2024–2025 | 1,187 | -24.89 | Flat trend doesn't help |
| Prophet (2006–2023, no CPI) | 2006–2023 | 2024–2025 | 900 | -13.65 | More data doesn't fix the problem |

## Key findings

1. **The original model's MAE 193 was misleading** — it was tested on 2020–2022, before the 2022–2023 price spike. On the full 2020–2025 period it gives MAE 1,112.

2. **The 2022–2023 price spike is a structural break** that broke every model. Any model trained through the spike extrapolates high prices into 2024, but prices actually corrected downward.

3. **The naive rolling mean (MAE 196) is the best performer on recent data** — it doesn't try to predict trends, just says "next month ≈ average of last 3 months."

4. **RF v2 with CPI (MAE 658) is the best ML model on recent data** and is currently deployed.

## What's needed to improve

- CPI data backfilled to 2006 (currently only available from July 2017)
- More price cycles in training data to teach the model that prices go up AND come down
- Additional features: rainfall, fuel prices, regional conflict data
