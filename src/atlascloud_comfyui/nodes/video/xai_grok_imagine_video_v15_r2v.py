from __future__ import annotations

from typing import Any, Dict, List, Tuple

from ..auth.atlas_client_node import AtlasClientHandle

VOICE_IDS = [
    "altair",
    "ara",
    "atlas",
    "carina",
    "castor",
    "celeste",
    "cosmo",
    "eve",
    "helios",
    "helix",
    "iris",
    "kepler",
    "leo",
    "lumen",
    "luna",
    "lux",
    "naksh",
    "orion",
    "perseus",
    "rex",
    "rigel",
    "sal",
    "sirius",
    "ursa",
    "zagan",
    "zenith",
]


class AtlasGrokImagineVideoV15ReferenceToVideo:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "prompt": ("STRING", {"multiline": True, "tooltip": "Video prompt; use <IMAGE_N> tags to reference inputs"}),
                "image_urls": (
                    "STRING",
                    {"multiline": True, "default": "", "tooltip": "1-7 reference images, one per line (URL or base64)"},
                ),
            },
            "optional": {
                "voice_ids": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": "",
                        "tooltip": f"Optional xAI preset voices, one per line (max 3). Allowed: {', '.join(VOICE_IDS)}",
                    },
                ),
                "duration": ("INT", {"default": 8, "min": 1, "max": 15, "tooltip": "Duration (seconds, 1-15)"}),
                "resolution": (["480p", "720p"], {"default": "720p", "tooltip": "Output resolution (capped at 720p)"}),
                "aspect_ratio": (
                    ["1:1", "16:9", "9:16", "4:3", "3:4", "3:2", "2:3"],
                    {"default": "16:9", "tooltip": "Output aspect ratio"},
                ),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"}),
                "timeout_sec": ("INT", {"default": 900, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        prompt: str,
        image_urls: str,
        voice_ids: str = "",
        duration: int = 8,
        resolution: str = "720p",
        aspect_ratio: str = "16:9",
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        prompt = (prompt or "").strip()
        if not prompt:
            raise RuntimeError("prompt is required")

        urls: List[str] = [v.strip() for v in (image_urls or "").splitlines() if v.strip()]
        if not urls:
            raise RuntimeError("image_urls is required (1-7 lines)")
        if len(urls) > 7:
            raise RuntimeError("image_urls maxItems is 7")

        voices: List[str] = [v.strip() for v in (voice_ids or "").splitlines() if v.strip()]
        if len(voices) > 3:
            raise RuntimeError("voice_ids maxItems is 3")
        unknown = [v for v in voices if v not in VOICE_IDS]
        if unknown:
            raise RuntimeError(f"Unknown voice_ids {unknown}; allowed: {', '.join(VOICE_IDS)}")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "xai/grok-imagine-video-v1.5/reference-to-video",
            "prompt": prompt,
            "image_urls": urls,
            "duration": int(duration),
            "resolution": resolution,
            "aspect_ratio": aspect_ratio,
        }
        if voices:
            payload["voice_ids"] = voices

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
