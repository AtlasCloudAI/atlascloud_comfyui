from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasQwenImageTextToImagePlus:
    CATEGORY = "AtlasCloud/Image"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("image_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "prompt": ("STRING", {"multiline": True, "tooltip": "Text prompt"}),
                "size": (
                    [
                        "1664*928",
                        "1472*1104",
                        "1328*1328",
                        "1104*1472",
                        "928*1664",
                    ],
                    {"default": "1664*928", "tooltip": "Size (width*height)"},
                ),
            },
            "optional": {
                "negative_prompt": ("STRING", {"multiline": True, "default": "", "tooltip": "Negative prompt"}),
                "enable_prompt_expansion": (
                    "BOOLEAN",
                    {"default": False, "tooltip": "Enable prompt optimizer"},
                ),
                "seed": (
                    "INT",
                    {"default": -1, "min": -1, "max": 2**31 - 1, "tooltip": "Random if -1"},
                ),
                "enable_base64_output": (
                    "BOOLEAN",
                    {"default": False, "tooltip": "Return base64 instead of URL if supported"},
                ),
                "enable_sync_mode": (
                    "BOOLEAN",
                    {"default": False, "tooltip": "If true, server may try to return result synchronously"},
                ),
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
        size: str,
        negative_prompt: str = "",
        enable_prompt_expansion: bool = False,
        seed: int = -1,
        enable_base64_output: bool = False,
        enable_sync_mode: bool = False,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 300,
    ) -> Tuple[str, str]:
        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "alibaba/qwen-image/text-to-image-plus",
            "prompt": prompt,
            "size": size,
            "enable_prompt_expansion": bool(enable_prompt_expansion),
            "seed": int(seed),
            "enable_base64_output": bool(enable_base64_output),
            "enable_sync_mode": bool(enable_sync_mode),
        }

        neg = (negative_prompt or "").strip()
        if neg:
            payload["negative_prompt"] = neg

        prediction_id = client.generate_image(payload)
        result = client.poll_prediction(
            prediction_id,
            poll_interval_sec=poll_interval_sec,
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
