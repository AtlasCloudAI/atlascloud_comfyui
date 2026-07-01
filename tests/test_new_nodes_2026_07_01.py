"""Metadata-only tests for newly added nodes (2026-07-01).

Nano Banana 2 Lite family: text-to-image (+ developer) and edit (+ developer).
These tests MUST NOT require ATLASCLOUD_API_KEY.
"""


def test_nano_banana2_lite_t2i_metadata():
    from src.atlascloud_comfyui.nodes.image.nano_banana2_lite_t2i import (
        AtlasNanoBanana2LiteTextToImage,
    )

    required = AtlasNanoBanana2LiteTextToImage.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert AtlasNanoBanana2LiteTextToImage.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasNanoBanana2LiteTextToImage.CATEGORY == "AtlasCloud/Image"


def test_nano_banana2_lite_t2i_dev_metadata():
    from src.atlascloud_comfyui.nodes.image.nano_banana2_lite_t2i_dev import (
        AtlasNanoBanana2LiteTextToImageDev,
    )

    required = AtlasNanoBanana2LiteTextToImageDev.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert AtlasNanoBanana2LiteTextToImageDev.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasNanoBanana2LiteTextToImageDev.CATEGORY == "AtlasCloud/Image"


def test_nano_banana2_lite_edit_metadata():
    from src.atlascloud_comfyui.nodes.image.nano_banana2_lite_edit import (
        AtlasNanoBanana2LiteEdit,
    )

    required = AtlasNanoBanana2LiteEdit.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert "prompt" in required
    assert AtlasNanoBanana2LiteEdit.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasNanoBanana2LiteEdit.CATEGORY == "AtlasCloud/Image"


def test_nano_banana2_lite_edit_dev_metadata():
    from src.atlascloud_comfyui.nodes.image.nano_banana2_lite_edit_dev import (
        AtlasNanoBanana2LiteEditDev,
    )

    required = AtlasNanoBanana2LiteEditDev.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert "prompt" in required
    assert AtlasNanoBanana2LiteEditDev.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasNanoBanana2LiteEditDev.CATEGORY == "AtlasCloud/Image"


def test_new_nodes_2026_07_01_registered():
    from src.atlascloud_comfyui.registry import (
        NODE_CLASS_MAPPINGS,
        NODE_DISPLAY_NAME_MAPPINGS,
    )

    for key in (
        "AtlasCloud Nano Banana 2 Lite Text-to-Image",
        "AtlasCloud Nano Banana 2 Lite Text-to-Image Developer",
        "AtlasCloud Nano Banana 2 Lite Edit",
        "AtlasCloud Nano Banana 2 Lite Edit Developer",
    ):
        assert key in NODE_CLASS_MAPPINGS
        assert key in NODE_DISPLAY_NAME_MAPPINGS


def test_new_nodes_2026_07_01_model_ids():
    import inspect

    from src.atlascloud_comfyui.nodes.image.nano_banana2_lite_edit import AtlasNanoBanana2LiteEdit
    from src.atlascloud_comfyui.nodes.image.nano_banana2_lite_edit_dev import AtlasNanoBanana2LiteEditDev
    from src.atlascloud_comfyui.nodes.image.nano_banana2_lite_t2i import AtlasNanoBanana2LiteTextToImage
    from src.atlascloud_comfyui.nodes.image.nano_banana2_lite_t2i_dev import AtlasNanoBanana2LiteTextToImageDev

    expected = {
        AtlasNanoBanana2LiteTextToImage: "google/nano-banana-2-lite/text-to-image",
        AtlasNanoBanana2LiteTextToImageDev: "google/nano-banana-2-lite/text-to-image-developer",
        AtlasNanoBanana2LiteEdit: "google/nano-banana-2-lite/edit",
        AtlasNanoBanana2LiteEditDev: "google/nano-banana-2-lite/edit-developer",
    }
    for cls, model_id in expected.items():
        assert model_id in inspect.getsource(cls.run)
