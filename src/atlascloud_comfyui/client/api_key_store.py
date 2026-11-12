"""Keeps the AtlasCloud API key out of workflows.

Lookup order: the ATLASCLOUD_API_KEY environment variable, then the key saved from the
AtlasCloud Client node's "Set API key" button. That file lives in ComfyUI's
``user/__atlascloud/`` system-user directory, which ComfyUI never serves over HTTP, so it
is not part of any workflow, prompt or image metadata.
"""

from __future__ import annotations

import os
from typing import Any, Dict, Optional

ENV_VAR = "ATLASCLOUD_API_KEY"


def key_file_path() -> Optional[str]:
    try:
        import folder_paths
    except ImportError:  # running outside ComfyUI (tests, scripts)
        return None
    # Same path as folder_paths.get_system_user_directory("atlascloud"), which older ComfyUI lacks.
    return os.path.join(folder_paths.get_user_directory(), "__atlascloud", "api_key")


def load_api_key() -> str:
    key = os.getenv(ENV_VAR, "").strip()
    if key:
        return key
    path = key_file_path()
    if path and os.path.isfile(path):
        with open(path, encoding="utf-8") as f:
            return f.read().strip()
    return ""


def save_api_key(key: str) -> None:
    path = key_file_path()
    if path is None:
        raise RuntimeError("Saving the API key requires running inside ComfyUI")
    key = (key or "").strip()
    if not key:
        if os.path.exists(path):
            os.remove(path)
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(key)


def api_key_status() -> Dict[str, Any]:
    """What the UI may know about the key: never the key itself, only its last 4 characters."""
    key = load_api_key()
    if not key:
        return {"configured": False, "source": None, "hint": ""}
    source = "env" if os.getenv(ENV_VAR, "").strip() else "file"
    return {"configured": True, "source": source, "hint": key[-4:]}
