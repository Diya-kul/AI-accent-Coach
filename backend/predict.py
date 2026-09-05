import os
import joblib
from backend.features import extract_features

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "models", "accent_model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "models", "scaler.pkl")

# Validate model and scaler files before loading
def safe_load(path, name):
    if not os.path.exists(path):
        raise FileNotFoundError(f"{name} file not found at {path}")
    if os.path.getsize(path) == 0:
        raise ValueError(f"{name} file at {path} is empty or corrupted")
    return joblib.load(path)

model = safe_load(MODEL_PATH, "Accent model")
scaler = safe_load(SCALER_PATH, "Scaler")


def predict_accent(file_path: str) -> str:
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

    return accent_map.get(predicted_class, "Unable to detect accent")
