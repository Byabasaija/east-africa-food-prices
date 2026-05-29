# Model Benchmarks

All models below use the same standard test set: **January 2024 to April 2025 (16 months)**.

| Model | Train Period | Features | MAE (UGX/kg) | R² | Notes |
|---|---|---|---|---|---|
| Naive baseline (rolling mean 3) | N/A | N/A | 196 | -0.10 | Just average last 3 months |
| **RF v3 — maize CPI (current best)** | **2017–2023** | **8 (maize CPI)** | **224** | **-0.35** | **Best ML model — deploy next** |
| RF v1 — no CPI | 2006–2023 | 7 | 282 | -0.91 | More data but no CPI |
| RF v2 — broad food CPI (deployed) | 2017–2019 | 8 | 658 | 0.05 | Currently live — needs replacing |
| RF v3 — broad food CPI | 2017–2023 | 8 | 700 | -8.81 | Wrong CPI signal |
| Prophet (2006–2023, no CPI) | 2006–2023 | time series | 900 | -13.65 | Statistical model, not suitable |
| Original RF (old test period) | 2006–2019 | 7 | 193 | N/A | Tested on 2020–2022 only — not comparable |

## Key findings

1. **Maize-specific CPI (MAE 224) beats broad Food CPI (MAE 700)** — using the exact maize price index from UBOS instead of the general food basket made a 68% improvement.

2. **RF v3 with maize CPI (MAE 224) is now the best ML model** — just 28 UGX/kg above the naive baseline on the hardest test period we've used.

3. **The naive baseline (MAE 196) is still the ceiling** — beating it consistently requires more features and more price cycles in training data.

4. **The deployed model (RF v2, MAE 658) needs to be replaced** with RF v3 (maize CPI).

## What's needed to improve

- CPI data backfilled to 2006 (currently only available from July 2017)
- More price cycles in training data to teach the model that prices go up AND come down
- Additional features: rainfall, fuel prices, regional conflict data
