from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasHailuo23Fast:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                'atlas_client': ('ATLAS_CLIENT',),
                'image': ('STRING', {'default': '', 'tooltip': 'The model generates video with the picture passed in as the first frame.Base64 encoded strings in data:image/jpeg; base64,{data} format for incoming images, or URLs accessible via the public network. The uploaded image needs to meet the following conditions: Format is JPG/JPEG/PNG; The aspect ratio is greater than 2:5 and less than 5:2; Short side pixels greater than 300px; The image file size cannot exceed 20MB.'}),
            },
            "optional": {
                'poll_interval_sec': ('FLOAT', {'default': 2.0, 'min': 0.5, 'max': 10.0, 'tooltip': 'Polling interval (seconds)'}),
                'timeout_sec': ('INT', {'default': 900, 'min': 30, 'max': 7200, 'tooltip': 'Timeout (seconds)'}),
                'prompt': ('STRING', {'multiline': True, 'tooltip': 'The positive prompt for the generation.'}),
                'duration': ([6, 10], {'default': 6, 'tooltip': 'The duration of the generated media in seconds.'}),
                'enable_prompt_expansion': ('BOOLEAN', {'default': True, 'tooltip': 'The model automatically optimizes incoming prompts to enhance output quality. This also activates the safety checker, which ensures content safety by detecting and filtering potential risks.'}),
                'go_fast': ('BOOLEAN', {'default': True, 'tooltip': 'Prioritize faster video generation speed with a moderate trade-off in visual quality'}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        image: str,
        prompt: str = '',
        duration: int = 6,
        enable_prompt_expansion: bool = True,
        go_fast: bool = True,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        image = (image or "").strip()
        if not image:
            raise RuntimeError("image is required for AtlasCloud Hailuo-2.3 Fast")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "minimax/hailuo-2.3/fast",
            "image": image,
        }

        if (prompt or "").strip():
            payload["prompt"] = prompt

        if str(duration).strip():
            payload["duration"] = duration

        payload["enable_prompt_expansion"] = bool(enable_prompt_expansion)

        payload["go_fast"] = bool(go_fast)

        prediction_id = client.generate_video(payload)
        result = client.poll_prediction(prediction_id, poll_interval_sec=float(poll_interval_sec), timeout_sec=float(timeout_sec))

        outputs = (result.get("data") or {}).get("outputs") or []
        if not outputs:
            raise RuntimeError(f"No outputs returned for prediction {prediction_id}: {result}")

        first = outputs[0]
        if not isinstance(first, str):
            raise RuntimeError(f"Unexpected output type for prediction {prediction_id}: {type(first).__name__} {first!r}")

        return (first, prediction_id)
