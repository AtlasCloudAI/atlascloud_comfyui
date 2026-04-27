from __future__ import annotations

from typing import Any, Dict, List, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasHappyHorse10VideoEdit:
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
                "prompt": ("STRING", {"multiline": True, "tooltip": "Text prompt"}),
            },
            "optional": {
                "images": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": "",
                        "tooltip": "Optional reference image URLs/base64, one per line (up to 5)",
                    },
                ),
                "resolution": (
                    ["720P", "1080P"],
                    {"default": "1080P", "tooltip": "Resolution"},
                ),
                "audio_setting": (
                    ["auto", "origin"],
                    {
                        "default": "auto",
                        "tooltip": "Audio behavior (auto or keep origin)",
                    },
                ),
                "seed": (
                    "INT",
                    {"default": -1, "min": -1, "max": 2**31 - 1, "tooltip": "Random if -1"},
                ),
                "poll_interval_sec": (
                    "FLOAT",
                    {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"},
                ),
                "timeout_sec": (
                    "INT",
                    {"default": 1200, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"},
                ),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        video: str,
        prompt: str,
        images: str = "",
        resolution: str = "1080P",
        audio_setting: str = "auto",
        seed: int = -1,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 1200,
    ) -> Tuple[str, str]:
        video = (video or "").strip()
        if not video:
            raise RuntimeError("video is required for Alibaba HappyHorse-1.0 Video-Edit")

        prompt = (prompt or "").strip()
        if not prompt:
            raise RuntimeError("prompt is required for Alibaba HappyHorse-1.0 Video-Edit")

        image_list: List[str] = [v.strip() for v in (images or "").splitlines() if v.strip()]

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "alibaba/happyhorse-1.0/video-edit",
            "video": video,
            "prompt": prompt,
            "resolution": resolution,
            "audio_setting": audio_setting,
        }

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
