"""Metadata-only tests for newly added nodes (2026-09-10).

New models: the MiniMax H3 Max Turbo pair (Text-to-Video / Image-to-Video). The
turbo tier is a cheaper sibling of h3-max and shares its request schema, minus
`prompt_expansion`, which h3-max-turbo does not accept. These tests pin the
model ids so the turbo tier cannot silently fall back to h3-max, and pin the
schema deltas.
These tests MUST NOT require ATLASCLOUD_API_KEY.
"""

import inspect

import pytest

from src.atlascloud_comfyui.nodes.video.minimax_h3_max_turbo_i2v import (
    AtlasMinimaxH3MaxTurboImageToVideo,
)
from src.atlascloud_comfyui.nodes.video.minimax_h3_max_turbo_t2v import (
    AtlasMinimaxH3MaxTurboTextToVideo,
)

_MODEL_IDS = {
    AtlasMinimaxH3MaxTurboTextToVideo: "minimax/h3-max-turbo/text-to-video",
    AtlasMinimaxH3MaxTurboImageToVideo: "minimax/h3-max-turbo/image-to-video",
}

_CLASSES = list(_MODEL_IDS)


@pytest.mark.parametrize("cls", _CLASSES)
def test_node_shape(cls):
    inputs = cls.INPUT_TYPES()
    assert "atlas_client" in inputs["required"]
    assert "prompt" in inputs["required"]
    assert "poll_interval_sec" in inputs["optional"]
    assert "timeout_sec" in inputs["optional"]
    assert cls.RETURN_TYPES == ("STRING", "STRING")
    assert cls.CATEGORY == "AtlasCloud/Video"
    assert cls.RETURN_NAMES == ("video_url", "prediction_id")


@pytest.mark.parametrize("cls", _CLASSES)
def test_model_id(cls):
    source = inspect.getsource(cls.run)
    assert f'"model": "{_MODEL_IDS[cls]}"' in source


@pytest.mark.parametrize("cls", _CLASSES)
def test_does_not_fall_back_to_sibling_tier(cls):
    source = inspect.getsource(cls.run)
    for prefix in ('"model": "minimax/h3-max/', '"model": "minimax/h3-fast/', '"model": "minimax/h3/'):
        assert prefix not in source


@pytest.mark.parametrize("cls", _CLASSES)
def test_resolution_and_duration(cls):
    optional = cls.INPUT_TYPES()["optional"]
    assert optional["resolution"][0] == ["480P", "768P"]
    assert optional["resolution"][1]["default"] == "768P"
    duration = optional["duration"][1]
    assert (duration["default"], duration["min"], duration["max"]) == (8, 5, 15)


@pytest.mark.parametrize("cls", _CLASSES)
def test_no_prompt_expansion(cls):
    # h3-max accepts prompt_expansion; h3-max-turbo does not.
    inputs = cls.INPUT_TYPES()
    assert "prompt_expansion" not in inputs["required"]
    assert "prompt_expansion" not in inputs["optional"]
    assert "prompt_expansion" not in inspect.getsource(cls.run)


def test_t2v_ratio_choices():
    ratio = AtlasMinimaxH3MaxTurboTextToVideo.INPUT_TYPES()["optional"]["ratio"]
    assert ratio[0] == ["21:9", "16:9", "4:3", "1:1", "3:4", "9:16"]
    assert ratio[1]["default"] == "1:1"


def test_i2v_ratio_is_adaptive_only():
    ratio = AtlasMinimaxH3MaxTurboImageToVideo.INPUT_TYPES()["optional"]["ratio"]
    assert ratio[0] == ["adaptive"]
    assert ratio[1]["default"] == "adaptive"


def test_t2v_has_no_image_inputs():
    inputs = AtlasMinimaxH3MaxTurboTextToVideo.INPUT_TYPES()
    for key in ("image", "end_image"):
        assert key not in inputs["required"]
        assert key not in inputs["optional"]


@pytest.mark.parametrize("bad_prompt", ["", "  \n \n"])
def test_t2v_requires_prompt(bad_prompt):
    with pytest.raises(RuntimeError, match="prompt is required"):
        AtlasMinimaxH3MaxTurboTextToVideo().run(None, bad_prompt)


@pytest.mark.parametrize("bad_image", ["", "  \n \n"])
def test_i2v_requires_image(bad_image):
    with pytest.raises(RuntimeError, match="image is required"):
        AtlasMinimaxH3MaxTurboImageToVideo().run(None, bad_image, "a prompt")


@pytest.mark.parametrize("bad_prompt", ["", "  \n \n"])
def test_i2v_requires_prompt(bad_prompt):
    with pytest.raises(RuntimeError, match="prompt is required"):
        AtlasMinimaxH3MaxTurboImageToVideo().run(None, "https://example.com/a.png", bad_prompt)


def test_i2v_end_image_is_optional():
    inputs = AtlasMinimaxH3MaxTurboImageToVideo.INPUT_TYPES()
    assert "end_image" in inputs["optional"]
    assert inputs["optional"]["end_image"][1]["default"] == ""
    # Blank last frames must not be sent to the API.
    source = inspect.getsource(AtlasMinimaxH3MaxTurboImageToVideo.run)
    assert 'payload["end_image"] = end_image.strip()' in source


def test_new_nodes_registered():
    from src.atlascloud_comfyui.registry import (
        NODE_CLASS_MAPPINGS,
        NODE_DISPLAY_NAME_MAPPINGS,
    )

    for key, cls in (
        ("AtlasCloud MiniMax H3 Max Turbo Text-to-Video", AtlasMinimaxH3MaxTurboTextToVideo),
        ("AtlasCloud MiniMax H3 Max Turbo Image-to-Video", AtlasMinimaxH3MaxTurboImageToVideo),
    ):
        # registry.py imports under the `atlascloud_comfyui.*` path while the
        # tests import under `src.atlascloud_comfyui.*`, so compare by name.
        assert NODE_CLASS_MAPPINGS[key].__name__ == cls.__name__
        assert NODE_DISPLAY_NAME_MAPPINGS[key] == key
