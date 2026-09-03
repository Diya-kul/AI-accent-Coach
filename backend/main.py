from fastapi import FastAPI, UploadFile, File, HTTPException
import os
import shutil
import uuid

from compare import dtw_distance
from feedback import generate_feedback
from predict import predict_accent


app = FastAPI(
    title="AI Accent Coach API",
    description="API for accent detection and pronunciation analysis",
    version="1.0"
)


# Base directory of the backend
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Important folders
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
REFERENCE_FOLDER = os.path.join(BASE_DIR, "data", "reference")

# Create uploads folder if it doesn't exist
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

    # Create reference audio path
    ref_audio = os.path.join(
        REFERENCE_FOLDER,
        f"{word.lower()}.wav"
    )

    # Check if reference audio exists
    if not os.path.isfile(ref_audio):
        raise HTTPException(
            status_code=404,
            detail=f"No reference audio found for '{word}'."
        )

    # Get uploaded file extension
    file_extension = os.path.splitext(audio.filename)[1].lower()

    # Allow supported audio formats
    allowed_extensions = [".wav", ".mp3", ".m4a", ".ogg"]

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Unsupported audio format. Please upload WAV, MP3, M4A, or OGG."
        )

    # Create a unique filename
    unique_filename = f"{uuid.uuid4()}{file_extension}"

    user_audio_path = os.path.join(
        UPLOAD_FOLDER,
        unique_filename
    )

    # Save uploaded audio
    try:
        with open(user_audio_path, "wb") as buffer:
            shutil.copyfileobj(audio.file, buffer)

        # 1. Predict accent
        accent = predict_accent(user_audio_path)

        # 2. Compare pronunciation with reference
        distance = dtw_distance(
            user_audio_path,
            ref_audio
        )

        # 3. Calculate pronunciation score
        score = max(
            0,
            min(100, 100 - int(distance / 4000))
        )

        # 4. Generate feedback
        feedback = generate_feedback(distance)

        # Return results
        return {
            "word": word.lower(),
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

    finally:
        # Close the uploaded file
        await audio.close()