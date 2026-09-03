# Load Trained model and scaler
import joblib
from features import extract_features

# LOAD MODEL FOR PREDICTION
model= joblib.load("accent_model.pkl")
scaler = joblib.load("scaler.pkl")

def predict_accent(file_path):
    
    # Extract features from the audio
    features= extract_features(file_path)
    
    # Handle feature extraction failure
    if features is None:
        return "Unable to process audio. Try again."

    # Scaler features
    features = scaler.transform([features])
    
    #Predict accent
    prediction = model.predict(features)
        
    # Get predicted class
    predicted_class = prediction[0]
    
    # Map predicted class to accent
    if predicted_class == 0:
        return "Indian accent"
    elif predicted_class==1:
        return "British accent"
    elif predicted_class==2:
        return "American accent"
    else:
        return "Sorry unable to detect!..Try Again."