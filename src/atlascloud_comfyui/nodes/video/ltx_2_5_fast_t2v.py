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


class AtlasLtx25FastTextToVideo:
    """
    ComfyUI Node: AtlasCloud LTX 2.5 Fast Text-to-Video (remote API)
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
                "prompt": ("STRING", {"multiline": True, "tooltip": "Scene description: content, camera movement and atmosphere"}),
            },
            "optional": {
                "duration": ([-1, 6, 8, 10, 12, 14, 16, 18, 20], {"default": -1, "tooltip": "Video length in seconds (-1 lets the model choose)"}),
                "resolution": (_RESOLUTIONS, {"default": "720p", "tooltip": "Output resolution tier; combined with aspect_ratio to pick the frame size"}),
                "aspect_ratio": (_ASPECT_RATIOS, {"default": "16:9", "tooltip": "Frame orientation"}),
                "fps": ([24, 25, 48, 50], {"default": 24, "tooltip": "Output frame rate"}),
                "generate_audio": ("BOOLEAN", {"default": True, "tooltip": "Generate a synchronized audio track"}),
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
        prompt: str,
        duration: int = -1,
        resolution: str = "720p",
        aspect_ratio: str = "16:9",
        fps: int = 24,
        generate_audio: bool = True,
        camera_motion: str = "auto",
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        prompt = (prompt or "").strip()
        if not prompt:
            raise RuntimeError("prompt is required for LTX 2.5 Fast Text-to-Video")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "ltx/ltx-2.5-fast/text-to-video",
            "prompt": prompt,
            "duration": int(duration),
            "resolution": resolution,
            "aspect_ratio": aspect_ratio,
            "fps": int(fps),
            "generate_audio": bool(generate_audio),
        }

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
