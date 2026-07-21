from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle

_ASPECT_RATIOS = [
    "auto",
    "4:1",
    "3:1",
    "21:9",
    "2:1",
    "17:9",
    "16:9",
    "3:2",
    "4:3",
    "5:4",
    "1:1",
    "4:5",
    "3:4",
    "2:3",
    "9:16",
    "1:2",
    "1:3",
    "1:4",
]


class AtlasReve21Edit:
    CATEGORY = "AtlasCloud/Image"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("image_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "image": ("STRING", {"default": "", "tooltip": "Input image URL or base64 to edit"}),
                "prompt": ("STRING", {"multiline": True, "tooltip": "Instruction describing the desired edit (max 2560 chars)"}),
                "aspect_ratio": (_ASPECT_RATIOS, {"default": "auto", "tooltip": "Aspect ratio ('auto' keeps the input ratio)"}),
                "output_format": (["png", "jpeg", "webp"], {"default": "png", "tooltip": "Output format"}),
            },
            "optional": {
                "remove_background": ("BOOLEAN", {"default": False, "tooltip": "Keep only the central subject, transparent background"}),
                "enable_base64_output": ("BOOLEAN", {"default": False, "tooltip": "Return base64 instead of URL if supported"}),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"}),
                "timeout_sec": ("INT", {"default": 300, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        image: str,
        prompt: str,
        aspect_ratio: str = "auto",
        output_format: str = "png",
        remove_background: bool = False,
        enable_base64_output: bool = False,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 300,
    ) -> Tuple[str, str]:
        client = atlas_client.client

        p = (prompt or "").strip()
        if not p:
            raise RuntimeError("prompt is required")

        img = (image or "").strip()
        if not img:
            raise RuntimeError("image is required (URL or base64)")

        payload: Dict[str, Any] = {
            "model": "reve-ai/reve-2.1/edit",
            "prompt": p,
            "image": img,
            "aspect_ratio": aspect_ratio,
            "resolution": "4k",
            "remove_background": bool(remove_background),
            "output_format": output_format,
            "enable_base64_output": bool(enable_base64_output),
        }

        prediction_id = client.generate_image(payload)
        result = client.poll_prediction(
            prediction_id,
            poll_interval_sec=poll_interval_sec,
            timeout_sec=float(timeout_sec),
        )

        outputs = (result.get("data") or {}).get("outputs") or []
        if not outputs:
            raise RuntimeError(f"No outputs returned for prediction {prediction_id}: {result}")

        return (outputs[0], prediction_id)
