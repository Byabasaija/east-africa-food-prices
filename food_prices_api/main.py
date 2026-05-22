from contextlib import asynccontextmanager

import joblib
import pandas as pd
from fastapi import FastAPI
from huggingface_hub import hf_hub_download

from features import compute_features
from models import PredictRequest, PredictResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    model_path = hf_hub_download(
        repo_id="byabasaija/uganda-food-prices-model",
        filename="maize_price_model.pkl",
    )
    app.state.model = joblib.load(model_path)
    yield


app = FastAPI(title="Maize Price Prediction API", lifespan=lifespan)

FEATURE_COLS = [
    "price_lag_1", "price_lag_2", "price_lag_3",
    "rolling_mean_3", "rolling_mean_6",
    "month", "year",
]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    features = compute_features(request.prices, request.month, request.year)
    X = pd.DataFrame([[features[col] for col in FEATURE_COLS]], columns=FEATURE_COLS)
    prediction = app.state.model.predict(X)[0]
    return PredictResponse(predicted_price=round(float(prediction), 2))
