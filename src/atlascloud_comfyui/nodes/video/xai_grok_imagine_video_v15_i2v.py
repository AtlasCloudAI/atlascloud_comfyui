from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasGrokImagineVideoV15ImageToVideo:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "prompt": ("STRING", {"multiline": True, "tooltip": "Motion prompt; first frame comes from image_url"}),
                "image_url": ("STRING", {"default": "", "tooltip": "Starting-frame image (HTTPS URL or base64 data URI)"}),
            },
            "optional": {
                "duration": ("INT", {"default": 8, "min": 1, "max": 15, "tooltip": "Duration (seconds, 1-15)"}),
                "resolution": (["480p", "720p"], {"default": "720p", "tooltip": "Output resolution"}),
                "aspect_ratio": (
                    ["1:1", "16:9", "9:16", "4:3", "3:4", "3:2", "2:3"],
                    {"default": "16:9", "tooltip": "Output aspect ratio"},
                ),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"}),
                "timeout_sec": ("INT", {"default": 900, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        prompt: str,
        image_url: str,
        duration: int = 8,
        resolution: str = "720p",
        aspect_ratio: str = "16:9",
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        prompt = (prompt or "").strip()
        if not prompt:
            raise RuntimeError("prompt is required")

        image_url = (image_url or "").strip()
        if not image_url:
            raise RuntimeError("image_url is required (URL or base64 data URI)")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "xai/grok-imagine-video-v1.5/image-to-video",
            "prompt": prompt,
            "image_url": image_url,
            "duration": int(duration),
            "resolution": resolution,
            "aspect_ratio": aspect_ratio,
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
