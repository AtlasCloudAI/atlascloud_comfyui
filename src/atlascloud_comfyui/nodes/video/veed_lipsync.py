from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasVeedLipsync:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "video": ("STRING", {"default": "", "tooltip": "Input talking-head video URL/base64 to re-lipsync (mp4/mov/webm)"}),
                "audio": ("STRING", {"default": "", "tooltip": "Driving audio URL/base64 (wav/mp3/m4a)"}),
            },
            "optional": {
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"}),
                "timeout_sec": ("INT", {"default": 900, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        video: str,
        audio: str,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        video = (video or "").strip()
        if not video:
            raise RuntimeError("video is required (URL or base64)")

        audio = (audio or "").strip()
        if not audio:
            raise RuntimeError("audio is required (URL or base64)")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "veed/lipsync",
            "video_url": video,
            "audio_url": audio,
        }

        prediction_id = client.generate_video(payload)
        result = client.poll_prediction(prediction_id, poll_interval_sec=poll_interval_sec, timeout_sec=float(timeout_sec))

        outputs = (result.get("data") or {}).get("outputs") or []
        if not outputs:
            raise RuntimeError(f"No outputs returned for prediction {prediction_id}: {result}")

        return (outputs[0], prediction_id)
