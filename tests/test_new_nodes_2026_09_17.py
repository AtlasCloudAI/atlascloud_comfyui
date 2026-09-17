"""Metadata-only tests for newly added nodes (2026-09-17).

New model: `black-forest-labs/flux-3/edit-video`, the FLUX 3 family's
prompt-driven video re-render. Unlike its Extend Video sibling it has a
deliberately narrow schema — prompt and video_url are both required, and the
only other knob is `safety_tolerance`. No aspect_ratio / resolution / duration /
generate_audio / seed: the output follows the input clip. These tests pin the
model id so it cannot silently fall back to extend-video, and pin the absence of
the sibling's knobs so nobody copy-pastes them back in.
These tests MUST NOT require ATLASCLOUD_API_KEY.
"""

import inspect

import pytest

from src.atlascloud_comfyui.nodes.video.flux3_edit_video import AtlasFlux3EditVideo

_MODEL_ID = "black-forest-labs/flux-3/edit-video"


def test_node_shape():
    inputs = AtlasFlux3EditVideo.INPUT_TYPES()
    assert "atlas_client" in inputs["required"]
    assert "prompt" in inputs["required"]
    assert "video_url" in inputs["required"]
    assert "poll_interval_sec" in inputs["optional"]
    assert "timeout_sec" in inputs["optional"]
    assert AtlasFlux3EditVideo.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasFlux3EditVideo.RETURN_NAMES == ("video_url", "prediction_id")
    assert AtlasFlux3EditVideo.CATEGORY == "AtlasCloud/Video"


def test_model_id():
    source = inspect.getsource(AtlasFlux3EditVideo.run)
    assert f'"model": "{_MODEL_ID}"' in source


def test_does_not_fall_back_to_sibling_endpoint():
    source = inspect.getsource(AtlasFlux3EditVideo.run)
    for forbidden in (
        '"model": "black-forest-labs/flux-3/extend-video"',
        '"model": "black-forest-labs/flux-3/image-to-video"',
        '"model": "black-forest-labs/flux-3/text-to-video"',
    ):
        assert forbidden not in source


@pytest.mark.parametrize("bad_prompt", ["", "  \n \n"])
def test_requires_prompt(bad_prompt):
    with pytest.raises(RuntimeError, match="prompt is required"):
        AtlasFlux3EditVideo().run(None, bad_prompt, "https://example.com/a.mp4")


@pytest.mark.parametrize("bad_video", ["", "   \n "])
def test_requires_video_url(bad_video):
    with pytest.raises(RuntimeError, match="video_url is required"):
        AtlasFlux3EditVideo().run(None, "make it a comic book", bad_video)


def test_safety_tolerance_bounds():
    safety = AtlasFlux3EditVideo.INPUT_TYPES()["optional"]["safety_tolerance"]
    assert safety[0] == "INT"
    assert safety[1]["default"] == 2
    assert safety[1]["min"] == 0
    assert safety[1]["max"] == 4


def test_no_extend_video_only_knobs():
    # edit-video re-renders the source clip, so duration / resolution /
    # aspect_ratio / generate_audio / seed are not part of its schema.
    inputs = AtlasFlux3EditVideo.INPUT_TYPES()
    source = inspect.getsource(AtlasFlux3EditVideo.run)
    for key in ("duration", "resolution", "aspect_ratio", "generate_audio", "seed"):
        assert key not in inputs["required"]
        assert key not in inputs["optional"]
        assert f'"{key}"' not in source


def test_new_nodes_registered():
    from src.atlascloud_comfyui.registry import (
        NODE_CLASS_MAPPINGS,
        NODE_DISPLAY_NAME_MAPPINGS,
    )

    key = "AtlasCloud FLUX 3 Edit Video"
    # registry.py imports under the `atlascloud_comfyui.*` path while the tests
    # import under `src.atlascloud_comfyui.*`, so compare by name.
    assert NODE_CLASS_MAPPINGS[key].__name__ == AtlasFlux3EditVideo.__name__
    assert NODE_DISPLAY_NAME_MAPPINGS[key] == key
