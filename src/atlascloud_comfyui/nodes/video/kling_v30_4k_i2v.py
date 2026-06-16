from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasKlingV304KImageToVideo:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                # Kling I2V: base image is required
                "image": ("STRING", {"default": "", "tooltip": "First frame image URL or base64"}),
                "prompt": ("STRING", {"multiline": True, "tooltip": "Text prompt"}),
                "duration": ([3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], {"default": 5, "tooltip": "Duration (seconds)"}),
                "cfg_scale": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.01, "tooltip": "Classifier-free guidance scale"}),
                "sound": ("BOOLEAN", {"default": True, "tooltip": "Generate sound track"}),
            },
            "optional": {
                "end_image": ("STRING", {"default": "", "tooltip": "Optional end image URL or base64"}),
                "negative_prompt": ("STRING", {"default": "", "multiline": True, "tooltip": "Negative prompt (optional)"}),
                "resolution": (["1080P", "4K"], {"default": "1080P", "tooltip": "Output resolution"}),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"}),
                "timeout_sec": ("INT", {"default": 900, "min": 30, "max": 7200, "tooltip": "Polling timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        image: str,
        prompt: str,
        duration: int,
        cfg_scale: float,
        sound: bool,
        end_image: str = "",
        negative_prompt: str = "",
        resolution: str = "1080P",
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        image = (image or "").strip()
        if not image:
            raise RuntimeError("image is required for Kling V3.0 4K Image-to-Video")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "kwaivgi/kling-v3.0-4k/image-to-video",
            "image": image,
            "prompt": (prompt or "").strip(),
            "duration": int(duration),
            "cfg_scale": float(cfg_scale),
            "sound": bool(sound),
            "resolution": resolution,
        }

        neg = (negative_prompt or "").strip()
        if neg:
            payload["negative_prompt"] = neg

        end_img = (end_image or "").strip()
        if end_img:
            payload["end_image"] = end_img

        prediction_id = client.generate_video(payload)
        result = client.poll_prediction(
            prediction_id,
            poll_interval_sec=float(poll_interval_sec),
            timeout_sec=float(timeout_sec),
        )

        outputs = (result.get("data") or {}).get("outputs") or []
        if not outputs:
            raise RuntimeError(f"No outputs returned for prediction {prediction_id}: {result}")

        return (outputs[0], prediction_id)
