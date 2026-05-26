from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasNanoBananaProTextToImageUltra:
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
                "aspect_ratio": (
                    ["16:9", "9:16", "1:1", "4:3", "3:4", "2:3", "3:2", "4:5", "5:4", "21:9"],
                    {"default": "16:9", "tooltip": "Aspect ratio"},
                ),
                "resolution": (["2k", "4k"], {"default": "4k", "tooltip": "Resolution preset"}),
                "output_format": (["png", "jpeg"], {"default": "png", "tooltip": "Output format"}),
                "enable_base64_output": ("BOOLEAN", {"default": False, "tooltip": "Return base64 instead of URL if supported"}),
                "enable_sync_mode": ("BOOLEAN", {"default": False, "tooltip": "If true, server may try to return result synchronously"}),
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
        aspect_ratio: str,
        resolution: str,
        output_format: str,
        enable_base64_output: bool,
        enable_sync_mode: bool,
        negative_prompt: str = "",
        seed: int = -1,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 300,
    ) -> Tuple[str, str]:
        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "google/nano-banana-pro/text-to-image-ultra",
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "seed": seed,
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
            "output_format": output_format,
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
