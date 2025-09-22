import React, { useCallback, useMemo, useState } from "react";
import { editTextFileWithLLM } from "../services/llmEditor.service";

const LLMEditorPage = ({ onBack }) => {
  const [file, setFile] = useState(null);
  const [prompt, setPrompt] = useState("");
  const [modelName, setModelName] = useState("gpt-oss:20b");
  const [systemPrompt, setSystemPrompt] = useState(
    "You are a helpful assistant."
  );
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);

  const onDrop = useCallback((event) => {
    event.preventDefault();
    event.stopPropagation();
    const dropped = event.dataTransfer?.files?.[0];
    if (dropped) {
      if (
        !dropped.name.toLowerCase().endsWith(".txt") &&
        !dropped.type.startsWith("text/")
      ) {
        setError("Please drop a .txt or text file");
        return;
      }
      setError("");
      setFile(dropped);
    }
  }, []);

  const onBrowse = useCallback((event) => {
    const f = event.target.files?.[0];
    if (f) {
      if (
        !f.name.toLowerCase().endsWith(".txt") &&
        !f.type.startsWith("text/")
      ) {
        setError("Please select a .txt or text file");
        return;
      }
      setError("");
      setFile(f);
    }
  }, []);

  const handleSubmit = useCallback(async () => {
    if (!file) {
      setError("Please select a file");
      return;
    }
    if (!prompt.trim()) {
      setError("Please enter a prompt");
      return;
    }
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const resp = await editTextFileWithLLM(file, prompt, {
        model_name: modelName,
        system_prompt: systemPrompt,
      });
      setResult(resp);
    } catch (e) {
      setError(e?.getUserMessage?.() || e?.message || "Request failed");
    } finally {
      setLoading(false);
    }
  }, [file, prompt, modelName, systemPrompt]);

  const modifiedBlobUrl = useMemo(() => {
    if (!result?.modified_code) return "";
    const blob = new Blob([result.modified_code], {
      type: "text/plain;charset=utf-8",
    });
    return URL.createObjectURL(blob);
  }, [result]);

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-3xl mx-auto bg-white rounded-xl shadow p-6">
        {onBack && (
          <button
            onClick={onBack}
            className="mb-4 px-3 py-1 text-sm text-gray-600 hover:text-gray-800 border border-gray-300 rounded hover:bg-gray-50"
          >
            ← Back to Dashboard
          </button>
        )}
        <h1 className="text-2xl font-semibold mb-4">LLM Text File Editor</h1>
        <p className="text-gray-600 mb-6">
          Upload a .txt file, enter a prompt, and get an edited version back.
        </p>

        <div
          onDrop={onDrop}
          onDragOver={(e) => {
            e.preventDefault();
            e.stopPropagation();
          }}
          className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center mb-4 bg-gray-50"
        >
          <p className="text-gray-700 mb-2">Drag & drop your .txt file here</p>
          <p className="text-gray-500 text-sm mb-3">or</p>
          <label className="inline-block px-4 py-2 bg-blue-600 text-white rounded cursor-pointer hover:bg-blue-700">
            Browse
            <input
              type="file"
              accept=".txt,text/plain"
              onChange={onBrowse}
              className="hidden"
            />
          </label>
          {file && (
            <div className="mt-3 text-sm text-gray-600">
              Selected: <span className="font-medium">{file.name}</span>
            </div>
          )}
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Prompt
          </label>
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            rows={4}
            className="w-full border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Describe the change to apply..."
          />
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Model (optional)
            </label>
            <input
              value={modelName}
              onChange={(e) => setModelName(e.target.value)}
              className="w-full border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="gpt-oss:20b"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              System Prompt (optional)
            </label>
            <input
              value={systemPrompt}
              onChange={(e) => setSystemPrompt(e.target.value)}
              className="w-full border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="You are a helpful assistant."
            />
          </div>
        </div>

        {error && (
          <div className="mb-4 p-3 rounded bg-red-50 text-red-700 text-sm">
            {error}
          </div>
        )}

        <button
          onClick={handleSubmit}
          disabled={loading}
          className={`px-4 py-2 rounded text-white ${
            loading ? "bg-gray-400" : "bg-blue-600 hover:bg-blue-700"
          }`}
        >
          {loading ? "Processing…" : "Submit"}
        </button>

        {result && (
          <div className="mt-6">
            <h2 className="text-lg font-semibold mb-2">Result</h2>
            <div className="grid grid-cols-1 gap-4">
              <div>
                <div className="text-sm text-gray-500 mb-1">
                  Modified Content
                </div>
                <pre className="whitespace-pre-wrap break-words border rounded p-3 bg-gray-50 max-h-96 overflow-auto">
                  {result.modified_code || ""}
                </pre>
                {modifiedBlobUrl && (
                  <a
                    href={modifiedBlobUrl}
                    download={
                      result.filename && result.filename.endsWith(".txt")
                        ? result.filename
                        : result.filename || "modified.txt"
                    }
                    className="inline-block mt-2 px-3 py-1 bg-green-600 text-white rounded hover:bg-green-700 text-sm"
                  >
                    Download .txt
                  </a>
                )}
              </div>
              <div>
                <div className="text-sm text-gray-500 mb-1">Metadata</div>
                <div className="text-sm text-gray-700">
                  <div>Status: {String(result.status)}</div>
                  <div>Modified: {String(result.modified)}</div>
                  <div>Replacements: {result.replacements}</div>
                  <div>Used Fallback: {String(result.used_fallback)}</div>
                  {result.message && <div>Message: {result.message}</div>}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default LLMEditorPage;
