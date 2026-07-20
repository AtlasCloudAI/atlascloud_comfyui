from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasKrea2TurboTextToImage:
    CATEGORY = "AtlasCloud/Image"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("image_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "prompt": ("STRING", {"multiline": True, "tooltip": "Text prompt"}),
                "image_size": (
                    ["square_hd", "square", "portrait_3_4", "portrait_9_16", "landscape_4_3", "landscape_16_9"],
                    {"default": "square_hd", "tooltip": "Output image size preset"},
                ),
            },
            "optional": {
                "num_images": ("INT", {"default": 1, "min": 1, "max": 4, "tooltip": "Number of images"}),
                "output_format": (["png", "jpeg"], {"default": "png", "tooltip": "Output image format"}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2147483647, "tooltip": "Random if -1"}),
                "enable_base64_output": ("BOOLEAN", {"default": False, "tooltip": "Return base64 instead of URL if supported"}),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"}),
                "timeout_sec": ("INT", {"default": 300, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        prompt: str,
        image_size: str = "square_hd",
        num_images: int = 1,
        output_format: str = "png",
        seed: int = -1,
        enable_base64_output: bool = False,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 300,
    ) -> Tuple[str, str]:
        client = atlas_client.client

        p = (prompt or "").strip()
        if not p:
            raise RuntimeError("prompt is required")

        payload: Dict[str, Any] = {
            "model": "krea-2-turbo/text-to-image",
            "prompt": p,
            "image_size": image_size,
            "num_images": int(num_images),
            "output_format": output_format,
            "enable_base64_output": bool(enable_base64_output),
        }

        if int(seed) >= 0:
            payload["seed"] = int(seed)

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
