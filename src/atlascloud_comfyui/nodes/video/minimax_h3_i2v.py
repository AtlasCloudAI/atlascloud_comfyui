from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasMinimaxH3ImageToVideo:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "image": ("STRING", {"default": "", "tooltip": "First frame image URL or base64"}),
                "prompt": ("STRING", {"multiline": True, "tooltip": "Text prompt describing the motion / action"}),
            },
            "optional": {
                "end_image": ("STRING", {"default": "", "tooltip": "Optional last frame image URL or base64"}),
                "resolution": (["2K"], {"default": "2K", "tooltip": "Output resolution"}),
                "duration": ("INT", {"default": 8, "min": 5, "max": 15, "tooltip": "Duration (seconds)"}),
                "ratio": (
                    ["adaptive", "21:9", "16:9", "4:3", "1:1", "3:4", "9:16"],
                    {"default": "adaptive", "tooltip": "Aspect ratio (adaptive = let the model choose)"},
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
        prompt: str,
        end_image: str = "",
        resolution: str = "2K",
        duration: int = 8,
        ratio: str = "adaptive",
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        img = (image or "").strip()
        if not img:
            raise RuntimeError("image is required for MiniMax H3 Image-to-Video")

        p = (prompt or "").strip()
        if not p:
            raise RuntimeError("prompt is required")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "minimax/h3/image-to-video",
            "image": img,
            "prompt": p,
            "resolution": resolution,
            "duration": int(duration),
            "ratio": ratio,
        }

        if (end_image or "").strip():
            payload["end_image"] = end_image.strip()

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
