from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasKwaivgiKlingV16I2VPro:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "prompt": ("STRING", {"multiline": True, "tooltip": 'The positive prompt for the generation. max length 2500'}),
                "image": ("STRING", {"default": "", "tooltip": 'First frame of the video; Supported image formats include.jpg/.jpeg/.png; The image file size cannot exceed 10MB, and the image resolution should not be less than 300*300px, and the aspect ratio of the image should be between 1:2.5 ~ 2.5:1.'}),
            },
            "optional": {
                "negative_prompt": ("STRING", {"multiline": True, "tooltip": 'The negative prompt for the generation.'}),
                "end_image": ("STRING", {"default": "", "tooltip": 'Tail frame of the video; Supported image formats include.jpg/.jpeg/.png; The image file size cannot exceed 10MB, and the image resolution should not be less than 300*300px.'}),
                "duration": ([5, 10], {"default": 5, "tooltip": 'The duration of the generated media in seconds.'}),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"}),
                "timeout_sec": ("INT", {"default": 900, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        prompt: str,
        image: str,
        negative_prompt: str = None,
        end_image: str = None,
        duration: int = 5,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        client = atlas_client.client

        image = (image or "").strip()
        if not image:
            raise RuntimeError("image is required (URL or base64)")

        payload: Dict[str, Any] = {
            "model": "kwaivgi/kling-v1.6-i2v-pro",
            "prompt": prompt,
            "image": image,
            "negative_prompt": negative_prompt,
            "end_image": end_image,
            "duration": int(duration),
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
