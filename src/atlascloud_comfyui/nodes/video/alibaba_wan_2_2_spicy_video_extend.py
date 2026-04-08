from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasWan22SpicyVideoExtend:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "video_url": ("STRING", {"default": "", "tooltip": "Input video URL"}),
                "prompt": ("STRING", {"multiline": True, "tooltip": "Extend instruction"}),
            },
            "optional": {
                "duration": ([5, 10], {"default": 5, "tooltip": "Duration (seconds)"}),
                "resolution": (["480p", "720p"], {"default": "480p", "tooltip": "Resolution"}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2**31 - 1, "tooltip": "Random if -1"}),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"}),
                "timeout_sec": ("INT", {"default": 900, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        video_url: str,
        prompt: str,
        duration: int = 5,
        resolution: str = "480p",
        seed: int = -1,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        video_url = (video_url or "").strip()
        if not video_url:
            raise RuntimeError("video_url is required")

        prompt = (prompt or "").strip()
        if not prompt:
            raise RuntimeError("prompt is required for Alibaba WAN2.2 Spicy Video Extend")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "alibaba/wan-2.2-spicy/video-extend",
            "video_url": video_url,
            "prompt": prompt,
            "resolution": resolution,
            "duration": int(duration),
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
        if isinstance(first, dict):
            url = first.get("url") or first.get("video") or first.get("output")
            if isinstance(url, str) and url.strip():
                return (url, prediction_id)
            raise RuntimeError(f"Unexpected output object for prediction {prediction_id}: {first}")

        if not isinstance(first, str):
            raise RuntimeError(f"Unexpected output type for prediction {prediction_id}: {type(first).__name__} {first!r}")

        return (first, prediction_id)
