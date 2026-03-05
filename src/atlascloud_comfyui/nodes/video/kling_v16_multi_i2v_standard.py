from __future__ import annotations

from typing import Any, Dict, List, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasKlingV16MultiI2VStandard:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                'atlas_client': ('ATLAS_CLIENT',),
                'prompt': ('STRING', {'multiline': True, 'tooltip': 'The positive prompt for the generation. max length 2500'}),
                'images': ('STRING', {'multiline': True, 'default': '', 'tooltip': 'A list of images to use as style references.'}),
            },
            "optional": {
                'poll_interval_sec': ('FLOAT', {'default': 2.0, 'min': 0.5, 'max': 10.0, 'tooltip': 'Polling interval (seconds)'}),
                'timeout_sec': ('INT', {'default': 900, 'min': 30, 'max': 7200, 'tooltip': 'Timeout (seconds)'}),
                'duration': ([5, 10], {'default': 5, 'tooltip': 'The duration of the generated media in seconds.'}),
                'aspect_ratio': (['1:1', '16:9', '9:16'], {'default': '1:1', 'tooltip': 'The aspect ratio of the generated media.'}),
                'negative_prompt': ('STRING', {'multiline': True, 'default': '', 'tooltip': 'The negative prompt for the generation.'}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        prompt: str,
        images: str,
        duration: int = 5,
        aspect_ratio: str = '1:1',
        negative_prompt: str = "",
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        image_list: List[str] = [v.strip() for v in (images or "").splitlines() if v.strip()]
        if not image_list:
            raise RuntimeError("images is required for AtlasCloud Kling v1.6 Multi I2V Standard (one URL per line)")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "",
            "prompt": prompt,
            "images": image_list,
        }

        if str(duration).strip():
            payload["duration"] = duration

        if str(aspect_ratio).strip():
            payload["aspect_ratio"] = aspect_ratio

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
