from __future__ import annotations

from typing import Any, Dict, List, Tuple

from ..auth.atlas_client_node import AtlasClientHandle
from ..utils.audio_output import SEED_INPUT, generate_audio_outputs, load_audio_url

_SPEAKERS = [
    "none",
    "zh_female_vv_uranus_bigtts",
    "zh_female_xiaohe_uranus_bigtts",
    "zh_male_m191_uranus_bigtts",
    "zh_male_taocheng_uranus_bigtts",
    "zh_male_liufei_uranus_bigtts",
    "zh_female_sophie_uranus_bigtts",
    "zh_female_qingxinnvsheng_uranus_bigtts",
    "zh_female_cancan_uranus_bigtts",
    "zh_female_tianmeitaozi_uranus_bigtts",
    "zh_male_ruyayichen_uranus_bigtts",
]


class AtlasSeedAudio10:
    CATEGORY = "AtlasCloud/Audio"
    FUNCTION = "run"
    RETURN_TYPES = ("AUDIO", "STRING", "STRING")
    RETURN_NAMES = ("audio", "audio_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "text": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": "A phone vibrates first, then a calm male voice says: Welcome to Seed Audio.",
                        "tooltip": "Describe speech, sound effects and music; cite references as @audio1, @audio2...",
                    },
                ),
                "seed": SEED_INPUT,
            },
            "optional": {
                "speaker": (_SPEAKERS, {"default": "none", "tooltip": "Preset voice reference"}),
                "reference_audios": (
                    "STRING",
                    {"multiline": True, "default": "", "tooltip": "Reference audio URLs, one per line (up to 3)"},
                ),
                "format": (["mp3", "wav", "ogg_opus"], {"default": "mp3", "tooltip": "Output audio format"}),
                "sample_rate": ([8000, 16000, 24000, 32000, 44100, 48000], {"default": 24000, "tooltip": "Sample rate (Hz)"}),
                "pitch_rate": ("INT", {"default": 0, "min": -12, "max": 12, "tooltip": "Pitch shift (semitones)"}),
                "speech_rate": ("INT", {"default": 0, "min": -50, "max": 100, "tooltip": "Speech rate"}),
                "loudness_rate": ("INT", {"default": 0, "min": -50, "max": 100, "tooltip": "Loudness"}),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"}),
                "timeout_sec": ("INT", {"default": 600, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        text: str,
        seed: int,
        speaker: str = "none",
        reference_audios: str = "",
        format: str = "mp3",
        sample_rate: int = 24000,
        pitch_rate: int = 0,
        speech_rate: int = 0,
        loudness_rate: int = 0,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 600,
    ) -> Tuple[Dict[str, Any], str, str]:
        text = (text or "").strip()
        if not text:
            raise RuntimeError("text is required for AtlasCloud Seed Audio 1.0")

        references: List[Dict[str, str]] = []
        if speaker != "none":
            references.append({"speaker": speaker})
        references.extend({"audio_url": v.strip()} for v in (reference_audios or "").splitlines() if v.strip())

        payload: Dict[str, Any] = {
            "model": "bytedance/seed-audio-1.0",
            "text": text,
            "format": format,
            "sample_rate": int(sample_rate),
            "pitch_rate": int(pitch_rate),
            "speech_rate": int(speech_rate),
            "loudness_rate": int(loudness_rate),
        }
        if references:
            payload["references"] = references

        outputs, prediction_id = generate_audio_outputs(atlas_client, payload, poll_interval_sec=poll_interval_sec, timeout_sec=timeout_sec)
        return (load_audio_url(outputs[0]), outputs[0], prediction_id)
