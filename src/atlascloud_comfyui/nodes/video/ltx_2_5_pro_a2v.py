from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle

_RESOLUTIONS = ["720p", "1080p", "1440p", "4k"]
_ASPECT_RATIOS = ["16:9", "9:16"]
_CAMERA_MOTIONS = [
    "auto",
    "dolly_in",
    "dolly_out",
    "dolly_left",
    "dolly_right",
    "jib_up",
    "jib_down",
    "static",
    "focus_shift",
]


class AtlasLtx25ProAudioToVideo:
    """
    ComfyUI Node: AtlasCloud LTX 2.5 Pro Audio-to-Video (remote API)
    Outputs: video_url, prediction_id
    """

    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "audio": ("STRING", {"default": "", "tooltip": "Driving audio track (MP3/M4A/OGG); plain PCM WAV is rejected"}),
            },
            "optional": {
                "image": ("STRING", {"default": "", "tooltip": "Optional first-frame image; required when prompt is empty"}),
                "last_image": ("STRING", {"default": "", "tooltip": "Optional last-frame image; requires image"}),
                "prompt": ("STRING", {"multiline": True, "default": "", "tooltip": "Text prompt; required when image is empty"}),
                "resolution": (_RESOLUTIONS, {"default": "1080p", "tooltip": "Output resolution tier; combined with aspect_ratio to pick the frame size"}),
                "aspect_ratio": (_ASPECT_RATIOS, {"default": "16:9", "tooltip": "Frame orientation"}),
                "fps": ([24, 25, 48, 50], {"default": 24, "tooltip": "Output frame rate"}),
                "camera_motion": (_CAMERA_MOTIONS, {"default": "auto", "tooltip": "Camera move preset; auto leaves it to the model"}),
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
        audio: str,
        image: str = "",
        last_image: str = "",
        prompt: str = "",
        resolution: str = "1080p",
        aspect_ratio: str = "16:9",
        fps: int = 24,
        camera_motion: str = "auto",
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        audio = (audio or "").strip()
        if not audio:
            raise RuntimeError("audio is required for LTX 2.5 Pro Audio-to-Video")

        image = (image or "").strip()
        last_image = (last_image or "").strip()
        prompt = (prompt or "").strip()
        if not image and not prompt:
            raise RuntimeError("prompt is required for LTX 2.5 Pro Audio-to-Video when image is empty")
        if last_image and not image:
            raise RuntimeError("last_image requires image for LTX 2.5 Pro Audio-to-Video")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "ltx/ltx-2.5-pro/audio-to-video",
            "audio": audio,
            "resolution": resolution,
            "aspect_ratio": aspect_ratio,
            "fps": int(fps),
        }

        if image:
            payload["image"] = image
        if last_image:
            payload["last_image"] = last_image
        if prompt:
            payload["prompt"] = prompt

        if camera_motion != "auto":
            payload["camera_motion"] = camera_motion

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
        if isinstance(first, dict):
            url = first.get("url") or first.get("video") or first.get("output")
            if isinstance(url, str) and url.strip():
                return (url, prediction_id)
            raise RuntimeError(f"Unexpected output object for prediction {prediction_id}: {first}")

        if not isinstance(first, str):
            raise RuntimeError(f"Unexpected output type for prediction {prediction_id}: {type(first).__name__} {first!r}")

        return (first, prediction_id)
