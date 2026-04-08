from __future__ import annotations

from typing import Any, Dict, List, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasWan27ImageEdit:
    CATEGORY = "AtlasCloud/Image"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("image_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "prompt": ("STRING", {"multiline": True, "tooltip": "Edit instruction"}),
                "images": (
                    "STRING",
                    {"multiline": True, "default": "", "tooltip": "1+ image URLs/base64, one per line"},
                ),
            },
            "optional": {
                "size": (
                    ["1K", "2K"],
                    {"default": "2K", "tooltip": "Output resolution"},
                ),
                "thinking_mode": ("BOOLEAN", {"default": True, "tooltip": "Enable thinking mode"}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2**31 - 1, "tooltip": "Random if -1"}),
                "enable_sync_mode": ("BOOLEAN", {"default": False, "tooltip": "Try to return synchronously"}),
                "enable_base64_output": ("BOOLEAN", {"default": False, "tooltip": "Return base64 if supported"}),
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
        size: str = "2K",
        thinking_mode: bool = True,
        seed: int = -1,
        enable_sync_mode: bool = False,
        enable_base64_output: bool = False,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 300,
    ) -> Tuple[str, str]:
        prompt = (prompt or "").strip()
        if not prompt:
            raise RuntimeError("prompt is required for Alibaba WAN2.7 Image Edit")

        image_list: List[str] = [v.strip() for v in (images or "").splitlines() if v.strip()]
        if not image_list:
            raise RuntimeError("images is required (provide 1+ lines)")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "alibaba/wan-2.7/image-edit",
            "prompt": prompt,
            "images": image_list,
            "size": size,
            "n": 1,
            "thinking_mode": bool(thinking_mode),
            "seed": int(seed),
            "enable_sync_mode": bool(enable_sync_mode),
            "enable_base64_output": bool(enable_base64_output),
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
            # Some schemas declare outputs as objects; best-effort common fields.
            url = first.get("url") or first.get("image") or first.get("output")
            if isinstance(url, str) and url.strip():
                return (url, prediction_id)
            raise RuntimeError(f"Unexpected output object for prediction {prediction_id}: {first}")

        if not isinstance(first, str):
            raise RuntimeError(f"Unexpected output type for prediction {prediction_id}: {type(first).__name__} {first!r}")

        return (first, prediction_id)
