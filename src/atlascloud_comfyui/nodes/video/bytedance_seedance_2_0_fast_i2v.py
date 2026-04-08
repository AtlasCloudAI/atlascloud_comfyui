from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasSeedance20FastImageToVideo:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "image": (
                    "STRING",
                    {"default": "", "tooltip": "First frame image (URL or base64)"},
                ),
            },
            "optional": {
                "prompt": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": "The scene comes alive with gentle motion and cinematic lighting",
                        "tooltip": "Prompt (optional)",
                    },
                ),
                "duration": (
                    [-1, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                    {"default": 5, "tooltip": "Duration (seconds), or -1 for auto"},
                ),
                "resolution": (["480p", "720p"], {"default": "720p", "tooltip": "Resolution"}),
                "ratio": (
                    ["16:9", "4:3", "1:1", "3:4", "9:16", "21:9", "adaptive"],
                    {"default": "adaptive", "tooltip": "Aspect ratio (adaptive = auto)"},
                ),
                "generate_audio": ("BOOLEAN", {"default": True, "tooltip": "Generate audio"}),
                "last_image": (
                    "STRING",
                    {"default": "", "tooltip": "Optional last frame image (URL/base64)"},
                ),
                "watermark": ("BOOLEAN", {"default": False, "tooltip": "Add watermark"}),
                "return_last_frame": ("BOOLEAN", {"default": False, "tooltip": "Return last frame (if supported)"}),
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
        image: str,
        prompt: str = "The scene comes alive with gentle motion and cinematic lighting",
        duration: int = 5,
        resolution: str = "720p",
        ratio: str = "adaptive",
        generate_audio: bool = True,
        last_image: str = "",
        watermark: bool = False,
        return_last_frame: bool = False,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        image = (image or "").strip()
        if not image:
            raise RuntimeError("image is required for AtlasCloud Seedance 2.0 Fast Image-to-Video")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "bytedance/seedance-2.0-fast/image-to-video",
            "image": image,
            "duration": int(duration),
            "resolution": resolution,
            "ratio": ratio,
            "generate_audio": bool(generate_audio),
            "watermark": bool(watermark),
            "return_last_frame": bool(return_last_frame),
        }

        p = (prompt or "").strip()
        if p:
            payload["prompt"] = p

        li = (last_image or "").strip()
        if li:
            payload["last_image"] = li

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
