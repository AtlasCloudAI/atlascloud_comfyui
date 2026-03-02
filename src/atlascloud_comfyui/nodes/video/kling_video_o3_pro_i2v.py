from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasKlingVideoO3ProImageToVideo:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "prompt": ("STRING", {"multiline": True}),
                "image": ("STRING", {"default": "", "tooltip": "First frame image URL"}),
            },
            "optional": {
                "end_image": ("STRING", {"default": "", "tooltip": "Last frame image URL (optional)"}),
                "duration": ("INT", {"default": 5, "min": 3, "max": 15}),
                "generate_audio": ("BOOLEAN", {"default": False}),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0}),
                "timeout_sec": ("INT", {"default": 900, "min": 30, "max": 7200}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        prompt: str,
        image: str,
        end_image: str = "",
        duration: int = 5,
        generate_audio: bool = False,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        if not (image or "").strip():
            raise RuntimeError("image is required for Kling Video O3 Pro Image-to-Video")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "kwaivgi/kling-video-o3-pro/image-to-video",
            "prompt": prompt,
            "image": image,
            "duration": int(duration),
            "generate_audio": bool(generate_audio),
        }

        if (end_image or "").strip():
            payload["end_image"] = end_image

        prediction_id = client.generate_video(payload)
        result = client.poll_prediction(prediction_id, poll_interval_sec=poll_interval_sec, timeout_sec=float(timeout_sec))

        outputs = (result.get("data") or {}).get("outputs") or []
        if not outputs:
            raise RuntimeError(f"No outputs returned for prediction {prediction_id}: {result}")

        return (outputs[0], prediction_id)
