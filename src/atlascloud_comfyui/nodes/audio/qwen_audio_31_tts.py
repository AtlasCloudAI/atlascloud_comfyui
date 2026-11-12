from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle
from ..utils.audio_output import generate_audio_outputs, load_audio_url

_PLUS_VOICES = ["longanhuan_v3.1", "longanlingxin_v3.1", "longanfengyue_v3.1", "xunanchuan_v3.1"]
_FLASH_ONLY_VOICES = [
    "Emily_v3.1",
    "Luna_v3.1",
    "Eric_v3.1",
    "Luca_v3.1",
    "Abby_v3.1",
    "Annie_v3.1",
    "Ava_v3.1",
    "Beth_v3.1",
    "Betty_v3.1",
    "Cally_v3.1",
    "Cindy_v3.1",
    "Donna_v3.1",
    "Andy_v3.1",
    "Brian_v3.1",
    "David_v3.1",
] + [
    f"qwen-audio-3.1-tts-flash-{name}"
    for name in (
        "zora_bg",
        "linde_nl",
        "hajnal_hu",
        "senin_ro",
        "birk_da",
        "lipa_hr",
        "avgi_el",
        "jitrenka_cs",
        "solglimt_nn",
        "glimma_sv",
        "svar_hi",
        "iskra_sk",
        "aava_fi",
        "sahar_ur",
        "jasna_sr",
        "brisa_es_mx",
        "ausra_lt",
        "rasa_lv",
        "deniz_tr",
        "ava_fa",
        "or_he",
        "ayalguu_mn",
        "zarja_sl",
        "ishiq_az",
        "zorza_pl",
        "alba_ca",
        "romduol_km",
        "aurora_pt_br",
        "dao_lo",
        "tsiskari_ka",
        "lente_af",
        "kiran_ne",
        "zorka_be",
        "nilaav_ml",
        "staer_lb",
        "drita_sq",
        "nila_ta",
        "aruna_si",
        "vennela_te",
        "sade_et",
        "bituon_ceb",
        "vedrina_bs",
        "layaung_my",
        "luys_hy",
        "lumen_la",
        "birta_is",
        "zerniq_mt",
        "nuru_sw",
        "arai_kk",
        "zetwal_crs",
        "zoria_uk",
    )
]


class AtlasQwenAudio31TextToSpeech:
    CATEGORY = "AtlasCloud/Audio"
    FUNCTION = "run"
    RETURN_TYPES = ("AUDIO", "STRING", "STRING")
    RETURN_NAMES = ("audio", "audio_url", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "model": (["flash", "plus"], {"default": "flash", "tooltip": "Qwen-Audio 3.1 TTS tier"}),
                "text": ("STRING", {"multiline": True, "default": "", "tooltip": "Text to speak"}),
                "voice": (
                    _PLUS_VOICES + _FLASH_ONLY_VOICES,
                    {"default": "longanhuan_v3.1", "tooltip": "Voice (plus supports only the first four)"},
                ),
                "seed": ("INT", {"default": 0, "min": 0, "max": 65535, "control_after_generate": True, "tooltip": "Seed"}),
            },
            "optional": {
                "instruction": (
                    "STRING",
                    {"multiline": True, "default": "", "tooltip": "Delivery instruction, e.g. speak softly and slowly"},
                ),
                "language_hint": (
                    ["auto", "zh", "en", "ja", "ko", "fr", "de", "pt", "it", "vi", "id"],
                    {"default": "auto", "tooltip": "Language hint"},
                ),
                "output_format": (["mp3", "wav", "opus"], {"default": "mp3", "tooltip": "Output audio format"}),
                "sample_rate": ([8000, 12000, 16000, 22050, 24000, 44100, 48000], {"default": 22050, "tooltip": "Sample rate (Hz)"}),
                "speed": ("FLOAT", {"default": 1.0, "min": 0.5, "max": 2.0, "step": 0.05, "tooltip": "Speech speed"}),
                "pitch": ("FLOAT", {"default": 1.0, "min": 0.5, "max": 2.0, "step": 0.05, "tooltip": "Pitch"}),
                "volume": ("INT", {"default": 50, "min": 0, "max": 100, "tooltip": "Volume"}),
                "enable_ssml": ("BOOLEAN", {"default": False, "tooltip": "Treat text as SSML"}),
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
        instruction: str = "",
        language_hint: str = "auto",
        output_format: str = "mp3",
        sample_rate: int = 22050,
        speed: float = 1.0,
        pitch: float = 1.0,
        volume: int = 50,
        enable_ssml: bool = False,
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 300,
    ) -> Tuple[Dict[str, Any], str, str]:
        text = (text or "").strip()
        if not text:
            raise RuntimeError("text is required for AtlasCloud Qwen-Audio 3.1 Text-to-Speech")

        payload: Dict[str, Any] = {
            "model": f"alibaba/qwen-audio-3.1-tts-{model}/text-to-speech",
            "text": text,
            "voice": voice,
            "output_format": output_format,
            "sample_rate": int(sample_rate),
            "speed": float(speed),
            "pitch": float(pitch),
            "volume": int(volume),
            "enable_ssml": bool(enable_ssml),
            "seed": int(seed),
        }
        if (instruction or "").strip():
            payload["instruction"] = instruction.strip()
        if language_hint != "auto":
            payload["language_hints"] = [language_hint]

        outputs, prediction_id = generate_audio_outputs(atlas_client, payload, poll_interval_sec=poll_interval_sec, timeout_sec=timeout_sec)
        return (load_audio_url(outputs[0]), outputs[0], prediction_id)
