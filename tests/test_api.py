import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"

@pytest.mark.parametrize(
    "tweet, expected_sentiment",
    [
        ("I love this wonderful product", "positive"),
        ("I hate this terrible product", "negative"),
    ]
)
def test_sentiment(client, tweet, expected_sentiment):
    response = client.post("/predict", json={"tweet": tweet})

    assert response.status_code == 200
    result = response.get_json()
    assert result["sentiment"] == expected_sentiment
    assert result["tweet"] == tweet

def test_missing_tweet(client):
    response = client.post("/predict", json={})
    assert response.status_code == 400

def test_empty_tweet(client):
    response = client.post("/predict", json={"tweet": "   "})
    assert response.status_code == 400

def test_invalid_type(client):
    response = client.post("/predict", json={"tweet": 123})
    assert response.status_code == 400

def test_invalid_json(client):
    response = client.post(
        "/predict",
        data="not JSON",
        content_type="application/json"
    )
    assert response.status_code == 400
