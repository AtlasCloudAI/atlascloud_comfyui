from __future__ import annotations

from typing import Any, Dict, List, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasWan27ReferenceToVideo:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "prompt": ("STRING", {"multiline": True, "tooltip": "Text prompt"}),
                "images": (
                    "STRING",
                    {"multiline": True, "default": "", "tooltip": "0+ image URLs/base64, one per line"},
                ),
                "videos": (
                    "STRING",
                    {"multiline": True, "default": "", "tooltip": "0+ video URLs, one per line"},
                ),
            },
            "optional": {
                "negative_prompt": ("STRING", {"multiline": True, "default": "", "tooltip": "Negative prompt"}),
                "duration": ("INT", {"default": 5, "min": 1, "max": 60, "tooltip": "Duration (seconds)"}),
                "resolution": (["720P", "1080P"], {"default": "1080P", "tooltip": "Resolution"}),
                "ratio": (
                    ["16:9", "9:16", "1:1", "4:3", "3:4"],
                    {"default": "16:9", "tooltip": "Aspect ratio"},
                ),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2**31 - 1, "tooltip": "Random if -1"}),
                "prompt_extend": ("BOOLEAN", {"default": False, "tooltip": "Auto prompt expansion"}),
                "audio": ("STRING", {"default": "", "tooltip": "Optional audio URL"}),
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
        prompt: str,
        images: str,
        videos: str,
        negative_prompt: str = "",
        duration: int = 5,
        resolution: str = "1080P",
        ratio: str = "16:9",
        seed: int = -1,
        prompt_extend: bool = False,
        audio: str = "",
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        prompt = (prompt or "").strip()
        if not prompt:
            raise RuntimeError("prompt is required for AtlasCloud WAN2.7 Reference-to-Video")

        image_list: List[str] = [v.strip() for v in (images or "").splitlines() if v.strip()]
        video_list: List[str] = [v.strip() for v in (videos or "").splitlines() if v.strip()]
        if not image_list and not video_list:
            raise RuntimeError("Provide at least one image or video reference")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "alibaba/wan-2.7/reference-to-video",
            "prompt": prompt,
            "duration": int(duration),
            "resolution": resolution,
            "ratio": ratio,
            "prompt_extend": bool(prompt_extend),
        }

        if image_list:
            payload["images"] = image_list
        if video_list:
            payload["videos"] = video_list

        neg = (negative_prompt or "").strip()
        if neg:
            payload["negative_prompt"] = neg

        a = (audio or "").strip()
        if a:
            payload["audio"] = a

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
