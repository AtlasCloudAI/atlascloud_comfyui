from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle
from ..utils.audio_output import SEED_INPUT, generate_audio_outputs, load_audio_url


class AtlasMiniMaxMusic:
    CATEGORY = "AtlasCloud/Audio"
    FUNCTION = "run"
    RETURN_TYPES = ("AUDIO", "STRING", "STRING")
    RETURN_NAMES = ("audio", "audio_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "model": (["music-3.0", "music-2.6"], {"default": "music-3.0", "tooltip": "MiniMax music model"}),
                "prompt": (
                    "STRING",
                    {"multiline": True, "default": "", "tooltip": "Style, mood and instrumentation (required for music-2.6)"},
                ),
                "lyrics": (
                    "STRING",
                    {"multiline": True, "default": "", "tooltip": "Lyrics with section tags such as [Verse] / [Chorus]"},
                ),
                "seed": SEED_INPUT,
            },
            "optional": {
                "is_instrumental": ("BOOLEAN", {"default": False, "tooltip": "Instrumental only; lyrics are ignored"}),
                "lyrics_optimizer": ("BOOLEAN", {"default": False, "tooltip": "music-3.0 only: write lyrics from the prompt"}),
                "format": (["mp3", "wav"], {"default": "mp3", "tooltip": "Output audio format"}),
                "sample_rate": ([16000, 24000, 32000, 44100], {"default": 44100, "tooltip": "Sample rate (Hz)"}),
                "bitrate": ([32000, 64000, 128000, 256000], {"default": 256000, "tooltip": "Bitrate (bps)"}),
                "poll_interval_sec": ("FLOAT", {"default": 3.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"}),
                "timeout_sec": ("INT", {"default": 900, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        model: str,
        prompt: str,
        lyrics: str,
        seed: int,
        is_instrumental: bool = False,
        lyrics_optimizer: bool = False,
        format: str = "mp3",
        sample_rate: int = 44100,
        bitrate: int = 256000,
        poll_interval_sec: float = 3.0,
        timeout_sec: int = 900,
    ) -> Tuple[Dict[str, Any], str, str]:
        payload: Dict[str, Any] = {
            "model": f"minimax/{model}",
            "prompt": (prompt or "").strip(),
            "lyrics": (lyrics or "").strip(),
            "is_instrumental": bool(is_instrumental),
            "format": format,
            "sample_rate": int(sample_rate),
            "bitrate": int(bitrate),
        }
        if model == "music-3.0":
            payload["lyrics_optimizer"] = bool(lyrics_optimizer)

        outputs, prediction_id = generate_audio_outputs(atlas_client, payload, poll_interval_sec=poll_interval_sec, timeout_sec=timeout_sec)
        return (load_audio_url(outputs[0]), outputs[0], prediction_id)
