from __future__ import annotations

# NOTE: This node targets a model id that is no longer present in AtlasCloud /api/v1/models
# It is kept for backward compatibility with existing ComfyUI workflows.
DEPRECATED_MODEL_ID = True
DEPRECATION_REASON = "Model id not returned by AtlasCloud /api/v1/models; likely deprecated or removed upstream."

import os

from typing import Any, Dict, List, Tuple

from ...auth.atlas_client_node import AtlasClientHandle


class AtlasViduQ2ProFastReferenceToVideoWithAudio:
    CATEGORY = "AtlasCloud/Deprecated/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "images": ("STRING", {"multiline": True, "tooltip": "1-7 image URLs/base64, one per line"}),
                "prompt": ("STRING", {"multiline": True, "tooltip": "Text prompt"}),
                "duration": ("FLOAT", {"default": 5.0, "min": 1.0, "max": 60.0, "tooltip": "Duration (seconds)"}),
                "aspect_ratio": (["16:9", "9:16", "1:1"], {"default": "16:9", "tooltip": "Aspect ratio"}),
                "resolution": (["720p", "1080p"], {"default": "720p", "tooltip": "Resolution"}),
            },
            "optional": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 2**31 - 1, "tooltip": "Seed"}),
                "generate_audio": ("BOOLEAN", {"default": True, "tooltip": "Whether to generate audio"}),
                "audio_type": ("STRING", {"default": "", "tooltip": "Audio type (optional)"}),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"}),
                "timeout_sec": ("INT", {"default": 900, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        images: str,
        prompt: str,
        duration: float,
        aspect_ratio: str,
        resolution: str,
        seed: int = 0,
        generate_audio: bool = True,
        audio_type: str = "",
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        # Deprecated model guard
        if os.getenv("ATLAS_ALLOW_DEPRECATED_MODELS", "").lower() not in ("1", "true", "yes"):
            raise RuntimeError(
                "Deprecated model id: vidu/q2-pro-fast/reference-to-video-with-audio. This node is kept for backward compatibility, but the model is not returned by AtlasCloud /api/v1/models. "
                "Set ATLAS_ALLOW_DEPRECATED_MODELS=1 to force execution at your own risk."
            )

        imgs: List[str] = [ln.strip() for ln in (images or "").splitlines() if ln.strip()]
        if not imgs:
            raise RuntimeError("images is required (provide 1-7 lines)")
        if len(imgs) > 7:
            raise RuntimeError("images maxItems is 7")

        p = (prompt or "").strip()
        if not p:
            raise RuntimeError("prompt is required")

        # API schema uses `subjects` (array of objects) rather than `images`.
        subjects: List[Dict[str, Any]] = [{"id": "subject1", "images": imgs}]

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "vidu/q2-pro-fast/reference-to-video-with-audio",
            "subjects": subjects,
            "prompt": p,
            "generate_audio": bool(generate_audio),
            "audio_type": (audio_type or "").strip(),
            "duration": float(duration),
            "seed": int(seed),
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
        }

        if not (payload.get("audio_type") or "").strip():
            payload.pop("audio_type", None)

        prediction_id = client.generate_video(payload)
        result = client.poll_prediction(prediction_id, poll_interval_sec=float(poll_interval_sec), timeout_sec=float(timeout_sec))

        outputs = (result.get("data") or {}).get("outputs") or []
        if not outputs:
            raise RuntimeError(f"No outputs returned for prediction {prediction_id}: {result}")

        first = outputs[0]
        if not isinstance(first, str):
            raise RuntimeError(f"Unexpected output type for prediction {prediction_id}: {type(first).__name__} {first!r}")

        return (first, prediction_id)
