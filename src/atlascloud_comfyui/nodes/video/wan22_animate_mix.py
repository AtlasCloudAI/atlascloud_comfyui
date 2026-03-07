from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasWan22AnimateMix:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {'atlas_client': ('ATLAS_CLIENT',), 'image': ('STRING', {'default': '', 'tooltip': 'Input image URL/base64'}), 'video': ('STRING', {'default': '', 'tooltip': 'Reference/input video URL'}), 'mode': (['wan-std', 'wan-pro'], {'default': 'wan-pro', 'tooltip': 'Mode'})},
            "optional": {'poll_interval_sec': ('FLOAT', {'default': 2.0, 'min': 0.5, 'max': 10.0, 'tooltip': 'Polling interval (seconds)'}), 'timeout_sec': ('INT', {'default': 900, 'min': 30, 'max': 7200, 'tooltip': 'Timeout (seconds)'})},
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        image: str,
        video: str,
        mode: str,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        client = atlas_client.client

        image = (image or '').strip()
        if not image:
            raise RuntimeError('image is required (URL or base64)')

        video = (video or '').strip()
        if not video:
            raise RuntimeError('video is required (URL)')

        payload: Dict[str, Any] = {
            'model': 'alibaba/wan-2.2/animate-mix',
            'mode': mode,
            'image': image,
            'video': video,
        }

        prediction_id = client.generate_video(payload)
        result = client.poll_prediction(prediction_id, poll_interval_sec=poll_interval_sec, timeout_sec=float(timeout_sec))

        outputs = (result.get('data') or {}).get('outputs') or []
        if not outputs:
            raise RuntimeError(f'No outputs returned for prediction {prediction_id}: {result}')

        first = outputs[0]
        if not isinstance(first, str):
            raise RuntimeError(f'Unexpected output type for prediction {prediction_id}: {type(first).__name__} {first!r}')

        return (first, prediction_id)
