from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasViduQ2ProStartEndToVideo:
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
                "image": ("STRING", {"default": "", "tooltip": "Start image URL/base64"}),
                "end_image": ("STRING", {"default": "", "tooltip": "End image URL/base64"}),
            },
            "optional": {
                "duration": ("FLOAT", {"default": 5.0, "min": 1.0, "max": 60.0, "tooltip": "Duration (seconds)"}),
                "resolution": (["540p", "720p", "1080p"], {"default": "720p", "tooltip": "Resolution"}),
                "movement_amplitude": (["auto", "small", "medium", "large"], {"default": "auto", "tooltip": "Movement amplitude"}),
                "bgm": ("BOOLEAN", {"default": True, "tooltip": "Background music"}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 2147483647, "tooltip": "Seed"}),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"}),
                "timeout_sec": ("INT", {"default": 900, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        prompt: str,
        image: str,
        end_image: str,
        duration: float = 5.0,
        resolution: str = '720p',
        movement_amplitude: str = 'auto',
        bgm: bool = True,
        seed: int = 0,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        p = (prompt or "").strip()
        if not p:
            raise RuntimeError("prompt is required")

        image = (image or "").strip()
        if not image:
            raise RuntimeError("image is required")
        end_image = (end_image or "").strip()
        if not end_image:
            raise RuntimeError("end_image is required")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "vidu/q2-pro/start-end-to-video",
            "prompt": p,
            "image": image,
            "end_image": end_image,
            "duration": float(duration),
            "resolution": resolution,
            "movement_amplitude": movement_amplitude,
            "bgm": bool(bgm),
            "seed": int(seed),
        }

        prediction_id = client.generate_video(payload)
        result = client.poll_prediction(prediction_id, poll_interval_sec=float(poll_interval_sec), timeout_sec=float(timeout_sec))

        outputs = (result.get("data") or {}).get("outputs") or []
        if not outputs:
            raise RuntimeError(f"No outputs returned for prediction {prediction_id}: {result}")

        first = outputs[0]
        if not isinstance(first, str):
            raise RuntimeError(f"Unexpected output type for prediction {prediction_id}: {type(first).__name__} {first!r}")

        return (first, prediction_id)
