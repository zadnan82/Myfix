from typing import List, Dict, Any
import os
from pathlib import Path
import logging

import requests
import json
from user_backend.app.core.files import safe_write_file

from agent_system.coding_agent import solve_subtask
from agent_system.rag_integration import AgentRAGService

logger = logging.getLogger(__name__)


def discover_sevdo_files(project_name: str) -> Dict[str, str]:
    """Discover existing .s files in templates directory for context-aware planning."""
    project_root = Path(f"./generated_websites/{project_name}/")

    sevdo_files = {}
    if project_root.exists():
        for file_path in project_root.rglob("*.s"):
            try:
                content = file_path.read_text(encoding="utf-8")
                relative_path = str(file_path.relative_to(project_root))
                sevdo_files[relative_path] = content
            except Exception as e:
                logger.warning(f"Could not read {file_path}: {e}")

    return sevdo_files


def plan_subtasks(
    task: str, project_name: str, model: str = "llama3.2:3b"
) -> Dict[str, Any]:
    """
    Enhanced planning that uses file discovery and RAG for context-aware task decomposition.
    Returns subtasks with file context and suggested SEVDO tokens.
    """

    # Discover existing SEVDO files for context
    sevdo_files = discover_sevdo_files(project_name)

    # Build file context for the prompt
    file_context = ""
    if sevdo_files:
        file_context = "\n\nExisting SEVDO files in project:\n"
        for file_path, content in sevdo_files.items():
            file_context += f"- {file_path}: {content.strip()[:100]}...\n"
    print(file_context)
    system_prompt = (
        "You are a sprintmaster working with an existing SEVDO project. Break the user's task into "
        "the smallest set of absolutely necessary subtasks. Be very sure to be stingy with the amount of subtasks."
        "For modifications to existing files, specify the exact file path, like 'frontend/.s/Home.s' to modify separate from the task description."
        "\n\nRules:"
        "\n- Return 1-3 bullet points, each a short imperative phrase"
        "\n- Provide difficulty level 1-3 for each subtask"
        "\n- Provide the exact file path to modify"
        "\n\nSEVDO uses letters/groups for components (frontend: h,t,i,b,lf,rf; backend: l,r,m,o)"
        + file_context
    )

    user_prompt = f"Task: {task}\n\nProvide focused subtasks that leverage the available patterns and tokens."

    format = {
        "type": "object",
        "properties": {
            "subtasks": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "task": {"type": "string"},
                        "difficulty": {"type": "number"},
                        "file_path": {"type": "string"},
                    },
                },
            }
        },
    }
    try:
        base_url = os.environ.get(
            "LLM_GATEWAY_URL", "http://192.168.16.103:8000"
        )

        url_fc = f"{base_url}/ollama_fc"
        url_simple = f"{base_url}/ollama"
        payload = {
            "model_name": model,
            "prompt": user_prompt,
            "system_prompt": system_prompt,
            "format": format,
        }

        http_resp = requests.post(url_fc, json=payload, timeout=60)
        if http_resp.status_code != 200:
            http_resp = requests.post(url_simple, json=payload, timeout=60)

        data = http_resp.json()
        content = data.get("content")
        print(content)
        logger.info(content)
    except Exception as e:
        logger.error(f"Error calling LLM gateway: {e}")
        content = ""
    try:
        subtasks = json.loads(content)
        if "subtasks" not in subtasks:
            logger.warning(f"No 'subtasks' key in response: {subtasks}")
            # Fallback: create simple subtask list
        for i, sub in enumerate(subtasks["subtasks"]):
            sub_path = sub.get("file_path")

            subtasks["subtasks"][i]["file_content"] = sevdo_files[sub_path]
    except (json.JSONDecodeError, KeyError) as e:
        logger.error(f"Error parsing ollama response: {e}")
        logger.debug(f"Raw content: {content}")

    return {"subtasks": subtasks["subtasks"]}


def execute_task(
    task: str,
    project_name: str,
    master_model: str = "llama3.2:3b",
    code_model: str = "llama3.2:3b",
) -> Dict[str, Any]:
    """
    Enhanced task execution using RAG system for context-aware planning and execution.
    """
    # Initialize RAG service
    rag_service = AgentRAGService()

    # Use RAG-enhanced planning
    planning_result = plan_subtasks(task, project_name, model=master_model)
    subtasks = planning_result["subtasks"]

    # Execute subtasks with RAG context
    results: List[Dict[str, Any]] = []
    for sub in subtasks:
        sub_description = sub.get("task")
        sub_content = sub.get("file_content")

        result = solve_subtask(
            f"{sub_description}\n. This is the current file content:\n{sub_content}",
            rag_service,
            model=code_model,
        )
        result["file_path"] = (
            f"generated_websites/{project_name}/{sub.get('file_path')}"
        )

        # Write result to disk using shared helper
        wrote = safe_write_file(result["file_path"], result["output"])
        result["wrote_to_disk"] = wrote

        results.append(result)

    return {"task": task, "subtasks": subtasks, "results": results}


if __name__ == "__main__":
    discover_sevdo_files()
