from __future__ import annotations

from typing import Any, Dict, List, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasWAN26VideoToVideo:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "prompt": ("STRING", {"multiline": True, "tooltip": "Use character1/character2... to refer to input videos"}),
                "videos": ("STRING", {"multiline": True, "tooltip": "1-3 video URLs, one per line"}),
                "size": (
                    [
                        "1280*720",
                        "720*1280",
                        "960*960",
                        "1088*832",
                        "832*1088",
                        "1920*1080",
                        "1080*1920",
                        "1440*1440",
                        "1632*1248",
                        "1248*1632",
                    ],
                    {"default": "1280*720"},
                ),
            },
            "optional": {
                "negative_prompt": ("STRING", {"multiline": True, "default": ""}),
                "duration": ([5, 10], {"default": 5}),
                "enable_prompt_expansion": ("BOOLEAN", {"default": True}),
                "shot_type": (["multi", "single"], {"default": "multi"}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2**31 - 1}),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0}),
                "timeout_sec": ("INT", {"default": 900, "min": 30, "max": 7200}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        prompt: str,
        videos: str,
        size: str,
        negative_prompt: str = "",
        duration: int = 5,
        enable_prompt_expansion: bool = True,
        shot_type: str = "multi",
        seed: int = -1,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        client = atlas_client.client

        video_list: List[str] = [v.strip() for v in (videos or "").splitlines() if v.strip()]
        if not video_list:
            raise RuntimeError("videos is required (provide 1-3 URLs, one per line)")
        if len(video_list) > 3:
            raise RuntimeError("videos maxItems is 3")

        payload: Dict[str, Any] = {
            "model": "alibaba/wan-2.6/video-to-video",
            "prompt": prompt,
            "videos": video_list,
            "size": size,
            "duration": int(duration),
            "enable_prompt_expansion": bool(enable_prompt_expansion),
            "shot_type": shot_type,
            "seed": int(seed),
        }

        if (negative_prompt or "").strip():
            payload["negative_prompt"] = negative_prompt

        prediction_id = client.generate_video(payload)
        result = client.poll_prediction(prediction_id, poll_interval_sec=poll_interval_sec, timeout_sec=float(timeout_sec))

        outputs = (result.get("data") or {}).get("outputs") or []
        if not outputs:
            raise RuntimeError(f"No outputs returned for prediction {prediction_id}: {result}")

        return (outputs[0], prediction_id)
