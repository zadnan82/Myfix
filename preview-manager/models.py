from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PreviewCreateRequest(BaseModel):
    project_id: str
    project_path: str


class PreviewResponse(BaseModel):
    container_id: str
    container_name: str
    project_id: str
    port: int
    status: str
    url: str
    created_at: str


class PreviewListResponse(BaseModel):
    previews: list[PreviewResponse]
    total: int


class PreviewStatusResponse(BaseModel):
    is_running: bool
    details: Optional[PreviewResponse] = None
    message: str
