"""Metadata-only tests for newly added nodes (2026-05-30).

These tests MUST NOT require ATLASCLOUD_API_KEY.
"""


def test_flux2_flex_edit_metadata():
    from src.atlascloud_comfyui.nodes.image.flux2_flex_edit import AtlasFlux2FlexEdit

    required = AtlasFlux2FlexEdit.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert "images" in required
    assert AtlasFlux2FlexEdit.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasFlux2FlexEdit.CATEGORY == "AtlasCloud/Image"


def test_flux2_pro_edit_metadata():
    from src.atlascloud_comfyui.nodes.image.flux2_pro_edit import AtlasFlux2ProEdit

    required = AtlasFlux2ProEdit.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert "images" in required
    assert AtlasFlux2ProEdit.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasFlux2ProEdit.CATEGORY == "AtlasCloud/Image"


def test_grok_imagine_video_edit_metadata():
    from src.atlascloud_comfyui.nodes.video.xai_grok_imagine_video_edit_video import (
        AtlasGrokImagineVideoEdit,
    )

    required = AtlasGrokImagineVideoEdit.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert "video_url" in required
    assert AtlasGrokImagineVideoEdit.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasGrokImagineVideoEdit.CATEGORY == "AtlasCloud/Video"


def test_grok_imagine_video_extend_metadata():
    from src.atlascloud_comfyui.nodes.video.xai_grok_imagine_video_extend_video import (
        AtlasGrokImagineVideoExtend,
    )

    required = AtlasGrokImagineVideoExtend.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert "video_url" in required
    assert AtlasGrokImagineVideoExtend.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasGrokImagineVideoExtend.CATEGORY == "AtlasCloud/Video"


def test_new_nodes_registered():
    from src.atlascloud_comfyui.registry import (
        NODE_CLASS_MAPPINGS,
        NODE_DISPLAY_NAME_MAPPINGS,
    )

    for key in (
        "AtlasCloud FLUX.2 Flex Edit",
        "AtlasCloud FLUX.2 Pro Edit",
        "AtlasCloud Grok Imagine Video Edit",
        "AtlasCloud Grok Imagine Video Extend",
    ):
        assert key in NODE_CLASS_MAPPINGS
        assert key in NODE_DISPLAY_NAME_MAPPINGS
