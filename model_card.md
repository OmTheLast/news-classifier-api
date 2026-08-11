# Model Card: AG News Category Classifier

## Model Description

TF-IDF vectorizer with 50,000 maximum features, unigrams and bigrams, and Logistic Regression. The model classifies English news text into four categories: World, Sports, Business, and Technology.

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

From Project 2:

- Validation accuracy: 92.17%
- Test accuracy: 91.78%
- Strongest class: Sports
- Weakest class: Business
- Main confusion pair: Business and Technology

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

This API has no authentication or rate limiting by default. It is acceptable for a low-risk educational demo, but a real public production API should add API keys, rate limiting, logging, and monitoring.

