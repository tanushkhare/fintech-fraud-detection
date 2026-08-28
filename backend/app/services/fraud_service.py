from datetime import datetime, timezone
from typing import Dict, Any, List

class FintechFraudEngine:
    def evaluate_transaction(
        self,
        txn_id: str,
        amount: float,
        country: str,
        is_foreign: bool,
        velocity: int,
        device_trust: float
    ) -> Dict[str, Any]:
        risk_score = 0.05
        factors: List[str] = []

        # 1. Amount threshold heuristic
        if amount > 5000.0:
            risk_score += 0.35
            factors.append(f"High transaction value (${amount:,.2f})")
        elif amount > 1500.0:
            risk_score += 0.15
            factors.append("Elevated transaction value ($1.5k+)")

        # 2. Velocity spike check
        if velocity >= 5:
            risk_score += 0.30
            factors.append(f"High transaction velocity ({velocity} txns/hr)")
        elif velocity >= 3:
            risk_score += 0.15
            factors.append(f"Moderate velocity surge ({velocity} txns/hr)")

        # 3. Foreign origin and device trustworthiness
        if is_foreign:
            risk_score += 0.15
            factors.append("Cross-border foreign transaction origin")

        if device_trust < 0.50:
            risk_score += 0.25
            factors.append(f"Untrusted or unrecognized client device (Trust: {device_trust})")

        risk_score = round(min(0.99, max(0.01, risk_score)), 3)
        fraud_prob = round(risk_score * 100, 1)

        if risk_score >= 0.70:
            verdict = "BLOCK_TRANSACTION"
        elif risk_score >= 0.40:
            verdict = "FLAG_FOR_MANUAL_REVIEW"
        else:
            verdict = "APPROVE_TRANSACTION"

        if not factors:
            factors.append("Standard behavioral baseline match")

        return {
            "transaction_id": txn_id,
            "amount_usd": amount,
            "risk_score": risk_score,
            "fraud_probability": fraud_prob,
            "decision_verdict": verdict,
            "risk_factors": factors,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

fraud_engine = FintechFraudEngine()
