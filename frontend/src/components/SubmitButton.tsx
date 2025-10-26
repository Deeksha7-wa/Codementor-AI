import React from "react";

interface SubmitButtonProps {
  onClick: () => void;
  loading?: boolean;
}

const SubmitButton: React.FC<SubmitButtonProps> = ({ onClick, loading }) => (
  <button
    onClick={onClick}
    disabled={loading}
    className={`mt-4 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition ${
      loading ? "opacity-50 cursor-not-allowed" : ""
    }`}
  >
    {loading ? "Submitting..." : "Submit Code"}
  </button>
);

export default SubmitButton;

