import React, { useEffect, useState } from "react";
import CodeMirror from "@uiw/react-codemirror";
import { dracula } from "@uiw/codemirror-theme-dracula";
import { python } from "@codemirror/lang-python";
import { javascript } from "@codemirror/lang-javascript";
import { java } from "@codemirror/lang-java";
import { cpp } from "@codemirror/lang-cpp";
import { html } from "@codemirror/lang-html";

interface CodeEditorProps {
  code: string;
  setCode: (code: string) => void;
  language: string;
}

const CodeEditor: React.FC<CodeEditorProps> = ({ code, setCode, language }) => {
  const [extensions, setExtensions] = useState<any[]>([]);

  // Load language based on selected option
  useEffect(() => {
    switch (language) {
      case "python":
        setExtensions([python()]);
        break;
      case "javascript":
        setExtensions([javascript()]);
        break;
      case "java":
        setExtensions([java()]);
        break;
      case "cpp":
      case "c":
        setExtensions([cpp()]);
        break;
      case "html":
        setExtensions([html()]);
        break;
      default:
        setExtensions([]);
        break;
    }
  }, [language]);

  return (
    <div className="border rounded-lg overflow-hidden shadow-md">
      <CodeMirror
        value={code}
        height="350px"
        theme={dracula}
        extensions={extensions}
        onChange={(value) => setCode(value)}
      />
    </div>
  );
};

export default CodeEditor;

