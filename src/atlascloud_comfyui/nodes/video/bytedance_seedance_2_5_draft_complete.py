from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasSeedance25DraftComplete:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "draft_id": (
                    "STRING",
                    {"default": "", "tooltip": "prediction_id of a Seedance 2.5 run made with draft enabled (valid for 7 days)"},
                ),
            },
            "optional": {
                "watermark": ("BOOLEAN", {"default": False, "tooltip": "Add watermark"}),
                "return_last_frame": ("BOOLEAN", {"default": False, "tooltip": "Return last frame (if supported)"}),
                "output_format": (["mp4", "mov"], {"default": "mp4", "tooltip": "Output container format"}),
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
        draft_id: str,
        watermark: bool = False,
        return_last_frame: bool = False,
        output_format: str = "mp4",
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        draft_id = (draft_id or "").strip()
        if not draft_id:
            raise RuntimeError("draft_id is required for AtlasCloud Seedance 2.5 Draft Complete")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "bytedance/seedance-2.5/draft-complete",
            "draft_id": draft_id,
            "watermark": bool(watermark),
            "return_last_frame": bool(return_last_frame),
            "output_format": output_format,
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
