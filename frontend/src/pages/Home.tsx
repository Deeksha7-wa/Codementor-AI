import React, { useState, useEffect } from "react";
import CodeEditor from "../components/CodeEditor";
import FeedbackPanel from "../components/FeedbackPanel";
import SubmitButton from "../components/SubmitButton";
import HistoryPanel from "../components/HistoryPanel";
import axios from "axios";

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

  // --- Submit Code (Sync SQLite backend handles saving) ---
  const handleSubmit = async () => {
    setLoading(true);
    try {
      const res = await axios.post("http://127.0.0.1:8000/submit-code", {
        language,
        code,
        user_id: userId,
      });
      setFeedback(res.data);
      await fetchHistory(); // Reload saved history from DB
    } catch (err) {
      console.error("Submission error:", err);
      alert("Error: Make sure FastAPI backend is running on port 8000");
    } finally {
      setLoading(false);
    }
  };

  // --- Fetch Submission History (from SQLite via FastAPI) ---
  const fetchHistory = async () => {
    try {
      const res = await axios.get("http://127.0.0.1:8000/history", {
        params: { user_id: userId },
      });
      setHistory(res.data);
    } catch (err) {
      console.error("History fetch error:", err);
    }
  };

  // --- Load history on component mount ---
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
          <option value="java">Java</option>
          <option value="cpp">C++</option>
          <option value="c">C</option>
          <option value="html">HTML</option>
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
