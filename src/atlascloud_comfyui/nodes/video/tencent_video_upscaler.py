from __future__ import annotations

from typing import Any, Dict, List, Tuple

from ..auth.atlas_client_node import AtlasClientHandle

TEMPLATES: List[str] = [
    "live-action-enhance-720p",
    "live-action-enhance-1080p",
    "live-action-enhance-2k",
    "live-action-enhance-4k",
    "anime-enhance-720p",
    "anime-enhance-1080p",
    "anime-enhance-2k",
    "anime-enhance-4k",
    "restore-720p",
    "restore-1080p",
    "restore-2k",
    "restore-4k",
    "live-action-smallface-720p",
    "live-action-smallface-1080p",
    "live-action-smallface-2k",
    "live-action-smallface-4k",
    "anime-smallface-720p",
    "anime-smallface-1080p",
    "anime-smallface-2k",
    "anime-smallface-4k",
    "seedance2-enhance-720p",
    "seedance2-enhance-1080p",
    "seedance2-enhance-2k",
    "seedance2-enhance-4k",
]


class AtlasTencentVideoUpscaler:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "video_url": ("STRING", {"default": "", "tooltip": "Public HTTP(S) URL of the source video"}),
            },
            "optional": {
                "template": (
                    TEMPLATES,
                    {"default": "anime-enhance-4k", "tooltip": "Enhancement template (content type + target tier)"},
                ),
                "short": (
                    "INT",
                    {"default": 0, "min": 0, "max": 4320, "tooltip": "Output short edge in pixels (0 = keep source)"},
                ),
                "fps": (
                    "INT",
                    {"default": 0, "min": 0, "max": 120, "tooltip": "Frame-interpolation target FPS (0 = keep source)"},
                ),
                "keep_metadata": ("BOOLEAN", {"default": True, "tooltip": "Preserve source media metadata"}),
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
        video_url: str,
        template: str = "anime-enhance-4k",
        short: int = 0,
        fps: int = 0,
        keep_metadata: bool = True,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        vid = (video_url or "").strip()
        if not vid:
            raise RuntimeError("video_url is required for Tencent Video Upscaler")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "tencent/video/upscaler",
            "video_url": vid,
            "template": template,
            "short": int(short),
            "keep_metadata": bool(keep_metadata),
        }

        if int(fps) > 0:
            payload["fps"] = int(fps)

        prediction_id = client.generate_video(payload)
        result = client.poll_prediction(
            prediction_id,
            poll_interval_sec=float(poll_interval_sec),
            timeout_sec=float(timeout_sec),
        )

        outputs = (result.get("data") or {}).get("outputs") or []
        if not outputs:
            raise RuntimeError(f"No outputs returned for prediction {prediction_id}: {result}")

        return (outputs[0], prediction_id)
