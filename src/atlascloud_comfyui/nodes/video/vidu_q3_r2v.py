from __future__ import annotations

from typing import Any, Dict, List, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasViduQ3ReferenceToVideo:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "images": ("STRING", {"multiline": True, "tooltip": "1+ images, one per line"}),
                "prompt": ("STRING", {"multiline": True, "tooltip": "Text prompt"}),
            },
            "optional": {
                "movement_amplitude": (
                    ["auto", "small", "medium", "large"],
                    {"default": "auto", "tooltip": "Movement amplitude"},
                ),
                "duration": ("FLOAT", {"default": 5.0, "min": 1.0, "max": 60.0, "tooltip": "Duration (seconds)"}),
                "aspect_ratio": (
                    ["16:9", "9:16", "3:4", "4:3", "1:1"],
                    {"default": "16:9", "tooltip": "Aspect ratio"},
                ),
                "resolution": (["540p", "720p", "1080p"], {"default": "720p", "tooltip": "Resolution"}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 2**31 - 1, "tooltip": "Seed"}),
                "generate_audio": ("BOOLEAN", {"default": True, "tooltip": "Generate audio"}),
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
        images: str,
        prompt: str,
        movement_amplitude: str = "auto",
        duration: float = 5.0,
        aspect_ratio: str = "16:9",
        resolution: str = "720p",
        seed: int = 0,
        generate_audio: bool = True,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        prompt = (prompt or "").strip()
        if not prompt:
            raise RuntimeError("prompt is required for AtlasCloud Vidu Q3 Reference-to-Video")

        imgs: List[str] = [ln.strip() for ln in (images or "").splitlines() if ln.strip()]
        if not imgs:
            raise RuntimeError("images is required (provide 1+ lines)")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "vidu/q3/reference-to-video",
            "images": imgs,
            "prompt": prompt,
            "movement_amplitude": movement_amplitude,
            "duration": float(duration),
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
            "seed": int(seed),
            "generate_audio": bool(generate_audio),
        }

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
