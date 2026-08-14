import time
import logging

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, field_validator

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.model import get_model, predict


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="News Category Classifier",
    description="Classifies news text into World, Sports, Business, or Technology.",
    version="1.0.0",
)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time

    logger.info(
        "%s %s -> %s %.3fs",
        request.method,
        request.url.path,
        response.status_code,
        duration,
    )

    return response


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
@limiter.limit("60/minute")
def health(request: Request):
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
@limiter.limit("30/minute")
def predict_endpoint(request: Request, payload: PredictRequest):
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
        result = predict(payload.text)
        return PredictResponse(**result)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

