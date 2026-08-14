# Model Card: AG News Category Classifier

## Model Description

TF-IDF vectorizer with 50,000 maximum features, unigrams and bigrams, and Logistic Regression. The model classifies English news text into four categories: World, Sports, Business, and Technology.

## Deployment

This model is served through a FastAPI application and deployed on Railway.

Live API:

```text
https://news-classifier-api-production.up.railway.app
```

## Intended Use

- Educational demonstration of model serving
- Routing or tagging English-language news examples
- API deployment practice

## Out-of-Scope Uses

- Non-English classification
- High-stakes decisions
- News outside the AG News label schema

## Training Data

AG News training split from Project 2. The original 120,000 training examples were split into 108,000 training examples and 12,000 validation examples with stratification.

## Evaluation Results

From TARQ Project 2:

| Class | Precision | Recall | F1 |
|---|---:|---:|---:|
| World | 0.93 | 0.91 | 0.92 |
| Sports | 0.95 | 0.98 | 0.97 |
| Business | 0.89 | 0.88 | 0.89 |
| Technology | 0.89 | 0.90 | 0.90 |

Overall:

| Split | Accuracy |
|---|---:|
| Validation | 92.17% |
| Test | 91.78% |


## Known Limitations

- TF-IDF loses word order and deeper context.
- Business and Technology frequently overlap.
- World and Business overlap on oil, trade, government, and economic topics.
- Some AG News labels appear ambiguous or noisy.
- The model was trained on historical AG News data and may degrade on recent or out-of-distribution news.

## API

```http
GET /health
POST /predict
```

Request body:

```json
{"text": "<news text>"}
```

## Security Note

This API has basic rate limiting but no authentication. It is acceptable for a low-risk educational demo, but a real public production API should add API keys or OAuth, stronger rate limits, structured logging, and monitoring.
