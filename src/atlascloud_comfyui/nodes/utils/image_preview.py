from __future__ import annotations

import base64
import io
import re
import urllib.request
from typing import Tuple

import numpy as np
import torch
from PIL import Image


def _pil_to_comfy_image(pil: Image.Image) -> torch.Tensor:
    arr = np.array(pil.convert("RGB")).astype(np.float32) / 255.0
    return torch.from_numpy(arr)[None, ...]  # [1,H,W,3]


def _load_image(source: str, timeout_sec: int = 60) -> Image.Image:
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

    def run(self, source: str, timeout_sec: int = 60) -> Tuple[torch.Tensor, int, int]:
        pil = _load_image(source, timeout_sec=timeout_sec)
        w, h = pil.size
        image = _pil_to_comfy_image(pil)
        return (image, w, h)
