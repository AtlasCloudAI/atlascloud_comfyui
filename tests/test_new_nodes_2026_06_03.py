"""Metadata-only tests for newly added nodes (2026-06-03).

These tests MUST NOT require ATLASCLOUD_API_KEY.
"""


def test_gemini_omni_flash_r2v_dev_metadata():
    from src.atlascloud_comfyui.nodes.video.google_gemini_omni_flash_r2v_dev import (
        AtlasGeminiOmniFlashReferenceToVideoDev,
    )

    required = AtlasGeminiOmniFlashReferenceToVideoDev.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert "images" in required
    assert "video_url" in required
    assert AtlasGeminiOmniFlashReferenceToVideoDev.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasGeminiOmniFlashReferenceToVideoDev.CATEGORY == "AtlasCloud/Video"


def test_nano_banana2_r2i_metadata():
    from src.atlascloud_comfyui.nodes.image.nano_banana2_r2i import (
        AtlasNanoBanana2ReferenceToImage,
    )

    required = AtlasNanoBanana2ReferenceToImage.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert "video_url" in required
    assert AtlasNanoBanana2ReferenceToImage.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasNanoBanana2ReferenceToImage.CATEGORY == "AtlasCloud/Image"


def test_nano_banana2_r2i_dev_metadata():
    from src.atlascloud_comfyui.nodes.image.nano_banana2_r2i_dev import (
        AtlasNanoBanana2ReferenceToImageDev,
    )

    required = AtlasNanoBanana2ReferenceToImageDev.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert "video_url" in required
    assert AtlasNanoBanana2ReferenceToImageDev.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasNanoBanana2ReferenceToImageDev.CATEGORY == "AtlasCloud/Image"


def test_new_nodes_registered():
    from src.atlascloud_comfyui.registry import (
        NODE_CLASS_MAPPINGS,
        NODE_DISPLAY_NAME_MAPPINGS,
    )

    for key in (
        "AtlasCloud Gemini Omni Flash Reference-to-Video Developer",
        "AtlasCloud Nano Banana 2 Reference-to-Image",
        "AtlasCloud Nano Banana 2 Reference-to-Image Developer",
    ):
        assert key in NODE_CLASS_MAPPINGS
        assert key in NODE_DISPLAY_NAME_MAPPINGS
