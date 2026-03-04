from __future__ import annotations

from typing import Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasKlingV26ProAvatar:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "audio": ("STRING", {"default": "", "tooltip": "Audio URL/base64"}),
                "image": ("STRING", {"default": "", "tooltip": "Reference image URL/base64"}),
                "prompt": ("STRING", {"multiline": True, "default": "", "tooltip": "Optional prompt"}),
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
        audio: str,
        image: str,
        prompt: str = "",
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        if not (audio or "").strip():
            raise RuntimeError("audio is required for Kling V2.6 Pro Avatar")
        if not (image or "").strip():
            raise RuntimeError("image is required for Kling V2.6 Pro Avatar")

        client = atlas_client.client

        payload = {
            "model": "kwaivgi/kling-v2.6-pro/avatar",
            "audio": (audio or "").strip(),
            "image": (image or "").strip(),
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
