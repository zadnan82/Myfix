from typing import List, Optional, Dict, Any
import json
import os
import subprocess
import asyncio
import tempfile
from pathlib import Path
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse
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

logger.info(f"Templates directory: {TEMPLATES_DIR}")
logger.info(f"Templates directory exists: {TEMPLATES_DIR.exists()}")

if TEMPLATES_DIR.exists():
    logger.info(
        f"Templates found: {[d.name for d in TEMPLATES_DIR.iterdir() if d.is_dir()]}"
    )
else:
    logger.warning(f"Templates directory does not exist: {TEMPLATES_DIR}")

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
    """Read SEVDO template metadata from template.json with better error handling"""
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

    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        logger.error(f"Error reading metadata file {metadata_file}: {e}")
        return None
    except Exception as e:
        logger.error(f"Error parsing template metadata {metadata_file}: {e}")
        return None


def determine_featured_status(
    template_id: str, metadata: SevdoTemplateMetadata
) -> bool:
    """Determine if template should be featured based on category and features"""
    featured_categories = [
        "fitness",
        "real_estate",
        "ecommerce",
        "restaurant",
        "business",
    ]

    if metadata.category in featured_categories:
        return True

    if metadata.features and len(metadata.features) > 8:
        return True

    return False


def calculate_template_rating(metadata: SevdoTemplateMetadata) -> float:
    """Calculate template rating based on features and complexity"""
    base_rating = 4.5

    if metadata.features:
        feature_bonus = min(len(metadata.features) * 0.05, 0.5)
        base_rating += feature_bonus

    if metadata.structure:
        if metadata.structure.backend and metadata.structure.frontend:
            base_rating += 0.2

    category_bonuses = {
        "fitness": 0.1,
        "real_estate": 0.2,
        "restaurant": 0.1,
        "ecommerce": 0.2,
        "business": 0.1,
    }

    base_rating += category_bonuses.get(metadata.category, 0)

    return min(base_rating, 5.0)


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
        is_featured=determine_featured_status(template_id, metadata),
        is_public=True,
        usage_count=0,
        rating=calculate_template_rating(metadata),
        structure=metadata.structure,
        required_prefabs=metadata.required_prefabs or [],
        customization=metadata.customization or {},
        features=metadata.features or [],
        installation=metadata.installation,
        created_at="2024-01-01T00:00:00Z",
        updated_at=datetime.now().isoformat() + "Z",
    )


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

    logger.info(f"Listing templates from: {TEMPLATES_DIR}")

    if not TEMPLATES_DIR.exists():
        logger.error(f"Templates directory not found: {TEMPLATES_DIR}")
        return []

    for template_dir in TEMPLATES_DIR.iterdir():
        if template_dir.is_dir() and not template_dir.name.startswith("."):
            try:
                metadata = get_template_metadata(template_dir)
                if metadata is None:
                    logger.warning(
                        f"Skipping template {template_dir.name}: no valid metadata"
                    )
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

    logger.info(f"Found {len(templates)} valid templates")

    templates.sort(key=lambda x: (-int(x.is_featured), -x.rating, x.name))

    start_idx = offset
    end_idx = offset + limit
    return templates[start_idx:end_idx]


@router.get("/{template_name}/preview")
async def get_template_preview(template_name: str):
    """Get template preview with SEVDO metadata and file contents"""
    template_path = TEMPLATES_DIR / template_name

    if not template_path.exists() or not template_path.is_dir():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template '{template_name}' not found",
        )

    try:
        logger.info(f"Loading preview for template: {template_name}")

        metadata = get_template_metadata(template_path)
        if metadata is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Template metadata is invalid",
            )

        preview_data = {
            "template_name": template_name,
            "metadata": metadata.dict(),
            "frontend": "",
            "backend": "",
            "files": {},
            "structure": [],
            "frontend_files": [],
            "backend_files": [],
        }

        if metadata.structure:
            if metadata.structure.frontend:
                preview_data["frontend_files"] = metadata.structure.frontend.files
            if metadata.structure.backend:
                preview_data["backend_files"] = metadata.structure.backend.files

        for file_path in template_path.rglob("*"):
            if file_path.is_file():
                relative_path = file_path.relative_to(template_path)
                preview_data["structure"].append(str(relative_path))

                if file_path.suffix.lower() in [
                    ".png",
                    ".jpg",
                    ".jpeg",
                    ".gif",
                    ".ico",
                    ".pdf",
                    ".zip",
                ]:
                    continue

                if file_path.stat().st_size > 1024 * 1024:
                    continue

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        preview_data["files"][str(relative_path)] = content

                        filename = file_path.name.lower()
                        relative_str = str(relative_path).lower()

                        if (
                            filename.endswith(".s")
                            or relative_str.startswith("frontend/")
                            or filename in preview_data["frontend_files"]
                        ):
                            if not preview_data["frontend"]:
                                preview_data["frontend"] = (
                                    f"// SEVDO Frontend File: {relative_path}\n{content}"
                                )

                        elif (
                            filename.endswith(".py")
                            or relative_str.startswith("backend/")
                            or filename in preview_data["backend_files"]
                        ):
                            if not preview_data["backend"]:
                                preview_data["backend"] = (
                                    f"# SEVDO Backend File: {relative_path}\n{content}"
                                )

                except UnicodeDecodeError:
                    logger.debug(f"Skipping binary file: {relative_path}")
                    continue
                except Exception as file_error:
                    logger.error(f"Error reading file {relative_path}: {file_error}")
                    continue

        preview_data.update(
            {
                "file_count": len(preview_data["files"]),
                "has_frontend": bool(preview_data["frontend"]),
                "has_backend": bool(preview_data["backend"]),
                "template_type": metadata.category,
                "version": metadata.version,
                "author": metadata.author,
                "feature_count": len(metadata.features) if metadata.features else 0,
                "prefab_count": len(metadata.required_prefabs)
                if metadata.required_prefabs
                else 0,
            }
        )

        logger.info(
            f"Preview loaded for template {template_name}: "
            f"{preview_data['file_count']} files, "
            f"frontend: {preview_data['has_frontend']}, "
            f"backend: {preview_data['has_backend']}, "
            f"features: {preview_data['feature_count']}"
        )

        return preview_data

    except Exception as e:
        logger.error(f"Error loading template preview for {template_name}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load template preview: {str(e)}",
        )


@router.get("/{template_name}/files/{file_path:path}")
async def get_template_file(template_name: str, file_path: str):
    """Get a specific file from a template"""
    template_path = TEMPLATES_DIR / template_name
    file_full_path = template_path / file_path

    if not template_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template '{template_name}' not found",
        )

    if not file_full_path.exists() or not file_full_path.is_file():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File '{file_path}' not found in template '{template_name}'",
        )

    try:
        file_full_path.resolve().relative_to(template_path.resolve())
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: file outside template directory",
        )

    try:
        with open(file_full_path, "r", encoding="utf-8") as f:
            content = f.read()

        return {
            "template_name": template_name,
            "file_path": file_path,
            "content": content,
            "size": len(content),
            "extension": file_full_path.suffix,
        }
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="File is not a text file"
        )
    except Exception as e:
        logger.error(
            f"Error reading file {file_path} from template {template_name}: {e}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to read file: {str(e)}",
        )


@router.post("/{template_name}/use", response_model=ProjectOutSchema)
async def use_template(
    template_name: str,
    template_use: TemplateUseSchema,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Create project from SEVDO template"""
    template_path = TEMPLATES_DIR / template_name

    if not template_path.exists() or not template_path.is_dir():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template '{template_name}' not found",
        )

    metadata = get_template_metadata(template_path)
    if metadata is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Template metadata is invalid",
        )

    new_project = Project(
        name=template_use.project_name,
        description=template_use.project_description or metadata.description,
        project_type=ProjectType.WEB_APP,
        tokens=metadata.required_prefabs or [],
        config={
            "template_source": template_name,
            "template_version": metadata.version,
            "template_author": metadata.author,
            "customization": metadata.customization,
            **template_use.customize_config,
        }
        if template_use.customize_config
        else {
            "template_source": template_name,
            "template_version": metadata.version,
            "template_author": metadata.author,
            "customization": metadata.customization,
        },
        user_id=current_user.id,
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return ProjectOutSchema.model_validate(new_project)


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
            detail=f"Template '{template_name}' not found. Available: {[d.name for d in TEMPLATES_DIR.iterdir() if d.is_dir() and (d / 'template.json').exists()]}",
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

        logger.info(f"🚀 Generating website: {template_name} -> {output_dir}")
        logger.info(f"Generation ID: {generation_id}")

        cmd = ["python", "/app/sevdo_integrator.py", template_name, str(output_dir)]

        logger.info(f"Running command: {' '.join(cmd)}")

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
            logger.error(f"Stdout: {stdout.decode() if stdout else 'No stdout'}")
            raise HTTPException(status_code=500, detail=f"Generation failed: {error}")

        logger.info(f"Integrator stdout: {stdout.decode() if stdout else 'No output'}")

        if output_dir.exists():
            file_count = len([f for f in output_dir.rglob("*") if f.is_file()])
        else:
            logger.error(f"Output directory not created: {output_dir}")
            raise HTTPException(
                status_code=500,
                detail="Generation completed but output directory not found",
            )

        frontend_dir = output_dir / "frontend"
        backend_dir = output_dir / "backend"

        generation_info = {
            "has_frontend": frontend_dir.exists(),
            "has_backend": backend_dir.exists(),
            "frontend_files": len(list(frontend_dir.rglob("*")))
            if frontend_dir.exists()
            else 0,
            "backend_files": len(list(backend_dir.rglob("*")))
            if backend_dir.exists()
            else 0,
        }

        logger.info(f"Generation info: {generation_info}")

        new_project = Project(
            name=request.project_name,
            description=f"Generated from {template_name} template using SEVDO integrator",
            project_type=ProjectType.WEB_APP,
            user_id=current_user.id,
            config={
                "template_used": template_name,
                "generation_id": generation_id,
                "customizations": request.customizations,
                "generated_at": datetime.now().isoformat(),
                "generation_source": "sevdo_integrator",
                "output_directory": str(output_dir),
                "file_count": file_count,
                "has_frontend": generation_info["has_frontend"],
                "has_backend": generation_info["has_backend"],
            },
        )

        db.add(new_project)
        db.commit()
        db.refresh(new_project)

        logger.info(
            f"✅ Successfully generated {template_name} for {current_user.email}: {file_count} files"
        )

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


@router.get("/{template_name}/download")
async def download_template(template_name: str):
    """Download SEVDO template as a ZIP file"""
    logger.info(f"Download request for template: {template_name}")

    template_path = TEMPLATES_DIR / template_name

    if not template_path.exists() or not template_path.is_dir():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template '{template_name}' not found",
        )

    EXCLUDE_PATTERNS = {
        "__pycache__",
        ".git",
        ".vscode",
        ".pytest_cache",
        "venv",
        "env",
        ".env",
        "node_modules",
        ".next",
        "dist",
        "build",
        "coverage",
        ".coverage",
        ".DS_Store",
        "Thumbs.db",
    }

    def should_exclude(file_path: Path) -> bool:
        """Check if file should be excluded from download"""
        path_parts = file_path.parts

        for part in path_parts:
            if part in EXCLUDE_PATTERNS:
                return True
            if part.endswith((".log", ".cache", ".tmp")):
                return True

        try:
            if file_path.stat().st_size > 10 * 1024 * 1024:
                logger.warning(
                    f"Excluding large file: {file_path} ({file_path.stat().st_size} bytes)"
                )
                return True
        except:
            pass

        return False

    try:
        temp_zip = tempfile.NamedTemporaryFile(delete=False, suffix=".zip")

        with zipfile.ZipFile(temp_zip.name, "w", zipfile.ZIP_DEFLATED) as zipf:
            file_count = 0
            excluded_count = 0

            for file_path in template_path.rglob("*"):
                if file_path.is_file():
                    if should_exclude(file_path):
                        excluded_count += 1
                        continue

                    arc_name = file_path.relative_to(template_path)
                    zipf.write(file_path, arc_name)
                    file_count += 1

            logger.info(
                f"Created ZIP with {file_count} files, excluded {excluded_count} files"
            )

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
                "Content-Disposition": f'attachment; filename="{template_name}-sevdo-template.zip"'
            },
        )

    except Exception as e:
        logger.error(f"Error creating ZIP for template {template_name}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create template download: {str(e)}",
        )


@router.get("/{template_name}/download-generated")
async def download_generated_template(template_name: str):
    """Download the most recently generated version of a template"""

    generated_dir = Path("/app/generated_websites")

    if not generated_dir.exists():
        raise HTTPException(
            status_code=404,
            detail="No generated websites found. Generate a template first.",
        )

    matching_dirs = [
        d for d in generated_dir.iterdir() if d.is_dir() and template_name in d.name
    ]

    if not matching_dirs:
        raise HTTPException(
            status_code=404,
            detail=f"No generated version of {template_name} found. Generate it first.",
        )

    latest_dir = sorted(matching_dirs, key=lambda x: x.stat().st_mtime)[-1]

    try:
        EXCLUDE_PATTERNS = {
            "__pycache__",
            ".git",
            ".vscode",
            ".pytest_cache",
            "venv",
            "env",
            ".env",
            "node_modules",
            ".next",
            "dist",
            "build",
            "coverage",
            ".coverage",
            ".DS_Store",
            "Thumbs.db",
        }

        def should_exclude(file_path: Path) -> bool:
            path_parts = file_path.parts
            for part in path_parts:
                if part in EXCLUDE_PATTERNS:
                    return True
                if part.endswith((".log", ".cache", ".tmp")):
                    return True
            return False

        temp_zip = tempfile.NamedTemporaryFile(delete=False, suffix=".zip")

        with zipfile.ZipFile(temp_zip.name, "w", zipfile.ZIP_DEFLATED) as zipf:
            file_count = 0
            for file_path in latest_dir.rglob("*"):
                if file_path.is_file() and not should_exclude(file_path):
                    arc_name = file_path.relative_to(latest_dir)
                    zipf.write(file_path, arc_name)
                    file_count += 1

            logger.info(f"Created ZIP with {file_count} files from {latest_dir}")

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


@router.get("/{template_name}/live/{generation_id}")
async def serve_live_website(template_name: str, generation_id: str):
    """Serve the generated website live in browser"""

    generated_dir = Path("/app/generated_websites")
    website_dir = None

    for dir_path in generated_dir.iterdir():
        if (
            dir_path.is_dir()
            and generation_id in dir_path.name
            and template_name in dir_path.name
        ):
            website_dir = dir_path
            break

    if not website_dir:
        logger.error(f"Generated website not found: {template_name}/{generation_id}")
        raise HTTPException(
            status_code=404,
            detail=f"Generated website not found. Generation ID: {generation_id}",
        )

    frontend_dir = website_dir / "frontend"
    index_file = frontend_dir / "public" / "index.html"

    if not index_file.exists():
        alt_index = frontend_dir / "index.html"
        if alt_index.exists():
            index_file = alt_index
        else:
            logger.error(f"Frontend index.html not found in {website_dir}")
            raise HTTPException(
                status_code=404,
                detail="Website frontend not found. The generated website may be incomplete.",
            )

    try:
        with open(index_file, "r", encoding="utf-8") as f:
            html_content = f.read()

        base_url = f"/api/v1/templates/{template_name}/live/{generation_id}/assets"

        if "<head>" in html_content:
            html_content = html_content.replace(
                "<head>", f'<head>\n    <base href="{base_url}/">'
            )

        preview_banner = (
            """
        <div style="position: fixed; top: 0; left: 0; right: 0; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); color: white; padding: 8px; text-align: center; font-size: 14px; z-index: 10000; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            🌐 Live Preview Mode - Generated with SEVDO | 
            <span style="opacity: 0.8;">Template: """
            + template_name
            + """</span>
        </div>
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                document.body.style.marginTop = '40px';
            });
        </script>
        """
        )

        if "</head>" in html_content:
            html_content = html_content.replace("</head>", preview_banner + "</head>")

        logger.info(f"Serving live website: {template_name}/{generation_id}")
        return HTMLResponse(content=html_content)

    except Exception as e:
        logger.error(f"Error serving live website {template_name}/{generation_id}: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to serve live website: {str(e)}"
        )


@router.get("/{template_name}/live/{generation_id}/assets/{file_path:path}")
async def serve_website_assets(template_name: str, generation_id: str, file_path: str):
    """Serve CSS, JS, images and other assets for the live website"""

    generated_dir = Path("/app/generated_websites")
    website_dir = None

    for dir_path in generated_dir.iterdir():
        if (
            dir_path.is_dir()
            and generation_id in dir_path.name
            and template_name in dir_path.name
        ):
            website_dir = dir_path
            break

    if not website_dir:
        raise HTTPException(status_code=404, detail="Generated website not found")

    possible_paths = [
        website_dir / "frontend" / "public" / file_path,
        website_dir / "frontend" / "src" / file_path,
        website_dir / "frontend" / file_path,
        website_dir / file_path,
    ]

    asset_path = None
    for path in possible_paths:
        if path.exists() and path.is_file():
            asset_path = path
            break

    if not asset_path:
        logger.warning(f"Asset not found: {file_path} in {website_dir}")
        raise HTTPException(status_code=404, detail=f"Asset '{file_path}' not found")

    try:
        asset_path.resolve().relative_to(website_dir.resolve())
    except ValueError:
        logger.warning(
            f"Security violation: attempt to access {asset_path} outside {website_dir}"
        )
        raise HTTPException(
            status_code=403, detail="Access denied: asset outside website directory"
        )

    media_type = "application/octet-stream"
    suffix = asset_path.suffix.lower()

    media_types = {
        ".html": "text/html",
        ".css": "text/css",
        ".js": "application/javascript",
        ".json": "application/json",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".svg": "image/svg+xml",
        ".ico": "image/x-icon",
        ".woff": "font/woff",
        ".woff2": "font/woff2",
        ".ttf": "font/ttf",
        ".eot": "application/vnd.ms-fontobject",
    }

    media_type = media_types.get(suffix, media_type)

    try:
        logger.debug(f"Serving asset: {file_path} as {media_type}")
        return FileResponse(
            path=asset_path, media_type=media_type, filename=asset_path.name
        )

    except Exception as e:
        logger.error(f"Error serving asset {file_path}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to serve asset: {str(e)}")


@router.get("/{template_name}/live-status/{generation_id}")
async def get_live_website_status(template_name: str, generation_id: str):
    """Check if a generated website is available for live preview"""

    generated_dir = Path("/app/generated_websites")
    website_dir = None

    for dir_path in generated_dir.iterdir():
        if (
            dir_path.is_dir()
            and generation_id in dir_path.name
            and template_name in dir_path.name
        ):
            website_dir = dir_path
            break

    if not website_dir:
        return {
            "available": False,
            "reason": "Website directory not found",
            "generation_id": generation_id,
            "template_name": template_name,
        }

    frontend_dir = website_dir / "frontend"
    index_file = frontend_dir / "public" / "index.html"

    if not index_file.exists():
        index_file = frontend_dir / "index.html"

    analysis = {
        "available": index_file.exists(),
        "has_frontend": frontend_dir.exists(),
        "has_backend": (website_dir / "backend").exists(),
        "has_index": index_file.exists(),
        "index_path": str(index_file) if index_file.exists() else None,
        "file_count": len(list(website_dir.rglob("*"))) if website_dir.exists() else 0,
        "generation_id": generation_id,
        "template_name": template_name,
        "website_path": str(website_dir),
        "live_url": f"/api/v1/templates/{template_name}/live/{generation_id}"
        if index_file.exists()
        else None,
    }

    if not analysis["available"]:
        analysis["reason"] = "Frontend index.html not found"

    return analysis


@router.get("/generated-status")
async def get_generated_status():
    """Get status of generated websites"""

    generated_dir = Path("/app/generated_websites")
    integrator_path = Path("/app/sevdo_integrator.py")

    generated_websites = []
    if generated_dir.exists():
        for website_dir in generated_dir.iterdir():
            if website_dir.is_dir():
                file_count = len([f for f in website_dir.rglob("*") if f.is_file()])
                generated_websites.append(
                    {
                        "name": website_dir.name,
                        "created": datetime.fromtimestamp(
                            website_dir.stat().st_mtime
                        ).isoformat(),
                        "file_count": file_count,
                        "has_frontend": (website_dir / "frontend").exists(),
                        "has_backend": (website_dir / "backend").exists(),
                    }
                )

    return {
        "templates_directory": str(TEMPLATES_DIR),
        "templates_exist": TEMPLATES_DIR.exists(),
        "integrator_exists": integrator_path.exists(),
        "sevdo_frontend_exists": Path("/app/sevdo_frontend").exists(),
        "sevdo_backend_exists": Path("/app/sevdo_backend").exists(),
        "generated_directory": str(generated_dir),
        "generated_websites": generated_websites,
        "total_generated": len(generated_websites),
        "available_templates": [
            d.name
            for d in TEMPLATES_DIR.iterdir()
            if d.is_dir() and (d / "template.json").exists()
        ],
        "status": "ready" if integrator_path.exists() else "integrator_missing",
    }


@router.get("/health")
async def templates_health_check():
    """Health check for SEVDO templates system"""
    template_info = []
    valid_templates = 0

    if TEMPLATES_DIR.exists():
        for template_dir in TEMPLATES_DIR.iterdir():
            if template_dir.is_dir():
                metadata = get_template_metadata(template_dir)
                files = list(template_dir.glob("*"))

                template_status = {
                    "name": template_dir.name,
                    "has_metadata": metadata is not None,
                    "file_count": len(files),
                    "files": [f.name for f in files[:5]],
                }

                if metadata:
                    valid_templates += 1
                    template_status.update(
                        {
                            "template_name": metadata.name,
                            "category": metadata.category,
                            "version": metadata.version,
                            "author": metadata.author,
                            "feature_count": len(metadata.features)
                            if metadata.features
                            else 0,
                            "prefab_count": len(metadata.required_prefabs)
                            if metadata.required_prefabs
                            else 0,
                        }
                    )

                template_info.append(template_status)

    return {
        "status": "healthy" if valid_templates > 0 else "warning",
        "templates_directory": str(TEMPLATES_DIR),
        "directory_exists": TEMPLATES_DIR.exists(),
        "total_directories": len(template_info),
        "valid_templates": valid_templates,
        "template_details": template_info,
        "sevdo_format": "SEVDO template format with structure, prefabs, and customization",
    }


@router.get("/{template_name}", response_model=TemplateOutSchema)
async def get_template(template_name: str):
    """Get a single SEVDO template by name"""
    template_path = TEMPLATES_DIR / template_name

    if not template_path.exists() or not template_path.is_dir():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template '{template_name}' not found",
        )

    try:
        metadata = get_template_metadata(template_path)
        if metadata is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Template metadata is invalid",
            )

        return convert_to_output_schema(template_name, metadata)

    except Exception as e:
        logger.error(f"Error loading template {template_name}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load template: {str(e)}",
        )


@router.get("/{template_name}/live-preview")
async def get_template_live_preview(template_name: str):
    """Serve the live preview of a SEVDO template"""
    template_path = TEMPLATES_DIR / template_name

    if not template_path.exists() or not template_path.is_dir():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template '{template_name}' not found",
        )

    metadata = get_template_metadata(template_path)
    if metadata is None:
        return HTMLResponse(
            content=create_error_page(template_name, "Invalid template metadata"),
            status_code=500,
        )

    try:
        sevdo_files = list(template_path.glob("frontend/*.s"))

        if not sevdo_files:
            sevdo_files = list(template_path.glob("*.s"))

        home_file = None
        for file_path in sevdo_files:
            filename = file_path.stem.lower()
            if filename in ["home", "hem", "index", "main"]:
                home_file = file_path
                break

        if not home_file and sevdo_files:
            home_file = sevdo_files[0]

        if home_file:
            with open(home_file, "r", encoding="utf-8") as f:
                sevdo_content = f.read()

            html_content = create_sevdo_preview_html(
                template_name, metadata, sevdo_content, sevdo_files
            )
            return HTMLResponse(content=html_content)
        else:
            return HTMLResponse(
                content=create_template_info_page(template_name, metadata)
            )

    except Exception as e:
        logger.error(f"Error serving live preview for {template_name}: {e}")
        return HTMLResponse(
            content=create_error_page(template_name, str(e)), status_code=500
        )


@router.get("/{template_name}/assets/{file_path:path}")
async def get_template_asset(template_name: str, file_path: str):
    """Get static assets (CSS, JS, images) for template live preview"""
    template_path = TEMPLATES_DIR / template_name
    asset_path = template_path / file_path

    if not template_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template '{template_name}' not found",
        )

    if not asset_path.exists() or not asset_path.is_file():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Asset '{file_path}' not found in template '{template_name}'",
        )

    try:
        asset_path.resolve().relative_to(template_path.resolve())
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: asset outside template directory",
        )

    media_type = "application/octet-stream"
    if asset_path.suffix == ".css":
        media_type = "text/css"
    elif asset_path.suffix == ".js":
        media_type = "application/javascript"
    elif asset_path.suffix in [".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg"]:
        media_type = f"image/{asset_path.suffix[1:]}"

    try:
        return FileResponse(asset_path, media_type=media_type)
    except Exception as e:
        logger.error(
            f"Error serving asset {file_path} from template {template_name}: {e}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to serve asset: {str(e)}",
        )


# =============================================================================
# PREVIEW HTML GENERATION FUNCTIONS
# =============================================================================


def create_sevdo_preview_html(
    template_name: str,
    metadata: SevdoTemplateMetadata,
    sevdo_content: str,
    all_files: list,
) -> str:
    """Create HTML preview from SEVDO content"""

    nav_items = extract_navigation(sevdo_content)
    page_sections = parse_sevdo_content(sevdo_content)

    page_links = ""
    for file_path in all_files:
        page_name = file_path.stem
        page_links += (
            f'<a href="#{page_name.lower()}" class="page-link">{page_name}</a> '
        )

    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{metadata.name} - Live Preview</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                line-height: 1.6; color: #333; background: #f8fafc;
            }}
            .preview-header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white; padding: 1rem; text-align: center;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            .preview-header h1 {{ font-size: 1.8rem; margin-bottom: 0.5rem; }}
            .preview-header p {{ opacity: 0.9; font-size: 0.9rem; }}
            .preview-nav {{
                background: white; padding: 1rem; border-bottom: 1px solid #e5e7eb;
                text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }}
            .page-link {{
                display: inline-block; margin: 0 0.5rem; padding: 0.5rem 1rem;
                background: #f3f4f6; color: #374151; text-decoration: none;
                border-radius: 6px; transition: all 0.2s;
            }}
            .page-link:hover {{ background: #e5e7eb; }}
            .page-link.active {{ background: #3b82f6; color: white; }}
            .content {{ max-width: 1200px; margin: 2rem auto; padding: 0 1rem; }}
            .section {{ 
                background: white; margin-bottom: 2rem; padding: 2rem; 
                border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }}
            .section h2 {{ 
                color: #1f2937; margin-bottom: 1rem; font-size: 1.5rem;
                border-bottom: 2px solid #e5e7eb; padding-bottom: 0.5rem;
            }}
            .section p {{ margin-bottom: 1rem; color: #6b7280; }}
            .hero {{ 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white; text-align: center; padding: 4rem 2rem;
                border-radius: 12px; margin-bottom: 2rem;
            }}
            .hero h1 {{ font-size: 2.5rem; margin-bottom: 1rem; }}
            .hero p {{ font-size: 1.1rem; opacity: 0.9; margin-bottom: 2rem; }}
            .btn {{
                display: inline-block; padding: 0.75rem 1.5rem; 
                background: #3b82f6; color: white; text-decoration: none;
                border-radius: 6px; transition: all 0.2s;
            }}
            .btn:hover {{ background: #2563eb; transform: translateY(-1px); }}
            .template-info {{
                background: #eff6ff; border: 1px solid #bfdbfe; padding: 1rem;
                border-radius: 8px; margin-bottom: 2rem;
            }}
            .template-info h3 {{ color: #1e40af; margin-bottom: 0.5rem; }}
            .template-info p {{ color: #1e3a8a; font-size: 0.9rem; }}
            @media (max-width: 768px) {{
                .hero {{ padding: 2rem 1rem; }}
                .hero h1 {{ font-size: 1.8rem; }}
                .content {{ padding: 0 0.5rem; }}
                .section {{ padding: 1.5rem; }}
            }}
        </style>
    </head>
    <body>
        <div class="preview-header">
            <h1>{metadata.name}</h1>
            <p>SEVDO Template Live Preview Version {metadata.version} by {metadata.author}</p>
        </div>
        
        <div class="preview-nav">
            <div class="template-info">
                <h3>Template: {template_name}</h3>
                <p>Category: {metadata.category} • {len(metadata.features or [])} features • {len(metadata.required_prefabs or [])} components</p>
            </div>
            <div>Available Pages: {page_links}</div>
        </div>
        
        <div class="content">
            {page_sections}
        </div>
        
        <script>
            document.querySelectorAll('.page-link').forEach(link => {{
                link.addEventListener('click', (e) => {{
                    e.preventDefault();
                    document.querySelectorAll('.page-link').forEach(l => l.classList.remove('active'));
                    e.target.classList.add('active');
                    console.log('Navigating to:', e.target.textContent);
                }});
            }});
            
            document.querySelector('.page-link')?.classList.add('active');
        </script>
    </body>
    </html>
    """

    return html_template


def extract_navigation(sevdo_content: str) -> list:
    """Extract navigation items from SEVDO content"""
    lines = sevdo_content.split("\n")
    for line in lines:
        if line.strip().startswith("mn("):
            nav_content = line.strip()[3:-1]
            return [item.strip() for item in nav_content.split(",")]
    return []


def parse_sevdo_content(sevdo_content: str) -> str:
    """Parse SEVDO content and convert to functional HTML sections"""
    lines = sevdo_content.split("\n")
    sections = []
    current_section = ""

    for line in lines:
        line = line.strip()
        if not line or line.startswith("mn("):
            continue

        if line.startswith("ho("):
            content = line[3:-1]
            parts = content.split(",")
            if len(parts) >= 3:
                title = parts[0].replace("h(", "").replace(")", "")
                desc = parts[1].replace("t(", "").replace(")", "")
                btn_text = parts[2].replace("b(", "").replace(")", "")

                sections.append(f"""
                <div class="hero">
                    <h1>{title}</h1>
                    <p>{desc}</p>
                    <a href="#" class="btn btn-primary" onclick="alert('This is a preview!')">{btn_text}</a>
                </div>
                """)

        elif line.startswith("h("):
            if current_section:
                current_section += "</div>"
                sections.append(current_section)
            title = line[2:-1]
            current_section = f'<div class="section"><h2>{title}</h2>'

        elif line.startswith("t("):
            text = line[2:-1]
            if current_section:
                current_section += f"<p>{text}</p>"

        elif line.startswith("cf("):
            if current_section:
                current_section += """
                <div class="contact-form">
                    <form onsubmit="alert('Form submitted in preview mode!'); return false;">
                        <div style="margin-bottom: 1rem;">
                            <label style="display: block; margin-bottom: 0.5rem;">Name</label>
                            <input type="text" name="name" required style="width: 100%; padding: 0.5rem; border: 1px solid #ccc; border-radius: 4px;">
                        </div>
                        <div style="margin-bottom: 1rem;">
                            <label style="display: block; margin-bottom: 0.5rem;">Email</label>
                            <input type="email" name="email" required style="width: 100%; padding: 0.5rem; border: 1px solid #ccc; border-radius: 4px;">
                        </div>
                        <div style="margin-bottom: 1rem;">
                            <label style="display: block; margin-bottom: 0.5rem;">Message</label>
                            <textarea name="message" required style="width: 100%; padding: 0.5rem; border: 1px solid #ccc; border-radius: 4px; height: 100px;"></textarea>
                        </div>
                        <button type="submit" class="btn btn-primary">Send Message</button>
                    </form>
                </div>
                """

    if current_section:
        current_section += "</div>"
        sections.append(current_section)

    return "\n".join(sections)


def create_template_info_page(
    template_name: str, metadata: SevdoTemplateMetadata
) -> str:
    """Create a template information page when no preview is available"""
    features_list = ""
    if metadata.features:
        features_list = "".join(
            [f"<li>{feature}</li>" for feature in metadata.features]
        )

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{metadata.name} - Template Info</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background: #f8fafc; }}
            .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
            .header {{ text-align: center; margin-bottom: 2rem; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 8px; }}
            .info-grid {{ display: grid; gap: 1rem; margin: 2rem 0; }}
            .info-item {{ background: #f8fafc; padding: 1rem; border-radius: 6px; border-left: 4px solid #3b82f6; }}
            .features {{ columns: 2; gap: 1rem; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>{metadata.name}</h1>
                <p>{metadata.description}</p>
                <p><strong>Version:</strong> {metadata.version} • <strong>Category:</strong> {metadata.category}</p>
            </div>
            
            <div class="info-grid">
                <div class="info-item">
                    <h3>Author</h3>
                    <p>{metadata.author}</p>
                </div>
                <div class="info-item">
                    <h3>Template Type</h3>
                    <p>SEVDO Frontend Template</p>
                </div>
            </div>
            
            <div class="info-item">
                <h3>Features ({len(metadata.features or [])})</h3>
                <ul class="features">{features_list}</ul>
            </div>
        </div>
    </body>
    </html>
    """


def create_error_page(template_name: str, error_message: str) -> str:
    """Create an error page for failed previews"""
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Preview Error - {template_name}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background: #fef2f2; color: #991b1b; }}
            .container {{ max-width: 600px; margin: 0 auto; text-align: center; }}
            .error-box {{ background: white; padding: 2rem; border-radius: 8px; border: 1px solid #fecaca; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="error-box">
                <h1>Preview Error</h1>
                <p>Failed to load preview for template: <strong>{template_name}</strong></p>
                <p><strong>Error:</strong> {error_message}</p>
                <p>This SEVDO template may require compilation or have missing files.</p>
            </div>
        </div>
    </body>
    </html>
    """
