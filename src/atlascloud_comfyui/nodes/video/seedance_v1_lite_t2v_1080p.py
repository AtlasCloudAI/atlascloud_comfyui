from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasSeedanceV1LiteT2V1080p:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                'atlas_client': ('ATLAS_CLIENT',),
                'prompt': ('STRING', {'multiline': True, 'tooltip': 'Text prompt for video generation; Positive text prompt; Cannot exceed 2000 characters.'}),
            },
            "optional": {
                'poll_interval_sec': ('FLOAT', {'default': 2.0, 'min': 0.5, 'max': 10.0, 'tooltip': 'Polling interval (seconds)'}),
                'timeout_sec': ('INT', {'default': 900, 'min': 30, 'max': 7200, 'tooltip': 'Timeout (seconds)'}),
                'duration': ('INT', {'default': 5, 'min': 1, 'max': 120, 'tooltip': 'The duration of the generated media in seconds.'}),
                'aspect_ratio': (['21:9', '16:9', '4:3', '1:1', '3:4', '9:16'], {'default': '16:9', 'tooltip': 'The aspect ratio of the generated video.'}),
                'camera_fixed': ('BOOLEAN', {'default': False, 'tooltip': 'Whether to fix the camera position.'}),
                'seed': ('INT', {'default': -1, 'min': -1, 'max': 2147483647, 'tooltip': 'The random seed to use for the generation. -1 means a random seed will be used.'}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        prompt: str,
        duration: int = 5,
        aspect_ratio: str = '16:9',
        camera_fixed: bool = False,
        seed: int = -1,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "bytedance/seedance-v1-lite-t2v-1080p",
            "prompt": prompt,
        }

        if str(duration).strip():
            payload["duration"] = duration

        if str(aspect_ratio).strip():
            payload["aspect_ratio"] = aspect_ratio

        payload["camera_fixed"] = bool(camera_fixed)

        payload["seed"] = int(seed)

        prediction_id = client.generate_video(payload)
        result = client.poll_prediction(prediction_id, poll_interval_sec=float(poll_interval_sec), timeout_sec=float(timeout_sec))

        outputs = (result.get("data") or {}).get("outputs") or []
        if not outputs:
            raise RuntimeError(f"No outputs returned for prediction {prediction_id}: {result}")

        first = outputs[0]
        if not isinstance(first, str):
            raise RuntimeError(f"Unexpected output type for prediction {prediction_id}: {type(first).__name__} {first!r}")

        return (first, prediction_id)
