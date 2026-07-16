from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasFaceSwapImage:
    CATEGORY = "AtlasCloud/Image"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("image_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "source_face": ("STRING", {"default": "", "tooltip": "Source Face — the face to transfer (clear front-facing photo)"}),
                "target_image": ("STRING", {"default": "", "tooltip": "Target Image — the photo whose face gets replaced (pose/clothing/background preserved)"}),
            },
            "optional": {
                "size": (
                    ["auto", "2048*2048", "2304*1728", "1728*2304", "2720*1530", "1530*2720", "2496*1664", "1664*2496", "1024*1024", "1536*1536", "1776*1328", "1328*1776", "2048*1152", "1152*2048"],
                    {"default": "auto", "tooltip": "Output resolution/size"},
                ),
                "output_format": (["jpeg", "png"], {"default": "jpeg", "tooltip": "Output image format"}),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"}),
                "timeout_sec": ("INT", {"default": 300, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        source_face: str,
        target_image: str,
        size: str = "auto",
        output_format: str = "jpeg",
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 300,
    ) -> Tuple[str, str]:
        face = (source_face or "").strip()
        if not face:
            raise RuntimeError("source_face is required for AtlasCloud Face Swap (Image)")

        target = (target_image or "").strip()
        if not target:
            raise RuntimeError("target_image is required for AtlasCloud Face Swap (Image)")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "atlascloud/face-swap-image",
            "image": face,
            "Image": target,
            "size": size,
            "output_format": output_format,
        }

        prediction_id = client.generate_image(payload)
        result = client.poll_prediction(
            prediction_id,
            poll_interval_sec=float(poll_interval_sec),
            timeout_sec=float(timeout_sec),
        )

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
