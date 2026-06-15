# Project Roadmap

## In Progress
- [ ] Backfill CPI data to 2006 — downloading UBOS Excel/PDF reports and extracting maize CPI per month

## Done — CPI Improvements
- [x] Switch from broad Food CPI to maize-specific CPI
  - "Whole grain maize" (01.1.1.1.1) and "Maize Flour" (01.1.1.2.1) from the Decomposed sheet of the UBOS Excel
  - MAE dropped from 658 → 224 vs naive baseline 196
- [x] Retrain model v3 with maize-specific CPI (2017–2023 train, 2024–2025 test)

## Next Up — CPI Improvements
- [ ] Add FX (USD/UGX) as a feature — Bank of Uganda historical data, goes back decades

## Next Up — Data Pipeline
- [ ] Build a price database pipeline
  - Tables: `prices` (market, commodity, date, price, pricetype) and `food_cpi` (year, month, food_cpi)
  - Admin endpoints: POST /admin/upload-prices and POST /admin/upload-cpi
  - API queries database directly instead of downloading from HuggingFace at startup
  - UI becomes: pick market + target month → predict (no manual price entry)

## Future Features
- [ ] Rainfall data (CHIRPS) as a feature
- [ ] Fuel prices as a feature
- [ ] Fertilizer prices as a feature
- [ ] Regional conflict data as a feature
- [ ] Expand to more markets beyond Owino, Kampala
- [ ] Expand to more commodities — each commodity gets its own model (beans, rice, cassava)
- [ ] Automate CPI and price updates via scheduled jobs

## Commodity Strategy
- Focus on Maize until the pipeline and features are solid
- The maize model is the blueprint — same architecture reused per commodity
- Each commodity has different price drivers (beans = weather, rice = imports, etc.)
