from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasFlux2FlexTextToImage:
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
                # ✅ image nodes: width/height -> size string
                "width": ("INT", {"default": 1024, "min": 256, "max": 1536, "step": 64, "tooltip": "Width"}),
                "height": ("INT", {"default": 1024, "min": 256, "max": 1536, "step": 64, "tooltip": "Height"}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2**31 - 1, "tooltip": "Random if -1"}),
                "enable_base64_output": ("BOOLEAN", {"default": False, "tooltip": "Return base64 instead of URL if supported"}),
            },
            "optional": {
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
        enable_base64_output: bool,
        negative_prompt: str = "",
        enable_sync_mode: bool = False,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 300,
    ) -> Tuple[str, str]:
        client = atlas_client.client
        size = f"{width}*{height}"

        payload: Dict[str, Any] = {
            "model": "black-forest-labs/flux-2-flex/text-to-image",
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "seed": seed,
            "size": size,
            "enable_base64_output": enable_base64_output,
            "enable_sync_mode": enable_sync_mode,
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
