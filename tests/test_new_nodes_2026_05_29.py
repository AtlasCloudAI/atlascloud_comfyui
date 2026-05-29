"""Metadata-only tests for newly added nodes (2026-05-29).

These tests MUST NOT require ATLASCLOUD_API_KEY.
"""


def test_grok_imagine_video_t2v_metadata():
    from src.atlascloud_comfyui.nodes.video.xai_grok_imagine_video_t2v import (
        AtlasGrokImagineVideoTextToVideo,
    )

    required = AtlasGrokImagineVideoTextToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert AtlasGrokImagineVideoTextToVideo.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasGrokImagineVideoTextToVideo.CATEGORY == "AtlasCloud/Video"


def test_grok_imagine_video_i2v_metadata():
    from src.atlascloud_comfyui.nodes.video.xai_grok_imagine_video_i2v import (
        AtlasGrokImagineVideoImageToVideo,
    )

    required = AtlasGrokImagineVideoImageToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert "image_url" in required
    assert AtlasGrokImagineVideoImageToVideo.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasGrokImagineVideoImageToVideo.CATEGORY == "AtlasCloud/Video"


def test_grok_imagine_video_r2v_metadata():
    from src.atlascloud_comfyui.nodes.video.xai_grok_imagine_video_r2v import (
        AtlasGrokImagineVideoReferenceToVideo,
    )

    required = AtlasGrokImagineVideoReferenceToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert "image_urls" in required
    assert AtlasGrokImagineVideoReferenceToVideo.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasGrokImagineVideoReferenceToVideo.CATEGORY == "AtlasCloud/Video"


def test_flux2_pro_t2i_metadata():
    from src.atlascloud_comfyui.nodes.image.flux2_pro_t2i import (
        AtlasFlux2ProTextToImage,
    )

    required = AtlasFlux2ProTextToImage.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert AtlasFlux2ProTextToImage.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasFlux2ProTextToImage.CATEGORY == "AtlasCloud/Image"


def test_new_nodes_registered():
    from src.atlascloud_comfyui.registry import (
        NODE_CLASS_MAPPINGS,
        NODE_DISPLAY_NAME_MAPPINGS,
    )

    for key in (
        "AtlasCloud Grok Imagine Video Text-to-Video",
        "AtlasCloud Grok Imagine Video Image-to-Video",
        "AtlasCloud Grok Imagine Video Reference-to-Video",
        "AtlasCloud FLUX.2 Pro Text-to-Image",
    ):
        assert key in NODE_CLASS_MAPPINGS
        assert key in NODE_DISPLAY_NAME_MAPPINGS
