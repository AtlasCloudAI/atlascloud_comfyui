from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasIdeogramV4QualityTextToImage:
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
                    {"default": "landscape_16_9", "tooltip": "Output image resolution preset"},
                ),
                "output_format": (["jpeg", "png"], {"default": "jpeg", "tooltip": "Output image file format"}),
            },
            "optional": {
                "randomize_seed": ("BOOLEAN", {"default": True, "tooltip": "开启后每次生成随机结果；关闭后使用下方固定 seed"}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 2**31 - 1, "tooltip": "固定 seed（仅在随机开关关闭时生效）"}),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"}),
                "timeout_sec": ("INT", {"default": 300, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        prompt: str,
        image_size: str,
        output_format: str,
        randomize_seed: bool = True,
        seed: int = 0,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 300,
    ) -> Tuple[str, str]:
        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "ideogram/v4/quality/text-to-image",
            "prompt": prompt,
            "image_size": image_size,
            "output_format": output_format,
        }

        if not randomize_seed:
            payload["seed"] = seed

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
