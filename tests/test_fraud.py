import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

def test_high_risk_fraud_transaction():
    payload = {
        "transaction_id": "TXN_SUSPICIOUS_01",
        "amount_usd": 12000.0,
        "location_country": "KY",
        "is_foreign_transaction": True,
        "velocity_1h_count": 8,
        "device_trust_score": 0.20
    }
    res = client.post("/api/v1/fraud/evaluate", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["decision_verdict"] == "BLOCK_TRANSACTION"
    assert data["risk_score"] >= 0.70
    assert len(data["risk_factors"]) >= 3

def test_low_risk_legitimate_transaction():
    payload = {
        "transaction_id": "TXN_LEGIT_01",
        "amount_usd": 45.0,
        "location_country": "US",
        "is_foreign_transaction": False,
        "velocity_1h_count": 1,
        "device_trust_score": 0.95
    }
    res = client.post("/api/v1/fraud/evaluate", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["decision_verdict"] == "APPROVE_TRANSACTION"
    assert data["risk_score"] < 0.40
