from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


# Naming note: file uses wan26_t2i.py for brevity, but the model is text-to-image.
# We still name the class AtlasWAN26TextToImage to match the product naming.


class AtlasWAN26TextToImage:
    CATEGORY = "AtlasCloud/Image"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("image_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "prompt": ("STRING", {"multiline": True}),
            },
            "optional": {
                "negative_prompt": ("STRING", {"multiline": True, "default": ""}),
                "size": (
                    [
                        "576*1344",
                        "720*1280",
                        "720*1680",
                        "768*1024",
                        "800*1200",
                        "936*2184",
                        "960*1280",
                        "960*1440",
                        "1024*768",
                        "1024*1024",
                        "1080*1920",
                        "1168*1752",
                        "1200*800",
                        "1200*1600",
                        "1224*1632",
                        "1280*720",
                        "1280*960",
                        "1280*1280",
                        "1344*576",
                        "1440*960",
                        "1440*1440",
                        "1600*1200",
                        "1632*1224",
                        "1680*720",
                        "1752*1168",
                        "1920*1080",
                        "2184*936",
                    ],
                    {"default": "1280*1280"},
                ),
                "enable_prompt_expansion": ("BOOLEAN", {"default": False}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2**31 - 1}),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0}),
                "timeout_sec": ("INT", {"default": 300, "min": 30, "max": 7200}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        prompt: str,
        negative_prompt: str = "",
        size: str = "1280*1280",
        enable_prompt_expansion: bool = False,
        seed: int = -1,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 300,
    ) -> Tuple[str, str]:
        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "alibaba/wan-2.6/text-to-image",
            "prompt": prompt,
            "size": size,
            "enable_prompt_expansion": bool(enable_prompt_expansion),
            "seed": int(seed),
        }

        if (negative_prompt or "").strip():
            payload["negative_prompt"] = negative_prompt

        prediction_id = client.generate_image(payload)
        result = client.poll_prediction(prediction_id, poll_interval_sec=poll_interval_sec, timeout_sec=float(timeout_sec))

        outputs = (result.get("data") or {}).get("outputs") or []
        if not outputs:
            raise RuntimeError(f"No outputs returned for prediction {prediction_id}: {result}")

        return (outputs[0], prediction_id)
