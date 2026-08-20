import streamlit as st
import requests

st.title("🛡️ FinTech Real-Time Fraud Detection")
tx_id = st.text_input("Transaction ID", "TX-98421")
amount = st.number_input("Amount ($)", value=1200.0)
location = st.text_input("Location", "New York")
device = st.text_input("Device Fingerprint", "iPhone-15-Pro")

if st.button("Evaluate Transaction"):
    res = requests.post("http://127.0.0.1:8000/api/check", json={
        "transaction_id": tx_id, "amount": amount, "location": location, "device_fingerprint": device
    })
    if res.status_code == 200:
        data = res.json()
        st.metric("Risk Score", data["risk_score"])
        st.write(f"**Flagged Status:** {'🚨 Fraud Suspected' : '✅ Cleared' if not data['is_flagged'] else '🚨 Fraud Suspected'}")
        st.info(f"**Reason:** {data['reason']}")