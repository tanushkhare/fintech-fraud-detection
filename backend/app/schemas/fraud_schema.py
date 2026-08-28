from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class TransactionEvaluationRequest(BaseModel):
    transaction_id: str = Field(..., description="Unique transaction reference (e.g. TXN-9981)")
    amount_usd: float = Field(..., ge=0.01, description="Transaction monetary value")
    location_country: str = Field(default="US", description="Origin country code")
    is_foreign_transaction: bool = Field(default=False)
    velocity_1h_count: int = Field(default=1, ge=0, description="Transactions initiated by user in the past hour")
    device_trust_score: float = Field(default=0.95, ge=0.0, le=1.0)

class FraudEvaluationResponse(BaseModel):
    transaction_id: str
    amount_usd: float
    risk_score: float
    fraud_probability: float
    decision_verdict: str
    risk_factors: List[str]
    timestamp: str
