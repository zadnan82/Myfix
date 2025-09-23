from typing import List, Optional, Dict, Any
import json
import os
import subprocess
import asyncio
import tempfile
import threading
import time
import requests
from pathlib import Path
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import (
    FileResponse,
    HTMLResponse,
    StreamingResponse,
    RedirectResponse,
)
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
import logging
import zipfile

from user_backend.app.models import (
    Project,
    ProjectType,
    User,
)
from user_backend.app.schemas import (
    ProjectOutSchema,
    TemplateUseSchema,
)
from user_backend.app.core.security import get_current_active_user
from user_backend.app.db_setup import get_db

router = APIRouter()
logger = logging.getLogger(__name__)

# Templates directory path
TEMPLATES_DIR = Path("/app/templates")

# Global dictionary to track running React servers
active_react_servers = {}

# =============================================================================
# PYDANTIC MODELS
# =============================================================================


class TemplateStructureBackend(BaseModel):
    description: str
    files: List[str]
    features: List[str]


class TemplateStructureFrontend(BaseModel):
    description: str
    files: List[str]
    pages: Optional[Dict[str, str]] = {}


class TemplateStructure(BaseModel):
    backend: Optional[TemplateStructureBackend] = None
    frontend: Optional[TemplateStructureFrontend] = None


class TemplateInstallation(BaseModel):
    backend: Optional[str] = None
    frontend: Optional[str] = None
    customization: Optional[str] = None


class SevdoTemplateMetadata(BaseModel):
    name: str
    description: str = "No description available"
    version: str = "1.0.0"
    category: str = "general"
    author: str = "Unknown Author"
    tags: List[str] = []
    structure: Optional[TemplateStructure] = None
    required_prefabs: Optional[List[str]] = []
    customization: Optional[Dict[str, Any]] = {}
    features: Optional[List[str]] = []
    installation: Optional[TemplateInstallation] = None

    class Config:
        extra = "allow"


class TemplateOutSchema(BaseModel):
    id: str
    name: str
    description: str
    version: str
    category: str
    author: str
    tags: List[str]
    is_featured: bool
    is_public: bool
    usage_count: int
    rating: float
    structure: Optional[TemplateStructure] = None
    required_prefabs: List[str]
    customization: Dict[str, Any]
    features: List[str]
    installation: Optional[TemplateInstallation] = None
    created_at: str
    updated_at: str


class TemplateGenerateRequest(BaseModel):
    project_name: str = Field(..., min_length=1, max_length=100)
    customizations: Dict[str, Any] = Field(default_factory=dict)
    include_docker: bool = True
    include_readme: bool = True


class GenerationResult(BaseModel):
    success: bool
    project_name: str
    files_count: int
    message: str
    generation_id: str


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================


def get_template_metadata(template_dir: Path) -> Optional[SevdoTemplateMetadata]:
    """Read SEVDO template metadata from template.json"""
    metadata_file = template_dir / "template.json"

    if not metadata_file.exists():
        logger.warning(f"No template.json found in {template_dir.name}")
        return None

    try:
        with open(metadata_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        if "name" not in data:
            data["name"] = template_dir.name.replace("_", " ").title()
        if "version" not in data:
            data["version"] = "1.0.0"
        if "author" not in data:
            data["author"] = "Unknown Author"
        if "category" not in data:
            data["category"] = "general"

        return SevdoTemplateMetadata(**data)

    except Exception as e:
        logger.error(f"Error parsing template metadata {metadata_file}: {e}")
        return None


def convert_to_output_schema(
    template_id: str, metadata: SevdoTemplateMetadata
) -> TemplateOutSchema:
    """Convert SEVDO template metadata to output schema"""
    return TemplateOutSchema(
        id=template_id,
        name=metadata.name,
        description=metadata.description,
        version=metadata.version,
        category=metadata.category,
        author=metadata.author,
        tags=metadata.tags,
        is_featured=metadata.category
        in ["fitness", "real_estate", "ecommerce", "restaurant", "business"],
        is_public=True,
        usage_count=0,
        rating=min(4.5 + len(metadata.features or []) * 0.05, 5.0),
        structure=metadata.structure,
        required_prefabs=metadata.required_prefabs or [],
        customization=metadata.customization or {},
        features=metadata.features or [],
        installation=metadata.installation,
        created_at="2024-01-01T00:00:00Z",
        updated_at=datetime.now().isoformat() + "Z",
    )


def start_react_server(frontend_path: Path, generation_id: str) -> int:
    """Start a React development server and return the port"""

    # Find available port
    for port in range(3000, 3100):
        try:
            response = requests.get(f"http://localhost:{port}", timeout=1)
        except requests.exceptions.ConnectionError:
            # Port is available
            break
    else:
        raise Exception("No available ports")

    # Check if server already running for this generation
    if generation_id in active_react_servers:
        existing_port = active_react_servers[generation_id]["port"]
        try:
            response = requests.get(f"http://localhost:{existing_port}", timeout=2)
            if response.status_code == 200:
                logger.info(f"React server already running on port {existing_port}")
                return existing_port
        except:
            # Server died, remove from tracking
            del active_react_servers[generation_id]

    def run_server():
        try:
            logger.info(f"Installing npm dependencies for {generation_id}")

            # Install dependencies
            install_process = subprocess.run(
                ["npm", "install"],
                cwd=frontend_path,
                capture_output=True,
                text=True,
                timeout=120,
            )

            if install_process.returncode != 0:
                logger.error(f"npm install failed: {install_process.stderr}")
                return

            logger.info(f"Starting React server on port {port}")

            # Start React dev server
            env = os.environ.copy()
            env.update(
                {"PORT": str(port), "BROWSER": "none", "CHOKIDAR_USEPOLLING": "true"}
            )

            process = subprocess.Popen(
                ["npm", "start"],
                cwd=frontend_path,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            # Store process info
            active_react_servers[generation_id] = {
                "process": process,
                "port": port,
                "started_at": time.time(),
            }

            # Wait for process to complete
            process.wait()

        except Exception as e:
            logger.error(f"Failed to start React server: {e}")
        finally:
            # Clean up when server stops
            if generation_id in active_react_servers:
                del active_react_servers[generation_id]

    # Start server in background thread
    thread = threading.Thread(target=run_server, daemon=True)
    thread.start()

    # Wait for server to be ready (up to 60 seconds)
    for i in range(90):
        try:
            response = requests.get(f"http://localhost:{port}", timeout=2)
            if response.status_code == 200:
                logger.info(f"React server ready on port {port}")
                return port
        except:
            time.sleep(2)

    raise Exception(f"React server failed to start within 60 seconds")


# =============================================================================
# API ENDPOINTS
# =============================================================================


@router.get("/", response_model=List[TemplateOutSchema])
async def list_templates(
    category: Optional[str] = Query(None),
    featured_only: bool = Query(False),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """List available SEVDO project templates"""
    templates = []

    if not TEMPLATES_DIR.exists():
        return []

    for template_dir in TEMPLATES_DIR.iterdir():
        if template_dir.is_dir() and not template_dir.name.startswith("."):
            try:
                metadata = get_template_metadata(template_dir)
                if metadata is None:
                    continue

                template_output = convert_to_output_schema(template_dir.name, metadata)

                if category and template_output.category != category:
                    continue
                if featured_only and not template_output.is_featured:
                    continue

                templates.append(template_output)

            except Exception as e:
                logger.error(f"Error processing template {template_dir}: {e}")
                continue

    templates.sort(key=lambda x: (-int(x.is_featured), -x.rating, x.name))
    return templates[offset : offset + limit]


@router.post("/{template_name}/generate", response_model=GenerationResult)
async def generate_custom_template(
    template_name: str,
    request: TemplateGenerateRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Generate a customized website using sevdo_integrator.py"""

    template_path = TEMPLATES_DIR / template_name

    if not template_path.exists() or not template_path.is_dir():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template '{template_name}' not found",
        )

    try:
        generation_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = (
            Path("/app/generated_websites")
            / f"{template_name}_{request.project_name}_{current_user.id}_{generation_id}"
        )
        output_dir.parent.mkdir(exist_ok=True)

        env = os.environ.copy()
        env.update(
            {
                "SEVDO_PROJECT_NAME": request.project_name,
                "SEVDO_COMPANY_NAME": request.customizations.get("company_name", ""),
                "SEVDO_PRIMARY_COLOR": request.customizations.get(
                    "primary_color", "#3b82f6"
                ),
            }
        )

        logger.info(f"Generating website: {template_name} -> {output_dir}")

        cmd = ["python", "/app/sevdo_integrator.py", template_name, str(output_dir)]

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd="/app",
            env=env,
        )

        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            error = stderr.decode() if stderr else "Unknown error"
            logger.error(f"Integrator failed: {error}")
            raise HTTPException(status_code=500, detail=f"Generation failed: {error}")

        if output_dir.exists():
            file_count = len([f for f in output_dir.rglob("*") if f.is_file()])
        else:
            raise HTTPException(status_code=500, detail="Output directory not created")

        new_project = Project(
            name=request.project_name,
            description=f"Generated from {template_name} template",
            project_type=ProjectType.WEB_APP,
            user_id=current_user.id,
            config={
                "template_used": template_name,
                "generation_id": generation_id,
                "customizations": request.customizations,
                "generated_at": datetime.now().isoformat(),
                "output_directory": str(output_dir),
                "file_count": file_count,
            },
        )

        db.add(new_project)
        db.commit()
        db.refresh(new_project)

        return GenerationResult(
            success=True,
            project_name=request.project_name,
            files_count=file_count,
            message=f"Successfully generated {request.project_name} with {file_count} files",
            generation_id=generation_id,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Generation failed for {template_name}: {e}")
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


@router.get("/{template_name}/live/{generation_id}")
async def serve_live_website(template_name: str, generation_id: str):
    """Start and serve live React development server"""

    generated_dir = Path("/app/generated_websites")
    website_dir = None

    for dir_path in generated_dir.iterdir():
        if (
            dir_path.is_dir()
            and template_name in dir_path.name
            and generation_id in dir_path.name
        ):
            website_dir = dir_path
            break

    if not website_dir:
        raise HTTPException(status_code=404, detail="Website not found")

    frontend_dir = website_dir / "frontend"

    try:
        # Start React server with longer timeout and better process handling
        port = await start_react_server_async(frontend_dir, generation_id)
        live_url = f"http://localhost:{port}"
        return RedirectResponse(url=live_url, status_code=302)

    except Exception as e:
        logger.error(f"Failed to start React server: {e}")
        raise HTTPException(
            status_code=500, detail=f"Could not start live preview: {str(e)}"
        )


async def start_react_server_async(frontend_path: Path, generation_id: str) -> int:
    """Start React server with async process handling"""

    # Check if already running
    if generation_id in active_react_servers:
        existing_port = active_react_servers[generation_id]["port"]
        try:
            response = requests.get(f"http://localhost:{existing_port}", timeout=2)
            if response.status_code == 200:
                return existing_port
        except:
            del active_react_servers[generation_id]

    # Find available port
    for port in range(3000, 3100):
        try:
            requests.get(f"http://localhost:{port}", timeout=1)
        except requests.exceptions.ConnectionError:
            break
    else:
        raise Exception("No available ports")

    logger.info(f"Starting React server for {generation_id} on port {port}")

    # Install dependencies
    install_process = await asyncio.create_subprocess_exec(
        "npm",
        "install",
        cwd=frontend_path,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdout, stderr = await install_process.communicate()
    if install_process.returncode != 0:
        raise Exception(f"npm install failed: {stderr.decode()}")

    # Start React dev server
    env = os.environ.copy()
    env.update({"PORT": str(port), "BROWSER": "none"})

    process = await asyncio.create_subprocess_exec(
        "npm",
        "start",
        cwd=frontend_path,
        env=env,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    active_react_servers[generation_id] = {
        "process": process,
        "port": port,
        "started_at": time.time(),
    }

    # Wait for server to be ready (with longer timeout)
    for i in range(120):  # 4 minutes
        try:
            response = requests.get(f"http://localhost:{port}", timeout=2)
            if response.status_code == 200:
                logger.info(f"React server ready on port {port}")
                return port
        except:
            await asyncio.sleep(2)

    raise Exception("React server failed to start within timeout")


def start_production_server(frontend_path: Path, generation_id: str) -> int:
    """Start a production Express server for the built React app"""

    # Find available port
    for port in range(3000, 3100):
        try:
            response = requests.get(f"http://localhost:{port}", timeout=1)
        except requests.exceptions.ConnectionError:
            break
    else:
        raise Exception("No available ports")

    # Check if server already running
    if generation_id in active_react_servers:
        existing_port = active_react_servers[generation_id]["port"]
        try:
            response = requests.get(f"http://localhost:{existing_port}", timeout=2)
            if response.status_code == 200:
                return existing_port
        except:
            del active_react_servers[generation_id]

    def run_server():
        try:
            logger.info(
                f"Starting production server for {generation_id} on port {port}"
            )

            # Install express if needed
            subprocess.run(
                ["npm", "install"], cwd=frontend_path, capture_output=True, timeout=60
            )

            # Start production server
            env = os.environ.copy()
            env["PORT"] = str(port)

            process = subprocess.Popen(
                ["npm", "run", "serve"],
                cwd=frontend_path,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            active_react_servers[generation_id] = {
                "process": process,
                "port": port,
                "started_at": time.time(),
                "type": "production",
            }

            process.wait()

        except Exception as e:
            logger.error(f"Production server failed: {e}")
        finally:
            if generation_id in active_react_servers:
                del active_react_servers[generation_id]

    thread = threading.Thread(target=run_server, daemon=True)
    thread.start()

    # Wait for server (production servers start faster)
    for i in range(30):  # 30 seconds max
        try:
            response = requests.get(f"http://localhost:{port}", timeout=2)
            if response.status_code == 200:
                logger.info(f"Production server ready on port {port}")
                return port
        except:
            time.sleep(1)

    raise Exception("Production server failed to start")


async def serve_static_build(build_dir: Path):
    """Serve static build files directly if server fails"""
    index_file = build_dir / "index.html"

    if not index_file.exists():
        raise HTTPException(status_code=404, detail="Built React app not found")

    try:
        with open(index_file, "r", encoding="utf-8") as f:
            html_content = f.read()

        # Add base href for proper asset loading
        if "<head>" in html_content:
            base_href = f'<base href="/api/v1/templates/static/{build_dir.parent.parent.name}/">'
            html_content = html_content.replace("<head>", f"<head>\n{base_href}")

        return HTMLResponse(content=html_content)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to serve static app: {str(e)}"
        )


# Add endpoint to serve static assets from build directory
@router.get("/static/{generation_path}/{file_path:path}")
async def serve_static_assets(generation_path: str, file_path: str):
    """Serve static assets from built React app"""

    generated_dir = Path("/app/generated_websites")
    website_dir = generated_dir / generation_path
    asset_path = website_dir / "frontend" / "build" / file_path

    if not asset_path.exists():
        raise HTTPException(status_code=404, detail="Asset not found")

    # Determine media type
    media_type = "application/octet-stream"
    suffix = asset_path.suffix.lower()
    media_types = {
        ".html": "text/html",
        ".css": "text/css",
        ".js": "application/javascript",
        ".json": "application/json",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".gif": "image/gif",
        ".svg": "image/svg+xml",
        ".ico": "image/x-icon",
    }
    media_type = media_types.get(suffix, media_type)

    return FileResponse(path=asset_path, media_type=media_type)


@router.get("/{template_name}/live-status/{generation_id}")
async def get_live_website_status(template_name: str, generation_id: str):
    """Check if a React development server is running for this generation"""

    if generation_id in active_react_servers:
        server_info = active_react_servers[generation_id]
        port = server_info["port"]

        # Check if server is actually responding
        try:
            response = requests.get(f"http://localhost:{port}", timeout=5)
            if response.status_code == 200:
                return {
                    "available": True,
                    "status": "running",
                    "port": port,
                    "url": f"http://localhost:{port}",
                    "generation_id": generation_id,
                    "template_name": template_name,
                    "uptime_seconds": int(time.time() - server_info["started_at"]),
                }
        except:
            # Server not responding, remove from tracking
            del active_react_servers[generation_id]

    return {
        "available": False,
        "status": "stopped",
        "generation_id": generation_id,
        "template_name": template_name,
        "reason": "React development server not running",
    }


@router.delete("/{template_name}/stop-live/{generation_id}")
async def stop_live_website(template_name: str, generation_id: str):
    """Stop the React development server for a generation"""

    if generation_id not in active_react_servers:
        raise HTTPException(
            status_code=404, detail="No running server found for this generation"
        )

    try:
        server_info = active_react_servers[generation_id]
        process = server_info["process"]

        # Terminate the process
        process.terminate()

        # Wait for it to stop
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()

        # Remove from tracking
        del active_react_servers[generation_id]

        return {"message": f"React server stopped for generation {generation_id}"}

    except Exception as e:
        logger.error(f"Error stopping React server: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to stop React server: {str(e)}"
        )


@router.get("/{template_name}/download-generated")
async def download_generated_template(template_name: str):
    """Download the most recently generated version of a template"""

    generated_dir = Path("/app/generated_websites")

    if not generated_dir.exists():
        raise HTTPException(status_code=404, detail="No generated websites found")

    matching_dirs = [
        d for d in generated_dir.iterdir() if d.is_dir() and template_name in d.name
    ]

    if not matching_dirs:
        raise HTTPException(
            status_code=404, detail=f"No generated version of {template_name} found"
        )

    latest_dir = sorted(matching_dirs, key=lambda x: x.stat().st_mtime)[-1]

    try:
        EXCLUDE_PATTERNS = {
            "__pycache__",
            ".git",
            ".vscode",
            "node_modules",
            ".next",
            "dist",
            "build",
        }

        def should_exclude(file_path: Path) -> bool:
            return any(part in EXCLUDE_PATTERNS for part in file_path.parts)

        temp_zip = tempfile.NamedTemporaryFile(delete=False, suffix=".zip")

        with zipfile.ZipFile(temp_zip.name, "w", zipfile.ZIP_DEFLATED) as zipf:
            file_count = 0
            for file_path in latest_dir.rglob("*"):
                if file_path.is_file() and not should_exclude(file_path):
                    arc_name = file_path.relative_to(latest_dir)
                    zipf.write(file_path, arc_name)
                    file_count += 1

        def iter_file():
            try:
                with open(temp_zip.name, "rb") as file:
                    while chunk := file.read(8192):
                        yield chunk
            finally:
                try:
                    os.unlink(temp_zip.name)
                except:
                    pass

        return StreamingResponse(
            iter_file(),
            media_type="application/zip",
            headers={
                "Content-Disposition": f'attachment; filename="{template_name}-generated-website.zip"'
            },
        )

    except Exception as e:
        logger.error(f"Download failed: {e}")
        raise HTTPException(status_code=500, detail="Download failed")


@router.get("/health")
async def templates_health_check():
    """Health check for templates system"""
    template_count = 0
    if TEMPLATES_DIR.exists():
        template_count = len([d for d in TEMPLATES_DIR.iterdir() if d.is_dir()])

    return {
        "status": "healthy",
        "templates_directory": str(TEMPLATES_DIR),
        "template_count": template_count,
        "active_react_servers": len(active_react_servers),
    }
