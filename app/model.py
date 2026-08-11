from pathlib import Path

import joblib
import numpy as np


MODEL_PATH = Path(__file__).parent.parent / "models" / "baseline_model.pkl"

LABELS = {
    0: "World",
    1: "Sports",
    2: "Business",
    3: "Technology",
}

_model = None


def get_model():
    global _model
    if _model is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Model file not found at {MODEL_PATH}. "
                "Run Project 2 and copy models/baseline_model.pkl into this project."
            )
        _model = joblib.load(MODEL_PATH)
    return _model


def predict(text: str) -> dict:
    model = get_model()
    probs = model.predict_proba([text])[0]
    pred = int(np.argmax(probs))

    return {
        "label": LABELS[pred],
        "label_id": pred,
        "confidence": round(float(probs[pred]), 4),
        "probabilities": {
            LABELS[i]: round(float(p), 4)
            for i, p in enumerate(probs)
        },
    }

