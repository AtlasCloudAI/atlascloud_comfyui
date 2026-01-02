from __future__ import annotations

from typing import Any, Dict, Tuple


class AtlasSeedanceV15ProTextToVideo:
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
                "duration": ("INT", {"default": 8, "min": 4, "max": 12, "tooltip": "Duration (seconds)"}),

                "aspect_ratio": (["16:9", "9:16", "1:1", "4:3", "3:4","21:9"], {"default": "16:9", "tooltip": "Aspect ratio"}),
                "resolution": (["720p", "480p"], {"default": "720p", "tooltip": "Output resolution preset"}),

                "camera_fixed": ("BOOLEAN", {"default": False, "tooltip": "If true, camera is fixed"}),
                "generate_audio": ("BOOLEAN", {"default": True, "tooltip": "If true, generate audio track"}),
                "seed": ("INT", {"default": -1, "min": -1, "max": 2147483647, "tooltip": "Seed (-1 for random)"}),
            },
            "optional": {
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
        resolution: str,
        camera_fixed: bool,
        generate_audio: bool,
        seed: int,
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
            "model": "bytedance/seedance-v1.5-pro/text-to-video",
            "prompt": prompt,
            "duration": int(duration),
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
            "camera_fixed": bool(camera_fixed),
            "generate_audio": bool(generate_audio),
            "seed": int(seed),
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


NODE_CLASS_MAPPINGS = {"AtlasCloud Seedance V1.5 Pro Text-to-Video": AtlasSeedanceV15ProTextToVideo}
NODE_DISPLAY_NAME_MAPPINGS = {"AtlasCloud Seedance V1.5 Pro Text-to-Video": "AtlasCloud Seedance V1.5 Pro Text-to-Video"}
