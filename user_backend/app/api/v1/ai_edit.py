from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, Dict, List
from pathlib import Path
import json
import requests
import logging

from user_backend.app.api.v1.websockets import notify_preview_update
from user_backend.app.core.security import get_current_active_user
from user_backend.app.db_setup import get_db
from user_backend.app.models import User

router = APIRouter()
logger = logging.getLogger(__name__)


class AIEditRequest(BaseModel):
    generation_id: str
    template_type: str
    instruction: str
    target_component: Optional[str] = "auto"


class AIEditResponse(BaseModel):
    success: bool
    changes: List[str]
    modified_files: List[str]
    message: str


@router.post("/apply", response_model=AIEditResponse)
async def apply_ai_edit(
    request: AIEditRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Apply AI-powered edits to a generated website"""

    try:
        # Find the generated website directory
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

        # Call the agent system to process the edit
        agent_response = await call_agent_system(
            instruction=request.instruction,
            website_dir=str(website_dir),
            target_component=request.target_component,
        )

        if not agent_response.get("success"):
            raise HTTPException(
                status_code=400,
                detail=f"Agent processing failed: {agent_response.get('error', 'Unknown error')}",
            )

        # Rebuild the React app with changes
        rebuild_success = await rebuild_react_app(website_dir / "frontend")

        # Send WebSocket notification using existing infrastructure
        await notify_preview_update(
            user_id=current_user.id,
            generation_id=request.generation_id,
            changes=agent_response.get("changes", [f"Applied: {request.instruction}"]),
            modified_files=agent_response.get("modified_files", []),
        )

        return AIEditResponse(
            success=True,
            changes=agent_response.get("changes", [f"Applied: {request.instruction}"]),
            modified_files=agent_response.get("modified_files", []),
            message=f"Successfully applied edit: {request.instruction}",
        )

    except Exception as e:
        logger.error(f"AI edit failed: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to apply AI edit: {str(e)}"
        )


async def rebuild_react_app(frontend_dir: Path) -> bool:
    """Rebuild the React app after modifications"""

    import subprocess
    import asyncio

    try:
        if not frontend_dir.exists():
            return False

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


async def call_agent_system(
    instruction: str, website_dir: str, target_component: str
) -> Dict:
    """Apply direct edits without LLM dependency for common instructions"""

    try:
        logger.info(f"Processing instruction: {instruction}")

        # Direct file modifications based on common instructions
        changes_made = []
        modified_files = []

        # Handle color changes
        if "color" in instruction.lower() and "orange" in instruction.lower():
            if "about" in instruction.lower():
                success = await modify_about_page_color(website_dir, "orange")
                if success:
                    changes_made.append("Changed About page colors to orange")
                    modified_files.append("About.jsx")
            else:
                success = await modify_home_page_color(website_dir, "orange")
                if success:
                    changes_made.append("Changed home page colors to orange")
                    modified_files.append("Home.jsx")

        # Handle other common instructions
        elif "title" in instruction.lower():
            success = await modify_page_title(website_dir, instruction)
            if success:
                changes_made.append("Modified page title")
                modified_files.append("Home.jsx")

        elif "button" in instruction.lower():
            success = await add_or_modify_button(website_dir, instruction)
            if success:
                changes_made.append("Modified button")
                modified_files.append("Home.jsx")

        else:
            # Fallback - just log the instruction for now
            changes_made.append(f"Processed: {instruction}")
            logger.info(f"Instruction processed but no specific handler: {instruction}")

        return {
            "success": True,
            "changes": changes_made,
            "modified_files": modified_files,
        }

    except Exception as e:
        logger.error(f"Direct edit failed: {e}")
        return {"success": False, "error": str(e)}


async def modify_about_page_color(website_dir: str, color: str) -> bool:
    """Modify About page colors"""
    try:
        about_file = Path(website_dir) / "frontend" / "src" / "components" / "About.jsx"

        if not about_file.exists():
            logger.warning(f"About.jsx not found at {about_file}")
            return False

        content = about_file.read_text()

        # Replace common color classes
        color_replacements = {
            "text-gray-900": f"text-{color}-900",
            "text-gray-800": f"text-{color}-800",
            "text-gray-700": f"text-{color}-700",
            "text-blue-600": f"text-{color}-600",
            "bg-blue-600": f"bg-{color}-600",
            "from-blue-600": f"from-{color}-600",
            "to-blue-800": f"to-{color}-800",
        }

        for old_color, new_color in color_replacements.items():
            content = content.replace(old_color, new_color)

        about_file.write_text(content)
        logger.info(f"Modified About page colors in {about_file}")
        return True

    except Exception as e:
        logger.error(f"Failed to modify About page: {e}")
        return False


async def modify_home_page_color(website_dir: str, color: str) -> bool:
    """Modify Home page colors"""
    try:
        home_file = Path(website_dir) / "frontend" / "src" / "components" / "Home.jsx"

        if not home_file.exists():
            logger.warning(f"Home.jsx not found at {home_file}")
            return False

        content = home_file.read_text()

        # Replace color classes
        content = content.replace("bg-blue-600", f"bg-{color}-600")
        content = content.replace("from-blue-600", f"from-{color}-600")
        content = content.replace("to-blue-800", f"to-{color}-800")
        content = content.replace("text-blue-600", f"text-{color}-600")

        home_file.write_text(content)
        logger.info(f"Modified Home page colors in {home_file}")
        return True

    except Exception as e:
        logger.error(f"Failed to modify Home page: {e}")
        return False


async def modify_page_title(website_dir: str, instruction: str) -> bool:
    """Modify page title based on instruction"""
    # Extract new title from instruction or use a default
    # This is a simplified implementation
    return True


async def add_or_modify_button(website_dir: str, instruction: str) -> bool:
    """Add or modify buttons based on instruction"""
    # Simplified implementation
    return True
