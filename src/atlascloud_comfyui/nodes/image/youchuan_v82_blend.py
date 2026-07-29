from __future__ import annotations

from typing import Any, Dict, List, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasYouchuanV82Blend:
    CATEGORY = "AtlasCloud/Image"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("image_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "images": ("STRING", {"multiline": True, "default": "", "tooltip": "2-5 input image URLs to blend, one per line"}),
            },
            "optional": {
                "prompt": ("STRING", {"multiline": True, "default": "", "tooltip": "Optional text prompt guiding the blend (max 1024 chars)"}),
                "aspect_ratio": (
                    ["1:1", "9:16", "16:9", "4:3", "3:4", "2:3", "3:2", "9:21", "21:9"],
                    {"default": "1:1", "tooltip": "Aspect ratio of the generated image"},
                ),
                "hd": ("BOOLEAN", {"default": False, "tooltip": "Enable native 2K HD generation (costs 1.5x)"}),
                "stylize": ("INT", {"default": 0, "min": 0, "max": 1000, "tooltip": "How strongly the default aesthetic is applied (0-1000)"}),
                "chaos": ("INT", {"default": 0, "min": 0, "max": 100, "tooltip": "Higher values produce more varied results (0-100)"}),
                "weird": ("INT", {"default": 0, "min": 0, "max": 3000, "tooltip": "Makes results quirky and unconventional (0-3000)"}),
                "quality": ([1, 4], {"default": 1, "tooltip": "Image detail. 4 = higher detail at same price (slower)"}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2**31 - 1, "tooltip": "Random if -1"}),
                "enable_base64_output": ("BOOLEAN", {"default": False, "tooltip": "Return base64 instead of URL if supported"}),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"}),
                "timeout_sec": ("INT", {"default": 300, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        images: str,
        prompt: str = "",
        aspect_ratio: str = "1:1",
        hd: bool = False,
        stylize: int = 0,
        chaos: int = 0,
        weird: int = 0,
        quality: int = 1,
        seed: int = -1,
        enable_base64_output: bool = False,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 300,
    ) -> Tuple[str, str]:
        image_list: List[str] = [v.strip() for v in (images or "").splitlines() if v.strip()]
        if len(image_list) < 2:
            raise RuntimeError("images requires at least 2 URLs (one per line) for Youchuan V8.2 Blend")
        if len(image_list) > 5:
            raise RuntimeError("images maxItems is 5 for Youchuan V8.2 Blend")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "youchuan/v8.2/blend",
            "images": image_list,
            "aspect_ratio": aspect_ratio,
            "hd": bool(hd),
            "stylize": int(stylize),
            "chaos": int(chaos),
            "weird": int(weird),
            "quality": int(quality),
            "enable_base64_output": bool(enable_base64_output),
        }

        p = (prompt or "").strip()
        if p:
            payload["prompt"] = p
        if int(seed) >= 0:
            payload["seed"] = int(seed)

        prediction_id = client.generate_image(payload)
        result = client.poll_prediction(
            prediction_id,
            poll_interval_sec=float(poll_interval_sec),
            timeout_sec=float(timeout_sec),
        )

        outputs = (result.get("data") or {}).get("outputs") or []
        if not outputs:
            raise RuntimeError(f"No outputs returned for prediction {prediction_id}: {result}")

        return (outputs[0], prediction_id)
