from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasFaceSwapVideo:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "source_face": ("STRING", {"default": "", "tooltip": "Source Face — clear front-facing photo of the face to place into the video"}),
                "video": ("STRING", {"default": "", "tooltip": "Target Video — the video whose person will be replaced (MP4/MOV, 2-10s, <=100MB)"}),
            },
            "optional": {
                "resolution": (["720P", "1080P"], {"default": "1080P", "tooltip": "Output video resolution"}),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"}),
                "timeout_sec": ("INT", {"default": 900, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        source_face: str,
        video: str,
        resolution: str = "1080P",
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        face = (source_face or "").strip()
        if not face:
            raise RuntimeError("source_face is required for AtlasCloud Face Swap (Video)")

        vid = (video or "").strip()
        if not vid:
            raise RuntimeError("video is required for AtlasCloud Face Swap (Video)")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "atlascloud/face-swap-video",
            "image": face,
            "video": vid,
            "resolution": resolution,
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

        return (outputs[0], prediction_id)
