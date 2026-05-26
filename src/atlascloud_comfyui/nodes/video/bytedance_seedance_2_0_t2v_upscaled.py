from __future__ import annotations

# NOTE: This node targets a model id that is no longer present in AtlasCloud /api/v1/models
# It is kept for backward compatibility with existing ComfyUI workflows.
DEPRECATED_MODEL_ID = True
DEPRECATION_REASON = "Model id not returned by AtlasCloud /api/v1/models; likely deprecated or removed upstream."

import os

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasSeedance20TextToVideoUpscaled:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "prompt": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": "The scene comes alive with gentle motion and cinematic lighting",
                        "tooltip": "Text prompt",
                    },
                ),
            },
            "optional": {
                "duration": (
                    [-1, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                    {"default": 5, "tooltip": "Duration (seconds), or -1 for auto"},
                ),
                "resolution": (["1080p", "2k"], {"default": "1080p", "tooltip": "Resolution"}),
                "ratio": (
                    ["16:9", "4:3", "1:1", "3:4", "9:16", "21:9"],
                    {"default": "16:9", "tooltip": "Aspect ratio"},
                ),
                "generate_audio": ("BOOLEAN", {"default": True, "tooltip": "Generate audio"}),
                "watermark": ("BOOLEAN", {"default": False, "tooltip": "Add watermark"}),
                "return_last_frame": (
                    "BOOLEAN",
                    {"default": False, "tooltip": "Return last frame (if supported)"},
                ),
                "web_search": ("BOOLEAN", {"default": False, "tooltip": "Enable web search (seedance-2.0 only)"}),
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
        duration: int = 5,
        resolution: str = "1080p",
        ratio: str = "16:9",
        generate_audio: bool = True,
        watermark: bool = False,
        return_last_frame: bool = False,
        web_search: bool = False,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        # Deprecated model guard
        if os.getenv("ATLAS_ALLOW_DEPRECATED_MODELS", "").lower() not in ("1", "true", "yes"):
            raise RuntimeError(
                "Deprecated model id: bytedance/seedance-2.0/text-to-video-upscaled. This node is kept for backward compatibility, but the model is not returned by AtlasCloud /api/v1/models. "
                "Set ATLAS_ALLOW_DEPRECATED_MODELS=1 to force execution at your own risk."
            )

        prompt = (prompt or "").strip()
        if not prompt:
            raise RuntimeError("prompt is required for AtlasCloud Seedance 2.0 Text-to-Video Upscaled")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "bytedance/seedance-2.0/text-to-video-upscaled",
            "prompt": prompt,
            "duration": int(duration),
            "resolution": resolution,
            "ratio": ratio,
            "generate_audio": bool(generate_audio),
            "watermark": bool(watermark),
            "return_last_frame": bool(return_last_frame),
            "web_search": bool(web_search),
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
            raise RuntimeError(f"Unexpected output type for prediction {prediction_id}: {type(first).__name__} {first!r}")

        return (first, prediction_id)
