"""Metadata-only tests for newly added nodes (2026-08-19).

New models: Qwen Image 3.0 Pro (Text-to-Image / Edit).
These tests MUST NOT require ATLASCLOUD_API_KEY.
"""

import inspect

import pytest


def test_qwen_image_30_pro_t2i_metadata():
    from src.atlascloud_comfyui.nodes.image.qwen_image_30_pro_t2i import (
        AtlasQwenImage30ProTextToImage,
    )

    inputs = AtlasQwenImage30ProTextToImage.INPUT_TYPES()
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
    assert "poll_interval_sec" in optional
    assert "timeout_sec" in optional
    assert AtlasQwenImage30ProTextToImage.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasQwenImage30ProTextToImage.RETURN_NAMES == ("image_url", "prediction_id")
    assert AtlasQwenImage30ProTextToImage.CATEGORY == "AtlasCloud/Image"


@pytest.mark.parametrize("bad_prompt", ["", "   "])
def test_qwen_image_30_pro_t2i_requires_prompt(bad_prompt):
    from src.atlascloud_comfyui.nodes.image.qwen_image_30_pro_t2i import (
        AtlasQwenImage30ProTextToImage,
    )

    with pytest.raises(RuntimeError, match="prompt is required"):
        AtlasQwenImage30ProTextToImage().run(None, bad_prompt)


def test_qwen_image_30_pro_t2i_omits_optional_fields():
    from src.atlascloud_comfyui.nodes.image.qwen_image_30_pro_t2i import (
        AtlasQwenImage30ProTextToImage,
    )

    source = inspect.getsource(AtlasQwenImage30ProTextToImage.run)
    assert 'payload["size"] = sz' in source
    assert 'payload["negative_prompt"] = neg' in source
    assert "if seed >= 0:" in source


def test_qwen_image_30_pro_edit_metadata():
    from src.atlascloud_comfyui.nodes.image.qwen_image_30_pro_edit import (
        AtlasQwenImage30ProEdit,
    )

    inputs = AtlasQwenImage30ProEdit.INPUT_TYPES()
    required = inputs["required"]
    optional = inputs["optional"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert "reference_image_urls" in required
    assert optional["n"][1]["max"] == 4
    # The pro/edit schema only exposes the single-pass "direct" rewrite strategy.
    assert optional["prompt_extend_mode"][0] == ["direct"]
    assert optional["prompt_extend_mode"][1]["default"] == "direct"
    assert AtlasQwenImage30ProEdit.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasQwenImage30ProEdit.RETURN_NAMES == ("image_url", "prediction_id")
    assert AtlasQwenImage30ProEdit.CATEGORY == "AtlasCloud/Image"


def test_qwen_image_30_pro_edit_requires_prompt():
    from src.atlascloud_comfyui.nodes.image.qwen_image_30_pro_edit import (
        AtlasQwenImage30ProEdit,
    )

    with pytest.raises(RuntimeError, match="prompt is required"):
        AtlasQwenImage30ProEdit().run(None, "  ", "https://example.com/a.png")


@pytest.mark.parametrize("bad_refs", ["", "  \n \n"])
def test_qwen_image_30_pro_edit_requires_reference_images(bad_refs):
    from src.atlascloud_comfyui.nodes.image.qwen_image_30_pro_edit import (
        AtlasQwenImage30ProEdit,
    )

    with pytest.raises(RuntimeError, match="reference_image_urls is required"):
        AtlasQwenImage30ProEdit().run(None, "a prompt", bad_refs)


def test_qwen_image_30_pro_edit_rejects_too_many_reference_images():
    from src.atlascloud_comfyui.nodes.image.qwen_image_30_pro_edit import (
        AtlasQwenImage30ProEdit,
    )

    urls = "\n".join(f"https://example.com/{i}.png" for i in range(4))
    with pytest.raises(RuntimeError, match="reference_image_urls maxItems is 3"):
        AtlasQwenImage30ProEdit().run(None, "a prompt", urls)


def test_new_nodes_2026_08_19_registered():
    from src.atlascloud_comfyui.registry import (
        NODE_CLASS_MAPPINGS,
        NODE_DISPLAY_NAME_MAPPINGS,
    )

    keys = [
        "AtlasCloud Qwen Image 3.0 Pro Text-to-Image",
        "AtlasCloud Qwen Image 3.0 Pro Edit",
    ]
    for key in keys:
        assert key in NODE_CLASS_MAPPINGS
        assert key in NODE_DISPLAY_NAME_MAPPINGS


def test_new_nodes_2026_08_19_model_ids():
    from src.atlascloud_comfyui.nodes.image.qwen_image_30_pro_edit import (
        AtlasQwenImage30ProEdit,
    )
    from src.atlascloud_comfyui.nodes.image.qwen_image_30_pro_t2i import (
        AtlasQwenImage30ProTextToImage,
    )

    expected = [
        (AtlasQwenImage30ProTextToImage, "qwen-image-3.0-pro/text-to-image"),
        (AtlasQwenImage30ProEdit, "qwen-image-3.0-pro/edit"),
    ]
    for cls, model_id in expected:
        source = inspect.getsource(cls.run)
        assert f'"model": "{model_id}"' in source
