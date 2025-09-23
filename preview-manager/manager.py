from pathlib import Path
import docker
import asyncio
import json
import logging
import redis
import os
from typing import Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class PreviewManager:
    def __init__(self):
        # FIX: Use the correct Docker socket path
        try:
            self.docker_client = docker.DockerClient(
                base_url="unix:///var/run/docker.sock"
            )
            # Test the connection
            self.docker_client.ping()
            logger.info("✅ Docker client connected successfully")
        except Exception as e:
            logger.error(f"❌ Failed to connect to Docker: {e}")
            # Fallback to environment-based client
            try:
                self.docker_client = docker.from_env()
                self.docker_client.ping()
                logger.info("✅ Docker client connected via from_env()")
            except Exception as e2:
                logger.error(f"❌ Docker connection completely failed: {e2}")
                raise

        self.redis_client = redis.Redis.from_url(
            os.getenv("REDIS_URL", "redis://redis:6379/0")
        )
        self.base_port = int(os.getenv("PREVIEW_BASE_PORT", 3000))
        self.max_previews = int(os.getenv("MAX_CONCURRENT_PREVIEWS", 50))

    def get_available_port(self) -> Optional[int]:
        """Find an available port for new preview"""
        used_ports = self.get_used_ports()

        for port in range(self.base_port, self.base_port + self.max_previews):
            if port not in used_ports:
                return port
        return None

    def get_used_ports(self) -> set:
        """Get all currently used preview ports"""
        used_ports = set()

        # Check running containers
        for container in self.docker_client.containers.list():
            try:
                if "preview-" in container.name:
                    for port in container.ports.values():
                        if port and port[0]["HostPort"]:
                            used_ports.add(int(port[0]["HostPort"]))
            except Exception as e:
                logger.warning(f"Error checking container {container.name}: {e}")

        return used_ports

    async def create_preview(self, project_id: str, project_path: str) -> dict:
        """Create a new preview container for a project"""
        try:
            port = self.get_available_port()
            if not port:
                raise Exception("No available ports for preview")

            container_name = f"preview-{project_id}"

            # Start the preview container
            container = self.docker_client.containers.run(
                image="node:18-alpine",
                name=container_name,
                command=["sh", "-c", "cd /app && npm install && npm start"],
                ports={"3000/tcp": port},
                volumes={project_path: {"bind": "/app", "mode": "rw"}},
                environment={
                    "BROWSER": "none",
                    "CHOKIDAR_USEPOLLING": "true",
                    "WDS_SOCKET_PORT": "0",
                },
                detach=True,
                mem_limit="512m",
                mem_reservation="128m",
                cpu_period=100000,
                cpu_quota=50000,  # 0.5 CPU
                network="sevdo2_sevdo-network",
            )

            preview_data = {
                "container_id": container.id,
                "container_name": container_name,
                "project_id": project_id,
                "port": port,
                "status": "starting",
                "created_at": datetime.now().isoformat(),
                "url": f"/preview/{project_id}/",
            }

            # Store in Redis
            self.redis_client.set(
                f"preview:{project_id}",
                json.dumps(preview_data),
                ex=86400,  # 24 hours TTL
            )

            # Store port mapping
            self.redis_client.set(f"preview_port:{port}", project_id)

            logger.info(
                f"Created preview container for project {project_id} on port {port}"
            )

            # Wait for container to be ready
            await self.wait_for_container_ready(container, port)

            preview_data["status"] = "running"
            self.redis_client.set(f"preview:{project_id}", json.dumps(preview_data))

            return preview_data

        except Exception as e:
            logger.error(f"Failed to create preview for {project_id}: {e}")
            raise

    async def wait_for_container_ready(self, container, port, timeout=120):
        """Wait for the React dev server to be ready"""
        import aiohttp
        import async_timeout

        start_time = asyncio.get_event_loop().time()

        while asyncio.get_event_loop().time() - start_time < timeout:
            try:
                # Check if container is still running
                container.reload()
                if container.status != "running":
                    raise Exception(
                        f"Container stopped with status: {container.status}"
                    )

                async with async_timeout.timeout(5):
                    async with aiohttp.ClientSession() as session:
                        async with session.get(f"http://localhost:{port}") as response:
                            if response.status == 200:
                                logger.info(
                                    f"Preview container on port {port} is ready"
                                )
                                return True
            except Exception as e:
                logger.debug(f"Container not ready yet: {e}")
                await asyncio.sleep(5)

        raise Exception(f"Preview container failed to start within {timeout} seconds")

    def stop_preview(self, project_id: str) -> bool:
        """Stop a preview container"""
        try:
            preview_data = self.get_preview(project_id)
            if not preview_data:
                return False

            container = self.docker_client.containers.get(preview_data["container_id"])
            container.stop()
            container.remove()

            # Clean up Redis
            self.redis_client.delete(f"preview:{project_id}")
            self.redis_client.delete(f"preview_port:{preview_data['port']}")

            logger.info(f"Stopped preview container for project {project_id}")
            return True

        except Exception as e:
            logger.error(f"Error stopping preview {project_id}: {e}")
            return False

    def get_preview(self, project_id: str) -> Optional[dict]:
        """Get preview container info"""
        data = self.redis_client.get(f"preview:{project_id}")
        if data:
            return json.loads(data)
        return None

    def list_previews(self) -> list:
        """List all active previews"""
        previews = []
        for key in self.redis_client.scan_iter("preview:*"):
            data = self.redis_client.get(key)
            if data:
                previews.append(json.loads(data))
        return previews

    def create_preview_container(self, project_path: str, generation_id: str):
        """Create optimized container for React app"""

        dockerfile_content = f"""
FROM node:18-alpine

WORKDIR /app

# Copy package.json first for better caching
COPY frontend/package.json ./
RUN npm install

# Copy frontend source
COPY frontend/ ./

# Set environment for React dev server
ENV CHOKIDAR_USEPOLLING=true
ENV WDS_SOCKET_PORT=0
ENV BROWSER=none
ENV PORT=3000

EXPOSE 3000

CMD ["npm", "start"]
"""
        dockerfile_path = Path(project_path) / "Dockerfile"
        dockerfile_path.write_text(dockerfile_content)

        # Build custom image
        image_name = f"sevdo-preview-{generation_id}"
        self.docker_client.images.build(
            path=str(project_path), dockerfile="Dockerfile", tag=image_name, rm=True
        )

        container = self.docker_client.containers.run(
            image=image_name,
            name=f"preview-{generation_id}",
            ports={"3000/tcp": self.get_available_port()},
            detach=True,
            remove=True,  # Auto-cleanup when stopped
            mem_limit="512m",
            network="sevdo2_sevdo-network",
        )

        return container


# REMOVE the problematic initialization at the bottom
