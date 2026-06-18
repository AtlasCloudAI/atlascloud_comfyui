from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasKlingV30TurboImageToVideo:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                # Kling I2V: base image is required
                "image": ("STRING", {"default": "", "tooltip": "First frame image URL or base64"}),
                "duration": ([3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], {"default": 5, "tooltip": "Duration (seconds)"}),
                "resolution": (["720p", "1080p"], {"default": "1080p", "tooltip": "Output resolution"}),
            },
            "optional": {
                "prompt": ("STRING", {"default": "", "multiline": True, "tooltip": "Text prompt (optional)"}),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"}),
                "timeout_sec": ("INT", {"default": 900, "min": 30, "max": 7200, "tooltip": "Polling timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        image: str,
        duration: int,
        resolution: str = "1080p",
        prompt: str = "",
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        image = (image or "").strip()
        if not image:
            raise RuntimeError("image is required for Kling V3.0 Turbo Image-to-Video")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "kwaivgi/kling-v3.0-turbo/image-to-video",
            "image": image,
            "duration": int(duration),
            "resolution": resolution,
        }

        prompt = (prompt or "").strip()
        if prompt:
            payload["prompt"] = prompt

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
