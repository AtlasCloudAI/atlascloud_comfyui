from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle

_RATIOS = ["16:9", "9:16", "1:1", "3:4", "4:3"]
_RESOLUTIONS = ["480p", "720p", "720p-esr", "1080p-esr", "1440p-esr", "4k-esr"]


class AtlasStudioTrendRemix:
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
                    {"default": "", "tooltip": "Product image URL to place into the remix (single image, <=10MB)"},
                ),
                "reference_video": (
                    "STRING",
                    {"default": "", "tooltip": "Trending reference video URL, 4-20s, <=20MB, mp4/mov"},
                ),
                "user_prompt": (
                    "STRING",
                    {"multiline": True, "tooltip": "Brand, selling points and the style/tone you want"},
                ),
            },
            "optional": {
                "model_image": (
                    "STRING",
                    {"default": "", "tooltip": "Optional model image URL; pass it only to lock the same on-camera person"},
                ),
                "duration": (
                    "INT",
                    {"default": 0, "min": 0, "max": 20, "tooltip": "Video length in seconds (4-20); 0 matches the reference video"},
                ),
                "ratio": (_RATIOS, {"default": "16:9", "tooltip": "Aspect ratio; use 9:16 for vertical short video"}),
                "resolution": (_RESOLUTIONS, {"default": "720p", "tooltip": "Resolution; -esr tiers upscale after generation"}),
                "generate_audio": (["yes", "no"], {"default": "yes", "tooltip": "Generate ambient sound and light score"}),
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
        reference_video: str,
        user_prompt: str,
        model_image: str = "",
        duration: int = 0,
        ratio: str = "16:9",
        resolution: str = "720p",
        generate_audio: str = "yes",
        count: int = 1,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 1800,
    ) -> Tuple[str, str]:
        product_image = (product_image or "").strip()
        if not product_image:
            raise RuntimeError("product_image is required for AtlasCloud Studio Trend Remix")

        reference_video = (reference_video or "").strip()
        if not reference_video:
            raise RuntimeError("reference_video is required for AtlasCloud Studio Trend Remix")

        user_prompt = (user_prompt or "").strip()
        if not user_prompt:
            raise RuntimeError("user_prompt is required for AtlasCloud Studio Trend Remix")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "atlascloud/studio/trend-remix",
            "product_image": [product_image],
            "reference_video": [reference_video],
            "user_prompt": user_prompt,
            "ratio": ratio,
            "resolution": resolution,
            "generate_audio": generate_audio,
            "count": int(count),
        }

        mi = (model_image or "").strip()
        if mi:
            payload["model_image"] = [mi]

        # duration is optional: leaving it out makes the clip match the reference video's length.
        if int(duration) > 0:
            payload["duration"] = int(duration)

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
