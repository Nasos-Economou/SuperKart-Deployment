
from flask import Flask, request, jsonify
import pandas as pd
import joblib
import io
import traceback

# Create the Flask application
superkart_api = Flask(__name__)

# Load the trained model when the app starts
# This means the model is only loaded once, not on every request
model = joblib.load("superkart_model.joblib")

@superkart_api.route("/")
def home():
    """Home endpoint - confirms the API is running"""
    return jsonify({"message": "SuperKart Sales Prediction API is running!"})


@superkart_api.post("/v1/predict")
def predict():
    """
    Single prediction endpoint.
    Accepts JSON with product features and returns the predicted sales.
    """
    try:
        # Get the JSON data from the request
        data = request.get_json()

        # Convert it to a DataFrame (the model expects a DataFrame as input)
        input_df = pd.DataFrame([data])

        # Make the prediction
        prediction = model.predict(input_df)

        # Return the result as JSON
        return jsonify({"predicted_sales": round(float(prediction[0]), 2)})

    except Exception as e:
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 400


@superkart_api.post("/v1/predictbatch")
def predict_batch():
    """
    Batch prediction endpoint.
    Accepts a CSV file with multiple products and returns predictions for all.
    """
    try:
        # Read the uploaded CSV file
        file = request.files["file"]
        data = pd.read_csv(io.StringIO(file.read().decode("utf-8")))

        # Make predictions for all rows
        predictions = model.predict(data)

        # Return predictions as a dictionary with row indices as keys
        result = {str(i): round(float(p), 2) for i, p in enumerate(predictions)}

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 400


if __name__ == "__main__":
    # Run the API on port 7860, accessible from any network interface
    superkart_api.run(host="0.0.0.0", port=7860, debug=False)
