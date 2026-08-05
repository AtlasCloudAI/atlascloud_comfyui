"""Metadata-only tests for newly added nodes (2026-08-05).

New models: Qwen Image 3.0 (Text-to-Image / Edit).
These tests MUST NOT require ATLASCLOUD_API_KEY.
"""

import inspect

import pytest


def test_qwen_image_30_t2i_metadata():
    from src.atlascloud_comfyui.nodes.image.qwen_image_30_t2i import (
        AtlasQwenImage30TextToImage,
    )

    inputs = AtlasQwenImage30TextToImage.INPUT_TYPES()
    required = inputs["required"]
    optional = inputs["optional"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert optional["n"][1]["min"] == 1
    assert optional["n"][1]["max"] == 4
    assert optional["n"][1]["default"] == 1
    assert optional["prompt_extend"][0] == "BOOLEAN"
    assert optional["prompt_extend"][1]["default"] is True
    assert optional["prompt_extend_mode"][0] == ["direct", "agent"]
    assert optional["prompt_extend_mode"][1]["default"] == "direct"
    assert optional["seed"][1]["min"] == -1
    assert AtlasQwenImage30TextToImage.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasQwenImage30TextToImage.RETURN_NAMES == ("image_url", "prediction_id")
    assert AtlasQwenImage30TextToImage.CATEGORY == "AtlasCloud/Image"


@pytest.mark.parametrize("bad_prompt", ["", "   "])
def test_qwen_image_30_t2i_requires_prompt(bad_prompt):
    from src.atlascloud_comfyui.nodes.image.qwen_image_30_t2i import (
        AtlasQwenImage30TextToImage,
    )

    with pytest.raises(RuntimeError, match="prompt is required"):
        AtlasQwenImage30TextToImage().run(None, bad_prompt)


def test_qwen_image_30_t2i_omits_optional_fields():
    from src.atlascloud_comfyui.nodes.image.qwen_image_30_t2i import (
        AtlasQwenImage30TextToImage,
    )

    source = inspect.getsource(AtlasQwenImage30TextToImage.run)
    assert 'payload["size"] = sz' in source
    assert 'payload["negative_prompt"] = neg' in source
    assert "if seed >= 0:" in source


def test_qwen_image_30_edit_metadata():
    from src.atlascloud_comfyui.nodes.image.qwen_image_30_edit import (
        AtlasQwenImage30Edit,
    )

    inputs = AtlasQwenImage30Edit.INPUT_TYPES()
    required = inputs["required"]
    optional = inputs["optional"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert "reference_image_urls" in required
    assert optional["n"][1]["max"] == 4
    assert optional["prompt_extend_mode"][0] == ["direct", "agent"]
    assert AtlasQwenImage30Edit.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasQwenImage30Edit.RETURN_NAMES == ("image_url", "prediction_id")
    assert AtlasQwenImage30Edit.CATEGORY == "AtlasCloud/Image"


def test_qwen_image_30_edit_requires_prompt():
    from src.atlascloud_comfyui.nodes.image.qwen_image_30_edit import (
        AtlasQwenImage30Edit,
    )

    with pytest.raises(RuntimeError, match="prompt is required"):
        AtlasQwenImage30Edit().run(None, "  ", "https://example.com/a.png")


@pytest.mark.parametrize("bad_refs", ["", "  \n \n"])
def test_qwen_image_30_edit_requires_reference_images(bad_refs):
    from src.atlascloud_comfyui.nodes.image.qwen_image_30_edit import (
        AtlasQwenImage30Edit,
    )

    with pytest.raises(RuntimeError, match="reference_image_urls is required"):
        AtlasQwenImage30Edit().run(None, "a prompt", bad_refs)


def test_qwen_image_30_edit_rejects_too_many_reference_images():
    from src.atlascloud_comfyui.nodes.image.qwen_image_30_edit import (
        AtlasQwenImage30Edit,
    )

    urls = "\n".join(f"https://example.com/{i}.png" for i in range(4))
    with pytest.raises(RuntimeError, match="reference_image_urls maxItems is 3"):
        AtlasQwenImage30Edit().run(None, "a prompt", urls)


def test_new_nodes_2026_08_05_registered():
    from src.atlascloud_comfyui.registry import (
        NODE_CLASS_MAPPINGS,
        NODE_DISPLAY_NAME_MAPPINGS,
    )

    keys = [
        "AtlasCloud Qwen Image 3.0 Text-to-Image",
        "AtlasCloud Qwen Image 3.0 Edit",
    ]
    for key in keys:
        assert key in NODE_CLASS_MAPPINGS
        assert key in NODE_DISPLAY_NAME_MAPPINGS


def test_new_nodes_2026_08_05_model_ids():
    from src.atlascloud_comfyui.nodes.image.qwen_image_30_edit import (
        AtlasQwenImage30Edit,
    )
    from src.atlascloud_comfyui.nodes.image.qwen_image_30_t2i import (
        AtlasQwenImage30TextToImage,
    )

    expected = [
        (AtlasQwenImage30TextToImage, "qwen-image-3.0/text-to-image"),
        (AtlasQwenImage30Edit, "qwen-image-3.0/edit"),
    ]
    for cls, model_id in expected:
        source = inspect.getsource(cls.run)
        assert f'"model": "{model_id}"' in source
