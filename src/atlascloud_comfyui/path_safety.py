from __future__ import annotations

import os
import re


def _bad_segment_error(label: str, value: str) -> RuntimeError:
    return RuntimeError(f"Invalid {label} {value!r}: must be a relative name without '..' or path escapes")


def safe_relative_dir(value: str, label: str = "subfolder") -> str:
    """Normalize a user-supplied relative sub-directory (``a`` or ``a/b``).

    Returns the cleaned relative path using ``/`` separators ("" when empty).
    Rejects absolute paths, drive letters, ``..`` segments and NUL.
    """
    raw = (value or "").strip()
    if not raw:
        return ""
    if "\x00" in raw:
        raise _bad_segment_error(label, raw)
    if raw[0] in ("/", "\\") or os.path.isabs(raw) or re.match(r"^[A-Za-z]:", raw):
        raise _bad_segment_error(label, raw)
    parts = [p for p in re.split(r"[\\/]+", raw) if p not in ("", ".")]
    if any(p == ".." for p in parts):
        raise _bad_segment_error(label, raw)
    return "/".join(parts)


def safe_filename_part(value: str, label: str = "filename_prefix") -> str:
    """Validate a single file-name component (no separators, no ``..``)."""
    raw = value or ""
    if raw in (".", "..") or any(c in raw for c in ("/", "\\", "\x00")) or re.match(r"^[A-Za-z]:", raw):
        raise _bad_segment_error(label, raw)
    return raw


def confine(path: str, base: str) -> str:
    """Return realpath(path) only if it stays inside realpath(base).

    Resolves symlinks, so a link under *base* pointing outside is rejected.
    """
    real = os.path.realpath(path)
    root = os.path.realpath(base)
    try:
        inside = os.path.commonpath([real, root]) == root
    except ValueError:  # different drives on Windows
        inside = False
    if not inside:
        raise RuntimeError(f"Path escapes the output directory: {path!r}")
    return real
