from __future__ import annotations

from typing import Any, Dict, List, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasNanoBanana2ReferenceToImageDev:
    CATEGORY = "AtlasCloud/Image"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("image_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "prompt": ("STRING", {"multiline": True, "tooltip": "Text prompt for generation"}),
                "video_url": ("STRING", {"default": "", "tooltip": "Source video clip URL (HTTP <=15MB or YouTube URL)"}),
            },
            "optional": {
                "seed": ("INT", {"default": -1, "min": -1, "max": 4294967295, "tooltip": "Random seed; -1 = random each run"}),
                "video_start": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 86400.0, "tooltip": "Trim start (seconds)"}),
                "video_ends": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 86400.0, "tooltip": "Trim end (seconds); 0 = whole video"}),
                "video_fps": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 24.0, "tooltip": "FPS of the video clip"}),
                "images": ("STRING", {"multiline": True, "default": "", "tooltip": "Optional 0-10 reference image URLs/base64, one per line"}),
                "aspect_ratio": (
                    ["1:1", "3:2", "2:3", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"],
                    {"default": "1:1", "tooltip": "Aspect ratio"},
                ),
                "resolution": (["1k", "2k", "4k"], {"default": "1k", "tooltip": "Resolution preset"}),
                "enable_web_search": ("BOOLEAN", {"default": False, "tooltip": "Ground generation with web search"}),
                "enable_base64_output": ("BOOLEAN", {"default": False, "tooltip": "Return base64 instead of URL if supported"}),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"}),
                "timeout_sec": ("INT", {"default": 300, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        prompt: str,
        video_url: str,
        video_start: float = 0.0,
        video_ends: float = 0.0,
        video_fps: float = 1.0,
        images: str = "",
        aspect_ratio: str = "1:1",
        resolution: str = "1k",
        enable_web_search: bool = False,
        enable_base64_output: bool = False,
        seed: int = -1,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 300,
    ) -> Tuple[str, str]:
        prompt = (prompt or "").strip()
        if not prompt:
            raise RuntimeError("prompt is required")

        video_url = (video_url or "").strip()
        if not video_url:
            raise RuntimeError("video_url is required")

        image_list: List[str] = [v.strip() for v in (images or "").splitlines() if v.strip()]
        if len(image_list) > 10:
            raise RuntimeError("images maxItems is 10")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "google/nano-banana-2/reference-to-image-developer",
            "prompt": prompt,
            "video_clips": [
                {
                    "url": video_url,
                    "start": float(video_start),
                    "ends": float(video_ends),
                    "fps": float(video_fps),
                }
            ],
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
            "enable_web_search": bool(enable_web_search),
            "enable_base64_output": bool(enable_base64_output),
        }

        if image_list:
            payload["images"] = image_list

        if seed >= 0:
            payload["seed"] = seed

        prediction_id = client.generate_image(payload)
        result = client.poll_prediction(
            prediction_id,
            poll_interval_sec=poll_interval_sec,
            timeout_sec=float(timeout_sec),
        )

        outputs = (result.get("data") or {}).get("outputs") or []
        if not outputs:
            raise RuntimeError(f"No outputs returned for prediction {prediction_id}: {result}")

        return (outputs[0], prediction_id)
