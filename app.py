import os
from pathlib import Path

import joblib
from flask import Flask, jsonify, request

from preprocessing import clean_tweet

app = Flask(__name__)

model_path = Path(__file__).resolve().with_name("sentiment_model.joblib")
model = joblib.load(model_path)

sentiment_names = {
    0: "negative",
    2: "neutral",
    4: "positive"
}

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Send a JSON object."}), 400

    tweet = data.get("tweet")

    if not isinstance(tweet, str) or not tweet.strip():
        return jsonify({"error": "Provide a non-empty 'tweet' string."}), 400

    cleaned = clean_tweet(tweet)

    if not cleaned:
        return jsonify({"error": "Tweet contains no usable text."}), 400

    label = int(model.predict([cleaned])[0])

    return jsonify({
        "tweet": tweet,
        "prediction": label,
        "sentiment": sentiment_names[label]
    })
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "model_version": os.environ.get("MODEL_VERSION", "local")
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
