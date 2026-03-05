from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasKlingV20I2VMaster:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "image": ("STRING", {"default": "", "tooltip": "First frame image URL/base64"}),
                "prompt": ("STRING", {"multiline": True, "tooltip": "Text prompt"}),
                "duration": ([5, 10], {"default": 5, "tooltip": "Duration (seconds)"}),
                "guidance_scale": (
                    "FLOAT",
                    {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.01, "tooltip": "Guidance scale"},
                ),
            },
            "optional": {
                "end_image": ("STRING", {"default": "", "tooltip": "Optional tail frame image URL/base64"}),
                "negative_prompt": ("STRING", {"multiline": True, "default": "", "tooltip": "Negative prompt"}),
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
        duration: int,
        guidance_scale: float,
        end_image: str = "",
        negative_prompt: str = "",
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        image = (image or "").strip()
        if not image:
            raise RuntimeError("image is required (URL or base64)")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "kwaivgi/kling-v2.0-i2v-master",
            "image": image,
            "prompt": prompt,
            "duration": int(duration),
            "guidance_scale": float(guidance_scale),
        }

        end_image = (end_image or "").strip()
        if end_image:
            payload["end_image"] = end_image

        neg = (negative_prompt or "").strip()
        if neg:
            payload["negative_prompt"] = neg

        prediction_id = client.generate_video(payload)
        result = client.poll_prediction(prediction_id, poll_interval_sec=float(poll_interval_sec), timeout_sec=float(timeout_sec))

        outputs = (result.get("data") or {}).get("outputs") or []
        if not outputs:
            raise RuntimeError(f"No outputs returned for prediction {prediction_id}: {result}")

        first = outputs[0]
        if not isinstance(first, str):
            raise RuntimeError(f"Unexpected output type for prediction {prediction_id}: {type(first).__name__} {first!r}")

        return (first, prediction_id)
