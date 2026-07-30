from __future__ import annotations

from typing import Any, Dict, List, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasWan27SpicyReferenceToVideo:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "reference_images": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": "",
                        "tooltip": "1-4 image URLs/base64, one per line (images only; video/audio refs unsupported)",
                    },
                ),
                "prompt": (
                    "STRING",
                    {"multiline": True, "tooltip": "Text prompt; bind subjects with @image1, @image2, ..."},
                ),
            },
            "optional": {
                "duration": ("INT", {"default": 5, "min": 2, "max": 15, "tooltip": "Duration (seconds)"}),
                "resolution": (
                    ["720P", "1080P", "1080P-SR", "1440P-SR"],
                    {"default": "720P", "tooltip": "Output resolution (SR variants use super-resolution)"},
                ),
                "aspect_ratio": (
                    ["auto", "16:9", "9:16", "4:3", "3:4", "1:1"],
                    {"default": "auto", "tooltip": "Aspect ratio (auto = follow reference images)"},
                ),
                "poll_interval_sec": (
                    "FLOAT",
                    {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"},
                ),
                "timeout_sec": ("INT", {"default": 900, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        reference_images: str,
        prompt: str,
        duration: int = 5,
        resolution: str = "720P",
        aspect_ratio: str = "auto",
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        ref_imgs: List[str] = [v.strip() for v in (reference_images or "").splitlines() if v.strip()]
        if not ref_imgs:
            raise RuntimeError(
                "reference_images is required for AtlasCloud WAN2.7 Spicy Reference-to-Video (1-4 images)"
            )
        if len(ref_imgs) > 4:
            raise RuntimeError(f"At most 4 reference images are supported, got {len(ref_imgs)}")

        p = (prompt or "").strip()
        if not p:
            raise RuntimeError("prompt is required")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "atlascloud/wan-2.7-spicy/reference-to-video",
            "reference_images": ref_imgs,
            "prompt": p,
            "duration": int(duration),
            "resolution": resolution,
            "aspect_ratio": aspect_ratio,
        }

        prediction_id = client.generate_video(payload)
        result = client.poll_prediction(
            prediction_id,
            poll_interval_sec=float(poll_interval_sec),
            timeout_sec=float(timeout_sec),
        )

        outputs = (result.get("data") or {}).get("outputs") or []
        if not outputs:
            raise RuntimeError(f"No outputs returned for prediction {prediction_id}: {result}")

        first = outputs[0]
        if not isinstance(first, str):
            raise RuntimeError(
                f"Unexpected output type for prediction {prediction_id}: {type(first).__name__} {first!r}"
            )

        return (first, prediction_id)
