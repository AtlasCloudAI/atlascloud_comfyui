from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasAvatarOmniHumanV15:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "image_url": ("STRING", {"default": "", "tooltip": "Reference portrait image URL (clear, front-facing face)"}),
                "audio_url": ("STRING", {"default": "", "tooltip": "Driving audio URL (MP3/WAV, max 60s)"}),
            },
            "optional": {
                "prompt": ("STRING", {"multiline": True, "default": "", "tooltip": "Optional action/scene/expression hint"}),
                "output_resolution": ([720, 1080], {"default": 1080, "tooltip": "Output resolution (720 or 1080)"}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2**31 - 1, "tooltip": "Random if -1"}),
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
        image_url: str,
        audio_url: str,
        prompt: str = "",
        output_resolution: int = 1080,
        seed: int = -1,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        image_url = (image_url or "").strip()
        if not image_url:
            raise RuntimeError("image_url is required for AtlasCloud Avatar Omni Human 1.5")

        audio_url = (audio_url or "").strip()
        if not audio_url:
            raise RuntimeError("audio_url is required for AtlasCloud Avatar Omni Human 1.5")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "bytedance/avatar-omni-human-v1.5",
            "image_url": image_url,
            "audio_url": audio_url,
            "output_resolution": int(output_resolution),
        }

        p = (prompt or "").strip()
        if p:
            payload["prompt"] = p

        if int(seed) >= 0:
            payload["seed"] = int(seed)

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
