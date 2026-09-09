from __future__ import annotations

from typing import Any, Dict, List, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasOpenAIGPTImage25SunburstEdit:
    CATEGORY = "AtlasCloud/Image"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("image_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "prompt": ("STRING", {"multiline": True, "tooltip": "Text instruction for editing (up to 32000 characters)"}),
                # Schema requires 'images' as an array; follow existing GPT Image Edit UX: multiline string, one per line.
                "images": ("STRING", {"multiline": True, "default": "", "tooltip": "1-16 image URLs/base64/asset:// refs, one per line"}),
            },
            "optional": {
                "mask": (
                    "STRING",
                    {"default": "", "tooltip": "Optional mask image (URL/base64/asset:// ref); transparent areas are edited."},
                ),
                "quality": (
                    ["auto", "low", "medium", "high", "xhigh", "max"],
                    {"default": "medium", "tooltip": "Rendering quality tier. gpt-image-2.5 adds xhigh and max on top of low/medium/high."},
                ),
                "size": (
                    ["auto", "1024x1024", "1024x768", "768x1024", "1024x1536", "1536x1024", "2048x2048", "2048x1152", "1152x2048", "2560x1088", "1088x2560", "2880x2160", "2160x2880", "3840x2160", "2160x3840"],
                    {"default": "1024x1024", "tooltip": "The size of the generated image in pixels (width x height). Resolutions above 2560x1440 are experimental."},
                ),
                "background": (
                    ["auto", "opaque", "transparent"],
                    {"default": "auto", "tooltip": "Background handling. Use transparent for cut-outs (png/webp only)."},
                ),
                "output_format": (
                    ["png", "jpeg", "webp"],
                    {"default": "png", "tooltip": "The format of the output image."},
                ),
                "moderation": (
                    ["auto", "low"],
                    {"default": "auto", "tooltip": "Content moderation strictness."},
                ),
                "poll_interval_sec": (
                    "FLOAT",
                    {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"},
                ),
                "timeout_sec": (
                    "INT",
                    {"default": 300, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"},
                ),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        prompt: str,
        images: str,
        mask: str = "",
        quality: str = "medium",
        size: str = "1024x1024",
        background: str = "auto",
        output_format: str = "png",
        moderation: str = "auto",
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 300,
    ) -> Tuple[str, str]:
        p = (prompt or "").strip()
        if not p:
            raise RuntimeError("prompt is required")

        image_list: List[str] = [v.strip() for v in (images or "").splitlines() if v.strip()]
        if not image_list:
            raise RuntimeError("images is required (1-16 lines)")
        if len(image_list) > 16:
            raise RuntimeError("images maxItems is 16")

        payload: Dict[str, Any] = {
            "model": "openai/gpt-image-2.5-sunburst/edit",
            "prompt": p,
            "images": image_list,
            "quality": quality,
            "size": size,
            "background": background,
            "output_format": output_format,
            "moderation": moderation,
        }

        m = (mask or "").strip()
        if m:
            payload["mask"] = m

        client = atlas_client.client
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
