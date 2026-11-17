from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle
from ..utils.audio_output import SEED_INPUT, generate_audio_outputs, load_audio_url

_WEIGHT_TOOLTIP = "Needs lyrics or instrumental; -1 leaves it to the API"


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
                        "tooltip": "Describe the song: genre, mood, instruments, vocals",
                    },
                ),
                "lyrics": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": "",
                        "tooltip": "Your lyrics ([Verse] / [Chorus] ...). Leave empty and Suno writes its own; turn on instrumental for no vocals",
                    },
                ),
                "instrumental": ("BOOLEAN", {"default": False, "tooltip": "No vocals"}),
                "seed": SEED_INPUT,
            },
            "optional": {
                "title": ("STRING", {"default": "", "tooltip": "Song title (needs lyrics or instrumental)"}),
                "style": (
                    "STRING",
                    {
                        "default": "",
                        "tooltip": "Style tags, e.g. synthwave, female vocal; empty = use the prompt (needs lyrics or instrumental)",
                    },
                ),
                "negative_tags": ("STRING", {"default": "", "tooltip": "Styles to avoid (needs lyrics or instrumental)"}),
                "vocal_gender": (["auto", "Male", "Female"], {"default": "auto", "tooltip": "Vocal gender"}),
                "variety": (
                    ["auto", "off", "normal", "high", "extra", "max"],
                    {"default": "auto", "tooltip": "How far the two takes stray from the obvious rendition"},
                ),
                "auto_lyrics": ("BOOLEAN", {"default": False, "tooltip": "Let Suno rewrite your lyrics (only when lyrics are given)"}),
                "duration": (
                    "INT",
                    {"default": 0, "min": 0, "max": 360, "tooltip": "Seconds (10-360, needs lyrics or instrumental); 0 = auto"},
                ),
                "style_weight": ("FLOAT", {"default": -1.0, "min": -1.0, "max": 1.0, "step": 0.05, "tooltip": _WEIGHT_TOOLTIP}),
                "weirdness_constraint": ("FLOAT", {"default": -1.0, "min": -1.0, "max": 1.0, "step": 0.05, "tooltip": _WEIGHT_TOOLTIP}),
                "audio_weight": ("FLOAT", {"default": -1.0, "min": -1.0, "max": 1.0, "step": 0.05, "tooltip": _WEIGHT_TOOLTIP}),
                "persona_id": ("STRING", {"default": "", "tooltip": "Persona (voice identity) id (needs lyrics or instrumental)"}),
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
        description = (prompt or "").strip()
        lyrics = (lyrics or "").strip()
        # Suno's custom mode reads `prompt` as lyrics and is the only mode where title, style,
        # duration and the weights apply; inspiration mode reads `prompt` as a description and
        # always writes its own lyrics unless instrumental.
        custom = bool(lyrics) or bool(instrumental)
        payload: Dict[str, Any] = {
            "model": f"suno/{model}",
            "custom": custom,
            "instrumental": bool(instrumental),
        }
        if vocal_gender != "auto":
            payload["vocal_gender"] = vocal_gender
        if variety != "auto":
            payload["variety"] = variety

        if not custom:
            payload["prompt"] = description
        else:
            if lyrics:
                payload["prompt"] = lyrics
                payload["auto_lyrics"] = bool(auto_lyrics)
            style = (style or "").strip() or description
            for key, value in (("title", title), ("style", style), ("negative_tags", negative_tags), ("persona_id", persona_id)):
                if (value or "").strip():
                    payload[key] = value.strip()
            if duration > 0:
                payload["duration"] = int(duration)
            for key, value in (
                ("style_weight", style_weight),
                ("weirdness_constraint", weirdness_constraint),
                ("audio_weight", audio_weight),
            ):
                if value >= 0:
                    payload[key] = float(value)

        outputs, prediction_id = generate_audio_outputs(atlas_client, payload, poll_interval_sec=poll_interval_sec, timeout_sec=timeout_sec)
        # Suno returns two takes per request.
        first = load_audio_url(outputs[0])
        second = load_audio_url(outputs[1]) if len(outputs) > 1 else first
        return (first, second, "\n".join(outputs), prediction_id)
