from __future__ import annotations

from pathlib import Path
from typing import Optional, Any, Dict
from pydantic import BaseModel
import requests
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse

from user_backend.app.core.logging_config import StructuredLogger
from user_backend.app.core.security import get_current_active_user
from user_backend.app.core.files import safe_write_file
from user_backend.app.models import User
from user_backend.app.settings import settings


router = APIRouter()
logger = StructuredLogger(__name__)


def _extract_text_from_gpu_response(payload: Any) -> str:
    if isinstance(payload, str):
        return payload
    if isinstance(payload, dict):
        # Primary shape
        content = payload.get("content")
        if isinstance(content, str):
            return content
        # Alternate shape { message: { content: "..." } }
        message = payload.get("message")
        if isinstance(message, dict):
            mc = message.get("content")
            if isinstance(mc, str):
                return mc
        # Nested data
        data = payload.get("data")
        if isinstance(data, dict) and isinstance(data.get("content"), str):
            return data["content"]
    if isinstance(payload, list) and payload:
        first = payload[0]
        if isinstance(first, str):
            return first
        if isinstance(first, dict):
            return _extract_text_from_gpu_response(first)
    return ""


def _call_gpu_endpoint(
    *,
    base_url: str,
    model_name: str,
    user_prompt: str,
    system_prompt: str,
    timeout: int = 90,
) -> str:
    url = base_url.rstrip("/") + "/ollama_fc"
    payload: Dict[str, Any] = {
        "model_name": model_name,
        "prompt": user_prompt,
        "system_prompt": system_prompt,
    }

    try:
        resp = requests.post(url, json=payload, timeout=timeout)
    except requests.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Failed to reach GPU server: {e}",
        )

    if not resp.ok:
        # Try to surface server error body
        text = resp.text
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"GPU server error {resp.status_code}: {text[:200]}",
        )

    try:
        data = resp.json()
    except ValueError:
        data = resp.text

    content = _extract_text_from_gpu_response(data)
    if not isinstance(content, str) or not content.strip():
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="GPU response did not contain usable 'content' text",
        )
    return content


@router.post("/edit-text-file")
async def edit_text_file_with_llm(
    *,
    file: UploadFile = File(...),
    prompt: str = Form(...),
    model_name: Optional[str] = Form(None),
    system_prompt: Optional[str] = Form(None),
    current_user: User = Depends(get_current_active_user),
):
    """Accept a text file and a prompt, call the GPU LLM, and return modified content.

    The returned JSON includes fields the frontend expects and we also write a .txt file
    with the same filename under uploads/llm_editor for auditing.
    """
    try:
        filename = file.filename or "uploaded.txt"
        # Enforce .txt output regardless of input mimetype
        base_name = Path(filename).name

        # Read original content
        raw_bytes = await file.read()
        try:
            original_text = raw_bytes.decode("utf-8")
        except UnicodeDecodeError:
            # Fallback with errors replaced to preserve most text
            original_text = raw_bytes.decode("utf-8", errors="replace")

        if not prompt or not prompt.strip():
            raise HTTPException(status_code=400, detail="Prompt is required")

        gpu_base_url = (
            settings.GPU_LLM_BASE_URL or "http://192.168.16.103:8000"
        )
        model = model_name or settings.LLM_DEFAULT_MODEL_NAME or "gpt-oss:20b"
        sys_prompt = (
            system_prompt or settings.LLM_DEFAULT_SYSTEM_PROMPT or "You are a helpful assistant."
        )

        # Compose combined user prompt
        combined_prompt = (
            "FOLLOW THESE INSTRUCTIONS EXACTLY.\n\n"
            + prompt.strip()
            + "\n\nFILE CONTENT:\n-----BEGIN FILE-----\n"
            + original_text
            + "\n-----END FILE-----\n\nRespond with ONLY the edited file content as plain text."
        )

        modified_text = _call_gpu_endpoint(
            base_url=gpu_base_url,
            model_name=model,
            user_prompt=combined_prompt,
            system_prompt=sys_prompt,
        )

        return {
            "status": "success",
            "success": True,
            "modified": True,
            "replacements": 0,
            "original_code": original_text,
            "modified_code": modified_text,
            "wrote_file": False,
            "file_path": None,
            "filename": base_name,
            "used_fallback": False,
            "message": None,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"LLM editor failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process file with LLM",
        )


@router.post("/edit-text-file/public")
async def edit_text_file_with_llm_public(
    *,
    file: UploadFile = File(...),
    prompt: str = Form(...),
    model_name: Optional[str] = Form(None),
    system_prompt: Optional[str] = Form(None),
):
    """Public variant for testing. Enabled only if settings allow it."""
    if not getattr(settings, "LLM_EDITOR_ALLOW_PUBLIC", False):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": "Public LLM editor is disabled"},
        )

    # Reuse the authenticated handler by faking a minimal current_user
    class _AnonUser:
        id = 0

    return await edit_text_file_with_llm(
        file=file,
        prompt=prompt,
        model_name=model_name,
        system_prompt=system_prompt,
        current_user=_AnonUser(),
    )


# ============ JSON-based Edit API (no file upload) ============


class EditFileJSONRequest(BaseModel):
    path: str
    prompt: str
    content: Optional[str] = None
    model_name: Optional[str] = None
    system_prompt: Optional[str] = None
    dry_run: Optional[bool] = False


class EditFileJSONResponse(BaseModel):
    path: str
    updated_content: str
    wrote_to_disk: bool


def _resolve_within_projects_root(raw_path: str) -> Path:
    root = Path(getattr(settings, "PROJECTS_ROOT", "/srv/projects")).resolve()
    p = Path(raw_path)
    if not p.is_absolute():
        p = root / p
    rp = p.resolve()
    if not str(rp).startswith(str(root)):
        raise HTTPException(
            status_code=400, detail="Path outside PROJECTS_ROOT")
    return rp


def _compose_prompt_with_content(user_prompt: str, file_text: str) -> str:
    return (
        "FOLLOW THESE INSTRUCTIONS EXACTLY.\n\n"
        + user_prompt.strip()
        + "\n\nFILE CONTENT:\n-----BEGIN FILE-----\n"
        + file_text
        + "\n-----END FILE-----\n\nRespond with ONLY the edited file content as plain text."
    )


@router.post("/edit-file", response_model=EditFileJSONResponse)
async def edit_file_json(
    req: EditFileJSONRequest,
    current_user: User = Depends(get_current_active_user),
):
    if not req.prompt or not req.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt is required")

    # Read content if not provided
    original_text: str
    if req.content is not None:
        original_text = req.content
    else:
        rp = _resolve_within_projects_root(req.path)
        if not rp.exists() or not rp.is_file():
            raise HTTPException(status_code=404, detail="File not found")
        try:
            original_text = rp.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            original_text = rp.read_text(encoding="utf-8", errors="replace")

    gpu_base_url = settings.GPU_LLM_BASE_URL or "http://192.168.16.103:8000"
    model = req.model_name or settings.LLM_DEFAULT_MODEL_NAME or "gpt-oss:20b"
    sys_prompt = req.system_prompt or settings.LLM_DEFAULT_SYSTEM_PROMPT or "You are a helpful assistant."

    combined_prompt = _compose_prompt_with_content(req.prompt, original_text)
    # Increase timeout when VPN is on/remote GPU
    updated_text = _call_gpu_endpoint(
        base_url=gpu_base_url,
        model_name=model,
        user_prompt=combined_prompt,
        system_prompt=sys_prompt,
        timeout=180,
    )

    wrote = False
    wrote = safe_write_file(req.path, updated_text)

    return EditFileJSONResponse(path=req.path, updated_content=updated_text, wrote_to_disk=wrote)


@router.post("/edit-file/public", response_model=EditFileJSONResponse)
async def edit_file_json_public(req: EditFileJSONRequest):
    if not getattr(settings, "LLM_EDITOR_ALLOW_PUBLIC", False):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": "Public LLM editor is disabled"},
        )
    # Delegate to auth variant using a dummy user

    class _AnonUser:
        id = 0

    return await edit_file_json(req, current_user=_AnonUser())
