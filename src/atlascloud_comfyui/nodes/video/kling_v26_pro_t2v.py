from __future__ import annotations

from typing import Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasKlingV26ProTextToVideo:
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
                "negative_prompt": ("STRING", {"multiline": True, "default": "", "tooltip": "Negative prompt"}),
                "aspect_ratio": (["16:9", "9:16", "1:1"], {"default": "16:9", "tooltip": "Aspect ratio"}),
                "duration": ([5, 10], {"default": 5, "tooltip": "Duration (seconds)"}),
                "cfg_scale": ("FLOAT", {"default": 0.50, "min": 0.00, "max": 1.00, "step": 0.01, "tooltip": "CFG scale"}),
                "sound": ("BOOLEAN", {"default": True, "tooltip": "Generate sound/audio"}),
            },
            "optional": {
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"}),
                "timeout_sec": ("INT", {"default": 900, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        prompt: str,
        negative_prompt: str,
        aspect_ratio: str,
        cfg_scale: float,
        duration: int,
        sound: bool,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        client = atlas_client.client

        payload = {
            "model": "kwaivgi/kling-v2.6-pro/text-to-video",
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "aspect_ratio": aspect_ratio,
            "cfg_scale": cfg_scale,
            "duration": duration,
            "sound": sound,
        }

        prediction_id = client.generate_video(payload)
        result = client.poll_prediction(
            prediction_id,
            poll_interval_sec=poll_interval_sec,
            timeout_sec=float(timeout_sec),
        )

        outputs = (result.get("data") or {}).get("outputs") or []
        if not outputs:
            raise RuntimeError(f"No outputs returned for prediction {prediction_id}: {result}")

        return (outputs[0], prediction_id)
