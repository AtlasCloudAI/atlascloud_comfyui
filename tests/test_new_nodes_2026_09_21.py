"""Metadata-only tests for newly added nodes (2026-09-21).

New family: LTX-2 native API (`ltx/ltx-2.{3,5}-{fast,pro}/*`). These are a
different endpoint family from the older `ltx-2.3-quality/*` nodes already in
the repo — the payload keys changed (`image` not `image_url`, `duration` in
seconds not `num_frames`, resolution tiers not fal-style presets), so the tests
below pin both the new model ids and the new key names to stop anyone
copy-pasting the quality-family schema back in.

Coverage split across the 10 nodes:
  * text-to-video x4  — prompt required
  * image-to-video x4 — image required, prompt optional
  * audio-to-video x2 — audio required, and prompt required only when no image

Duration enums differ per tier: 2.3-fast/2.5-fast go up to 20s, the pro tiers
cap at 10s, and the 2.5 tiers accept -1 ("model picks"). fps enums differ too
(pro tiers are 24/48 only). Those are pinned per-node.

These tests MUST NOT require ATLASCLOUD_API_KEY.
"""

import inspect

import pytest

from src.atlascloud_comfyui.nodes.video.ltx_2_3_fast_i2v import AtlasLtx23FastImageToVideo
from src.atlascloud_comfyui.nodes.video.ltx_2_3_fast_t2v import AtlasLtx23FastTextToVideo
from src.atlascloud_comfyui.nodes.video.ltx_2_3_pro_a2v import AtlasLtx23ProAudioToVideo
from src.atlascloud_comfyui.nodes.video.ltx_2_3_pro_i2v import AtlasLtx23ProImageToVideo
from src.atlascloud_comfyui.nodes.video.ltx_2_3_pro_t2v import AtlasLtx23ProTextToVideo
from src.atlascloud_comfyui.nodes.video.ltx_2_5_fast_i2v import AtlasLtx25FastImageToVideo
from src.atlascloud_comfyui.nodes.video.ltx_2_5_fast_t2v import AtlasLtx25FastTextToVideo
from src.atlascloud_comfyui.nodes.video.ltx_2_5_pro_a2v import AtlasLtx25ProAudioToVideo
from src.atlascloud_comfyui.nodes.video.ltx_2_5_pro_i2v import AtlasLtx25ProImageToVideo
from src.atlascloud_comfyui.nodes.video.ltx_2_5_pro_t2v import AtlasLtx25ProTextToVideo

T2V = [
    (AtlasLtx23FastTextToVideo, "ltx/ltx-2.3-fast/text-to-video", "AtlasCloud LTX 2.3 Fast Text-to-Video"),
    (AtlasLtx23ProTextToVideo, "ltx/ltx-2.3-pro/text-to-video", "AtlasCloud LTX 2.3 Pro Text-to-Video"),
    (AtlasLtx25FastTextToVideo, "ltx/ltx-2.5-fast/text-to-video", "AtlasCloud LTX 2.5 Fast Text-to-Video"),
    (AtlasLtx25ProTextToVideo, "ltx/ltx-2.5-pro/text-to-video", "AtlasCloud LTX 2.5 Pro Text-to-Video"),
]

I2V = [
    (AtlasLtx23FastImageToVideo, "ltx/ltx-2.3-fast/image-to-video", "AtlasCloud LTX 2.3 Fast Image-to-Video"),
    (AtlasLtx23ProImageToVideo, "ltx/ltx-2.3-pro/image-to-video", "AtlasCloud LTX 2.3 Pro Image-to-Video"),
    (AtlasLtx25FastImageToVideo, "ltx/ltx-2.5-fast/image-to-video", "AtlasCloud LTX 2.5 Fast Image-to-Video"),
    (AtlasLtx25ProImageToVideo, "ltx/ltx-2.5-pro/image-to-video", "AtlasCloud LTX 2.5 Pro Image-to-Video"),
]

A2V = [
    (AtlasLtx23ProAudioToVideo, "ltx/ltx-2.3-pro/audio-to-video", "AtlasCloud LTX 2.3 Pro Audio-to-Video"),
    (AtlasLtx25ProAudioToVideo, "ltx/ltx-2.5-pro/audio-to-video", "AtlasCloud LTX 2.5 Pro Audio-to-Video"),
]

ALL = T2V + I2V + A2V

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


@pytest.mark.parametrize("node,model_id,display", ALL)
def test_node_shape(node, model_id, display):
    inputs = node.INPUT_TYPES()
    assert "atlas_client" in inputs["required"]
    assert "poll_interval_sec" in inputs["optional"]
    assert "timeout_sec" in inputs["optional"]
    assert node.RETURN_TYPES == ("STRING", "STRING")
    assert node.RETURN_NAMES == ("video_url", "prediction_id")
    assert node.CATEGORY == "AtlasCloud/Video"
    assert node.FUNCTION == "run"


@pytest.mark.parametrize("node,model_id,display", ALL)
def test_model_id(node, model_id, display):
    source = inspect.getsource(node.run)
    assert f'"model": "{model_id}"' in source


@pytest.mark.parametrize("node,model_id,display", ALL)
def test_does_not_fall_back_to_quality_family(node, model_id, display):
    # The older ltx-2.3-quality/* endpoints take image_url + num_frames and a
    # fal-style resolution preset. Nothing from that family belongs here.
    source = inspect.getsource(node.run)
    for forbidden in (
        '"model": "ltx-2.3-quality/text-to-video"',
        '"model": "ltx-2.3-quality/image-to-video"',
        '"model": "ltx-2.3-quality/extend-video"',
        '"image_url"',
        '"num_frames"',
    ):
        assert forbidden not in source


@pytest.mark.parametrize("node,model_id,display", ALL)
def test_shared_enums(node, model_id, display):
    optional = node.INPUT_TYPES()["optional"]
    assert optional["resolution"][0] == _RESOLUTIONS
    assert optional["aspect_ratio"][0] == _ASPECT_RATIOS
    assert optional["aspect_ratio"][1]["default"] == "16:9"
    assert optional["camera_motion"][0] == _CAMERA_MOTIONS
    assert optional["camera_motion"][1]["default"] == "auto"
    assert optional["fps"][1]["default"] == 24


@pytest.mark.parametrize("node,model_id,display", ALL)
def test_camera_motion_auto_is_not_sent(node, model_id, display):
    # "auto" is our sentinel for "leave it to the model" — it is not a value the
    # API accepts, so it must never reach the payload.
    source = inspect.getsource(node.run)
    assert 'if camera_motion != "auto":' in source
    assert 'payload["camera_motion"] = camera_motion' in source


@pytest.mark.parametrize("node,model_id,display", T2V)
def test_t2v_requires_prompt(node, model_id, display):
    assert "prompt" in node.INPUT_TYPES()["required"]
    label = display.replace("AtlasCloud ", "")
    for bad_prompt in ("", "  \n \n"):
        with pytest.raises(RuntimeError, match=f"prompt is required for {label}"):
            node().run(None, bad_prompt)


@pytest.mark.parametrize("node,model_id,display", I2V)
def test_i2v_requires_image(node, model_id, display):
    inputs = node.INPUT_TYPES()
    assert "image" in inputs["required"]
    # prompt is only recommended for i2v, never required
    assert "prompt" in inputs["optional"]
    assert "last_image" in inputs["optional"]
    label = display.replace("AtlasCloud ", "")
    for bad_image in ("", "   \n "):
        with pytest.raises(RuntimeError, match=f"image is required for {label}"):
            node().run(None, bad_image)


@pytest.mark.parametrize("node,model_id,display", A2V)
def test_a2v_requires_audio(node, model_id, display):
    inputs = node.INPUT_TYPES()
    assert "audio" in inputs["required"]
    for key in ("image", "last_image", "prompt"):
        assert key in inputs["optional"]
    label = display.replace("AtlasCloud ", "")
    for bad_audio in ("", "   \n "):
        with pytest.raises(RuntimeError, match=f"audio is required for {label}"):
            node().run(None, bad_audio)


@pytest.mark.parametrize("node,model_id,display", A2V)
def test_a2v_requires_prompt_when_image_missing(node, model_id, display):
    label = display.replace("AtlasCloud ", "")
    with pytest.raises(RuntimeError, match=f"prompt is required for {label} when image is empty"):
        node().run(None, "https://example.com/a.mp3", image="", prompt="")


@pytest.mark.parametrize("node,model_id,display", A2V)
def test_a2v_last_image_requires_image(node, model_id, display):
    label = display.replace("AtlasCloud ", "")
    with pytest.raises(RuntimeError, match=f"last_image requires image for {label}"):
        node().run(
            None,
            "https://example.com/a.mp3",
            image="",
            last_image="https://example.com/last.png",
            prompt="a person speaking",
        )


@pytest.mark.parametrize("node,model_id,display", A2V)
def test_a2v_has_no_duration_or_generate_audio(node, model_id, display):
    # audio-to-video takes its length and its soundtrack from the input audio.
    inputs = node.INPUT_TYPES()
    source = inspect.getsource(node.run)
    for key in ("duration", "generate_audio"):
        assert key not in inputs["required"]
        assert key not in inputs["optional"]
        assert f'"{key}"' not in source
    assert inputs["optional"]["resolution"][1]["default"] == "1080p"


@pytest.mark.parametrize(
    "node,durations,default,fps,generate_audio_default",
    [
        (AtlasLtx23FastTextToVideo, [6, 8, 10, 12, 14, 16, 18, 20], 6, [24, 25, 48, 50], False),
        (AtlasLtx23FastImageToVideo, [6, 8, 10, 12, 14, 16, 18, 20], 6, [24, 25, 48, 50], False),
        (AtlasLtx23ProTextToVideo, [6, 8, 10], 6, [24, 48], True),
        (AtlasLtx23ProImageToVideo, [6, 8, 10], 6, [24, 48], True),
        (AtlasLtx25FastTextToVideo, [-1, 6, 8, 10, 12, 14, 16, 18, 20], -1, [24, 25, 48, 50], True),
        (AtlasLtx25FastImageToVideo, [-1, 6, 8, 10, 12, 14, 16, 18, 20], -1, [24, 25, 48, 50], True),
        (AtlasLtx25ProTextToVideo, [-1, 6, 8, 10], -1, [24, 48], True),
        (AtlasLtx25ProImageToVideo, [-1, 6, 8, 10], -1, [24, 48], True),
    ],
)
def test_per_tier_duration_fps_and_audio(node, durations, default, fps, generate_audio_default):
    optional = node.INPUT_TYPES()["optional"]
    assert optional["duration"][0] == durations
    assert optional["duration"][1]["default"] == default
    assert optional["fps"][0] == fps
    assert optional["generate_audio"][1]["default"] is generate_audio_default


def test_new_nodes_registered():
    from src.atlascloud_comfyui.registry import (
        NODE_CLASS_MAPPINGS,
        NODE_DISPLAY_NAME_MAPPINGS,
    )

    for node, _model_id, display in ALL:
        # registry.py imports under the `atlascloud_comfyui.*` path while the
        # tests import under `src.atlascloud_comfyui.*`, so compare by name.
        assert NODE_CLASS_MAPPINGS[display].__name__ == node.__name__
        assert NODE_DISPLAY_NAME_MAPPINGS[display] == display


def test_readme_lists_new_models():
    import pathlib

    readme = pathlib.Path(__file__).resolve().parents[1] / "README.md"
    text = readme.read_text(encoding="utf-8")
    for _node, model_id, display in ALL:
        assert f"| {display} | {model_id} |" in text
