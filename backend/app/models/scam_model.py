import joblib
from pathlib import Path

MODEL_PATH = Path(__file__).resolve().parents[2] / "saved_models" / "scam_classifier.pkl"

model = None

def load_model():
    global model
    if model is None:
        model = joblib.load(MODEL_PATH)
    return model
