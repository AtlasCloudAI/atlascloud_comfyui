"""Metadata-only tests for newly added nodes (2026-09-04).

New models: the MAI-Image-2.5-Pro image pair (Text-to-Image / Edit). The Pro
tier shares the request schema of the existing `microsoft/mai-image-2.5/*`
nodes, so these tests mainly pin the model ids to make sure the Pro nodes do
not silently fall back to the base or `-flash` tiers.
These tests MUST NOT require ATLASCLOUD_API_KEY.
"""

import inspect

import pytest

from src.atlascloud_comfyui.nodes.image.mai_image_25_pro_edit import (
    AtlasMAIImage25ProEdit,
)
from src.atlascloud_comfyui.nodes.image.mai_image_25_pro_t2i import (
    AtlasMAIImage25ProTextToImage,
)

_PRO_MODEL_IDS = {
    AtlasMAIImage25ProTextToImage: "microsoft/mai-image-2.5-pro/text-to-image",
    AtlasMAIImage25ProEdit: "microsoft/mai-image-2.5-pro/edit",
}

_PRO_CLASSES = list(_PRO_MODEL_IDS)


@pytest.mark.parametrize("cls", _PRO_CLASSES)
def test_mai_pro_node_shape(cls):
    inputs = cls.INPUT_TYPES()
    assert "atlas_client" in inputs["required"]
    assert "prompt" in inputs["required"]
    assert "enable_sync_mode" in inputs["optional"]
    assert "enable_base64_output" in inputs["optional"]
    assert "poll_interval_sec" in inputs["optional"]
    assert "timeout_sec" in inputs["optional"]
    assert cls.RETURN_TYPES == ("STRING", "STRING")
    assert cls.RETURN_NAMES == ("image_url", "prediction_id")
    assert cls.CATEGORY == "AtlasCloud/Image"
    assert cls.FUNCTION == "run"


@pytest.mark.parametrize("cls", _PRO_CLASSES)
def test_mai_pro_model_id(cls):
    source = inspect.getsource(cls.run)
    assert f'"model": "{_PRO_MODEL_IDS[cls]}"' in source
    # must not fall back to the base or flash tiers
    assert '"model": "microsoft/mai-image-2.5/' not in source
    assert '"model": "microsoft/mai-image-2.5-flash/' not in source


@pytest.mark.parametrize("cls", _PRO_CLASSES)
@pytest.mark.parametrize("bad_prompt", ["", "  \n \n"])
def test_mai_pro_requires_prompt(cls, bad_prompt):
    args = ("https://example.com/a.png",) if cls is AtlasMAIImage25ProEdit else ()
    with pytest.raises(RuntimeError, match="prompt is required"):
        cls().run(None, bad_prompt, *args)


def test_mai_pro_t2i_size_default():
    size = AtlasMAIImage25ProTextToImage.INPUT_TYPES()["optional"]["size"]
    assert size[0] == "STRING"
    assert size[1]["default"] == "1024*1024"


def test_mai_pro_t2i_has_no_image_input():
    inputs = AtlasMAIImage25ProTextToImage.INPUT_TYPES()
    assert "image" not in inputs["required"]
    assert "image" not in inputs["optional"]


def test_mai_pro_edit_image_input():
    inputs = AtlasMAIImage25ProEdit.INPUT_TYPES()
    assert "image" in inputs["required"]
    # the edit schema exposes no size control
    assert "size" not in inputs["optional"]


@pytest.mark.parametrize("bad_image", ["", "   "])
def test_mai_pro_edit_requires_image(bad_image):
    with pytest.raises(RuntimeError, match="image is required"):
        AtlasMAIImage25ProEdit().run(None, "a prompt", bad_image)


def test_mai_pro_nodes_registered():
    from src.atlascloud_comfyui.registry import (
        NODE_CLASS_MAPPINGS,
        NODE_DISPLAY_NAME_MAPPINGS,
    )

    for key, cls in (
        ("AtlasCloud MAI-Image-2.5-Pro Text-to-Image", AtlasMAIImage25ProTextToImage),
        ("AtlasCloud MAI-Image-2.5-Pro Edit", AtlasMAIImage25ProEdit),
    ):
        # registry.py imports under the `atlascloud_comfyui.*` path while the
        # tests import under `src.atlascloud_comfyui.*`, so compare by name.
        assert NODE_CLASS_MAPPINGS[key].__name__ == cls.__name__
        assert NODE_DISPLAY_NAME_MAPPINGS[key] == key
