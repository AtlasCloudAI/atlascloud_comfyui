"""Metadata-only tests for newly added nodes (2026-07-09).

Seedream v5.0 Pro (text-to-image, edit), Nvidia Cosmos 3 Super
(text-to-image, image-to-video), and Ideogram v4 (turbo, quality) text-to-image.
These tests MUST NOT require ATLASCLOUD_API_KEY.
"""


def test_seedream_v50_pro_t2i_metadata():
    from src.atlascloud_comfyui.nodes.image.seedream_v50_pro_t2i import (
        AtlasSeedreamV50ProTextToImage,
    )

    required = AtlasSeedreamV50ProTextToImage.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert AtlasSeedreamV50ProTextToImage.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasSeedreamV50ProTextToImage.CATEGORY == "AtlasCloud/Image"


def test_seedream_v50_pro_edit_metadata():
    from src.atlascloud_comfyui.nodes.image.seedream_v50_pro_edit import (
        AtlasSeedreamV50ProEdit,
    )

    required = AtlasSeedreamV50ProEdit.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert "images" in required
    assert AtlasSeedreamV50ProEdit.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasSeedreamV50ProEdit.CATEGORY == "AtlasCloud/Image"


def test_cosmos_3_super_t2i_metadata():
    from src.atlascloud_comfyui.nodes.image.nvidia_cosmos_3_super_t2i import (
        AtlasCosmos3SuperTextToImage,
    )

    required = AtlasCosmos3SuperTextToImage.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert AtlasCosmos3SuperTextToImage.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasCosmos3SuperTextToImage.CATEGORY == "AtlasCloud/Image"


def test_cosmos_3_super_i2v_metadata():
    from src.atlascloud_comfyui.nodes.video.nvidia_cosmos_3_super_i2v import (
        AtlasCosmos3SuperImageToVideo,
    )

    required = AtlasCosmos3SuperImageToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert "image_url" in required
    assert AtlasCosmos3SuperImageToVideo.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasCosmos3SuperImageToVideo.CATEGORY == "AtlasCloud/Video"


def test_ideogram_v4_turbo_t2i_metadata():
    from src.atlascloud_comfyui.nodes.image.ideogram_v4_turbo_t2i import (
        AtlasIdeogramV4TurboTextToImage,
    )

    required = AtlasIdeogramV4TurboTextToImage.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert AtlasIdeogramV4TurboTextToImage.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasIdeogramV4TurboTextToImage.CATEGORY == "AtlasCloud/Image"


def test_ideogram_v4_quality_t2i_metadata():
    from src.atlascloud_comfyui.nodes.image.ideogram_v4_quality_t2i import (
        AtlasIdeogramV4QualityTextToImage,
    )

    required = AtlasIdeogramV4QualityTextToImage.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert AtlasIdeogramV4QualityTextToImage.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasIdeogramV4QualityTextToImage.CATEGORY == "AtlasCloud/Image"


def test_new_nodes_2026_07_09_registered():
    from src.atlascloud_comfyui.registry import (
        NODE_CLASS_MAPPINGS,
        NODE_DISPLAY_NAME_MAPPINGS,
    )

    for key in (
        "AtlasCloud Seedream V5.0 Pro Text-to-Image",
        "AtlasCloud Seedream V5.0 Pro Edit",
        "AtlasCloud Cosmos 3 Super Text-to-Image",
        "AtlasCloud Cosmos 3 Super Image-to-Video",
        "AtlasCloud Ideogram V4 Turbo Text-to-Image",
        "AtlasCloud Ideogram V4 Quality Text-to-Image",
    ):
        assert key in NODE_CLASS_MAPPINGS
        assert key in NODE_DISPLAY_NAME_MAPPINGS


def test_new_nodes_2026_07_09_model_ids():
    import inspect

    from src.atlascloud_comfyui.nodes.image.seedream_v50_pro_t2i import AtlasSeedreamV50ProTextToImage
    from src.atlascloud_comfyui.nodes.image.seedream_v50_pro_edit import AtlasSeedreamV50ProEdit
    from src.atlascloud_comfyui.nodes.image.nvidia_cosmos_3_super_t2i import AtlasCosmos3SuperTextToImage
    from src.atlascloud_comfyui.nodes.video.nvidia_cosmos_3_super_i2v import AtlasCosmos3SuperImageToVideo
    from src.atlascloud_comfyui.nodes.image.ideogram_v4_turbo_t2i import AtlasIdeogramV4TurboTextToImage
    from src.atlascloud_comfyui.nodes.image.ideogram_v4_quality_t2i import AtlasIdeogramV4QualityTextToImage

    expected = {
        AtlasSeedreamV50ProTextToImage: "bytedance/seedream-v5.0-pro/text-to-image",
        AtlasSeedreamV50ProEdit: "bytedance/seedream-v5.0-pro/edit",
        AtlasCosmos3SuperTextToImage: "nvidia/cosmos-3-super/text-to-image",
        AtlasCosmos3SuperImageToVideo: "nvidia/cosmos-3-super/image-to-video",
        AtlasIdeogramV4TurboTextToImage: "ideogram/v4/turbo/text-to-image",
        AtlasIdeogramV4QualityTextToImage: "ideogram/v4/Quality/text-to-image",
    }
    for cls, model_id in expected.items():
        src = inspect.getsource(cls.run)
        assert f'"model": "{model_id}"' in src
