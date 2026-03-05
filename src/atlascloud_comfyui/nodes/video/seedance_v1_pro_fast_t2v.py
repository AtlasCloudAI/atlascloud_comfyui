from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasSeedanceV1ProFastTextToVideo:
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
                "resolution": (["480p", "720p", "1080p"], {"default": "480p", "tooltip": "Resolution"}),
                "duration": (
                    [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                    {"default": 5, "tooltip": "Duration (seconds)"},
                ),
                "aspect_ratio": (
                    ["21:9", "16:9", "4:3", "1:1", "3:4", "9:16"],
                    {"default": "16:9", "tooltip": "Aspect ratio"},
                ),
                "camera_fixed": ("BOOLEAN", {"default": False, "tooltip": "Fix camera position"}),
                "seed": (
                    "INT",
                    {"default": -1, "min": -1, "max": 2**31 - 1, "tooltip": "Random if -1"},
                ),
            },
            "optional": {
                "poll_interval_sec": (
                    "FLOAT",
                    {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"},
                ),
                "timeout_sec": (
                    "INT",
                    {"default": 900, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"},
                ),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        prompt: str,
        resolution: str,
        duration: int,
        aspect_ratio: str,
        camera_fixed: bool,
        seed: int,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "bytedance/seedance-v1-pro-fast/text-to-video",
            "prompt": prompt,
            "resolution": resolution,
            "duration": int(duration),
            "aspect_ratio": aspect_ratio,
            "camera_fixed": bool(camera_fixed),
            "seed": int(seed),
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

        first = outputs[0]
        if not isinstance(first, str):
            raise RuntimeError(f"Unexpected output type for prediction {prediction_id}: {type(first).__name__} {first!r}")

        return (first, prediction_id)
