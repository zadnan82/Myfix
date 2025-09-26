# preview-manager/manager.py - WITH LIVE RELOAD
from pathlib import Path
import docker
import asyncio
import json
import logging
import redis
import os
from typing import Dict, Optional
from datetime import datetime
import time

logger = logging.getLogger(__name__)

# Use environment variable for projects root
PROJECTS_ROOT = Path(os.getenv("PROJECTS_ROOT", "/app/generated_websites"))


class PreviewManager:
    def __init__(self):
        try:
            self.docker_client = docker.DockerClient(
                base_url="unix:///var/run/docker.sock"
            )
            self.docker_client.ping()
            logger.info("✅ Docker client connected")
        except Exception as e:
            logger.error(f"❌ Docker connection failed: {e}")
            raise

        self.redis_client = redis.Redis.from_url(
            os.getenv("REDIS_URL", "redis://redis:6379/0")
        )
        self.base_port = int(os.getenv("PREVIEW_BASE_PORT", 3000))
        self.max_previews = int(os.getenv("MAX_CONCURRENT_PREVIEWS", 50))

    async def create_preview(self, project_id: str, project_path: str) -> dict:
        """Create preview container with LIVE RELOAD support"""
        try:
            port = self.get_available_port()
            if not port:
                raise Exception("No available ports")

            container_name = f"preview-{project_id}"

            # Resolve absolute path
            if not Path(project_path).is_absolute():
                project_path = str(PROJECTS_ROOT / project_path)

            frontend_path = Path(project_path) / "frontend"

            if not frontend_path.exists():
                raise Exception(f"Frontend directory not found: {frontend_path}")

            logger.info(f"🚀 Creating preview for {project_id}")
            logger.info(f"   📁 Frontend path: {frontend_path}")
            logger.info(f"   🔌 Port: {port}")

            # Create container with LIVE RELOAD environment
            container = self.docker_client.containers.run(
                image="node:18-alpine",
                name=container_name,
                command=[
                    "sh",
                    "-c",
                    "npm install && WATCHPACK_POLLING=true CHOKIDAR_USEPOLLING=true npm start",
                ],
                ports={"3000/tcp": port},
                volumes={
                    str(frontend_path): {
                        "bind": "/app",
                        "mode": "rw",
                    }  # READ-WRITE for live updates
                },
                environment={
                    "BROWSER": "none",
                    "CHOKIDAR_USEPOLLING": "true",  # Enable polling for file changes
                    "WATCHPACK_POLLING": "true",  # Webpack polling
                    "WDS_SOCKET_PORT": "0",
                    "FAST_REFRESH": "true",  # Enable Fast Refresh
                },
                detach=True,
                mem_limit="512m",
                cpu_period=100000,
                cpu_quota=50000,
                network="sevdo_sevdo-network",
            )

            preview_data = {
                "container_id": container.id,
                "container_name": container_name,
                "project_id": project_id,
                "port": port,
                "status": "starting",
                "created_at": datetime.now().isoformat(),
                "url": f"http://localhost:{port}",
                "project_path": project_path,
            }

            # Store in Redis
            self.redis_client.set(
                f"preview:{project_id}",
                json.dumps(preview_data),
                ex=86400,
            )

            # Wait for container to be ready
            await self.wait_for_container_ready(container, port)

            preview_data["status"] = "running"
            self.redis_client.set(f"preview:{project_id}", json.dumps(preview_data))

            logger.info(f"✅ Preview ready at http://localhost:{port}")
            return preview_data

        except Exception as e:
            logger.error(f"Failed to create preview: {e}")
            raise

    async def wait_for_container_ready(self, container, port, timeout=180):
        """Wait for React dev server with extended timeout"""
        import aiohttp

        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                container.reload()
                if container.status != "running":
                    raise Exception(f"Container stopped: {container.status}")

                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        f"http://localhost:{port}", timeout=5
                    ) as response:
                        if response.status == 200:
                            logger.info(f"✅ Preview ready on port {port}")
                            return True
            except Exception as e:
                logger.debug(
                    f"Waiting for container... ({int(time.time() - start_time)}s)"
                )
                await asyncio.sleep(5)

        raise Exception(f"Container failed to start within {timeout}s")

    def trigger_reload(self, project_id: str) -> bool:
        """Trigger reload by touching a file (React will detect change)"""
        try:
            preview_data = self.get_preview(project_id)
            if not preview_data:
                return False

            project_path = Path(preview_data["project_path"])
            trigger_file = project_path / "frontend" / ".reload_trigger"

            # Touch file to trigger reload
            trigger_file.touch()

            logger.info(f"🔄 Triggered reload for {project_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to trigger reload: {e}")
            return False

    def get_available_port(self) -> Optional[int]:
        """Find available port"""
        used_ports = self.get_used_ports()

        for port in range(self.base_port, self.base_port + self.max_previews):
            if port not in used_ports:
                return port
        return None

    def get_used_ports(self) -> set:
        """Get all currently used ports"""
        used_ports = set()

        for container in self.docker_client.containers.list():
            try:
                if "preview-" in container.name:
                    for port_mappings in container.ports.values():
                        if port_mappings:
                            for mapping in port_mappings:
                                if mapping.get("HostPort"):
                                    used_ports.add(int(mapping["HostPort"]))
            except Exception as e:
                logger.warning(f"Error checking container: {e}")

        return used_ports

    def get_preview(self, project_id: str) -> Optional[dict]:
        """Get preview info from Redis"""
        data = self.redis_client.get(f"preview:{project_id}")
        if data:
            return json.loads(data)
        return None

    def stop_preview(self, project_id: str) -> bool:
        """Stop preview container"""
        try:
            preview_data = self.get_preview(project_id)
            if not preview_data:
                return False

            container = self.docker_client.containers.get(preview_data["container_id"])
            container.stop()
            container.remove()

            self.redis_client.delete(f"preview:{project_id}")
            logger.info(f"🛑 Stopped preview for {project_id}")
            return True

        except Exception as e:
            logger.error(f"Error stopping preview: {e}")
            return False
