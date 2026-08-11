# TARQ Project 3: News Classifier API

This project turns the AG News classifier from TARQ Project 2 into a live, tested, containerized API.

The goal was not just to train a model, but to make it usable as real software: a client sends news text to an API endpoint, the API validates the input, runs the saved classifier, and returns a JSON prediction.

## Live Demo

Railway deployment:

```text
https://news-classifier-api-production.up.railway.app
```

Health check:

```bash
curl https://news-classifier-api-production.up.railway.app/health
```

Example prediction:

```bash
curl -X POST https://news-classifier-api-production.up.railway.app/predict \
  -H 'Content-Type: application/json' \
  -d '{"text": "India wins cricket World Cup in dramatic final"}'
```

Example response:

```json
{
  "label": "Sports",
  "label_id": 1,
  "confidence": 0.9755,
  "probabilities": {
    "World": 0.0216,
    "Sports": 0.9755,
    "Business": 0.0015,
    "Technology": 0.0014
  }
}
```

## What This Project Builds

This project serves a trained AG News classifier through a FastAPI web service.

It includes:

- `/health` endpoint for service readiness
- `/predict` endpoint for text classification
- Pydantic request validation
- Model loading once at startup
- JSON response with label, confidence, and probabilities
- pytest test suite
- Docker containerization
- Railway deployment
- model card for responsible documentation

## How the API Works

Request flow:

```text
Client
→ HTTP POST request
→ FastAPI
→ Pydantic validation
→ saved Project 2 model
→ JSON response
```

The model is loaded once when the server starts. This avoids reloading `baseline_model.pkl` from disk for every request, keeping prediction responses fast.

## Model

The API uses the baseline model trained in TARQ Project 2:

```text
TF-IDF Vectorizer + Logistic Regression
```

The model classifies English news text into four categories:

- World
- Sports
- Business
- Technology

Project 2 evaluation results:

| Metric | Result |
|---|---:|
| Validation accuracy | 92.17% |
| Test accuracy | 91.78% |
| Strongest class | Sports |
| Weakest class | Business |
| Main confusion pair | Business ↔ Technology |

The model file is stored at:

```text
models/baseline_model.pkl
```

## API Endpoints

### `GET /health`

Checks whether the API is running and whether the model is loaded.

Example response:

```json
{
  "status": "ok",
  "model_ready": true,
  "version": "1.0.0"
}
```

### `POST /predict`

Classifies news text.

Request body:

```json
{
  "text": "Apple reports record quarterly revenue from iPhone sales"
}
```

Response body:

```json
{
  "label": "Technology",
  "label_id": 3,
  "confidence": 0.8345,
  "probabilities": {
    "World": 0.0171,
    "Sports": 0.0094,
    "Business": 0.139,
    "Technology": 0.8345
  }
}
```

## Input Validation

The API uses Pydantic to validate requests before prediction runs.

The `text` field must:

- exist in the request body
- not be empty or whitespace
- contain at least 10 characters
- contain fewer than 10,000 characters

Invalid requests return `422 Unprocessable Entity`.

Example invalid request:

```json
{
  "text": ""
}
```

## Project Structure

```text
news-classifier-api/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI routes and validation
│   └── model.py         # model loading and prediction logic
├── models/
│   └── baseline_model.pkl
├── tests/
│   ├── __init__.py
│   └── test_api.py
├── Dockerfile
├── requirements.txt
├── model_card.md
├── CORRECTIONS.md
├── .gitignore
├── .dockerignore
└── README.md
```

## Run Locally

Create and activate a virtual environment:

```bash
python3.11 -m venv env
source env/bin/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Run the API:

```bash
uvicorn app.main:app --reload --port 8000
```

Open the interactive API docs:

```text
http://localhost:8000/docs
```

## Run Tests

```bash
pytest tests/ -v
```

The test suite checks:

- `/health` returns 200
- model is ready
- valid `/predict` requests work
- response schema is correct
- probabilities sum to 1
- invalid inputs return 422
- edge cases do not crash the API

Current status:

```text
14 tests passed
```

## Run with Docker

Build the Docker image:

```bash
docker build -t news-classifier:latest .
```

Run the container:

```bash
docker run -p 8000:8000 news-classifier:latest
```

Then open:

```text
http://localhost:8000/docs
```

Docker packages the app, Python environment, dependencies, and model file into one portable container. This helps avoid the “works on my machine” problem.

## Deployment

The API is deployed on Railway using the Dockerfile in this repository.

Railway builds the Docker image from the GitHub repo and exposes the FastAPI service through a public HTTPS URL.

Live URL:

```text
https://news-classifier-api-production.up.railway.app
```

## Known Limitations

- The model was trained on AG News, so it is designed for English news classification only.
- It should not be used for high-stakes decisions.
- Business and Technology are often confused because technology companies are frequently discussed using business vocabulary.
- World and Business can overlap on oil, trade, government, markets, and economic topics.
- Some AG News labels may be ambiguous or noisy.
- TF-IDF + Logistic Regression relies on word and phrase patterns rather than deep contextual understanding.
- The API currently has no authentication or rate limiting.

## What I Learned

This project taught me how to move a machine learning model from local evaluation to a usable web service.

I learned how to:

- separate model logic from API logic
- use FastAPI to build prediction endpoints
- use Pydantic for input validation
- return structured JSON responses
- write automated API tests with pytest
- containerize an ML API with Docker
- deploy a Dockerized API to Railway
- document a deployed model with a model card

Project 2 answered: “Does the model work?”

Project 3 answered: “Can the model be served as real software?”