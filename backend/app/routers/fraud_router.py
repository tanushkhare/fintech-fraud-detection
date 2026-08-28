from fastapi import APIRouter, HTTPException
from backend.app.schemas.fraud_schema import TransactionEvaluationRequest, FraudEvaluationResponse
from backend.app.services.fraud_service import fraud_engine

router = APIRouter(prefix="/api/v1/fraud", tags=["Fintech Fraud Detection Engine"])

@router.post("/evaluate", response_model=FraudEvaluationResponse)
async def evaluate_transaction_risk(payload: TransactionEvaluationRequest):
    try:
        result = fraud_engine.evaluate_transaction(
            payload.transaction_id,
            payload.amount_usd,
            payload.location_country,
            payload.is_foreign_transaction,
            payload.velocity_1h_count,
            payload.device_trust_score
        )
        return FraudEvaluationResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
