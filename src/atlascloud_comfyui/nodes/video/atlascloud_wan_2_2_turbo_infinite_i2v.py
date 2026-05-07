from __future__ import annotations

from typing import Any, Dict, List, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasWan22TurboInfiniteImageToVideo:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "image": (
                    "STRING",
                    {"default": "", "tooltip": "First-frame image URL/base64"},
                ),
                "prompt": (
                    "STRING",
                    {
                        "multiline": True,
                        "tooltip": "Prompts (one per line). Each segment generates `duration` seconds.",
                    },
                ),
            },
            "optional": {
                "duration": (
                    "INT",
                    {"default": 5, "min": 1, "max": 60, "tooltip": "Seconds per prompt segment"},
                ),
                "resolution": (
                    ["480p", "720p", "1080p"],
                    {"default": "720p", "tooltip": "Output resolution"},
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
                    {"default": 900, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"},
                ),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        image: str,
        prompt: str,
        duration: int = 5,
        resolution: str = "720p",
        seed: int = -1,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        client = atlas_client.client

        image = (image or "").strip()
        if not image:
            raise RuntimeError("image is required (URL or base64)")

        # Schema expects an ordered list of prompts (array). ComfyUI provides STRING, so split by lines.
        prompt_lines: List[str] = [ln.strip() for ln in (prompt or "").splitlines() if ln.strip()]
        if not prompt_lines:
            raise RuntimeError("prompt is required")

        payload: Dict[str, Any] = {
            "model": "atlascloud/wan-2.2-turbo/infinite-image-to-video",
            "image": image,
            "prompt": prompt_lines,
            "duration": int(duration),
            "resolution": resolution,
            "seed": int(seed),
        }

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
