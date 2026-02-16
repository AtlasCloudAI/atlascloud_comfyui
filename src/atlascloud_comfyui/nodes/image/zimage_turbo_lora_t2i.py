class AtlasZImageTurboLoraTextToImage:
    CATEGORY = "AtlasCloud/Image"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("image_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "prompt": ("STRING", {"multiline": True, "tooltip": "Text prompt"}),
                # ✅ width/height
                "width": ("INT", {"default": 1024, "min": 256, "max": 1536, "step": 64, "tooltip": "Width"}),
                "height": ("INT", {"default": 1024, "min": 256, "max": 1536, "step": 64, "tooltip": "Height"}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2**31 - 1, "tooltip": "Random if -1"}),
                "enable_base64_output": ("BOOLEAN", {"default": False, "tooltip": "Return base64 instead of URL if supported"}),
                "enable_sync_mode": ("BOOLEAN", {"default": False, "tooltip": "If true, server may try to return result synchronously"}),
            },
            "optional": {
                "negative_prompt": ("STRING", {"multiline": True, "default": "", "tooltip": "Negative text prompt"}),
                "loras_json": ("STRING", {"default": "[]", "multiline": True, "tooltip": "JSON array for loras. Example: []"}),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"}),
                "timeout_sec": ("INT", {"default": 300, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client,
        prompt: str,
        width: int,
        height: int,
        seed: int,
        enable_base64_output: bool,
        enable_sync_mode: bool,
        negative_prompt: str = "",
        loras_json: str = "[]",
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 300,
    ):
        import json

        client = atlas_client.client
        size = f"{width}*{height}"  # ✅ compose for API

        try:
            loras = json.loads(loras_json) if (loras_json or "").strip() else []
            if not isinstance(loras, list):
                raise ValueError("loras_json must be a JSON array")
        except Exception as e:
            raise RuntimeError(f"Invalid loras_json. Must be a JSON array. Error: {e}") from e

        payload = {
            "model": "z-image/turbo-lora",
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "size": size,
            "seed": seed,
            "enable_base64_output": enable_base64_output,
            "enable_sync_mode": enable_sync_mode,
            "loras": loras,
        }

        prediction_id = client.generate_image(payload)
        result = client.poll_prediction(
            prediction_id,
            poll_interval_sec=poll_interval_sec,
            timeout_sec=float(timeout_sec),
        )

        outputs = (result.get("data") or {}).get("outputs") or []
        if not outputs:
            raise RuntimeError(f"No outputs returned for prediction {prediction_id}: {result}")

        return (outputs[0], prediction_id)
