"""Metadata-only tests for newly added nodes (2026-08-28).

New models: the MiniMax H3-Developer family (Text/Image/Reference-to-Video).
These are the self-hosted "developer" tier of MiniMax H3 — same shape as the
plain H3 nodes but with 480P/768P resolutions and a prompt_expansion switch,
so these tests also pin the model ids to make sure the Developer nodes do not
silently fall back to the non-Developer endpoints.
These tests MUST NOT require ATLASCLOUD_API_KEY.
"""

import inspect

import pytest

from src.atlascloud_comfyui.nodes.video.minimax_h3_developer_i2v import (
    AtlasMinimaxH3DeveloperImageToVideo,
)
from src.atlascloud_comfyui.nodes.video.minimax_h3_developer_r2v import (
    AtlasMinimaxH3DeveloperReferenceToVideo,
)
from src.atlascloud_comfyui.nodes.video.minimax_h3_developer_t2v import (
    AtlasMinimaxH3DeveloperTextToVideo,
)

_DEV_CLASSES = [
    AtlasMinimaxH3DeveloperTextToVideo,
    AtlasMinimaxH3DeveloperImageToVideo,
    AtlasMinimaxH3DeveloperReferenceToVideo,
]

_DEV_MODEL_IDS = {
    AtlasMinimaxH3DeveloperTextToVideo: "minimax/h3-developer/text-to-video",
    AtlasMinimaxH3DeveloperImageToVideo: "minimax/h3-developer/image-to-video",
    AtlasMinimaxH3DeveloperReferenceToVideo: "minimax/h3-developer/reference-to-video",
}


@pytest.mark.parametrize("cls", _DEV_CLASSES)
def test_dev_node_shape(cls):
    inputs = cls.INPUT_TYPES()
    assert "atlas_client" in inputs["required"]
    assert "prompt" in inputs["required"]
    assert "poll_interval_sec" in inputs["optional"]
    assert "timeout_sec" in inputs["optional"]
    assert cls.RETURN_TYPES == ("STRING", "STRING")
    assert cls.RETURN_NAMES == ("video_url", "prediction_id")
    assert cls.CATEGORY == "AtlasCloud/Video"
    assert cls.FUNCTION == "run"


@pytest.mark.parametrize("cls", _DEV_CLASSES)
def test_dev_model_id(cls):
    source = inspect.getsource(cls.run)
    assert f'"model": "{_DEV_MODEL_IDS[cls]}"' in source
    # must not fall back to the non-developer endpoint
    assert '"model": "minimax/h3/' not in source


@pytest.mark.parametrize("cls", _DEV_CLASSES)
def test_dev_common_options(cls):
    optional = cls.INPUT_TYPES()["optional"]
    assert optional["resolution"][0] == ["480P", "768P"]
    assert optional["resolution"][1]["default"] == "768P"
    assert optional["duration"][1]["min"] == 4
    assert optional["duration"][1]["max"] == 15
    assert optional["duration"][1]["default"] == 8
    assert optional["prompt_expansion"][0] == "BOOLEAN"
    assert optional["prompt_expansion"][1]["default"] is False


@pytest.mark.parametrize("cls", _DEV_CLASSES)
def test_dev_sends_prompt_expansion(cls):
    source = inspect.getsource(cls.run)
    assert '"prompt_expansion": bool(prompt_expansion)' in source


def test_dev_t2v_metadata():
    ratio = AtlasMinimaxH3DeveloperTextToVideo.INPUT_TYPES()["optional"]["ratio"]
    assert ratio[0] == ["21:9", "16:9", "4:3", "1:1", "3:4", "9:16"]
    assert ratio[1]["default"] == "1:1"


@pytest.mark.parametrize("bad_prompt", ["", "   "])
def test_dev_t2v_requires_prompt(bad_prompt):
    with pytest.raises(RuntimeError, match="prompt is required"):
        AtlasMinimaxH3DeveloperTextToVideo().run(None, bad_prompt)


def test_dev_i2v_metadata():
    inputs = AtlasMinimaxH3DeveloperImageToVideo.INPUT_TYPES()
    assert "image" in inputs["required"]
    assert "end_image" in inputs["optional"]
    # the schema only accepts 'adaptive' here — the ratio comes from the first frame
    ratio = inputs["optional"]["ratio"]
    assert ratio[0] == ["adaptive"]
    assert ratio[1]["default"] == "adaptive"


@pytest.mark.parametrize("bad_image", ["", "   "])
def test_dev_i2v_requires_image(bad_image):
    with pytest.raises(RuntimeError, match="image is required"):
        AtlasMinimaxH3DeveloperImageToVideo().run(None, bad_image, "a prompt")


def test_dev_i2v_requires_prompt():
    with pytest.raises(RuntimeError, match="prompt is required"):
        AtlasMinimaxH3DeveloperImageToVideo().run(None, "https://example.com/a.png", "  ")


def test_dev_i2v_omits_empty_end_image():
    source = inspect.getsource(AtlasMinimaxH3DeveloperImageToVideo.run)
    assert 'payload["end_image"] = end_image.strip()' in source


def test_dev_r2v_metadata():
    inputs = AtlasMinimaxH3DeveloperReferenceToVideo.INPUT_TYPES()
    assert "refers" in inputs["required"]
    ratio = inputs["optional"]["ratio"]
    assert ratio[0] == ["adaptive", "21:9", "16:9", "4:3", "1:1", "3:4", "9:16"]
    assert ratio[1]["default"] == "adaptive"


@pytest.mark.parametrize("bad_refers", ["", "  \n \n"])
def test_dev_r2v_requires_refers(bad_refers):
    with pytest.raises(RuntimeError, match="refers is required"):
        AtlasMinimaxH3DeveloperReferenceToVideo().run(None, bad_refers, "a prompt")


def test_dev_r2v_requires_prompt():
    with pytest.raises(RuntimeError, match="prompt is required"):
        AtlasMinimaxH3DeveloperReferenceToVideo().run(None, "https://example.com/a.png", " ")


def test_dev_r2v_wraps_refers_as_url_objects():
    source = inspect.getsource(AtlasMinimaxH3DeveloperReferenceToVideo.run)
    assert '[{"url": u} for u in urls]' in source


def test_dev_nodes_registered():
    from src.atlascloud_comfyui.registry import (
        NODE_CLASS_MAPPINGS,
        NODE_DISPLAY_NAME_MAPPINGS,
    )

    for key, cls in (
        ("AtlasCloud MiniMax H3-Developer Text-to-Video", AtlasMinimaxH3DeveloperTextToVideo),
        ("AtlasCloud MiniMax H3-Developer Image-to-Video", AtlasMinimaxH3DeveloperImageToVideo),
        ("AtlasCloud MiniMax H3-Developer Reference-to-Video", AtlasMinimaxH3DeveloperReferenceToVideo),
    ):
        # registry.py imports under the `atlascloud_comfyui.*` path while the
        # tests import under `src.atlascloud_comfyui.*`, so compare by name.
        assert NODE_CLASS_MAPPINGS[key].__name__ == cls.__name__
        assert NODE_DISPLAY_NAME_MAPPINGS[key] == key
