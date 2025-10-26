import React from "react";

interface FeedbackPanelProps {
  errors: string[];
  hints: string[];
  suggestions: string[];
}

const FeedbackPanel: React.FC<FeedbackPanelProps> = ({ errors, hints, suggestions }) => {
  return (
    <div className="mt-6 p-4 border rounded-lg bg-white shadow-sm">
      <h2 className="font-bold text-lg mb-3">Feedback</h2>

      {errors.length > 0 && (
        <div className="mb-3">
          <h3 className="font-semibold text-red-600">Errors:</h3>
          <ul className="list-disc list-inside text-red-700">
            {errors.map((err, i) => <li key={i}>{err}</li>)}
          </ul>
        </div>
      )}

      {hints.length > 0 && (
        <div className="mb-3">
          <h3 className="font-semibold text-blue-600">Hints:</h3>
          <ul className="list-disc list-inside text-blue-700">
            {hints.map((hint, i) => <li key={i}>{hint}</li>)}
          </ul>
        </div>
      )}

      {suggestions.length > 0 && (
        <div>
          <h3 className="font-semibold text-green-600">Suggestions:</h3>
          <ul className="list-disc list-inside text-green-700">
            {suggestions.map((sugg, i) => <li key={i}>{sugg}</li>)}
          </ul>
        </div>
      )}
    </div>
  );
};

export default FeedbackPanel;

