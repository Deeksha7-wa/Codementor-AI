import React from "react";

interface HistoryPanelProps {
  submissions: any[];
}

const HistoryPanel: React.FC<HistoryPanelProps> = ({ submissions }) => {
  return (
    <div className="mt-6 border rounded p-4 bg-gray-50">
      <h2 className="font-bold mb-2 text-lg">Submission History</h2>
      {submissions.length === 0 ? (
        <p>No submissions yet.</p>
      ) : (
        submissions.map((s) => (
          <div key={s.id} className="mb-4 p-2 border rounded bg-white">
            <p><strong>Language:</strong> {s.language}</p>
            <p><strong>Code:</strong> <pre>{s.code}</pre></p>
            <p><strong>Hints:</strong> {s.hints.join(", ")}</p>
            <p><strong>Suggestions:</strong> {s.suggestions.join(", ")}</p>
            <p><strong>Timestamp:</strong> {s.timestamp}</p>
          </div>
        ))
      )}
    </div>
  );
};

export default HistoryPanel;
