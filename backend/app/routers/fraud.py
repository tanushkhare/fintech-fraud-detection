from fastapi import APIRouter
from app.schemas.fraud import TransactionRequest, FraudResponse
from app.services.fraud_service import evaluate_transaction

router = APIRouter(prefix="/api", tags=["Fraud Detection"])

@router.post("/check", response_model=FraudResponse)
def check_fraud(payload: TransactionRequest):
    return evaluate_transaction(payload)