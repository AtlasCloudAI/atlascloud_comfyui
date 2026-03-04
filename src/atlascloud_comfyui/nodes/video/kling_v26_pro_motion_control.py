from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasKlingV26ProMotionControl:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "image": ("STRING", {"default": "", "tooltip": "Start image URL/base64"}),
                "video": ("STRING", {"default": "", "tooltip": "Reference video URL"}),
                "character_orientation": (
                    ["left", "right", "front", "back"],
                    {"default": "front", "tooltip": "Character orientation"},
                ),
                "prompt": ("STRING", {"multiline": True, "default": "", "tooltip": "Optional prompt"}),
            },
            "optional": {
                "keep_original_sound": ("BOOLEAN", {"default": True, "tooltip": "Keep original sound"}),
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
        video: str,
        character_orientation: str,
        prompt: str = "",
        keep_original_sound: bool = True,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        if not (image or "").strip():
            raise RuntimeError("image is required for Kling V2.6 Pro Motion-Control")
        if not (video or "").strip():
            raise RuntimeError("video is required for Kling V2.6 Pro Motion-Control")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "kwaivgi/kling-v2.6-pro/motion-control",
            "image": (image or "").strip(),
            "video": (video or "").strip(),
            "character_orientation": character_orientation,
            "keep_original_sound": bool(keep_original_sound),
        }

        p = (prompt or "").strip()
        if p:
            payload["prompt"] = p

        prediction_id = client.generate_video(payload)
        result = client.poll_prediction(prediction_id, poll_interval_sec=poll_interval_sec, timeout_sec=float(timeout_sec))

        outputs = (result.get("data") or {}).get("outputs") or []
        if not outputs:
            raise RuntimeError(f"No outputs returned for prediction {prediction_id}: {result}")

        return (outputs[0], prediction_id)
