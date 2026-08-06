from __future__ import annotations

import json
from typing import Any, Dict, List, Tuple

from ..auth.atlas_client_node import AtlasClientHandle

_ASPECT_RATIOS = ["auto", "21:9", "2:1", "16:9", "4:3", "1:1", "3:4", "9:16"]
_RESOLUTIONS = ["720p", "1080p"]
_MAX_KEYFRAMES = 10
_FPS = 24

_KEYFRAMES_TOOLTIP = (
    'JSON array of keyframes, e.g. [{"image_url": "https://...", "frame_index": 0}]. '
    "Up to 10 entries with unique frame_index values; video is 24 fps so frame_index must be <= duration * 24"
)


class AtlasFlux3KeyframesToVideo:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "keyframes": ("STRING", {"multiline": True, "default": "", "tooltip": _KEYFRAMES_TOOLTIP}),
            },
            "optional": {
                "prompt": ("STRING", {"multiline": True, "default": "", "tooltip": "Text description of the video to generate"}),
                "aspect_ratio": (
                    _ASPECT_RATIOS,
                    {"default": "auto", "tooltip": "Aspect ratio of the generated video ('auto' lets the model choose)"},
                ),
                "resolution": (_RESOLUTIONS, {"default": "720p", "tooltip": "Output resolution"}),
                "duration": ("INT", {"default": 5, "min": 5, "max": 20, "tooltip": "Duration (seconds, 5-20)"}),
                "generate_audio": ("BOOLEAN", {"default": True, "tooltip": "Whether to generate audio for the video"}),
                "safety_tolerance": (
                    "INT",
                    {"default": 2, "min": 0, "max": 4, "tooltip": "Safety tolerance (0 strictest, 4 most permissive)"},
                ),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2**31 - 1, "tooltip": "Random seed (-1 for random)"}),
                "poll_interval_sec": (
                    "FLOAT",
                    {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"},
                ),
                "timeout_sec": ("INT", {"default": 900, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    @staticmethod
    def _parse_keyframes(keyframes: str, duration: int) -> List[Dict[str, Any]]:
        raw = (keyframes or "").strip()
        if not raw:
            raise RuntimeError("keyframes is required (JSON array of {image_url, frame_index})")

        try:
            parsed = json.loads(raw)
        except ValueError as exc:
            raise RuntimeError(f"keyframes must be valid JSON: {exc}") from exc

        if not isinstance(parsed, list) or not parsed:
            raise RuntimeError("keyframes must be a non-empty JSON array")
        if len(parsed) > _MAX_KEYFRAMES:
            raise RuntimeError(f"keyframes maxItems is {_MAX_KEYFRAMES}")

        max_frame_index = int(duration) * _FPS
        cleaned: List[Dict[str, Any]] = []
        seen_indices = set()
        for item in parsed:
            if not isinstance(item, dict):
                raise RuntimeError("each keyframe must be an object with image_url and frame_index")

            image_url = str(item.get("image_url") or "").strip()
            if not image_url:
                raise RuntimeError("each keyframe requires image_url")

            if "frame_index" not in item:
                raise RuntimeError("each keyframe requires frame_index")
            try:
                frame_index = int(item["frame_index"])
            except (TypeError, ValueError) as exc:
                raise RuntimeError("keyframe frame_index must be an integer") from exc

            if frame_index < 0 or frame_index > max_frame_index:
                raise RuntimeError(f"keyframe frame_index must be between 0 and duration * 24 ({max_frame_index})")
            if frame_index in seen_indices:
                raise RuntimeError(f"keyframe frame_index values must be unique (duplicate {frame_index})")
            seen_indices.add(frame_index)

            cleaned.append({"image_url": image_url, "frame_index": frame_index})

        return cleaned

    def run(
        self,
        atlas_client: AtlasClientHandle,
        keyframes: str,
        prompt: str = "",
        aspect_ratio: str = "auto",
        resolution: str = "720p",
        duration: int = 5,
        generate_audio: bool = True,
        safety_tolerance: int = 2,
        seed: int = -1,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        parsed_keyframes = self._parse_keyframes(keyframes, duration)

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "black-forest-labs/flux-3/keyframes-to-video",
            "keyframes": parsed_keyframes,
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
            "duration": int(duration),
            "generate_audio": bool(generate_audio),
            "safety_tolerance": int(safety_tolerance),
        }

        p = (prompt or "").strip()
        if p:
            payload["prompt"] = p
        if seed >= 0:
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
