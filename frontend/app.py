import streamlit as st

st.markdown("""
    <style>
        .stApp {
            background-color: #090d16;
            color: #f8fafc;
            font-family: 'Inter', sans-serif;
        }
        .sidebar .stSidebar {
            background-color: #0f172a;
            border-right: 1px solid #1e293b;
        }
        h1, h2, h3 {
            color: #f8fafc;
            font-weight: 700;
            letter-spacing: -0.02em;
        }
        .stButton>button {
            background: linear-gradient(135deg, #38bdf8 0%, #0284c7 100%);
            color: #090d16;
            font-weight: 600;
            border: none;
            border-radius: 0.5rem;
            padding: 0.5rem 1rem;
        }
    </style>
""", unsafe_allow_html=True)

import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Fintech Fraud Detection", layout="wide")

st.title("💳 Real-Time Fintech Fraud Detection Engine")
st.markdown("Isolation Forest anomaly scoring, transaction risk factor attribution, and evaluation.")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Transaction Ingestion Parameters")
    tx_id = st.text_input("Transaction Reference ID", value="TX-8492041")
    acc_id = st.text_input("Account Principal ID", value="ACC-772910")
    amount = st.number_input("Monetary Amount ($)", value=2450.0, step=100.0)
    dist = st.slider("Geographic Leap Distance (km)", 0.0, 1500.0, 120.0)
    velocity = st.slider("Transaction Velocity (past hour)", 1, 20, 2)
    is_intl = st.checkbox("Cross-Border / International Clearing", value=False)
    device_risk = st.slider("Device Fingerprint Risk Coefficient", 0.0, 1.0, 0.15)

    if st.button("Evaluate Transaction Stream", type="primary"):
        payload = {
            "transaction_id": tx_id,
            "account_id": acc_id,
            "amount": amount,
            "location_distance_km": dist,
            "velocity_past_hour": velocity,
            "is_international": is_intl,
            "device_risk_score": device_risk
        }
        try:
            res = requests.post("http://localhost:8000/api/v1/fraud/evaluate", json=payload, timeout=5)
            if res.status_code == 200:
                st.session_state["p12_res"] = res.json()
                st.success("Evaluation complete.")
            else:
                st.error(f"Error: {res.text}")
        except Exception:
            st.warning("Backend offline. Executing client-side fallback evaluation.")
            prob = 0.82 if amount > 5000 or dist > 500 else 0.15
            st.session_state["p12_res"] = {
                "transaction_id": tx_id,
                "anomaly_score": -0.64 if prob > 0.5 else 0.70,
                "fraud_probability": prob,
                "decision": "FLAGGED_FRAUD_REVIEW" if prob > 0.5 else "TRANSACTION_APPROVED",
                "is_anomalous": prob > 0.5,
                "risk_factors": ["High transaction amount", "Rapid velocity"] if prob > 0.5 else ["Standard spending baseline"],
                "timestamp": "2026-08-28T12:00:00Z"
            }

with col2:
    if "p12_res" in st.session_state:
        r = st.session_state["p12_res"]
        st.subheader(f"Risk Audit: {r['transaction_id']}")
        m1, m2 = st.columns(2)
        m1.metric("Fraud Probability", f"{r['fraud_probability'] * 100:.1f}%")
        m2.metric("Anomaly Metric", f"{r['anomaly_score']:.4f}")

        if r["is_anomalous"]:
            st.error(f"Decision: **{r['decision']}**")
        else:
            st.success(f"Decision: **{r['decision']}**")

        st.markdown("### ⚠️ Attributed Risk Vectors")
        for rf in r["risk_factors"]:
            st.write(f"- {rf}")

