from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle

_RESOLUTIONS = ["1080P", "720P", "480P"]


class AtlasWan30PrimeImageToVideo:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "prompt": ("STRING", {"multiline": True, "tooltip": "Motion / action for the video (up to 20000 chars)"}),
                "image": ("STRING", {"default": "", "tooltip": "First frame image URL (jpeg/jpg/png/bmp/webp)"}),
            },
            "optional": {
                "last_image": (
                    "STRING",
                    {"default": "", "tooltip": "Optional last frame; the model interpolates from the first frame to it"},
                ),
                "resolution": (_RESOLUTIONS, {"default": "1080P", "tooltip": "Resolution"}),
                "duration": (
                    "INT",
                    {"default": 5, "min": -1, "max": 30, "tooltip": "Video length in seconds (2-30); -1 for smart-duration"},
                ),
                "audio": ("BOOLEAN", {"default": True, "tooltip": "Include an audio track (same price either way)"}),
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
        last_image: str = "",
        resolution: str = "1080P",
        duration: int = 5,
        audio: bool = True,
        seed: int = -1,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        prompt = (prompt or "").strip()
        if not prompt:
            raise RuntimeError("prompt is required for AtlasCloud WAN3.0-Prime Image-to-Video")

        image = (image or "").strip()
        if not image:
            raise RuntimeError("image is required for AtlasCloud WAN3.0-Prime Image-to-Video")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "alibaba/wan-3.0-prime/image-to-video",
            "prompt": prompt,
            "image": image,
            "resolution": resolution,
            "duration": int(duration),
            "audio": bool(audio),
        }

        li = (last_image or "").strip()
        if li:
            payload["last_image"] = li

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
