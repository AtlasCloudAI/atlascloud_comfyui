"""Metadata-only tests for newly added nodes (2026-09-14).

New models: the GPT Image 2.5 Developer tiers — Sunburst Developer and Flare
Developer, each with a Text-to-Image and an Edit variant. They share the
gpt-image-2.5 request schema (size up to 3840x2160, background, webp output,
Edit takes up to 16 images) but the developer schemas drop `quality`
altogether, and Edit-Developer additionally drops `mask`. These tests pin the
model ids so a developer tier cannot silently fall back to its consumer sibling,
and pin the dropped knobs.
These tests MUST NOT require ATLASCLOUD_API_KEY.
"""

import inspect

import pytest

from src.atlascloud_comfyui.nodes.image.openai_gpt_image_25_flare_developer_edit import (
    AtlasOpenAIGPTImage25FlareDeveloperEdit,
)
from src.atlascloud_comfyui.nodes.image.openai_gpt_image_25_flare_developer_t2i import (
    AtlasOpenAIGPTImage25FlareDeveloperTextToImage,
)
from src.atlascloud_comfyui.nodes.image.openai_gpt_image_25_sunburst_developer_edit import (
    AtlasOpenAIGPTImage25SunburstDeveloperEdit,
)
from src.atlascloud_comfyui.nodes.image.openai_gpt_image_25_sunburst_developer_t2i import (
    AtlasOpenAIGPTImage25SunburstDeveloperTextToImage,
)

_MODEL_IDS = {
    AtlasOpenAIGPTImage25SunburstDeveloperTextToImage: "openai/gpt-image-2.5-sunburst-developer/text-to-image",
    AtlasOpenAIGPTImage25SunburstDeveloperEdit: "openai/gpt-image-2.5-sunburst-developer/edit",
    AtlasOpenAIGPTImage25FlareDeveloperTextToImage: "openai/gpt-image-2.5-flare-developer/text-to-image",
    AtlasOpenAIGPTImage25FlareDeveloperEdit: "openai/gpt-image-2.5-flare-developer/edit",
}

_CLASSES = list(_MODEL_IDS)

_T2I_CLASSES = [
    AtlasOpenAIGPTImage25SunburstDeveloperTextToImage,
    AtlasOpenAIGPTImage25FlareDeveloperTextToImage,
]

_EDIT_CLASSES = [
    AtlasOpenAIGPTImage25SunburstDeveloperEdit,
    AtlasOpenAIGPTImage25FlareDeveloperEdit,
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
    "cls, forbidden_prefixes",
    [
        (
            AtlasOpenAIGPTImage25SunburstDeveloperTextToImage,
            (
                '"model": "openai/gpt-image-2.5-sunburst/',
                '"model": "openai/gpt-image-2.5-flare',
                '"model": "openai/gpt-image-2/',
            ),
        ),
        (
            AtlasOpenAIGPTImage25SunburstDeveloperEdit,
            (
                '"model": "openai/gpt-image-2.5-sunburst/',
                '"model": "openai/gpt-image-2.5-flare',
                '"model": "openai/gpt-image-2/',
            ),
        ),
        (
            AtlasOpenAIGPTImage25FlareDeveloperTextToImage,
            (
                '"model": "openai/gpt-image-2.5-flare/',
                '"model": "openai/gpt-image-2.5-sunburst',
                '"model": "openai/gpt-image-2/',
            ),
        ),
        (
            AtlasOpenAIGPTImage25FlareDeveloperEdit,
            (
                '"model": "openai/gpt-image-2.5-flare/',
                '"model": "openai/gpt-image-2.5-sunburst',
                '"model": "openai/gpt-image-2/',
            ),
        ),
    ],
)
def test_does_not_fall_back_to_sibling_tier(cls, forbidden_prefixes):
    source = inspect.getsource(cls.run)
    for prefix in forbidden_prefixes:
        assert prefix not in source


@pytest.mark.parametrize("cls", _CLASSES)
def test_developer_tier_has_no_quality(cls):
    # The developer schemas drop `quality` entirely, unlike the consumer tiers.
    inputs = cls.INPUT_TYPES()
    assert "quality" not in inputs["required"]
    assert "quality" not in inputs["optional"]
    assert '"quality"' not in inspect.getsource(cls.run)


@pytest.mark.parametrize("cls", _CLASSES)
def test_size_covers_high_resolution_tiers(cls):
    size = cls.INPUT_TYPES()["optional"]["size"]
    assert size[1]["default"] == "1024x1024"
    assert size[0][0] == "auto"
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
def test_edit_developer_has_no_mask(cls):
    # Unlike the consumer Edit tiers, the developer Edit schema has no `mask`.
    inputs = cls.INPUT_TYPES()
    assert "mask" not in inputs["required"]
    assert "mask" not in inputs["optional"]
    assert '"mask"' not in inspect.getsource(cls.run)


def test_new_nodes_registered():
    from src.atlascloud_comfyui.registry import (
        NODE_CLASS_MAPPINGS,
        NODE_DISPLAY_NAME_MAPPINGS,
    )

    for key, cls in (
        ("AtlasCloud GPT Image-2.5 Sunburst Developer Text-to-Image", AtlasOpenAIGPTImage25SunburstDeveloperTextToImage),
        ("AtlasCloud GPT Image-2.5 Sunburst Developer Edit", AtlasOpenAIGPTImage25SunburstDeveloperEdit),
        ("AtlasCloud GPT Image-2.5 Flare Developer Text-to-Image", AtlasOpenAIGPTImage25FlareDeveloperTextToImage),
        ("AtlasCloud GPT Image-2.5 Flare Developer Edit", AtlasOpenAIGPTImage25FlareDeveloperEdit),
    ):
        # registry.py imports under the `atlascloud_comfyui.*` path while the
        # tests import under `src.atlascloud_comfyui.*`, so compare by name.
        assert NODE_CLASS_MAPPINGS[key].__name__ == cls.__name__
        assert NODE_DISPLAY_NAME_MAPPINGS[key] == key
