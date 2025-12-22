from __future__ import annotations
from typing import Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasWAN26TextToVideo:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),  # <--- connect from AtlasClientNode
                "prompt": ("STRING", {"multiline": True}),
                "negative_prompt": ("STRING", {"multiline": True, "default": ""}),
                "duration": ([5, 10, 15], {"default": 15}),
                "size": (
                    [
                        "1280*720",
                        "1920*1080",
                        "720*1280",
                        "1080*1920",
                        "960*960",
                        "1088*832",
                        "832*1088",
                        "1440*1440",
                        "1632*1248",
                        "1248*1632",
                    ],
                    {"default": "1920*1080", "tooltip": "Resulution"},
                ),
                "shot_type": (["single", "multi"], {"default": "multi", "tooltip": "Shot Type"}),
                "enable_prompt_expansion": ("BOOLEAN", {"default": True}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2**31 - 1}),
            },
            "optional": {
                "audio": ("STRING", {"default": ""}),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0}),
                "timeout_sec": ("INT", {"default": 900, "min": 30, "max": 7200}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        prompt: str,
        negative_prompt: str,
        duration: int,
        size: str,
        shot_type: str,
        enable_prompt_expansion: bool,
        seed: int,
        audio: str = "",
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        client = atlas_client.client

        payload = {
            "model": "alibaba/wan-2.6/text-to-video",
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "duration": duration,
            "size": size,
            "shot_type": shot_type,
            "enable_prompt_expansion": enable_prompt_expansion,
            "seed": seed,
        }
        if audio:
            payload["audio"] = audio

        prediction_id = client.generate_video(payload)
        result = client.poll_prediction(prediction_id, poll_interval_sec=poll_interval_sec, timeout_sec=float(timeout_sec))

        outputs = (result.get("data") or {}).get("outputs") or []
        if not outputs:
            raise RuntimeError(f"No outputs returned for prediction {prediction_id}: {result}")

        return (outputs[0], prediction_id)
