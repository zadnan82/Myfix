#!/usr/bin/env python3
"""
Enhanced Modular Playground Server for Frontend and Backend DSL Compiler

This is the main server file that coordinates all the modular components.
The heavy lifting is done by separate modules to keep this file clean and maintainable.
"""

import time
from pathlib import Path
from typing import List
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.websockets import WebSocket, WebSocketDisconnect

# Import our modular components
from compilation import CompilationManager
from server_management import BackendServerManager
from file_watcher import FileWatcherManager
from template_utils import (
    create_default_files,
    create_default_backend_files,
    create_default_index_template,
)

# Configuration
INPUT_DIR = Path(__file__).parent / "input_files"
OUTPUT_DIR = Path(__file__).parent / "output_files"
BACKEND_INPUT_DIR = Path(__file__).parent / "backend_input_files"
BACKEND_OUTPUT_DIR = Path(__file__).parent / "backend_output_files"
TEMPLATES_DIR = Path(__file__).parent / "templates"

# Ensure directories exist
for directory in [
    INPUT_DIR,
    OUTPUT_DIR,
    BACKEND_INPUT_DIR,
    BACKEND_OUTPUT_DIR,
    TEMPLATES_DIR,
]:
    directory.mkdir(parents=True, exist_ok=True)

# Global managers
compilation_manager = CompilationManager(
    INPUT_DIR, OUTPUT_DIR, BACKEND_INPUT_DIR, BACKEND_OUTPUT_DIR
)
server_manager = BackendServerManager(BACKEND_OUTPUT_DIR)

# WebSocket connections for real-time updates
file_change_connections: List[WebSocket] = []


async def notify_clients():
    """Notify all connected WebSocket clients of file changes."""
    message = {"type": "files_changed", "timestamp": time.time()}
    disconnected = []

    for ws in file_change_connections:
        try:
            await ws.send_json(message)
        except Exception:
            disconnected.append(ws)

    # Remove disconnected clients
    for ws in disconnected:
        if ws in file_change_connections:
            file_change_connections.remove(ws)


# Initialize file watcher
file_watcher = FileWatcherManager(
    INPUT_DIR, BACKEND_INPUT_DIR, compilation_manager, server_manager, notify_clients
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    from sevdo_frontend.frontend_compiler import load_prefabs

    load_prefabs()
    compilation_manager.compile_all_frontend_files()
    compilation_manager.compile_all_backend_files()
    file_watcher.start_watching()
    yield
    # Shutdown
    file_watcher.stop_watching()
    server_manager.cleanup()


# Create FastAPI app
app = FastAPI(lifespan=lifespan, title="SEVDO Enhanced Playground Server")

# Mount static files and setup templates
app.mount("/static", StaticFiles(directory=str(OUTPUT_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


# ===== MAIN ROUTES =====


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main playground interface."""
    frontend_files = compilation_manager.get_frontend_file_info()
    backend_files = compilation_manager.get_backend_file_info()

    return templates.TemplateResponse(
        "index2.html",
        {
            "request": request,
            "frontend_files": frontend_files,
            "backend_files": backend_files,
            "input_dir": str(INPUT_DIR),
            "output_dir": str(OUTPUT_DIR),
            "backend_input_dir": str(BACKEND_INPUT_DIR),
            "backend_output_dir": str(BACKEND_OUTPUT_DIR),
        },
    )


# ===== API ENDPOINTS =====


@app.get("/files")
async def list_files():
    """API endpoint to list all input and output files."""
    frontend_files = []
    backend_files = []
    output_files = []

    for info in compilation_manager.get_frontend_file_info():
        frontend_files.append(
            {
                "name": info["name"],
                "path": info["input_path"],
                "last_modified": info["last_modified"],
                "has_output": info["exists"],
            }
        )

    for info in compilation_manager.get_backend_file_info():
        backend_files.append(
            {
                "name": info["name"],
                "path": info["input_path"],
                "last_modified": info["last_modified"],
                "has_output": info["exists"],
            }
        )

    for f in OUTPUT_DIR.glob("*.jsx"):
        output_files.append(
            {"name": f.stem, "path": str(f), "last_modified": f.stat().st_mtime}
        )

    return {
        "frontend_files": frontend_files,
        "backend_files": backend_files,
        "output_files": output_files,
    }


@app.get("/backend/files")
async def list_backend_files():
    """API endpoint to list all backend input and output files."""
    backend_input_files = compilation_manager.get_backend_file_info()
    backend_output_files = []

    for f in BACKEND_OUTPUT_DIR.glob("*.py"):
        backend_output_files.append(
            {
                "name": f.stem,
                "path": str(f),
                "last_modified": f.stat().st_mtime,
                "size": f.stat().st_size,
            }
        )

    return {
        "backend_input_files": backend_input_files,
        "backend_output_files": backend_output_files,
    }


# ===== FRONTEND COMPILATION ENDPOINTS =====


@app.post("/compile/{filename}")
async def compile_single_file(filename: str):
    """API endpoint to manually compile a specific frontend file."""
    input_path = INPUT_DIR / f"{filename}.txt"
    if not input_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    success = compilation_manager.compile_frontend_file(input_path)
    if success:
        await notify_clients()
        return {"success": True, "message": f"Compiled {filename}"}
    else:
        raise HTTPException(status_code=500, detail="Compilation failed")


@app.post("/compile-all")
async def compile_all():
    """API endpoint to compile all frontend files."""
    count = compilation_manager.compile_all_frontend_files()
    await notify_clients()
    return {"success": True, "message": f"Compiled {count} frontend files"}


# ===== BACKEND COMPILATION ENDPOINTS =====


@app.post("/backend/compile/{filename}")
async def compile_single_backend_file(filename: str):
    """API endpoint to manually compile a specific backend file."""
    input_path = BACKEND_INPUT_DIR / f"{filename}.txt"
    if not input_path.exists():
        raise HTTPException(status_code=404, detail="Backend file not found")

    success = compilation_manager.compile_backend_file(input_path)
    if success:
        await server_manager.restart_server()
        await notify_clients()
        return {"success": True, "message": f"Compiled backend {filename}"}
    else:
        raise HTTPException(status_code=500, detail="Backend compilation failed")


@app.post("/backend/compile-all")
async def compile_all_backend():
    """API endpoint to compile all backend files."""
    count = compilation_manager.compile_all_backend_files()
    await server_manager.restart_server()
    await notify_clients()
    return {"success": True, "message": f"Compiled {count} backend files"}


# ===== BACKEND SERVER MANAGEMENT ENDPOINTS =====


@app.post("/backend/start")
async def start_backend():
    """API endpoint to start the backend server."""
    success = await server_manager.start_server()
    if success:
        return {"success": True, "message": "Backend server started on port 8004"}
    else:
        raise HTTPException(status_code=500, detail="Failed to start backend server")


@app.post("/backend/stop")
async def stop_backend():
    """API endpoint to stop the backend server."""
    success = await server_manager.stop_server()
    if success:
        return {"success": True, "message": "Backend server stopped"}
    else:
        return {"success": False, "message": "Backend server not running"}


@app.get("/backend/status")
async def backend_status():
    """API endpoint to check backend server status."""
    return server_manager.get_status()


@app.get("/backend/swagger")
async def backend_swagger():
    """Serve Swagger UI for the backend API."""
    status = server_manager.get_status()
    if not status["running"]:
        # Try to start the backend server if it's not running
        await server_manager.start_server()
        import asyncio

        await asyncio.sleep(3)  # Wait for server to start
        status = server_manager.get_status()

        if not status["running"]:
            raise HTTPException(
                status_code=503,
                detail="Backend server is not running and could not be started",
            )

    # Create HTML page with embedded Swagger UI
    swagger_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>SEVDO Backend API Documentation</title>
        <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@3.25.0/swagger-ui.css" />
        <style>
            html {{ box-sizing: border-box; overflow: -moz-scrollbars-vertical; overflow-y: scroll; }}
            *, *:before, *:after {{ box-sizing: inherit; }}
            body {{ margin:0; background: #fafafa; }}
            .swagger-ui .topbar {{ display: none; }}
            .swagger-ui .info {{ margin: 20px 0; }}
            .swagger-ui .info .title {{ color: #3b4151; }}
        </style>
    </head>
    <body>
        <div id="swagger-ui"></div>
        <script src="https://unpkg.com/swagger-ui-dist@3.25.0/swagger-ui-bundle.js"></script>
        <script>
            SwaggerUIBundle({{
                url: 'http://localhost:8004/openapi.json',
                dom_id: '#swagger-ui',
                presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIBundle.presets.standalone
                ],
                layout: "BaseLayout",
                deepLinking: true,
                showExtensions: true,
                showCommonExtensions: true,
                tryItOutEnabled: true
            }});
        </script>
    </body>
    </html>
    """

    return HTMLResponse(swagger_html)


# ===== WEBSOCKET ENDPOINT =====


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time file change notifications."""
    await websocket.accept()
    file_change_connections.append(websocket)

    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        if websocket in file_change_connections:
            file_change_connections.remove(websocket)


# ===== COMPONENT VIEWING ENDPOINTS =====


@app.get("/view/{filename}")
async def view_component(filename: str):
    """Serve a specific compiled frontend component."""
    jsx_file = OUTPUT_DIR / f"{filename}.jsx"
    if not jsx_file.exists():
        raise HTTPException(status_code=404, detail="Component not found")

    # Read the JSX content
    jsx_content = jsx_file.read_text(encoding="utf-8")

    # Create a complete HTML page to render the component
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{filename} Component</title>
        <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
        <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
        <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            body {{ font-family: system-ui, -apple-system, sans-serif; margin: 0; padding: 20px; }}
            .component-container {{ max-width: 800px; margin: 0 auto; }}
            .component-header {{ margin-bottom: 20px; padding-bottom: 10px; border-bottom: 1px solid #e2e8f0; }}
            .error {{ color: #dc2626; background: #fef2f2; padding: 10px; border-radius: 6px; margin: 10px 0; }}
        </style>
    </head>
    <body>
        <div class="component-container">
            <div class="component-header">
                <h1>{filename}</h1>
                <p>Compiled SEVDO Component</p>
            </div>
            <div id="root"></div>
        </div>

        <script type="text/babel">
            {jsx_content}

            const root = ReactDOM.createRoot(document.getElementById('root'));
            
            try {{
                // Try to render the component
                root.render(React.createElement({filename.replace("-", "")}Component));
            }} catch (error) {{
                console.error('Error rendering component:', error);
                const pre = document.createElement('pre');
                pre.className = 'error';
                pre.textContent = 'Error rendering component: ' + (error.message ? error.message : error);
                document.querySelector('.component-container').appendChild(pre);
            }}
        </script>
    </body>
    </html>
    """

    return HTMLResponse(html_content)


if __name__ == "__main__":
    # Create default example files if needed
    create_default_files(INPUT_DIR)
    create_default_backend_files(BACKEND_INPUT_DIR)
    create_default_index_template(TEMPLATES_DIR)

    # Start the server
    print("🚀 Starting Enhanced SEVDO Playground Server...")
    print(f"📂 Frontend input files: {INPUT_DIR}")
    print(f"📂 Frontend output files: {OUTPUT_DIR}")
    print(f"📂 Backend input files: {BACKEND_INPUT_DIR}")
    print(f"📂 Backend output files: {BACKEND_OUTPUT_DIR}")
    print("🌐 Open http://localhost:8003 in your browser")
    print("📚 Backend API testing available at http://localhost:8003/backend/swagger")

    uvicorn.run(
        "playground_server2:app",
        host="localhost",
        port=8003,
        reload=False,  # We handle reloading ourselves
        log_level="info",
    )
