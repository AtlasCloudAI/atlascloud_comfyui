from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasCosmos3SuperImageToVideo:
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
                "image_url": ("STRING", {"default": "", "tooltip": "First frame image (URL or data:image/...;base64,...)"}),
            },
            "optional": {
                "negative_prompt": ("STRING", {"multiline": True, "default": "", "tooltip": "Negative prompt"}),
                "image_size": (
                    ["square_hd", "square", "portrait_4_3", "portrait_16_9", "landscape_4_3", "landscape_16_9"],
                    {"default": "landscape_16_9", "tooltip": "Output resolution preset"},
                ),
                "duration": ([1, 2, 3, 4, 5, 6, 7], {"default": 5, "tooltip": "Duration (seconds)"}),
                "num_inference_steps": ("INT", {"default": 28, "min": 1, "max": 50, "tooltip": "Inference steps"}),
                "guidance_scale": ("FLOAT", {"default": 6.0, "min": 1.0, "max": 20.0, "tooltip": "Guidance scale"}),
                "randomize_seed": ("BOOLEAN", {"default": True, "tooltip": "开启后每次生成随机结果；关闭后使用下方固定 seed"}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 2**31 - 1, "tooltip": "固定 seed（仅在随机开关关闭时生效）"}),
                "enable_safety_checker": ("BOOLEAN", {"default": False, "tooltip": "Enable safety checker"}),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"}),
                "timeout_sec": ("INT", {"default": 900, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        prompt: str,
        image_url: str,
        negative_prompt: str = "",
        image_size: str = "landscape_16_9",
        duration: int = 5,
        num_inference_steps: int = 28,
        guidance_scale: float = 6.0,
        randomize_seed: bool = True,
        seed: int = 0,
        enable_safety_checker: bool = False,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        image_url = (image_url or "").strip()
        if not image_url:
            raise RuntimeError("image_url is required for Cosmos 3 Super Image-to-Video")

        p = (prompt or "").strip()
        if not p:
            raise RuntimeError("prompt is required")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "nvidia/cosmos-3-super/image-to-video",
            "prompt": p,
            "image_url": image_url,
            "image_size": image_size,
            "duration": int(duration),
            "num_inference_steps": int(num_inference_steps),
            "guidance_scale": float(guidance_scale),
            "enable_safety_checker": bool(enable_safety_checker),
        }

        neg = (negative_prompt or "").strip()
        if neg:
            payload["negative_prompt"] = neg
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
