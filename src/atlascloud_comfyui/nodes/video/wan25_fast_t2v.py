from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasWAN25TextToVideoFast:
    """
    AtlasCloud WAN 2.5 Text-to-Video Fast
    """

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
                "size": (
                    [
                        "1280*720",
                        "720*1280",
                        "1920*1080",
                        "1080*1920",
                    ],
                    {"default": "1280*720", "tooltip": "Size (width*height)"},
                ),
                "duration": ([5, 10], {"default": 5, "tooltip": "Duration (seconds)"}),
                "enable_prompt_expansion": (
                    "BOOLEAN",
                    {"default": False, "tooltip": "Enable prompt optimizer"},
                ),
                "seed": (
                    "INT",
                    {"default": -1, "min": -1, "max": 2**31 - 1, "tooltip": "Random if -1"},
                ),
            },
            "optional": {
                "negative_prompt": ("STRING", {"multiline": True, "default": "", "tooltip": "Negative prompt"}),
                "audio": ("STRING", {"default": "", "tooltip": "Audio URL (optional)"}),
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
        size: str,
        duration: int,
        enable_prompt_expansion: bool,
        seed: int,
        negative_prompt: str = "",
        audio: str = "",
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "alibaba/wan-2.5/text-to-video-fast",
            "prompt": prompt,
            "size": size,
            "duration": int(duration),
            "enable_prompt_expansion": bool(enable_prompt_expansion),
            "seed": int(seed),
        }

        neg = (negative_prompt or "").strip()
        if neg:
            payload["negative_prompt"] = neg

        aud = (audio or "").strip()
        if aud:
            payload["audio"] = aud

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
