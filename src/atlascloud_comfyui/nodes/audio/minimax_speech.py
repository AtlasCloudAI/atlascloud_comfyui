from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle
from ..utils.audio_output import SEED_INPUT, generate_audio_outputs, load_audio_url

_VOICES = [
    "English_expressive_narrator",
    "English_radiant_girl",
    "English_magnetic_voiced_man",
    "English_compelling_lady1",
    "English_Aussie_Bloke",
    "English_captivating_female1",
    "English_Upbeat_Woman",
    "English_Trustworth_Man",
    "English_CalmWoman",
    "English_UpsetGirl",
    "English_Gentle-voiced_man",
    "English_Whispering_girl",
    "English_Diligent_Man",
    "English_Graceful_Lady",
    "English_ReservedYoungMan",
]
_LANGUAGES = [
    "auto",
    "English",
    "Chinese",
    "Chinese,Yue",
    "Japanese",
    "Korean",
    "Spanish",
    "French",
    "Portuguese",
    "German",
    "Italian",
    "Arabic",
    "Russian",
    "Turkish",
    "Dutch",
    "Ukrainian",
    "Vietnamese",
    "Indonesian",
    "Thai",
    "Polish",
    "Romanian",
    "Greek",
    "Czech",
    "Finnish",
    "Hindi",
    "Bulgarian",
    "Danish",
    "Hebrew",
    "Malay",
    "Persian",
    "Slovak",
    "Swedish",
    "Croatian",
    "Filipino",
    "Hungarian",
    "Norwegian",
    "Slovenian",
    "Catalan",
    "Nynorsk",
    "Tamil",
    "Afrikaans",
]


class AtlasMiniMaxSpeech:
    CATEGORY = "AtlasCloud/Audio"
    FUNCTION = "run"
    RETURN_TYPES = ("AUDIO", "STRING", "STRING")
    RETURN_NAMES = ("audio", "audio_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "model": (
                    ["speech-2.8-hd", "speech-2.8-turbo", "speech-2.6-hd", "speech-2.6-turbo"],
                    {"default": "speech-2.8-hd", "tooltip": "MiniMax speech model"},
                ),
                "text": (
                    "STRING",
                    {"multiline": True, "default": "", "tooltip": "Text to speak; 2.8 supports tags such as (laughs)"},
                ),
                "voice": (_VOICES, {"default": "English_expressive_narrator", "tooltip": "Voice"}),
                "seed": SEED_INPUT,
            },
            "optional": {
                "speed": ("FLOAT", {"default": 1.0, "min": 0.5, "max": 2.0, "step": 0.05, "tooltip": "Speech speed"}),
                "vol": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 10.0, "step": 0.1, "tooltip": "Volume"}),
                "pitch": ("INT", {"default": 0, "min": -12, "max": 12, "tooltip": "Pitch (semitones)"}),
                "emotion": (
                    ["auto", "happy", "sad", "angry", "fearful", "disgusted", "surprised", "calm", "fluent", "neutral"],
                    {"default": "auto", "tooltip": "Emotion (fluent / neutral are 2.6 only)"},
                ),
                "language_boost": (_LANGUAGES, {"default": "auto", "tooltip": "Language hint"}),
                "output_format": (["mp3", "wav", "flac"], {"default": "mp3", "tooltip": "Output audio format"}),
                "sample_rate": ([8000, 16000, 22050, 24000, 32000, 44100], {"default": 32000, "tooltip": "Sample rate (Hz)"}),
                "bitrate": ([32000, 64000, 128000, 256000], {"default": 128000, "tooltip": "Bitrate (bps)"}),
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
        speed: float = 1.0,
        vol: float = 1.0,
        pitch: int = 0,
        emotion: str = "auto",
        language_boost: str = "auto",
        output_format: str = "mp3",
        sample_rate: int = 32000,
        bitrate: int = 128000,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 300,
    ) -> Tuple[Dict[str, Any], str, str]:
        text = (text or "").strip()
        if not text:
            raise RuntimeError("text is required for AtlasCloud MiniMax Speech")

        payload: Dict[str, Any] = {
            "model": f"minimax/{model}",
            "text": text,
            "voice": voice,
            "speed": float(speed),
            "vol": float(vol),
            "pitch": int(pitch),
            "emotion": emotion,
            "language_boost": language_boost,
            "sample_rate": int(sample_rate),
            "bitrate": int(bitrate),
        }
        # 2.6 names the format field "format"; 2.8 uses "output_format".
        payload["format" if model.startswith("speech-2.6") else "output_format"] = output_format

        outputs, prediction_id = generate_audio_outputs(atlas_client, payload, poll_interval_sec=poll_interval_sec, timeout_sec=timeout_sec)
        return (load_audio_url(outputs[0]), outputs[0], prediction_id)
