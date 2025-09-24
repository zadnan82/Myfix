from typing import List, Dict, Any
import os
from pathlib import Path
import logging
import re

import requests
import json

from .coding_agent import solve_subtask
from .rag_integration import AgentRAGService

logger = logging.getLogger(__name__)


def discover_sevdo_files() -> Dict[str, str]:
    """Discover existing .s files in templates directory for context-aware planning."""
    project_root = Path(__file__).parent.parent
    templates_dir = project_root / "templates"

    sevdo_files = {}
    if templates_dir.exists():
        for file_path in templates_dir.rglob("*.s"):
            try:
                content = file_path.read_text(encoding="utf-8")
                relative_path = str(file_path.relative_to(project_root))
                sevdo_files[relative_path] = content
            except Exception as e:
                logger.warning(f"Could not read {file_path}: {e}")

    return sevdo_files


def generate_file_paths(task: str, model: str = "gpt-oss:20b") -> List[str]:
    """
    Generate file paths that need to be created or modified for a given task.
    Returns list of file paths (both new files and existing files to modify).
    """
    # Get existing project context
    sevdo_files = discover_sevdo_files()

    # Add file context to prompt
    file_context = ""
    if sevdo_files:
        file_context = "\n\nExisting files in project:\n"
        for file_path in sevdo_files.keys():
            file_context += f"- {file_path}\n"

    # Build system prompt
    system_prompt = (
        "You are a file path generator for SEVDO projects. Given a task, "
        "return file paths that need to be created or modified. "
        "Consider both new files and existing files that need updates."
        + file_context
    )

    # Create user prompt
    user_prompt = f"Task: {task}\n\nReturn file paths needed for this task."

    # Call LLM gateway via HTTP (same pattern as coding_agent) using JSON body
    try:
        base_url = os.environ.get(
            "LLM_GATEWAY_URL", "http://192.168.16.103:8000"
        )
        url_simple = f"{base_url}/ollama"
        payload = {
            "model": model,
            "prompt": user_prompt,
            "system_prompt": system_prompt,
        }

        http_resp = requests.post(url_simple, json=payload, timeout=60)

        data = http_resp.json()
        content = data.get("content")

        logger.debug(f"AI response: {content}")
    except Exception as e:
        logger.error(f"Error calling LLM gateway: {e}")
        return []

    # Parse file paths from content
    try:
        lines = content.strip().split("\n")
        paths = []
        for line in lines:
            line = line.strip()
            # Skip empty lines and obvious non-path lines
            if line and (
                "/" in line or ".s" in line or ".py" in line or ".jsx" in line
            ):
                # Clean up bullet points, numbers, etc
                cleaned = (
                    line.replace("- ", "")
                    .replace("* ", "")
                    .replace("1. ", "")
                    .replace("2. ", "")
                )
                cleaned = (
                    cleaned.replace("3. ", "")
                    .replace("4. ", "")
                    .replace("5. ", "")
                    .replace("6. ", "")
                )
                cleaned = cleaned.replace("File path: ", "").strip()

                # Extract path from backticks if present: `path` description -> path
                if "`" in cleaned:
                    match = re.search(r"`([^`]+)`", cleaned)
                    if match:
                        cleaned = match.group(1).strip()

                # Remove everything after first space (descriptions)
                cleaned = cleaned.split()[0] if cleaned.split() else cleaned

                if cleaned and (
                    "/" in cleaned or cleaned.endswith((".s", ".py", ".jsx"))
                ):
                    paths.append(cleaned)

        return paths
    except Exception as e:
        logger.error(f"Error parsing file paths: {e}")
        logger.debug(f"Raw content: {content}")
        # Fallback: return empty list
        return []


def plan_subtasks(task: str, model: str = "gpt-oss:20b") -> Dict[str, Any]:
    """
    Enhanced planning that uses file discovery and RAG for context-aware task decomposition.
    Returns subtasks with file context and suggested SEVDO tokens.
    """

    # Discover existing SEVDO files for context
    sevdo_files = discover_sevdo_files()

    # Build file context for the prompt
    file_context = ""
    if sevdo_files:
        file_context = "\n\nExisting SEVDO files in project:\n"
        for file_path, content in sevdo_files.items():
            file_context += f"- {file_path}: {content.strip()[:100]}...\n"
        file_context += "\nWhen modifying existing files, reference them specifically in subtasks.\n"

    system_prompt = (
        "You are a sprintmaster working with an existing SEVDO project. Break the user's task into "
        "the smallest set of absolutely necessary subtasks. For modifications to existing files, "
        "specify the exact file to modify. For new features, create specific subtasks."
        "\n\nRules:"
        "\n- Return 1-4 bullet points, each a short imperative phrase"
        "\n- Provide difficulty level 1-3 for each subtask"
        "\n- Reference specific .s files when modifying existing components"
        "\n- Use format: 'Modify {file}: change X to Y' or 'Create new component: description'"
        "\n\nSEVDO uses letters/groups for components (frontend: h,t,i,b,lf,rf; backend: l,r,m,o)"
        + file_context
    )

    user_prompt = f"Task: {task}\n\nProvide focused subtasks that leverage the available patterns and tokens."

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
        }

        http_resp = requests.post(url_fc, json=payload, timeout=60)
        if http_resp.status_code != 200:
            http_resp = requests.post(url_simple, json=payload, timeout=60)

        data = http_resp.json()
        content = data.get("content")
        print(content)
        logger.debug(content)
    except Exception as e:
        logger.error(f"Error calling LLM gateway: {e}")
        content = ""
    try:
        subtasks = json.loads(content)
        if "subtasks" not in subtasks:
            logger.warning(f"No 'subtasks' key in response: {subtasks}")
            # Fallback: create simple subtask list
            subtasks = {
                "subtasks": [
                    {"description": "Complete the task", "difficulty": 2}
                ]
            }
    except (json.JSONDecodeError, KeyError) as e:
        logger.error(f"Error parsing ollama response: {e}")
        logger.debug(f"Raw content: {content}")
        # Fallback to simple format
        subtasks = {
            "subtasks": [{"description": "Complete the task", "difficulty": 2}]
        }

    return {"subtasks": subtasks["subtasks"]}


def execute_task(
    task: str,
    master_model: str = "gpt-oss:20b",
    code_model: str = "gpt-oss:20b",
) -> Dict[str, Any]:
    """
    Enhanced task execution using RAG system for context-aware planning and execution.
    """
    # Initialize RAG service
    rag_service = AgentRAGService()

    # Use RAG-enhanced planning
    planning_result = plan_subtasks(task, model=master_model)
    subtasks = planning_result["subtasks"]

    # Execute subtasks with RAG context
    results: List[Dict[str, Any]] = []
    for sub in subtasks:
        # Handle both dict and string formats for compatibility
        if isinstance(sub, dict):
            sub_description = sub.get("task", str(sub))
        else:
            sub_description = str(sub)

        result = solve_subtask(sub_description, rag_service, model=code_model)
        # Add RAG metadata to result
        results.append(result)

    return {"task": task, "subtasks": subtasks, "results": results}
