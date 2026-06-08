from __future__ import annotations

from typing import Any, Dict, List, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasGrokImagineImageEdit:
    CATEGORY = "AtlasCloud/Image"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("image_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "prompt": ("STRING", {"multiline": True, "tooltip": "Edit prompt"}),
                "image_urls": ("STRING", {"multiline": True, "tooltip": "1-8 image URLs (one per line)"}),
                "resolution": (["1k", "2k"], {"default": "1k"}),
                "aspect_ratio": (
                    ["auto", "1:1", "3:4", "4:3", "9:16", "16:9", "2:3", "3:2", "9:19.5", "19.5:9", "9:20", "20:9", "1:2", "2:1"],
                    {"default": "auto", "tooltip": "Aspect ratio"},
                ),
                "num_images": ([1, 2, 3, 4], {"default": 1}),
                "enable_base64_output": ("BOOLEAN", {"default": False, "tooltip": "Return base64 instead of URL if supported"}),
            },
            "optional": {
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0}),
                "timeout_sec": ("INT", {"default": 300, "min": 30, "max": 7200}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        prompt: str,
        image_urls: str,
        resolution: str,
        aspect_ratio: str,
        num_images: int,
        enable_base64_output: bool,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 300,
    ) -> Tuple[str, str]:
        images: List[str] = [u.strip() for u in (image_urls or "").splitlines() if u.strip()]
        if not images:
            raise RuntimeError("image_urls is required (provide 1-8 URLs, one per line)")
        if len(images) > 8:
            raise RuntimeError("image_urls maxItems is 8")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "xai/grok-imagine-image/edit",
            "prompt": prompt,
            "image_urls": images,
            "resolution": resolution,
            "aspect_ratio": aspect_ratio,
            "num_images": int(num_images),
            "enable_base64_output": bool(enable_base64_output),
        }

        prediction_id = client.generate_image(payload)
        result = client.poll_prediction(
            prediction_id,
            poll_interval_sec=poll_interval_sec,
            timeout_sec=float(timeout_sec),
        )

        outputs = (result.get("data") or {}).get("outputs") or []
        if not outputs:
            raise RuntimeError(f"No outputs returned for prediction {prediction_id}: {result}")

        return (outputs[0], prediction_id)
