from __future__ import annotations

from typing import Any, Dict, List, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasWan27VideoEdit:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "video": ("STRING", {"default": "", "tooltip": "Input video URL"}),
            },
            "optional": {
                "prompt": ("STRING", {"multiline": True, "default": "", "tooltip": "Prompt (optional)"}),
                "negative_prompt": ("STRING", {"multiline": True, "default": "", "tooltip": "Negative prompt"}),
                "duration": ("INT", {"default": 0, "min": 0, "max": 60, "tooltip": "Optional duration"}),
                "resolution": (["720P", "1080P"], {"default": "1080P", "tooltip": "Resolution"}),
                "ratio": (
                    ["16:9", "9:16", "1:1", "4:3", "3:4"],
                    {"default": "16:9", "tooltip": "Aspect ratio"},
                ),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2**31 - 1, "tooltip": "Random if -1"}),
                "prompt_extend": ("BOOLEAN", {"default": True, "tooltip": "Auto prompt expansion"}),
                "audio": ("STRING", {"default": "", "tooltip": "Optional audio URL"}),
                "images": (
                    "STRING",
                    {"multiline": True, "default": "", "tooltip": "Optional images, one per line"},
                ),
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
        video: str,
        prompt: str = "",
        negative_prompt: str = "",
        duration: int = 0,
        resolution: str = "1080P",
        ratio: str = "16:9",
        seed: int = -1,
        prompt_extend: bool = True,
        audio: str = "",
        images: str = "",
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        video = (video or "").strip()
        if not video:
            raise RuntimeError("video is required for AtlasCloud WAN2.7 Video-Edit")

        image_list: List[str] = [v.strip() for v in (images or "").splitlines() if v.strip()]

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "alibaba/wan-2.7/video-edit",
            "video": video,
            "resolution": resolution,
            "ratio": ratio,
            "prompt_extend": bool(prompt_extend),
        }

        p = (prompt or "").strip()
        if p:
            payload["prompt"] = p

        neg = (negative_prompt or "").strip()
        if neg:
            payload["negative_prompt"] = neg

        if int(duration) > 0:
            payload["duration"] = int(duration)

        a = (audio or "").strip()
        if a:
            payload["audio"] = a

        if image_list:
            payload["images"] = image_list

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
