"""Metadata-only tests for newly added nodes (2026-05-26).

These tests MUST NOT require ATLASCLOUD_API_KEY.
"""


def test_gemini_omni_flash_t2v_dev_node_metadata():
    from src.atlascloud_comfyui.nodes.video.google_gemini_omni_flash_t2v_dev import (
        AtlasGeminiOmniFlashTextToVideoDev,
    )

    required = AtlasGeminiOmniFlashTextToVideoDev.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert AtlasGeminiOmniFlashTextToVideoDev.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasGeminiOmniFlashTextToVideoDev.CATEGORY == "AtlasCloud/Video"


def test_gemini_omni_flash_i2v_dev_node_metadata():
    from src.atlascloud_comfyui.nodes.video.google_gemini_omni_flash_i2v_dev import (
        AtlasGeminiOmniFlashImageToVideoDev,
    )

    required = AtlasGeminiOmniFlashImageToVideoDev.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert "images" in required
    assert AtlasGeminiOmniFlashImageToVideoDev.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasGeminiOmniFlashImageToVideoDev.CATEGORY == "AtlasCloud/Video"


def test_gemini_omni_flash_nodes_registered():
    from src.atlascloud_comfyui.registry import (
        NODE_CLASS_MAPPINGS,
        NODE_DISPLAY_NAME_MAPPINGS,
    )

    for key in (
        "AtlasCloud Gemini Omni Flash Text-to-Video Developer",
        "AtlasCloud Gemini Omni Flash Image-to-Video Developer",
    ):
        assert key in NODE_CLASS_MAPPINGS
        assert key in NODE_DISPLAY_NAME_MAPPINGS
