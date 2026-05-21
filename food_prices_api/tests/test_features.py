import pytest
from features import compute_features


def test_lag_features():
    prices = [700.0, 720.0, 750.0, 780.0, 800.0, 820.0]
    features = compute_features(prices, month=4, year=2024)
    assert features["price_lag_1"] == 820.0
    assert features["price_lag_2"] == 800.0
    assert features["price_lag_3"] == 780.0


def test_rolling_mean_3():
    prices = [700.0, 720.0, 750.0, 780.0, 800.0, 820.0]
    features = compute_features(prices, month=4, year=2024)
    assert features["rolling_mean_3"] == round((780.0 + 800.0 + 820.0) / 3, 4)


def test_rolling_mean_6():
    prices = [700.0, 720.0, 750.0, 780.0, 800.0, 820.0]
    features = compute_features(prices, month=4, year=2024)
    assert features["rolling_mean_6"] == round(sum(prices) / 6, 4)


def test_calendar_features():
    prices = [700.0, 720.0, 750.0, 780.0, 800.0, 820.0]
    features = compute_features(prices, month=7, year=2025)
    assert features["month"] == 7
    assert features["year"] == 2025


def test_returns_correct_keys():
    prices = [700.0, 720.0, 750.0, 780.0, 800.0, 820.0]
    features = compute_features(prices, month=1, year=2024)
    expected_keys = {
        "price_lag_1", "price_lag_2", "price_lag_3",
        "rolling_mean_3", "rolling_mean_6", "month", "year",
    }
    assert set(features.keys()) == expected_keys


def test_requires_at_least_6_prices():
    with pytest.raises(ValueError, match="at least 6"):
        compute_features([700.0, 720.0], month=1, year=2024)
