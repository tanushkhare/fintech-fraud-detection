from pydantic import BaseModel, Field
from typing import List

class TransactionScoreRequest(BaseModel):
    amount: float = Field(..., gt=0.0)
    merchant_category: str
    geo_velocity_score: float = Field(..., ge=0.0, le=1.0)
    device_trust_score: float = Field(..., ge=0.0, le=1.0)

class TransactionScoreResponse(BaseModel):
    is_fraud: bool
    risk_score: float
    status_text: str
    risk_factors: List[str]
