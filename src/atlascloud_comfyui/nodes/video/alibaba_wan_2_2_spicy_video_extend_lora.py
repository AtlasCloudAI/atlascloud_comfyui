from __future__ import annotations

from typing import Any, Dict, List, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasWan22SpicyVideoExtendLora:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "video": ("STRING", {"default": "", "tooltip": "Input video URL/base64"}),
                "prompt": ("STRING", {"multiline": True, "tooltip": "Extend instruction"}),
            },
            "optional": {
                "duration": ([5, 8], {"default": 5, "tooltip": "Duration (seconds)"}),
                "resolution": (["480p", "720p"], {"default": "480p", "tooltip": "Resolution"}),
                "seed": (
                    "INT",
                    {"default": -1, "min": -1, "max": 2**31 - 1, "tooltip": "Random if -1"},
                ),
                "loras_json": (
                    "STRING",
                    {
                        "default": "[]",
                        "multiline": True,
                        "tooltip": "Optional JSON array for `loras`",
                    },
                ),
                "low_noise_loras_json": (
                    "STRING",
                    {
                        "default": "[]",
                        "multiline": True,
                        "tooltip": "Optional JSON array for `low_noise_loras`",
                    },
                ),
                "high_noise_loras_json": (
                    "STRING",
                    {
                        "default": "[]",
                        "multiline": True,
                        "tooltip": "Optional JSON array for `high_noise_loras`",
                    },
                ),
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
        video: str,
        prompt: str,
        duration: int = 5,
        resolution: str = "480p",
        seed: int = -1,
        loras_json: str = "[]",
        low_noise_loras_json: str = "[]",
        high_noise_loras_json: str = "[]",
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        client = atlas_client.client

        video = (video or "").strip()
        if not video:
            raise RuntimeError("video is required (URL or base64)")

        prompt = (prompt or "").strip()
        if not prompt:
            raise RuntimeError("prompt is required for Alibaba WAN2.2 Spicy Video Extend LoRA")

        payload: Dict[str, Any] = {
            "model": "alibaba/wan-2.2-spicy/video-extend-lora",
            "prompt": prompt,
            "video": video,
            "duration": int(duration),
            "resolution": resolution,
            "seed": int(seed),
        }

        def parse_json_array(s: str, *, field_name: str) -> List[Any]:
            s = (s or "").strip()
            if not s or s == "[]":
                return []
            import json

            try:
                v = json.loads(s)
            except Exception as e:
                raise RuntimeError(f"Invalid {field_name}. Must be a JSON array. Error: {e}") from e
            if not isinstance(v, list):
                raise RuntimeError(f"{field_name} must be a JSON array")
            return v

        loras = parse_json_array(loras_json, field_name="loras_json")
        if loras:
            payload["loras"] = loras

        low = parse_json_array(low_noise_loras_json, field_name="low_noise_loras_json")
        if low:
            payload["low_noise_loras"] = low

        high = parse_json_array(high_noise_loras_json, field_name="high_noise_loras_json")
        if high:
            payload["high_noise_loras"] = high

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
