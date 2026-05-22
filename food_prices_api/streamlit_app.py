import os

import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="Maize Price Predictor", page_icon="🌽")

st.title("🌽 Maize Price Predictor")
st.caption("Kampala Owino Market · Powered by historical price data")
st.markdown("Enter the last 6 months of Maize prices (UGX/kg), oldest first.")

col1, col2 = st.columns(2)

prices = []
labels = ["6 months ago", "5 months ago", "4 months ago", "3 months ago", "2 months ago", "Last month"]
for i, label in enumerate(labels):
    col = col1 if i < 3 else col2
    price = col.number_input(label, min_value=100, max_value=5000, value=800, step=10)
    prices.append(float(price))

st.divider()

col3, col4 = st.columns(2)
month = col3.selectbox(
    "Target month",
    list(range(1, 13)),
    index=5,
    format_func=lambda m: ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"][m-1],
)
year = col4.number_input("Target year", min_value=2020, max_value=2030, value=2024)

if st.button("Predict price", type="primary"):
    try:
        response = requests.post(
            f"{API_URL}/predict",
            json={"prices": prices, "month": month, "year": int(year)},
        )
        if response.status_code == 200:
            data = response.json()
            st.success(f"Predicted price: **{data['predicted_price']:,.0f} {data['currency']}/kg**")
            st.caption(f"{data['commodity']} · {data['market']}")
        else:
            st.error(f"API error: {response.text}")
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to API. Make sure the FastAPI server is running on port 8000.")
