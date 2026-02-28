from __future__ import annotations


class AtlasLightricksLtx2FastImageToVideo:
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
                "duration": ([6, 8, 10, 12, 14, 16, 18, 20], {"default": 6, "tooltip": "The duration of the generated media in seconds."}),
            },
            "optional": {
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
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ):
        client = getattr(atlas_client, "client", None)
        if client is None:
            raise RuntimeError("Invalid ATLAS_CLIENT handle: missing `.client`")

        payload = {
            "model": "lightricks/ltx-2-fast/image-to-video",
            "prompt": prompt,
            "duration": int(duration),
        }

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


NODE_CLASS_MAPPINGS = {"AtlasCloud Ltx-2 Fast Image-to-video": AtlasLightricksLtx2FastImageToVideo}
NODE_DISPLAY_NAME_MAPPINGS = {"AtlasCloud Ltx-2 Fast Image-to-video": "AtlasCloud Ltx-2 Fast Image-to-video"}
