from fastapi import FastAPI, UploadFile, File
import librosa
import numpy as np
import joblib
import os
import uuid

app= FastAPI()

# LOAD MODEL AND SCALER
model= joblib.load("accent_model.pkl")
scaler= joblib.load("scaler.pkl")

# FEATURE EXTRACTION
def extract_features(file_path):
    try:
        audio, sr= librosa.load(file_path, sr=16000)
        
        if len(audio)==0:
            return None
        
        mfcc= librosa.feature.mfcc( y=audio, sr=sr, n_mfcc=20)
        return np.mean( mfcc.T, axis=0)
    except Exception as e:
        print("Error:",e)
        return None
    
# PREDICTION API
@app.post("/predict")
async def predict( file: UploadFile = File(...)):
    # SAVE UPLOADED FILE TEMPORARILY
    temp_file = f"temp_{uuid.uuid4().hex}.wav"
    
    with open( temp_file, "wb") as f:
        f.write( await file.read())
        
    # EXTRACT FEATURES
    features= extract_features(temp_file)
    
    # REMOVE TEMP FILE
    try:
        features = extract_features(temp_file)
    finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        
    if features is None:
        return {"error":"Invalid audio file"}
    
    # SCALE FEATURES
    features= scaler.transform([features])
    
    # PREDICT
    prediction= model.predict(features)[0]
    
    # CONVERT LABEL TO TEXT
    if prediction == 0:
        accent = "Indian"
    elif prediction == 1:
        accent = "British"
    else:
        accent = "American"
        
    return { "accent" : accent }