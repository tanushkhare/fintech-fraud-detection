import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

def test_legitimate_transaction():
    payload = {
        "transaction_id": "TX-TEST-001",
        "account_id": "ACC-TEST",
        "amount": 45.00,
        "location_distance_km": 2.0,
        "velocity_past_hour": 1,
        "is_international": False,
        "device_risk_score": 0.05
    }
    res = client.post("/api/v1/fraud/evaluate", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["is_anomalous"] is False
    assert data["decision"] == "TRANSACTION_APPROVED"

def test_anomalous_fraud_transaction():
    payload = {
        "transaction_id": "TX-FRAUD-999",
        "account_id": "ACC-FLAGGED",
        "amount": 9500.00,
        "location_distance_km": 1200.0,
        "velocity_past_hour": 9,
        "is_international": True,
        "device_risk_score": 0.85
    }
    res = client.post("/api/v1/fraud/evaluate", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["is_anomalous"] is True
    assert data["decision"] == "FLAGGED_FRAUD_REVIEW"
    assert len(data["risk_factors"]) >= 3
