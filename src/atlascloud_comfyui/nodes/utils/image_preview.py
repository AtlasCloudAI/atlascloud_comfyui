from __future__ import annotations

import base64
import io
import re
import urllib.request


def _load_image(source: str, timeout_sec: int = 60):
    # PIL Image at runtime (do NOT import PIL at module top)
    try:
        from PIL import Image
    except ModuleNotFoundError as e:
        raise RuntimeError(
            "AtlasImagePreviewURL requires Pillow. Install in ComfyUI Python env:\n"
            "  ~/Documents/ComfyUI/.venv/bin/python -m pip install pillow"
        ) from e

    s = (source or "").strip()
    if not s:
        raise RuntimeError("source is empty")

    if s.startswith("http://") or s.startswith("https://"):
        req = urllib.request.Request(s, headers={"User-Agent": "atlascloud-comfyui/1.0"}, method="GET")
        with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
            data = resp.read()
        return Image.open(io.BytesIO(data))

    # base64: supports "data:image/png;base64,...." or raw base64
    m = re.match(r"^data:image\/[a-zA-Z0-9.+-]+;base64,(.*)$", s)
    b64 = m.group(1) if m else s
    data = base64.b64decode(b64)
    return Image.open(io.BytesIO(data))


class AtlasImagePreviewURL:
    CATEGORY = "AtlasCloud/Utils"
    FUNCTION = "run"
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
            },
        }

    def run(self, source: str, timeout_sec: int = 60):
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

        pil = _load_image(source, timeout_sec=timeout_sec)
        pil = pil.convert("RGB")
        w, h = pil.size

        arr = np.array(pil).astype(np.float32) / 255.0
        image = torch.from_numpy(arr)[None, ...]  # [1,H,W,3]

        return (image, w, h)
