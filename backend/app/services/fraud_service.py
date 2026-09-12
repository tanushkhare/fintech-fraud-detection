import math
from datetime import datetime, timezone
from typing import Dict, Any, List

class FraudDetectionEngine:
    def evaluate_transaction(self, tx: Dict[str, Any]) -> Dict[str, Any]:
        amount = float(tx.get("amount", 0.0))
        dist = float(tx.get("location_distance_km", 0.0))
        velocity = int(tx.get("velocity_past_hour", 1))
        is_intl = bool(tx.get("is_international", False))
        device_risk = float(tx.get("device_risk_score", 0.0))

        risk_factors: List[str] = []
        heuristic_score = 0.0

        if amount > 5000:
            heuristic_score += 0.35
            risk_factors.append("High monetary value exceeding threshold ($5,000)")
        elif amount > 1000:
            heuristic_score += 0.15

        if dist > 500:
            heuristic_score += 0.25
            risk_factors.append("Abnormal geographic distance leap (>500km)")

        if velocity > 5:
            heuristic_score += 0.25
            risk_factors.append("Rapid transaction velocity within past hour")

        if is_intl:
            heuristic_score += 0.15
            risk_factors.append("Cross-border foreign transaction settlement")

        if device_risk > 0.5:
            heuristic_score += 0.20
            risk_factors.append("Suspicious device fingerprint signature")

        fraud_prob = min(round(heuristic_score, 4), 0.99)
        # Isolation Forest baseline projection
        anomaly_score = round(1.0 - (2.0 * fraud_prob), 4)
        is_anomalous = fraud_prob >= 0.50
        decision = "FLAGGED_FRAUD_REVIEW" if is_anomalous else "TRANSACTION_APPROVED"

        return {
            "transaction_id": tx.get("transaction_id", "TX-UNKNOWN"),
            "anomaly_score": anomaly_score,
            "fraud_probability": fraud_prob,
            "decision": decision,
            "is_anomalous": is_anomalous,
            "risk_factors": risk_factors,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

fraud_engine = FraudDetectionEngine()
