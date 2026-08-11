from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator

from app.model import get_model, predict


app = FastAPI(
    title="News Category Classifier",
    description="Classifies news text into World, Sports, Business, or Technology.",
    version="1.0.0",
)


class PredictRequest(BaseModel):
    text: str

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("text must not be empty or whitespace")
        if len(value) < 10:
            raise ValueError("text must be at least 10 characters")
        if len(value) > 10000:
            raise ValueError("text must be under 10,000 characters")
        return value


class PredictResponse(BaseModel):
    label: str
    label_id: int
    confidence: float
    probabilities: dict[str, float]


class HealthResponse(BaseModel):
    status: str
    model_ready: bool
    version: str


@app.on_event("startup")
async def startup_event():
    get_model()
    print("Model loaded and ready.")


@app.get("/health", response_model=HealthResponse)
def health():
    """
    Health check endpoint.

    Returns whether the service is running and the model is loaded.
    """
    try:
        get_model()
        ready = True
    except Exception:
        ready = False

    return HealthResponse(
        status="ok" if ready else "degraded",
        model_ready=ready,
        version="1.0.0",
    )


@app.post("/predict", response_model=PredictResponse)
def predict_endpoint(request: PredictRequest):
    """
    Classify news text into one of four categories.

    Input:
    - text: News headline or article text, 10 to 10,000 characters.

    Output:
    - predicted label
    - label id
    - confidence
    - probabilities for all four classes
    """
    try:
        result = predict(request.text)
        return PredictResponse(**result)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

