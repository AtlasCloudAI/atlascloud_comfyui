from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasKlingV21I2VMaster:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                'atlas_client': ('ATLAS_CLIENT',),
                'prompt': ('STRING', {'multiline': True, 'tooltip': 'Text prompt for generation; Positive text prompt; Cannot exceed 2500 characters.'}),
                'image': ('STRING', {'default': 'https://static.atlascloud.ai/media/images/1749522950129341275_kHvrnkgd.jpeg', 'tooltip': 'First frame of the video; Supported image formats include.jpg/.jpeg/.png; The image file size cannot exceed 10MB, and the image resolution should not be less than 300*300px.'}),
            },
            "optional": {
                'poll_interval_sec': ('FLOAT', {'default': 2.0, 'min': 0.5, 'max': 10.0, 'tooltip': 'Polling interval (seconds)'}),
                'timeout_sec': ('INT', {'default': 900, 'min': 30, 'max': 7200, 'tooltip': 'Timeout (seconds)'}),
                'duration': (['5', '10'], {'default': '5', 'tooltip': 'The duration of the generated media in seconds.'}),
                'guidance_scale': ('FLOAT', {'default': 0.5, 'min': 0.0, 'max': 1.0, 'step': 0.1, 'tooltip': 'The guidance scale to use for the generation.'}),
                'negative_prompt': ('STRING', {'multiline': True, 'default': 'blur, distort, and low quality', 'tooltip': 'Negative text prompt; Cannot exceed 2500 characters.'}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        prompt: str,
        image: str,
        duration: str = '5',
        guidance_scale: float = 0.5,
        negative_prompt: str = "",
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        image = (image or "").strip()
        if not image:
            raise RuntimeError("image is required for AtlasCloud Kling v2.1 I2V Master")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": 'kwaivgi/kling-v2.1-i2v-master',
            "prompt": prompt,
            "image": image,
        }

        if str(duration).strip():
            payload["duration"] = duration

        payload["guidance_scale"] = float(guidance_scale)

        neg = (negative_prompt or "").strip()
        if neg:
            payload["negative_prompt"] = neg

        prediction_id = client.generate_video(payload)
        result = client.poll_prediction(prediction_id, poll_interval_sec=float(poll_interval_sec), timeout_sec=float(timeout_sec))

        outputs = (result.get("data") or {}).get("outputs") or []
        if not outputs:
            raise RuntimeError(f"No outputs returned for prediction {prediction_id}: {result}")

        first = outputs[0]
        if not isinstance(first, str):
            raise RuntimeError(f"Unexpected output type for prediction {prediction_id}: {type(first).__name__} {first!r}")

        return (first, prediction_id)
