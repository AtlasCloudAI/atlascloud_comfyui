from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasFluxKontextDevLoraEdit:
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
                "image": ("STRING", {"default": "", "tooltip": "Input image URL/base64"}),
                "size": ("STRING", {"default": "1024*1024", "tooltip": "Output size (WIDTH*HEIGHT)"}),
            },
            "optional": {
                "num_images": ("INT", {"default": 1, "min": 1, "max": 4, "tooltip": "Number of images"}),
                "num_inference_steps": ("INT", {"default": 28, "min": 1, "max": 50, "tooltip": "Inference steps"}),
                "guidance_scale": ("FLOAT", {"default": 2.5, "min": 0.0, "max": 20.0, "tooltip": "Guidance scale"}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2**31 - 1, "tooltip": "Random if -1"}),
                "loras_json": (
                    "STRING",
                    {
                        "default": "[]",
                        "multiline": True,
                        "tooltip": 'JSON array for loras. Example: [{"path":"https://.../lora.safetensors","scale":1.0}]',
                    },
                ),
                "enable_base64_output": ("BOOLEAN", {"default": False, "tooltip": "Return base64 instead of URL if supported"}),
                "enable_sync_mode": ("BOOLEAN", {"default": False, "tooltip": "If true, server may try to return result synchronously"}),
                "output_format": (["png", "jpeg"], {"default": "png", "tooltip": "Output image format"}),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"}),
                "timeout_sec": ("INT", {"default": 300, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        prompt: str,
        image: str,
        size: str,
        num_images: int = 1,
        num_inference_steps: int = 28,
        guidance_scale: float = 2.5,
        seed: int = -1,
        loras_json: str = "[]",
        enable_base64_output: bool = False,
        enable_sync_mode: bool = False,
        output_format: str = "png",
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 300,
    ) -> Tuple[str, str]:
        client = atlas_client.client

        p = (prompt or "").strip()
        if not p:
            raise RuntimeError("prompt is required")

        img = (image or "").strip()
        if not img:
            raise RuntimeError("image is required (URL or base64)")

        import json

        try:
            loras = json.loads(loras_json) if (loras_json or "").strip() else []
            if not isinstance(loras, list):
                raise ValueError("loras_json must be a JSON array")
        except Exception as e:
            raise RuntimeError(f"Invalid loras_json. Must be a JSON array. Error: {e}") from e

        payload: Dict[str, Any] = {
            "model": "black-forest-labs/flux-kontext-dev-lora",
            "prompt": p,
            "image": img,
            "size": str(size).strip(),
            "num_images": int(num_images),
            "num_inference_steps": int(num_inference_steps),
            "guidance_scale": float(guidance_scale),
            "seed": int(seed),
            "loras": loras,
            "enable_base64_output": bool(enable_base64_output),
            "enable_sync_mode": bool(enable_sync_mode),
            "output_format": output_format,
        }

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
