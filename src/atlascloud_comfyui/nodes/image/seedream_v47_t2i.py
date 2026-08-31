from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle

# Shared size presets for the Seedream v4.7 family (1K / 2K / 4K tiers).
SEEDREAM_V47_SIZES = [
    "2048*2048", "2304*1728", "1728*2304", "2848*1600", "1600*2848",
    "2496*1664", "1664*2496", "3136*1344", "4096*4096", "4704*3520",
    "3520*4704", "5504*3040", "3040*5504", "4992*3328", "3328*4992",
    "6240*2656", "1024*1024", "1280*720", "720*1280", "1248*832",
    "832*1248", "1568*672",
]


class AtlasSeedreamV47TextToImage:
    CATEGORY = "AtlasCloud/Image"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("image_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "prompt": ("STRING", {"multiline": True, "tooltip": "The positive prompt for the generation"}),
                "size": (SEEDREAM_V47_SIZES, {"default": "2048*2048", "tooltip": "Output image size WIDTH*HEIGHT"}),
            },
            "optional": {
                "prompt_expansion_mode": (
                    ["standard", "fast"],
                    {"default": "standard", "tooltip": "'standard' favours quality; 'fast' lowers latency"},
                ),
                "enable_base64_output": ("BOOLEAN", {"default": False, "tooltip": "Return base64 instead of URL if supported"}),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"}),
                "timeout_sec": ("INT", {"default": 300, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        prompt: str,
        size: str = "2048*2048",
        prompt_expansion_mode: str = "standard",
        enable_base64_output: bool = False,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 300,
    ) -> Tuple[str, str]:
        p = (prompt or "").strip()
        if not p:
            raise RuntimeError("prompt is required")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "bytedance/seedream-v4.7/text-to-image",
            "prompt": p,
            "size": str(size).strip(),
            "prompt_expansion_mode": prompt_expansion_mode,
            "enable_base64_output": bool(enable_base64_output),
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
