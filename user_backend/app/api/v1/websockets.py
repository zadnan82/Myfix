# user_backend/app/api/v1/ _websockets.py

import json
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional, Set
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session

from user_backend.app.core.security import get_current_active_user_websocket
from user_backend.app.db_setup import get_db
from user_backend.app.models import User

router = APIRouter()
logger = logging.getLogger(__name__)


class ConnectionManager:
    """connection manager for real-time preview updates"""

    def __init__(self):
        # User connections: user_id -> List[WebSocket]
        self.user_connections: Dict[int, List[WebSocket]] = {}

        # Generation-specific connections: generation_id -> List[WebSocket]
        self.generation_connections: Dict[str, List[WebSocket]] = {}

        # Connection metadata: websocket -> Dict[str, any]
        self.connection_metadata: Dict[WebSocket, Dict] = {}

        # Active edit sessions: generation_id -> Dict[str, any]
        self.active_edit_sessions: Dict[str, Dict] = {}

    async def connect_user(
        self, websocket: WebSocket, user_id: int, generation_id: Optional[str] = None
    ):
        """Connect a user with optional generation-specific subscription"""
        await websocket.accept()

        # Add to user connections
        if user_id not in self.user_connections:
            self.user_connections[user_id] = []
        self.user_connections[user_id].append(websocket)

        # Add to generation connections if specified
        if generation_id:
            if generation_id not in self.generation_connections:
                self.generation_connections[generation_id] = []
            self.generation_connections[generation_id].append(websocket)

        # Store metadata
        self.connection_metadata[websocket] = {
            "user_id": user_id,
            "generation_id": generation_id,
            "connected_at": datetime.now(),
            "last_activity": datetime.now(),
        }

        logger.info(
            f"  WebSocket connected: user={user_id}, generation={generation_id}"
        )

    def disconnect_user(self, websocket: WebSocket):
        """Disconnect user and clean up all references"""
        metadata = self.connection_metadata.get(websocket, {})
        user_id = metadata.get("user_id")
        generation_id = metadata.get("generation_id")

        # Remove from user connections
        if user_id and user_id in self.user_connections:
            if websocket in self.user_connections[user_id]:
                self.user_connections[user_id].remove(websocket)
            if not self.user_connections[user_id]:
                del self.user_connections[user_id]

        # Remove from generation connections
        if generation_id and generation_id in self.generation_connections:
            if websocket in self.generation_connections[generation_id]:
                self.generation_connections[generation_id].remove(websocket)
            if not self.generation_connections[generation_id]:
                del self.generation_connections[generation_id]

        # Remove metadata
        if websocket in self.connection_metadata:
            del self.connection_metadata[websocket]

        logger.info(
            f"  WebSocket disconnected: user={user_id}, generation={generation_id}"
        )

    async def send_to_user(self, user_id: int, message: Dict):
        """Send message to all connections for a specific user"""
        if user_id not in self.user_connections:
            return False

        disconnected = []
        success_count = 0

        for websocket in self.user_connections[user_id]:
            try:
                await websocket.send_text(json.dumps(message))
                success_count += 1

                # Update last activity
                if websocket in self.connection_metadata:
                    self.connection_metadata[websocket]["last_activity"] = (
                        datetime.now()
                    )

            except Exception as e:
                logger.warning(f"Failed to send to user {user_id}: {e}")
                disconnected.append(websocket)

        # Clean up failed connections
        for websocket in disconnected:
            self.disconnect_user(websocket)

        return success_count > 0

    async def send_to_generation(self, generation_id: str, message: Dict):
        """Send message to all connections watching a specific generation"""
        if generation_id not in self.generation_connections:
            return False

        disconnected = []
        success_count = 0

        for websocket in self.generation_connections[generation_id]:
            try:
                await websocket.send_text(json.dumps(message))
                success_count += 1

                # Update last activity
                if websocket in self.connection_metadata:
                    self.connection_metadata[websocket]["last_activity"] = (
                        datetime.now()
                    )

            except Exception as e:
                logger.warning(f"Failed to send to generation {generation_id}: {e}")
                disconnected.append(websocket)

        # Clean up failed connections
        for websocket in disconnected:
            self.disconnect_user(websocket)

        return success_count > 0

    async def broadcast_preview_update(self, generation_id: str, update_data: Dict):
        """Broadcast preview update to all watchers of a generation"""
        message = {
            "type": "preview_update",
            "generation_id": generation_id,
            "data": update_data,
            "timestamp": datetime.now().isoformat(),
        }

        success = await self.send_to_generation(generation_id, message)
        logger.info(f"Broadcast preview update for {generation_id}: success={success}")
        return success

    async def start_edit_session(
        self, generation_id: str, user_id: int, instruction: str
    ):
        """Start an edit session and notify all watchers"""
        session_data = {
            "user_id": user_id,
            "instruction": instruction,
            "started_at": datetime.now().isoformat(),
            "status": "started",
        }

        self.active_edit_sessions[generation_id] = session_data

        # Notify all watchers that an edit has started
        await self.send_to_generation(
            generation_id,
            {
                "type": "edit_session_started",
                "generation_id": generation_id,
                "data": session_data,
            },
        )

    async def complete_edit_session(
        self,
        generation_id: str,
        success: bool,
        changes: List[str],
        modified_files: List[str],
    ):
        """Complete an edit session and trigger preview updates"""
        if generation_id in self.active_edit_sessions:
            session_data = self.active_edit_sessions[generation_id]
            session_data.update(
                {
                    "status": "completed",
                    "success": success,
                    "changes": changes,
                    "modified_files": modified_files,
                    "completed_at": datetime.now().isoformat(),
                }
            )

            # Notify all watchers
            await self.send_to_generation(
                generation_id,
                {
                    "type": "edit_session_completed",
                    "generation_id": generation_id,
                    "data": session_data,
                },
            )

            # If successful, trigger preview update
            if success:
                await self.broadcast_preview_update(
                    generation_id,
                    {
                        "action": "reload_preview",
                        "reason": "ai_edit_applied",
                        "changes": changes,
                        "modified_files": modified_files,
                        "instruction": session_data.get("instruction", ""),
                    },
                )

            # Clean up session
            del self.active_edit_sessions[generation_id]

    def get_connection_stats(self) -> Dict:
        """Get connection statistics"""
        return {
            "total_users_connected": len(self.user_connections),
            "total_connections": sum(
                len(connections) for connections in self.user_connections.values()
            ),
            "generations_being_watched": len(self.generation_connections),
            "active_edit_sessions": len(self.active_edit_sessions),
            "connection_details": {
                gen_id: len(connections)
                for gen_id, connections in self.generation_connections.items()
            },
        }


# Global   connection manager
manager = ConnectionManager()


@router.websocket("/preview-updates/{generation_id}")
async def websocket_preview_updates(
    websocket: WebSocket, generation_id: str, token: str, db: Session = Depends(get_db)
):
    """WebSocket endpoint for real-time preview updates"""
    user = None

    try:
        # Authenticate user
        user = await get_current_active_user_websocket(token, db)

        # Connect to   manager
        await manager.connect_user(websocket, user.id, generation_id)

        # Send initial status
        await websocket.send_text(
            json.dumps(
                {
                    "type": "connection_established",
                    "data": {
                        "generation_id": generation_id,
                        "user_id": user.id,
                        "timestamp": datetime.now().isoformat(),
                        "features": [
                            "preview_updates",
                            "edit_notifications",
                            "real_time_sync",
                        ],
                    },
                }
            )
        )

        # Listen for client messages
        while True:
            try:
                data = await websocket.receive_text()
                message = json.loads(data)

                await handle_client_message(websocket, message, user.id, generation_id)

            except json.JSONDecodeError:
                await websocket.send_text(
                    json.dumps(
                        {"type": "error", "data": {"message": "Invalid JSON message"}}
                    )
                )
            except Exception as e:
                logger.error(f"Error processing client message: {e}")
                break

    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected normally for generation {generation_id}")
    except Exception as e:
        logger.error(f"WebSocket connection error: {e}")
    finally:
        if user:
            manager.disconnect_user(websocket)


async def handle_client_message(
    websocket: WebSocket, message: Dict, user_id: int, generation_id: str
):
    """Handle messages from client"""

    message_type = message.get("type", "")

    if message_type == "ping":
        # Respond to ping with pong
        await websocket.send_text(
            json.dumps({"type": "pong", "timestamp": datetime.now().isoformat()})
        )

    elif message_type == "request_preview_refresh":
        # Trigger preview refresh for all watchers
        await manager.broadcast_preview_update(
            generation_id,
            {
                "action": "reload_preview",
                "reason": "user_requested",
                "requested_by": user_id,
            },
        )

    elif message_type == "subscribe_to_edits":
        # Client wants to receive edit notifications
        await websocket.send_text(
            json.dumps(
                {
                    "type": "subscription_confirmed",
                    "data": {
                        "subscription": "edit_notifications",
                        "generation_id": generation_id,
                    },
                }
            )
        )

    elif message_type == "get_connection_stats":
        # Send connection statistics
        stats = manager.get_connection_stats()
        await websocket.send_text(
            json.dumps({"type": "connection_stats", "data": stats})
        )

    else:
        logger.warning(f"Unknown message type: {message_type}")


# Helper functions for integration with existing systems


async def notify_preview_update(
    generation_id: str,
    changes: List[str],
    modified_files: List[str],
    instruction: str = "",
    user_id: Optional[int] = None,
):
    """preview update notification"""

    update_data = {
        "changes": changes,
        "modified_files": modified_files,
        "instruction": instruction,
        "updated_by": user_id,
        "message": f"Applied changes: {', '.join(changes)}"
        if changes
        else "Website updated",
    }

    return await manager.broadcast_preview_update(generation_id, update_data)


async def notify_edit_session_start(generation_id: str, user_id: int, instruction: str):
    """Notify that an edit session has started"""
    return await manager.start_edit_session(generation_id, user_id, instruction)


async def notify_edit_session_complete(
    generation_id: str, success: bool, changes: List[str], modified_files: List[str]
):
    """Notify that an edit session has completed"""
    return await manager.complete_edit_session(
        generation_id, success, changes, modified_files
    )


@router.get("/connection-stats")
async def get_connection_stats():
    """Get real-time connection statistics"""
    return manager.get_connection_stats()


@router.post("/trigger-preview-refresh/{generation_id}")
async def trigger_preview_refresh(generation_id: str):
    """Manually trigger preview refresh for testing"""
    success = await manager.broadcast_preview_update(
        generation_id,
        {
            "action": "reload_preview",
            "reason": "manual_trigger",
            "timestamp": datetime.now().isoformat(),
        },
    )

    return {
        "success": success,
        "generation_id": generation_id,
        "message": "Preview refresh triggered" if success else "No active connections",
    }
