import React, { useEffect, useState, useMemo } from "react";
import { apiClient } from "../../services/api";
import { browseTree } from "../../services/llmEditor.service";
import Button from "../../components/ui/Button";

const ProjectsLandingPage = ({
  onBack,
  onSelectProject,
  navigate,
  useFsProjects = true,
}) => {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [filter, setFilter] = useState("");
  const [startingPreviewId, setStartingPreviewId] = useState(null);

  useEffect(() => {
    let mounted = true;
    const fetchProjects = async () => {
      setLoading(true);
      setError("");
      try {
        if (useFsProjects) {
          const nodes = await browseTree("/");
          const dirs = (nodes || []).filter((n) => n.type === "dir");
          if (mounted)
            setProjects(
              dirs.map((d) => ({
                id: d.name,
                name: d.name,
                path: d.path,
                description: "File-system project",
                status: "active",
              }))
            );
        } else {
          const res = await apiClient.get("/api/v1/projects");
          if (mounted) setProjects(Array.isArray(res) ? res : res?.data || []);
        }
      } catch (e) {
        console.error("Failed to load projects", e);
        if (mounted) setError("Failed to load projects");
      } finally {
        if (mounted) setLoading(false);
      }
    };
    fetchProjects();
    return () => {
      mounted = false;
    };
  }, []);

  const filteredProjects = useMemo(() => {
    const f = filter.trim().toLowerCase();
    if (!f) return projects;
    return projects.filter((p) =>
      [p.name, p.description, p.project_type, p.status]
        .filter(Boolean)
        .some((v) => String(v).toLowerCase().includes(f))
    );
  }, [projects, filter]);

  const startPreview = async (projectId) => {
    try {
      setStartingPreviewId(projectId);
      const resp = await apiClient.post(
        `/api/v1/projects/${projectId}/preview`
      );
      const previewUrl = resp?.preview_url || resp?.preview?.url;
      if (previewUrl) {
        const url = previewUrl.startsWith("http")
          ? previewUrl
          : `${window.location.origin}${previewUrl}`;
        window.open(url, "_blank");
        return;
      }
      const status = await apiClient.get(
        `/api/v1/projects/${projectId}/preview`
      );
      const url = status?.details?.url;
      if (url) {
        const openUrl = url.startsWith("http")
          ? url
          : `${window.location.origin}${url}`;
        window.open(openUrl, "_blank");
      } else {
        window.open(
          `${window.location.origin}/preview/${projectId}/`,
          "_blank"
        );
      }
    } catch (e) {
      console.error("Preview failed", e);
      alert("Preview failed. See console.");
    } finally {
      setStartingPreviewId(null);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="flex items-center justify-between mb-8">
          <div>
            <div className="inline-flex items-center justify-center w-12 h-12 rounded-full bg-gradient-to-br from-purple-600 to-blue-500 text-white font-bold shadow-sm mb-3">
              S
            </div>
            <h1 className="text-3xl font-bold text-gray-900">Select Project</h1>
            <p className="text-gray-600">
              Choose a root folder to edit with LLM.
            </p>
          </div>
          {onBack && (
            <button
              onClick={onBack}
              className="inline-flex items-center text-sm text-gray-600 hover:text-gray-900"
            >
              ← Back to Dashboard
            </button>
          )}
        </div>

        <div className="mb-6 flex items-center gap-3">
          <input
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            placeholder="Search projects..."
            className="border border-gray-200 focus:border-purple-400 focus:ring-2 focus:ring-purple-100 rounded-lg px-3 py-2 w-full max-w-md transition"
          />
        </div>

        {loading && (
          <div className="bg-white shadow rounded-xl p-8 text-center text-gray-600">
            Loading projects…
          </div>
        )}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 rounded-lg p-4 mb-4">
            {error}
          </div>
        )}

        {!loading && !error && (
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {filteredProjects.map((project) => {
              const subtitle =
                project.description || project.project_type || "Project";
              const meta = [];
              if (project.generation_count > 0)
                meta.push(`${project.generation_count} gens`);
              if (project.last_generated_at) meta.push("updated");
              return (
                <div
                  key={project.id}
                  className="bg-white rounded-xl shadow-sm hover:shadow-md transition p-5 flex flex-col border border-gray-100"
                >
                  <div className="mb-2">
                    <div className="text-xs uppercase tracking-wide text-gray-500 mb-1">
                      {project.status || "active"}
                    </div>
                    <h3 className="text-lg font-semibold text-gray-900 truncate">
                      {project.name}
                    </h3>
                    <p className="text-gray-600 text-sm line-clamp-2">
                      {subtitle}
                    </p>
                    {meta.length > 0 && (
                      <div className="mt-1 text-xs text-gray-500">
                        {meta.join(" • ")}
                      </div>
                    )}
                  </div>
                  <div className="mt-auto pt-4 grid grid-cols-2 gap-3">
                    {!useFsProjects && (
                      <Button
                        variant="outline"
                        onClick={() => startPreview(project.id)}
                        disabled={startingPreviewId === project.id}
                      >
                        {startingPreviewId === project.id
                          ? "Starting…"
                          : "Preview"}
                      </Button>
                    )}
                    <Button
                      onClick={() =>
                        onSelectProject
                          ? onSelectProject(project)
                          : navigate
                          ? navigate(
                              `/edit-with-llm/${encodeURIComponent(
                                (useFsProjects ? project.path : project.id) ||
                                  project.name
                              )}`
                            )
                          : (window.location.href = `/edit-with-llm/${encodeURIComponent(
                              (useFsProjects ? project.path : project.id) ||
                                project.name
                            )}`)
                      }
                    >
                      Select Project
                    </Button>
                  </div>
                </div>
              );
            })}
            {filteredProjects.length === 0 && (
              <div className="col-span-full bg-white border rounded-xl p-10 text-center text-gray-600">
                No projects found.
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default ProjectsLandingPage;
