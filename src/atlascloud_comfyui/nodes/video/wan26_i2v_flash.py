from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasWAN26ImageToVideoFlash:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "image": ("STRING", {"default": "", "tooltip": "Image URL or base64"}),
                "prompt": ("STRING", {"multiline": True}),
                "resolution": (["720p", "1080p"], {"default": "720p"}),
            },
            "optional": {
                "audio": ("STRING", {"default": "", "tooltip": "Optional audio URL"}),
                "negative_prompt": ("STRING", {"multiline": True, "default": ""}),
                "duration": ("INT", {"default": 5, "min": 5, "max": 15, "tooltip": "Seconds"}),
                "enable_prompt_expansion": ("BOOLEAN", {"default": True}),
                "shot_type": (["multi", "single"], {"default": "multi"}),
                "generate_audio": ("BOOLEAN", {"default": True}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2**31 - 1}),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0}),
                "timeout_sec": ("INT", {"default": 900, "min": 30, "max": 7200}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        image: str,
        prompt: str,
        resolution: str,
        audio: str = "",
        negative_prompt: str = "",
        duration: int = 5,
        enable_prompt_expansion: bool = True,
        shot_type: str = "multi",
        generate_audio: bool = True,
        seed: int = -1,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        if not (image or "").strip():
            raise RuntimeError("image is required for WAN2.6 Image-to-Video Flash")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "alibaba/wan-2.6/image-to-video-flash",
            "image": image,
            "prompt": prompt,
            "resolution": resolution,
            "duration": int(duration),
            "enable_prompt_expansion": bool(enable_prompt_expansion),
            "shot_type": shot_type,
            "generate_audio": bool(generate_audio),
            "seed": int(seed),
        }

        if (audio or "").strip():
            payload["audio"] = audio
        if (negative_prompt or "").strip():
            payload["negative_prompt"] = negative_prompt

        prediction_id = client.generate_video(payload)
        result = client.poll_prediction(prediction_id, poll_interval_sec=poll_interval_sec, timeout_sec=float(timeout_sec))

        outputs = (result.get("data") or {}).get("outputs") or []
        if not outputs:
            raise RuntimeError(f"No outputs returned for prediction {prediction_id}: {result}")

        return (outputs[0], prediction_id)
