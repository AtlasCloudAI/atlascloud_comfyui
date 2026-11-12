from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle
from ..utils.audio_output import generate_audio_outputs, load_audio_url

_VOICES = [
    "Adam",
    "Alice",
    "Bella",
    "Bill",
    "Brian",
    "Callum",
    "Charlie",
    "Chris",
    "Daniel",
    "Eric",
    "George",
    "Harry",
    "Jessica",
    "Laura",
    "Liam",
    "Lily",
    "Matilda",
    "River",
    "Roger",
    "Sarah",
    "Will",
]


class AtlasElevenLabsV4TextToSpeech:
    CATEGORY = "AtlasCloud/Audio"
    FUNCTION = "run"
    RETURN_TYPES = ("AUDIO", "STRING", "STRING")
    RETURN_NAMES = ("audio", "audio_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "model": (["v4", "v4-turbo"], {"default": "v4", "tooltip": "ElevenLabs model"}),
                "text": ("STRING", {"multiline": True, "default": "", "tooltip": "Text to speak; supports inline delivery tags"}),
                "voice": (_VOICES, {"default": "Roger", "tooltip": "Preset voice"}),
                "seed": (
                    "INT",
                    {"default": 0, "min": 0, "max": 4294967295, "control_after_generate": True, "tooltip": "Seed"},
                ),
            },
            "optional": {
                "voice_id": ("STRING", {"default": "", "tooltip": "Raw ElevenLabs voice_id (e.g. your cloned voice); overrides voice"}),
                "output_format": (
                    ["mp3_44100_128", "mp3_44100_64", "mp3_22050_32", "opus_48000_128", "wav_44100"],
                    {"default": "mp3_44100_128", "tooltip": "Output audio format"},
                ),
                "stability": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.05, "tooltip": "Voice stability"}),
                "similarity_boost": ("FLOAT", {"default": 0.75, "min": 0.0, "max": 1.0, "step": 0.05, "tooltip": "Similarity boost"}),
                "language_code": ("STRING", {"default": "", "tooltip": "ISO 639-1 code to enforce a language; empty = auto"}),
                "apply_text_normalization": (["auto", "on", "off"], {"default": "auto", "tooltip": "Text normalization"}),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"}),
                "timeout_sec": ("INT", {"default": 300, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        model: str,
        text: str,
        voice: str,
        seed: int,
        voice_id: str = "",
        output_format: str = "mp3_44100_128",
        stability: float = 0.5,
        similarity_boost: float = 0.75,
        language_code: str = "",
        apply_text_normalization: str = "auto",
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 300,
    ) -> Tuple[Dict[str, Any], str, str]:
        text = (text or "").strip()
        if not text:
            raise RuntimeError("text is required for AtlasCloud ElevenLabs v4 Text-to-Speech")

        payload: Dict[str, Any] = {
            "model": f"elevenlabs/{model}/text-to-speech",
            "text": text,
            "voice": (voice_id or "").strip() or voice,
            "output_format": output_format,
            "stability": float(stability),
            "similarity_boost": float(similarity_boost),
            "apply_text_normalization": apply_text_normalization,
            "seed": int(seed),
        }
        if (language_code or "").strip():
            payload["language_code"] = language_code.strip()

        outputs, prediction_id = generate_audio_outputs(atlas_client, payload, poll_interval_sec=poll_interval_sec, timeout_sec=timeout_sec)
        return (load_audio_url(outputs[0]), outputs[0], prediction_id)
