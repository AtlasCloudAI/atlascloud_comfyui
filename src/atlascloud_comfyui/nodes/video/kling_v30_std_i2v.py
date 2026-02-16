from __future__ import annotations

from typing import Any, Dict, Tuple


def _require_http_url(url: str, field_name: str) -> str:
    s = (url or "").strip()
    if not s:
        raise RuntimeError(f"{field_name} is required")
    if not (s.startswith("http://") or s.startswith("https://")):
        raise RuntimeError(f"{field_name} must start with http:// or https://")
    return s


class AtlasKlingV30StdImageToVideo:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("video_url",)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT", {"tooltip": "Connect from 'AtlasCloud Client (API Key/Base URL)' node"}),
                "image_url": ("STRING", {"default": "", "tooltip": "Start image URL (http/https)."}),
                "prompt": ("STRING", {"default": "", "multiline": True, "tooltip": "Prompt"}),
                "duration": ([5, 10], {"default": 5, "tooltip": "Duration (seconds)"}),
                "cfg_scale": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.01, "tooltip": "CFG scale"}),
                "sound": ("BOOLEAN", {"default": False, "tooltip": "Generate sound/audio (if supported)"}),
            },
            "optional": {
                "end_image_url": ("STRING", {"default": "", "tooltip": "Optional end image URL (http/https)."}),
                "negative_prompt": ("STRING", {"default": "", "multiline": True, "tooltip": "Negative prompt (optional)"}),
                "timeout_sec": ("INT", {"default": 900, "min": 30, "max": 7200, "tooltip": "Polling timeout (seconds)"}),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client,
        image_url: str,
        prompt: str,
        duration: int,
        cfg_scale: float,
        sound: bool,
        end_image_url: str = "",
        negative_prompt: str = "",
        timeout_sec: int = 900,
        poll_interval_sec: float = 2.0,
    ) -> Tuple[str]:
        client = getattr(atlas_client, "client", None)
        if client is None:
            raise RuntimeError("Invalid ATLAS_CLIENT handle: missing `.client`")

        prompt = (prompt or "").strip()
        if not prompt:
            raise RuntimeError("prompt is required")

        image_url = _require_http_url(image_url, "image_url")

        payload: Dict[str, Any] = {
            "model": "kwaivgi/kling-v3.0-std/image-to-video",
            "cfg_scale": float(cfg_scale),
            "duration": int(duration),
            "image": image_url,
            "prompt": prompt,
            "sound": bool(sound),
        }

        neg = (negative_prompt or "").strip()
        if neg:
            payload["negative_prompt"] = neg

        endu = (end_image_url or "").strip()
        if endu:
            payload["end_image"] = _require_http_url(endu, "end_image_url")

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


NODE_CLASS_MAPPINGS = {"AtlasCloud Kling V3.0 Std Image-to-Video": AtlasKlingV30StdImageToVideo}
NODE_DISPLAY_NAME_MAPPINGS = {"AtlasCloud Kling V3.0 Std Image-to-Video": "AtlasCloud Kling V3.0 Std Image-to-Video"}
