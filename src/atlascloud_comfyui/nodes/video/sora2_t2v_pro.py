from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasSora2TextToVideoPro:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("video_url",)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT", {"tooltip": "AtlasCloud Client from 'AtlasCloud Client' node"}),
                "prompt": ("STRING", {"default": "", "multiline": True, "tooltip": "Text prompt"}),
                "duration": ([4, 8, 12], {"default": 4, "tooltip": "Duration (seconds)"}),
                "size": (["720*1280", "1280*720", "1024*1794", "1794*1024"], {"default": "720*1280", "tooltip": "Resolution (WxH)"}),
            },
            "optional": {
                "timeout_sec": ("INT", {"default": 900, "min": 30, "max": 7200, "tooltip": "Polling timeout (seconds)"}),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        prompt: str,
        duration: int,
        size: str,
        timeout_sec: int = 900,
        poll_interval_sec: float = 2.0,
    ) -> Tuple[str]:
        prompt = (prompt or "").strip()
        if not prompt:
            raise RuntimeError("prompt is required")

        client = getattr(atlas_client, "client", None)
        if client is None:
            raise RuntimeError("Invalid ATLAS_CLIENT handle: missing `.client`")

        payload: Dict[str, Any] = {
            "model": "openai/sora-2/text-to-video-pro",
            "duration": int(duration),
            "prompt": prompt,
            "size": size,
        }

        prediction_id = client.generate_video(payload)
        result = client.poll_prediction(
            prediction_id,
            poll_interval_sec=float(poll_interval_sec),
            timeout_sec=float(timeout_sec),
        )

        outputs = (result.get("data") or {}).get("outputs") or []
        if not outputs:
            raise RuntimeError(f"No outputs in prediction response: {result}")

        return (outputs[0],)
