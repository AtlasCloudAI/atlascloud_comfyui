"""Metadata-only tests for newly added nodes (2026-09-09).

New models: the GPT Image 2.5 Sunburst pair (Text-to-Image / Edit) and the GPT
Image 2.5 Flare pair. Both tiers share the gpt-image-2.5 request schema, which
differs from gpt-image-2: quality gains the `xhigh` / `max` tiers, `size`
stretches up to 3840x2160, `background` and `webp` output arrive, and Edit takes
up to 16 images plus an optional mask. These tests pin the model ids so a tier
cannot silently fall back to its sibling, and pin the schema deltas.
These tests MUST NOT require ATLASCLOUD_API_KEY.
"""

import inspect

import pytest

from src.atlascloud_comfyui.nodes.image.openai_gpt_image_25_flare_edit import (
    AtlasOpenAIGPTImage25FlareEdit,
)
from src.atlascloud_comfyui.nodes.image.openai_gpt_image_25_flare_t2i import (
    AtlasOpenAIGPTImage25FlareTextToImage,
)
from src.atlascloud_comfyui.nodes.image.openai_gpt_image_25_sunburst_edit import (
    AtlasOpenAIGPTImage25SunburstEdit,
)
from src.atlascloud_comfyui.nodes.image.openai_gpt_image_25_sunburst_t2i import (
    AtlasOpenAIGPTImage25SunburstTextToImage,
)

_MODEL_IDS = {
    AtlasOpenAIGPTImage25SunburstTextToImage: "openai/gpt-image-2.5-sunburst/text-to-image",
    AtlasOpenAIGPTImage25SunburstEdit: "openai/gpt-image-2.5-sunburst/edit",
    AtlasOpenAIGPTImage25FlareTextToImage: "openai/gpt-image-2.5-flare/text-to-image",
    AtlasOpenAIGPTImage25FlareEdit: "openai/gpt-image-2.5-flare/edit",
}

_CLASSES = list(_MODEL_IDS)

_T2I_CLASSES = [
    AtlasOpenAIGPTImage25SunburstTextToImage,
    AtlasOpenAIGPTImage25FlareTextToImage,
]

_EDIT_CLASSES = [
    AtlasOpenAIGPTImage25SunburstEdit,
    AtlasOpenAIGPTImage25FlareEdit,
]


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


@pytest.mark.parametrize(
    "cls, sibling_prefixes",
    [
        (
            AtlasOpenAIGPTImage25SunburstTextToImage,
            ('"model": "openai/gpt-image-2/', '"model": "openai/gpt-image-2.5-flare/'),
        ),
        (
            AtlasOpenAIGPTImage25SunburstEdit,
            ('"model": "openai/gpt-image-2/', '"model": "openai/gpt-image-2.5-flare/'),
        ),
        (
            AtlasOpenAIGPTImage25FlareTextToImage,
            ('"model": "openai/gpt-image-2/', '"model": "openai/gpt-image-2.5-sunburst/'),
        ),
        (
            AtlasOpenAIGPTImage25FlareEdit,
            ('"model": "openai/gpt-image-2/', '"model": "openai/gpt-image-2.5-sunburst/'),
        ),
    ],
)
def test_does_not_fall_back_to_sibling_tier(cls, sibling_prefixes):
    source = inspect.getsource(cls.run)
    for prefix in sibling_prefixes:
        assert prefix not in source


@pytest.mark.parametrize("cls", _CLASSES)
def test_quality_adds_xhigh_and_max(cls):
    quality = cls.INPUT_TYPES()["optional"]["quality"]
    assert quality[0] == ["auto", "low", "medium", "high", "xhigh", "max"]
    assert quality[1]["default"] == "medium"


@pytest.mark.parametrize("cls", _CLASSES)
def test_size_covers_high_resolution_tiers(cls):
    size = cls.INPUT_TYPES()["optional"]["size"]
    assert size[1]["default"] == "1024x1024"
    assert size[0][0] == "auto"
    # gpt-image-2.5 goes past the 1536x1024 ceiling of gpt-image-2.
    for expected in ("2048x2048", "2880x2160", "3840x2160", "2160x3840"):
        assert expected in size[0]


@pytest.mark.parametrize("cls", _CLASSES)
def test_background_and_output_format(cls):
    optional = cls.INPUT_TYPES()["optional"]
    assert optional["background"][0] == ["auto", "opaque", "transparent"]
    assert optional["background"][1]["default"] == "auto"
    assert optional["output_format"][0] == ["png", "jpeg", "webp"]
    assert optional["output_format"][1]["default"] == "png"
    assert optional["moderation"][0] == ["auto", "low"]


@pytest.mark.parametrize("cls", _T2I_CLASSES)
def test_t2i_has_no_image_inputs(cls):
    inputs = cls.INPUT_TYPES()
    for key in ("images", "mask"):
        assert key not in inputs["required"]
        assert key not in inputs["optional"]


@pytest.mark.parametrize("cls", _T2I_CLASSES)
@pytest.mark.parametrize("bad_prompt", ["", "  \n \n"])
def test_t2i_requires_prompt(cls, bad_prompt):
    with pytest.raises(RuntimeError, match="prompt is required"):
        cls().run(None, bad_prompt)


@pytest.mark.parametrize("cls", _EDIT_CLASSES)
@pytest.mark.parametrize("bad_prompt", ["", "  \n \n"])
def test_edit_requires_prompt(cls, bad_prompt):
    with pytest.raises(RuntimeError, match="prompt is required"):
        cls().run(None, bad_prompt, "https://example.com/a.png")


@pytest.mark.parametrize("cls", _EDIT_CLASSES)
def test_edit_images_bounds(cls):
    node = cls()
    with pytest.raises(RuntimeError, match="images is required"):
        node.run(None, "a prompt", "   \n  ")
    too_many = "\n".join(f"https://example.com/{i}.png" for i in range(17))
    with pytest.raises(RuntimeError, match="images maxItems is 16"):
        node.run(None, "a prompt", too_many)


@pytest.mark.parametrize("cls", _EDIT_CLASSES)
def test_edit_mask_is_optional(cls):
    inputs = cls.INPUT_TYPES()
    assert "mask" in inputs["optional"]
    assert inputs["optional"]["mask"][1]["default"] == ""
    # Blank masks must not be sent to the API.
    source = inspect.getsource(cls.run)
    assert 'payload["mask"] = m' in source


def test_new_nodes_registered():
    from src.atlascloud_comfyui.registry import (
        NODE_CLASS_MAPPINGS,
        NODE_DISPLAY_NAME_MAPPINGS,
    )

    for key, cls in (
        ("AtlasCloud GPT Image-2.5 Sunburst Text-to-Image", AtlasOpenAIGPTImage25SunburstTextToImage),
        ("AtlasCloud GPT Image-2.5 Sunburst Edit", AtlasOpenAIGPTImage25SunburstEdit),
        ("AtlasCloud GPT Image-2.5 Flare Text-to-Image", AtlasOpenAIGPTImage25FlareTextToImage),
        ("AtlasCloud GPT Image-2.5 Flare Edit", AtlasOpenAIGPTImage25FlareEdit),
    ):
        # registry.py imports under the `atlascloud_comfyui.*` path while the
        # tests import under `src.atlascloud_comfyui.*`, so compare by name.
        assert NODE_CLASS_MAPPINGS[key].__name__ == cls.__name__
        assert NODE_DISPLAY_NAME_MAPPINGS[key] == key
