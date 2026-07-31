from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle


class AtlasBytePlusVideoUpscaler:
    CATEGORY = "AtlasCloud/Video"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("video_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "video_url": ("STRING", {"default": "", "tooltip": "Public HTTP(S) URL of the source video"}),
            },
            "optional": {
                "tool_version": (
                    ["standard", "professional"],
                    {"default": "standard", "tooltip": "professional = strongest quality, ~10x the cost"},
                ),
                "scene": (
                    ["common", "ugc", "short_series", "aigc", "old_film"],
                    {"default": "common", "tooltip": "Scene template (only effective when tool_version=standard)"},
                ),
                "resolution": (
                    ["240p", "360p", "480p", "540p", "720p", "1080p", "2k", "4k", "8k"],
                    {"default": "1080p", "tooltip": "Target resolution (mutually exclusive with resolution_limit)"},
                ),
                "resolution_limit": (
                    "INT",
                    {
                        "default": 0,
                        "min": 0,
                        "max": 4320,
                        "tooltip": "Short-edge pixel cap [128, 4320]; ignored when resolution is set (0 = unset)",
                    },
                ),
                "bitrate_level": (["low", "medium", "high"], {"default": "medium", "tooltip": "Target bitrate tier"}),
                "fps": (
                    "INT",
                    {"default": 0, "min": 0, "max": 120, "tooltip": "Frame interpolation target [15, 120] (0 = keep source)"},
                ),
                "bit_depth": (
                    [8, 10, 12],
                    {"default": 8, "tooltip": "Color bit depth (only effective when tool_version=professional)"},
                ),
                "poll_interval_sec": (
                    "FLOAT",
                    {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"},
                ),
                "timeout_sec": ("INT", {"default": 900, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        video_url: str,
        tool_version: str = "standard",
        scene: str = "common",
        resolution: str = "1080p",
        resolution_limit: int = 0,
        bitrate_level: str = "medium",
        fps: int = 0,
        bit_depth: int = 8,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 900,
    ) -> Tuple[str, str]:
        vid = (video_url or "").strip()
        if not vid:
            raise RuntimeError("video_url is required for BytePlus Video Upscaler")

        client = atlas_client.client

        payload: Dict[str, Any] = {
            "model": "byteplus/video/upscaler",
            "video_url": vid,
            "tool_version": tool_version,
            "scene": scene,
            "resolution": resolution,
            "bitrate_level": bitrate_level,
            "bit_depth": int(bit_depth),
        }

        if int(resolution_limit) > 0:
            payload["resolution_limit"] = int(resolution_limit)
        if int(fps) > 0:
            payload["fps"] = int(fps)

        prediction_id = client.generate_video(payload)
        result = client.poll_prediction(
            prediction_id,
            poll_interval_sec=float(poll_interval_sec),
            timeout_sec=float(timeout_sec),
        )

        outputs = (result.get("data") or {}).get("outputs") or []
        if not outputs:
            raise RuntimeError(f"No outputs returned for prediction {prediction_id}: {result}")

        return (outputs[0], prediction_id)
