"""
Metadata-only tests for newly added nodes (2026-03-04).

These tests MUST NOT require ATLASCLOUD_API_KEY.
"""


def test_kling_v26_pro_avatar_node_metadata():
    from src.atlascloud_comfyui.nodes.video.kling_v26_pro_avatar import AtlasKlingV26ProAvatar

    assert "atlas_client" in AtlasKlingV26ProAvatar.INPUT_TYPES()["required"]
    assert "audio" in AtlasKlingV26ProAvatar.INPUT_TYPES()["required"]
    assert "image" in AtlasKlingV26ProAvatar.INPUT_TYPES()["required"]
    assert AtlasKlingV26ProAvatar.RETURN_TYPES == ("STRING", "STRING")


def test_kling_v26_std_avatar_node_metadata():
    from src.atlascloud_comfyui.nodes.video.kling_v26_std_avatar import AtlasKlingV26StdAvatar

    assert "atlas_client" in AtlasKlingV26StdAvatar.INPUT_TYPES()["required"]
    assert "audio" in AtlasKlingV26StdAvatar.INPUT_TYPES()["required"]
    assert "image" in AtlasKlingV26StdAvatar.INPUT_TYPES()["required"]
    assert AtlasKlingV26StdAvatar.RETURN_TYPES == ("STRING", "STRING")


def test_kling_v26_pro_motion_control_node_metadata():
    from src.atlascloud_comfyui.nodes.video.kling_v26_pro_motion_control import AtlasKlingV26ProMotionControl

    required = AtlasKlingV26ProMotionControl.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert "video" in required
    assert "character_orientation" in required
    assert AtlasKlingV26ProMotionControl.RETURN_TYPES == ("STRING", "STRING")


def test_kling_v26_std_motion_control_node_metadata():
    from src.atlascloud_comfyui.nodes.video.kling_v26_std_motion_control import AtlasKlingV26StdMotionControl

    required = AtlasKlingV26StdMotionControl.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert "video" in required
    assert "character_orientation" in required
    assert AtlasKlingV26StdMotionControl.RETURN_TYPES == ("STRING", "STRING")


def test_seedance_v15_pro_i2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.seedance_v15_pro_i2v import AtlasSeedanceV15ProImageToVideo

    required = AtlasSeedanceV15ProImageToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert AtlasSeedanceV15ProImageToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_seedance_v15_pro_i2v_fast_node_metadata():
    from src.atlascloud_comfyui.nodes.video.seedance_v15_pro_i2v_fast import AtlasSeedanceV15ProImageToVideoFast

    required = AtlasSeedanceV15ProImageToVideoFast.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert AtlasSeedanceV15ProImageToVideoFast.RETURN_TYPES == ("STRING", "STRING")


def test_seedance_v15_pro_t2v_fast_node_metadata():
    from src.atlascloud_comfyui.nodes.video.seedance_v15_pro_t2v_fast import AtlasSeedanceV15ProTextToVideoFast

    required = AtlasSeedanceV15ProTextToVideoFast.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert AtlasSeedanceV15ProTextToVideoFast.RETURN_TYPES == ("STRING", "STRING")


def test_kling_video_o1_i2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.kling_video_o1_i2v import AtlasKlingVideoO1ImageToVideo

    required = AtlasKlingVideoO1ImageToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert "prompt" in required
    assert AtlasKlingVideoO1ImageToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_kling_v26_pro_i2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.kling_v26_pro_i2v import AtlasKlingV26ProImageToVideo

    required = AtlasKlingV26ProImageToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert "prompt" in required
    assert AtlasKlingV26ProImageToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_zimage_turbo_t2i_node_metadata():
    from src.atlascloud_comfyui.nodes.image.zimage_turbo_t2i import AtlasZImageTurboTextToImage

    required = AtlasZImageTurboTextToImage.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert "width" in required
    assert "height" in required
    assert AtlasZImageTurboTextToImage.RETURN_TYPES == ("STRING", "STRING")


def test_seedream_v45_edit_node_metadata():
    from src.atlascloud_comfyui.nodes.image.seedream_v45_edit import AtlasSeedreamV45Edit

    required = AtlasSeedreamV45Edit.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "images" in required
    assert "prompt" in required
    assert AtlasSeedreamV45Edit.RETURN_TYPES == ("STRING", "STRING")


def test_seedream_v45_sequential_t2i_node_metadata():
    from src.atlascloud_comfyui.nodes.image.seedream_v45_sequential_t2i import AtlasSeedreamV45SequentialTextToImage

    required = AtlasSeedreamV45SequentialTextToImage.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert AtlasSeedreamV45SequentialTextToImage.RETURN_TYPES == ("STRING", "STRING")


def test_seedream_v45_edit_sequential_node_metadata():
    from src.atlascloud_comfyui.nodes.image.seedream_v45_edit_sequential import AtlasSeedreamV45EditSequential

    required = AtlasSeedreamV45EditSequential.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "images" in required
    assert "prompt" in required
    assert AtlasSeedreamV45EditSequential.RETURN_TYPES == ("STRING", "STRING")


def test_qwen_image_edit_node_metadata():
    from src.atlascloud_comfyui.nodes.image.qwen_image_edit import AtlasQwenImageEdit

    required = AtlasQwenImageEdit.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert "prompt" in required
    assert AtlasQwenImageEdit.RETURN_TYPES == ("STRING", "STRING")


def test_nano_banana_pro_t2i_node_metadata():
    from src.atlascloud_comfyui.nodes.image.nano_banana_pro_t2i import AtlasNanoBananaProTextToImage

    required = AtlasNanoBananaProTextToImage.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert AtlasNanoBananaProTextToImage.RETURN_TYPES == ("STRING", "STRING")


def test_nano_banana_pro_edit_node_metadata():
    from src.atlascloud_comfyui.nodes.image.nano_banana_pro_edit import AtlasNanoBananaProEdit

    required = AtlasNanoBananaProEdit.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "images" in required
    assert "prompt" in required
    assert AtlasNanoBananaProEdit.RETURN_TYPES == ("STRING", "STRING")
