import os
import joblib

from features import extract_features


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "accent_model.pkl"
)

SCALER_PATH = os.path.join(
    BASE_DIR,
    "models",
    "scaler.pkl"
)


# Load model and scaler
model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)


def predict_accent(file_path):

    # Extract features
    features = extract_features(file_path)

    if features is None:
        return "Unable to process audio."

    # Scale features
    features = scaler.transform([features])

    # Predict accent
    prediction = model.predict(features)

    predicted_class = prediction[0]

    accent_map = {
        0: "Indian accent",
        1: "British accent",
        2: "American accent"
    }

    return accent_map.get(
        predicted_class,
        "Unable to detect accent"
    )