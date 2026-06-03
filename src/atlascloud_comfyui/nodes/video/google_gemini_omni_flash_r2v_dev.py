from __future__ import annotations

from typing import Any, Dict, List, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasGeminiOmniFlashReferenceToVideoDev:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "prompt": ("STRING", {"multiline": True, "tooltip": "Text prompt (max 20,000 chars)"}),
                "images": ("STRING", {"multiline": True, "default": "", "tooltip": "1-5 reference image URLs/base64, one per line"}),
                "video_url": ("STRING", {"default": "", "tooltip": "Source video clip URL (<=100MB, <=30s)"}),
            },
            "optional": {
                "video_start": ("INT", {"default": 0, "min": 0, "max": 29, "tooltip": "Trim start (seconds)"}),
                "video_ends": ("INT", {"default": 10, "min": 1, "max": 30, "tooltip": "Trim end (seconds); ends-start must be <= 10"}),
                "duration": ([4, 6, 8, 10], {"default": 8, "tooltip": "Duration (seconds)"}),
                "aspect_ratio": (["16:9", "9:16"], {"default": "16:9", "tooltip": "Aspect ratio"}),
                "resolution": (["720p", "1080p", "4k"], {"default": "720p", "tooltip": "Resolution"}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2**31 - 1, "tooltip": "Random if -1"}),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"}),
                "timeout_sec": ("INT", {"default": 900, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        prompt: str,
        images: str,
        video_url: str,
        video_start: int = 0,
        video_ends: int = 10,
        duration: int = 8,
        aspect_ratio: str = "16:9",
        resolution: str = "720p",
        seed: int = -1,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        prompt = (prompt or "").strip()
        if not prompt:
            raise RuntimeError("prompt is required")

        image_list: List[str] = [v.strip() for v in (images or "").splitlines() if v.strip()]
        if not image_list:
            raise RuntimeError("images is required (1-5 lines)")
        if len(image_list) > 5:
            raise RuntimeError("images maxItems is 5")

        video_url = (video_url or "").strip()
        if not video_url:
            raise RuntimeError("video_url is required")
        if int(video_ends) - int(video_start) > 10:
            raise RuntimeError("video_ends - video_start must not exceed 10 seconds")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "google/gemini-omni-flash/reference-to-video-developer",
            "prompt": prompt,
            "images": image_list,
            "video_clips": [
                {"url": video_url, "start": int(video_start), "ends": int(video_ends)}
            ],
            "duration": int(duration),
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
        }

        if int(seed) >= 0:
            payload["seed"] = int(seed)

        prediction_id = client.generate_video(payload)
        result = client.poll_prediction(prediction_id, poll_interval_sec=float(poll_interval_sec), timeout_sec=float(timeout_sec))

        outputs = (result.get("data") or {}).get("outputs") or []
        if not outputs:
            raise RuntimeError(f"No outputs returned for prediction {prediction_id}: {result}")

        return (outputs[0], prediction_id)
