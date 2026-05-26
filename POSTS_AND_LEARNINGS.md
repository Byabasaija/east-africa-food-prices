# Post Ideas & Learning Notes

Things worth writing about publicly or reading deeper into.

---

## 1. The Simple Baseline Beats the Fancy Model
**What happened:** Every model we tried — Random Forest (MAE 700), Prophet (MAE 1,169), RF with more data (MAE 900) — was beaten by simply averaging the last 3 months of prices (MAE 196). The naive baseline won every single comparison on recent data.

**Why it matters:** In time series forecasting, recent values are often the strongest signal. A complex model can overfit to training patterns and fail badly when those patterns shift — like the 2022–2023 price spike followed by a 2024 correction.

**Post angle:** "I tried Random Forest, then Prophet, then more data. A 3-line moving average beat all of them. Here's what I learned."

**Read more:** Look up "naive baselines in forecasting", "Makridakis M-competitions", "when simple models win"

---

## 2. Distribution Shift — When Your Test Data Lives in a Different World
**What happened:** The model trained on 2017–2023 prices (which included a COVID spike to 3000–3500 UGX/kg). In 2024, prices corrected back to 1700–2000. The model had no way to predict that correction — it just kept predicting "high."

**Why it matters:** This is one of the most common failure modes in production ML. The world changes; your model doesn't.

**Post angle:** "My food price model failed in 2024 — and it's not a bug, it's a lesson about distribution shift."

**Read more:** "Covariate shift in machine learning", "concept drift", "temporal train/test split"

---

## 3. Random Forest Can't Extrapolate
**What happened:** All 16 test predictions clustered around 2800 UGX/kg regardless of input. The model was essentially predicting the mean of the high-price training years.

**Why it matters:** Random Forest is a tree-based model — it can only predict values within the range it was trained on. It cannot extrapolate trends up or down beyond training data.

**Post angle:** "Why Random Forest fails at time series — and what to use instead."

**Read more:** "Random Forest extrapolation problem", "tree models vs time series", "why use Prophet/ARIMA for forecasting"

---

## 4. Data Quality Is the Real Bottleneck
**What happened:** WFP data had both Wholesale and Retail prices for the same month, sometimes multiple entries. This corrupted our lag features completely — the model was comparing same-month prices instead of month-over-month trends.

**Why it matters:** Garbage in, garbage out. One data cleaning decision (filter to Retail, average duplicates) changed the entire dataset shape.

**Post angle:** "Before you train your model, clean your data. Here's what bad data did to mine."

**Read more:** "Data cleaning for time series", "WFP food price data documentation"

---

## 5. Government Data Exists — You Just Have to Find It
**What happened:** Uganda's UBOS publishes monthly Consumer Price Index data going back to 2017 in Excel format, freely available. We added it as a feature and it improved the model even with a small dataset.

**Why it matters:** In Africa, people assume no data exists. It does — it's just not in a convenient API. Sometimes you have to download a spreadsheet from a government website.

**Post angle:** "Building AI for Africa: the data isn't missing, it's just inconvenient."

**Read more:** UBOS data portal, WFP VAM data, FAO GIEWS, World Bank Open Data

---

## 7. Your Test Set Tells the Truth — If You Let It
**What happened:** The original model had MAE 193 tested on 2020–2022. That looked great. But when we tested the same model on 2020–2025 (including the spike and correction), MAE jumped to 1,112. The model wasn't good — the test period was just too short and too convenient.

**Why it matters:** Choosing a test period that avoids hard data is the most common way to fool yourself in ML. Always test on the most recent data you have, including any disruptions.

**Post angle:** "My model had MAE 193. Then I changed the test period and it became 1,112. Here's what I was hiding from myself."

**Read more:** "Temporal validation in machine learning", "backtesting bias", "walk-forward validation"

---

## 8. Prophet Is a Tool, Not a Silver Bullet
**What happened:** Switched from Random Forest to Prophet expecting improvement. Prophet with trend gave MAE 1,169 — worse than Random Forest. Flat trend gave 1,187 — even worse. More training data gave 900 — still 4.5x worse than the naive baseline.

**Why it matters:** Prophet is excellent for business time series with strong seasonality (website traffic, retail sales). It struggles when the dominant signal is a structural break — a price spike caused by external shocks, not a repeating seasonal pattern.

**Post angle:** "Prophet is not always the answer for time series. Here's when it fails and why."

**Read more:** "When to use Prophet vs ARIMA", "structural breaks in time series", "Prophet limitations"

---

## 6. Why FastAPI and Not Just a Notebook
**What happened:** Intentional decision to wrap the model in a FastAPI endpoint rather than sharing a Colab notebook.

**Why it matters:** NGOs, traders, and agricultural planners can't run Python notebooks. A REST API means any app, any language, any device can use your model.

**Post angle:** "The difference between a data science project and a product is an API."

**Read more:** FastAPI docs, "ML model deployment best practices", "serving models in production"
