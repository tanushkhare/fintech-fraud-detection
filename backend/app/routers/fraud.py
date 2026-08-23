from fastapi import APIRouter
from backend.app.schemas.fraud import TransactionScoreRequest, TransactionScoreResponse
from backend.app.services.fraud_service import fraud_service

router = APIRouter(prefix="/api/v1", tags=["Fraud Detection Engine"])

@router.post("/score", response_model=TransactionScoreResponse)
async def score_transaction(payload: TransactionScoreRequest):
    return fraud_service.evaluate(payload)
