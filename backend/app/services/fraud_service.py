def evaluate_transaction(tx):
    risk_score = 0.1
    reason = "Normal transaction pattern"
    
    if tx.amount > 5000.0:
        risk_score += 0.6
        reason = "High transaction amount threshold exceeded"
    if tx.location.lower() in ["foreign", "unknown", "high-risk"]:
        risk_score += 0.3
        reason += "; Unrecognized geographic location"
        
    is_flagged = risk_score >= 0.5
    return {
        "transaction_id": tx.transaction_id,
        "risk_score": round(risk_score, 2),
        "is_flagged": is_flagged,
        "reason": reason
    }