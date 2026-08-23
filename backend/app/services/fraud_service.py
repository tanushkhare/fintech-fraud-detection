from backend.app.schemas.fraud import TransactionScoreRequest, TransactionScoreResponse

class FraudScoringEngine:
    @staticmethod
    def evaluate(payload: TransactionScoreRequest) -> TransactionScoreResponse:
        amount_factor = min(payload.amount / 5000.0, 1.0) * 0.35
        geo_factor = payload.geo_velocity_score * 0.40
        trust_factor = (1.0 - payload.device_trust_score) * 0.25

        risk_score = round(min(max(amount_factor + geo_factor + trust_factor, 0.0), 1.0), 2)
        is_fraud = risk_score >= 0.65

        factors = []
        if payload.amount >= 2000.0:
            factors.append(f"High monetary velocity (${payload.amount:,.2f})")
        if payload.geo_velocity_score >= 0.5:
            factors.append(f"Geo-velocity anomaly detected (Score: {payload.geo_velocity_score})")
        if payload.device_trust_score <= 0.4:
            factors.append(f"Untrusted device signature (Trust: {payload.device_trust_score})")
        if not factors:
            factors.append("Nominal device and transaction telemetry metrics")

        return TransactionScoreResponse(
            is_fraud=is_fraud,
            risk_score=risk_score,
            status_text="FRAUD DETECTED" if is_fraud else "LEGITIMATE TRANSACTION",
            risk_factors=factors
        )

fraud_service = FraudScoringEngine()
