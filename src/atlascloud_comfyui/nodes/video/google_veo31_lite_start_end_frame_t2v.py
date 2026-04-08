from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasVeo31LiteStartEndFrameToVideo:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "prompt": ("STRING", {"multiline": True, "tooltip": "Text prompt"}),
                "image": ("STRING", {"default": "", "tooltip": "Start frame image (URL/base64)"}),
                "last_image": ("STRING", {"default": "", "tooltip": "End frame image (URL/base64)"}),
            },
            "optional": {
                "duration": ([4, 6, 8], {"default": 8, "tooltip": "Duration (seconds)"}),
                "aspect_ratio": (["16:9", "9:16"], {"default": "16:9", "tooltip": "Aspect ratio"}),
                "resolution": (["720p", "1080p"], {"default": "720p", "tooltip": "Resolution"}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2**31 - 1, "tooltip": "Random if -1"}),
                "poll_interval_sec": (
                    "FLOAT",
                    {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"},
                ),
                "timeout_sec": ("INT", {"default": 900, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        prompt: str,
        image: str,
        last_image: str,
        duration: int = 8,
        aspect_ratio: str = "16:9",
        resolution: str = "720p",
        seed: int = -1,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        prompt = (prompt or "").strip()
        if not prompt:
            raise RuntimeError("prompt is required for AtlasCloud VEO3.1 Lite Start-End Frame-to-Video")

        image = (image or "").strip()
        if not image:
            raise RuntimeError("image is required for AtlasCloud VEO3.1 Lite Start-End Frame-to-Video")

        last_image = (last_image or "").strip()
        if not last_image:
            raise RuntimeError("last_image is required for AtlasCloud VEO3.1 Lite Start-End Frame-to-Video")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "google/veo3.1-lite/start-end-frame-to-video",
            "prompt": prompt,
            "image": image,
            "last_image": last_image,
            "duration": int(duration),
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
        }

        if int(seed) >= 0:
            payload["seed"] = int(seed)

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
