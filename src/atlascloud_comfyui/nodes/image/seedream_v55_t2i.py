from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle

_SIZES = [
    "2048*2048", "2368*1776", "1776*2368", "2816*1584", "1584*2816", "2496*1664", "1664*2496", "3136*1344",
    "1536*1536", "1792*1344", "1344*1792", "2048*1152", "1152*2048", "1872*1248", "1248*1872", "2352*1008",
    "1024*1024", "1152*864", "864*1152", "1424*800", "800*1424", "1248*832", "832*1248", "1568*672",
]


class AtlasSeedreamV55TextToImage:
    CATEGORY = "AtlasCloud/Image"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("image_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "prompt": ("STRING", {"multiline": True, "tooltip": "Text prompt (recommended under 600 English words)"}),
                "seed": (
                    "INT",
                    {
                        "default": 0,
                        "min": 0,
                        "max": 0xFFFFFFFFFFFFFFFF,
                        "control_after_generate": True,
                        "tooltip": "Change to run the node again (not sent to the API)",
                    },
                ),
                "size": (_SIZES, {"default": "2048*2048", "tooltip": "Output image size WIDTH*HEIGHT"}),
                "output_format": (["png", "jpeg"], {"default": "png", "tooltip": "Output image file format"}),
                "background": (["auto", "transparent", "opaque"], {"default": "auto", "tooltip": "Transparent background requires png output"}),
                "enable_base64_output": ("BOOLEAN", {"default": False, "tooltip": "Return base64 instead of URL if supported"}),
            },
            "optional": {
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"}),
                "timeout_sec": ("INT", {"default": 300, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        prompt: str,
        seed: int,
        size: str,
        output_format: str,
        background: str,
        enable_base64_output: bool,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 300,
    ) -> Tuple[str, str]:
        p = (prompt or "").strip()
        if not p:
            raise RuntimeError("prompt is required for Seedream V5.5 Text-to-Image")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "bytedance/seedream-v5.5/text-to-image",
            "prompt": p,
            "size": size,
            "output_format": output_format,
            "background": background,
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
