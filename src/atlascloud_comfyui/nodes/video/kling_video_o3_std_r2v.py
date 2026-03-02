from __future__ import annotations

from typing import Any, Dict, List, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasKlingVideoO3StdReferenceToVideo:
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
            },
            "optional": {
                "video": ("STRING", {"default": "", "tooltip": "Reference video URL (optional)"}),
                "images": ("STRING", {"multiline": True, "default": "", "tooltip": "0-7 image URLs, one per line"}),
                "keep_original_sound": ("BOOLEAN", {"default": True}),
                "sound": ("BOOLEAN", {"default": False}),
                "aspect_ratio": (["16:9", "9:16", "1:1"], {"default": "16:9"}),
                "duration": ("INT", {"default": 5, "min": 3, "max": 15}),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0}),
                "timeout_sec": ("INT", {"default": 900, "min": 30, "max": 7200}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        prompt: str,
        video: str = "",
        images: str = "",
        keep_original_sound: bool = True,
        sound: bool = False,
        aspect_ratio: str = "16:9",
        duration: int = 5,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        client = atlas_client.client

        image_list: List[str] = [v.strip() for v in (images or "").splitlines() if v.strip()]
        if len(image_list) > 7:
            raise RuntimeError("images maxItems is 7")

        payload: Dict[str, Any] = {
            "model": "kwaivgi/kling-video-o3-std/reference-to-video",
            "prompt": prompt,
            "keep_original_sound": bool(keep_original_sound),
            "sound": bool(sound),
            "aspect_ratio": aspect_ratio,
            "duration": int(duration),
        }

        if (video or "").strip():
            payload["video"] = video
        if image_list:
            payload["images"] = image_list

        prediction_id = client.generate_video(payload)
        result = client.poll_prediction(prediction_id, poll_interval_sec=poll_interval_sec, timeout_sec=float(timeout_sec))

        outputs = (result.get("data") or {}).get("outputs") or []
        if not outputs:
            raise RuntimeError(f"No outputs returned for prediction {prediction_id}: {result}")

        return (outputs[0], prediction_id)
