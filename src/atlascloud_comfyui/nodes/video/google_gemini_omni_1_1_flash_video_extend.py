from __future__ import annotations

from typing import Any, Dict, List, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasGeminiOmni11FlashVideoExtend:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "video": ("STRING", {"default": "", "tooltip": "Source video URL to extend (MP4, <=10s)"}),
                "prompt": ("STRING", {"multiline": True, "tooltip": "How the video should continue (max 20,000 chars); reference an upload with <IMAGE_REF_N> (0-based)"}),
            },
            "optional": {
                "reference_images": ("STRING", {"multiline": True, "default": "", "tooltip": "Optional 1-10 reference image URLs/base64, one per line"}),
                "duration": ("INT", {"default": 10, "min": 3, "max": 10, "tooltip": "Continuation length (seconds); total video must stay <=40s"}),
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
        video: str,
        prompt: str,
        reference_images: str = "",
        duration: int = 10,
        resolution: str = "720p",
        thinking_level: str = "default",
        seed: int = -1,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        prompt = (prompt or "").strip()
        if not prompt:
            raise RuntimeError("prompt is required")

        video = (video or "").strip()
        if not video:
            raise RuntimeError("video is required")

        image_list: List[str] = [v.strip() for v in (reference_images or "").splitlines() if v.strip()]
        if len(image_list) > 10:
            raise RuntimeError("reference_images maxItems is 10")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "google/gemini-omni-1.1-flash/video-extend",
            "video": video,
            "prompt": prompt,
            "duration": int(duration),
            "resolution": resolution,
            "thinking_level": thinking_level,
        }

        if image_list:
            payload["reference_images"] = image_list

        if int(seed) >= 0:
            payload["seed"] = int(seed)

        prediction_id = client.generate_video(payload)
        result = client.poll_prediction(prediction_id, poll_interval_sec=float(poll_interval_sec), timeout_sec=float(timeout_sec))

        outputs = (result.get("data") or {}).get("outputs") or []
        if not outputs:
            raise RuntimeError(f"No outputs returned for prediction {prediction_id}: {result}")

        return (outputs[0], prediction_id)
