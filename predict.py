import joblib
from features import extract_features

# LOAD MODEL FOR PREDICTION
model= joblib.load("accent_model.pkl")
scaler = joblib.load("scaler.pkl")

def predict_accent(file_path):
    
    features= extract_features(file_path)
    if features is not None:
        features= scaler.transform([features])
        prediction= model.predict(features)
    if prediction[0] == 0:
        print("Indian accent")
    elif prediction[0]==1:
        print("British accent")
    elif prediction[0]==2:
        print("American accent")
    else:
        print("Sorry unable to detect!..Try Again.")
    
