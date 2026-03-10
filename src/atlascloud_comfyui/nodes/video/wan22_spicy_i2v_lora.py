from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasWan22SpicyImageToVideoLora:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "image": ("STRING", {"default": "", "tooltip": "Input image URL or base64"}),
                "prompt": ("STRING", {"multiline": True, "tooltip": "Text prompt"}),
                "resolution": (["480p", "720p"], {"default": "480p", "tooltip": "Resolution"}),
                "duration": ([5, 8], {"default": 5, "tooltip": "Duration (seconds)"}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2**31 - 1, "tooltip": "Random if -1"}),
                "loras_json": (
                    "STRING",
                    {
                        "default": "[]",
                        "multiline": True,
                        "tooltip": 'JSON array of LoRA objects for `loras`. Example: [{"path":"https://.../lora.safetensors","scale":1.0}]',
                    },
                ),
                "low_noise_loras_json": (
                    "STRING",
                    {
                        "default": "[]",
                        "multiline": True,
                        "tooltip": 'JSON array for `low_noise_loras`. Example: [{"path":"https://...","scale":1.0}]',
                    },
                ),
                "high_noise_loras_json": (
                    "STRING",
                    {
                        "default": "[]",
                        "multiline": True,
                        "tooltip": 'JSON array for `high_noise_loras`. Example: [{"path":"https://...","scale":1.0}]',
                    },
                ),
            },
            "optional": {
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
        image: str,
        prompt: str,
        resolution: str,
        duration: int,
        seed: int,
        loras_json: str = "[]",
        low_noise_loras_json: str = "[]",
        high_noise_loras_json: str = "[]",
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        image = (image or "").strip()
        if not image:
            raise RuntimeError("image is required (URL or base64)")

        prompt = (prompt or "").strip()
        if not prompt:
            raise RuntimeError("prompt is required")

        import json

        def parse_array(s: str, name: str):
            try:
                arr = json.loads(s) if (s or "").strip() else []
                if not isinstance(arr, list):
                    raise ValueError(f"{name} must be a JSON array")
                return arr
            except Exception as e:
                raise RuntimeError(f"Invalid {name}. Must be a JSON array. Error: {e}") from e

        loras = parse_array(loras_json, "loras_json")
        low_noise_loras = parse_array(low_noise_loras_json, "low_noise_loras_json")
        high_noise_loras = parse_array(high_noise_loras_json, "high_noise_loras_json")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "alibaba/wan-2.2-spicy/image-to-video-lora",
            "image": image,
            "prompt": prompt,
            "resolution": resolution,
            "duration": int(duration),
            "seed": int(seed),
        }

        if loras:
            payload["loras"] = loras
        if low_noise_loras:
            payload["low_noise_loras"] = low_noise_loras
        if high_noise_loras:
            payload["high_noise_loras"] = high_noise_loras

        prediction_id = client.generate_video(payload)
        result = client.poll_prediction(prediction_id, poll_interval_sec=float(poll_interval_sec), timeout_sec=float(timeout_sec))

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
