from __future__ import annotations

from typing import Any, Dict, List, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasWAN26ImageEdit:
    CATEGORY = "AtlasCloud/Image"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("image_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "prompt": ("STRING", {"multiline": True, "tooltip": "Edit instruction"}),
                "images": ("STRING", {"multiline": True, "default": "", "tooltip": "1-4 image URLs/base64, one per line"}),
                "size": (
                    [
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
                    ],
                    {"default": "1280*1280", "tooltip": "Output size (WIDTH*HEIGHT)"},
                ),
            },
            "optional": {
                "negative_prompt": ("STRING", {"multiline": True, "default": "", "tooltip": "Negative prompt"}),
                "enable_prompt_expansion": ("BOOLEAN", {"default": False, "tooltip": "Enable prompt optimizer"}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2**31 - 1, "tooltip": "Random if -1"}),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"}),
                "timeout_sec": ("INT", {"default": 300, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        prompt: str,
        images: str,
        size: str,
        negative_prompt: str = "",
        enable_prompt_expansion: bool = False,
        seed: int = -1,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 300,
    ) -> Tuple[str, str]:
        prompt = (prompt or "").strip()
        if not prompt:
            raise RuntimeError("prompt is required")

        image_list: List[str] = [v.strip() for v in (images or "").splitlines() if v.strip()]
        if not image_list:
            raise RuntimeError("images is required (1-4 lines)")
        if len(image_list) > 4:
            raise RuntimeError("images maxItems is 4")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "alibaba/wan-2.6/image-edit",
            "images": image_list,
            "prompt": prompt,
            "size": size,
        }

        neg = (negative_prompt or "").strip()
        if neg:
            payload["negative_prompt"] = neg

        payload["enable_prompt_expansion"] = bool(enable_prompt_expansion)

        if int(seed) >= 0:
            payload["seed"] = int(seed)

        prediction_id = client.generate_image(payload)
        result = client.poll_prediction(prediction_id, poll_interval_sec=float(poll_interval_sec), timeout_sec=float(timeout_sec))

        outputs = (result.get("data") or {}).get("outputs") or []
        if not outputs:
            raise RuntimeError(f"No outputs returned for prediction {prediction_id}: {result}")

        first = outputs[0]
        if isinstance(first, dict):
            # Some schemas declare outputs as objects; best-effort common fields.
            url = first.get("url") or first.get("image") or first.get("output")
            if isinstance(url, str) and url.strip():
                return (url, prediction_id)
            raise RuntimeError(f"Unexpected output object for prediction {prediction_id}: {first}")

        if not isinstance(first, str):
            raise RuntimeError(f"Unexpected output type for prediction {prediction_id}: {type(first).__name__} {first!r}")

        return (first, prediction_id)
