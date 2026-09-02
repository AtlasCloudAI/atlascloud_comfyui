from __future__ import annotations

from typing import Any, Dict, List, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasGeminiOmni11FlashReferenceToVideo:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "prompt": ("STRING", {"multiline": True, "tooltip": "Text prompt (max 20,000 chars); reference an upload with <IMAGE_REF_N> / <VIDEO_REF_N> (0-based)"}),
                "reference_images": ("STRING", {"multiline": True, "default": "", "tooltip": "1-10 reference image URLs/base64, one per line"}),
            },
            "optional": {
                "reference_videos": ("STRING", {"multiline": True, "default": "", "tooltip": "Optional 1-3 reference video URLs (MP4, <=3s each), one per line"}),
                "duration": ("INT", {"default": 10, "min": 3, "max": 10, "tooltip": "Duration (seconds)"}),
                "aspect_ratio": (["16:9", "9:16"], {"default": "16:9", "tooltip": "Aspect ratio"}),
                "resolution": (["360p", "720p", "1080p", "4k"], {"default": "720p", "tooltip": "Resolution (360p is a fast draft mode)"}),
                "thinking_level": (["default", "high", "low"], {"default": "default", "tooltip": "Internal reasoning level"}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2**31 - 1, "tooltip": "Random if -1"}),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"}),
                "timeout_sec": ("INT", {"default": 900, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        prompt: str,
        reference_images: str,
        reference_videos: str = "",
        duration: int = 10,
        aspect_ratio: str = "16:9",
        resolution: str = "720p",
        thinking_level: str = "default",
        seed: int = -1,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        prompt = (prompt or "").strip()
        if not prompt:
            raise RuntimeError("prompt is required")

        image_list: List[str] = [v.strip() for v in (reference_images or "").splitlines() if v.strip()]
        if not image_list:
            raise RuntimeError("reference_images is required (1-10 lines)")
        if len(image_list) > 10:
            raise RuntimeError("reference_images maxItems is 10")

        video_list: List[str] = [v.strip() for v in (reference_videos or "").splitlines() if v.strip()]
        if len(video_list) > 3:
            raise RuntimeError("reference_videos maxItems is 3")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "google/gemini-omni-1.1-flash/reference-to-video",
            "prompt": prompt,
            "reference_images": image_list,
            "duration": int(duration),
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
            "thinking_level": thinking_level,
        }

        if video_list:
            payload["reference_videos"] = video_list

        if int(seed) >= 0:
            payload["seed"] = int(seed)

        prediction_id = client.generate_video(payload)
        result = client.poll_prediction(prediction_id, poll_interval_sec=float(poll_interval_sec), timeout_sec=float(timeout_sec))

        outputs = (result.get("data") or {}).get("outputs") or []
        if not outputs:
            raise RuntimeError(f"No outputs returned for prediction {prediction_id}: {result}")

        return (outputs[0], prediction_id)
