from __future__ import annotations

from typing import Any, Dict, List, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasKlingVideoO3ProVideoEdit:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "prompt": ("STRING", {"multiline": True}),
                "video": ("STRING", {"default": "", "tooltip": "Video URL (<=10s)"}),
            },
            "optional": {
                "images": ("STRING", {"multiline": True, "default": "", "tooltip": "0-4 image URLs, one per line"}),
                "keep_original_sound": ("BOOLEAN", {"default": True}),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0}),
                "timeout_sec": ("INT", {"default": 900, "min": 30, "max": 7200}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        prompt: str,
        video: str,
        images: str = "",
        keep_original_sound: bool = True,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        if not (video or "").strip():
            raise RuntimeError("video is required for Kling Video O3 Pro Video-Edit")

        client = atlas_client.client

        image_list: List[str] = [v.strip() for v in (images or "").splitlines() if v.strip()]
        if len(image_list) > 4:
            raise RuntimeError("images maxItems is 4")

        payload: Dict[str, Any] = {
            "model": "kwaivgi/kling-video-o3-pro/video-edit",
            "prompt": prompt,
            "video": video,
            "keep_original_sound": bool(keep_original_sound),
        }

        if image_list:
            payload["images"] = image_list

        prediction_id = client.generate_video(payload)
        result = client.poll_prediction(prediction_id, poll_interval_sec=poll_interval_sec, timeout_sec=float(timeout_sec))

        outputs = (result.get("data") or {}).get("outputs") or []
        if not outputs:
            raise RuntimeError(f"No outputs returned for prediction {prediction_id}: {result}")

        return (outputs[0], prediction_id)
