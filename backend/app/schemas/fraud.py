from pydantic import BaseModel

class TransactionRequest(BaseModel):
    transaction_id: str
    amount: float
    location: str
    device_fingerprint: str

class FraudResponse(BaseModel):
    transaction_id: str
    risk_score: float
    is_flagged: bool
    reason: str