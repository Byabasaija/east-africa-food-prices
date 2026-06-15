import io
import warnings
from contextlib import asynccontextmanager

import joblib
import numpy as np
import pandas as pd
import requests
from fastapi import FastAPI
from huggingface_hub import hf_hub_download

from features import compute_features
from models import PredictRequest, PredictResponse

warnings.filterwarnings("ignore")

FEATURE_COLS = [
    "price_lag_1", "price_lag_2", "price_lag_3",
    "price_lag_6", "price_lag_12",
    "rolling_mean_3", "rolling_mean_6",
    "price_momentum",
    "sin_month", "cos_month",
    "year",
    "regional_maize_usd", "fx_ugx_usd",
]


def _fetch_ea_maize() -> pd.Series:
    """Monthly EA maize price in USD/kg. Kenya primary, Tanzania secondary.
    Returns a Series indexed by (year, month) tuples."""
    ke_url = "https://data.humdata.org/dataset/e0d3fba6-f9a2-45d7-b949-140c455197ff/resource/517ee1bf-2437-4f8c-aa1b-cb9925b9d437/download/wfp_food_prices_ken.csv"
    tz_url = "https://data.humdata.org/dataset/5090d858-a300-49fe-a953-4ec4e3526fc2/resource/2ff38c1a-a8f7-45b2-9209-090200c859da/download/wfp_food_prices_tza.csv"

    def _load(url, commodity, unit, market, divisor=1):
        try:
            df = pd.read_csv(io.StringIO(requests.get(url, timeout=30, verify=False).text))
            sub = df[(df["commodity"] == commodity) & (df["unit"] == unit) & (df["market"] == market)]
            sub = sub[["date", "usdprice"]].copy()
            sub["date"] = pd.to_datetime(sub["date"])
            sub["usdprice"] = sub["usdprice"] / divisor
            sub["year"] = sub["date"].dt.year
            sub["month"] = sub["date"].dt.month
            return sub.set_index(["year", "month"])["usdprice"]
        except Exception:
            return pd.Series(dtype=float)

    ke = _load(ke_url, "Maize", "KG", "Nairobi")
    tz = _load(tz_url, "Maize", "100 KG", "Dar Es Salaam", divisor=100)

    combined = pd.concat([ke, tz], axis=1, keys=["ke", "tz"])
    return combined.mean(axis=1)


def _fetch_global_maize() -> pd.Series:
    """World Bank Pink Sheet monthly maize price in USD/kg.
    Returns a Series indexed by (year, month) tuples."""
    url = "https://thedocs.worldbank.org/en/doc/5d903e848db1d1b83e0ec8f744e55570-0350012021/related/CMO-Historical-Data-Monthly.xlsx"
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    raw = pd.read_excel(io.BytesIO(resp.content), sheet_name="Monthly Prices", header=4)
    raw = raw.rename(columns={"Unnamed: 0": "date"})
    raw = raw[raw["date"].notna() & raw["date"].astype(str).str.match(r"\d{4}M\d{2}")]
    raw["date"] = pd.to_datetime(raw["date"].astype(str).str.replace("M", "-"), format="%Y-%m")
    raw["year"] = raw["date"].dt.year
    raw["month"] = raw["date"].dt.month
    raw["usd_kg"] = raw["Maize"] / 1000
    return raw.dropna(subset=["usd_kg"]).set_index(["year", "month"])["usd_kg"]


def _fetch_fx() -> pd.Series:
    """World Bank annual UGX/USD exchange rate. Returns a Series indexed by year."""
    resp = requests.get(
        "https://api.worldbank.org/v2/country/UGA/indicator/PA.NUS.FCRF",
        params={"format": "json", "per_page": 100},
        timeout=30,
    )
    resp.raise_for_status()
    records = [r for r in resp.json()[1] if r["value"] is not None]
    return pd.Series(
        {int(r["date"]): r["value"] for r in records},
        name="fx_ugx_usd",
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    model_path = hf_hub_download(
        repo_id="byabasaija/uganda-food-prices-model",
        filename="maize_price_model_v6.pkl",
    )
    app.state.model = joblib.load(model_path)
    app.state.ea_maize = _fetch_ea_maize()
    app.state.global_maize = _fetch_global_maize()
    app.state.fx = _fetch_fx()
    yield


app = FastAPI(title="Maize Price Prediction API — v6", lifespan=lifespan)


def _regional_maize_usd(year: int, month: int) -> float:
    """EA price for (year, month) if available, else global fallback."""
    key = (year, month)
    ea = app.state.ea_maize
    if key in ea.index and not np.isnan(ea[key]):
        return float(ea[key])
    # Fallback: global maize
    gm = app.state.global_maize
    if key in gm.index:
        return float(gm[key])
    # Last known value
    return float(gm.iloc[-1])


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    features = compute_features(request.prices, request.month, request.year)
    features["regional_maize_usd"] = _regional_maize_usd(request.year, request.month)
    features["fx_ugx_usd"] = float(
        app.state.fx.get(request.year, app.state.fx.iloc[-1])
    )
    X = pd.DataFrame([[features[col] for col in FEATURE_COLS]], columns=FEATURE_COLS)
    prediction = app.state.model.predict(X)[0]
    return PredictResponse(predicted_price=round(float(prediction), 2))
