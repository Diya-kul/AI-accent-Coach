import { useState } from "react";
import "./App.css";

function App() {
  const [word, setWord] = useState("hello");
  const [audio, setAudio] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const analyzeAudio = async () => {
    if (!audio) {
      setError("Please select an audio file first.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    const formData = new FormData();
    formData.append("word", word);
    formData.append("audio", audio);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/analyze?word=" + encodeURIComponent(word),
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Analysis failed.");
      }

      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="hero">
        <p className="badge">AI POWERED</p>

        <h1>AI Accent Coach</h1>

        <p className="subtitle">
          Improve your pronunciation with AI-powered accent analysis.
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

        <label>Upload your pronunciation</label>

        <input
          type="file"
          accept="audio/*,.wav"
          onChange={(e) => setAudio(e.target.files[0])}
        />

        {audio && (
          <p className="file-name">
            Selected: {audio.name}
          </p>
        )}

        <button onClick={analyzeAudio} disabled={loading}>
          {loading ? "Analyzing..." : "Analyze Pronunciation"}
        </button>

        {error && <div className="error">{error}</div>}

        {result && (
          <section className="result">
            <h2>Analysis Result</h2>

            <div className="result-grid">
              <div>
                <span>Word</span>
                <strong>{result.word}</strong>
              </div>

              <div>
                <span>Predicted Accent</span>
                <strong>{result.predicted_accent}</strong>
              </div>

              <div>
                <span>Pronunciation Score</span>
                <strong>{result.pronunciation_score}/100</strong>
              </div>

              <div>
                <span>DTW Distance</span>
                <strong>{result.dtw_distance}</strong>
              </div>
            </div>

            <div className="feedback">
              <h3>AI Feedback</h3>
              <p>{result.feedback}</p>
            </div>
          </section>
        )}
      </main>
    </div>
  );
}

export default App;