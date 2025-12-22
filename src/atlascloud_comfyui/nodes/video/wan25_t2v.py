from __future__ import annotations

from typing import Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasWAN25TextToVideo:
    """
    ComfyUI Node: AtlasCloud WAN 2.5 Text-to-Video (remote API)
    Outputs: video_url, prediction_id
    """

    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "prompt": ("STRING", {"multiline": True}),
                "negative_prompt": ("STRING", {"multiline": True, "default": ""}),
                "duration": ([5, 10], {"default": 5}),
                "size": (
                    ["1280*720", "1920*1080", "720*1280", "1080*1920", "832*480", "480*832"],
                    {"default": "1280*720", "tooltip": "Resolution"},
                ),
                "enable_prompt_expansion": ("BOOLEAN", {"default": False}),
                "seed": ("INT", {"default": 1010059064, "min": -1, "max": 2**31 - 1}),
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
        enable_prompt_expansion: bool,
        seed: int,
        audio: str = "",
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        client = atlas_client.client

        payload = {
            "model": "alibaba/wan-2.5/text-to-video",
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "duration": duration,
            "size": size,
            "enable_prompt_expansion": enable_prompt_expansion,
            "seed": seed,
        }
        if audio:
            payload["audio"] = audio

        prediction_id = client.generate_video(payload)
        result = client.poll_prediction(
            prediction_id,
            poll_interval_sec=poll_interval_sec,
            timeout_sec=float(timeout_sec),
        )

        outputs = (result.get("data") or {}).get("outputs") or []
        if not outputs:
            raise RuntimeError(f"No outputs returned for prediction {prediction_id}: {result}")

        video_url = outputs[0]
        return (video_url, prediction_id)
