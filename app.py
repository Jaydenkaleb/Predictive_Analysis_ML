import pickle
from pathlib import Path
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load your trained logistic regression model
model_path = Path("logistic_model.pkl")

with model_path.open("rb") as model_file:
    model = pickle.load(model_file)

species_names = ["setosa", "versicolor", "virginica"]


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify(error="Please provide a JSON object."), 400

    try:
        # Features must follow the same order as the Iris training data
        features = [[
            float(data["sepal_length"]),
            float(data["sepal_width"]),
            float(data["petal_length"]),
            float(data["petal_width"])
        ]]
    except (KeyError, TypeError, ValueError):
        return jsonify(
            error="Provide all four features with numeric values."
        ), 400

    prediction = int(model.predict(features)[0])

    return jsonify(
        prediction=prediction,
        species=species_names[prediction]
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)