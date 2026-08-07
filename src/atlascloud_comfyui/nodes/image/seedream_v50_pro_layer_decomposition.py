from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasSeedreamV50ProLayerDecomposition:
    CATEGORY = "AtlasCloud/Image"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("image_url", "layer_urls", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "image": (
                    "STRING",
                    {"default": "", "tooltip": "Image to decompose into layers (URL or base64), exactly one"},
                ),
                "size": (
                    ["auto", "1K", "1.5K", "2K"],
                    {"default": "auto", "tooltip": "Output resolution tier (auto follows the input image)"},
                ),
                "output_format": (["jpeg", "png"], {"default": "jpeg", "tooltip": "File format of the base image"}),
                "enable_base64_output": ("BOOLEAN", {"default": False, "tooltip": "Return base64 instead of URL if supported"}),
            },
            "optional": {
                "prompt": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": "",
                        "tooltip": "Optional: which elements to split. Leave empty for automatic detection. Supports <bbox>x1 y1 x2 y2</bbox> in [0,1000] coords",
                    },
                ),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"}),
                "timeout_sec": ("INT", {"default": 300, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        image: str,
        size: str,
        output_format: str,
        enable_base64_output: bool,
        prompt: str = "",
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 300,
    ) -> Tuple[str, str, str]:
        image = (image or "").strip()
        if not image:
            raise RuntimeError("image is required for Seedream V5.0 Pro Layer Decomposition")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "bytedance/seedream-v5.0-pro/layer-decomposition",
            "image": image,
            "size": size,
            "output_format": output_format,
            "enable_base64_output": bool(enable_base64_output),
        }

        p = (prompt or "").strip()
        if p:
            payload["prompt"] = p

        prediction_id = client.generate_image(payload)
        result = client.poll_prediction(
            prediction_id,
            poll_interval_sec=poll_interval_sec,
            timeout_sec=float(timeout_sec),
        )

        outputs = (result.get("data") or {}).get("outputs") or []
        if not outputs:
            raise RuntimeError(f"No outputs returned for prediction {prediction_id}: {result}")

        # outputs[0] is the base image; the remaining entries are the decomposed layers.
        return (outputs[0], "\n".join(outputs[1:]), prediction_id)
