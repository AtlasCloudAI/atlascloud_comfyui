"""Metadata-only tests for newly added nodes (2026-07-24).

New model: Nano Banana 2 Lite Reference-to-Image.
These tests MUST NOT require ATLASCLOUD_API_KEY.
"""


def test_nano_banana2_lite_r2i_metadata():
    from src.atlascloud_comfyui.nodes.image.nano_banana2_lite_r2i import (
        AtlasNanoBanana2LiteReferenceToImage,
    )

    required = AtlasNanoBanana2LiteReferenceToImage.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert "video_url" in required
    assert AtlasNanoBanana2LiteReferenceToImage.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasNanoBanana2LiteReferenceToImage.CATEGORY == "AtlasCloud/Image"


def test_new_nodes_2026_07_24_registered():
    from src.atlascloud_comfyui.registry import (
        NODE_CLASS_MAPPINGS,
        NODE_DISPLAY_NAME_MAPPINGS,
    )

    key = "AtlasCloud Nano Banana 2 Lite Reference-to-Image"
    assert key in NODE_CLASS_MAPPINGS
    assert key in NODE_DISPLAY_NAME_MAPPINGS


def test_new_nodes_2026_07_24_model_ids():
    import inspect

    from src.atlascloud_comfyui.nodes.image.nano_banana2_lite_r2i import (
        AtlasNanoBanana2LiteReferenceToImage,
    )

    assert (
        '"model": "google/nano-banana-2-lite/reference-to-image"'
        in inspect.getsource(AtlasNanoBanana2LiteReferenceToImage.run)
    )
