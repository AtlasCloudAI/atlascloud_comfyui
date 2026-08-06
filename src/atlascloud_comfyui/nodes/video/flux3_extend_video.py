from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle

_ASPECT_RATIOS = ["auto", "21:9", "2:1", "16:9", "4:3", "1:1", "3:4", "9:16"]
_RESOLUTIONS = ["720p", "1080p"]


class AtlasFlux3ExtendVideo:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "video_url": (
                    "STRING",
                    {"default": "", "tooltip": "URL of the input video to extend (mp4, under 50MB and under 15s)"},
                ),
            },
            "optional": {
                "prompt": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": "",
                        "tooltip": "How the video continues from the source clip's final frames",
                    },
                ),
                "aspect_ratio": (
                    _ASPECT_RATIOS,
                    {"default": "auto", "tooltip": "Aspect ratio of the generated video ('auto' lets the model choose)"},
                ),
                "resolution": (_RESOLUTIONS, {"default": "720p", "tooltip": "Output resolution"}),
                "duration": ("INT", {"default": 5, "min": 5, "max": 20, "tooltip": "Duration (seconds, 5-20)"}),
                "generate_audio": ("BOOLEAN", {"default": True, "tooltip": "Whether to generate audio for the video"}),
                "safety_tolerance": (
                    "INT",
                    {"default": 2, "min": 0, "max": 4, "tooltip": "Safety tolerance (0 strictest, 4 most permissive)"},
                ),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2**31 - 1, "tooltip": "Random seed (-1 for random)"}),
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
        prompt: str = "",
        aspect_ratio: str = "auto",
        resolution: str = "720p",
        duration: int = 5,
        generate_audio: bool = True,
        safety_tolerance: int = 2,
        seed: int = -1,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        video_url = (video_url or "").strip()
        if not video_url:
            raise RuntimeError("video_url is required (public mp4 URL)")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "black-forest-labs/flux-3/extend-video",
            "video_url": video_url,
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
            "duration": int(duration),
            "generate_audio": bool(generate_audio),
            "safety_tolerance": int(safety_tolerance),
        }

        p = (prompt or "").strip()
        if p:
            payload["prompt"] = p
        if seed >= 0:
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
