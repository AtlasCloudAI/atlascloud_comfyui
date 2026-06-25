"""Metadata-only tests for newly added nodes (2026-06-25).

Seedance 2.0 Mini family (text/image/reference-to-video), Avatar Omni Human 1.5,
and the AtlasCloud Image Upscaler.
These tests MUST NOT require ATLASCLOUD_API_KEY.
"""


def test_seedance_20_mini_t2v_metadata():
    from src.atlascloud_comfyui.nodes.video.bytedance_seedance_2_0_mini_t2v import (
        AtlasSeedance20MiniTextToVideo,
    )

    required = AtlasSeedance20MiniTextToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert AtlasSeedance20MiniTextToVideo.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasSeedance20MiniTextToVideo.CATEGORY == "AtlasCloud/Video"


def test_seedance_20_mini_i2v_metadata():
    from src.atlascloud_comfyui.nodes.video.bytedance_seedance_2_0_mini_i2v import (
        AtlasSeedance20MiniImageToVideo,
    )

    required = AtlasSeedance20MiniImageToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert AtlasSeedance20MiniImageToVideo.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasSeedance20MiniImageToVideo.CATEGORY == "AtlasCloud/Video"


def test_seedance_20_mini_r2v_metadata():
    from src.atlascloud_comfyui.nodes.video.bytedance_seedance_2_0_mini_r2v import (
        AtlasSeedance20MiniReferenceToVideo,
    )

    required = AtlasSeedance20MiniReferenceToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "reference_images" in required
    assert "reference_videos" in required
    assert AtlasSeedance20MiniReferenceToVideo.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasSeedance20MiniReferenceToVideo.CATEGORY == "AtlasCloud/Video"


def test_avatar_omni_human_v15_metadata():
    from src.atlascloud_comfyui.nodes.video.bytedance_avatar_omni_human_v15 import (
        AtlasAvatarOmniHumanV15,
    )

    required = AtlasAvatarOmniHumanV15.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image_url" in required
    assert "audio_url" in required
    assert AtlasAvatarOmniHumanV15.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasAvatarOmniHumanV15.CATEGORY == "AtlasCloud/Video"


def test_image_upscaler_metadata():
    from src.atlascloud_comfyui.nodes.image.atlascloud_image_upscaler import (
        AtlasImageUpscaler,
    )

    required = AtlasImageUpscaler.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert AtlasImageUpscaler.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasImageUpscaler.CATEGORY == "AtlasCloud/Image"


def test_new_nodes_2026_06_25_registered():
    from src.atlascloud_comfyui.registry import (
        NODE_CLASS_MAPPINGS,
        NODE_DISPLAY_NAME_MAPPINGS,
    )

    for key in (
        "AtlasCloud Seedance 2.0 Mini Text-to-Video",
        "AtlasCloud Seedance 2.0 Mini Image-to-Video",
        "AtlasCloud Seedance 2.0 Mini Reference-to-Video",
        "AtlasCloud Avatar Omni Human 1.5",
        "AtlasCloud Image Upscaler",
    ):
        assert key in NODE_CLASS_MAPPINGS
        assert key in NODE_DISPLAY_NAME_MAPPINGS


def test_new_nodes_2026_06_25_model_ids():
    import inspect

    from src.atlascloud_comfyui.nodes.image.atlascloud_image_upscaler import AtlasImageUpscaler
    from src.atlascloud_comfyui.nodes.video.bytedance_avatar_omni_human_v15 import AtlasAvatarOmniHumanV15
    from src.atlascloud_comfyui.nodes.video.bytedance_seedance_2_0_mini_i2v import AtlasSeedance20MiniImageToVideo
    from src.atlascloud_comfyui.nodes.video.bytedance_seedance_2_0_mini_r2v import AtlasSeedance20MiniReferenceToVideo
    from src.atlascloud_comfyui.nodes.video.bytedance_seedance_2_0_mini_t2v import AtlasSeedance20MiniTextToVideo

    expected = {
        AtlasSeedance20MiniTextToVideo: "bytedance/seedance-2.0-mini/text-to-video",
        AtlasSeedance20MiniImageToVideo: "bytedance/seedance-2.0-mini/image-to-video",
        AtlasSeedance20MiniReferenceToVideo: "bytedance/seedance-2.0-mini/reference-to-video",
        AtlasAvatarOmniHumanV15: "bytedance/avatar-omni-human-v1.5",
        AtlasImageUpscaler: "atlascloud/image-upscaler",
    }
    for cls, model_id in expected.items():
        assert model_id in inspect.getsource(cls.run)
