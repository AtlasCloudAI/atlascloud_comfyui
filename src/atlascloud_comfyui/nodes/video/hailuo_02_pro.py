from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasHailuo02Pro:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                'atlas_client': ('ATLAS_CLIENT',),
                'prompt': ('STRING', {'multiline': True, 'tooltip': 'Generate a description of the video.(Note: Maximum support 2000 characters).'}),
            },
            "optional": {
                'poll_interval_sec': ('FLOAT', {'default': 2.0, 'min': 0.5, 'max': 10.0, 'tooltip': 'Polling interval (seconds)'}),
                'timeout_sec': ('INT', {'default': 900, 'min': 30, 'max': 7200, 'tooltip': 'Timeout (seconds)'}),
                'image': ('STRING', {'default': '', 'tooltip': 'The model generates video with the picture passed in as the first frame.Base64 encoded strings in data:image/jpeg; base64,{data} format for incoming images, or URLs accessible via the public network. The uploaded image needs to meet the following conditions: Format is JPG/JPEG/PNG; The aspect ratio is greater than 2:5 and less than 5:2; Short side pixels greater than 300px; The image file size cannot exceed 20MB.'}),
                'duration': ([6], {'default': 6, 'tooltip': 'The duration of the generated media in seconds.'}),
                'enable_prompt_expansion': ('BOOLEAN', {'default': False, 'tooltip': 'The model automatically optimizes incoming prompts to enhance output quality. This also activates the safety checker, which ensures content safety by detecting and filtering potential risks.'}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        prompt: str,
        image: str = '',
        duration: int = 6,
        enable_prompt_expansion: bool = False,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": 'minimax/hailuo-02/pro',
            "prompt": prompt,
        }

        if (image or "").strip():
            payload["image"] = image

        if str(duration).strip():
            payload["duration"] = duration

        payload["enable_prompt_expansion"] = bool(enable_prompt_expansion)

        prediction_id = client.generate_video(payload)
        result = client.poll_prediction(prediction_id, poll_interval_sec=float(poll_interval_sec), timeout_sec=float(timeout_sec))

        outputs = (result.get("data") or {}).get("outputs") or []
        if not outputs:
            raise RuntimeError(f"No outputs returned for prediction {prediction_id}: {result}")

        first = outputs[0]
        if not isinstance(first, str):
            raise RuntimeError(f"Unexpected output type for prediction {prediction_id}: {type(first).__name__} {first!r}")

        return (first, prediction_id)
