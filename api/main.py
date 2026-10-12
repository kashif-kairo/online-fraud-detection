from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal

from src.prediction import predict_fraud

app = FastAPI(
    title="Online Fraud Detection API",
    description="API for detecting potentially fraudulent financial transactions.",
    version="1.0.0",
)


class Transaction(BaseModel):
    step: int = Field(..., ge=0)
    type: Literal["CASH_IN", "CASH_OUT", "DEBIT", "PAYMENT", "TRANSFER"]
    amount: float = Field(..., ge=0)
    oldbalanceOrg: float = Field(..., ge=0)
    newbalanceOrig: float = Field(..., ge=0)
    oldbalanceDest: float = Field(..., ge=0)
    newbalanceDest: float = Field(..., ge=0)


@app.get("/")
def home():
    return {
        "message": "Online Fraud Detection API is running!",
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/predict")
def predict(transaction: Transaction):
    try:
        result = predict_fraud(transaction.model_dump())
        return result
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))