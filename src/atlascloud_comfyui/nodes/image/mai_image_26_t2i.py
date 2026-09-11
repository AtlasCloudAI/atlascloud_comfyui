from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasMAIImage26TextToImage:
    CATEGORY = "AtlasCloud/Image"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("image_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "prompt": ("STRING", {"multiline": True, "tooltip": "Text prompt describing the image to generate"}),
            },
            "optional": {
                "size": (
                    "STRING",
                    {
                        "default": "default",
                        "tooltip": (
                            "WIDTH*HEIGHT (each side >= 768, product <= 2,359,296), "
                            "or 'default' / 'auto' to let the model pick the aspect ratio"
                        ),
                    },
                ),
                "enable_web_search": ("BOOLEAN", {"default": False, "tooltip": "Ground generation with web search"}),
                "enable_sync_mode": ("BOOLEAN", {"default": False, "tooltip": "Try to return synchronously"}),
                "enable_base64_output": ("BOOLEAN", {"default": False, "tooltip": "Return base64 if supported"}),
                "poll_interval_sec": (
                    "FLOAT",
                    {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"},
                ),
                "timeout_sec": (
                    "INT",
                    {"default": 300, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"},
                ),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        prompt: str,
        size: str = "default",
        enable_web_search: bool = False,
        enable_sync_mode: bool = False,
        enable_base64_output: bool = False,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 300,
    ) -> Tuple[str, str]:
        prompt = (prompt or "").strip()
        if not prompt:
            raise RuntimeError("prompt is required for MAI-Image-2.6 Text-to-Image")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "microsoft/mai-image-2.6/text-to-image",
            "prompt": prompt,
            "size": str(size).strip() or "default",
            "enable_web_search": bool(enable_web_search),
            "enable_sync_mode": bool(enable_sync_mode),
            "enable_base64_output": bool(enable_base64_output),
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
