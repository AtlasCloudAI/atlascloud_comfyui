from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasKlingV25TurboProImageToVideo:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "image": ("STRING", {"default": "", "tooltip": "Input image URL (jpg/jpeg/png, max 10MB)"}),
                "prompt": ("STRING", {"multiline": True, "tooltip": "Text prompt (max 2500 chars)"}),
                "duration": ([5, 10], {"default": 5, "tooltip": "Duration (seconds)"}),
                "guidance_scale": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.01, "tooltip": "Guidance scale"}),
            },
            "optional": {
                "negative_prompt": ("STRING", {"multiline": True, "default": "", "tooltip": "Negative prompt"}),
                "last_image": ("STRING", {"default": "", "tooltip": "End frame image URL for interpolation"}),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"}),
                "timeout_sec": ("INT", {"default": 900, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        image: str,
        prompt: str,
        duration: int,
        guidance_scale: float,
        negative_prompt: str = "",
        last_image: str = "",
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        client = atlas_client.client

        image = (image or "").strip()
        if not image:
            raise RuntimeError("image is required (URL or base64)")

        payload: Dict[str, Any] = {
            "model": "kwaivgi/kling-v2.5-turbo-pro/image-to-video",
            "image": image,
            "prompt": prompt,
            "duration": int(duration),
            "guidance_scale": guidance_scale,
        }

        neg = (negative_prompt or "").strip()
        if neg:
            payload["negative_prompt"] = neg

        end_img = (last_image or "").strip()
        if end_img:
            payload["last_image"] = end_img

        prediction_id = client.generate_video(payload)
        result = client.poll_prediction(
            prediction_id,
            poll_interval_sec=poll_interval_sec,
            timeout_sec=float(timeout_sec),
        )

        outputs = (result.get("data") or {}).get("outputs") or []
        if not outputs:
            raise RuntimeError(f"No outputs returned for prediction {prediction_id}: {result}")

        return (outputs[0], prediction_id)
