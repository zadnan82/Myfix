import React, { useEffect, useMemo, useRef, useState } from "react";
import {
  browseTree,
  readProjectFile,
  writeProjectFile,
  editFileJSON,
} from "../../services/llmEditor.service";
import { apiClient } from "../../services/api";

const StatusChip = ({ status }) => {
  const cls =
    {
      pending: "bg-gray-100 text-gray-700",
      editing: "bg-blue-100 text-blue-700",
      saving: "bg-amber-100 text-amber-700",
      done: "bg-green-100 text-green-700",
      failed: "bg-red-100 text-red-700",
    }[status] || "bg-gray-100 text-gray-700";
  return <span className={`px-2 py-0.5 text-xs rounded ${cls}`}>{status}</span>;
};

const NodeRow = ({ node, level, toggle, toggleSelect }) => {
  return (
    <div
      className="flex items-center py-1 text-sm"
      style={{ paddingLeft: 8 + level * 12 }}
      title={
        node.type === "file"
          ? `${node.name} • ${node.size || 0} bytes`
          : node.name
      }
    >
      {node.type === "dir" ? (
        <button onClick={() => toggle(node)} className="w-5 text-gray-600 mr-1">
          {node.expanded ? "▾" : "▸"}
        </button>
      ) : (
        <span className="w-5 mr-1" />
      )}
      <input
        type="checkbox"
        checked={!!node.selected}
        onChange={() => toggleSelect(node)}
        className="mr-2"
      />
      <span className="truncate">{node.name}</span>
    </div>
  );
};

const flatten = (nodes, level = 0) => {
  const out = [];
  nodes.forEach((n) => {
    out.push({ node: n, level });
    if (n.type === "dir" && n.expanded && Array.isArray(n.children)) {
      out.push(...flatten(n.children, level + 1));
    }
  });
  return out;
};

const EditWithLLMBatchPage = ({ onBack, projectId: propProjectId }) => {
  const [projectId] = useState(
    propProjectId ? decodeURIComponent(String(propProjectId)) : null
  );
  const [projectBasePath, setProjectBasePath] = useState("/");
  const [rootNodes, setRootNodes] = useState([]);
  const [loadingTree, setLoadingTree] = useState(false);
  const [treeError, setTreeError] = useState("");
  const [filter, setFilter] = useState("");
  const [prompt, setPrompt] = useState("");
  const [options, setOptions] = useState({
    dryRun: false,
    systemPrompt: "",
    temperature: 0.2,
  });
  const [status, setStatus] = useState({});
  const [results, setResults] = useState({});
  const [running, setRunning] = useState(false);
  const abortRef = useRef(null);

  useEffect(() => {
    const loadRoot = async () => {
      setLoadingTree(true);
      try {
        setTreeError("");
        const base = projectId ? String(projectId) : "/";
        const nodes = await browseTree(base);
        setRootNodes(
          (nodes || []).map((n) => ({ ...n, expanded: false, selected: false }))
        );
        setProjectBasePath(base);
      } catch (e) {
        setTreeError(
          e?.getUserMessage?.() || e?.message || "Failed to load project files"
        );
      } finally {
        setLoadingTree(false);
      }
    };
    loadRoot();
  }, [projectId]);

  const toggle = async (node) => {
    if (node.type !== "dir") return;
    node.expanded = !node.expanded;
    if (node.expanded && !node.childrenLoaded) {
      try {
        const children = await browseTree(node.path);
        node.children = children || [];
        node.childrenLoaded = true;
      } catch (e) {}
    }
    setRootNodes([...rootNodes]);
  };

  const toggleSelect = (n) => {
    n.selected = !n.selected;
    setRootNodes([...rootNodes]);
  };

  const allRows = useMemo(() => flatten(rootNodes), [rootNodes]);
  const filteredRows = useMemo(() => {
    if (!filter.trim()) return allRows;
    const f = filter.toLowerCase();
    return allRows.filter(({ node }) => node.name.toLowerCase().includes(f));
  }, [allRows, filter]);

  const selectedFiles = useMemo(
    () =>
      filteredRows
        .map((r) => r.node)
        .filter((n) => n.type === "file" && n.selected)
        .map((n) => n.path),
    [filteredRows]
  );

  const runBatch = async () => {
    if (!prompt.trim() || selectedFiles.length === 0) return;
    setRunning(true);
    abortRef.current = new AbortController();
    const queue = [...selectedFiles];
    const concurrency = 3;

    const runOne = async (path) => {
      try {
        setStatus((s) => ({ ...s, [path]: "editing" }));
        const original = await readProjectFile(path);
        const res = await editFileJSON({
          path,
          content: original,
          prompt,
          options,
        });
        const updated = res?.updated_content;
        if (typeof updated !== "string") throw new Error("Invalid AI response");
        setStatus((s) => ({ ...s, [path]: "saving" }));
        if (!options.dryRun && res?.wrote_to_disk === false) {
          await writeProjectFile(path, updated);
        }
        const diffSummary = (() => {
          const oLines = String(original).split("\n").length;
          const nLines = String(updated).split("\n").length;
          return `${nLines - oLines} lines`;
        })();
        setResults((r) => ({
          ...r,
          [path]: {
            ok: true,
            usage: res.usage || null,
            diffSummary,
            editedContent: updated,
            original,
          },
        }));
        setStatus((s) => ({ ...s, [path]: "done" }));
      } catch (err) {
        setResults((r) => ({
          ...r,
          [path]: { ok: false, error: err?.message || String(err) },
        }));
        setStatus((s) => ({ ...s, [path]: "failed" }));
      }
    };

    const workers = Array.from({ length: concurrency }).map(async () => {
      while (queue.length) {
        const path = queue.shift();
        if (!path) break;
        if (abortRef.current?.aborted) break;
        await runOne(path);
      }
    });
    await Promise.all(workers);
    setRunning(false);
    abortRef.current = null;
  };

  const cancelBatch = () => {
    if (!running || !abortRef.current) return;
    abortRef.current.aborted = true;
    setRunning(false);
  };

  const exportAuditJson = () => {
    const audit = {
      timestamp: new Date().toISOString(),
      prompt,
      options,
      files: selectedFiles.map((p) => ({
        path: p,
        status: status[p] || "pending",
        usage: results[p]?.usage || null,
        diffSummary: results[p]?.diffSummary || null,
      })),
    };
    const blob = new Blob([JSON.stringify(audit, null, 2)], {
      type: "application/json",
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "edit-with-llm-audit.json";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const copySummaryMarkdown = async () => {
    const lines = [
      `# Edit with LLM Summary`,
      `- Timestamp: ${new Date().toISOString()}`,
      `- Files: ${selectedFiles.length}`,
      `- Dry Run: ${options.dryRun}`,
      `\n## Prompt\n`,
      "```",
      prompt,
      "```",
      `\n## Results`,
      ...selectedFiles.map(
        (p) =>
          `- ${status[p] || "pending"}: ${p} (${
            results[p]?.diffSummary || "n/a"
          })`
      ),
    ];
    try {
      await navigator.clipboard.writeText(lines.join("\n"));
    } catch {}
  };

  const selectedCount = selectedFiles.length;
  const canRun = selectedCount > 0 && !!prompt.trim() && !running;

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white p-4 sm:p-6">
      <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-4">
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-lg font-semibold">
              {projectId
                ? decodeURIComponent(String(projectId))
                : "All Projects"}
            </h2>
            <div
              className="text-xs text-gray-500 ml-2 truncate max-w-[50%]"
              title={projectBasePath || "/"}
            >
              Base: {projectBasePath || "/"}
            </div>
            <input
              value={filter}
              onChange={(e) => setFilter(e.target.value)}
              placeholder="Search..."
              className="border border-gray-200 rounded px-2 py-1 text-sm focus:ring-2 focus:ring-purple-100 focus:border-purple-400"
            />
          </div>
          {onBack && (
            <button
              onClick={onBack}
              className="mb-3 text-sm text-gray-600 hover:text-gray-900"
            >
              ← Back to Dashboard
            </button>
          )}
          {treeError && (
            <div className="mb-3 p-2 rounded bg-red-50 text-red-700 text-sm flex items-center justify-between">
              <span>{treeError}</span>
              <button
                className="underline"
                onClick={() => window.location.reload()}
              >
                Retry
              </button>
            </div>
          )}
          {loadingTree ? (
            <div className="text-gray-500 text-sm">Loading...</div>
          ) : (
            <div className="border rounded max-h-[60vh] overflow-auto">
              {filteredRows.map(({ node, level }) => (
                <NodeRow
                  key={node.path}
                  node={node}
                  level={level}
                  toggle={toggle}
                  toggleSelect={toggleSelect}
                />
              ))}
            </div>
          )}
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
          <h2 className="text-lg font-semibold mb-3">
            Selected Files & Prompt
          </h2>
          <div className="text-sm text-gray-600 mb-2">
            Selected: {selectedCount}
          </div>
          <textarea
            className="w-full border border-gray-200 rounded p-2 mb-2 h-32 focus:ring-2 focus:ring-purple-100 focus:border-purple-400"
            placeholder="Describe the changes you want across selected files…"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
          />
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 mb-3">
            <label className="text-sm flex items-center gap-2">
              <input
                type="checkbox"
                checked={options.dryRun}
                onChange={(e) =>
                  setOptions({ ...options, dryRun: e.target.checked })
                }
              />
              Dry Run
            </label>
            <input
              className="border rounded p-1 text-sm"
              placeholder="System prompt (optional)"
              value={options.systemPrompt}
              onChange={(e) =>
                setOptions({ ...options, systemPrompt: e.target.value })
              }
            />
            <input
              className="border rounded p-1 text-sm"
              type="number"
              step="0.1"
              min="0"
              max="1"
              placeholder="Temperature"
              value={options.temperature}
              onChange={(e) =>
                setOptions({ ...options, temperature: Number(e.target.value) })
              }
            />
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={runBatch}
              disabled={!canRun}
              className={`px-4 py-2 rounded text-white ${
                canRun ? "bg-blue-600 hover:bg-blue-700" : "bg-gray-400"
              }`}
            >
              {running ? "Running…" : "Run Edits"}
            </button>
            <button
              onClick={cancelBatch}
              disabled={!running}
              className={`px-3 py-2 rounded ${
                running
                  ? "bg-gray-200 hover:bg-gray-300"
                  : "bg-gray-100 text-gray-400"
              }`}
            >
              Cancel
            </button>
            <button
              onClick={exportAuditJson}
              className="ml-auto px-3 py-2 text-sm border rounded hover:bg-gray-50"
            >
              Export Audit
            </button>
            <button
              onClick={copySummaryMarkdown}
              className="px-3 py-2 text-sm border rounded hover:bg-gray-50"
            >
              Copy Summary
            </button>
          </div>
        </div>

        <div className="lg:col-span-2 bg-white rounded-xl shadow-sm border border-gray-100 p-4">
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-lg font-semibold">Activity & Diffs</h2>
            <div className="text-sm text-gray-600">Per-file progress</div>
          </div>
          <div className="max-h-[40vh] overflow-auto border rounded">
            {selectedFiles.map((p) => (
              <div key={p} className="border-b p-2">
                <div className="flex items-center justify-between">
                  <div className="text-sm font-mono truncate mr-2">{p}</div>
                  <StatusChip status={status[p] || "pending"} />
                </div>
                {results[p] && results[p].ok && (
                  <details className="mt-2">
                    <summary className="text-xs text-gray-600 cursor-pointer">
                      Diff summary: {results[p].diffSummary} (click to view)
                    </summary>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-2 mt-2">
                      <div>
                        <div className="text-xs text-gray-500 mb-1">
                          Original
                        </div>
                        <pre className="text-xs border rounded p-2 max-h-64 overflow-auto whitespace-pre-wrap break-words">
                          {String(results[p].original || "")}
                        </pre>
                      </div>
                      <div>
                        <div className="text-xs text-gray-500 mb-1">Edited</div>
                        <pre className="text-xs border rounded p-2 max-h-64 overflow-auto whitespace-pre-wrap break-words">
                          {String(results[p].editedContent || "")}
                        </pre>
                      </div>
                    </div>
                  </details>
                )}
                {results[p] && results[p].error && (
                  <div className="text-xs text-red-600 mt-1">
                    Error: {results[p].error}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default EditWithLLMBatchPage;
