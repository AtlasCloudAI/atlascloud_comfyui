from __future__ import annotations

from typing import Any, Dict, List, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasWan22TurboSpicyInfiniteImageToVideoLoRA:
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
                    {"default": "", "tooltip": "First-frame image URL/base64"},
                ),
                "prompt": (
                    "STRING",
                    {
                        "multiline": True,
                        "tooltip": "Prompts (one per line). Each segment generates `duration` seconds.",
                    },
                ),
            },
            "optional": {
                "duration": (
                    "INT",
                    {"default": 5, "min": 1, "max": 60, "tooltip": "Seconds per prompt segment"},
                ),
                "resolution": (
                    ["480p", "720p", "1080p"],
                    {"default": "720p", "tooltip": "Output resolution"},
                ),
                "seed": (
                    "INT",
                    {"default": -1, "min": -1, "max": 2**31 - 1, "tooltip": "Random if -1"},
                ),
                "loras_json": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": True,
                        "tooltip": "Optional JSON array for `loras` (leave empty to omit)",
                    },
                ),
                "low_noise_loras_json": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": True,
                        "tooltip": "Optional JSON array for `low_noise_loras` (leave empty to omit)",
                    },
                ),
                "high_noise_loras_json": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": True,
                        "tooltip": "Optional JSON array for `high_noise_loras` (leave empty to omit)",
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
        image: str,
        prompt: str,
        duration: int = 5,
        resolution: str = "720p",
        seed: int = -1,
        loras_json: str = "",
        low_noise_loras_json: str = "",
        high_noise_loras_json: str = "",
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        import json

        client = atlas_client.client

        image = (image or "").strip()
        if not image:
            raise RuntimeError("image is required (URL or base64)")

        prompt_lines: List[str] = [ln.strip() for ln in (prompt or "").splitlines() if ln.strip()]
        if not prompt_lines:
            raise RuntimeError("prompt is required")

        payload: Dict[str, Any] = {
            "model": "atlascloud/wan-2.2-turbo-spicy/infinite-image-to-video-lora",
            "image": image,
            "prompt": prompt_lines,
            "duration": int(duration),
            "resolution": resolution,
            "seed": int(seed),
        }

        for key, raw in [
            ("loras", loras_json),
            ("low_noise_loras", low_noise_loras_json),
            ("high_noise_loras", high_noise_loras_json),
        ]:
            raw = (raw or "").strip()
            if not raw:
                continue
            try:
                val = json.loads(raw)
            except Exception as e:
                raise RuntimeError(f"{key}_json must be valid JSON: {e}")
            if not isinstance(val, list):
                raise RuntimeError(f"{key}_json must be a JSON array")
            payload[key] = val

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
