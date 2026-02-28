from __future__ import annotations


class AtlasAlibabaWan22T2v480pLoraUltraFast:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("video_url",)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT", {"tooltip": "Connect from 'AtlasCloud Client' node"}),
                "prompt": ("STRING", {"multiline": True, "default": "", "tooltip": "The prompt for generating the output."}),
                "duration": ([5, 8], {"default": 5, "tooltip": "The duration of the generated media in seconds."}),
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
        seed: int = -1,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ):
        client = getattr(atlas_client, "client", None)
        if client is None:
            raise RuntimeError("Invalid ATLAS_CLIENT handle: missing `.client`")

        payload = {
            "model": "alibaba/wan-2.2/t2v-480p-lora-ultra-fast",
            "prompt": prompt,
            "duration": int(duration),
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


NODE_CLASS_MAPPINGS = {"AtlasCloud Wan-2.2 t2v 480p Lora Ultra Fast": AtlasAlibabaWan22T2v480pLoraUltraFast}
NODE_DISPLAY_NAME_MAPPINGS = {"AtlasCloud Wan-2.2 t2v 480p Lora Ultra Fast": "AtlasCloud Wan-2.2 t2v 480p Lora Ultra Fast"}
