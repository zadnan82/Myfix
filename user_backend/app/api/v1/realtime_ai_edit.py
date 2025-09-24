# user_backend/app/api/v1/realtime_ai_edit.py

import asyncio
import json
import logging
import os
from pathlib import Path
from typing import Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, WebSocket
from sqlalchemy.orm import Session
from pydantic import BaseModel

from user_backend.app.core.security import get_current_active_user
from user_backend.app.db_setup import get_db
from user_backend.app.models import User
from user_backend.app.api.v1.websockets import notify_preview_update

# Import your agent system
from agent_system.rag_integration import AgentRAGService
from agent_system.llm_editor import apply_llm_edit
from agent_system.coding_agent import solve_subtask, compile_tokens

router = APIRouter()
logger = logging.getLogger(__name__)


class RealtimeEditRequest(BaseModel):
    generation_id: str
    template_type: str
    instruction: str
    target_component: Optional[str] = "auto"
    preview_mode: str = "live"  # "live" or "built"


class RealtimeEditResponse(BaseModel):
    success: bool
    changes: List[str]
    modified_files: List[str]
    compilation_results: Dict[str, any]
    preview_updated: bool
    message: str


class RealtimeAIEditor:
    """AI editor that provides real-time preview updates"""

    def __init__(self):
        self.rag_service = AgentRAGService()
        self.active_edits = {}  # Track ongoing edits

    async def apply_realtime_edit(
        self,
        generation_id: str,
        template_type: str,
        instruction: str,
        user_id: int,
        target_component: str = "auto",
    ) -> RealtimeEditResponse:
        """Apply AI edit with real-time preview updates"""

        try:
            # 1. Find the generated website directory
            website_dir = await self._find_website_directory(
                generation_id, template_type
            )
            if not website_dir:
                raise HTTPException(
                    404, f"Generated website not found: {generation_id}"
                )

            # 2. Analyze instruction and determine target files
            target_files = await self._analyze_instruction_and_find_files(
                instruction, website_dir, target_component
            )

            changes_made = []
            modified_files = []
            compilation_results = {}

            # 3. Process each target file
            for file_info in target_files:
                file_path = file_info["path"]
                file_type = file_info["type"]  # "frontend" or "backend"

                logger.info(f"Processing {file_type} file: {file_path}")

                # Apply LLM edit to .s file
                edit_result = apply_llm_edit(
                    task=instruction,
                    file_path=str(file_path),
                    model="deepseek-coder:6.7b",
                    dry_run=False,
                    gpu_base_url=os.environ.get("GPU_AGENT_BASE_URL"),
                )

                if edit_result.success:
                    changes_made.append(f"Modified {file_path.name}: {instruction}")
                    modified_files.append(str(file_path))

                    # 4. Compile .s file to actual code
                    compilation_result = await self._compile_sevdo_file(
                        file_path, file_type, website_dir
                    )
                    compilation_results[str(file_path)] = compilation_result

                    if compilation_result["success"]:
                        # 5. Write compiled code to appropriate location
                        await self._write_compiled_code(
                            compilation_result, file_info, website_dir
                        )

            # 6. Trigger React rebuild if frontend changes
            if any("frontend" in str(f) for f in modified_files):
                rebuild_success = await self._rebuild_react_app(
                    website_dir / "frontend"
                )
                if not rebuild_success:
                    logger.warning(
                        "React rebuild failed - preview may show stale content"
                    )

            # 7. Send WebSocket notification for live preview update
            await notify_preview_update(
                user_id=user_id,
                generation_id=generation_id,
                changes=changes_made,
                modified_files=modified_files,
            )

            return RealtimeEditResponse(
                success=True,
                changes=changes_made,
                modified_files=modified_files,
                compilation_results=compilation_results,
                preview_updated=True,
                message=f"Successfully applied: {instruction}",
            )

        except Exception as e:
            logger.error(f"Realtime edit failed: {e}")
            return RealtimeEditResponse(
                success=False,
                changes=[],
                modified_files=[],
                compilation_results={},
                preview_updated=False,
                message=f"Edit failed: {str(e)}",
            )

    async def _find_website_directory(
        self, generation_id: str, template_type: str
    ) -> Optional[Path]:
        """Find the generated website directory"""
        generated_dir = Path("/app/generated_websites")

        for dir_path in generated_dir.iterdir():
            if (
                dir_path.is_dir()
                and template_type in dir_path.name
                and generation_id in dir_path.name
            ):
                return dir_path
        return None

    async def _analyze_instruction_and_find_files(
        self, instruction: str, website_dir: Path, target_component: str
    ) -> List[Dict[str, any]]:
        """Use RAG to analyze instruction and find relevant .s files to modify"""

        # Get relevant context from RAG
        context = self.rag_service.get_relevant_context(instruction)
        suggested_tokens = self.rag_service.suggest_tokens(instruction)

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
            ]
        )

        # Default to frontend if ambiguous
        if not is_backend and not is_frontend:
            is_frontend = True

        target_files = []

        # Find .s files in the appropriate directory
        if is_frontend:
            frontend_s_dir = website_dir / "frontend"
            if frontend_s_dir.exists():
                for s_file in frontend_s_dir.glob("*.s"):
                    target_files.append(
                        {"path": s_file, "type": "frontend", "tokens": suggested_tokens}
                    )

        if is_backend:
            backend_s_dir = website_dir / "backend"
            if backend_s_dir.exists():
                for s_file in backend_s_dir.glob("*.s"):
                    target_files.append(
                        {"path": s_file, "type": "backend", "tokens": suggested_tokens}
                    )

        return target_files

    async def _compile_sevdo_file(
        self, s_file_path: Path, file_type: str, website_dir: Path
    ) -> Dict[str, any]:
        """Compile .s file using SEVDO compilers"""

        try:
            # Read .s file content
            s_content = s_file_path.read_text(encoding="utf-8")

            # Compile using appropriate compiler
            if file_type == "frontend":
                import requests

                fe_base = os.environ.get(
                    "SEVDO_FRONTEND_URL", "http://sevdo-frontend:8002"
                )

                response = requests.post(
                    f"{fe_base}/api/fe-translate/to-s-direct",
                    json={
                        "dsl_content": s_content,
                        "component_name": s_file_path.stem.capitalize(),
                        "include_imports": True,
                    },
                    timeout=10,
                )

                if response.status_code == 200:
                    return {
                        "success": True,
                        "compiled_code": response.json().get("code", ""),
                        "file_type": "jsx",
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Frontend compilation failed: {response.status_code}",
                    }

            elif file_type == "backend":
                tokens = s_content.strip().split()
                be_base = os.environ.get(
                    "SEVDO_BACKEND_URL", "http://sevdo-backend:8001"
                )

                response = requests.post(
                    f"{be_base}/api/translate/to-s-direct",
                    json={"tokens": tokens, "include_imports": True},
                    timeout=10,
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
                        "error": f"Backend compilation failed: {response.status_code}",
                    }

        except Exception as e:
            return {"success": False, "error": f"Compilation error: {str(e)}"}

    async def _write_compiled_code(
        self, compilation_result: Dict, file_info: Dict, website_dir: Path
    ):
        """Write compiled code to appropriate location"""

        if not compilation_result["success"]:
            return

        compiled_code = compilation_result["compiled_code"]
        file_path = file_info["path"]
        file_type = file_info["type"]

        if file_type == "frontend":
            # Write JSX to src/components/
            component_name = file_path.stem.capitalize()
            jsx_file = (
                website_dir
                / "frontend"
                / "src"
                / "components"
                / f"{component_name}.jsx"
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

    async def _rebuild_react_app(self, frontend_dir: Path) -> bool:
        """Rebuild React app for live preview updates"""

        try:
            # Only rebuild if there's a package.json
            if not (frontend_dir / "package.json").exists():
                return True  # No rebuild needed

            logger.info("Starting React rebuild for live preview...")

            # Run npm run build
            process = await asyncio.create_subprocess_exec(
                "npm",
                "run",
                "build",
                cwd=frontend_dir,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdout, stderr = await process.communicate()

            if process.returncode == 0:
                logger.info("React app rebuilt successfully")
                return True
            else:
                logger.error(f"React build failed: {stderr.decode()}")
                return False

        except Exception as e:
            logger.error(f"React rebuild error: {e}")
            return False


# Global editor instance
realtime_editor = RealtimeAIEditor()


@router.post("/realtime-edit", response_model=RealtimeEditResponse)
async def apply_realtime_ai_edit(
    request: RealtimeEditRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Apply AI edit with real-time preview updates"""

    return await realtime_editor.apply_realtime_edit(
        generation_id=request.generation_id,
        template_type=request.template_type,
        instruction=request.instruction,
        user_id=current_user.id,
        target_component=request.target_component,
    )


@router.websocket("/realtime-edit/{generation_id}")
async def websocket_realtime_edit(
    websocket: WebSocket, generation_id: str, token: str, db: Session = Depends(get_db)
):
    """WebSocket endpoint for real-time editing session"""

    try:
        # Authenticate user (reuse existing auth)
        from user_backend.app.core.security import get_current_active_user_websocket

        user = await get_current_active_user_websocket(token, db)

        await websocket.accept()
        logger.info(f"Realtime edit WebSocket connected for {generation_id}")

        while True:
            try:
                data = await websocket.receive_text()
                message = json.loads(data)

                if message.get("type") == "apply_edit":
                    # Apply edit and send result
                    result = await realtime_editor.apply_realtime_edit(
                        generation_id=generation_id,
                        template_type=message.get("template_type", ""),
                        instruction=message.get("instruction", ""),
                        user_id=user.id,
                        target_component=message.get("target_component", "auto"),
                    )

                    await websocket.send_text(
                        json.dumps({"type": "edit_result", "data": result.dict()})
                    )

                elif message.get("type") == "preview_status":
                    # Send preview status
                    await websocket.send_text(
                        json.dumps(
                            {
                                "type": "preview_status",
                                "data": {
                                    "generation_id": generation_id,
                                    "status": "ready",
                                    "timestamp": asyncio.get_event_loop().time(),
                                },
                            }
                        )
                    )

            except json.JSONDecodeError:
                await websocket.send_text(
                    json.dumps(
                        {"type": "error", "data": {"message": "Invalid JSON message"}}
                    )
                )
            except Exception as e:
                logger.error(f"WebSocket message error: {e}")
                await websocket.send_text(
                    json.dumps(
                        {
                            "type": "error",
                            "data": {"message": f"Processing error: {str(e)}"},
                        }
                    )
                )

    except Exception as e:
        logger.error(f"WebSocket connection error: {e}")
    finally:
        logger.info(f"Realtime edit WebSocket closed for {generation_id}")
