"""Metadata-only tests for newly added WAN2.6 + Kling O3 nodes.

Keep these tests lightweight: they should not require ATLASCLOUD_API_KEY.
"""

from __future__ import annotations


def test_wan26_t2i_node_metadata():
    from src.atlascloud_comfyui.nodes.image.wan26_t2i import AtlasWAN26TextToImage

    required = AtlasWAN26TextToImage.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert AtlasWAN26TextToImage.RETURN_TYPES == ("STRING", "STRING")


def test_wan26_i2v_flash_node_metadata():
    from src.atlascloud_comfyui.nodes.video.wan26_i2v_flash import AtlasWAN26ImageToVideoFlash

    required = AtlasWAN26ImageToVideoFlash.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert "prompt" in required
    assert AtlasWAN26ImageToVideoFlash.RETURN_TYPES == ("STRING", "STRING")


def test_wan26_v2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.wan26_v2v import AtlasWAN26VideoToVideo

    required = AtlasWAN26VideoToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "videos" in required
    assert "prompt" in required
    assert AtlasWAN26VideoToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_kling_video_o3_pro_nodes_metadata():
    from src.atlascloud_comfyui.nodes.video.kling_video_o3_pro_t2v import AtlasKlingVideoO3ProTextToVideo
    from src.atlascloud_comfyui.nodes.video.kling_video_o3_pro_i2v import AtlasKlingVideoO3ProImageToVideo
    from src.atlascloud_comfyui.nodes.video.kling_video_o3_pro_r2v import AtlasKlingVideoO3ProReferenceToVideo
    from src.atlascloud_comfyui.nodes.video.kling_video_o3_pro_video_edit import AtlasKlingVideoO3ProVideoEdit

    assert "atlas_client" in AtlasKlingVideoO3ProTextToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in AtlasKlingVideoO3ProImageToVideo.INPUT_TYPES()["required"]
    assert "image" in AtlasKlingVideoO3ProImageToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in AtlasKlingVideoO3ProReferenceToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in AtlasKlingVideoO3ProVideoEdit.INPUT_TYPES()["required"]
    assert "video" in AtlasKlingVideoO3ProVideoEdit.INPUT_TYPES()["required"]


def test_kling_video_o3_std_nodes_metadata():
    from src.atlascloud_comfyui.nodes.video.kling_video_o3_std_t2v import AtlasKlingVideoO3StdTextToVideo
    from src.atlascloud_comfyui.nodes.video.kling_video_o3_std_i2v import AtlasKlingVideoO3StdImageToVideo
    from src.atlascloud_comfyui.nodes.video.kling_video_o3_std_r2v import AtlasKlingVideoO3StdReferenceToVideo
    from src.atlascloud_comfyui.nodes.video.kling_video_o3_std_video_edit import AtlasKlingVideoO3StdVideoEdit

    assert "atlas_client" in AtlasKlingVideoO3StdTextToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in AtlasKlingVideoO3StdImageToVideo.INPUT_TYPES()["required"]
    assert "image" in AtlasKlingVideoO3StdImageToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in AtlasKlingVideoO3StdReferenceToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in AtlasKlingVideoO3StdVideoEdit.INPUT_TYPES()["required"]
    assert "video" in AtlasKlingVideoO3StdVideoEdit.INPUT_TYPES()["required"]
