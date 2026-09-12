from fastapi import APIRouter, HTTPException
from backend.app.schemas.fraud_schema import TransactionPayload, TransactionEvaluationResponse
from backend.app.services.fraud_service import fraud_engine

router = APIRouter(prefix="/api/v1/fraud", tags=["Fintech Fraud Detection Engine"])

@router.post("/evaluate", response_model=TransactionEvaluationResponse)
async def evaluate_transaction_endpoint(payload: TransactionPayload):
    try:
        tx_dict = payload.model_dump()
        result = fraud_engine.evaluate_transaction(tx_dict)
        return TransactionEvaluationResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
