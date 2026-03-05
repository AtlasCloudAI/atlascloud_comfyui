from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasVeo3FastImageToVideo:
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
                "aspect_ratio": (["16:9", "9:16"], {"default": "16:9", "tooltip": "Aspect ratio"}),
                "duration": ([8, 6, 4], {"default": 8, "tooltip": "Duration (seconds)"}),
                "resolution": (["720p", "1080p"], {"default": "720p", "tooltip": "Resolution"}),
                "generate_audio": ("BOOLEAN", {"default": False, "tooltip": "Generate audio"}),
            },
            "optional": {
                "negative_prompt": ("STRING", {"multiline": True, "default": "", "tooltip": "Negative prompt"}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2**31 - 1, "tooltip": "Seed"}),
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
        aspect_ratio: str,
        duration: int,
        resolution: str,
        generate_audio: bool,
        negative_prompt: str = "",
        seed: int = -1,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        image = (image or "").strip()
        if not image:
            raise RuntimeError("image is required (URL or base64)")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "google/veo3-fast/image-to-video",
            "image": image,
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "duration": int(duration),
            "resolution": resolution,
            "generate_audio": bool(generate_audio),
        }

        neg = (negative_prompt or "").strip()
        if neg:
            payload["negative_prompt"] = neg

        if int(seed) >= 0:
            payload["seed"] = int(seed)

        prediction_id = client.generate_video(payload)
        result = client.poll_prediction(prediction_id, poll_interval_sec=float(poll_interval_sec), timeout_sec=float(timeout_sec))

        outputs = (result.get("data") or {}).get("outputs") or []
        if not outputs:
            raise RuntimeError(f"No outputs returned for prediction {prediction_id}: {result}")

        first = outputs[0]
        if not isinstance(first, str):
            raise RuntimeError(f"Unexpected output type for prediction {prediction_id}: {type(first).__name__} {first!r}")

        return (first, prediction_id)
