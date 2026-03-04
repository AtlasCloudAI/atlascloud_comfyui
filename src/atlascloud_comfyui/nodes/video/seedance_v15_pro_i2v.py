from __future__ import annotations

from typing import Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasSeedanceV15ProImageToVideo:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "image": ("STRING", {"default": "", "tooltip": "Start image URL/base64"}),
                "aspect_ratio": (
                    ["21:9", "16:9", "4:3", "1:1", "3:4", "9:16"],
                    {"default": "16:9", "tooltip": "Aspect ratio"},
                ),
                "duration": ("INT", {"default": 5, "min": 1, "max": 60, "tooltip": "Duration (seconds)"}),
                "resolution": (["720p", "480p"], {"default": "720p", "tooltip": "Resolution preset"}),
                "prompt": ("STRING", {"multiline": True, "default": "", "tooltip": "Optional prompt"}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2**31 - 1, "tooltip": "Random if -1"}),
            },
            "optional": {
                "camera_fixed": ("BOOLEAN", {"default": False, "tooltip": "Fixed camera"}),
                "generate_audio": ("BOOLEAN", {"default": True, "tooltip": "Generate audio"}),
                "last_image": ("STRING", {"default": "", "tooltip": "Optional last image URL/base64"}),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"}),
                "timeout_sec": ("INT", {"default": 900, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        image: str,
        aspect_ratio: str,
        duration: int,
        resolution: str,
        prompt: str,
        seed: int,
        camera_fixed: bool = False,
        generate_audio: bool = True,
        last_image: str = "",
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        if not (image or "").strip():
            raise RuntimeError("image is required for Seedance V1.5 Pro Image-to-Video")

        client = atlas_client.client

        payload = {
            "model": "bytedance/seedance-v1.5-pro/image-to-video",
            "image": (image or "").strip(),
            "aspect_ratio": aspect_ratio,
            "duration": int(duration),
            "resolution": resolution,
            "seed": int(seed),
            "camera_fixed": bool(camera_fixed),
            "generate_audio": bool(generate_audio),
        }

        p = (prompt or "").strip()
        if p:
            payload["prompt"] = p

        li = (last_image or "").strip()
        if li:
            payload["last_image"] = li

        prediction_id = client.generate_video(payload)
        result = client.poll_prediction(prediction_id, poll_interval_sec=poll_interval_sec, timeout_sec=float(timeout_sec))

        outputs = (result.get("data") or {}).get("outputs") or []
        if not outputs:
            raise RuntimeError(f"No outputs returned for prediction {prediction_id}: {result}")

        return (outputs[0], prediction_id)
