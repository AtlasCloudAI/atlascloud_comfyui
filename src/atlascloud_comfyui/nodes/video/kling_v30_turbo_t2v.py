from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasKlingV30TurboTextToVideo:
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
                "duration": ([3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], {"default": 5, "tooltip": "Duration (seconds)"}),
                "aspect_ratio": (["16:9", "9:16", "1:1"], {"default": "16:9", "tooltip": "Aspect ratio"}),
                "resolution": (["720p", "1080p"], {"default": "1080p", "tooltip": "Output resolution"}),
            },
            "optional": {
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"}),
                "timeout_sec": ("INT", {"default": 900, "min": 30, "max": 7200, "tooltip": "Polling timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        prompt: str,
        duration: int,
        aspect_ratio: str,
        resolution: str = "1080p",
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        prompt = (prompt or "").strip()
        if not prompt:
            raise RuntimeError("prompt is required for Kling V3.0 Turbo Text-to-Video")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "kwaivgi/kling-v3.0-turbo/text-to-video",
            "prompt": prompt,
            "duration": int(duration),
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
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

        return (outputs[0], prediction_id)
