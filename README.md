<h1 align="center">News Classifier API</h1>

**Send English news text to an API and receive one of four AG News categories with class probabilities.**

[Demo or published artifacts](https://news-classifier-api-production.up.railway.app/docs)

Python 3.11. FastAPI server with a saved TF-IDF model. Public API has rate limits and no authentication.

By Om Patnaik · repository created August 2026.

## Install

| Platform / path | Start here |
| --- | --- |
| Python | `pip install -r requirements.txt` in a Python 3.11 virtual environment |
| Docker | `docker build -t news-classifier:latest .` |

Run the command below and open http://localhost:8000/docs. Use a short sample news paragraph to try the API without training a model.

```bash
uvicorn app.main:app --reload --port 8000
```

```bash
uvicorn app.main:app --reload --port 8000
```

## Why

You have a trained classifier, but a usable service also needs input validation, structured output, and failure handling. This API serves the AG News TF-IDF/Logistic Regression baseline. It is limited to English news and can confuse Business with Technology or World.

## Send a prediction

Call `POST /predict` with the JSON schema shown in `/docs`; `GET /health` reports service readiness. Invalid input returns 422 and throttled requests return 429.

## Run the saved model

The committed model is loaded from `models/baseline_model.pkl`. The service adds input checks and basic SlowAPI limits; it does not retrain or improve the classifier.

## Notes from building it

I separated the model loader from the API routes so serving can be checked independently. Request validation and response tests made the baseline usable as software. I would evaluate new article distributions before claiming the same performance beyond AG News.

## Commands

```bash
uvicorn app.main:app --reload --port 8000  # run the API
pytest tests/ -v                          # run API checks
docker build -t news-classifier:latest .   # build the container
docker run -p 8000:8000 news-classifier:latest  # serve the container
```

## Verify it yourself

```bash
pytest tests/ -v
```

Tests check health, model readiness, prediction schema, probability sums, invalid inputs, and edge cases. The earlier README records 14 passing tests; that historical count is not a new run or an accuracy measure.

## Credits, license and pointers

Built with FastAPI, Pydantic, scikit-learn, SlowAPI, pytest, and Docker; classifier trained on AG News. No source license file is present. [Model card](model_card.md).

[Full setup, original notes, and project history](README-DETAILS.md).
