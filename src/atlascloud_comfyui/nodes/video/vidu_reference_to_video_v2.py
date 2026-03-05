from __future__ import annotations

from typing import Any, Dict, List, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasViduReferenceToVideoV2:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "images": ("STRING", {"multiline": True, "tooltip": "1-3 image URLs/base64, one per line"}),
                "prompt": ("STRING", {"multiline": True, "tooltip": "Text prompt"}),
                "aspect_ratio": (["16:9", "9:16", "1:1"], {"default": "16:9", "tooltip": "Aspect ratio"}),
                "movement_amplitude": (
                    ["auto", "small", "medium", "large"],
                    {"default": "auto", "tooltip": "Movement amplitude"},
                ),
            },
            "optional": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 2**31 - 1, "tooltip": "Seed"}),
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
        images: str,
        prompt: str,
        aspect_ratio: str,
        movement_amplitude: str,
        seed: int = 0,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        imgs: List[str] = [ln.strip() for ln in (images or "").splitlines() if ln.strip()]
        if not imgs:
            raise RuntimeError("images is required (provide 1-3 lines)")
        if len(imgs) > 3:
            raise RuntimeError("Vidu Reference-to-Video supports up to 3 images")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "vidu/reference-to-video-2.0",
            "images": imgs,
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "movement_amplitude": movement_amplitude,
            "seed": int(seed),
        }

        prediction_id = client.generate_video(payload)
        result = client.poll_prediction(prediction_id, poll_interval_sec=float(poll_interval_sec), timeout_sec=float(timeout_sec))

        outputs = (result.get("data") or {}).get("outputs") or []
        if not outputs:
            raise RuntimeError(f"No outputs returned for prediction {prediction_id}: {result}")

        first = outputs[0]
        if not isinstance(first, str):
            raise RuntimeError(f"Unexpected output type for prediction {prediction_id}: {type(first).__name__} {first!r}")

        return (first, prediction_id)
