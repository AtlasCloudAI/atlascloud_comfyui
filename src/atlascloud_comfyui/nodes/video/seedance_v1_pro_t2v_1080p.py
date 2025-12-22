from __future__ import annotations

from typing import Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasSeedanceV1ProT2V1080p:
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
                "duration": ([5, 10], {"default": 5, "tooltip": "Duration (seconds)"}),
                "aspect_ratio": (["16:9", "9:16", "1:1", "21:9", "1:1", "4:3", "3:4"], {"default": "16:9", "tooltip": "Aspect ratio"}),
                "camera_fixed": ("BOOLEAN", {"default": False, "tooltip": "Fix camera (no camera motion)"}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2**31 - 1, "tooltip": "Random if -1"}),
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
        duration: int,
        aspect_ratio: str,
        camera_fixed: bool,
        seed: int,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        client = atlas_client.client

        payload = {
            "model": "bytedance/seedance-v1-pro-t2v-1080p",
            "prompt": prompt,
            "duration": duration,
            "aspect_ratio": aspect_ratio,
            "camera_fixed": camera_fixed,
            "seed": seed,
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
