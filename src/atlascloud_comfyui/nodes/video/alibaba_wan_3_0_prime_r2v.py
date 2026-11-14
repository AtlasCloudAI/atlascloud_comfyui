from __future__ import annotations

from typing import Any, Dict, List, Tuple

from ..auth.atlas_client_node import AtlasClientHandle

_RESOLUTIONS = ["1080P", "720P", "480P"]
_RATIOS = ["adaptive", "16:9", "4:3", "1:1", "3:4", "9:16"]

# Per-kind caps from the model's x-media-limits.
_MAX_IMAGES = 10
_MAX_VIDEOS = 5
_MAX_AUDIOS = 5
_MAX_REFERS = 20


class AtlasWan30PrimeReferenceToVideo:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING", "DICT")
    RETURN_NAMES = ("video_url", "prediction_id", "payload")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "prompt": ("STRING", {"multiline": True, "tooltip": "Scene and action for the referenced subjects"}),
                "reference_images": (
                    "STRING",
                    {"multiline": True, "default": "", "tooltip": "0-10 reference image URLs, ONE PER LINE"},
                ),
            },
            "optional": {
                "reference_videos": (
                    "STRING",
                    {"multiline": True, "default": "", "tooltip": "0-5 reference video URLs (<=15s total), ONE PER LINE"},
                ),
                "reference_audios": (
                    "STRING",
                    {"multiline": True, "default": "", "tooltip": "0-5 reference audio URLs (<=15s total), ONE PER LINE"},
                ),
                "resolution": (_RESOLUTIONS, {"default": "1080P", "tooltip": "Resolution"}),
                "duration": (
                    "INT",
                    {"default": 5, "min": -1, "max": 30, "tooltip": "Video length in seconds (2-30); -1 for smart-duration"},
                ),
                "ratio": (_RATIOS, {"default": "adaptive", "tooltip": "Aspect ratio; 'adaptive' derives it from the references"}),
                "audio": ("BOOLEAN", {"default": True, "tooltip": "Include an audio track (same price either way)"}),
                "enable_thinking": ("BOOLEAN", {"default": True, "tooltip": "Let the model reason over the references first"}),
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
        prompt: str,
        reference_images: str,
        reference_videos: str = "",
        reference_audios: str = "",
        resolution: str = "1080P",
        duration: int = 5,
        ratio: str = "adaptive",
        audio: bool = True,
        enable_thinking: bool = True,
        seed: int = -1,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        prompt = (prompt or "").strip()
        if not prompt:
            raise RuntimeError("prompt is required for AtlasCloud WAN3.0-Prime Reference-to-Video")

        # Split on newlines, NOT commas: base64 data URLs contain a comma.
        images: List[str] = [u.strip() for u in (reference_images or "").splitlines() if u.strip()]
        videos: List[str] = [u.strip() for u in (reference_videos or "").splitlines() if u.strip()]
        audios: List[str] = [u.strip() for u in (reference_audios or "").splitlines() if u.strip()]

        if not images and not videos and not audios:
            raise RuntimeError("Provide at least one reference image, video or audio")
        if len(images) > _MAX_IMAGES:
            raise RuntimeError(f"reference_images maxItems is {_MAX_IMAGES}")
        if len(videos) > _MAX_VIDEOS:
            raise RuntimeError(f"reference_videos maxItems is {_MAX_VIDEOS}")
        if len(audios) > _MAX_AUDIOS:
            raise RuntimeError(f"reference_audios maxItems is {_MAX_AUDIOS}")

        refers: List[Dict[str, str]] = []
        refers.extend({"url": u, "type": "image"} for u in images)
        refers.extend({"url": u, "type": "video"} for u in videos)
        refers.extend({"url": u, "type": "audio"} for u in audios)
        if len(refers) > _MAX_REFERS:
            raise RuntimeError(f"refers maxItems is {_MAX_REFERS}")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "alibaba/wan-3.0-prime/reference-to-video",
            "prompt": prompt,
            "refers": refers,
            "resolution": resolution,
            "duration": int(duration),
            "ratio": ratio,
            "audio": bool(audio),
            "enable_thinking": bool(enable_thinking),
        }

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

        return (first, prediction_id, payload)
