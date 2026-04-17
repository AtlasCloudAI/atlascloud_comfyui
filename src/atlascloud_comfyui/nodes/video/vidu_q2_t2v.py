from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasViduQ2TextToVideo:
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
            },
            "optional": {
                "duration": ("FLOAT", {"default": 5.0, "min": 1.0, "max": 60.0, "tooltip": "Duration (seconds)"}),
                "resolution": (["540p", "720p", "1080p"], {"default": "720p", "tooltip": "Resolution"}),
                "aspect_ratio": (["16:9", "9:16", "1:1", "4:3", "3:4"], {"default": "16:9", "tooltip": "Aspect ratio"}),
                "style": (["general", "anime"], {"default": "general", "tooltip": "Style"}),
                "movement_amplitude": (["auto", "small", "medium", "large"], {"default": "auto", "tooltip": "Movement amplitude"}),
                "generate_audio": ("BOOLEAN", {"default": True, "tooltip": "Whether to generate audio"}),
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
        duration: float = 5.0,
        resolution: str = '720p',
        aspect_ratio: str = '16:9',
        style: str = 'general',
        movement_amplitude: str = 'auto',
        generate_audio: bool = True,
        bgm: bool = True,
        seed: int = 0,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        p = (prompt or "").strip()
        if not p:
            raise RuntimeError("prompt is required")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "vidu/q2/text-to-video",
            "prompt": p,
            "duration": float(duration),
            "resolution": resolution,
            "aspect_ratio": aspect_ratio,
            "style": style,
            "movement_amplitude": movement_amplitude,
            "generate_audio": bool(generate_audio),
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
