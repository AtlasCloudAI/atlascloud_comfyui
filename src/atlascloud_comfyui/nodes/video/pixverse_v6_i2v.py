from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasPixVerseV6ImageToVideo:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "image": ("STRING", {"default": "", "tooltip": "Input image URL or base64 (.jpg/.jpeg/.png)"}),
                "prompt": ("STRING", {"multiline": True, "tooltip": "Text prompt (1-5000 chars)"}),
            },
            "optional": {
                "duration": ("INT", {"default": 5, "min": 1, "max": 15, "tooltip": "Duration (seconds, 1-15)"}),
                "quality": (["360p", "540p", "720p", "1080p"], {"default": "720p", "tooltip": "Output resolution"}),
                "sound": ("BOOLEAN", {"default": True, "tooltip": "Generate audio together with the video"}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 2**31 - 1, "tooltip": "Random seed"}),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"}),
                "timeout_sec": ("INT", {"default": 900, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        image: str,
        prompt: str,
        duration: int = 5,
        quality: str = "720p",
        sound: bool = True,
        seed: int = 0,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        image = (image or "").strip()
        if not image:
            raise RuntimeError("image is required (URL or base64)")

        prompt = (prompt or "").strip()
        if not prompt:
            raise RuntimeError("prompt is required")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "pixverse/v6/image-to-video",
            "image": image,
            "prompt": prompt,
            "duration": int(duration),
            "quality": quality,
            "sound": bool(sound),
            "seed": int(seed),
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
