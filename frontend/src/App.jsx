import { useRef, useState } from "react";
import "./App.css";

function App() {
  const [word, setWord] = useState("hello");
  const [audio, setAudio] = useState(null);
  const [audioUrl, setAudioUrl] = useState("");
  const [isRecording, setIsRecording] = useState(false);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);
  const API_URL = import.meta.env.VITE_API_URL;

  // Start microphone recording
  const startRecording = async () => {
    try {
      setError("");
      setResult(null);

      const stream = await navigator.mediaDevices.getUserMedia({
        audio: true,
      });

      const recorder = new MediaRecorder(stream);

      mediaRecorderRef.current = recorder;
      chunksRef.current = [];

      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data);
        }
      };

      recorder.onstop = async () => {
        const blob = new Blob(chunksRef.current, {
          type: recorder.mimeType,
        });

        const wavBlob = await convertToWav(blob);

        const file = new File(
          [wavBlob],
          "recorded_audio.wav",
          { type: "audio/wav" }
        );

        setAudio(file);
        setAudioUrl(URL.createObjectURL(wavBlob));

        stream.getTracks().forEach((track) => track.stop());
      };

      recorder.start();
      setIsRecording(true);
    } catch (err) {
      setError("Microphone access was denied or unavailable.");
    }
  };

  // Stop microphone recording
  const stopRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  // Convert browser recording to WAV
  const convertToWav = async (blob) => {
    const arrayBuffer = await blob.arrayBuffer();

    const audioContext = new AudioContext();
    const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);

    const channelData = audioBuffer.getChannelData(0);

    const buffer = new ArrayBuffer(44 + channelData.length * 2);
    const view = new DataView(buffer);

    const writeString = (offset, string) => {
      for (let i = 0; i < string.length; i++) {
        view.setUint8(offset + i, string.charCodeAt(i));
      }
    };

    const write16 = (offset, value) => {
      view.setUint16(offset, value, true);
    };

    const write32 = (offset, value) => {
      view.setUint32(offset, value, true);
    };

    writeString(0, "RIFF");
    write32(4, 36 + channelData.length * 2);
    writeString(8, "WAVE");

    writeString(12, "fmt ");
    write32(16, 16);
    write16(20, 1);
    write16(22, 1);
    write32(24, audioBuffer.sampleRate);
    write32(28, audioBuffer.sampleRate * 2);
    write16(32, 2);
    write16(34, 16);

    writeString(36, "data");
    write32(40, channelData.length * 2);

    let offset = 44;

    for (let i = 0; i < channelData.length; i++) {
      const sample = Math.max(-1, Math.min(1, channelData[i]));

      view.setInt16(
        offset,
        sample < 0 ? sample * 0x8000 : sample * 0x7fff,
        true
      );

      offset += 2;
    }

    await audioContext.close();

    return new Blob([buffer], {
      type: "audio/wav",
    });
  };

  // Upload audio to backend
  const analyzeAudio = async () => {
    if (!audio) {
      setError("Please record or upload an audio file first.");
      return;
    }

    if (!word.trim()) {
      setError("Please enter a word.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    const formData = new FormData();
    formData.append("audio", audio);

    try {
  const response = await fetch(
    `${API_URL}/analyze?word=${encodeURIComponent(word.trim())}`,
    {
      method: "POST",
      body: formData,
    }
  );

  let data = {};

  try {
    data = await response.json();
  } catch {
    data = {};
  }

  if (!response.ok) {
    throw new Error(
      data.detail || `Analysis failed (${response.status}).`
    );
  }

  setResult(data);

  } catch (err) {

    if (err instanceof TypeError) {
      setError(
        "Unable to connect to the backend. Please make sure the FastAPI server is running."
      );
    } else {
      setError(
        err.message || "Something went wrong during analysis."
      );
    }

  } finally {
    setLoading(false);
  }
}

  // Upload an existing audio file
  const handleFileChange = (event) => {
    const file = event.target.files[0];

    if (!file) return;

    setAudio(file);
    setAudioUrl(URL.createObjectURL(file));
    setResult(null);
    setError("");
  };

  return (
    <div className="app">
      <header className="hero">
        <p className="badge">AI POWERED</p>

        <h1>AI Accent Coach</h1>

        <p className="subtitle">
          Practice your pronunciation and improve your accent with AI.
        </p>
      </header>

      <main className="card">
        <label>Word to practice</label>

        <input
          type="text"
          value={word}
          onChange={(e) => setWord(e.target.value)}
          placeholder="Enter a word"
        />

        <div className="record-section">
          <label>Practice pronunciation</label>

          {!isRecording ? (
            <button
              className="record-button"
              onClick={startRecording}
            >
              🎙️ Start Recording
            </button>
          ) : (
            <button
              className="stop-button"
              onClick={stopRecording}
            >
              ⏹ Stop Recording
            </button>
          )}
        </div>

        <div className="divider">
          <span>OR</span>
        </div>

        <label>Upload an audio file</label>

        <input
          type="file"
          accept="audio/*,.wav"
          onChange={handleFileChange}
        />

        {audio && (
          <div className="audio-preview">
            <p>Selected: {audio.name}</p>

            {audioUrl && (
              <audio
                controls
                src={audioUrl}
              />
            )}
          </div>
        )}

        <button
          className="analyze-button"
          onClick={analyzeAudio}
          disabled={loading || isRecording}
        >
          {loading ? "🤖 Analyzing..." : "✨ Analyze Pronunciation"}
        </button>

        {error && (
          <div className="error">
            {error}
          </div>
        )}

        {result && (
  <section className="result">
    <div className="result-header">
      <div>
        <p className="result-label">YOUR ANALYSIS</p>
        <h2>Pronunciation Results</h2>
      </div>

      <button
        className="try-again"
        onClick={() => {
          setResult(null);
          setAudio(null);
          setAudioUrl("");
          setError("");
        }}
      >
        ↻ Try Again
      </button>
    </div>

    <div className="score-section">
      <div
        className="score-circle"
        style={{
          "--score": `${result.pronunciation_score}%`,
        }}
      >
        <div className="score-inner">
          <strong>{result.pronunciation_score}</strong>
          <span>/100</span>
        </div>
      </div>

      <div className="score-text">
        <p className="result-label">PRONUNCIATION SCORE</p>

        <h3>
          {result.pronunciation_score >= 80
            ? "Great job! 🎉"
            : result.pronunciation_score >= 60
            ? "Good effort! 👍"
            : "Keep practicing! 💪"}
        </h3>

        <p>
          Your pronunciation has been analyzed using
          AI-powered accent detection and speech comparison.
        </p>
      </div>
    </div>

    <div className="result-grid">
      <div className="result-box">
        <span>Practice Word</span>
        <strong>{result.word}</strong>
      </div>

      <div className="result-box">
        <span>Detected Accent</span>
        <strong>{result.predicted_accent}</strong>
      </div>

      <div className="result-box">
        <span>DTW Distance</span>
        <strong>{result.dtw_distance}</strong>
      </div>
    </div>

    <div className="feedback">
      <div className="feedback-icon">💡</div>

      <div>
        <h3>AI Feedback</h3>
        <p>{result.feedback}</p>
      </div>
    </div>
  </section>
)}
      </main>
    </div>
  );
}

export default App;
