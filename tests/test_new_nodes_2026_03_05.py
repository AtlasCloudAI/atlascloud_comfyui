"""
Metadata-only tests for newly added nodes (2026-03-05).

These tests MUST NOT require ATLASCLOUD_API_KEY.
"""


def test_hailuo_23_t2v_standard_node_metadata():
    from src.atlascloud_comfyui.nodes.video.hailuo_23_t2v_standard import AtlasHailuo23T2VStandard

    required = AtlasHailuo23T2VStandard.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert AtlasHailuo23T2VStandard.RETURN_TYPES == ("STRING", "STRING")


def test_hailuo_23_i2v_standard_node_metadata():
    from src.atlascloud_comfyui.nodes.video.hailuo_23_i2v_standard import AtlasHailuo23I2VStandard

    required = AtlasHailuo23I2VStandard.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert AtlasHailuo23I2VStandard.RETURN_TYPES == ("STRING", "STRING")


def test_hailuo_23_i2v_pro_node_metadata():
    from src.atlascloud_comfyui.nodes.video.hailuo_23_i2v_pro import AtlasHailuo23I2VPro

    required = AtlasHailuo23I2VPro.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert AtlasHailuo23I2VPro.RETURN_TYPES == ("STRING", "STRING")


def test_hailuo_23_fast_node_metadata():
    from src.atlascloud_comfyui.nodes.video.hailuo_23_fast import AtlasHailuo23Fast

    required = AtlasHailuo23Fast.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert AtlasHailuo23Fast.RETURN_TYPES == ("STRING", "STRING")


def test_hailuo_02_fast_node_metadata():
    from src.atlascloud_comfyui.nodes.video.hailuo_02_fast import AtlasHailuo02Fast

    required = AtlasHailuo02Fast.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert AtlasHailuo02Fast.RETURN_TYPES == ("STRING", "STRING")


def test_hailuo_02_pro_node_metadata():
    from src.atlascloud_comfyui.nodes.video.hailuo_02_pro import AtlasHailuo02Pro

    required = AtlasHailuo02Pro.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert AtlasHailuo02Pro.RETURN_TYPES == ("STRING", "STRING")


def test_hailuo_02_t2v_standard_node_metadata():
    from src.atlascloud_comfyui.nodes.video.hailuo_02_t2v_standard import AtlasHailuo02T2VStandard

    required = AtlasHailuo02T2VStandard.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert AtlasHailuo02T2VStandard.RETURN_TYPES == ("STRING", "STRING")


def test_kling_v21_i2v_master_node_metadata():
    from src.atlascloud_comfyui.nodes.video.kling_v21_i2v_master import AtlasKlingV21I2VMaster

    required = AtlasKlingV21I2VMaster.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert "prompt" in required
    assert AtlasKlingV21I2VMaster.RETURN_TYPES == ("STRING", "STRING")


def test_kling_v21_i2v_pro_start_end_frame_node_metadata():
    from src.atlascloud_comfyui.nodes.video.kling_v21_i2v_pro_start_end_frame import AtlasKlingV21I2VProStartEndFrame

    required = AtlasKlingV21I2VProStartEndFrame.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert "end_image" in required
    assert "prompt" in required
    assert AtlasKlingV21I2VProStartEndFrame.RETURN_TYPES == ("STRING", "STRING")


def test_kling_v16_multi_i2v_pro_node_metadata():
    from src.atlascloud_comfyui.nodes.video.kling_v16_multi_i2v_pro import AtlasKlingV16MultiI2VPro

    required = AtlasKlingV16MultiI2VPro.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "images" in required
    assert "prompt" in required
    assert AtlasKlingV16MultiI2VPro.RETURN_TYPES == ("STRING", "STRING")


def test_kling_v16_multi_i2v_standard_node_metadata():
    from src.atlascloud_comfyui.nodes.video.kling_v16_multi_i2v_standard import AtlasKlingV16MultiI2VStandard

    required = AtlasKlingV16MultiI2VStandard.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "images" in required
    assert "prompt" in required
    assert AtlasKlingV16MultiI2VStandard.RETURN_TYPES == ("STRING", "STRING")


def test_kling_effects_node_metadata():
    from src.atlascloud_comfyui.nodes.video.kling_effects import AtlasKlingEffects

    required = AtlasKlingEffects.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert "effect_scene" in required
    assert AtlasKlingEffects.RETURN_TYPES == ("STRING", "STRING")


def test_seedance_v1_lite_t2v_1080p_node_metadata():
    from src.atlascloud_comfyui.nodes.video.seedance_v1_lite_t2v_1080p import AtlasSeedanceV1LiteT2V1080p

    required = AtlasSeedanceV1LiteT2V1080p.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert AtlasSeedanceV1LiteT2V1080p.RETURN_TYPES == ("STRING", "STRING")


def test_seedance_v1_lite_t2v_720p_node_metadata():
    from src.atlascloud_comfyui.nodes.video.seedance_v1_lite_t2v_720p import AtlasSeedanceV1LiteT2V720p

    required = AtlasSeedanceV1LiteT2V720p.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert "duration" in required
    assert AtlasSeedanceV1LiteT2V720p.RETURN_TYPES == ("STRING", "STRING")


def test_seedance_v1_lite_i2v_1080p_node_metadata():
    from src.atlascloud_comfyui.nodes.video.seedance_v1_lite_i2v_1080p import AtlasSeedanceV1LiteI2V1080p

    required = AtlasSeedanceV1LiteI2V1080p.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert AtlasSeedanceV1LiteI2V1080p.RETURN_TYPES == ("STRING", "STRING")
