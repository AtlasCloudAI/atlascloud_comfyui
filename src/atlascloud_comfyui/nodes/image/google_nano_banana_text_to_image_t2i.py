from __future__ import annotations


class AtlasGoogleNanoBananaTextToImage:
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
                "aspect_ratio": (['1:1', '3:2', '2:3', '3:4', '4:3', '4:5', '5:4', '9:16', '16:9', '21:9'], {"default": '1:1', "tooltip": "The aspect ratio of the generated media."}),
            },
            "optional": {
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (s)"}),
                "timeout_sec": ("INT", {"default": 900, "min": 30, "max": 7200, "tooltip": "Timeout (s)"}),
            },
        }

    def run(
        self,
        atlas_client,
        prompt: str,
        aspect_ratio: str,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ):
        client = getattr(atlas_client, "client", None)
        if client is None:
            raise RuntimeError("Invalid ATLAS_CLIENT handle: missing `.client`")

        payload = {
            "model": "google/nano-banana/text-to-image",
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
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


NODE_CLASS_MAPPINGS = {"AtlasCloud Nano Banana Text-to-image": AtlasGoogleNanoBananaTextToImage}
NODE_DISPLAY_NAME_MAPPINGS = {"AtlasCloud Nano Banana Text-to-image": "AtlasCloud Nano Banana Text-to-image"}
