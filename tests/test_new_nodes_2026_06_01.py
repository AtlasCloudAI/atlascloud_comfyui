"""Metadata-only tests for newly added nodes (2026-06-01).

These tests MUST NOT require ATLASCLOUD_API_KEY.
"""


def test_grok_imagine_video_v15_i2v_metadata():
    from src.atlascloud_comfyui.nodes.video.xai_grok_imagine_video_v15_i2v import (
        AtlasGrokImagineVideoV15ImageToVideo,
    )

    required = AtlasGrokImagineVideoV15ImageToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert "image_url" in required
    assert AtlasGrokImagineVideoV15ImageToVideo.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasGrokImagineVideoV15ImageToVideo.CATEGORY == "AtlasCloud/Video"


def test_new_nodes_registered():
    from src.atlascloud_comfyui.registry import (
        NODE_CLASS_MAPPINGS,
        NODE_DISPLAY_NAME_MAPPINGS,
    )

    for key in ("AtlasCloud Grok Imagine Video v1.5 Image-to-Video",):
        assert key in NODE_CLASS_MAPPINGS
        assert key in NODE_DISPLAY_NAME_MAPPINGS
