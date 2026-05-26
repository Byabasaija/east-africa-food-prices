# Project Roadmap

## In Progress
- [ ] Switch from Random Forest to Prophet for time series forecasting (notebook `06_prophet.ipynb`)

## Next Up
- [ ] Build a price database pipeline
  - PostgreSQL on Render or Supabase
  - Tables: `prices` (market, commodity, date, price, pricetype) and `food_cpi` (year, month, food_cpi)
  - Admin interface or script to upload new WFP CSV and UBOS Excel → inserts new rows
  - API queries database directly instead of reading CSVs from disk
  - UI becomes: pick market + target month → predict (no manual price entry)

## Future Features
- [ ] Rainfall data (CHIRPS) as a feature
- [ ] Fuel prices as a feature
- [ ] Regional conflict data as a feature
- [ ] Expand to more markets beyond Owino, Kampala
- [ ] Expand to more commodities beyond Maize
- [ ] Automate CPI updates (scheduled job that pulls new UBOS data monthly)
- [ ] Automate price updates (pull from WFP API or scrape when available)

## Data Gaps to Address
- [ ] CPI data before July 2017 — extract from UBOS PDF reports to extend training window back to 2006
