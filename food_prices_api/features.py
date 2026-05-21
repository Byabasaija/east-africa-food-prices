import numpy as np


def compute_features(prices: list[float], month: int, year: int) -> dict:
    if len(prices) < 6:
        raise ValueError("Need at least 6 months of prices to compute features")

    last6 = prices[-6:]

    return {
        "price_lag_1": last6[-1],
        "price_lag_2": last6[-2],
        "price_lag_3": last6[-3],
        "rolling_mean_3": round(float(np.mean(last6[-3:])), 4),
        "rolling_mean_6": round(float(np.mean(last6)), 4),
        "month": month,
        "year": year,
    }
