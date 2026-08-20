import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Fintech Fraud Detection Engine", layout="wide")

st.title("🛡️ Real-Time Fintech Fraud Detection Pipeline")
st.markdown("Automated anomaly detection engine scoring high-throughput financial transactions.")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Transaction Ingestion")
    amount = st.number_input("Transaction Amount ($)", min_value=0.01, value=150.00, step=10.0)
    merchant = st.selectbox("Merchant Category", ["E-Commerce", "Point of Sale", "Crypto Exchange", "Wire Transfer", "ATM Withdrawal"])
    location_score = st.slider("Geo-Velocity Anomaly Score", min_value=0.0, max_value=1.0, value=0.15)
    device_trust = st.slider("Device Trust Score", min_value=0.0, max_value=1.0, value=0.95)
    
    if st.button("Score Transaction", type="primary"):
        payload = {
            "amount": amount,
            "merchant_category": merchant,
            "geo_velocity_score": location_score,
            "device_trust_score": device_trust
        }
        try:
            res = requests.post("http://localhost:8000/api/v1/score", json=payload, timeout=5)
            if res.status_code == 200:
                data = res.json()
                is_fraud = data.get("is_fraud", False)
                risk_score = data.get("risk_score", 0.0)
                status_text = "FRAUD DETECTED" if is_fraud else "LEGITIMATE TRANSACTION"
                
                if is_fraud:
                    st.error(f"Status: {status_text} | Risk Score: {risk_score:.2f}")
                else:
                    st.success(f"Status: {status_text} | Risk Score: {risk_score:.2f}")
            else:
                st.error(f"API Error: HTTP {res.status_code}")
        except requests.exceptions.RequestException:
            # Fallback local inference simulation
            simulated_risk = (amount / 5000.0) * 0.4 + (location_score * 0.4) + ((1.0 - device_trust) * 0.2)
            simulated_risk = min(max(simulated_risk, 0.0), 1.0)
            is_fraud = simulated_risk > 0.65
            status_text = "FRAUD DETECTED" if is_fraud else "LEGITIMATE TRANSACTION"
            
            if is_fraud:
                st.error(f"Status (Offline Simulation): {status_text} | Risk Score: {simulated_risk:.2f}")
            else:
                st.success(f"Status (Offline Simulation): {status_text} | Risk Score: {simulated_risk:.2f}")

with col2:
    st.subheader("Live Anomaly Stream Metrics")
    mock_df = pd.DataFrame({
        "Timestamp": pd.date_range(start="2026-08-20", periods=20, freq="min"),
        "Risk_Score": [0.12, 0.08, 0.15, 0.22, 0.91, 0.18, 0.05, 0.88, 0.14, 0.09, 0.11, 0.95, 0.21, 0.07, 0.19, 0.13, 0.04, 0.79, 0.10, 0.15]
    })
    fig = px.line(mock_df, x="Timestamp", y="Risk_Score", title="Transaction Risk Probability Timeline", markers=True)
    fig.add_hline(y=0.65, line_dash="dash", line_color="red", annotation_text="Fraud Threshold (0.65)")
    st.plotly_chart(fig, use_container_width=True)
