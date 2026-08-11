from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


class TestHealth:
    def test_returns_200(self):
        response = client.get("/health")
        assert response.status_code == 200

    def test_model_ready(self):
        data = client.get("/health").json()
        assert data["model_ready"] is True
        assert data["status"] == "ok"


class TestPredictHappyPath:
    def test_sports_article(self):
        response = client.post("/predict", json={
            "text": "Manchester United beat Chelsea 3-1 in Premier League"
        })
        assert response.status_code == 200
        assert response.json()["label"] == "Sports"
        assert response.json()["confidence"] > 0.5

    def test_technology_article(self):
        response = client.post("/predict", json={
            "text": "Apple unveils new MacBook Pro with M4 chip"
        })
        assert response.status_code == 200
        assert response.json()["label"] in ["Technology", "Business"]

    def test_probabilities_sum_to_one(self):
        response = client.post("/predict", json={
            "text": "Government announces new trade deal with the EU"
        })
        total = sum(response.json()["probabilities"].values())
        assert abs(total - 1.0) < 1e-4

    def test_response_schema(self):
        response = client.post("/predict", json={
            "text": "Stock markets fall amid rising inflation concerns"
        })
        data = response.json()
        for field in ["label", "label_id", "confidence", "probabilities"]:
            assert field in data
        assert 0 <= data["label_id"] <= 3


class TestPredictValidation:
    def test_empty_string_rejected(self):
        assert client.post("/predict", json={"text": ""}).status_code == 422

    def test_whitespace_rejected(self):
        assert client.post("/predict", json={"text": "    "}).status_code == 422

    def test_too_short_rejected(self):
        assert client.post("/predict", json={"text": "hello"}).status_code == 422

    def test_too_long_rejected(self):
        assert client.post("/predict", json={"text": "x" * 10001}).status_code == 422

    def test_missing_field_rejected(self):
        assert client.post("/predict", json={}).status_code == 422


class TestPredictEdgeCases:
    def test_minimum_valid_length(self):
        assert client.post("/predict", json={"text": "a" * 10}).status_code == 200

    def test_special_characters(self):
        response = client.post("/predict", json={
            "text": "Apple and Google face $5bn EU antitrust fine in 2024"
        })
        assert response.status_code == 200

    def test_unicode_text(self):
        response = client.post("/predict", json={
            "text": "Les marches financiers europeens ont chute aujourd hui"
        })
        assert response.status_code == 200

