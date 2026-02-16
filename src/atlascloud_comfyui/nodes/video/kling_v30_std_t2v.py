from __future__ import annotations

from typing import Any, Dict, Tuple


class AtlasKlingV30StdTextToVideo:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("video_url",)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT", {"tooltip": "Connect from 'AtlasCloud Client (API Key/Base URL)' node"}),
                "prompt": ("STRING", {"default": "", "multiline": True, "tooltip": "Text prompt"}),
                "duration": ([5, 10], {"default": 5, "tooltip": "Duration (seconds)"}),
                "aspect_ratio": (["16:9", "9:16", "1:1"], {"default": "16:9", "tooltip": "Aspect ratio"}),
                "cfg_scale": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.01, "tooltip": "Classifier-free guidance scale"}),
                "sound": ("BOOLEAN", {"default": False, "tooltip": "Generate sound track (if supported)"}),
            },
            "optional": {
                "negative_prompt": ("STRING", {"default": "", "multiline": True, "tooltip": "Negative prompt (optional)"}),
                "timeout_sec": ("INT", {"default": 900, "min": 30, "max": 7200, "tooltip": "Polling timeout (seconds)"}),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client,
        prompt: str,
        duration: int,
        aspect_ratio: str,
        cfg_scale: float,
        sound: bool,
        negative_prompt: str = "",
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
            "model": "kwaivgi/kling-v3.0-std/text-to-video",
            "prompt": prompt,
            "duration": int(duration),
            "aspect_ratio": aspect_ratio,
            "cfg_scale": float(cfg_scale),
            "sound": bool(sound),
        }

        neg = (negative_prompt or "").strip()
        if neg:
            payload["negative_prompt"] = neg

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


NODE_CLASS_MAPPINGS = {"AtlasCloud Kling V3.0 Std Text-to-Video": AtlasKlingV30StdTextToVideo}
NODE_DISPLAY_NAME_MAPPINGS = {"AtlasCloud Kling V3.0 Std Text-to-Video": "AtlasCloud Kling V3.0 Std Text-to-Video"}
