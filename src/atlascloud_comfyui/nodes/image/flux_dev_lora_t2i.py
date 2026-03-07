from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasFluxDevLoraTextToImage:
    CATEGORY = "AtlasCloud/Image"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("image_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {'atlas_client': ('ATLAS_CLIENT',), 'prompt': ('STRING', {'multiline': True, 'tooltip': 'Text prompt'}), 'image': ('STRING', {'default': '', 'tooltip': 'Input image URL/base64'}), 'size': ('STRING', {'default': '1024*1024', 'tooltip': 'Output size (WIDTH*HEIGHT)'})},
            "optional": {'num_images': ('INT', {'default': 1, 'min': 1, 'max': 4, 'tooltip': 'Number of images'}), 'strength': ('FLOAT', {'default': 0.8, 'min': 0.0, 'max': 1.0, 'tooltip': 'Strength (image transform)'}), 'guidance_scale': ('FLOAT', {'default': 3.5, 'min': 0.0, 'max': 20.0, 'tooltip': 'Guidance scale'}), 'mask_image': ('STRING', {'default': '', 'tooltip': 'Mask image URL/base64 (optional)'}), 'seed': ('INT', {'default': -1, 'min': -1, 'max': 2147483647, 'tooltip': 'Random if -1'}), 'loras_json': ('STRING', {'default': '[]', 'multiline': True, 'tooltip': 'JSON array for loras. Example: []'}), 'poll_interval_sec': ('FLOAT', {'default': 2.0, 'min': 0.5, 'max': 10.0, 'tooltip': 'Polling interval (seconds)'}), 'timeout_sec': ('INT', {'default': 300, 'min': 30, 'max': 7200, 'tooltip': 'Timeout (seconds)'})},
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        prompt: str,
        image: str,
        size: str,
        num_images: int = 1,
        strength: float = 0.8,
        mask_image: str = "",
        guidance_scale: float = 3.5,
        seed: int = -1,
        loras_json: str = "[]",
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 300,
    ) -> Tuple[str, str]:
        client = atlas_client.client

        p = (prompt or '').strip()
        if not p:
            raise RuntimeError('prompt is required')

        image = (image or '').strip()
        if not image:
            raise RuntimeError('image is required (URL or base64)')

        import json
        try:
            loras = json.loads(loras_json) if (loras_json or '').strip() else []
            if not isinstance(loras, list):
                raise ValueError('loras_json must be a JSON array')
        except Exception as e:
            raise RuntimeError(f'Invalid loras_json. Must be a JSON array. Error: {e}') from e

        payload: Dict[str, Any] = {
            'model': 'black-forest-labs/flux-dev-lora',
            'prompt': p,
            'image': image,
            'size': size,
            'num_images': int(num_images),
            'strength': float(strength),
            'mask_image': (mask_image or '').strip(),
            'guidance_scale': float(guidance_scale),
            'seed': int(seed),
            'loras': loras,
        }

        if not (payload.get('mask_image') or '').strip():
            payload.pop('mask_image', None)

        prediction_id = client.generate_image(payload)
        result = client.poll_prediction(prediction_id, poll_interval_sec=poll_interval_sec, timeout_sec=float(timeout_sec))

        outputs = (result.get('data') or {}).get('outputs') or []
        if not outputs:
            raise RuntimeError(f'No outputs returned for prediction {prediction_id}: {result}')

        first = outputs[0]
        if isinstance(first, dict):
            url = first.get('url') or first.get('image') or first.get('output')
            if isinstance(url, str) and url.strip():
                return (url, prediction_id)
            raise RuntimeError(f'Unexpected output object for prediction {prediction_id}: {first}')

        if not isinstance(first, str):
            raise RuntimeError(f'Unexpected output type for prediction {prediction_id}: {type(first).__name__} {first!r}')

        return (first, prediction_id)
