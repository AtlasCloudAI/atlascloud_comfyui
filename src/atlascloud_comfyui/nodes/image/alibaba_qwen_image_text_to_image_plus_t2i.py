from __future__ import annotations


class AtlasAlibabaQwenImageTextToImagePlus:
    CATEGORY = "AtlasCloud/Image"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("image_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT", {"tooltip": "Connect from 'AtlasCloud Client' node"}),
                "prompt": ("STRING", {"multiline": True, "default": "", "tooltip": "The prompt for generating the image."}),
            },
            "optional": {
                "seed": ("INT", {"default": -1, "min": -1, "max": 2147483647, "tooltip": "The random seed to use for the generation. -1 means a random seed will be used."}),
                "negative_prompt": ("STRING", {"multiline": True, "default": "", "tooltip": "Negative prompt for the generation."}),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (s)"}),
                "timeout_sec": ("INT", {"default": 900, "min": 30, "max": 7200, "tooltip": "Timeout (s)"}),
            },
        }

    def run(
        self,
        atlas_client,
        prompt: str,
        seed: int = -1,
        negative_prompt: str = "",
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ):
        client = getattr(atlas_client, "client", None)
        if client is None:
            raise RuntimeError("Invalid ATLAS_CLIENT handle: missing `.client`")

        payload = {
            "model": "alibaba/qwen-image/text-to-image-plus",
            "prompt": prompt,
            "seed": seed if seed >= 0 else None,
        }
        neg = (negative_prompt or "").strip()
        if neg:
            payload["negative_prompt"] = neg

        prediction_id = client.generate_image(payload)
        result = client.poll_prediction(
            prediction_id,
            poll_interval_sec=float(poll_interval_sec),
            timeout_sec=float(timeout_sec),
        )

        outputs = (result.get("data") or {}).get("outputs") or []
        if not outputs:
            raise RuntimeError(f"No outputs for prediction {prediction_id}: {result}")

        return (outputs[0], prediction_id)


NODE_CLASS_MAPPINGS = {"AtlasCloud Qwen-Image Text-to-image Plus": AtlasAlibabaQwenImageTextToImagePlus}
NODE_DISPLAY_NAME_MAPPINGS = {"AtlasCloud Qwen-Image Text-to-image Plus": "AtlasCloud Qwen-Image Text-to-image Plus"}
