from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class TransactionPayload(BaseModel):
    transaction_id: str = Field(..., description="Unique transaction ID")
    account_id: str = Field(..., description="Account identifier")
    amount: float = Field(..., gt=0.0, description="Transaction monetary amount")
    location_distance_km: float = Field(default=5.0, ge=0.0)
    velocity_past_hour: int = Field(default=1, ge=0)
    is_international: bool = Field(default=False)
    device_risk_score: float = Field(default=0.1, ge=0.0, le=1.0)

class TransactionEvaluationResponse(BaseModel):
    transaction_id: str
    anomaly_score: float
    fraud_probability: float
    decision: str
    is_anomalous: bool
    risk_factors: List[str]
    timestamp: str
