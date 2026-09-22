"""Metadata-only tests for newly added nodes (2026-09-22).

One new node: `ltx/ltx-2.5-fast/audio-to-video`, the fast tier of the LTX-2
native audio-to-video endpoint already covered by
`test_new_nodes_2026_09_21.py`. Its published schema is identical to the pro
tier's (same resolution/aspect_ratio/fps/camera_motion enums, same required
`audio`), so the tests below mainly pin that the model id actually points at
the fast tier and that the fast node did not inherit the pro model id from the
file it was derived from.

These tests MUST NOT require ATLASCLOUD_API_KEY.
"""

import inspect

import pytest

from src.atlascloud_comfyui.nodes.video.ltx_2_5_fast_a2v import AtlasLtx25FastAudioToVideo

MODEL_ID = "ltx/ltx-2.5-fast/audio-to-video"
DISPLAY = "AtlasCloud LTX 2.5 Fast Audio-to-Video"
LABEL = DISPLAY.replace("AtlasCloud ", "")

_RESOLUTIONS = ["720p", "1080p", "1440p", "4k"]
_ASPECT_RATIOS = ["16:9", "9:16"]
_CAMERA_MOTIONS = [
    "auto",
    "dolly_in",
    "dolly_out",
    "dolly_left",
    "dolly_right",
    "jib_up",
    "jib_down",
    "static",
    "focus_shift",
]


def test_node_shape():
    inputs = AtlasLtx25FastAudioToVideo.INPUT_TYPES()
    assert "atlas_client" in inputs["required"]
    assert "audio" in inputs["required"]
    assert "poll_interval_sec" in inputs["optional"]
    assert "timeout_sec" in inputs["optional"]
    assert AtlasLtx25FastAudioToVideo.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasLtx25FastAudioToVideo.RETURN_NAMES == ("video_url", "prediction_id")
    assert AtlasLtx25FastAudioToVideo.CATEGORY == "AtlasCloud/Video"
    assert AtlasLtx25FastAudioToVideo.FUNCTION == "run"


def test_model_id_is_the_fast_tier():
    source = inspect.getsource(AtlasLtx25FastAudioToVideo.run)
    assert f'"model": "{MODEL_ID}"' in source
    # derived from the pro node — make sure the pro id did not survive the copy
    assert "ltx-2.5-pro" not in source


def test_enums_match_published_schema():
    optional = AtlasLtx25FastAudioToVideo.INPUT_TYPES()["optional"]
    assert optional["resolution"][0] == _RESOLUTIONS
    assert optional["resolution"][1]["default"] == "1080p"
    assert optional["aspect_ratio"][0] == _ASPECT_RATIOS
    assert optional["aspect_ratio"][1]["default"] == "16:9"
    assert optional["fps"][0] == [24, 25, 48, 50]
    assert optional["fps"][1]["default"] == 24
    assert optional["camera_motion"][0] == _CAMERA_MOTIONS
    assert optional["camera_motion"][1]["default"] == "auto"


def test_camera_motion_auto_is_not_sent():
    # "auto" is our sentinel for "leave it to the model" — the API has no such
    # enum value, so it must never reach the payload.
    source = inspect.getsource(AtlasLtx25FastAudioToVideo.run)
    assert 'if camera_motion != "auto":' in source
    assert 'payload["camera_motion"] = camera_motion' in source


def test_has_no_duration_or_generate_audio():
    # audio-to-video takes its length and its soundtrack from the input audio.
    inputs = AtlasLtx25FastAudioToVideo.INPUT_TYPES()
    source = inspect.getsource(AtlasLtx25FastAudioToVideo.run)
    for key in ("duration", "generate_audio"):
        assert key not in inputs["required"]
        assert key not in inputs["optional"]
        assert f'"{key}"' not in source


def test_requires_audio():
    for bad_audio in ("", "   \n "):
        with pytest.raises(RuntimeError, match=f"audio is required for {LABEL}"):
            AtlasLtx25FastAudioToVideo().run(None, bad_audio)


def test_requires_prompt_when_image_missing():
    with pytest.raises(RuntimeError, match=f"prompt is required for {LABEL} when image is empty"):
        AtlasLtx25FastAudioToVideo().run(None, "https://example.com/a.mp3", image="", prompt="")


def test_last_image_requires_image():
    with pytest.raises(RuntimeError, match=f"last_image requires image for {LABEL}"):
        AtlasLtx25FastAudioToVideo().run(
            None,
            "https://example.com/a.mp3",
            image="",
            last_image="https://example.com/last.png",
            prompt="a person speaking",
        )


def test_registered():
    from src.atlascloud_comfyui.registry import (
        NODE_CLASS_MAPPINGS,
        NODE_DISPLAY_NAME_MAPPINGS,
    )

    # registry.py imports under the `atlascloud_comfyui.*` path while the tests
    # import under `src.atlascloud_comfyui.*`, so compare by name.
    assert NODE_CLASS_MAPPINGS[DISPLAY].__name__ == AtlasLtx25FastAudioToVideo.__name__
    assert NODE_DISPLAY_NAME_MAPPINGS[DISPLAY] == DISPLAY


def test_readme_lists_new_model():
    import pathlib

    readme = pathlib.Path(__file__).resolve().parents[1] / "README.md"
    assert f"| {DISPLAY} | {MODEL_ID} |" in readme.read_text(encoding="utf-8")
