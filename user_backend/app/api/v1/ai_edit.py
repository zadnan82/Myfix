# Updated user_backend/app/api/v1/ai_edit.py -    with real-time features

import asyncio
import os
import time
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, Dict, List
from pathlib import Path
import json
import requests
import logging

from user_backend.app.core.security import get_current_active_user
from user_backend.app.db_setup import get_db
from user_backend.app.models import User
from user_backend.app.api.v1.websockets import (
    notify_preview_update,
    notify_edit_session_start,
    notify_edit_session_complete,
)

# Import agent system components
from agent_system.rag_integration import AgentRAGService
from agent_system.llm_editor import apply_llm_edit

router = APIRouter()
logger = logging.getLogger(__name__)


class AIEditRequest(BaseModel):
    generation_id: str
    template_type: str
    instruction: str
    target_component: Optional[str] = "auto"
    real_time: bool = True  # Enable real-time updates


class AIEditResponse(BaseModel):
    success: bool
    changes: List[str]
    modified_files: List[str]
    compilation_results: Dict[str, any] = {}
    preview_updated: bool = False
    message: str
    session_id: Optional[str] = None


@router.post("/apply", response_model=AIEditResponse)
async def apply_ai_edit(
    request: AIEditRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Apply AI-powered edits with real-time preview updates"""

    session_id = f"{request.generation_id}_{current_user.id}_{int(time.time())}"

    try:
        # 1. Start edit session and notify watchers
        if request.real_time:
            await notify_edit_session_start(
                request.generation_id, current_user.id, request.instruction
            )

        # 2. Find the generated website directory
        generated_dir = Path("/app/generated_websites")
        website_dir = None

        for dir_path in generated_dir.iterdir():
            if (
                dir_path.is_dir()
                and request.template_type in dir_path.name
                and request.generation_id in dir_path.name
            ):
                website_dir = dir_path
                break

        if not website_dir:
            raise HTTPException(
                status_code=404,
                detail=f"Generated website not found for {request.generation_id}",
            )

        # 3. Initialize RAG service for smart file targeting
        rag_service = AgentRAGService()

        # 4. Determine target files using RAG context
        target_files = await analyze_instruction_with_rag(
            request.instruction, website_dir, rag_service, request.target_component
        )

        changes_made = []
        modified_files = []
        compilation_results = {}

        # 5. Process each target file
        for file_info in target_files:
            file_path = file_info["path"]
            file_type = file_info["type"]  # "frontend" or "backend"

            logger.info(f"Processing {file_type} file: {file_path}")

            # Apply LLM edit to .s file
            edit_result = apply_llm_edit(
                task=request.instruction,
                file_path=str(file_path),
                model="deepseek-coder:6.7b",
                dry_run=False,
                gpu_base_url=os.environ.get("GPU_AGENT_BASE_URL"),
            )

            if edit_result.success:
                changes_made.append(f"Modified {file_path.name}: {request.instruction}")
                modified_files.append(str(file_path))

                # 6. Compile .s file to actual code
                compilation_result = await compile_sevdo_file(
                    file_path, file_type, website_dir
                )
                compilation_results[str(file_path)] = compilation_result

                if compilation_result["success"]:
                    # 7. Write compiled code to appropriate location
                    await write_compiled_code(
                        compilation_result, file_info, website_dir
                    )

        # 8. Trigger React rebuild if frontend changes
        preview_updated = False
        if any("frontend" in str(f) for f in modified_files):
            rebuild_success = await rebuild_react_app(website_dir / "frontend")
            preview_updated = rebuild_success

            if not rebuild_success:
                logger.warning("React rebuild failed - preview may show stale content")

        # 9. Complete edit session and send notifications
        if request.real_time:
            await notify_edit_session_complete(
                request.generation_id,
                len(changes_made) > 0,
                changes_made,
                modified_files,
            )

        return AIEditResponse(
            success=len(changes_made) > 0,
            changes=changes_made,
            modified_files=modified_files,
            compilation_results=compilation_results,
            preview_updated=preview_updated,
            message=f"Successfully applied: {request.instruction}"
            if changes_made
            else "No changes applied",
            session_id=session_id,
        )

    except Exception as e:
        logger.error(f"AI edit failed: {e}")

        # Complete edit session with error
        if request.real_time:
            await notify_edit_session_complete(request.generation_id, False, [], [])

        raise HTTPException(
            status_code=500, detail=f"Failed to apply AI edit: {str(e)}"
        )


async def analyze_instruction_with_rag(
    instruction: str,
    website_dir: Path,
    rag_service: AgentRAGService,
    target_component: str = "auto",
) -> List[Dict]:
    """Use RAG to intelligently determine which files to modify"""

    # Get RAG context and suggested tokens
    context = rag_service.get_relevant_context(instruction)
    suggested_tokens = rag_service.suggest_tokens(instruction)

    # Determine if this is frontend or backend focused
    is_backend = any(
        keyword in instruction.lower()
        for keyword in [
            "api",
            "endpoint",
            "backend",
            "server",
            "database",
            "auth",
            "login",
            "logout",
            "session",
            "token",
        ]
    )

    is_frontend = any(
        keyword in instruction.lower()
        for keyword in [
            "color",
            "button",
            "text",
            "header",
            "page",
            "form",
            "style",
            "ui",
            "frontend",
            "layout",
            "design",
            "appearance",
            "size",
        ]
    )

    # Default to frontend if ambiguous (most user edits are UI)
    if not is_backend and not is_frontend:
        is_frontend = True

    target_files = []

    # Find relevant .s files
    if is_frontend:
        frontend_s_dir = website_dir / "frontend"
        if frontend_s_dir.exists():
            # Prioritize files based on instruction content
            for s_file in frontend_s_dir.glob("*.s"):
                # Score file relevance based on instruction keywords
                relevance_score = calculate_file_relevance(
                    s_file, instruction, suggested_tokens
                )

                if relevance_score > 0:
                    target_files.append(
                        {
                            "path": s_file,
                            "type": "frontend",
                            "relevance": relevance_score,
                            "suggested_tokens": suggested_tokens,
                        }
                    )

    if is_backend:
        backend_s_dir = website_dir / "backend"
        if backend_s_dir.exists():
            for s_file in backend_s_dir.glob("*.s"):
                relevance_score = calculate_file_relevance(
                    s_file, instruction, suggested_tokens
                )

                if relevance_score > 0:
                    target_files.append(
                        {
                            "path": s_file,
                            "type": "backend",
                            "relevance": relevance_score,
                            "suggested_tokens": suggested_tokens,
                        }
                    )

    # Sort by relevance and return top matches
    target_files.sort(key=lambda x: x["relevance"], reverse=True)

    # If no specific matches, default to common files
    if not target_files:
        if is_frontend:
            # Default to Home.s or index.s for frontend changes
            default_files = ["Home.s", "index.s", "main.s"]
            for filename in default_files:
                default_path = website_dir / "frontend" / filename
                if default_path.exists():
                    target_files.append(
                        {
                            "path": default_path,
                            "type": "frontend",
                            "relevance": 0.5,
                            "suggested_tokens": suggested_tokens,
                        }
                    )
                    break

    return target_files[:3]  # Limit to top 3 most relevant files


def calculate_file_relevance(
    s_file: Path, instruction: str, suggested_tokens: List[str]
) -> float:
    """Calculate how relevant a .s file is to the given instruction"""

    try:
        content = s_file.read_text(encoding="utf-8").lower()
        instruction_lower = instruction.lower()

        relevance_score = 0.0

        # File name relevance
        filename = s_file.stem.lower()
        if any(keyword in filename for keyword in ["home", "index", "main", "app"]):
            relevance_score += 0.3

        # Content keyword matching
        instruction_keywords = [
            "color",
            "button",
            "header",
            "nav",
            "form",
            "text",
            "title",
            "login",
            "contact",
            "about",
            "page",
        ]

        for keyword in instruction_keywords:
            if keyword in instruction_lower:
                if keyword in content or keyword in filename:
                    relevance_score += 0.2

        # Token presence
        for token in suggested_tokens:
            if token in content:
                relevance_score += 0.1

        # Specific component targeting
        if "header" in instruction_lower and ("h(" in content or "header" in filename):
            relevance_score += 0.5
        if "button" in instruction_lower and "b(" in content:
            relevance_score += 0.5
        if "form" in instruction_lower and ("f(" in content or "form" in filename):
            relevance_score += 0.5

        return min(relevance_score, 1.0)  # Cap at 1.0

    except Exception as e:
        logger.warning(f"Error calculating relevance for {s_file}: {e}")
        return 0.0


async def compile_sevdo_file(
    s_file_path: Path, file_type: str, website_dir: Path
) -> Dict:
    """Compile .s file using SEVDO compilers with error handling"""

    try:
        s_content = s_file_path.read_text(encoding="utf-8")

        if file_type == "frontend":
            fe_base = os.environ.get("SEVDO_FRONTEND_URL", "http://sevdo-frontend:8002")

            response = requests.post(
                f"{fe_base}/api/fe-translate/to-s-direct",
                json={
                    "dsl_content": s_content,
                    "component_name": s_file_path.stem.capitalize(),
                    "include_imports": True,
                },
                timeout=15,
            )

            if response.status_code == 200:
                return {
                    "success": True,
                    "compiled_code": response.json().get("code", ""),
                    "file_type": "jsx",
                    "component_name": s_file_path.stem.capitalize(),
                }
            else:
                return {
                    "success": False,
                    "error": f"Frontend compilation failed: {response.status_code} - {response.text}",
                }

        elif file_type == "backend":
            tokens = s_content.strip().split()
            be_base = os.environ.get("SEVDO_BACKEND_URL", "http://sevdo-backend:8001")

            response = requests.post(
                f"{be_base}/api/translate/to-s-direct",
                json={"tokens": tokens, "include_imports": True},
                timeout=15,
            )

            if response.status_code == 200:
                return {
                    "success": True,
                    "compiled_code": response.json().get("generated_code", ""),
                    "file_type": "py",
                }
            else:
                return {
                    "success": False,
                    "error": f"Backend compilation failed: {response.status_code} - {response.text}",
                }

    except requests.RequestException as e:
        return {
            "success": False,
            "error": f"Network error during compilation: {str(e)}",
        }
    except Exception as e:
        return {"success": False, "error": f"Compilation error: {str(e)}"}


async def write_compiled_code(
    compilation_result: Dict, file_info: Dict, website_dir: Path
):
    """Write compiled code to the appropriate location"""

    if not compilation_result["success"]:
        return

    compiled_code = compilation_result["compiled_code"]
    file_path = file_info["path"]
    file_type = file_info["type"]

    if file_type == "frontend":
        # Write JSX to src/components/
        component_name = compilation_result.get(
            "component_name", file_path.stem.capitalize()
        )
        jsx_file = (
            website_dir / "frontend" / "src" / "components" / f"{component_name}.jsx"
        )
        jsx_file.parent.mkdir(parents=True, exist_ok=True)
        jsx_file.write_text(compiled_code, encoding="utf-8")
        logger.info(f"Updated JSX component: {jsx_file}")

    elif file_type == "backend":
        # Write Python to backend/
        py_file = website_dir / "backend" / f"{file_path.stem}.py"
        py_file.parent.mkdir(parents=True, exist_ok=True)
        py_file.write_text(compiled_code, encoding="utf-8")
        logger.info(f"Updated Python file: {py_file}")


async def rebuild_react_app(frontend_dir: Path) -> bool:
    """Rebuild React app with optimized process"""

    try:
        if not (frontend_dir / "package.json").exists():
            return True  # No rebuild needed

        logger.info("Starting optimized React rebuild...")

        # Use incremental build if possible
        process = await asyncio.create_subprocess_exec(
            "npm",
            "run",
            "build",
            cwd=frontend_dir,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        # Set a reasonable timeout for rebuilds
        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=120.0,  # 2 minutes max
            )
        except asyncio.TimeoutError:
            logger.error("React build timed out after 2 minutes")
            process.kill()
            return False

        if process.returncode == 0:
            logger.info("React rebuild completed successfully")
            return True
        else:
            logger.error(f"React build failed: {stderr.decode()}")
            return False

    except Exception as e:
        logger.error(f"React rebuild error: {e}")
        return False
