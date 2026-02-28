from __future__ import annotations


class AtlasBytedanceSeedanceV1LiteT2v720p:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("video_url",)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT", {"tooltip": "Connect from 'AtlasCloud Client' node"}),
                "prompt": ("STRING", {"multiline": True, "default": "", "tooltip": "Text prompt for video generation; Positive text prompt; Cannot exceed 2000 characters."}),
                "duration": ([5, 10], {"default": 5, "tooltip": "The duration of the generated media in seconds."}),
                "aspect_ratio": (['21:9', '16:9', '4:3', '1:1', '3:4', '9:16'], {"default": '16:9', "tooltip": "The aspect ratio of the generated video."}),
            },
            "optional": {
                "seed": ("INT", {"default": -1, "min": -1, "max": 2147483647, "tooltip": "The random seed to use for the generation. -1 means a random seed will be used."}),
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
        seed: int = -1,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ):
        client = getattr(atlas_client, "client", None)
        if client is None:
            raise RuntimeError("Invalid ATLAS_CLIENT handle: missing `.client`")

        payload = {
            "model": "bytedance/seedance-v1-lite-t2v-720p",
            "prompt": prompt,
            "duration": int(duration),
            "aspect_ratio": aspect_ratio,
            "seed": seed if seed >= 0 else None,
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


NODE_CLASS_MAPPINGS = {"AtlasCloud Seedance v1 Lite t2v 720p": AtlasBytedanceSeedanceV1LiteT2v720p}
NODE_DISPLAY_NAME_MAPPINGS = {"AtlasCloud Seedance v1 Lite t2v 720p": "AtlasCloud Seedance v1 Lite t2v 720p"}
