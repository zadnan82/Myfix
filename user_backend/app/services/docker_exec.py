import subprocess
import shlex
import base64
import re
from typing import Literal, Dict

_CONTAINER_NAME_RE = re.compile(r"^[a-zA-Z0-9_.-]+$")


def _validate_container_name(container_name: str) -> bool:
    """Basic validation to avoid shell injection via container name."""
    return bool(_CONTAINER_NAME_RE.fullmatch(container_name))


def read_file_from_container(
    container_name: str,
    file_path: str,
    *,
    return_mode: Literal["text", "base64"] = "text",
    max_bytes: int = 1_048_576,
    timeout_seconds: int = 15,
) -> Dict:
    """
    Read a file from a running Docker container using `docker exec`.

    Returns a dict with metadata and content (as text or base64).

    Raises RuntimeError with descriptive messages on failure.
    """
    if not _validate_container_name(container_name):
        raise RuntimeError("Invalid container name")
    if not file_path or file_path.strip() == "":
        raise RuntimeError("file_path is required")
    if max_bytes <= 0:
        raise RuntimeError("max_bytes must be positive")

    safe_path = shlex.quote(file_path)
    shell_cmd = f"cat {safe_path} || exit 66"

    cmd = [
        "docker",
        "exec",
        "-i",
        container_name,
        shell_cmd,
    ]

    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired as e:
        raise RuntimeError("docker exec timed out") from e
    except FileNotFoundError as e:
        raise RuntimeError("docker CLI not found in PATH") from e

    if proc.returncode == 66:
        raise RuntimeError("File not found in container")
    if proc.returncode != 0:
        stderr_msg = (
            proc.stderr.decode(errors="replace") if proc.stderr else ""
        )
        raise RuntimeError(
            f"docker exec failed (code {proc.returncode}): {stderr_msg}"
        )

    data_bytes = proc.stdout or b""

    if return_mode == "base64":
        content_b64 = base64.b64encode(data_bytes).decode("ascii")
        return {
            "container": container_name,
            "file_path": file_path,
            "byte_length": len(data_bytes),
            "content_base64": content_b64,
            "truncated": len(data_bytes) >= max_bytes,
        }
    else:
        content_text = data_bytes.decode("utf-8", errors="replace")
        return {
            "container": container_name,
            "file_path": file_path,
            "byte_length": len(data_bytes),
            "content": content_text,
            "truncated": len(data_bytes) >= max_bytes,
        }


def write_file_to_container(
    container_name: str,
    file_path: str,
    *,
    content: str,
    input_mode: Literal["text", "base64"] = "text",
    encoding: str = "utf-8",
    mode: Literal["overwrite", "append"] = "overwrite",
    create_dirs: bool = True,
    max_bytes: int = 10_485_760,
    timeout_seconds: int = 15,
) -> Dict:
    """
    Write content to a file inside a running Docker container using `docker exec`.

    - input_mode: "text" expects plain text; "base64" expects base64-encoded data
    - mode: "overwrite" (>) or "append" (>>)
    - create_dirs: when True, attempts to mkdir -p the parent directory first
    - max_bytes: guards against excessively large writes
    """
    if not _validate_container_name(container_name):
        raise RuntimeError("Invalid container name")
    if not file_path or file_path.strip() == "":
        raise RuntimeError("file_path is required")
    if input_mode not in ("text", "base64"):
        raise RuntimeError("input_mode must be 'text' or 'base64'")
    if mode not in ("overwrite", "append"):
        raise RuntimeError("mode must be 'overwrite' or 'append'")

    # Prepare bytes to write
    if input_mode == "base64":
        try:
            data_bytes = base64.b64decode(content)
        except Exception as e:
            raise RuntimeError("Invalid base64 content") from e
    else:
        data_bytes = content.encode(encoding)

    if len(data_bytes) > max_bytes:
        raise RuntimeError("content exceeds max_bytes limit")

    safe_path = shlex.quote(file_path)
    redir = ">>" if mode == "append" else ">"
    mkdir_prefix = (
        f"mkdir -p $(dirname {safe_path}) && " if create_dirs else ""
    )
    shell_cmd = f"{mkdir_prefix}cat {redir} {safe_path}"

    cmd = [
        "docker",
        "exec",
        "-i",
        container_name,
        shell_cmd,
    ]

    try:
        proc = subprocess.run(
            cmd,
            input=data_bytes,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired as e:
        raise RuntimeError("docker exec timed out") from e
    except FileNotFoundError as e:
        raise RuntimeError("docker CLI not found in PATH") from e

    if proc.returncode != 0:
        stderr_msg = (
            proc.stderr.decode(errors="replace") if proc.stderr else ""
        )
        raise RuntimeError(
            f"docker exec failed (code {proc.returncode}): {stderr_msg}"
        )

    return {
        "container": container_name,
        "file_path": file_path,
        "written_bytes": len(data_bytes),
        "mode": mode,
        "created_parent_dirs": bool(create_dirs),
    }
