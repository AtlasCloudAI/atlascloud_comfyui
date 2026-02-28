from __future__ import annotations


class AtlasKwaivgiKlingV26ProImageToVideo:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("video_url",)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT", {"tooltip": "Connect from 'AtlasCloud Client' node"}),
                "image": ("STRING", {"default": "", "tooltip": "Input image URL or base64"}),
                "prompt": ("STRING", {"multiline": True, "default": "", "tooltip": "The positive prompt for the generation."}),
                "duration": ([5, 10], {"default": 5, "tooltip": "The duration of the generated media in seconds."}),
            },
            "optional": {
                "cfg_scale": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.01, "tooltip": "Flexibility in video generation; The higher the value, the lower the model’s degree of flexibility, and the stronger the relevance to the user’s prompt."}),
                "negative_prompt": ("STRING", {"multiline": True, "default": "", "tooltip": "The negative prompt for the generation."}),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (s)"}),
                "timeout_sec": ("INT", {"default": 900, "min": 30, "max": 7200, "tooltip": "Timeout (s)"}),
            },
        }

    def run(
        self,
        atlas_client,
        image: str,
        prompt: str,
        duration: int,
        cfg_scale: float = 0.5,
        negative_prompt: str = "",
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ):
        client = getattr(atlas_client, "client", None)
        if client is None:
            raise RuntimeError("Invalid ATLAS_CLIENT handle: missing `.client`")

        payload = {
            "model": "kwaivgi/kling-v2.6-pro/image-to-video",
            "prompt": prompt,
            "duration": int(duration),
            "cfg_scale": float(cfg_scale),
        }
        neg = (negative_prompt or "").strip()
        if neg:
            payload["negative_prompt"] = neg

        prediction_id = client.generate_video(payload)
        result = client.poll_prediction(
            prediction_id,
            poll_interval_sec=float(poll_interval_sec),
            timeout_sec=float(timeout_sec),
        )

        outputs = (result.get("data") or {}).get("outputs") or []
        if not outputs:
            raise RuntimeError(f"No outputs for prediction {prediction_id}: {result}")

        return (outputs[0],)


NODE_CLASS_MAPPINGS = {"AtlasCloud Kling v2.6 Pro Image-to-Video": AtlasKwaivgiKlingV26ProImageToVideo}
NODE_DISPLAY_NAME_MAPPINGS = {"AtlasCloud Kling v2.6 Pro Image-to-Video": "AtlasCloud Kling v2.6 Pro Image-to-Video"}
