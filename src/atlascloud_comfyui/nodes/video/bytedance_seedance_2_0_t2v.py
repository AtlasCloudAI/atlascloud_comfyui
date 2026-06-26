from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasSeedance20TextToVideo:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "prompt": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": "A golden retriever running on a sunny beach, waves crashing in the background, cinematic lighting",
                        "tooltip": "Text prompt",
                    },
                ),
            },
            "optional": {
                "duration": (
                    [-1, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                    {"default": 5, "tooltip": "Duration (seconds), or -1 for auto"},
                ),
                "resolution": (["480p", "720p", "1080p", "1080p-SR"], {"default": "720p", "tooltip": "Resolution (1080p = 原生1080p; 1080p-SR = 720p超分到1080p,更快更省但画质略降)"}),
                "ratio": (
                    ["16:9", "4:3", "1:1", "3:4", "9:16", "21:9", "adaptive"],
                    {"default": "adaptive", "tooltip": "Aspect ratio (adaptive = auto)"},
                ),
                "randomize_seed": ("BOOLEAN", {"default": True, "tooltip": "开启后每次生成随机结果；关闭后使用下方固定 seed"}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 4294967295, "tooltip": "固定 seed（仅在随机开关关闭时生效）"}),
                "generate_audio": ("BOOLEAN", {"default": True, "tooltip": "Generate audio"}),
                "web_search": ("BOOLEAN", {"default": False, "tooltip": "Enable web search (seedance-2.0 only)"}),
                "watermark": ("BOOLEAN", {"default": False, "tooltip": "Add watermark"}),
                "return_last_frame": ("BOOLEAN", {"default": False, "tooltip": "Return last frame (if supported)"}),
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
        prompt: str,
        randomize_seed: bool = True,
        seed: int = 0,
        duration: int = 5,
        resolution: str = "720p",
        ratio: str = "adaptive",
        generate_audio: bool = True,
        web_search: bool = False,
        watermark: bool = False,
        return_last_frame: bool = False,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        prompt = (prompt or "").strip()
        if not prompt:
            raise RuntimeError("prompt is required for AtlasCloud Seedance 2.0 Text-to-Video")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "bytedance/seedance-2.0/text-to-video",
            "prompt": prompt,
            "duration": int(duration),
            "resolution": resolution,
            "ratio": ratio,
            "generate_audio": bool(generate_audio),
            "web_search": bool(web_search),
            "watermark": bool(watermark),
            "return_last_frame": bool(return_last_frame),
        }

        if not randomize_seed:
            payload["seed"] = seed

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
