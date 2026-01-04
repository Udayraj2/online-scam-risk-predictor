# Risk keywords for explainability
SCAM_KEYWORDS = [
    "blocked", "verify", "unauthorized", "refund", "failed",
    "suspension", "reversal", "claim", "reward", "KYC", "suspend"
]




from fastapi import APIRouter
import pandas as pd
from app.models.scam_model import load_model
from app.schemas.request import ScamRequest

router = APIRouter()

@router.post("/predict")
def predict_scam(data: ScamRequest):
    model = load_model()

    input_df = pd.DataFrame([{
        "message": data.message,
        "amount": data.amount,
        "sender_type": data.sender_type
    }])

    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df).max()

    # Risk level logic
    if prediction == "scam" and probability > 0.8:
        risk = "High Risk"
    elif prediction == "scam":
        risk = "Medium Risk"
    else:
        risk = "Low Risk"

    # 🔹 Explainability
    explanation = []

    # Keyword check
    for kw in SCAM_KEYWORDS:
        if kw.lower() in data.message.lower():
            explanation.append(f"Contains keyword '{kw}'")

    # Amount check
    if data.amount > 10000:
        explanation.append(f"High transaction amount ₹{data.amount}")

    # Sender check
    if data.sender_type == "unknown":
        explanation.append("Unknown sender type")

    if not explanation:
        explanation.append("No obvious risk factors detected")

    return {
        "prediction": prediction,
        "risk_level": risk,
        "confidence": round(probability, 2),
        "explanation": explanation
    }
