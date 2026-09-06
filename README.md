# 🎙️ AI Accent Coach

An AI-powered pronunciation analysis system that detects a speaker's accent and evaluates pronunciation by comparing recorded speech with a reference pronunciation.

The project combines Machine Learning, audio feature extraction, Dynamic Time Warping (DTW), FastAPI, and React to provide an interactive pronunciation coaching experience.

---

## 🚀 Features

- 🎙️ Record pronunciation directly from the browser
- 📁 Upload an audio file for analysis
- 🤖 AI-based accent detection
- 🗣️ Pronunciation comparison with reference audio
- 📊 Pronunciation score
- 📐 Dynamic Time Warping (DTW) based comparison
- 💬 AI-generated pronunciation feedback
- ⏱️ Real-time recording timer
- 🔊 Audio preview
- 🔄 Try Again functionality
- ⚠️ User-friendly error handling
- 🌐 React frontend connected to FastAPI backend

---

## 🧠 How It Works

The application follows this pipeline:

```text
User Speech
     ↓
Audio Recording / Upload
     ↓
Audio Preprocessing
     ↓
Feature Extraction
     ↓
Accent Prediction
     ↓
Reference Audio Comparison
     ↓
Dynamic Time Warping (DTW)
     ↓
Pronunciation Score
     ↓
Feedback Generation
     ↓
Result Dashboard


## 🔮 Future Improvements

- Expand the reference pronunciation library to support more words
- Add multiple reference pronunciations for each word
- Improve pronunciation scoring using more advanced speech metrics
- Add phoneme-level pronunciation analysis
- Improve accent classification using a larger and more diverse dataset
- Provide detailed pronunciation visualizations
- Track pronunciation progress over time
- Deploy the application for online use