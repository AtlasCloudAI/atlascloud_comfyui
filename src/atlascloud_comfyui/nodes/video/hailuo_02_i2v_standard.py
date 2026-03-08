from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasHailuo02I2VStandard:
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
                        "tooltip": "First frame image URL/base64",
                    },
                ),
                "prompt": (
                    "STRING",
                    {
                        "multiline": True,
                        "tooltip": "Generate a description of the video.",
                    },
                ),
            },
            "optional": {
                "duration": ([6, 10], {"default": 6, "tooltip": "Duration (seconds)"}),
                "enable_prompt_expansion": (
                    "BOOLEAN",
                    {
                        "default": False,
                        "tooltip": "Enable prompt optimizer",
                    },
                ),
                "poll_interval_sec": (
                    "FLOAT",
                    {
                        "default": 2.0,
                        "min": 0.5,
                        "max": 10.0,
                        "tooltip": "Polling interval (seconds)",
                    },
                ),
                "timeout_sec": (
                    "INT",
                    {
                        "default": 900,
                        "min": 30,
                        "max": 7200,
                        "tooltip": "Timeout (seconds)",
                    },
                ),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        image: str,
        prompt: str,
        duration: int = 6,
        enable_prompt_expansion: bool = False,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        client = atlas_client.client

        img = (image or "").strip()
        if not img:
            raise RuntimeError("image is required (URL or base64)")

        p = (prompt or "").strip()
        if not p:
            raise RuntimeError("prompt is required")

        payload: Dict[str, Any] = {
            "model": "minimax/hailuo-02/standard",
            "image": img,
            "prompt": p,
            "duration": int(duration),
            "enable_prompt_expansion": bool(enable_prompt_expansion),
        }

        prediction_id = client.generate_video(payload)
        result = client.poll_prediction(prediction_id, poll_interval_sec=poll_interval_sec, timeout_sec=float(timeout_sec))

        outputs = (result.get("data") or {}).get("outputs") or []
        if not outputs:
            raise RuntimeError(f"No outputs returned for prediction {prediction_id}: {result}")

        first = outputs[0]
        if not isinstance(first, str):
            raise RuntimeError(f"Unexpected output type for prediction {prediction_id}: {type(first).__name__} {first!r}")

        return (first, prediction_id)
