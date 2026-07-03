from __future__ import annotations

from typing import Any, Dict, List, Tuple

from ..auth.atlas_client_node import AtlasClientHandle

_IMAGE_SIZES = [
    "square_hd",
    "square",
    "portrait_3_4",
    "portrait_9_16",
    "landscape_4_3",
    "landscape_16_9",
]


class AtlasHiDreamO115TextToImage:
    CATEGORY = "AtlasCloud/Image"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("image_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "prompt": ("STRING", {"multiline": True, "tooltip": "Text prompt (max 2500 chars)"}),
                "image_size": (_IMAGE_SIZES, {"default": "landscape_4_3", "tooltip": "Output image size preset"}),
                "num_inference_steps": ("INT", {"default": 50, "min": 1, "max": 100, "tooltip": "Denoising steps"}),
                "guidance_scale": ("FLOAT", {"default": 5.0, "min": 1.0, "max": 20.0, "tooltip": "Guidance scale"}),
                "output_format": (["png", "jpeg", "webp"], {"default": "png", "tooltip": "Output format"}),
            },
            "optional": {
                "reference_image_urls": ("STRING", {"multiline": True, "default": "", "tooltip": "Optional reference image URLs for subject-driven personalization, ONE PER LINE"}),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"}),
                "timeout_sec": ("INT", {"default": 300, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        prompt: str,
        image_size: str,
        num_inference_steps: int,
        guidance_scale: float,
        output_format: str,
        reference_image_urls: str = "",
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 300,
    ) -> Tuple[str, str]:
        client = atlas_client.client

        p = (prompt or "").strip()
        if not p:
            raise RuntimeError("prompt is required")

        payload: Dict[str, Any] = {
            "model": "hidream-o1-1.5/text-to-image",
            "prompt": p,
            "image_size": image_size,
            "num_inference_steps": int(num_inference_steps),
            "guidance_scale": float(guidance_scale),
            "output_format": output_format,
        }

        refs: List[str] = [u.strip() for u in (reference_image_urls or "").splitlines() if u.strip()]
        if refs:
            payload["reference_image_urls"] = refs

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
