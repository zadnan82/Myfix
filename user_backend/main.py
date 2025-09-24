# user_backend/app/main.py

print("🚀 MAIN.PY LOADED - DEBUG TEST")

import asyncio
from datetime import datetime
from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import httpx
import uvicorn
import os
import logging

from user_backend.app.core.exceptions import (
    UserAlreadyExistsError,
    InvalidCredentialsError,
    ValidationError,
    DatabaseError,
)
from user_backend.app.core.security import get_current_active_user
from user_backend.app.db_setup import get_db, init_db
from user_backend.app.services import template_generator
from user_backend.app.models import Project  # ADD THIS IMPORT
from sqlalchemy.orm import Session  # ADD THIS IMPORT

# Initialize logger
try:
    from user_backend.app.core.logging_config import StructuredLogger

    logger = StructuredLogger(__name__)
except ImportError:
    import logging

    logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting SEVDO Backend")

    # Initialize database tables
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")

    yield

    # Shutdown
    logger.info("Shutting down")


# Create FastAPI application
app = FastAPI(
    title="SEVDO User Backend API",
    description="""
    ## Enhanced Backend API for SEVDO Platform
    
    A comprehensive backend service with clean, organized endpoints for all SEVDO platform features.
    """,
    version="2.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/api/v1/openapi.json",
)

# Configure CORS
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:5000",
    "https://sevdo.com",
    "https://app.sevdo.com",
    "http://80.216.194.14",
    "https://80.216.194.14",
    "http://www.sevdo.se",
    "https://www.sevdo.se",
    "https://sevdo.se",
    "http://sevdo.se",
    # Add Vercel domains (update with your actual Vercel URL)
    "https://sevdo2.vercel.app",  # Common Vercel naming
]

# Parse CORS_ORIGINS from environment variable if provided
cors_origins_env = os.getenv("CORS_ORIGINS", "")
if cors_origins_env:
    # Split by comma and add each origin
    for origin in cors_origins_env.split(","):
        origin = origin.strip()
        if origin and origin not in ALLOWED_ORIGINS:
            ALLOWED_ORIGINS.append(origin)

# In development mode, add common development origins
if os.getenv("SEVDO_ENV", "development") == "development":
    # Don't use "*" with credentials=True, add specific development origins instead
    dev_origins = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8080",
    ]
    for origin in dev_origins:
        if origin not in ALLOWED_ORIGINS:
            ALLOWED_ORIGINS.append(origin)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)

# FIXED: Register WebSocket router with better error handling
print("🔧 DEBUG: WebSocket router registration...")
try:
    from user_backend.app.api.v1.websockets import router as websocket_router

    app.include_router(websocket_router, prefix="/api/v1/ws", tags=["WebSocket"])
    print("✅ DEBUG: WebSocket router registered successfully!")
    print(f"✅ DEBUG: WebSocket routes available: {len(websocket_router.routes)}")
    for route in websocket_router.routes:
        print(
            f"   - {route.path} ({route.methods if hasattr(route, 'methods') else 'WebSocket'})"
        )
except ImportError as import_error:
    print(f"❌ DEBUG: WebSocket router import failed: {import_error}")
    print(
        "⚠️  This may be due to missing dependencies. WebSocket endpoints will not be available."
    )
except Exception as e:
    print(f"❌ DEBUG: WebSocket router registration failed: {e}")
    import traceback

    traceback.print_exc()


# Exception handlers
@app.exception_handler(UserAlreadyExistsError)
async def user_already_exists_handler(request: Request, exc: UserAlreadyExistsError):
    return JSONResponse(
        status_code=409,
        content={
            "success": False,
            "error": {
                "type": "UserAlreadyExistsError",
                "message": str(exc),
                "code": "USER_EXISTS",
            },
            "timestamp": datetime.utcnow().isoformat(),
        },
    )


@app.exception_handler(InvalidCredentialsError)
async def invalid_credentials_handler(request: Request, exc: InvalidCredentialsError):
    return JSONResponse(
        status_code=401,
        content={
            "success": False,
            "error": {
                "type": "InvalidCredentialsError",
                "message": str(exc),
                "code": "INVALID_CREDENTIALS",
            },
            "timestamp": datetime.utcnow().isoformat(),
        },
    )


@app.exception_handler(ValidationError)
async def validation_error_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": {
                "type": "ValidationError",
                "message": str(exc),
                "code": "VALIDATION_FAILED",
            },
            "timestamp": datetime.utcnow().isoformat(),
        },
    )


@app.exception_handler(DatabaseError)
async def database_error_handler(request: Request, exc: DatabaseError):
    logger.error(f"Database error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "type": "DatabaseError",
                "message": "An internal server error occurred",
                "code": "DATABASE_ERROR",
            },
            "timestamp": datetime.utcnow().isoformat(),
        },
    )


# =============================================================================
# DIRECT ROUTER IMPORTS AND REGISTRATION
# =============================================================================

# Track successful registrations
registered_routers = []
failed_routers = []

# Core routers (required)
# In your main.py, update the core_routers list:

core_routers = [
    {"name": "auth", "prefix": "/api/v1/auth", "tags": ["Authentication"]},
    {"name": "projects", "prefix": "/api/v1/projects", "tags": ["Projects"]},
    {"name": "sevdo", "prefix": "/api/v1/sevdo", "tags": ["Sevdo Builder"]},
    {"name": "tokens", "prefix": "/api/v1/tokens", "tags": ["Tokens"]},
    {"name": "templates", "prefix": "/api/v1/templates", "tags": ["Templates"]},
    {"name": "ai", "prefix": "/api/v1/ai", "tags": ["AI Integration"]},
    {"name": "llm_editor", "prefix": "/api/v1/llm-editor", "tags": ["LLM Editor"]},
    {
        "name": "ai_edit",
        "prefix": "/api/v1/ai-edit",
        "tags": ["AI Editing"],
    },  # ADD THIS LINE
]

# Enhanced routers (optional)
enhanced_routers = [
    {
        "name": "analytics",
        "prefix": "/api/v1/analytics",
        "tags": ["Analytics & Reporting"],
    },
    {"name": "system", "prefix": "/api/v1/system", "tags": ["System Monitoring"]},
    {
        "name": "user_preferences",
        "prefix": "/api/v1/preferences",
        "tags": ["User Preferences"],
    },
    {
        "name": "notifications",
        "prefix": "/api/v1/notifications",
        "tags": ["Notifications"],
    },
    {
        "name": "websockets",
        "prefix": "/api/v1/ws",
        "tags": ["WebSocket", "Real-time Updates"],
    },
]


def register_router(router_config, required=True):
    """Register a router with error handling and duplicate prevention"""
    try:
        # Check if already registered
        router_name = router_config["name"]
        if any(r["name"] == router_name for r in registered_routers):
            logger.warning(f"⚠️  Router {router_name} already registered, skipping...")
            return True

        # Import the router
        module_path = f"user_backend.app.api.v1.{router_config['name']}"
        module = __import__(module_path, fromlist=["router"])
        router = getattr(module, "router")

        # Verify it's an APIRouter instance
        from fastapi import APIRouter

        if not isinstance(router, APIRouter):
            raise ValueError(f"Expected APIRouter instance, got {type(router)}")

        # Include the router with explicit configuration
        app.include_router(
            router,
            prefix=router_config["prefix"],
            tags=router_config["tags"],
            # Add this to ensure unique registration
            include_in_schema=True,
        )

        registered_routers.append(
            {
                "name": router_config["name"],
                "prefix": router_config["prefix"],
                "tags": router_config["tags"],
                "type": "core" if required else "enhanced",
            }
        )

        logger.info(
            f"✅ Registered {router_config['name']} router at {router_config['prefix']}"
        )
        return True

    except ImportError as e:
        failed_routers.append(
            {
                "name": router_config["name"],
                "prefix": router_config["prefix"],
                "error": f"Import failed: {str(e)}",
                "required": required,
            }
        )

        if required:
            logger.error(
                f"❌ Failed to import required router {router_config['name']}: {str(e)}"
            )
        else:
            logger.info(
                f"⚠️  Optional router {router_config['name']} not available: {str(e)}"
            )
        return False

    except Exception as e:
        failed_routers.append(
            {
                "name": router_config["name"],
                "prefix": router_config["prefix"],
                "error": f"Registration failed: {str(e)}",
                "required": required,
            }
        )

        logger.error(f"❌ Failed to register router {router_config['name']}: {str(e)}")
        return False


def register_all_routers():
    """Register all routers with the FastAPI app"""
    logger.info("🚀 DEBUG: Starting router registration section...")
    logger.info(f"🔍 DEBUG: Core routers count: {len(core_routers)}")
    logger.info(f"🔍 DEBUG: Enhanced routers count: {len(enhanced_routers)}")
    logger.info(
        f"🔍 DEBUG: Enhanced routers list: {[r['name'] for r in enhanced_routers]}"
    )

    # Register core routers
    logger.info("🔧 Registering core routers...")
    for router_config in core_routers:
        register_router(router_config, required=True)

    # Register enhanced routers
    logger.info("⭐ Registering enhanced routers...")
    for router_config in enhanced_routers:
        logger.info(f"🔄 Attempting to register {router_config['name']} router...")
        result = register_router(router_config, required=False)
        logger.info(f"📊 Registration result for {router_config['name']}: {result}")

    # Log summary
    core_registered = len([r for r in registered_routers if r["type"] == "core"])
    enhanced_registered = len(
        [r for r in registered_routers if r["type"] == "enhanced"]
    )
    total_failed = len(failed_routers)

    logger.info(f"📊 Router registration summary:")
    logger.info(f"   ✅ Core routers: {core_registered}/{len(core_routers)}")
    logger.info(
        f"   ⭐ Enhanced routers: {enhanced_registered}/{len(enhanced_routers)}"
    )
    logger.info(f"   ❌ Failed: {total_failed}")

    if failed_routers:
        critical_failures = [f for f in failed_routers if f["required"]]
        if critical_failures:
            logger.error("🚨 Critical router failures:")
            for failure in critical_failures:
                logger.error(f"   - {failure['name']}: {failure['error']}")

    logger.info("✅ Router registration completed")


# =============================================================================
# ROUTER REGISTRATION - Execute immediately when module loads
# =============================================================================

print("🚀 DEBUG: Executing router registration at module level...")
try:
    register_all_routers()
    print("✅ DEBUG: Module-level router registration completed!")
except Exception as e:
    print(f"❌ DEBUG: Module-level router registration failed: {e}")

# =============================================================================
# API STATUS ENDPOINTS
# =============================================================================


# =============================================================================
# ROOT ENDPOINTS
# =============================================================================


@app.api_route("/api/blog/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_blog_api(path: str, request: Request):
    """Proxy blog API requests to generated backend"""

    # Extract generation info from referer
    referer = request.headers.get("referer", "")
    generation_id = None

    # Parse generation ID from referer URL
    if "preview-built" in referer:
        parts = referer.split("/")
        if len(parts) > 2:
            generation_id = parts[-1] or parts[-2]

    if not generation_id:
        raise HTTPException(status_code=404, detail="Blog backend not found")

    # Forward to generated backend on port 9001
    backend_url = f"http://localhost:9001/api/blog/{path}"

    # Forward query parameters
    query_params = str(request.url.query)
    if query_params:
        backend_url += f"?{query_params}"

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            if request.method == "GET":
                response = await client.get(backend_url)
            elif request.method == "POST":
                body = await request.body()
                response = await client.post(backend_url, content=body)
            # Add other methods as needed

            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers),
            )
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Blog backend unavailable: {e}")


@app.post("/api/v1/projects/{project_id}/preview")
async def create_project_preview(
    project_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),  # ADD THIS IF YOU HAVE AUTH
):
    """Create a live preview container for a project"""
    try:
        # Get project details
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        # Verify user owns the project (if using authentication)
        # if project.user_id != current_user.id:
        #     raise HTTPException(status_code=403, detail="Access denied")

        # Get the generated project path from project config
        project_path = project.config.get("output_directory")
        if not project_path:
            raise HTTPException(status_code=400, detail="Project not generated yet")

        # Check if the project directory exists
        if not os.path.exists(project_path):
            raise HTTPException(
                status_code=400, detail="Generated project files not found"
            )

        # Call preview manager to create the container
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://preview-manager:8080/previews",
                json={"project_id": str(project_id), "project_path": project_path},
                timeout=30.0,  # 30 second timeout
            )

            if response.status_code != 200:
                error_detail = f"Preview manager error: {response.text}"
                raise HTTPException(status_code=500, detail=error_detail)

            preview_data = response.json()

            # Update project with preview URL
            if "config" not in project.config:
                project.config = {}
            project.config["preview_url"] = preview_data["url"]
            project.config["preview_status"] = "running"
            db.commit()

            return {
                "success": True,
                "preview": preview_data,
                "message": "Preview container started successfully",
            }

    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Preview manager timeout")
    except httpx.ConnectError:
        raise HTTPException(status_code=503, detail="Preview manager unavailable")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create preview: {str(e)}"
        )


@app.get("/api/v1/projects/{project_id}/preview")
async def get_project_preview_status(project_id: str):
    """Get preview status for a project"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"http://preview-manager:8080/previews/{project_id}", timeout=10.0
            )

            if response.status_code == 404:
                return {
                    "is_running": False,
                    "message": "No preview running for this project",
                }

            if response.status_code != 200:
                raise HTTPException(
                    status_code=500, detail="Failed to get preview status"
                )

            status_data = response.json()
            return status_data

    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Preview manager timeout")
    except httpx.ConnectError:
        raise HTTPException(status_code=503, detail="Preview manager unavailable")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get preview status: {str(e)}"
        )


@app.delete("/api/v1/projects/{project_id}/preview")
async def stop_project_preview(
    project_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),  # ADD THIS IF YOU HAVE AUTH
):
    """Stop a project preview"""
    try:
        # Get project details
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        # Verify user owns the project (if using authentication)
        # if project.user_id != current_user.id:
        #     raise HTTPException(status_code=403, detail="Access denied")

        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"http://preview-manager:8080/previews/{project_id}", timeout=10.0
            )

            if response.status_code == 404:
                return {"message": "Preview was not running"}

            if response.status_code != 200:
                raise HTTPException(status_code=500, detail="Failed to stop preview")

            # Update project config
            if "config" in project.config:
                project.config["preview_status"] = "stopped"
                db.commit()

            return {"success": True, "message": "Preview stopped successfully"}

    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Preview manager timeout")
    except httpx.ConnectError:
        raise HTTPException(status_code=503, detail="Preview manager unavailable")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to stop preview: {str(e)}")


@app.get("/api/v1/previews")
async def list_all_previews():
    """List all active previews (admin function)"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "http://preview-manager:8080/previews", timeout=10.0
            )

            if response.status_code != 200:
                raise HTTPException(status_code=500, detail="Failed to list previews")

            return response.json()

    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Preview manager timeout")
    except httpx.ConnectError:
        raise HTTPException(status_code=503, detail="Preview manager unavailable")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to list previews: {str(e)}"
        )


@app.get("/", tags=["Root"])
async def root():
    """API information"""
    return {
        "name": "SEVDO User Backend API",
        "version": "2.0.0",
        "status": "operational",
        "registered_endpoints": len(registered_routers),
        "documentation": "/docs",
        "api_status": "/api/v1/status",
    }


@app.get("/health", tags=["Root"])
async def health_check():
    """Health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "registered_routers": len(registered_routers),
    }


if __name__ == "__main__":
    uvicorn.run(
        "user_backend.app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
        access_log=True,
    )
