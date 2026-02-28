from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasNanoBanana2Edit:
    CATEGORY = "AtlasCloud/Image"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("image_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "image": ("STRING", {"default": "", "tooltip": "Input image URL or base64 (up to 14 reference images, comma-separated)"}),
                "prompt": ("STRING", {"multiline": True, "tooltip": "Text prompt for editing"}),
                "aspect_ratio": (
                    ["1:1", "3:2", "2:3", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"],
                    {"default": "1:1", "tooltip": "Aspect ratio"},
                ),
                "resolution": (["1k", "2k", "4k"], {"default": "1k", "tooltip": "Resolution preset"}),
                "output_format": (["png", "jpeg"], {"default": "png", "tooltip": "Output format"}),
                "enable_base64_output": ("BOOLEAN", {"default": False, "tooltip": "Return base64 instead of URL if supported"}),
            },
            "optional": {
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"}),
                "timeout_sec": ("INT", {"default": 300, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        image: str,
        prompt: str,
        aspect_ratio: str,
        resolution: str,
        output_format: str,
        enable_base64_output: bool,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 300,
    ) -> Tuple[str, str]:
        client = atlas_client.client

        image = (image or "").strip()
        if not image:
            raise RuntimeError("image is required (URL or base64)")

        images = [img.strip() for img in image.split(",") if img.strip()]

        payload: Dict[str, Any] = {
            "model": "google/nano-banana-2/edit",
            "images": images,
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
            "output_format": output_format,
            "enable_base64_output": enable_base64_output,
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
