from __future__ import annotations

from typing import Any, Dict, List, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasFlux2ProEdit:
    CATEGORY = "AtlasCloud/Image"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("image_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "prompt": ("STRING", {"multiline": True, "tooltip": "Text prompt for image editing"}),
                "images": ("STRING", {"multiline": True, "default": "", "tooltip": "1-8 image URLs/base64, one per line"}),
            },
            "optional": {
                "size": ("STRING", {"default": "1024*1024", "tooltip": "Image dimensions WIDTH*HEIGHT (256-2048)"}),
                "output_format": (["jpeg", "png"], {"default": "jpeg", "tooltip": "Output image format"}),
                "safety_tolerance": ("INT", {"default": 2, "min": 0, "max": 5, "tooltip": "0=strict, 5=least strict"}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2**31 - 1, "tooltip": "Random if -1"}),
                "enable_base64_output": ("BOOLEAN", {"default": False, "tooltip": "Return base64 instead of URL"}),
                "enable_sync_mode": ("BOOLEAN", {"default": False, "tooltip": "Wait for result inline if true"}),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"}),
                "timeout_sec": ("INT", {"default": 300, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        prompt: str,
        images: str,
        size: str = "1024*1024",
        output_format: str = "jpeg",
        safety_tolerance: int = 2,
        seed: int = -1,
        enable_base64_output: bool = False,
        enable_sync_mode: bool = False,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 300,
    ) -> Tuple[str, str]:
        client = atlas_client.client

        p = (prompt or "").strip()
        if not p:
            raise RuntimeError("prompt is required")

        image_list: List[str] = [v.strip() for v in (images or "").splitlines() if v.strip()]
        if not image_list:
            raise RuntimeError("images is required (1-8 lines)")
        if len(image_list) > 8:
            raise RuntimeError("images maxItems is 8")

        payload: Dict[str, Any] = {
            "model": "black-forest-labs/flux-2-pro/edit",
            "prompt": p,
            "images": image_list,
            "size": str(size).strip(),
            "output_format": output_format,
            "safety_tolerance": int(safety_tolerance),
            "seed": int(seed),
            "enable_base64_output": bool(enable_base64_output),
            "enable_sync_mode": bool(enable_sync_mode),
        }

        prediction_id = client.generate_image(payload)
        result = client.poll_prediction(
            prediction_id,
            poll_interval_sec=float(poll_interval_sec),
            timeout_sec=float(timeout_sec),
        )

        outputs = (result.get("data") or {}).get("outputs") or []
        if not outputs:
            raise RuntimeError(f"No outputs returned for prediction {prediction_id}: {result}")

        first = outputs[0]
        if isinstance(first, dict):
            url = first.get("url") or first.get("image") or first.get("output")
            if isinstance(url, str) and url.strip():
                return (url, prediction_id)
            raise RuntimeError(f"Unexpected output object for prediction {prediction_id}: {first}")

        if not isinstance(first, str):
            raise RuntimeError(f"Unexpected output type for prediction {prediction_id}: {type(first).__name__} {first!r}")

        return (first, prediction_id)
