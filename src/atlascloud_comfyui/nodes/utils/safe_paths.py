"""Confine user-supplied ``subfolder`` / ``filename_prefix`` widget values.

The preview nodes join these widget values onto ComfyUI's output directory and
then create directories and write downloaded bytes there. Widget values come
from workflow JSON, which can be shared by anyone, so they must never be able
to climb out of the output root.
"""

from __future__ import annotations

import os
from typing import Tuple


def _bad_segment(seg: str) -> bool:
    if seg in (".", "..") or "\x00" in seg or ":" in seg:
        return True
    return False


def safe_filename_prefix(prefix: str, default: str = "Atlas") -> str:
    """Return *prefix* if it is a single harmless filename component."""
    value = (prefix or "").strip() or default
    if "/" in value or "\\" in value or _bad_segment(value):
        raise RuntimeError("filename_prefix must not contain path separators or '..'")
    return value


def resolve_output_subdir(output_dir: str, subfolder: str) -> Tuple[str, str]:
    """Resolve *subfolder* under *output_dir*.

    Returns ``(safe_sub, absolute_dir)`` where ``safe_sub`` is the normalised
    relative subfolder (``/``-separated, possibly empty). Raises ``RuntimeError``
    for absolute paths, ``..`` segments, or anything whose real path (symlinks
    included) falls outside *output_dir*.
    """
    raw = (subfolder or "").strip()
    if raw.startswith(("/", "\\")) or os.path.isabs(raw):
        raise RuntimeError("subfolder must be relative to the output directory")
    segments = [s for s in raw.replace("\\", "/").split("/") if s]
    if any(_bad_segment(s) for s in segments):
        raise RuntimeError("subfolder must not contain '..' or drive/NUL characters")

    root = os.path.realpath(output_dir)
    target = os.path.realpath(os.path.join(root, *segments)) if segments else root
    try:
        inside = os.path.commonpath([target, root]) == root
    except ValueError:
        inside = False
    if not inside:
        raise RuntimeError("subfolder resolves outside the output directory")
    return "/".join(segments), target
