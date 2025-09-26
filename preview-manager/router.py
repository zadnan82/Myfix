from fastapi import FastAPI, APIRouter, HTTPException, status
from fastapi.responses import RedirectResponse
import logging
import os
import sys

# Add the parent directory to Python path for absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Use absolute import instead of relative import
from .manager import PreviewManager

# Create the FastAPI app instance
app = FastAPI(
    title="SEVDO Preview Manager API",
    description="API for managing preview containers",
    version="1.0.0",
)

router = APIRouter()
logger = logging.getLogger(__name__)

# Lazy initialization of preview manager
_preview_manager = None


def get_preview_manager():
    global _preview_manager
    if _preview_manager is None:
        try:
            _preview_manager = PreviewManager()
            logger.info("✅ Preview manager initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize preview manager: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Preview service unavailable - Docker not accessible",
            )
    return _preview_manager


@router.post("/previews")
async def create_preview(request: dict):
    """Create a new preview container"""
    try:
        preview_manager = get_preview_manager()

        # Validate request
        if not request.get("project_id") or not request.get("project_path"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="project_id and project_path are required",
            )

        # Check if preview already exists
        existing = preview_manager.get_preview(request.get("project_id"))
        if existing:
            return existing

        # Create new preview
        preview_data = await preview_manager.create_preview(
            request.get("project_id"), request.get("project_path")
        )

        return preview_data

    except Exception as e:
        logger.error(f"Failed to create preview: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create preview: {str(e)}",
        )


@router.delete("/previews/{project_id}")
async def stop_preview(project_id: str):
    """Stop a preview container"""
    try:
        preview_manager = get_preview_manager()
        success = preview_manager.stop_preview(project_id)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Preview for project {project_id} not found",
            )

        return {"message": f"Preview for project {project_id} stopped"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to stop preview: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to stop preview: {str(e)}",
        )


@router.get("/previews/{project_id}")
async def get_preview_status(project_id: str):
    """Get preview container status"""
    try:
        preview_manager = get_preview_manager()
        preview_data = preview_manager.get_preview(project_id)

        if preview_data:
            return {
                "is_running": True,
                "details": preview_data,
                "message": "Preview is running",
            }
        else:
            return {"is_running": False, "message": "No preview found for this project"}

    except Exception as e:
        logger.error(f"Failed to get preview status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get preview status: {str(e)}",
        )


@router.get("/previews")
async def list_previews():
    """List all active previews"""
    try:
        preview_manager = get_preview_manager()
        previews = preview_manager.list_previews()

        return {"previews": previews, "total": len(previews)}

    except Exception as e:
        logger.error(f"Failed to list previews: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list previews: {str(e)}",
        )


@router.get("/route/{project_id}")
async def route_to_preview(project_id: str):
    """Route request to the appropriate preview container (used by nginx)"""
    try:
        preview_manager = get_preview_manager()
        preview_data = preview_manager.get_preview(project_id)

        if not preview_data or preview_data.get("status") != "running":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Preview for project {project_id} not available",
            )

        # Return routing information for nginx
        return {
            "port": preview_data.get("port"),
            "container_name": preview_data.get("container_name"),
            "project_id": project_id,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to route to preview: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to route to preview: {str(e)}",
        )


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        preview_manager = get_preview_manager()
        previews = preview_manager.list_previews()

        return {
            "status": "healthy",
            "active_previews": len(previews),
            "docker_connected": True,
        }
    except Exception as e:
        return {"status": "unhealthy", "error": str(e), "docker_connected": False}


# Include the router in the app
app.include_router(router)


# Root endpoint
@app.get("/")
async def root():
    return {"name": "SEVDO Preview Manager", "version": "1.0.0", "status": "running"}


@router.post("/reload")
async def trigger_reload(request: dict):
    """Trigger reload for a project"""
    try:
        project_id = request.get("project_id")

        if not project_id:
            raise HTTPException(status_code=400, detail="project_id is required")

        preview_manager = get_preview_manager()

        # Check if preview exists
        preview_data = preview_manager.get_preview(project_id)

        if preview_data:
            # Trigger reload by touching a file
            success = preview_manager.trigger_reload(project_id)

            if success:
                return {
                    "success": True,
                    "message": f"Reload triggered for {project_id}",
                }
            else:
                return {
                    "success": False,
                    "message": f"Could not trigger reload for {project_id}",
                }
        else:
            return {
                "success": False,
                "message": f"No active preview found for {project_id}",
            }

    except Exception as e:
        logger.error(f"Reload failed: {e}")
        raise HTTPException(status_code=500, detail=f"Reload failed: {str(e)}")
