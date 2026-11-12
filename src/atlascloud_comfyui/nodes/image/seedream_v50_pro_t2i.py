from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasSeedreamV50ProTextToImage:
    CATEGORY = "AtlasCloud/Image"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("image_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "prompt": ("STRING", {"multiline": True, "tooltip": "Text prompt (recommended under 600 English words)"}),
                "size": (
                    [
                        "2048*2048", "2368*1776", "1776*2368", "2816*1584", "1584*2816",
                        "2496*1664", "1664*2496", "3136*1344", "1024*1024", "1536*1536",
                        "1776*1328", "1328*1776", "2048*1152", "1152*2048",
                    ],
                    {"default": "2048*2048", "tooltip": "Output image size WIDTH*HEIGHT"},
                ),
                "output_format": (["jpeg", "png"], {"default": "jpeg", "tooltip": "Output image file format"}),
                "enable_base64_output": ("BOOLEAN", {"default": False, "tooltip": "Return base64 instead of URL if supported"}),
            },
            "optional": {
                "thinking": (["enabled", "disabled"], {"default": "enabled", "tooltip": "Prompt-optimization thinking; disable for faster generation"}),
                "prompt_optimization_mode": (["standard", "fast"], {"default": "standard", "tooltip": "fast trades some prompt-optimization quality for speed"}),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"}),
                "timeout_sec": ("INT", {"default": 300, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        prompt: str,
        size: str,
        output_format: str,
        enable_base64_output: bool,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 300,
        thinking: str = "enabled",
        prompt_optimization_mode: str = "standard",
    ) -> Tuple[str, str]:
        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "bytedance/seedream-v5.0-pro/text-to-image",
            "prompt": prompt,
            "size": size,
            "output_format": output_format,
            "enable_base64_output": bool(enable_base64_output),
            "thinking": thinking,
            "prompt_optimization_mode": prompt_optimization_mode,
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
