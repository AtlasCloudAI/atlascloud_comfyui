from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasFluxSchnellTextToImage:
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
                "size": ("STRING", {"default": "1024*1024", "tooltip": "Output size (WIDTH*HEIGHT)"}),
            },
            "optional": {
                "image": ("STRING", {"default": "", "tooltip": "Optional input image URL/base64"}),
                "mask_image": ("STRING", {"default": "", "tooltip": "Optional mask image URL/base64"}),
                "strength": ("FLOAT", {"default": 0.8, "min": 0.0, "max": 1.0, "tooltip": "Strength (image transform)"}),
                "num_images": ("INT", {"default": 1, "min": 1, "max": 4, "tooltip": "Number of images"}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2**31 - 1, "tooltip": "Random if -1"}),
                "enable_base64_output": ("BOOLEAN", {"default": False, "tooltip": "Return base64 instead of URL if supported"}),
                "enable_sync_mode": ("BOOLEAN", {"default": False, "tooltip": "If true, server may try to return result synchronously"}),
                "enable_safety_checker": ("BOOLEAN", {"default": True, "tooltip": "Enable safety checker"}),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"}),
                "timeout_sec": ("INT", {"default": 300, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        prompt: str,
        size: str,
        image: str = "",
        strength: float = 0.8,
        mask_image: str = "",
        num_images: int = 1,
        seed: int = -1,
        enable_base64_output: bool = False,
        enable_sync_mode: bool = False,
        enable_safety_checker: bool = True,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 300,
    ) -> Tuple[str, str]:
        client = atlas_client.client

        p = (prompt or "").strip()
        if not p:
            raise RuntimeError("prompt is required")

        payload: Dict[str, Any] = {
            "model": "black-forest-labs/flux-schnell",
            "prompt": p,
            "size": str(size).strip(),
            "num_images": int(num_images),
            "seed": int(seed),
            "enable_base64_output": bool(enable_base64_output),
            "enable_sync_mode": bool(enable_sync_mode),
            "enable_safety_checker": bool(enable_safety_checker),
        }

        img = (image or "").strip()
        if img:
            payload["image"] = img
            payload["strength"] = float(strength)

            m = (mask_image or "").strip()
            if m:
                payload["mask_image"] = m

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
