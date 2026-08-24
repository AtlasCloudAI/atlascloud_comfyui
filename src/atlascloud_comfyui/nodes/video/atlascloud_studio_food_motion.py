from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle

_RATIOS = ["16:9", "9:16", "1:1", "3:4", "4:3"]
_RESOLUTIONS = ["480p", "720p", "720p-esr", "1080p-esr", "1440p-esr", "4k-esr"]


class AtlasStudioFoodMotion:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "product_image": (
                    "STRING",
                    {"default": "", "tooltip": "Food/drink product image URL (single image, <=10MB)"},
                ),
                "user_prompt": (
                    "STRING",
                    {"multiline": True, "tooltip": "Brand, flavors, textures and the tone you want"},
                ),
            },
            "optional": {
                "duration": ("INT", {"default": 10, "min": 4, "max": 15, "tooltip": "Video length in seconds (4-15)"}),
                "ratio": (_RATIOS, {"default": "16:9", "tooltip": "Aspect ratio; use 9:16 for vertical short video"}),
                "resolution": (_RESOLUTIONS, {"default": "720p", "tooltip": "Resolution; -esr tiers upscale after generation"}),
                "generate_audio": (["yes", "no"], {"default": "yes", "tooltip": "Generate ambient/food sound and light score"}),
                "count": ("INT", {"default": 1, "min": 1, "max": 2, "tooltip": "How many variants to generate"}),
                "poll_interval_sec": (
                    "FLOAT",
                    {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"},
                ),
                "timeout_sec": ("INT", {"default": 1800, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        product_image: str,
        user_prompt: str,
        duration: int = 10,
        ratio: str = "16:9",
        resolution: str = "720p",
        generate_audio: str = "yes",
        count: int = 1,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 1800,
    ) -> Tuple[str, str]:
        product_image = (product_image or "").strip()
        if not product_image:
            raise RuntimeError("product_image is required for AtlasCloud Studio Food Motion")

        user_prompt = (user_prompt or "").strip()
        if not user_prompt:
            raise RuntimeError("user_prompt is required for AtlasCloud Studio Food Motion")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "atlascloud/studio/food-motion",
            "product_image": [product_image],
            "user_prompt": user_prompt,
            "duration": int(duration),
            "ratio": ratio,
            "resolution": resolution,
            "generate_audio": generate_audio,
            "count": int(count),
        }

        prediction_id = client.generate_video(payload)
        result = client.poll_prediction(
            prediction_id,
            poll_interval_sec=float(poll_interval_sec),
            timeout_sec=float(timeout_sec),
        )

        outputs = (result.get("data") or {}).get("outputs") or []
        if not outputs:
            raise RuntimeError(f"No outputs returned for prediction {prediction_id}: {result}")

        first = outputs[0]
        if not isinstance(first, str):
            raise RuntimeError(
                f"Unexpected output type for prediction {prediction_id}: {type(first).__name__} {first!r}"
            )

        return (first, prediction_id)
