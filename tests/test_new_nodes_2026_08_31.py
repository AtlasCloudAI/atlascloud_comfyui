"""Metadata-only tests for newly added nodes (2026-08-31).

New models: the Seedream v4.7 family (Text-to-Image / Sequential / Edit /
Edit Sequential). Unlike the v4/v4.5 nodes, v4.7 takes `num_images` (not
`max_images`, max 14) and a `prompt_expansion_mode` switch, and its base
text-to-image endpoint is suffixed `/text-to-image` rather than being the bare
family id — so these tests pin both the model ids and the payload keys.
These tests MUST NOT require ATLASCLOUD_API_KEY.
"""

import inspect

import pytest

from src.atlascloud_comfyui.nodes.image.seedream_v47_edit import AtlasSeedreamV47Edit
from src.atlascloud_comfyui.nodes.image.seedream_v47_edit_sequential import (
    AtlasSeedreamV47EditSequential,
)
from src.atlascloud_comfyui.nodes.image.seedream_v47_sequential_t2i import (
    AtlasSeedreamV47SequentialTextToImage,
)
from src.atlascloud_comfyui.nodes.image.seedream_v47_t2i import (
    SEEDREAM_V47_SIZES,
    AtlasSeedreamV47TextToImage,
)

_V47_CLASSES = [
    AtlasSeedreamV47TextToImage,
    AtlasSeedreamV47SequentialTextToImage,
    AtlasSeedreamV47Edit,
    AtlasSeedreamV47EditSequential,
]

_V47_MODEL_IDS = {
    AtlasSeedreamV47TextToImage: "bytedance/seedream-v4.7/text-to-image",
    AtlasSeedreamV47SequentialTextToImage: "bytedance/seedream-v4.7/sequential",
    AtlasSeedreamV47Edit: "bytedance/seedream-v4.7/edit",
    AtlasSeedreamV47EditSequential: "bytedance/seedream-v4.7/edit-sequential",
}

_EDIT_CLASSES = [AtlasSeedreamV47Edit, AtlasSeedreamV47EditSequential]
_SEQUENTIAL_CLASSES = [AtlasSeedreamV47SequentialTextToImage, AtlasSeedreamV47EditSequential]


@pytest.mark.parametrize("cls", _V47_CLASSES)
def test_v47_node_shape(cls):
    inputs = cls.INPUT_TYPES()
    assert "atlas_client" in inputs["required"]
    assert "prompt" in inputs["required"]
    assert "size" in inputs["required"]
    assert "poll_interval_sec" in inputs["optional"]
    assert "timeout_sec" in inputs["optional"]
    assert cls.RETURN_TYPES == ("STRING", "STRING")
    assert cls.RETURN_NAMES == ("image_url", "prediction_id")
    assert cls.CATEGORY == "AtlasCloud/Image"
    assert cls.FUNCTION == "run"


@pytest.mark.parametrize("cls", _V47_CLASSES)
def test_v47_model_id(cls):
    source = inspect.getsource(cls.run)
    assert f'"model": "{_V47_MODEL_IDS[cls]}"' in source
    # must not fall back to an older Seedream generation
    assert '"model": "bytedance/seedream-v4.5' not in source
    assert '"model": "bytedance/seedream-v4"' not in source


@pytest.mark.parametrize("cls", _V47_CLASSES)
def test_v47_size_presets(cls):
    size = cls.INPUT_TYPES()["required"]["size"]
    assert size[0] == SEEDREAM_V47_SIZES
    assert size[1]["default"] == "2048*2048"
    # the 1K, 2K and 4K tiers are all offered
    assert "1024*1024" in SEEDREAM_V47_SIZES
    assert "2048*2048" in SEEDREAM_V47_SIZES
    assert "4096*4096" in SEEDREAM_V47_SIZES


@pytest.mark.parametrize("cls", _V47_CLASSES)
def test_v47_prompt_expansion_mode(cls):
    optional = cls.INPUT_TYPES()["optional"]
    assert optional["prompt_expansion_mode"][0] == ["standard", "fast"]
    assert optional["prompt_expansion_mode"][1]["default"] == "standard"
    assert '"prompt_expansion_mode": prompt_expansion_mode' in inspect.getsource(cls.run)


@pytest.mark.parametrize("cls", _SEQUENTIAL_CLASSES)
def test_v47_sequential_num_images(cls):
    num_images = cls.INPUT_TYPES()["required"]["num_images"]
    assert num_images[0] == "INT"
    assert num_images[1]["default"] == 1
    assert num_images[1]["min"] == 1
    assert num_images[1]["max"] == 14
    source = inspect.getsource(cls.run)
    assert '"num_images": int(num_images)' in source
    # v4.7 renamed the v4/v4.5 `max_images` field
    assert "max_images" not in source


@pytest.mark.parametrize("cls", [AtlasSeedreamV47TextToImage, AtlasSeedreamV47SequentialTextToImage])
def test_v47_t2i_has_no_images_input(cls):
    inputs = cls.INPUT_TYPES()
    assert "images" not in inputs["required"]
    assert "images" not in inputs["optional"]


def test_v47_t2i_requires_prompt():
    with pytest.raises(RuntimeError, match="prompt is required"):
        AtlasSeedreamV47TextToImage().run(None, "   ")


def test_v47_sequential_requires_prompt():
    with pytest.raises(RuntimeError, match="prompt is required"):
        AtlasSeedreamV47SequentialTextToImage().run(None, "")


@pytest.mark.parametrize("cls", _EDIT_CLASSES)
def test_v47_edit_images_input(cls):
    assert "images" in cls.INPUT_TYPES()["required"]


@pytest.mark.parametrize("cls", _EDIT_CLASSES)
@pytest.mark.parametrize("bad_images", ["", "  \n \n"])
def test_v47_edit_requires_images(cls, bad_images):
    with pytest.raises(RuntimeError, match="images is required"):
        cls().run(None, bad_images, "a prompt")


@pytest.mark.parametrize("cls", _EDIT_CLASSES)
def test_v47_edit_rejects_more_than_ten_images(cls):
    images = "\n".join(f"https://example.com/{i}.png" for i in range(11))
    with pytest.raises(RuntimeError, match="images maxItems is 10"):
        cls().run(None, images, "a prompt")


@pytest.mark.parametrize("cls", _EDIT_CLASSES)
def test_v47_edit_requires_prompt(cls):
    with pytest.raises(RuntimeError, match="prompt is required"):
        cls().run(None, "https://example.com/a.png", "  ")


def test_v47_nodes_registered():
    from src.atlascloud_comfyui.registry import (
        NODE_CLASS_MAPPINGS,
        NODE_DISPLAY_NAME_MAPPINGS,
    )

    for key, cls in (
        ("AtlasCloud Seedream V4.7 Text-to-Image", AtlasSeedreamV47TextToImage),
        ("AtlasCloud Seedream V4.7 Sequential Text-to-Image", AtlasSeedreamV47SequentialTextToImage),
        ("AtlasCloud Seedream V4.7 Edit", AtlasSeedreamV47Edit),
        ("AtlasCloud Seedream V4.7 Edit Sequential", AtlasSeedreamV47EditSequential),
    ):
        # registry.py imports under the `atlascloud_comfyui.*` path while the
        # tests import under `src.atlascloud_comfyui.*`, so compare by name.
        assert NODE_CLASS_MAPPINGS[key].__name__ == cls.__name__
        assert NODE_DISPLAY_NAME_MAPPINGS[key] == key
