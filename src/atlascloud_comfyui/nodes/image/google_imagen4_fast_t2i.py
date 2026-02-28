from __future__ import annotations


class AtlasGoogleImagen4Fast:
    CATEGORY = "AtlasCloud/Image"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("image_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT", {"tooltip": "Connect from 'AtlasCloud Client' node"}),
                "prompt": ("STRING", {"multiline": True, "default": "", "tooltip": "The positive prompt for image generation."}),
                "aspect_ratio": (['1:1', '16:9', '9:16', '4:3', '3:4'], {"default": '1:1', "tooltip": "The aspect ratio of the generated image."}),
            },
            "optional": {
                "seed": ("INT", {"default": -1, "min": -1, "max": 2147483647, "tooltip": "The random seed to use for the generation."}),
                "negative_prompt": ("STRING", {"multiline": True, "default": "", "tooltip": "The negative prmpt for generating the output."}),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (s)"}),
                "timeout_sec": ("INT", {"default": 900, "min": 30, "max": 7200, "tooltip": "Timeout (s)"}),
            },
        }

    def run(
        self,
        atlas_client,
        prompt: str,
        aspect_ratio: str,
        seed: int = -1,
        negative_prompt: str = "",
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ):
        client = getattr(atlas_client, "client", None)
        if client is None:
            raise RuntimeError("Invalid ATLAS_CLIENT handle: missing `.client`")

        payload = {
            "model": "google/imagen4-fast",
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
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


NODE_CLASS_MAPPINGS = {"AtlasCloud Imagen4 Fast": AtlasGoogleImagen4Fast}
NODE_DISPLAY_NAME_MAPPINGS = {"AtlasCloud Imagen4 Fast": "AtlasCloud Imagen4 Fast"}
