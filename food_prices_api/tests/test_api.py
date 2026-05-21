import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_returns_200(client):
    payload = {
        "prices": [700.0, 720.0, 750.0, 780.0, 800.0, 820.0],
        "month": 4,
        "year": 2024,
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200


def test_predict_returns_expected_fields(client):
    payload = {
        "prices": [700.0, 720.0, 750.0, 780.0, 800.0, 820.0],
        "month": 4,
        "year": 2024,
    }
    response = client.post("/predict", json=payload)
    data = response.json()
    assert "predicted_price" in data
    assert "currency" in data
    assert data["currency"] == "UGX"
    assert isinstance(data["predicted_price"], float)


def test_predict_rejects_too_few_prices(client):
    payload = {
        "prices": [700.0, 720.0],
        "month": 4,
        "year": 2024,
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422


def test_predict_rejects_invalid_month(client):
    payload = {
        "prices": [700.0, 720.0, 750.0, 780.0, 800.0, 820.0],
        "month": 13,
        "year": 2024,
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422
