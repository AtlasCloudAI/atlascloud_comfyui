from __future__ import annotations


class AtlasKwaivgiKlingV25TurboProTextToVideo:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("video_url",)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT", {"tooltip": "Connect from 'AtlasCloud Client' node"}),
                "prompt": ("STRING", {"multiline": True, "default": "", "tooltip": "The positive prompt for the generation. max length 2500"}),
                "duration": ([5, 10], {"default": 5, "tooltip": "The duration of the generated media in seconds."}),
                "aspect_ratio": (['1:1', '9:16', '16:9'], {"default": '16:9', "tooltip": "The aspect ratio of the generated media."}),
            },
            "optional": {
                "negative_prompt": ("STRING", {"multiline": True, "default": "", "tooltip": "The negative prompt for the generation."}),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (s)"}),
                "timeout_sec": ("INT", {"default": 900, "min": 30, "max": 7200, "tooltip": "Timeout (s)"}),
            },
        }

    def run(
        self,
        atlas_client,
        prompt: str,
        duration: int,
        aspect_ratio: str,
        negative_prompt: str = "",
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ):
        client = getattr(atlas_client, "client", None)
        if client is None:
            raise RuntimeError("Invalid ATLAS_CLIENT handle: missing `.client`")

        payload = {
            "model": "kwaivgi/kling-v2.5-turbo-pro/text-to-video",
            "prompt": prompt,
            "duration": int(duration),
            "aspect_ratio": aspect_ratio,
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


NODE_CLASS_MAPPINGS = {"AtlasCloud Kling v2.5 Turbo Pro Text-to-video": AtlasKwaivgiKlingV25TurboProTextToVideo}
NODE_DISPLAY_NAME_MAPPINGS = {"AtlasCloud Kling v2.5 Turbo Pro Text-to-video": "AtlasCloud Kling v2.5 Turbo Pro Text-to-video"}
