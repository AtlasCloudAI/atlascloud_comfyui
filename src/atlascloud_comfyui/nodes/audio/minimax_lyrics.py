from __future__ import annotations

from typing import Any, Dict, Tuple

from ..auth.atlas_client_node import AtlasClientHandle
from ..utils.audio_output import SEED_INPUT, generate_audio_outputs


class AtlasMiniMaxLyrics:
    CATEGORY = "AtlasCloud/Audio"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("lyrics", "prediction_id")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT",),
                "mode": (
                    ["write_full_song", "edit"],
                    {"default": "write_full_song", "tooltip": "write_full_song writes new lyrics; edit rewrites the lyrics input"},
                ),
                "prompt": (
                    "STRING",
                    {"multiline": True, "default": "", "tooltip": "Theme/style, or the edit instruction (empty = random song)"},
                ),
                "seed": SEED_INPUT,
            },
            "optional": {
                "lyrics": ("STRING", {"multiline": True, "default": "", "tooltip": "Existing lyrics (edit mode only)"}),
                "title": ("STRING", {"default": "", "tooltip": "Song title to keep"}),
                "poll_interval_sec": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"}),
                "timeout_sec": ("INT", {"default": 300, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"}),
            },
        }

    def run(
        self,
        atlas_client: AtlasClientHandle,
        mode: str,
        prompt: str,
        seed: int,
        lyrics: str = "",
        title: str = "",
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 300,
    ) -> Tuple[str, str]:
        payload: Dict[str, Any] = {
            "model": "minimax/lyrics-generation",
            "mode": mode,
            "prompt": (prompt or "").strip(),
            "lyrics": (lyrics or "").strip(),
            "title": (title or "").strip(),
        }

        outputs, prediction_id = generate_audio_outputs(atlas_client, payload, poll_interval_sec=poll_interval_sec, timeout_sec=timeout_sec)
        return (outputs[0], prediction_id)
