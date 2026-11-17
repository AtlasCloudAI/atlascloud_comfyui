from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle
from ..utils.audio_output import SEED_INPUT, generate_audio_outputs, load_audio_url

# v3 takes voice ids; the names match the v4 presets.
_VOICE_IDS = {
    "Adam": "pNInz6obpgDQGcFmaJgB",
    "Alice": "Xb7hH8MSUJpSbSDYk0k2",
    "Bella": "hpp4J3VqNfWAUOO0d1Us",
    "Bill": "pqHfZKP75CvOlQylNhV4",
    "Brian": "nPczCjzI2devNBz1zQrb",
    "Callum": "N2lVS1w4EtoT3dr4eOWO",
    "Charlie": "IKne3meq5aSn9XLyUdCD",
    "Chris": "iP95p4xoKVk53GoZ742B",
    "Daniel": "onwK4e9ZLuTAKqWW03F9",
    "Eric": "cjVigY5qzO86Huf0OWal",
    "George": "JBFqnCBsd6RMkjVDRZzb",
    "Harry": "SOYHLrjzK2X1ezoPC6cr",
    "Jessica": "cgSgspJ2msm6clMCkdW9",
    "Laura": "FGY2WhTYpPnrIDTdsKH5",
    "Liam": "TX3LPaxmHKxFdv7VOQHJ",
    "Lily": "pFZP5JQG7iQjIQuC4Bku",
    "Matilda": "XrExE9yKIg1WjnnlVkGX",
    "River": "SAz9YHcvj6GT2YYXdXww",
    "Roger": "CwhRBWXzGAHq8TQ4Fs17",
    "Sarah": "EXAVITQu4vr4xnSDxMaL",
    "Will": "bIHbv24MWmeRgasZH58o",
}


class AtlasElevenLabsV3TextToSpeech:
    CATEGORY = "AtlasCloud/Audio"
    FUNCTION = "run"
    RETURN_TYPES = ("AUDIO", "STRING", "STRING")
    RETURN_NAMES = ("audio", "audio_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "text": ("STRING", {"multiline": True, "default": "", "tooltip": "Text to speak; supports audio tags such as [whispers]"}),
                "voice": (list(_VOICE_IDS), {"default": "Bella", "tooltip": "Preset voice"}),
                "seed": SEED_INPUT,
            },
            "optional": {
                "stability": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.05, "tooltip": "Voice stability"}),
                "language_code": ("STRING", {"default": "", "tooltip": "ISO 639-1 code to enforce a language; empty = auto"}),
                "apply_text_normalization": (["auto", "on", "off"], {"default": "auto", "tooltip": "Text normalization"}),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"}),
                "timeout_sec": ("INT", {"default": 300, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        text: str,
        voice: str,
        seed: int,
        stability: float = 0.5,
        language_code: str = "",
        apply_text_normalization: str = "auto",
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 300,
    ) -> Tuple[Dict[str, Any], str, str]:
        text = (text or "").strip()
        if not text:
            raise RuntimeError("text is required for AtlasCloud ElevenLabs v3 Text-to-Speech")

        payload: Dict[str, Any] = {
            "model": "elevenlabs/v3/text-to-speech",
            "text": text,
            "voice": _VOICE_IDS[voice],
            "stability": float(stability),
            "apply_text_normalization": apply_text_normalization,
        }
        if (language_code or "").strip():
            payload["language_code"] = language_code.strip()

        outputs, prediction_id = generate_audio_outputs(atlas_client, payload, poll_interval_sec=poll_interval_sec, timeout_sec=timeout_sec)
        return (load_audio_url(outputs[0]), outputs[0], prediction_id)
