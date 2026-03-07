from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasAtlascloudVan25ImageToVideo:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {'atlas_client': ('ATLAS_CLIENT',), 'prompt': ('STRING', {'multiline': True, 'tooltip': 'Text prompt'}), 'image': ('STRING', {'default': '', 'tooltip': 'Input image URL/base64'}), 'resolution': (['720p', '1080p'], {'default': '720p', 'tooltip': 'Resolution'})},
            "optional": {'negative_prompt': ('STRING', {'multiline': True, 'default': '', 'tooltip': 'Negative prompt'}), 'duration': ([5, 10], {'default': 5, 'tooltip': 'Duration (seconds)'}), 'audio': ('STRING', {'default': '', 'tooltip': 'Audio URL (optional)'}), 'enable_prompt_expansion': ('BOOLEAN', {'default': False, 'tooltip': 'Enable prompt expansion'}), 'seed': ('INT', {'default': -1, 'min': -1, 'max': 2147483647, 'tooltip': 'Random if -1'}), 'poll_interval_sec': ('FLOAT', {'default': 2.0, 'min': 0.5, 'max': 10.0, 'tooltip': 'Polling interval (seconds)'}), 'timeout_sec': ('INT', {'default': 900, 'min': 30, 'max': 7200, 'tooltip': 'Timeout (seconds)'})},
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        prompt: str,
        image: str,
        resolution: str,
        negative_prompt: str = "",
        duration: int = 5,
        audio: str = "",
        enable_prompt_expansion: bool = False,
        seed: int = -1,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        client = atlas_client.client

        image = (image or '').strip()
        if not image:
            raise RuntimeError('image is required (URL or base64)')

        payload: Dict[str, Any] = {
            'model': 'atlascloud/van-2.5/image-to-video',
            'prompt': prompt,
            'resolution': resolution,
            'duration': int(duration),
            'enable_prompt_expansion': bool(enable_prompt_expansion),
            'seed': int(seed),
            'image': image,
        }

        neg = (negative_prompt or '').strip()
        if neg:
            payload['negative_prompt'] = neg

        a = (audio or '').strip()
        if a:
            payload['audio'] = a

        prediction_id = client.generate_video(payload)
        result = client.poll_prediction(prediction_id, poll_interval_sec=poll_interval_sec, timeout_sec=float(timeout_sec))

        outputs = (result.get('data') or {}).get('outputs') or []
        if not outputs:
            raise RuntimeError(f'No outputs returned for prediction {prediction_id}: {result}')

        first = outputs[0]
        if not isinstance(first, str):
            raise RuntimeError(f'Unexpected output type for prediction {prediction_id}: {type(first).__name__} {first!r}')

        return (first, prediction_id)
