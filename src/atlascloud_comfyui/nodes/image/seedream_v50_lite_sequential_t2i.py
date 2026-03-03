from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasSeedreamV50LiteSequentialTextToImage:
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
                        "2048*2048",
                        "2304*1728",
                        "1728*2304",
                        "2848*1600",
                        "1600*2848",
                        "2496*1664",
                        "1664*2496",
                        "3136*1344",
                        "3072*3072",
                        "3456*2592",
                        "2592*3456",
                        "4096*2304",
                        "2304*4096",
                        "2496*3744",
                        "3744*2496",
                        "4704*2016",
                    ],
                    {"default": "2048*2048", "tooltip": "Output size (WIDTH*HEIGHT)"},
                ),
                "max_images": ("INT", {"default": 1, "min": 1, "max": 15, "tooltip": "Max images (1-15)"}),
                "output_format": (["jpeg", "png"], {"default": "jpeg", "tooltip": "Output format"}),
            },
            "optional": {
                "optimize_prompt_mode": (["standard", "fast"], {"default": "standard", "tooltip": "Prompt optimization mode"}),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"}),
                "timeout_sec": ("INT", {"default": 300, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        prompt: str,
        size: str,
        max_images: int,
        output_format: str,
        optimize_prompt_mode: str = "standard",
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 300,
    ) -> Tuple[str, str]:
        prompt = (prompt or "").strip()
        if not prompt:
            raise RuntimeError("prompt is required")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "bytedance/seedream-v5.0-lite/sequential",
            "prompt": prompt,
            "size": size,
            "max_images": int(max_images),
            "output_format": output_format,
            "optimize_prompt_options": {"mode": optimize_prompt_mode},
        }

        prediction_id = client.generate_image(payload)
        result = client.poll_prediction(prediction_id, poll_interval_sec=float(poll_interval_sec), timeout_sec=float(timeout_sec))

        outputs = (result.get("data") or {}).get("outputs") or []
        if not outputs:
            raise RuntimeError(f"No outputs returned for prediction {prediction_id}: {result}")

        first = outputs[0]
        if not isinstance(first, str):
            raise RuntimeError(f"Unexpected output type for prediction {prediction_id}: {type(first).__name__} {first!r}")

        return (first, prediction_id)
