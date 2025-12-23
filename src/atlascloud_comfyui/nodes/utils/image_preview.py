from __future__ import annotations

import base64
import io
import os
import re
import time
import uuid
import urllib.request
from typing import Dict


def _load_image_bytes(source: str, timeout_sec: int = 60) -> bytes:
    s = (source or "").strip()
    if not s:
        raise RuntimeError("source is empty")

    if s.startswith("http://") or s.startswith("https://"):
        req = urllib.request.Request(s, headers={"User-Agent": "atlascloud-comfyui/1.0"}, method="GET")
        with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
            return resp.read()

    # base64: supports "data:image/png;base64,...." or raw base64
    m = re.match(r"^data:image\/[a-zA-Z0-9.+-]+;base64,(.*)$", s)
    b64 = m.group(1) if m else s
    return base64.b64decode(b64)


class AtlasImagePreviewURL:
    """
    Download/load image from URL or base64, save to ComfyUI output/, and preview inside the node.
    Still returns (IMAGE, width, height) so it can be connected downstream.
    """

    CATEGORY = "AtlasCloud/Utils"
    FUNCTION = "run"
    OUTPUT_NODE = True  # so UI payload is shown on this node

    RETURN_TYPES = ("IMAGE", "INT", "INT")
    RETURN_NAMES = ("image", "width", "height")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "source": ("STRING", {"default": "", "tooltip": "Image URL (http/https) or base64 (data:image/...;base64,...)"}),
            },
            "optional": {
                "timeout_sec": ("INT", {"default": 60, "min": 5, "max": 600, "tooltip": "Download timeout (seconds)"}),
                "subfolder": ("STRING", {"default": "atlascloud", "tooltip": "Subfolder under ComfyUI output/ for saved previews"}),
                "filename_prefix": ("STRING", {"default": "AtlasImage", "tooltip": "Saved filename prefix"}),
                "save_format": (["png", "jpg", "webp"], {"default": "png", "tooltip": "File format to save preview image"}),
                "quality": ("INT", {"default": 95, "min": 1, "max": 100, "tooltip": "JPG/WebP quality"}),
            },
        }

    def run(
        self,
        source: str,
        timeout_sec: int = 60,
        subfolder: str = "atlascloud",
        filename_prefix: str = "AtlasImage",
        save_format: str = "png",
        quality: int = 95,
    ) -> Dict:
        # runtime-only deps (CI/node-diff safe)
        try:
            import numpy as np
        except ModuleNotFoundError as e:
            raise RuntimeError(
                "AtlasImagePreviewURL requires numpy. Install in ComfyUI Python env:\n"
                "  ~/Documents/ComfyUI/.venv/bin/python -m pip install numpy"
            ) from e

        try:
            import torch
        except ModuleNotFoundError as e:
            raise RuntimeError(
                "AtlasImagePreviewURL requires torch (ComfyUI already includes it). "
                "If you are running outside ComfyUI, please use ComfyUI's Python env."
            ) from e

        try:
            from PIL import Image
        except ModuleNotFoundError as e:
            raise RuntimeError(
                "AtlasImagePreviewURL requires Pillow. Install in ComfyUI Python env:\n"
                "  ~/Documents/ComfyUI/.venv/bin/python -m pip install pillow"
            ) from e

        # Load bytes, decode with PIL
        img_bytes = _load_image_bytes(source, timeout_sec=timeout_sec)
        pil = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        w, h = pil.size

        # Convert to ComfyUI IMAGE tensor
        arr = np.array(pil).astype(np.float32) / 255.0
        image = torch.from_numpy(arr)[None, ...]  # [1,H,W,3]

        # Save to ComfyUI output and return UI preview payload
        # Prefer ComfyUI folder_paths if available
        try:
            import folder_paths  # type: ignore

            output_dir = folder_paths.get_output_directory()
        except Exception:
            output_dir = os.path.expanduser("~/Documents/ComfyUI/output")

        safe_sub = (subfolder or "").strip().strip("/").strip("\\")
        out_dir = os.path.join(output_dir, safe_sub) if safe_sub else output_dir
        os.makedirs(out_dir, exist_ok=True)

        stamp = time.strftime("%Y%m%d_%H%M%S")
        ext = save_format.lower()
        if ext not in ("png", "jpg", "webp"):
            ext = "png"

        filename = f"{filename_prefix}_{stamp}_{uuid.uuid4().hex[:8]}.{ext}"
        file_path = os.path.join(out_dir, filename)

        save_kwargs = {}
        if ext in ("jpg", "webp"):
            save_kwargs["quality"] = int(quality)

        pil.save(file_path, **save_kwargs)

        # This is the important part: ui.images lets ComfyUI show image previews in the node.
        # ComfyUI expects: [{"filename": "...", "subfolder": "...", "type": "output"}]
        ui_payload = {
            "images": [
                {
                    "filename": filename,
                    "subfolder": safe_sub,
                    "type": "output",
                }
            ]
        }

        return {"ui": ui_payload, "result": (image, w, h)}
