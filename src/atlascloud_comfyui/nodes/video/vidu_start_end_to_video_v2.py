from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasViduStartEndToVideoV2:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "start_image": ("STRING", {"default": "", "tooltip": "Start image URL/base64"}),
                "end_image": ("STRING", {"default": "", "tooltip": "End image URL/base64"}),
                "prompt": ("STRING", {"multiline": True, "tooltip": "Text prompt"}),
                "duration": ([4, 8], {"default": 4, "tooltip": "Duration (seconds)"}),
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
        start_image: str,
        end_image: str,
        prompt: str,
        duration: int,
        movement_amplitude: str,
        seed: int = 0,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        start_image = (start_image or "").strip()
        end_image = (end_image or "").strip()
        if not start_image:
            raise RuntimeError("start_image is required")
        if not end_image:
            raise RuntimeError("end_image is required")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "vidu/start-end-to-video-2.0",
            "images": [start_image, end_image],
            "prompt": prompt,
            "duration": int(duration),
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
