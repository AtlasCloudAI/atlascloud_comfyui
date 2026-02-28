from __future__ import annotations


class AtlasBlackForestLabsFluxKontextMaxTextToImage:
    CATEGORY = "AtlasCloud/Image"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("image_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT", {"tooltip": "Connect from 'AtlasCloud Client' node"}),
                "prompt": ("STRING", {"multiline": True, "default": "", "tooltip": "The prompt to generate an image from."}),
                "aspect_ratio": (['21:9', '16:9', '4:3', '3:2', '1:1', '2:3', '3:4', '9:16', '9:21'], {"default": '1:1', "tooltip": "The aspect ratio of the generated image."}),
            },
            "optional": {
                "seed": ("INT", {"default": -1, "min": -1, "max": 2147483647, "tooltip": "
            The same seed and the same prompt given to the same version of the model
            will output the same image every time.
        "}),
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
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ):
        client = getattr(atlas_client, "client", None)
        if client is None:
            raise RuntimeError("Invalid ATLAS_CLIENT handle: missing `.client`")

        payload = {
            "model": "black-forest-labs/flux-kontext-max/text-to-image",
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "seed": seed if seed >= 0 else None,
        }

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


NODE_CLASS_MAPPINGS = {"AtlasCloud Flux Kontext Max Text-to-Image": AtlasBlackForestLabsFluxKontextMaxTextToImage}
NODE_DISPLAY_NAME_MAPPINGS = {"AtlasCloud Flux Kontext Max Text-to-Image": "AtlasCloud Flux Kontext Max Text-to-Image"}
