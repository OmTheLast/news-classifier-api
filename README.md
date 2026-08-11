# TARQ Project 3 - News Classifier API

This project wraps the AG News classifier from Project 2 in a FastAPI service.

## What It Builds

- `/health` endpoint for service readiness
- `/predict` endpoint for classifying news text
- Pydantic request validation
- Model loading once at startup
- pytest test suite
- Dockerfile for containerized deployment
- model card for responsible API documentation

## Project Structure

```text
project3/
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── model.py
├── models/
│   └── baseline_model.pkl
├── tests/
│   ├── __init__.py
│   └── test_api.py
├── Dockerfile
├── requirements.txt
├── model_card.md
└── CORRECTIONS.md
```

## Setup

```bash
python3 -m venv env
source env/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run Locally

```bash
uvicorn app.main:app --reload --port 8000
```

Open:

```text
http://localhost:8000/docs
```

## Test

```bash
pytest tests/ -v
```

## Docker

```bash
docker build -t news-classifier:latest .
docker run -p 8000:8000 news-classifier:latest
```

