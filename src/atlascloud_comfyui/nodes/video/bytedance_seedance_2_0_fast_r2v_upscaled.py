from __future__ import annotations

from typing import Any, Dict, List, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasSeedance20FastReferenceToVideoUpscaled:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "reference_images": (
                    "STRING",
                    {"multiline": True, "default": "", "tooltip": "0+ image URLs/base64, one per line"},
                ),
                "reference_videos": (
                    "STRING",
                    {"multiline": True, "default": "", "tooltip": "0+ video URLs, one per line"},
                ),
            },
            "optional": {
                "prompt": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": "The scene comes alive with gentle motion and cinematic lighting",
                        "tooltip": "Prompt (optional)",
                    },
                ),
                "reference_audio": ("STRING", {"default": "", "tooltip": "Optional reference audio URL"}),
                "duration": (
                    [-1, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                    {"default": 5, "tooltip": "Duration (seconds), or -1 for auto"},
                ),
                "resolution": (['1080p', '2k'], {"default": "1080p", "tooltip": "Resolution"}),
                "ratio": (
                    ['16:9', '4:3', '1:1', '3:4', '9:16', '21:9', 'adaptive'],
                    {"default": "adaptive", "tooltip": "Aspect ratio (adaptive = auto)"},
                ),
                "generate_audio": ("BOOLEAN", {"default": True, "tooltip": "Generate audio"}),
                "watermark": ("BOOLEAN", {"default": False, "tooltip": "Add watermark"}),
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
        reference_images: str,
        reference_videos: str,
        prompt: str = "The scene comes alive with gentle motion and cinematic lighting",
        reference_audio: str = "",
        duration: int = 5,
        resolution: str = "1080p",
        ratio: str = "adaptive",
        generate_audio: bool = True,
        watermark: bool = False,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        ref_imgs: List[str] = [v.strip() for v in (reference_images or "").splitlines() if v.strip()]
        ref_vids: List[str] = [v.strip() for v in (reference_videos or "").splitlines() if v.strip()]
        if not ref_imgs and not ref_vids:
            raise RuntimeError("Provide at least one reference image or reference video")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "bytedance/seedance-2.0-fast/reference-to-video-upscaled",
            "duration": int(duration),
            "resolution": resolution,
            "ratio": ratio,
            "generate_audio": bool(generate_audio),
            "watermark": bool(watermark),
        }

        p = (prompt or "").strip()
        if p:
            payload["prompt"] = p

        ra = (reference_audio or "").strip()
        if ra:
            payload["reference_audio"] = ra

        if ref_imgs:
            payload["reference_images"] = ref_imgs
        if ref_vids:
            payload["reference_videos"] = ref_vids

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
