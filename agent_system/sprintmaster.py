# agent_system/sprintmaster.py - FIXED VERSION
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

# CRITICAL: Use environment variable for projects root
PROJECTS_ROOT = Path(os.getenv("PROJECTS_ROOT", "/app/generated_websites"))


def discover_sevdo_files(project_name: str) -> Dict[str, str]:
    """Discover existing .s files - FIXED to use correct base path"""
    # Use absolute path from environment
    project_root = PROJECTS_ROOT / project_name

    logger.info(f"🔍 Discovering SEVDO files in: {project_root}")

    if not project_root.exists():
        logger.warning(f"⚠️ Project directory does not exist: {project_root}")
        # Try to find it with pattern matching
        for potential_dir in PROJECTS_ROOT.iterdir():
            if project_name in potential_dir.name:
                project_root = potential_dir
                logger.info(f"✅ Found project at: {project_root}")
                break

    sevdo_files = {}
    if project_root.exists():
        # Check both frontend/.s/ and backend/.s/ directories
        for s_dir in [
            project_root / "frontend" / ".s",
            project_root / "backend" / ".s",
        ]:
            if s_dir.exists():
                for file_path in s_dir.glob("*.s"):
                    try:
                        content = file_path.read_text(encoding="utf-8")
                        # Store relative path from project root
                        relative_path = str(file_path.relative_to(project_root))
                        sevdo_files[relative_path] = content
                        logger.info(f"   📄 Found: {relative_path}")
                    except Exception as e:
                        logger.warning(f"Could not read {file_path}: {e}")

    logger.info(f"✅ Discovered {len(sevdo_files)} SEVDO files")
    return sevdo_files


def plan_subtasks(
    task: str,
    project_name: str,
    model: str = "mistral:instruct",  # FIXED
) -> Dict[str, Any]:
    """Enhanced planning with correct file paths"""

    sevdo_files = discover_sevdo_files(project_name)

    if not sevdo_files:
        logger.warning("⚠️ No SEVDO files found - this might be a new project")

    # Build file context for the prompt
    file_context = ""
    if sevdo_files:
        file_context = "\n\nExisting SEVDO files in project:\n"
        for file_path, content in sevdo_files.items():
            file_context += f"- {file_path}: {content.strip()[:100]}...\n"

    system_prompt = (
        "You are a sprintmaster working with an existing SEVDO project. "
        "Break the user's task into the smallest set of absolutely necessary subtasks. "
        "For modifications to existing files, specify the exact file path relative to project root.\n\n"
        "Available file paths:\n"
        + "\n".join(f"- {path}" for path in sevdo_files.keys())
        + "\n\nRules:"
        "\n- Return 1-3 bullet points, each a short imperative phrase"
        "\n- Provide difficulty level 1-3 for each subtask"
        "\n- Provide the exact file path to modify (use paths from the list above)"
        + file_context
    )

    user_prompt = f"Task: {task}\n\nProvide focused subtasks that leverage the available patterns and tokens."

    format_schema = {
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
        base_url = os.environ.get("LLM_GATEWAY_URL", "http://192.168.16.103:8000")
        url_fc = f"{base_url}/ollama_fc"

        payload = {
            "model_name": model,
            "prompt": user_prompt,
            "system_prompt": system_prompt,
            "format": format_schema,
        }

        http_resp = requests.post(url_fc, json=payload, timeout=60)
        data = http_resp.json()
        content = data.get("content", "{}")

        subtasks_data = json.loads(content)

        # Attach file content to each subtask
        for subtask in subtasks_data.get("subtasks", []):
            file_path = subtask.get("file_path", "")
            if file_path in sevdo_files:
                subtask["file_content"] = sevdo_files[file_path]
            else:
                # Try to find closest match
                for known_path in sevdo_files:
                    if file_path in known_path or known_path in file_path:
                        subtask["file_path"] = known_path
                        subtask["file_content"] = sevdo_files[known_path]
                        break

        return {"subtasks": subtasks_data.get("subtasks", [])}

    except Exception as e:
        logger.error(f"Error calling LLM gateway: {e}")
        return {"subtasks": []}


def execute_task(
    task: str,
    project_name: str,
    master_model: str = "mistral:instruct",  # Reliable for planning
    code_model: str = "mistral:instruct",  # Only confirmed working models
) -> Dict[str, Any]:
    """Execute task with FIXED path handling"""

    rag_service = AgentRAGService()

    # Plan subtasks
    planning_result = plan_subtasks(task, project_name, model=master_model)
    subtasks = planning_result["subtasks"]

    if not subtasks:
        logger.error("❌ No subtasks generated - planning failed")
        return {
            "task": task,
            "subtasks": [],
            "results": [],
            "error": "Planning failed to generate subtasks",
        }

    logger.info(f"📋 Executing {len(subtasks)} subtasks")

    results: List[Dict[str, Any]] = []

    for i, sub in enumerate(subtasks):
        sub_description = sub.get("task", "")
        sub_content = sub.get("file_content", "")
        sub_file_path = sub.get("file_path", "")

        logger.info(f"🔄 [{i + 1}/{len(subtasks)}] {sub_description}")
        logger.info(f"   📁 Target: {sub_file_path}")

        # Execute subtask
        result = solve_subtask(
            f"{sub_description}\n\nCurrent file content:\n{sub_content}",
            rag_service,
            model=code_model,
        )

        # Build ABSOLUTE path for file writing
        absolute_file_path = PROJECTS_ROOT / project_name / sub_file_path
        result["file_path"] = str(absolute_file_path)

        logger.info(f"   💾 Writing to: {absolute_file_path}")

        # Write result to disk
        wrote = safe_write_file(str(absolute_file_path), result["output"])
        result["wrote_to_disk"] = wrote

        if wrote:
            logger.info(f"   ✅ File written successfully")
        else:
            logger.error(f"   ❌ Failed to write file")

        results.append(result)

    return {"task": task, "subtasks": subtasks, "results": results}
