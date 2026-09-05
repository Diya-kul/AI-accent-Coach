from fastapi import FastAPI, UploadFile, File, HTTPException
import os
import shutil

from backend.compare import dtw_distance
from backend.feedback import generate_feedback
from backend.predict import predict_accent

app = FastAPI(
    title="AI Accent Coach API",
    description="API for accent detection and pronunciation analysis",
    version="1.0"
)


# Create uploads folder if it doesn't exist
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.get("/")
def home():
    return {
        "message": "AI Accent Coach API is running!"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/analyze")
async def analyze_audio(
    word: str,
    audio: UploadFile = File(...)
):

    # Check that an audio file was uploaded
    if not audio.filename:
        raise HTTPException(
            status_code=400,
            detail="No audio file uploaded."
        )

    # Reference audio path
    ref_audio = f"data/reference/{word.lower()}.wav"

    # Check reference audio exists
    if not os.path.isfile(ref_audio):
        raise HTTPException(
            status_code=404,
            detail=f"No reference audio found for '{word}'."
        )

    # Create a path to save uploaded audio
    file_extension = os.path.splitext(audio.filename)[1]

    if not file_extension:
        file_extension = ".wav"

    user_audio_path = os.path.join(
        UPLOAD_FOLDER,
        f"user_audio{file_extension}"
    )

    # Save uploaded audio
    try:
        with open(user_audio_path, "wb") as buffer:
            shutil.copyfileobj(audio.file, buffer)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error saving audio file: {str(e)}"
        )

    try:
        # 1. Predict accent
        accent = predict_accent(user_audio_path)

        # 2. Compare pronunciation
        distance = dtw_distance(
            user_audio_path,
            ref_audio
        )

        # 3. Calculate pronunciation score
        score = max(
            0,
            100 - int(distance / 4000)
        )

        # 4. Generate feedback
        feedback = generate_feedback(distance)

        # Return results
        return {
            "word": word,
            "predicted_accent": accent,
            "pronunciation_score": score,
            "dtw_distance": round(distance, 2),
            "feedback": feedback
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing audio: {str(e)}"
        )