from __future__ import annotations


class AtlasMinimaxVideo01:
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
                "prompt": ("STRING", {"multiline": True, "default": "", "tooltip": "Generate a description of the video.(Note: Maximum support 2000 characters). 1. Support inserting mirror operation instructions to realize mirror operation control: mirror operation instructions need to be inserted into the lens application position in prompt in the format of [ ]. The standard mirror operation instruction format is [C1,C2,C3], where C represents different types of mirror operation. In order to ensure the effect of mirror operation, it is recommended to combine no more than 3 mirror operation instructions. 2. Support natural language description to realize mirror operation control; using the command internal mirror name will improve the accuracy of mirror operation response. 3. mirror operation instructions and natural language descriptions can be effective at the same time."}),
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
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ):
        client = getattr(atlas_client, "client", None)
        if client is None:
            raise RuntimeError("Invalid ATLAS_CLIENT handle: missing `.client`")

        payload = {
            "model": "minimax/video-01",
            "prompt": prompt,
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


NODE_CLASS_MAPPINGS = {"AtlasCloud Video-01": AtlasMinimaxVideo01}
NODE_DISPLAY_NAME_MAPPINGS = {"AtlasCloud Video-01": "AtlasCloud Video-01"}
