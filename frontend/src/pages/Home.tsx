import React, { useState, useEffect } from "react";
import CodeEditor from "../components/CodeEditor";
import FeedbackPanel from "../components/FeedbackPanel";
import SubmitButton from "../components/SubmitButton";
import HistoryPanel from "../components/HistoryPanel";
import axios from "axios";

// ✅ Use your Render backend in production, localhost in development
const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

const Home: React.FC = () => {
  const pageTitle = "Codementor AI";

  useEffect(() => {
    document.title = pageTitle;
  }, []);

  const [code, setCode] = useState("print('Hello, AI Assistant!')");
  const [language, setLanguage] = useState("python");
  const [feedback, setFeedback] = useState({
    errors: [],
    hints: [],
    suggestions: [],
  });
  const [history, setHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const userId = "deeksha"; // Static user for now

  // --- Submit Code ---
  const handleSubmit = async () => {
    setLoading(true);
    try {
      const res = await axios.post(`${API_URL}/submit-code`, {
        language,
        code,
        user_id: userId,
      });
      setFeedback(res.data);
      await fetchHistory(); // Reload history
    } catch (err) {
      console.error("Submission error:", err);
      alert("Error: Backend might be down or misconfigured.");
    } finally {
      setLoading(false);
    }
  };

  // --- Fetch Submission History ---
  const fetchHistory = async () => {
    try {
      const res = await axios.get(`${API_URL}/history`, {
        params: { user_id: userId },
      });
      setHistory(res.data);
    } catch (err) {
      console.error("History fetch error:", err);
    }
  };

  // --- Load history on mount ---
  useEffect(() => {
    fetchHistory();
  }, []);

  return (
    <div className="max-w-4xl mx-auto mt-10">
      <h1 className="text-3xl font-bold mb-6 text-center">{pageTitle}</h1>

      <div className="mb-4 flex items-center justify-center gap-3">
        <label className="font-semibold">Language:</label>
     <select
  value={language}
  onChange={(e) => setLanguage(e.target.value)}
  className="border p-2 rounded"
>
  <option value="python">Python</option>
  <option value="javascript">JavaScript</option>
  <option disabled>──────────</option>
  <option disabled>More languages coming soon</option>
</select>

      </div>

      <CodeEditor code={code} setCode={setCode} language={language} />
      <SubmitButton onClick={handleSubmit} loading={loading} />
      <FeedbackPanel {...feedback} />
      <HistoryPanel submissions={history} />
    </div>
  );
};

export default Home;
