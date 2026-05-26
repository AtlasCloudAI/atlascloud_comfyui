from __future__ import annotations

# NOTE: This node targets a model id that is no longer present in AtlasCloud /api/v1/models
# It is kept for backward compatibility with existing ComfyUI workflows.
DEPRECATED_MODEL_ID = True
DEPRECATION_REASON = "Model id not returned by AtlasCloud /api/v1/models; likely deprecated or removed upstream."

import os

from typing import Tuple

from ...auth.atlas_client_node import AtlasClientHandle


class AtlasWAN22T2V720p:
    CATEGORY = "AtlasCloud/Deprecated/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "prompt": ("STRING", {"multiline": True}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2**31 - 1, "tooltip": "Random if -1"}),
                "size": (["1280*720", "720*1280"], {"default": "1280*720", "tooltip": "Resolution"}),
            },
            "optional": {
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"}),
                "timeout_sec": ("INT", {"default": 900, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        prompt: str,
        seed: int,
        size: str,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        # Deprecated model guard
        if os.getenv("ATLAS_ALLOW_DEPRECATED_MODELS", "").lower() not in ("1", "true", "yes"):
            raise RuntimeError(
                "Deprecated model id: alibaba/wan-2.2/t2v-720p. This node is kept for backward compatibility, but the model is not returned by AtlasCloud /api/v1/models. "
                "Set ATLAS_ALLOW_DEPRECATED_MODELS=1 to force execution at your own risk."
            )

        client = atlas_client.client

        payload = {
            "model": "alibaba/wan-2.2/t2v-720p",
            "prompt": prompt,
            "seed": seed,
            "size": size,
        }

        prediction_id = client.generate_video(payload)
        result = client.poll_prediction(
            prediction_id,
            poll_interval_sec=poll_interval_sec,
            timeout_sec=float(timeout_sec),
        )

        outputs = (result.get("data") or {}).get("outputs") or []
        if not outputs:
            raise RuntimeError(f"No outputs returned for prediction {prediction_id}: {result}")

        video_url = outputs[0]
        return (video_url, prediction_id)
