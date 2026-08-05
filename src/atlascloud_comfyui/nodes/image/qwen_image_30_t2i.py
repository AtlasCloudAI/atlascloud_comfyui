from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle

_PROMPT_EXTEND_MODES = ["direct", "agent"]


class AtlasQwenImage30TextToImage:
    CATEGORY = "AtlasCloud/Image"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("image_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "prompt": ("STRING", {"multiline": True, "tooltip": "Text prompt describing the image to generate"}),
            },
            "optional": {
                "size": (
                    "STRING",
                    {
                        "default": "",
                        "tooltip": "Output resolution as width*height (512*512-2048*2048). Leave empty to let the model pick",
                    },
                ),
                "n": ("INT", {"default": 1, "min": 1, "max": 4, "tooltip": "Number of images to generate"}),
                "negative_prompt": (
                    "STRING",
                    {"multiline": True, "default": "", "tooltip": "Content that should NOT appear in the image"},
                ),
                "seed": (
                    "INT",
                    {
                        "default": -1,
                        "min": -1,
                        "max": 2**31 - 1,
                        "tooltip": "Random seed (-1 for random)",
                    },
                ),
                "prompt_extend": (
                    "BOOLEAN",
                    {"default": True, "tooltip": "Enable intelligent prompt rewriting"},
                ),
                "prompt_extend_mode": (
                    _PROMPT_EXTEND_MODES,
                    {"default": "direct", "tooltip": "Prompt rewriting strategy: direct (DPE) or agent (APE)"},
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
        size: str = "",
        n: int = 1,
        negative_prompt: str = "",
        seed: int = -1,
        prompt_extend: bool = True,
        prompt_extend_mode: str = "direct",
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 300,
    ) -> Tuple[str, str]:
        p = (prompt or "").strip()
        if not p:
            raise RuntimeError("prompt is required")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "qwen-image-3.0/text-to-image",
            "prompt": p,
            "n": int(n),
            "prompt_extend": bool(prompt_extend),
            "prompt_extend_mode": prompt_extend_mode,
        }

        sz = (size or "").strip()
        if sz:
            payload["size"] = sz
        neg = (negative_prompt or "").strip()
        if neg:
            payload["negative_prompt"] = neg
        if seed >= 0:
            payload["seed"] = int(seed)

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
