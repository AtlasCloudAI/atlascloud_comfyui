from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasVan26ImageToVideo:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "image": ("STRING", {"default": "", "tooltip": "Input image URL or base64"}),
                "prompt": ("STRING", {"multiline": True, "tooltip": "Text prompt"}),
                "resolution": (["1080p"], {"default": "1080p", "tooltip": "Resolution"}),
                "shot_type": (["multi", "single"], {"default": "multi", "tooltip": "Shot type"}),
                "enable_prompt_expansion": (
                    "BOOLEAN",
                    {"default": True, "tooltip": "Enable prompt optimizer"},
                ),
                "generate_audio": (
                    "BOOLEAN",
                    {"default": True, "tooltip": "Whether to automatically add audio"},
                ),
                "seed": (
                    "INT",
                    {"default": -1, "min": -1, "max": 2**31 - 1, "tooltip": "Random if -1"},
                ),
            },
            "optional": {
                "negative_prompt": ("STRING", {"multiline": True, "default": "", "tooltip": "Negative prompt"}),
                "audio": ("STRING", {"default": "", "tooltip": "Audio URL (optional)"}),
                "duration": ([5, 10, 15], {"default": 5, "tooltip": "Duration (seconds)"}),
                "poll_interval_sec": (
                    "FLOAT",
                    {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"},
                ),
                "timeout_sec": (
                    "INT",
                    {"default": 900, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"},
                ),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        image: str,
        prompt: str,
        resolution: str,
        shot_type: str,
        enable_prompt_expansion: bool,
        generate_audio: bool,
        seed: int,
        negative_prompt: str = "",
        audio: str = "",
        duration: int = 5,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        image = (image or "").strip()
        if not image:
            raise RuntimeError("image is required (URL or base64)")

        if shot_type == "multi" and not enable_prompt_expansion:
            raise RuntimeError("shot_type='multi' requires enable_prompt_expansion=True")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "atlascloud/van-2.6/image-to-video",
            "image": image,
            "prompt": prompt,
            "resolution": resolution,
            "duration": int(duration),
            "shot_type": shot_type,
            "enable_prompt_expansion": bool(enable_prompt_expansion),
            "generate_audio": bool(generate_audio),
        }

        neg = (negative_prompt or "").strip()
        if neg:
            payload["negative_prompt"] = neg

        aud = (audio or "").strip()
        if aud:
            payload["audio"] = aud

        if int(seed) >= 0:
            payload["seed"] = int(seed)

        prediction_id = client.generate_video(payload)
        result = client.poll_prediction(
            prediction_id,
            poll_interval_sec=poll_interval_sec,
            timeout_sec=float(timeout_sec),
        )

        outputs = (result.get("data") or {}).get("outputs") or []
        if not outputs:
            raise RuntimeError(f"No outputs returned for prediction {prediction_id}: {result}")

        first = outputs[0]
        if not isinstance(first, str):
            raise RuntimeError(f"Unexpected output type for prediction {prediction_id}: {type(first).__name__} {first!r}")

        return (first, prediction_id)
