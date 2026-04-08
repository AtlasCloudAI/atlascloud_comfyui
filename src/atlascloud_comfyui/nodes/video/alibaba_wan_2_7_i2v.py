from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasWan27ImageToVideo:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "image": ("STRING", {"default": "", "tooltip": "First frame image (URL/base64)"}),
            },
            "optional": {
                "prompt": ("STRING", {"multiline": True, "default": "", "tooltip": "Prompt (optional)"}),
                "negative_prompt": ("STRING", {"multiline": True, "default": "", "tooltip": "Negative prompt"}),
                "duration": ("INT", {"default": 5, "min": 1, "max": 60, "tooltip": "Duration (seconds)"}),
                "resolution": (["720P", "1080P"], {"default": "1080P", "tooltip": "Resolution"}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2**31 - 1, "tooltip": "Random if -1"}),
                "prompt_extend": ("BOOLEAN", {"default": True, "tooltip": "Auto prompt expansion"}),
                "audio": ("STRING", {"default": "", "tooltip": "Optional audio URL"}),
                "last_image": ("STRING", {"default": "", "tooltip": "Optional last frame image (URL/base64)"}),
                "video": ("STRING", {"default": "", "tooltip": "(Optional) video URL"}),
                "poll_interval_sec": (
                    "FLOAT",
                    {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"},
                ),
                "timeout_sec": ("INT", {"default": 900, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        image: str,
        prompt: str = "",
        negative_prompt: str = "",
        duration: int = 5,
        resolution: str = "1080P",
        seed: int = -1,
        prompt_extend: bool = True,
        audio: str = "",
        last_image: str = "",
        video: str = "",
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        image = (image or "").strip()
        if not image:
            raise RuntimeError("image is required for AtlasCloud WAN2.7 Image-to-Video")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "alibaba/wan-2.7/image-to-video",
            "image": image,
            "duration": int(duration),
            "resolution": resolution,
            "prompt_extend": bool(prompt_extend),
        }

        p = (prompt or "").strip()
        if p:
            payload["prompt"] = p

        neg = (negative_prompt or "").strip()
        if neg:
            payload["negative_prompt"] = neg

        a = (audio or "").strip()
        if a:
            payload["audio"] = a

        li = (last_image or "").strip()
        if li:
            payload["last_image"] = li

        v = (video or "").strip()
        if v:
            payload["video"] = v

        if int(seed) >= 0:
            payload["seed"] = int(seed)

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
