from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasZImageTurboTextToImage:
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
                "width": ("INT", {"default": 1024, "min": 256, "max": 2048, "step": 64, "tooltip": "Width"}),
                "height": ("INT", {"default": 1536, "min": 256, "max": 2048, "step": 64, "tooltip": "Height"}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2**31 - 1, "tooltip": "Random if -1"}),
            },
            "optional": {
                "prompt_extend": ("BOOLEAN", {"default": False, "tooltip": "Prompt extension"}),
                "enable_base64_output": ("BOOLEAN", {"default": False, "tooltip": "Return base64 instead of URL if supported"}),
                "enable_sync_mode": ("BOOLEAN", {"default": False, "tooltip": "If true, server may try to return result synchronously"}),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"}),
                "timeout_sec": ("INT", {"default": 300, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        prompt: str,
        width: int,
        height: int,
        seed: int,
        prompt_extend: bool = False,
        enable_base64_output: bool = False,
        enable_sync_mode: bool = False,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 300,
    ) -> Tuple[str, str]:
        client = atlas_client.client

        size = f"{int(width)}*{int(height)}"

        payload: Dict[str, Any] = {
            "model": "z-image/turbo",
            "prompt": prompt,
            "prompt_extend": bool(prompt_extend),
            "seed": int(seed),
            "size": size,
            "enable_base64_output": bool(enable_base64_output),
            "enable_sync_mode": bool(enable_sync_mode),
        }

        prediction_id = client.generate_image(payload)
        result = client.poll_prediction(prediction_id, poll_interval_sec=poll_interval_sec, timeout_sec=float(timeout_sec))

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
