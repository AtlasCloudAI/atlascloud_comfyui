"""Metadata-only tests for newly added nodes (2026-06-10).

Midjourney V8.1 (text-to-image, image-to-video) and PixVerse extend / start-end families.
These tests MUST NOT require ATLASCLOUD_API_KEY.
"""


def test_midjourney_v81_t2i_metadata():
    from src.atlascloud_comfyui.nodes.image.midjourney_v81_t2i import (
        AtlasMidjourneyV81TextToImage,
    )

    required = AtlasMidjourneyV81TextToImage.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert AtlasMidjourneyV81TextToImage.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasMidjourneyV81TextToImage.CATEGORY == "AtlasCloud/Image"


def test_midjourney_v81_i2v_metadata():
    from src.atlascloud_comfyui.nodes.video.midjourney_v81_i2v import (
        AtlasMidjourneyV81ImageToVideo,
    )

    required = AtlasMidjourneyV81ImageToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert AtlasMidjourneyV81ImageToVideo.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasMidjourneyV81ImageToVideo.CATEGORY == "AtlasCloud/Video"


def test_pixverse_v6_video_extend_metadata():
    from src.atlascloud_comfyui.nodes.video.pixverse_v6_video_extend import (
        AtlasPixVerseV6VideoExtend,
    )

    required = AtlasPixVerseV6VideoExtend.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "video" in required
    assert "prompt" in required
    assert AtlasPixVerseV6VideoExtend.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasPixVerseV6VideoExtend.CATEGORY == "AtlasCloud/Video"


def test_pixverse_c1_start_end_metadata():
    from src.atlascloud_comfyui.nodes.video.pixverse_c1_start_end import (
        AtlasPixVerseC1StartEndToVideo,
    )

    required = AtlasPixVerseC1StartEndToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert "end_image" in required
    assert "prompt" in required
    assert AtlasPixVerseC1StartEndToVideo.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasPixVerseC1StartEndToVideo.CATEGORY == "AtlasCloud/Video"


def test_pixverse_v6_start_end_metadata():
    from src.atlascloud_comfyui.nodes.video.pixverse_v6_start_end import (
        AtlasPixVerseV6StartEndToVideo,
    )

    required = AtlasPixVerseV6StartEndToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert "end_image" in required
    assert "prompt" in required
    assert AtlasPixVerseV6StartEndToVideo.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasPixVerseV6StartEndToVideo.CATEGORY == "AtlasCloud/Video"


def test_new_nodes_2026_06_10_registered():
    from src.atlascloud_comfyui.registry import (
        NODE_CLASS_MAPPINGS,
        NODE_DISPLAY_NAME_MAPPINGS,
    )

    for key in (
        "AtlasCloud Midjourney V8.1 Text-to-Image",
        "AtlasCloud Midjourney V8.1 Image-to-Video",
        "AtlasCloud PixVerse V6 Video-Extend",
        "AtlasCloud PixVerse C1 Start-End-to-Video",
        "AtlasCloud PixVerse V6 Start-End-to-Video",
    ):
        assert key in NODE_CLASS_MAPPINGS
        assert key in NODE_DISPLAY_NAME_MAPPINGS


def test_new_nodes_2026_06_10_model_ids():
    import inspect

    from src.atlascloud_comfyui.nodes.image.midjourney_v81_t2i import AtlasMidjourneyV81TextToImage
    from src.atlascloud_comfyui.nodes.video.midjourney_v81_i2v import AtlasMidjourneyV81ImageToVideo
    from src.atlascloud_comfyui.nodes.video.pixverse_v6_video_extend import AtlasPixVerseV6VideoExtend
    from src.atlascloud_comfyui.nodes.video.pixverse_c1_start_end import AtlasPixVerseC1StartEndToVideo
    from src.atlascloud_comfyui.nodes.video.pixverse_v6_start_end import AtlasPixVerseV6StartEndToVideo

    expected = {
        AtlasMidjourneyV81TextToImage: "midjourney/v8.1/text-to-image",
        AtlasMidjourneyV81ImageToVideo: "midjourney/v8.1/image-to-video",
        AtlasPixVerseV6VideoExtend: "pixverse/v6/video-extend",
        AtlasPixVerseC1StartEndToVideo: "pixverse/c1/start-end-to-video",
        AtlasPixVerseV6StartEndToVideo: "pixverse/v6/start-end-to-video",
    }
    for cls, model_id in expected.items():
        assert model_id in inspect.getsource(cls.run)
