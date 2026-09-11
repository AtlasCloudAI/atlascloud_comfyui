"""Metadata-only tests for newly added nodes (2026-09-11).

New models: the MAI-Image-2.6 family (flagship + flash, Text-to-Image + Edit).
2.6 changed its request schema relative to 2.5: `size` now defaults to
"default" and accepts the special values "default"/"auto", edit takes a
`reference_images` array of 1-5 items instead of a single `image` string, and
both variants accept `enable_web_search`. These tests pin the model ids so a
2.6 node cannot silently fall back to a 2.5 tier, and pin those schema deltas.
These tests MUST NOT require ATLASCLOUD_API_KEY.
"""

import inspect

import pytest

from src.atlascloud_comfyui.nodes.image.mai_image_26_edit import AtlasMAIImage26Edit
from src.atlascloud_comfyui.nodes.image.mai_image_26_flash_edit import (
    AtlasMAIImage26FlashEdit,
)
from src.atlascloud_comfyui.nodes.image.mai_image_26_flash_t2i import (
    AtlasMAIImage26FlashTextToImage,
)
from src.atlascloud_comfyui.nodes.image.mai_image_26_t2i import (
    AtlasMAIImage26TextToImage,
)

_MODEL_IDS = {
    AtlasMAIImage26TextToImage: "microsoft/mai-image-2.6/text-to-image",
    AtlasMAIImage26FlashTextToImage: "microsoft/mai-image-2.6-flash/text-to-image",
    AtlasMAIImage26Edit: "microsoft/mai-image-2.6/edit",
    AtlasMAIImage26FlashEdit: "microsoft/mai-image-2.6-flash/edit",
}

_CLASSES = list(_MODEL_IDS)
_T2I_CLASSES = [AtlasMAIImage26TextToImage, AtlasMAIImage26FlashTextToImage]
_EDIT_CLASSES = [AtlasMAIImage26Edit, AtlasMAIImage26FlashEdit]


@pytest.mark.parametrize("cls", _CLASSES)
def test_node_shape(cls):
    inputs = cls.INPUT_TYPES()
    assert "atlas_client" in inputs["required"]
    assert "prompt" in inputs["required"]
    assert "poll_interval_sec" in inputs["optional"]
    assert "timeout_sec" in inputs["optional"]
    assert cls.RETURN_TYPES == ("STRING", "STRING")
    assert cls.CATEGORY == "AtlasCloud/Image"
    assert cls.RETURN_NAMES == ("image_url", "prediction_id")


@pytest.mark.parametrize("cls", _CLASSES)
def test_model_id(cls):
    source = inspect.getsource(cls.run)
    assert f'"model": "{_MODEL_IDS[cls]}"' in source


@pytest.mark.parametrize("cls", _CLASSES)
def test_does_not_fall_back_to_older_family(cls):
    source = inspect.getsource(cls.run)
    for prefix in (
        '"model": "microsoft/mai-image-2.5/',
        '"model": "microsoft/mai-image-2.5-flash/',
        '"model": "microsoft/mai-image-2.5-pro/',
    ):
        assert prefix not in source


@pytest.mark.parametrize("cls", _CLASSES)
def test_web_search_is_wired(cls):
    assert "enable_web_search" in cls.INPUT_TYPES()["optional"]
    assert '"enable_web_search": bool(enable_web_search)' in inspect.getsource(cls.run)


@pytest.mark.parametrize("cls", _T2I_CLASSES)
def test_t2i_size_is_free_form_and_defaults_to_default(cls):
    size = cls.INPUT_TYPES()["optional"]["size"]
    assert size[0] == "STRING"
    assert size[1]["default"] == "default"


@pytest.mark.parametrize("cls", _T2I_CLASSES)
def test_t2i_has_no_image_inputs(cls):
    inputs = cls.INPUT_TYPES()
    for key in ("image", "reference_images"):
        assert key not in inputs["required"]
        assert key not in inputs["optional"]


@pytest.mark.parametrize("cls", _EDIT_CLASSES)
def test_edit_size_is_default_or_auto(cls):
    size = cls.INPUT_TYPES()["optional"]["size"]
    assert size[0] == ["default", "auto"]
    assert size[1]["default"] == "default"


@pytest.mark.parametrize("cls", _EDIT_CLASSES)
def test_edit_takes_reference_images_not_single_image(cls):
    inputs = cls.INPUT_TYPES()
    assert "reference_images" in inputs["required"]
    assert inputs["required"]["reference_images"][1]["multiline"] is True
    assert "image" not in inputs["required"]
    assert "image" not in inputs["optional"]


@pytest.mark.parametrize("cls", _CLASSES)
@pytest.mark.parametrize("bad_prompt", ["", "  \n \n"])
def test_requires_prompt(cls, bad_prompt):
    args = (bad_prompt, "https://example.com/a.png") if cls in _EDIT_CLASSES else (bad_prompt,)
    with pytest.raises(RuntimeError, match="prompt is required"):
        cls().run(None, *args)


@pytest.mark.parametrize("cls", _EDIT_CLASSES)
@pytest.mark.parametrize("bad_images", ["", "  \n \n"])
def test_edit_requires_reference_images(cls, bad_images):
    with pytest.raises(RuntimeError, match="reference_images is required"):
        cls().run(None, "a prompt", bad_images)


@pytest.mark.parametrize("cls", _EDIT_CLASSES)
def test_edit_rejects_more_than_five_reference_images(cls):
    too_many = "\n".join(f"https://example.com/{i}.png" for i in range(6))
    with pytest.raises(RuntimeError, match="maxItems is 5"):
        cls().run(None, "a prompt", too_many)


def test_new_nodes_registered():
    from src.atlascloud_comfyui.registry import (
        NODE_CLASS_MAPPINGS,
        NODE_DISPLAY_NAME_MAPPINGS,
    )

    for key, cls in (
        ("AtlasCloud MAI-Image-2.6 Text-to-Image", AtlasMAIImage26TextToImage),
        ("AtlasCloud MAI-Image-2.6-Flash Text-to-Image", AtlasMAIImage26FlashTextToImage),
        ("AtlasCloud MAI-Image-2.6 Edit", AtlasMAIImage26Edit),
        ("AtlasCloud MAI-Image-2.6-Flash Edit", AtlasMAIImage26FlashEdit),
    ):
        # registry.py imports under the `atlascloud_comfyui.*` path while the
        # tests import under `src.atlascloud_comfyui.*`, so compare by name.
        assert NODE_CLASS_MAPPINGS[key].__name__ == cls.__name__
        assert NODE_DISPLAY_NAME_MAPPINGS[key] == key
