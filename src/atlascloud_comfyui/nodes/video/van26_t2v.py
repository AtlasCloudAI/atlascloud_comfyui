from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasVan26TextToVideo:
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
                        "1920*1080",
                        "1080*1920",
                        "1440*1440",
                        "1632*1248",
                        "1248*1632",
                    ],
                    {"default": "1920*1080", "tooltip": "Size (width*height)"},
                ),
                "duration": ([5, 10, 15], {"default": 5, "tooltip": "Duration (seconds)"}),
                "shot_type": (["multi", "single"], {"default": "multi", "tooltip": "Shot type"}),
                "enable_prompt_expansion": (
                    "BOOLEAN",
                    {"default": True, "tooltip": "Enable prompt optimizer"},
                ),
                "generate_audio": (
                    "BOOLEAN",
                    {"default": True, "tooltip": "Whether to automatically add audio"},
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
        shot_type: str,
        enable_prompt_expansion: bool,
        generate_audio: bool,
        seed: int,
        negative_prompt: str = "",
        audio: str = "",
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        # NOTE: Schema enforces enable_prompt_expansion==true when shot_type==multi.
        if shot_type == "multi" and not enable_prompt_expansion:
            raise RuntimeError("shot_type='multi' requires enable_prompt_expansion=True")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "atlascloud/van-2.6/text-to-video",
            "prompt": prompt,
            "size": size,
            "duration": int(duration),
            "shot_type": shot_type,
            "enable_prompt_expansion": bool(enable_prompt_expansion),
            "generate_audio": bool(generate_audio),
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
