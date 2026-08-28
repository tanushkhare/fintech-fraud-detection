from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routers import fraud_router
import uvicorn

app = FastAPI(
    title="Fintech Fraud Detection & Risk Scoring API",
    description="Real-time transaction risk scoring, velocity anomaly detection, and fraud classification engine.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(fraud_router.router)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "fintech-fraud-detection"}

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
