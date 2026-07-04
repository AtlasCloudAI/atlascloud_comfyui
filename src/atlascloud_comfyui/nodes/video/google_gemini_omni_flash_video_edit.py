from __future__ import annotations

from typing import Any, Dict, List, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasGeminiOmniFlashVideoEdit:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "video": ("STRING", {"default": "", "tooltip": "Source video URL (<=100MB, <=30s)"}),
                "prompt": ("STRING", {"multiline": True, "tooltip": "Edit prompt (max 20,000 chars)"}),
            },
            "optional": {
                "images": ("STRING", {"multiline": True, "default": "", "tooltip": "Optional 1-5 reference image URLs/base64, one per line"}),
                "resolution": (["720p"], {"default": "720p", "tooltip": "Resolution"}),
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
        images: str = "",
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

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "google/gemini-omni-flash/video-edit",
            "video": video,
            "prompt": prompt,
            "resolution": resolution,
            "thinking_level": thinking_level,
        }

        image_list: List[str] = [v.strip() for v in (images or "").splitlines() if v.strip()]
        if image_list:
            if len(image_list) > 5:
                raise RuntimeError("images maxItems is 5")
            payload["images"] = image_list

        if int(seed) >= 0:
            payload["seed"] = int(seed)

        prediction_id = client.generate_video(payload)
        result = client.poll_prediction(prediction_id, poll_interval_sec=float(poll_interval_sec), timeout_sec=float(timeout_sec))

        outputs = (result.get("data") or {}).get("outputs") or []
        if not outputs:
            raise RuntimeError(f"No outputs returned for prediction {prediction_id}: {result}")

        return (outputs[0], prediction_id)
