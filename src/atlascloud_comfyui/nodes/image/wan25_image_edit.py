from __future__ import annotations

from typing import Any, Dict, List, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasWan25ImageEdit:
    CATEGORY = "AtlasCloud/Image"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("image_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        sizes = [
            "576*1344",
            "720*1280",
            "720*1680",
            "768*1024",
            "800*1200",
            "816*1904",
            "936*1664",
            "960*1280",
            "960*1440",
            "1024*768",
            "1024*1024",
            "1040*1560",
            "1104*1472",
            "1200*800",
            "1280*720",
            "1280*960",
            "1280*1280",
            "1344*576",
            "1440*960",
            "1472*1104",
            "1560*1040",
            "1664*936",
            "1680*720",
            "1904*816",
        ]

        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "images": ("STRING", {"multiline": True, "default": "", "tooltip": "1-3 image URLs/base64, one per line"}),
                "prompt": ("STRING", {"multiline": True, "tooltip": "Edit instruction"}),
            },
            "optional": {
                "negative_prompt": ("STRING", {"multiline": True, "default": "", "tooltip": "Negative prompt"}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2**31 - 1, "tooltip": "Random if -1"}),
                "size": (sizes, {"default": "1280*1280", "tooltip": "Output size (WIDTH*HEIGHT)"}),
                "enable_prompt_expansion": ("BOOLEAN", {"default": False, "tooltip": "Enable prompt optimizer"}),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"}),
                "timeout_sec": ("INT", {"default": 300, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        images: str,
        prompt: str,
        negative_prompt: str = "",
        seed: int = -1,
        size: str = "1280*1280",
        enable_prompt_expansion: bool = False,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 300,
    ) -> Tuple[str, str]:
        image_list: List[str] = [v.strip() for v in (images or "").splitlines() if v.strip()]
        if not image_list:
            raise RuntimeError("images is required (1-3 lines)")
        if len(image_list) > 3:
            raise RuntimeError("images maxItems is 3")

        p = (prompt or "").strip()
        if not p:
            raise RuntimeError("prompt is required")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "alibaba/wan-2.5/image-edit",
            "images": image_list,
            "prompt": p,
            "size": size,
            "seed": int(seed),
            "enable_prompt_expansion": bool(enable_prompt_expansion),
        }

        neg = (negative_prompt or "").strip()
        if neg:
            payload["negative_prompt"] = neg

        prediction_id = client.generate_image(payload)
        result = client.poll_prediction(prediction_id, poll_interval_sec=poll_interval_sec, timeout_sec=float(timeout_sec))

        outputs = (result.get("data") or {}).get("outputs") or []
        if not outputs:
            raise RuntimeError(f"No outputs returned for prediction {prediction_id}: {result}")

        first = outputs[0]
        if isinstance(first, dict):
            url = first.get("url") or first.get("image") or first.get("output")
            if isinstance(url, str) and url.strip():
                return (url, prediction_id)
            raise RuntimeError(f"Unexpected output object for prediction {prediction_id}: {first}")

        if not isinstance(first, str):
            raise RuntimeError(f"Unexpected output type for prediction {prediction_id}: {type(first).__name__} {first!r}")

        return (first, prediction_id)
