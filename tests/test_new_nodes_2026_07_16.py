"""Metadata-only tests for newly added nodes (2026-07-16).

AtlasCloud tools: Face Swap (Image), Photo Cleanup, Face Swap (Video).
These tests MUST NOT require ATLASCLOUD_API_KEY.
"""


def test_face_swap_image_metadata():
    from src.atlascloud_comfyui.nodes.image.atlascloud_face_swap_image import (
        AtlasFaceSwapImage,
    )

    required = AtlasFaceSwapImage.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "source_face" in required
    assert "target_image" in required
    assert AtlasFaceSwapImage.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasFaceSwapImage.CATEGORY == "AtlasCloud/Image"


def test_photo_cleanup_metadata():
    from src.atlascloud_comfyui.nodes.image.atlascloud_photo_cleanup import (
        AtlasPhotoCleanup,
    )

    required = AtlasPhotoCleanup.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert AtlasPhotoCleanup.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasPhotoCleanup.CATEGORY == "AtlasCloud/Image"


def test_face_swap_video_metadata():
    from src.atlascloud_comfyui.nodes.video.atlascloud_face_swap_video import (
        AtlasFaceSwapVideo,
    )

    required = AtlasFaceSwapVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "source_face" in required
    assert "video" in required
    assert AtlasFaceSwapVideo.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasFaceSwapVideo.CATEGORY == "AtlasCloud/Video"


def test_new_nodes_2026_07_16_registered():
    from src.atlascloud_comfyui.registry import (
        NODE_CLASS_MAPPINGS,
        NODE_DISPLAY_NAME_MAPPINGS,
    )

    for key in (
        "AtlasCloud Face Swap (Image)",
        "AtlasCloud Photo Cleanup",
        "AtlasCloud Face Swap (Video)",
    ):
        assert key in NODE_CLASS_MAPPINGS
        assert key in NODE_DISPLAY_NAME_MAPPINGS


def test_new_nodes_2026_07_16_model_ids():
    import inspect

    from src.atlascloud_comfyui.nodes.image.atlascloud_face_swap_image import AtlasFaceSwapImage
    from src.atlascloud_comfyui.nodes.image.atlascloud_photo_cleanup import AtlasPhotoCleanup
    from src.atlascloud_comfyui.nodes.video.atlascloud_face_swap_video import AtlasFaceSwapVideo

    expected = {
        AtlasFaceSwapImage: "atlascloud/face-swap-image",
        AtlasPhotoCleanup: "atlascloud/photo-cleanup",
        AtlasFaceSwapVideo: "atlascloud/face-swap-video",
    }
    for cls, model_id in expected.items():
        src = inspect.getsource(cls.run)
        assert f'"model": "{model_id}"' in src
