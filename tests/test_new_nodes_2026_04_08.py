"""Metadata-only tests for newly added nodes (2026-04-08).

These tests MUST NOT require ATLASCLOUD_API_KEY.
"""


def test_wan27_t2i_node_metadata():
    from src.atlascloud_comfyui.nodes.image.alibaba_wan_2_7_t2i import AtlasWan27TextToImage

    required = AtlasWan27TextToImage.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert AtlasWan27TextToImage.RETURN_TYPES == ("STRING", "STRING")


def test_wan27_image_edit_node_metadata():
    from src.atlascloud_comfyui.nodes.image.alibaba_wan_2_7_edit import AtlasWan27ImageEdit

    required = AtlasWan27ImageEdit.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert "images" in required
    assert AtlasWan27ImageEdit.RETURN_TYPES == ("STRING", "STRING")


def test_wan27_pro_t2i_node_metadata():
    from src.atlascloud_comfyui.nodes.image.alibaba_wan_2_7_pro_t2i import AtlasWan27ProTextToImage

    required = AtlasWan27ProTextToImage.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert AtlasWan27ProTextToImage.RETURN_TYPES == ("STRING", "STRING")


def test_wan27_pro_image_edit_node_metadata():
    from src.atlascloud_comfyui.nodes.image.alibaba_wan_2_7_pro_edit import AtlasWan27ProImageEdit

    required = AtlasWan27ProImageEdit.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert "images" in required
    assert AtlasWan27ProImageEdit.RETURN_TYPES == ("STRING", "STRING")


def test_wan22_spicy_video_extend_node_metadata():
    from src.atlascloud_comfyui.nodes.video.alibaba_wan_2_2_spicy_video_extend import AtlasWan22SpicyVideoExtend

    required = AtlasWan22SpicyVideoExtend.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "video_url" in required
    assert "prompt" in required
    assert AtlasWan22SpicyVideoExtend.RETURN_TYPES == ("STRING", "STRING")


def test_atlascloud_wan22_i2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.atlascloud_wan_2_2_i2v import AtlasAtlascloudWan22ImageToVideo

    required = AtlasAtlascloudWan22ImageToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert "prompt" in required
    assert AtlasAtlascloudWan22ImageToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_atlascloud_wan22_i2v_lora_node_metadata():
    from src.atlascloud_comfyui.nodes.video.atlascloud_wan_2_2_i2v_lora import AtlasAtlascloudWan22ImageToVideoLora

    required = AtlasAtlascloudWan22ImageToVideoLora.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert "prompt" in required
    assert "loras_json" in required
    assert "high_noise_loras_json" in required
    assert "low_noise_loras_json" in required
    assert AtlasAtlascloudWan22ImageToVideoLora.RETURN_TYPES == ("STRING", "STRING")
