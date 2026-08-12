from __future__ import annotations

from typing import Any, Dict, List, Tuple

from ..auth.atlas_client_node import AtlasClientHandle

_DURATIONS = [-1, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]


class AtlasSeedance25ReferenceToVideo:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "reference_images": (
                    "STRING",
                    {"multiline": True, "default": "", "tooltip": "0+ image URLs/base64/asset://, one per line (up to 30)"},
                ),
                "reference_videos": (
                    "STRING",
                    {"multiline": True, "default": "", "tooltip": "0+ video URLs/asset://, one per line (up to 10)"},
                ),
            },
            "optional": {
                "prompt": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": "The character in image 1 dances gracefully to the music",
                        "tooltip": "Prompt (optional). Cite inputs with @Image1 / @Video1 / @Audio1. Video-editing prompts require duration -1",
                    },
                ),
                "reference_audios": (
                    "STRING",
                    {"multiline": True, "default": "", "tooltip": "Reference audio URLs, one per line"},
                ),
                "duration": (
                    "INT",
                    _DURATIONS,
                    {"default": 5, "tooltip": "Duration (seconds), or -1 for auto (required for video-editing mode)"},
                ),
                "resolution": (["480p", "720p"], {"default": "720p", "tooltip": "Resolution"}),
                "ratio": (
                    ["16:9", "4:3", "1:1", "3:4", "9:16", "21:9", "adaptive"],
                    {"default": "adaptive", "tooltip": "Aspect ratio (adaptive = auto)"},
                ),
                "generate_audio": ("BOOLEAN", {"default": True, "tooltip": "Generate audio"}),
                "watermark": ("BOOLEAN", {"default": False, "tooltip": "Add watermark"}),
                "return_last_frame": ("BOOLEAN", {"default": False, "tooltip": "Return last frame (if supported)"}),
                "output_format": (["mp4", "mov"], {"default": "mp4", "tooltip": "Output container format"}),
                "poll_interval_sec": (
                    "FLOAT",
                    {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"},
                ),
                "timeout_sec": (
                    "INT",
                    {"default": 900, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"},
                ),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        reference_images: str,
        reference_videos: str,
        prompt: str = "The character in image 1 dances gracefully to the music",
        reference_audios: str = "",
        duration: int = 5,
        resolution: str = "720p",
        ratio: str = "adaptive",
        generate_audio: bool = True,
        watermark: bool = False,
        return_last_frame: bool = False,
        output_format: str = "mp4",
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        ref_imgs: List[str] = [v.strip() for v in (reference_images or "").splitlines() if v.strip()]
        ref_vids: List[str] = [v.strip() for v in (reference_videos or "").splitlines() if v.strip()]
        if not ref_imgs and not ref_vids:
            raise RuntimeError("Provide at least one reference image or reference video")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "bytedance/seedance-2.5/reference-to-video",
            "duration": int(duration),
            "resolution": resolution,
            "ratio": ratio,
            "generate_audio": bool(generate_audio),
            "watermark": bool(watermark),
            "return_last_frame": bool(return_last_frame),
            "output_format": output_format,
        }

        p = (prompt or "").strip()
        if p:
            payload["prompt"] = p

        ref_auds: List[str] = [v.strip() for v in (reference_audios or "").splitlines() if v.strip()]
        if ref_auds:
            payload["reference_audios"] = ref_auds

        if ref_imgs:
            payload["reference_images"] = ref_imgs
        if ref_vids:
            payload["reference_videos"] = ref_vids

        prediction_id = client.generate_video(payload)
        result = client.poll_prediction(
            prediction_id,
            poll_interval_sec=float(poll_interval_sec),
            timeout_sec=float(timeout_sec),
        )

        outputs = (result.get("data") or {}).get("outputs") or []
        if not outputs:
            raise RuntimeError(f"No outputs returned for prediction {prediction_id}: {result}")

        first = outputs[0]
        if not isinstance(first, str):
            raise RuntimeError(
                f"Unexpected output type for prediction {prediction_id}: {type(first).__name__} {first!r}"
            )

        return (first, prediction_id)
