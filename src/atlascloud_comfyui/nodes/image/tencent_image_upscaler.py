from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasTencentImageUpscaler:
    CATEGORY = "AtlasCloud/Image"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("image_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "image_url": ("STRING", {"default": "", "tooltip": "Public HTTP(S) URL of the source image"}),
            },
            "optional": {
                "type": (
                    ["standard", "super", "ultra", "fidelity"],
                    {
                        "default": "ultra",
                        "tooltip": "Super-resolution type (standard = fastest, ultra = more detail)",
                    },
                ),
                "mode": (
                    ["percent", "aspect", "fixed"],
                    {"default": "percent", "tooltip": "percent = scale factor; aspect/fixed = target dimensions"},
                ),
                "percent": (
                    "FLOAT",
                    {"default": 2.0, "min": 1.0, "max": 10.0, "tooltip": "Scale factor for mode=percent"},
                ),
                "width": ("INT", {"default": 0, "min": 0, "max": 16384, "tooltip": "Target width (0 = unset)"}),
                "height": ("INT", {"default": 0, "min": 0, "max": 16384, "tooltip": "Target height (0 = unset)"}),
                "long_side": ("INT", {"default": 0, "min": 0, "max": 16384, "tooltip": "Target long edge (0 = unset)"}),
                "short_side": (
                    "INT",
                    {"default": 0, "min": 0, "max": 16384, "tooltip": "Target short edge (0 = unset)"},
                ),
                "encode_format": (
                    ["JPEG", "PNG", "WEBP", "BMP"],
                    {"default": "JPEG", "tooltip": "Output image encode format"},
                ),
                "encode_quality": (
                    "INT",
                    {"default": 80, "min": 1, "max": 100, "tooltip": "Encode quality for lossy formats"},
                ),
                "poll_interval_sec": (
                    "FLOAT",
                    {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"},
                ),
                "timeout_sec": ("INT", {"default": 300, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        image_url: str,
        type: str = "ultra",
        mode: str = "percent",
        percent: float = 2.0,
        width: int = 0,
        height: int = 0,
        long_side: int = 0,
        short_side: int = 0,
        encode_format: str = "JPEG",
        encode_quality: int = 80,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 300,
    ) -> Tuple[str, str]:
        img = (image_url or "").strip()
        if not img:
            raise RuntimeError("image_url is required for Tencent Image Upscaler")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "tencent/image/upscaler",
            "image_url": img,
            "type": type,
            "mode": mode,
            "encode_format": encode_format,
            "encode_quality": int(encode_quality),
        }

        if mode == "percent":
            payload["percent"] = float(percent)
        else:
            for key, value in (
                ("width", width),
                ("height", height),
                ("long_side", long_side),
                ("short_side", short_side),
            ):
                if int(value) > 0:
                    payload[key] = int(value)

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
