"""Metadata-only tests for newly added nodes (2026-06-16).

Kling V3.0 4K + Kling Video O3 4K (text/image-to-video) and Midjourney V8.1
image-to-image / blend / remove-background / style-transfer.
These tests MUST NOT require ATLASCLOUD_API_KEY.
"""


def test_kling_v30_4k_i2v_metadata():
    from src.atlascloud_comfyui.nodes.video.kling_v30_4k_i2v import (
        AtlasKlingV304KImageToVideo,
    )

    required = AtlasKlingV304KImageToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert AtlasKlingV304KImageToVideo.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasKlingV304KImageToVideo.CATEGORY == "AtlasCloud/Video"


def test_kling_v30_4k_t2v_metadata():
    from src.atlascloud_comfyui.nodes.video.kling_v30_4k_t2v import (
        AtlasKlingV304KTextToVideo,
    )

    required = AtlasKlingV304KTextToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert AtlasKlingV304KTextToVideo.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasKlingV304KTextToVideo.CATEGORY == "AtlasCloud/Video"


def test_kling_video_o3_4k_i2v_metadata():
    from src.atlascloud_comfyui.nodes.video.kling_video_o3_4k_i2v import (
        AtlasKlingVideoO34KImageToVideo,
    )

    required = AtlasKlingVideoO34KImageToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert AtlasKlingVideoO34KImageToVideo.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasKlingVideoO34KImageToVideo.CATEGORY == "AtlasCloud/Video"


def test_kling_video_o3_4k_t2v_metadata():
    from src.atlascloud_comfyui.nodes.video.kling_video_o3_4k_t2v import (
        AtlasKlingVideoO34KTextToVideo,
    )

    required = AtlasKlingVideoO34KTextToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert AtlasKlingVideoO34KTextToVideo.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasKlingVideoO34KTextToVideo.CATEGORY == "AtlasCloud/Video"


def test_midjourney_v81_i2i_metadata():
    from src.atlascloud_comfyui.nodes.image.midjourney_v81_i2i import (
        AtlasMidjourneyV81ImageToImage,
    )

    required = AtlasMidjourneyV81ImageToImage.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert "prompt" in required
    assert AtlasMidjourneyV81ImageToImage.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasMidjourneyV81ImageToImage.CATEGORY == "AtlasCloud/Image"


def test_midjourney_v81_blend_metadata():
    from src.atlascloud_comfyui.nodes.image.midjourney_v81_blend import (
        AtlasMidjourneyV81Blend,
    )

    required = AtlasMidjourneyV81Blend.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "images" in required
    assert AtlasMidjourneyV81Blend.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasMidjourneyV81Blend.CATEGORY == "AtlasCloud/Image"


def test_midjourney_v81_remove_bg_metadata():
    from src.atlascloud_comfyui.nodes.image.midjourney_v81_remove_bg import (
        AtlasMidjourneyV81RemoveBackground,
    )

    required = AtlasMidjourneyV81RemoveBackground.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert AtlasMidjourneyV81RemoveBackground.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasMidjourneyV81RemoveBackground.CATEGORY == "AtlasCloud/Image"


def test_midjourney_v81_style_transfer_metadata():
    from src.atlascloud_comfyui.nodes.image.midjourney_v81_style_transfer import (
        AtlasMidjourneyV81StyleTransfer,
    )

    required = AtlasMidjourneyV81StyleTransfer.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert "prompt" in required
    assert AtlasMidjourneyV81StyleTransfer.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasMidjourneyV81StyleTransfer.CATEGORY == "AtlasCloud/Image"


def test_new_nodes_2026_06_16_registered():
    from src.atlascloud_comfyui.registry import (
        NODE_CLASS_MAPPINGS,
        NODE_DISPLAY_NAME_MAPPINGS,
    )

    for key in (
        "AtlasCloud Kling V3.0 4K Image-to-Video",
        "AtlasCloud Kling V3.0 4K Text-to-Video",
        "AtlasCloud Kling Video O3 4K Image-to-Video",
        "AtlasCloud Kling Video O3 4K Text-to-Video",
        "AtlasCloud Midjourney V8.1 Image-to-Image",
        "AtlasCloud Midjourney V8.1 Blend",
        "AtlasCloud Midjourney V8.1 Remove Background",
        "AtlasCloud Midjourney V8.1 Style Transfer",
    ):
        assert key in NODE_CLASS_MAPPINGS
        assert key in NODE_DISPLAY_NAME_MAPPINGS


def test_new_nodes_2026_06_16_model_ids():
    import inspect

    from src.atlascloud_comfyui.nodes.video.kling_v30_4k_i2v import AtlasKlingV304KImageToVideo
    from src.atlascloud_comfyui.nodes.video.kling_v30_4k_t2v import AtlasKlingV304KTextToVideo
    from src.atlascloud_comfyui.nodes.video.kling_video_o3_4k_i2v import AtlasKlingVideoO34KImageToVideo
    from src.atlascloud_comfyui.nodes.video.kling_video_o3_4k_t2v import AtlasKlingVideoO34KTextToVideo
    from src.atlascloud_comfyui.nodes.image.midjourney_v81_i2i import AtlasMidjourneyV81ImageToImage
    from src.atlascloud_comfyui.nodes.image.midjourney_v81_blend import AtlasMidjourneyV81Blend
    from src.atlascloud_comfyui.nodes.image.midjourney_v81_remove_bg import AtlasMidjourneyV81RemoveBackground
    from src.atlascloud_comfyui.nodes.image.midjourney_v81_style_transfer import AtlasMidjourneyV81StyleTransfer

    expected = {
        AtlasKlingV304KImageToVideo: "kwaivgi/kling-v3.0-4k/image-to-video",
        AtlasKlingV304KTextToVideo: "kwaivgi/kling-v3.0-4k/text-to-video",
        AtlasKlingVideoO34KImageToVideo: "kwaivgi/kling-video-o3-4k/image-to-video",
        AtlasKlingVideoO34KTextToVideo: "kwaivgi/kling-video-o3-4k/text-to-video",
        AtlasMidjourneyV81ImageToImage: "midjourney/v8.1/image-to-image",
        AtlasMidjourneyV81Blend: "midjourney/v8.1/blend",
        AtlasMidjourneyV81RemoveBackground: "midjourney/v8.1/remove-background",
        AtlasMidjourneyV81StyleTransfer: "midjourney/v8.1/style-transfer",
    }
    for cls, model_id in expected.items():
        assert model_id in inspect.getsource(cls.run)
