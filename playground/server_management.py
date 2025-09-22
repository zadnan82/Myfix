"""
server_management.py - Backend server management functionality

This module handles starting, stopping, and monitoring the backend FastAPI server.
"""

import sys
import asyncio
import subprocess
from pathlib import Path
from typing import Optional


class BackendServerManager:
    """Manages the backend FastAPI server process."""

    def __init__(self, backend_output_dir: Path):
        self.backend_output_dir = backend_output_dir
        self.process: Optional[subprocess.Popen] = None
        self.port = 8004
        self.host = "localhost"

    async def start_server(self) -> bool:
        """Start the generated FastAPI backend server."""
        # Find the most recent backend output file
        backend_files = list(self.backend_output_dir.glob("*.py"))
        if not backend_files:
            print("No backend files to serve")
            return False

        # Use the most recently modified file
        latest_file = max(backend_files, key=lambda f: f.stat().st_mtime)

        try:
            # Stop existing server if running
            if self.process:
                self.process.terminate()
                self.process.wait()

            # Start new server
            cmd = [
                sys.executable,
                "-m",
                "uvicorn",
                f"{latest_file.stem}:app",
                "--host",
                self.host,
                "--port",
                str(self.port),
                "--reload",
            ]

            self.process = subprocess.Popen(
                cmd,
                cwd=str(self.backend_output_dir),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            # Wait a moment for the server to start
            await asyncio.sleep(2)

            print(f"Started backend server with {latest_file.name} on port {self.port}")
            return True

        except Exception as e:
            print(f"Error starting backend server: {e}")
            return False

    async def stop_server(self) -> bool:
        """Stop the backend server."""
        if self.process:
            self.process.terminate()
            self.process.wait()
            self.process = None
            print("Stopped backend server")
            return True
        return False

    async def restart_server(self) -> bool:
        """Restart the backend server with latest compiled code."""
        if self.process:
            return await self.start_server()
        return False

    def is_running(self) -> bool:
        """Check if the backend server is running."""
        return self.process is not None and self.process.poll() is None

    def get_status(self) -> dict:
        """Get the current status of the backend server."""
        if self.is_running():
            return {
                "running": True,
                "port": self.port,
                "url": f"http://{self.host}:{self.port}",
            }
        else:
            return {"running": False, "port": None, "url": None}

    def cleanup(self):
        """Clean up server process on shutdown."""
        if self.process:
            self.process.terminate()
            self.process.wait()
            print("Cleaned up backend server process")
