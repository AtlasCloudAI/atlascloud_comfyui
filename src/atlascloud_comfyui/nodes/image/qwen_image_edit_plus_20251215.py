from __future__ import annotations

from typing import Any, Dict, List, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasQwenImageEditPlus20251215:
    CATEGORY = "AtlasCloud/Image"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("image_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "images": ("STRING", {"multiline": True, "default": "", "tooltip": "1-3 image URLs/base64, one per line"}),
                "prompt": ("STRING", {"multiline": True, "tooltip": "Edit instruction"}),
            },
            "optional": {
                "negative_prompt": ("STRING", {"multiline": True, "default": "", "tooltip": "Exclude instruction"}),
                "prompt_extend": ("BOOLEAN", {"default": False, "tooltip": "Intelligent prompt rewriting"}),
                "size": ("STRING", {"default": "", "tooltip": "Output resolution (512-2048). Empty = keep last image resolution"}),
                "num_images": ("INT", {"default": 1, "min": 1, "max": 6, "tooltip": "Number of output images (1-6)"}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2**31 - 1, "tooltip": "Random if -1"}),
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
        prompt_extend: bool = False,
        size: str = "",
        num_images: int = 1,
        seed: int = -1,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 300,
    ) -> Tuple[str, str]:
        image_list: List[str] = [v.strip() for v in (images or "").splitlines() if v.strip()]
        if not image_list:
            raise RuntimeError("images is required (1-3 lines)")
        if len(image_list) > 3:
            raise RuntimeError("images maxItems is 3")

        prompt = (prompt or "").strip()
        if not prompt:
            raise RuntimeError("prompt is required")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "alibaba/qwen-image/edit-plus-20251215",
            "images": image_list,
            "prompt": prompt,
            "prompt_extend": bool(prompt_extend),
            "num_images": int(num_images),
            "seed": int(seed),
        }

        neg = (negative_prompt or "").strip()
        if neg:
            payload["negative_prompt"] = neg

        if (size or "").strip():
            payload["size"] = str(size).strip()

        prediction_id = client.generate_image(payload)
        result = client.poll_prediction(prediction_id, poll_interval_sec=float(poll_interval_sec), timeout_sec=float(timeout_sec))

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
