from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasMidjourneyV81ImageToVideo:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "image": ("STRING", {"default": "", "tooltip": "First-frame image to animate (public https URL or base64)"}),
            },
            "optional": {
                "prompt": ("STRING", {"multiline": True, "default": "gentle camera push in, cinematic", "tooltip": "Optional motion / scene description"}),
                "resolution": (["480p", "720p"], {"default": "480p", "tooltip": "Output resolution. 720p costs 3x of 480p"}),
                "motion": (["low", "high"], {"default": "low", "tooltip": "Amount of motion in the generated video"}),
                "enable_base64_output": ("BOOLEAN", {"default": False, "tooltip": "Return base64 instead of URL if supported"}),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"}),
                "timeout_sec": ("INT", {"default": 900, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        image: str,
        prompt: str = "gentle camera push in, cinematic",
        resolution: str = "480p",
        motion: str = "low",
        enable_base64_output: bool = False,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        image = (image or "").strip()
        if not image:
            raise RuntimeError("image is required for AtlasCloud Midjourney V8.1 Image-to-Video (URL or base64)")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "midjourney/v8.1/image-to-video",
            "image": image,
            "resolution": resolution,
            "motion": motion,
            "enable_base64_output": bool(enable_base64_output),
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
