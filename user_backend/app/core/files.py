from pathlib import Path

def safe_write_file(path: str, content: str) -> bool:
    """
    Attempt to write content to path.
    Returns True if successful, False otherwise.
    """
    try:
        rp = Path(path)
        rp.parent.mkdir(parents=True, exist_ok=True)
        rp.write_text(content, encoding="utf-8")
        return True
    except Exception:
        return False
