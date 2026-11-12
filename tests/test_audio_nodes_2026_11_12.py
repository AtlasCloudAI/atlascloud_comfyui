"""Tests for the audio generation nodes (2026-11-12).

Models: Seed Audio 1.0, MiniMax Music / Speech / Lyrics, Suno V6, ElevenLabs v3 / v4 TTS,
Qwen-Audio 3.1 TTS. These tests MUST NOT require ATLASCLOUD_API_KEY or network access.
"""

import io
import math
import struct
import wave
from unittest.mock import MagicMock

import pytest

from src.atlascloud_comfyui.history.local_history import _default_extension
from src.atlascloud_comfyui.nodes.audio import (
    elevenlabs_v3_tts,
    elevenlabs_v4_tts,
    minimax_lyrics,
    minimax_music,
    minimax_speech,
    qwen_audio_31_tts,
    seed_audio_v10,
    suno_v6,
)
from src.atlascloud_comfyui.nodes.utils.audio_output import decode_audio_bytes

AUDIO_MODULES = [seed_audio_v10, minimax_music, minimax_speech, suno_v6, elevenlabs_v4_tts, elevenlabs_v3_tts, qwen_audio_31_tts]


def _handle(outputs):
    handle = MagicMock()
    handle.client.generate_audio.return_value = "pred_audio"
    handle.client.poll_prediction.return_value = {"data": {"outputs": outputs}}
    return handle


@pytest.fixture
def fake_load(monkeypatch):
    loaded = []

    def _load(url):
        loaded.append(url)
        return {"waveform": url, "sample_rate": 1}

    for module in AUDIO_MODULES:
        monkeypatch.setattr(module, "load_audio_url", _load)
    return loaded


def _payload(handle):
    return handle.client.generate_audio.call_args[0][0]


def test_decode_audio_bytes_wav():
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(24000)
        w.writeframes(b"".join(struct.pack("<hh", int(16000 * math.sin(i / 10)), 0) for i in range(2400)))

    audio = decode_audio_bytes(buf.getvalue())
    assert audio["sample_rate"] == 24000
    assert tuple(audio["waveform"].shape) == (1, 2, 2400)
    assert str(audio["waveform"].dtype) == "torch.float32"


@pytest.mark.parametrize(
    "payload,ext",
    [({"format": "ogg_opus"}, ".ogg"), ({"output_format": "mp3_44100_128"}, ".mp3"), ({"output_format": "wav"}, ".wav"), ({}, ".mp3")],
)
def test_history_audio_extension(payload, ext):
    assert _default_extension("audio", payload) == ext


@pytest.mark.parametrize(
    "cls",
    [
        seed_audio_v10.AtlasSeedAudio10,
        minimax_music.AtlasMiniMaxMusic,
        minimax_speech.AtlasMiniMaxSpeech,
        suno_v6.AtlasSunoV6,
        elevenlabs_v4_tts.AtlasElevenLabsV4TextToSpeech,
        elevenlabs_v3_tts.AtlasElevenLabsV3TextToSpeech,
        qwen_audio_31_tts.AtlasQwenAudio31TextToSpeech,
    ],
)
def test_audio_node_metadata(cls):
    assert cls.CATEGORY == "AtlasCloud/Audio"
    required = cls.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert required["seed"][1]["control_after_generate"] is True
    assert cls.RETURN_TYPES[0] == "AUDIO"


def test_seed_audio_references(fake_load):
    handle = _handle(["http://x/out.mp3"])
    audio, url, pred = seed_audio_v10.AtlasSeedAudio10().run(
        handle, "hello", 0, speaker="zh_female_vv_uranus_bigtts", reference_audios="http://a.wav\n\nhttp://b.wav"
    )
    assert (url, pred) == ("http://x/out.mp3", "pred_audio")
    assert fake_load == ["http://x/out.mp3"]
    assert _payload(handle)["references"] == [
        {"speaker": "zh_female_vv_uranus_bigtts"},
        {"audio_url": "http://a.wav"},
        {"audio_url": "http://b.wav"},
    ]


def test_seed_audio_no_references(fake_load):
    handle = _handle(["http://x/out.mp3"])
    seed_audio_v10.AtlasSeedAudio10().run(handle, "hello", 0)
    assert "references" not in _payload(handle)
    assert "seed" not in _payload(handle)


def test_minimax_music_optimizer_only_for_30(fake_load):
    handle = _handle(["http://x/song.mp3"])
    minimax_music.AtlasMiniMaxMusic().run(handle, "music-3.0", "lofi", "", 0, lyrics_optimizer=True)
    assert _payload(handle)["model"] == "minimax/music-3.0"
    assert _payload(handle)["lyrics_optimizer"] is True

    minimax_music.AtlasMiniMaxMusic().run(handle, "music-2.6", "lofi", "", 0, lyrics_optimizer=True)
    assert _payload(handle)["model"] == "minimax/music-2.6"
    assert "lyrics_optimizer" not in _payload(handle)


@pytest.mark.parametrize("model,key", [("speech-2.8-hd", "output_format"), ("speech-2.6-turbo", "format")])
def test_minimax_speech_format_key(fake_load, model, key):
    handle = _handle(["http://x/speech.mp3"])
    minimax_speech.AtlasMiniMaxSpeech().run(handle, model, "hi", "English_CalmWoman", 0, output_format="flac")
    payload = _payload(handle)
    assert payload["model"] == f"minimax/{model}"
    assert payload[key] == "flac"


def test_minimax_lyrics_returns_text():
    handle = _handle(["[Verse]\nla la"])
    lyrics, pred = minimax_lyrics.AtlasMiniMaxLyrics().run(handle, "write_full_song", "summer", 0)
    assert (lyrics, pred) == ("[Verse]\nla la", "pred_audio")
    assert _payload(handle)["model"] == "minimax/lyrics-generation"


def test_suno_two_takes_and_optional_fields(fake_load):
    handle = _handle(["http://x/1.mp3", "http://x/2.mp3"])
    first, second, urls, pred = suno_v6.AtlasSunoV6().run(
        handle, "chirp-v6-wild", "[Verse] hi", True, False, 0, title="Song", style_weight=0.4
    )
    assert fake_load == ["http://x/1.mp3", "http://x/2.mp3"]
    assert urls == "http://x/1.mp3\nhttp://x/2.mp3"
    payload = _payload(handle)
    assert payload["model"] == "suno/chirp-v6-wild"
    assert payload["title"] == "Song"
    assert payload["style_weight"] == 0.4
    for key in ("style", "vocal_gender", "variety", "duration", "weirdness_constraint", "audio_weight", "persona_id"):
        assert key not in payload


def test_elevenlabs_v4_voice_id_override(fake_load):
    handle = _handle(["http://x/tts.mp3"])
    elevenlabs_v4_tts.AtlasElevenLabsV4TextToSpeech().run(handle, "v4-turbo", "hi", "Roger", 7, voice_id="myCloneId")
    payload = _payload(handle)
    assert payload["model"] == "elevenlabs/v4-turbo/text-to-speech"
    assert payload["voice"] == "myCloneId"
    assert payload["seed"] == 7


def test_elevenlabs_v3_maps_voice_name_to_id(fake_load):
    handle = _handle(["http://x/tts.mp3"])
    elevenlabs_v3_tts.AtlasElevenLabsV3TextToSpeech().run(handle, "hi", "Roger", 0)
    assert _payload(handle)["voice"] == "CwhRBWXzGAHq8TQ4Fs17"
    assert "seed" not in _payload(handle)


def test_qwen_audio_31_payload(fake_load):
    handle = _handle(["http://x/tts.mp3"])
    qwen_audio_31_tts.AtlasQwenAudio31TextToSpeech().run(handle, "plus", "hi", "longanhuan_v3.1", 12, language_hint="en")
    payload = _payload(handle)
    assert payload["model"] == "alibaba/qwen-audio-3.1-tts-plus/text-to-speech"
    assert payload["language_hints"] == ["en"]
    assert payload["seed"] == 12
    assert "instruction" not in payload


@pytest.mark.parametrize(
    "cls,args",
    [
        (seed_audio_v10.AtlasSeedAudio10, ("  ", 0)),
        (minimax_speech.AtlasMiniMaxSpeech, ("speech-2.8-hd", " ", "English_CalmWoman", 0)),
        (elevenlabs_v4_tts.AtlasElevenLabsV4TextToSpeech, ("v4", "", "Roger", 0)),
        (elevenlabs_v3_tts.AtlasElevenLabsV3TextToSpeech, ("", "Roger", 0)),
        (qwen_audio_31_tts.AtlasQwenAudio31TextToSpeech, ("flash", "", "Emily_v3.1", 0)),
    ],
)
def test_tts_requires_text(cls, args):
    with pytest.raises(RuntimeError, match="text is required"):
        cls().run(None, *args)


def test_audio_nodes_registered():
    from src.atlascloud_comfyui.registry import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

    names = [
        "AtlasCloud Seed Audio 1.0",
        "AtlasCloud MiniMax Music",
        "AtlasCloud MiniMax Speech",
        "AtlasCloud MiniMax Lyrics Generation",
        "AtlasCloud Suno V6",
        "AtlasCloud ElevenLabs v4 Text-to-Speech",
        "AtlasCloud ElevenLabs v3 Text-to-Speech",
        "AtlasCloud Qwen-Audio 3.1 Text-to-Speech",
    ]
    for name in names:
        assert name in NODE_CLASS_MAPPINGS
        assert NODE_DISPLAY_NAME_MAPPINGS[name] == name
