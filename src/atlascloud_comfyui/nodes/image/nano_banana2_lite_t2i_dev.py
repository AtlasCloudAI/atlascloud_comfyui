from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasNanoBanana2LiteTextToImageDev:
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
                    ["1:1", "3:2", "2:3", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"],
                    {"default": "16:9", "tooltip": "Aspect ratio"},
                ),
                "resolution": (["1k", "2k", "4k"], {"default": "1k", "tooltip": "Resolution preset"}),
                "output_format": (["png", "jpeg"], {"default": "png", "tooltip": "Output format"}),
                "enable_base64_output": ("BOOLEAN", {"default": False, "tooltip": "Return base64 instead of URL if supported"}),
            },
            "optional": {
                "randomize_seed": ("BOOLEAN", {"default": True, "tooltip": "开启后每次生成随机结果；关闭后使用下方固定 seed"}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 4294967295, "tooltip": "固定 seed（仅在随机开关关闭时生效）"}),
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
        randomize_seed: bool = True,
        seed: int = 0,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 300,
    ) -> Tuple[str, str]:
        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "google/nano-banana-2-lite/text-to-image-developer",
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
            "output_format": output_format,
            "enable_base64_output": enable_base64_output,
        }

        if not randomize_seed:
            payload["seed"] = seed

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
