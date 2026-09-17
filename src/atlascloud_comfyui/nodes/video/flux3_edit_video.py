from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasFlux3EditVideo:
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
                        "default": "",
                        "tooltip": "How to change the input video; motion, timing and framing are preserved",
                    },
                ),
                "video_url": (
                    "STRING",
                    {"default": "", "tooltip": "URL of the input video to edit (mp4, under 50MB and under 15s)"},
                ),
            },
            "optional": {
                "safety_tolerance": (
                    "INT",
                    {"default": 2, "min": 0, "max": 4, "tooltip": "Safety tolerance (0 strictest, 4 most permissive)"},
                ),
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
        video_url: str,
        safety_tolerance: int = 2,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        prompt = (prompt or "").strip()
        if not prompt:
            raise RuntimeError("prompt is required for AtlasCloud FLUX 3 Edit Video")

        video_url = (video_url or "").strip()
        if not video_url:
            raise RuntimeError("video_url is required (public mp4 URL)")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "black-forest-labs/flux-3/edit-video",
            "prompt": prompt,
            "video_url": video_url,
            "safety_tolerance": int(safety_tolerance),
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
