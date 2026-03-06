from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasBytedanceSeedanceV1LiteI2V720p:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "image": ("STRING", {"default": "", "tooltip": 'Input image supports both URL and Base64 format; Supported image formats include .jpg/.jpeg/.png; The image file size cannot exceed 10MB, and the image resolution should not be less than 300*300px'}),
                "prompt": ("STRING", {"multiline": True, "tooltip": 'Text prompt for video generation; Positive text prompt; Cannot exceed 2000 characters'}),
            },
            "optional": {
                "duration": ("INT", {"default": 5, "tooltip": 'Generate video duration length seconds.'}),
                "aspect_ratio": (['21:9', '16:9', '4:3', '1:1', '3:4', '9:16'], {"tooltip": 'The aspect ratio of the generated media.'}),
                "seed": ("INT", {"default": -1, "tooltip": 'The seed for random number generation.'}),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"}),
                "timeout_sec": ("INT", {"default": 900, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        image: str,
        prompt: str,
        duration: int = 5,
        aspect_ratio: str = None,
        seed: int = -1,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        client = atlas_client.client

        image = (image or "").strip()
        if not image:
            raise RuntimeError("image is required (URL or base64)")

        payload: Dict[str, Any] = {
            "model": "bytedance/seedance-v1-lite-i2v-720p",
            "image": image,
            "prompt": prompt,
            "duration": int(duration),
            "aspect_ratio": aspect_ratio,
            "seed": int(seed),
        }

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
            raise RuntimeError(
                f"Unexpected output type for prediction {prediction_id}: {type(first).__name__} {first!r}"
            )

        return (first, prediction_id)
