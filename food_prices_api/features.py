import numpy as np


def compute_features(prices: list[float], month: int, year: int) -> dict:
    if len(prices) < 12:
        raise ValueError("Need at least 12 months of prices to compute features")

    last12 = prices[-12:]

    return {
        "price_lag_1":   last12[-1],
        "price_lag_2":   last12[-2],
        "price_lag_3":   last12[-3],
        "price_lag_6":   last12[-6],
        "price_lag_12":  last12[-12],
        "rolling_mean_3": round(float(np.mean(last12[-3:])), 4),
        "rolling_mean_6": round(float(np.mean(last12[-6:])), 4),
        "price_momentum": last12[-1] - last12[-2],
        "sin_month": float(np.sin(2 * np.pi * month / 12)),
        "cos_month": float(np.cos(2 * np.pi * month / 12)),
        "year": year,
    }
