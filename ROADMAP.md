# Project Roadmap

## In Progress
- [ ] Backfill CPI data to 2006 — extract from UBOS PDF reports (one per month)

## Next Up — CPI Improvements
- [ ] Switch from broad Food CPI to maize-specific CPI
  - "Whole grain maize" (01.1.1.1.1) and "Maize Flour" (01.1.1.2.1) are in the Decomposed sheet of the UBOS Excel
  - Much stronger signal than the broad Food & Non-Alcoholic Beverages index
- [ ] Retrain model with maize-specific CPI once backfill is complete (2006–2025)
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
