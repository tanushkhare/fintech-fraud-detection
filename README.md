
# ⚡ FinTech Fraud Detection Pipeline

[![Live Web Demo](https://img.shields.io/badge/Live_App-Vercel-black?style=for-the-badge&logo=vercel)](https://fintech-fraud-detection-web.vercel.app)
[![Portfolio Hub](https://img.shields.io/badge/Portfolio_Hub-Live-blue?style=for-the-badge)](https://portfolio-showcase-hub-web11.vercel.app)

🔗 **Production URL:** [https://fintech-fraud-detection-web.vercel.app](https://fintech-fraud-detection-web.vercel.app)  
🌐 **Showcase Hub:** [https://portfolio-showcase-hub-web11.vercel.app](https://portfolio-showcase-hub-web11.vercel.app)

---

## 📌 Architectural Overview
Multivariate IsolationForest scoring transaction outliers across geo-distance deltas, purchase amounts, and hourly velocity spikes.

---

## 🛠️ Technology Ecosystem
* **Core Architecture:** Scikit-Learn, IsolationForest, FastAPI, Pydantic
* **Testing & Quality:** PyTest, Automated GitHub Actions CI
* **Deployment:** Vercel Edge Runtime

---

## 🛡️ Production Standards
* **Resolved Interpolation Error:** Cleaned up earlier string interpolation faults.
* **Feature Attribution:** Identifies specific contributing risk signals for each flag.
* **Rolling Velocity Windows:** Tracks transaction bursts over 1-hour windows.

---

## 🚀 API Contracts
```http
POST /api/v1/fraud/evaluate
Request:
{
  "amount": 6400,
  "location_distance_km": 640,
  "tx_velocity_last_hour": 7
}

Response (200 OK):
{
  "transaction_id": "TXN-9042",
  "fraud_probability": 0.725,
  "decision": "BLOCKED",
  "risk_tier": "CRITICAL_FRAUD",
  "factor_breakdown": ["High capital outflow", "Velocity spike"]
}

GET /health
Response: {"status": "healthy"}

💻 Local Quickstart

Bash

pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000
pytest tests/ -v