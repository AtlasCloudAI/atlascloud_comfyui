from __future__ import annotations

import os
import time
import uuid
import urllib.request
from urllib.parse import urlencode, urlparse
from typing import Dict


def _guess_ext_from_url(url: str) -> str:
    path = urlparse(url).path or ""
    _, ext = os.path.splitext(path)
    ext = (ext or "").lower()
    if ext in (".mp4", ".webm", ".mov", ".m4v", ".gif"):
        return ext
    return ".mp4"


def _download_file(url: str, dst_path: str, timeout_sec: int = 120) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": "atlascloud-comfyui/1.0"})
    with urllib.request.urlopen(req, timeout=timeout_sec) as resp, open(dst_path, "wb") as f:
        while True:
            chunk = resp.read(1024 * 1024)  # 1MB
            if not chunk:
                break
            f.write(chunk)


class AtlasVideoPreviewer:
    """
    Input: video_url (STRING)
    Output: preview in UI + local_path (STRING)
    """

    CATEGORY = "AtlasCloud/Utils"
    FUNCTION = "run"
    OUTPUT_NODE = True

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("local_video_path",)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video_url": ("STRING", {"default": "", "tooltip": "Direct video URL (mp4/webm recommended)"}),
                "subfolder": ("STRING", {"default": "atlascloud", "tooltip": "Subfolder under ComfyUI output/"}),
            },
            "optional": {
                "filename_prefix": ("STRING", {"default": "AtlasVideo", "tooltip": "Saved filename prefix"}),
                "timeout_sec": ("INT", {"default": 120, "min": 5, "max": 3600, "tooltip": "Download timeout (seconds)"}),
                "overwrite": ("BOOLEAN", {"default": False, "tooltip": "Overwrite if the same filename exists"}),
            },
        }

    def run(
        self,
        video_url: str,
        subfolder: str,
        filename_prefix: str = "AtlasVideo",
        timeout_sec: int = 120,
        overwrite: bool = False,
    ) -> Dict:
        video_url = (video_url or "").strip()
        if not video_url.startswith("http://") and not video_url.startswith("https://"):
            raise RuntimeError("video_url must start with http:// or https://")

        # Prefer ComfyUI output directory if available
        try:
            import folder_paths  # type: ignore  # only at runtime

            output_dir = folder_paths.get_output_directory()
        except Exception:
            # Fallback for non-ComfyUI contexts (adjust if your output dir differs)
            output_dir = os.path.expanduser("~/Documents/ComfyUI/output")

        safe_sub = (subfolder or "").strip().strip("/").strip("\\")
        out_folder = os.path.join(output_dir, safe_sub) if safe_sub else output_dir
        os.makedirs(out_folder, exist_ok=True)

        ext = _guess_ext_from_url(video_url)
        stamp = time.strftime("%Y%m%d_%H%M%S")
        name = f"{filename_prefix}_{stamp}_{uuid.uuid4().hex[:8]}{ext}"
        dst_path = os.path.join(out_folder, name)

        if (not overwrite) and os.path.exists(dst_path):
            raise RuntimeError(f"File already exists: {dst_path}")

        _download_file(video_url, dst_path, timeout_sec=timeout_sec)

        # Serve the downloaded file through ComfyUI's built-in /view endpoint.
        # This avoids CORS issues that can happen when previewing remote URLs directly.
        qs = urlencode(
            {
                "filename": name,
                "subfolder": safe_sub,
                "type": "output",
            }
        )
        local_view_url = f"/view?{qs}"

        return {"ui": {"video_url": [local_view_url]}, "result": (dst_path,)}
