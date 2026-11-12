from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle
from ..utils.audio_output import SEED_INPUT, generate_audio_outputs, load_audio_url

_WEIGHT_TOOLTIP = "Custom mode only; -1 leaves it to the API"


class AtlasSunoV6:
    CATEGORY = "AtlasCloud/Audio"
    FUNCTION = "run"
    RETURN_TYPES = ("AUDIO", "AUDIO", "STRING", "STRING")
    RETURN_NAMES = ("audio", "audio_2", "audio_urls", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "model": (["chirp-v6", "chirp-v6-mini", "chirp-v6-wild"], {"default": "chirp-v6", "tooltip": "Suno model"}),
                "prompt": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": "Late-night city lo-fi piano with the sound of rain",
                        "tooltip": "custom off: a description of the song. custom on: the lyrics ([Verse] / [Chorus] ...)",
                    },
                ),
                "custom": ("BOOLEAN", {"default": False, "tooltip": "Custom mode: prompt is lyrics; title/style/weights apply"}),
                "instrumental": ("BOOLEAN", {"default": False, "tooltip": "No vocals"}),
                "seed": SEED_INPUT,
            },
            "optional": {
                "title": ("STRING", {"default": "", "tooltip": "Song title (custom mode)"}),
                "style": ("STRING", {"default": "", "tooltip": "Style tags, e.g. synthwave, female vocal (custom mode)"}),
                "negative_tags": ("STRING", {"default": "", "tooltip": "Styles to avoid (custom mode)"}),
                "vocal_gender": (["auto", "Male", "Female"], {"default": "auto", "tooltip": "Vocal gender"}),
                "variety": (
                    ["auto", "off", "normal", "high", "extra", "max"],
                    {"default": "auto", "tooltip": "How far the two takes stray from the obvious rendition"},
                ),
                "auto_lyrics": ("BOOLEAN", {"default": False, "tooltip": "Let the model rewrite the lyrics (custom mode)"}),
                "duration": ("INT", {"default": 0, "min": 0, "max": 360, "tooltip": "Seconds (10-360, custom mode); 0 = auto"}),
                "style_weight": ("FLOAT", {"default": -1.0, "min": -1.0, "max": 1.0, "step": 0.05, "tooltip": _WEIGHT_TOOLTIP}),
                "weirdness_constraint": ("FLOAT", {"default": -1.0, "min": -1.0, "max": 1.0, "step": 0.05, "tooltip": _WEIGHT_TOOLTIP}),
                "audio_weight": ("FLOAT", {"default": -1.0, "min": -1.0, "max": 1.0, "step": 0.05, "tooltip": _WEIGHT_TOOLTIP}),
                "persona_id": ("STRING", {"default": "", "tooltip": "Persona (voice identity) id (custom mode)"}),
                "poll_interval_sec": ("FLOAT", {"default": 3.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"}),
                "timeout_sec": ("INT", {"default": 900, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        model: str,
        prompt: str,
        custom: bool,
        instrumental: bool,
        seed: int,
        title: str = "",
        style: str = "",
        negative_tags: str = "",
        vocal_gender: str = "auto",
        variety: str = "auto",
        auto_lyrics: bool = False,
        duration: int = 0,
        style_weight: float = -1.0,
        weirdness_constraint: float = -1.0,
        audio_weight: float = -1.0,
        persona_id: str = "",
        poll_interval_sec: float = 3.0,
        timeout_sec: int = 900,
    ) -> Tuple[Dict[str, Any], Dict[str, Any], str, str]:
        payload: Dict[str, Any] = {
            "model": f"suno/{model}",
            "prompt": (prompt or "").strip(),
            "custom": bool(custom),
            "instrumental": bool(instrumental),
            "auto_lyrics": bool(auto_lyrics),
        }
        for key, value in (("title", title), ("style", style), ("negative_tags", negative_tags), ("persona_id", persona_id)):
            if (value or "").strip():
                payload[key] = value.strip()
        if vocal_gender != "auto":
            payload["vocal_gender"] = vocal_gender
        if variety != "auto":
            payload["variety"] = variety
        if duration > 0:
            payload["duration"] = int(duration)
        for key, value in (("style_weight", style_weight), ("weirdness_constraint", weirdness_constraint), ("audio_weight", audio_weight)):
            if value >= 0:
                payload[key] = float(value)

        outputs, prediction_id = generate_audio_outputs(atlas_client, payload, poll_interval_sec=poll_interval_sec, timeout_sec=timeout_sec)
        # Suno returns two takes per request.
        first = load_audio_url(outputs[0])
        second = load_audio_url(outputs[1]) if len(outputs) > 1 else first
        return (first, second, "\n".join(outputs), prediction_id)
