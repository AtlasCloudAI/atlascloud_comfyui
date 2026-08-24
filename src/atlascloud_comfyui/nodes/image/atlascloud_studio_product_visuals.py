from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle

_VISUAL_TYPES = ["product_hero", "product_detail", "promo_poster"]
_RATIOS = ["1:1", "3:4", "4:3", "16:9", "9:16"]
_RESOLUTIONS = ["1k", "2k", "4k"]
_FORMATS = ["png", "jpeg"]


class AtlasStudioProductVisuals:
    CATEGORY = "AtlasCloud/Image"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("image_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "product_image": ("STRING", {"default": "", "tooltip": "Product image URL (<=10MB)"}),
                "user_prompt": (
                    "STRING",
                    {"multiline": True, "tooltip": "Brand, key benefits and the visual style you want"},
                ),
            },
            "optional": {
                "model_image": (
                    "STRING",
                    {"default": "", "tooltip": "Optional model image URL; omit to let the model invent one when needed"},
                ),
                "visual_type": (_VISUAL_TYPES, {"default": "product_hero", "tooltip": "Layout: hero shot, detail page or poster"}),
                "ratio": (_RATIOS, {"default": "9:16", "tooltip": "Aspect ratio"}),
                "resolution": (
                    _RESOLUTIONS,
                    {"default": "2k", "tooltip": "Output resolution; 4:3 and 3:4 have no mid tier, 1:1 caps at 2048"},
                ),
                "format": (_FORMATS, {"default": "png", "tooltip": "Output image format"}),
                "count": ("INT", {"default": 1, "min": 1, "max": 4, "tooltip": "Number of images to generate"}),
                "poll_interval_sec": (
                    "FLOAT",
                    {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"},
                ),
                "timeout_sec": ("INT", {"default": 600, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        product_image: str,
        user_prompt: str,
        model_image: str = "",
        visual_type: str = "product_hero",
        ratio: str = "9:16",
        resolution: str = "2k",
        format: str = "png",
        count: int = 1,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 600,
    ) -> Tuple[str, str]:
        product_image = (product_image or "").strip()
        if not product_image:
            raise RuntimeError("product_image is required for AtlasCloud Studio Product Visuals")

        user_prompt = (user_prompt or "").strip()
        if not user_prompt:
            raise RuntimeError("user_prompt is required for AtlasCloud Studio Product Visuals")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "atlascloud/studio/product-visuals",
            "product_image": product_image,
            "user_prompt": user_prompt,
            "visual_type": visual_type,
            "ratio": ratio,
            "resolution": resolution,
            "format": format,
            "count": int(count),
        }

        mi = (model_image or "").strip()
        if mi:
            payload["model_image"] = mi

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
