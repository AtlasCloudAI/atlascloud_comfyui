from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle

_CHARACTER_ORIENTATIONS = ["image", "video"]


class AtlasKlingV30ProMotionControl:
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
                    {
                        "default": "",
                        "tooltip": "Character image URL/base64 (jpg/jpeg/png, <=10MB, >=300px, aspect ratio 1:2.5-2.5:1)",
                    },
                ),
                "video": (
                    "STRING",
                    {
                        "default": "",
                        "tooltip": "Motion reference video URL (mp4/mov, <=10MB, >=300px, aspect ratio 1:2.5-2.5:1)",
                    },
                ),
                "character_orientation": (
                    _CHARACTER_ORIENTATIONS,
                    {"default": "image", "tooltip": "Match the character orientation to the image or to the video"},
                ),
            },
            "optional": {
                "prompt": ("STRING", {"multiline": True, "default": "", "tooltip": "Positive prompt for the generation"}),
                "keep_original_sound": (
                    "BOOLEAN",
                    {"default": True, "tooltip": "Whether to retain the original video sound"},
                ),
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
        character_orientation: str = "image",
        prompt: str = "",
        keep_original_sound: bool = True,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        image = (image or "").strip()
        if not image:
            raise RuntimeError("image is required (URL or base64)")

        video = (video or "").strip()
        if not video:
            raise RuntimeError("video is required (URL)")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "kwaivgi/kling-v3.0-pro/motion-control",
            "image": image,
            "video": video,
            "character_orientation": character_orientation,
            "keep_original_sound": bool(keep_original_sound),
        }

        p = (prompt or "").strip()
        if p:
            payload["prompt"] = p

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
