"""Metadata-only tests for newly added nodes (2026-09-01).

New models: the MiniMax H3 Max video family (Text-to-Video / Image-to-Video).
H3 Max sits between the 2K-only `minimax/h3/*` nodes and the self-hosted
`minimax/h3-developer/*` ones: it takes 480P/768P resolutions and a
`prompt_expansion` switch, and its image-to-video variant only accepts the
`adaptive` aspect ratio — so these tests pin the model ids, the enums and the
payload keys.
These tests MUST NOT require ATLASCLOUD_API_KEY.
"""

import inspect

import pytest

from src.atlascloud_comfyui.nodes.video.minimax_h3_max_i2v import AtlasMinimaxH3MaxImageToVideo
from src.atlascloud_comfyui.nodes.video.minimax_h3_max_t2v import AtlasMinimaxH3MaxTextToVideo

_H3_MAX_CLASSES = [AtlasMinimaxH3MaxTextToVideo, AtlasMinimaxH3MaxImageToVideo]

_H3_MAX_MODEL_IDS = {
    AtlasMinimaxH3MaxTextToVideo: "minimax/h3-max/text-to-video",
    AtlasMinimaxH3MaxImageToVideo: "minimax/h3-max/image-to-video",
}


@pytest.mark.parametrize("cls", _H3_MAX_CLASSES)
def test_h3_max_node_shape(cls):
    inputs = cls.INPUT_TYPES()
    assert "atlas_client" in inputs["required"]
    assert "prompt" in inputs["required"]
    assert "poll_interval_sec" in inputs["optional"]
    assert "timeout_sec" in inputs["optional"]
    assert cls.RETURN_TYPES == ("STRING", "STRING")
    assert cls.RETURN_NAMES == ("video_url", "prediction_id")
    assert cls.CATEGORY == "AtlasCloud/Video"
    assert cls.FUNCTION == "run"


@pytest.mark.parametrize("cls", _H3_MAX_CLASSES)
def test_h3_max_model_id(cls):
    source = inspect.getsource(cls.run)
    assert f'"model": "{_H3_MAX_MODEL_IDS[cls]}"' in source
    # must not fall back to the plain H3 or the self-hosted H3-Developer tier
    assert '"model": "minimax/h3/' not in source
    assert '"model": "minimax/h3-developer/' not in source


@pytest.mark.parametrize("cls", _H3_MAX_CLASSES)
def test_h3_max_resolution_and_duration(cls):
    optional = cls.INPUT_TYPES()["optional"]
    assert optional["resolution"][0] == ["480P", "768P"]
    assert optional["resolution"][1]["default"] == "768P"
    duration = optional["duration"]
    assert duration[0] == "INT"
    assert duration[1]["default"] == 8
    assert duration[1]["min"] == 5
    assert duration[1]["max"] == 15


@pytest.mark.parametrize("cls", _H3_MAX_CLASSES)
def test_h3_max_prompt_expansion(cls):
    optional = cls.INPUT_TYPES()["optional"]
    assert optional["prompt_expansion"][0] == "BOOLEAN"
    assert optional["prompt_expansion"][1]["default"] is False
    assert '"prompt_expansion": bool(prompt_expansion)' in inspect.getsource(cls.run)


def test_h3_max_t2v_ratio_presets():
    ratio = AtlasMinimaxH3MaxTextToVideo.INPUT_TYPES()["optional"]["ratio"]
    assert ratio[0] == ["21:9", "16:9", "4:3", "1:1", "3:4", "9:16"]
    assert ratio[1]["default"] == "1:1"


def test_h3_max_i2v_ratio_is_adaptive_only():
    ratio = AtlasMinimaxH3MaxImageToVideo.INPUT_TYPES()["optional"]["ratio"]
    assert ratio[0] == ["adaptive"]
    assert ratio[1]["default"] == "adaptive"


def test_h3_max_t2v_has_no_image_input():
    inputs = AtlasMinimaxH3MaxTextToVideo.INPUT_TYPES()
    assert "image" not in inputs["required"]
    assert "image" not in inputs["optional"]
    assert "end_image" not in inputs["optional"]


@pytest.mark.parametrize("bad_prompt", ["", "  \n \n"])
def test_h3_max_t2v_requires_prompt(bad_prompt):
    with pytest.raises(RuntimeError, match="prompt is required"):
        AtlasMinimaxH3MaxTextToVideo().run(None, bad_prompt)


def test_h3_max_i2v_image_inputs():
    inputs = AtlasMinimaxH3MaxImageToVideo.INPUT_TYPES()
    assert "image" in inputs["required"]
    assert "end_image" in inputs["optional"]


@pytest.mark.parametrize("bad_image", ["", "   "])
def test_h3_max_i2v_requires_image(bad_image):
    with pytest.raises(RuntimeError, match="image is required"):
        AtlasMinimaxH3MaxImageToVideo().run(None, bad_image, "a prompt")


def test_h3_max_i2v_requires_prompt():
    with pytest.raises(RuntimeError, match="prompt is required"):
        AtlasMinimaxH3MaxImageToVideo().run(None, "https://example.com/a.png", "  ")


def test_h3_max_i2v_end_image_is_optional_in_payload():
    source = inspect.getsource(AtlasMinimaxH3MaxImageToVideo.run)
    assert 'payload["end_image"] = end_image.strip()' in source


def test_h3_max_nodes_registered():
    from src.atlascloud_comfyui.registry import (
        NODE_CLASS_MAPPINGS,
        NODE_DISPLAY_NAME_MAPPINGS,
    )

    for key, cls in (
        ("AtlasCloud MiniMax H3 Max Text-to-Video", AtlasMinimaxH3MaxTextToVideo),
        ("AtlasCloud MiniMax H3 Max Image-to-Video", AtlasMinimaxH3MaxImageToVideo),
    ):
        # registry.py imports under the `atlascloud_comfyui.*` path while the
        # tests import under `src.atlascloud_comfyui.*`, so compare by name.
        assert NODE_CLASS_MAPPINGS[key].__name__ == cls.__name__
        assert NODE_DISPLAY_NAME_MAPPINGS[key] == key
