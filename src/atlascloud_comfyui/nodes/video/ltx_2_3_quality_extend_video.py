from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle

_RESOLUTIONS = [
    "square_hd",
    "square",
    "portrait_3_4",
    "portrait_9_16",
    "landscape_4_3",
    "landscape_16_9",
]

_DEFAULT_PROMPT = "Continue the scene naturally, maintaining the same style, lighting, and motion dynamics"


class AtlasLtx23QualityExtendVideo:
    """
    ComfyUI Node: AtlasCloud LTX 2.3 Quality Extend Video (remote API)
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
                "video_url": ("STRING", {"default": "", "tooltip": "Input video URL or data:video/...;base64,..."}),
                "prompt": ("STRING", {"multiline": True, "default": _DEFAULT_PROMPT, "tooltip": "Extended scene description (max 2000 chars)"}),
            },
            "optional": {
                "extend_direction": (
                    ["forward", "backward"],
                    {"default": "forward", "tooltip": "Forward (append after) or Backward (prepend before)"},
                ),
                "num_frames": (
                    "INT",
                    {"default": 81, "min": 9, "max": 481, "tooltip": "Extension frames; multiple of 8 plus 1"},
                ),
                "resolution": (_RESOLUTIONS, {"default": "landscape_16_9", "tooltip": "Output resolution preset"}),
                "match_input_fps": ("BOOLEAN", {"default": True, "tooltip": "Match the input video FPS"}),
                "generate_audio": ("BOOLEAN", {"default": False, "tooltip": "Generate accompanying audio"}),
                "randomize_seed": ("BOOLEAN", {"default": True, "tooltip": "开启后每次随机；关闭后使用下方固定 seed"}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 2**31 - 1, "tooltip": "固定 seed（仅在随机开关关闭时生效）"}),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"}),
                "timeout_sec": ("INT", {"default": 900, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        video_url: str,
        prompt: str,
        extend_direction: str = "forward",
        num_frames: int = 81,
        resolution: str = "landscape_16_9",
        match_input_fps: bool = True,
        generate_audio: bool = False,
        randomize_seed: bool = True,
        seed: int = 0,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        video_url = (video_url or "").strip()
        if not video_url:
            raise RuntimeError("video_url is required for LTX 2.3 Quality Extend Video")

        p = (prompt or "").strip()
        if not p:
            raise RuntimeError("prompt is required for LTX 2.3 Quality Extend Video")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "ltx-2.3-quality/extend-video",
            "prompt": p,
            "video_url": video_url,
            "extend_direction": extend_direction,
            "num_frames": int(num_frames),
            "resolution": resolution,
            "match_input_fps": bool(match_input_fps),
            "generate_audio": bool(generate_audio),
        }
        if not randomize_seed:
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
        if isinstance(first, dict):
            url = first.get("url") or first.get("video") or first.get("output")
            if isinstance(url, str) and url.strip():
                return (url, prediction_id)
            raise RuntimeError(f"Unexpected output object for prediction {prediction_id}: {first}")

        if not isinstance(first, str):
            raise RuntimeError(f"Unexpected output type for prediction {prediction_id}: {type(first).__name__} {first!r}")

        return (first, prediction_id)
