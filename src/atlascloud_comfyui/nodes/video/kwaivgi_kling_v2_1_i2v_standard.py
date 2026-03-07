from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasKwaivgiKlingV21I2VStandard:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {'atlas_client': ('ATLAS_CLIENT',), 'prompt': ('STRING', {'multiline': True, 'tooltip': 'Text prompt'}), 'image': ('STRING', {'default': '', 'tooltip': 'Input image URL/base64'})},
            "optional": {'negative_prompt': ('STRING', {'multiline': True, 'default': '', 'tooltip': 'Negative prompt'}), 'duration': ([5, 10], {'default': 5, 'tooltip': 'Duration (seconds)'}), 'poll_interval_sec': ('FLOAT', {'default': 2.0, 'min': 0.5, 'max': 10.0, 'tooltip': 'Polling interval (seconds)'}), 'timeout_sec': ('INT', {'default': 900, 'min': 30, 'max': 7200, 'tooltip': 'Timeout (seconds)'})},
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        prompt: str,
        image: str,
        negative_prompt: str = "",
        duration: int = 5,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        client = atlas_client.client

        image = (image or '').strip()
        if not image:
            raise RuntimeError('image is required (URL or base64)')

        payload: Dict[str, Any] = {
            'model': 'kwaivgi/kling-v2.1-i2v-standard',
            'prompt': prompt,
            'duration': int(duration),
            'image': image,
        }

        neg = (negative_prompt or '').strip()
        if neg:
            payload['negative_prompt'] = neg

        prediction_id = client.generate_video(payload)
        result = client.poll_prediction(prediction_id, poll_interval_sec=poll_interval_sec, timeout_sec=float(timeout_sec))

        outputs = (result.get('data') or {}).get('outputs') or []
        if not outputs:
            raise RuntimeError(f'No outputs returned for prediction {prediction_id}: {result}')

        first = outputs[0]
        if not isinstance(first, str):
            raise RuntimeError(f'Unexpected output type for prediction {prediction_id}: {type(first).__name__} {first!r}')

        return (first, prediction_id)
