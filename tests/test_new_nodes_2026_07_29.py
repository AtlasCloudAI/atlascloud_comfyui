"""Metadata-only tests for newly added nodes (2026-07-29).

New models: Youchuan V8.2 (text-to-image, image-to-image, blend,
remove-background, style-transfer, image-to-video).
These tests MUST NOT require ATLASCLOUD_API_KEY.
"""

import inspect

import pytest


def test_youchuan_v82_t2i_metadata():
    from src.atlascloud_comfyui.nodes.image.youchuan_v82_t2i import (
        AtlasYouchuanV82TextToImage,
    )

    required = AtlasYouchuanV82TextToImage.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert AtlasYouchuanV82TextToImage.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasYouchuanV82TextToImage.CATEGORY == "AtlasCloud/Image"


def test_youchuan_v82_i2i_metadata():
    from src.atlascloud_comfyui.nodes.image.youchuan_v82_i2i import (
        AtlasYouchuanV82ImageToImage,
    )

    required = AtlasYouchuanV82ImageToImage.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert "prompt" in required
    assert AtlasYouchuanV82ImageToImage.CATEGORY == "AtlasCloud/Image"


def test_youchuan_v82_blend_metadata():
    from src.atlascloud_comfyui.nodes.image.youchuan_v82_blend import (
        AtlasYouchuanV82Blend,
    )

    required = AtlasYouchuanV82Blend.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "images" in required
    assert AtlasYouchuanV82Blend.CATEGORY == "AtlasCloud/Image"


def test_youchuan_v82_remove_bg_metadata():
    from src.atlascloud_comfyui.nodes.image.youchuan_v82_remove_bg import (
        AtlasYouchuanV82RemoveBackground,
    )

    required = AtlasYouchuanV82RemoveBackground.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert AtlasYouchuanV82RemoveBackground.CATEGORY == "AtlasCloud/Image"


def test_youchuan_v82_style_transfer_metadata():
    from src.atlascloud_comfyui.nodes.image.youchuan_v82_style_transfer import (
        AtlasYouchuanV82StyleTransfer,
    )

    required = AtlasYouchuanV82StyleTransfer.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert "prompt" in required
    assert AtlasYouchuanV82StyleTransfer.CATEGORY == "AtlasCloud/Image"


def test_youchuan_v82_i2v_metadata():
    from src.atlascloud_comfyui.nodes.video.youchuan_v82_i2v import (
        AtlasYouchuanV82ImageToVideo,
    )

    required = AtlasYouchuanV82ImageToVideo.INPUT_TYPES()["required"]
    optional = AtlasYouchuanV82ImageToVideo.INPUT_TYPES()["optional"]
    assert "atlas_client" in required
    assert "image" in required
    assert optional["resolution"][0] == ["480p", "720p"]
    assert optional["motion"][0] == ["low", "high"]
    assert AtlasYouchuanV82ImageToVideo.RETURN_NAMES == ("video_url", "prediction_id")
    assert AtlasYouchuanV82ImageToVideo.CATEGORY == "AtlasCloud/Video"


def test_new_nodes_2026_07_29_registered():
    from src.atlascloud_comfyui.registry import (
        NODE_CLASS_MAPPINGS,
        NODE_DISPLAY_NAME_MAPPINGS,
    )

    for key in (
        "AtlasCloud Youchuan V8.2 Text-to-Image",
        "AtlasCloud Youchuan V8.2 Image-to-Image",
        "AtlasCloud Youchuan V8.2 Blend",
        "AtlasCloud Youchuan V8.2 Remove Background",
        "AtlasCloud Youchuan V8.2 Style Transfer",
        "AtlasCloud Youchuan V8.2 Image-to-Video",
    ):
        assert key in NODE_CLASS_MAPPINGS
        assert key in NODE_DISPLAY_NAME_MAPPINGS


@pytest.mark.parametrize(
    "module_path, class_name, model_id",
    [
        ("image.youchuan_v82_t2i", "AtlasYouchuanV82TextToImage", "youchuan/v8.2/text-to-image"),
        ("image.youchuan_v82_i2i", "AtlasYouchuanV82ImageToImage", "youchuan/v8.2/image-to-image"),
        ("image.youchuan_v82_blend", "AtlasYouchuanV82Blend", "youchuan/v8.2/blend"),
        ("image.youchuan_v82_remove_bg", "AtlasYouchuanV82RemoveBackground", "youchuan/v8.2/remove-background"),
        ("image.youchuan_v82_style_transfer", "AtlasYouchuanV82StyleTransfer", "youchuan/v8.2/style-transfer"),
        ("video.youchuan_v82_i2v", "AtlasYouchuanV82ImageToVideo", "youchuan/v8.2/image-to-video"),
    ],
)
def test_new_nodes_2026_07_29_model_ids(module_path, class_name, model_id):
    import importlib

    module = importlib.import_module(f"src.atlascloud_comfyui.nodes.{module_path}")
    node_cls = getattr(module, class_name)
    assert f'"model": "{model_id}"' in inspect.getsource(node_cls.run)
