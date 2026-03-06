"""
Metadata-only tests for newly added nodes (2026-03-06).

These tests MUST NOT require ATLASCLOUD_API_KEY.
"""


def test_minimax_hailuo_02_i2v_standard_node_metadata():
    from src.atlascloud_comfyui.nodes.video.minimax_hailuo_02_i2v_standard import AtlasMinimaxHailuo02I2VStandard

    required = AtlasMinimaxHailuo02I2VStandard.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert AtlasMinimaxHailuo02I2VStandard.RETURN_TYPES == ("STRING", "STRING")


def test_kwaivgi_kling_v2_1_i2v_pro_node_metadata():
    from src.atlascloud_comfyui.nodes.video.kwaivgi_kling_v2_1_i2v_pro import AtlasKwaivgiKlingV21I2VPro

    required = AtlasKwaivgiKlingV21I2VPro.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert "prompt" in required
    assert AtlasKwaivgiKlingV21I2VPro.RETURN_TYPES == ("STRING", "STRING")


def test_kwaivgi_kling_v1_6_t2v_standard_node_metadata():
    from src.atlascloud_comfyui.nodes.video.kwaivgi_kling_v1_6_t2v_standard import AtlasKwaivgiKlingV16T2VStandard

    required = AtlasKwaivgiKlingV16T2VStandard.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert AtlasKwaivgiKlingV16T2VStandard.RETURN_TYPES == ("STRING", "STRING")


def test_kwaivgi_kling_v1_6_i2v_pro_node_metadata():
    from src.atlascloud_comfyui.nodes.video.kwaivgi_kling_v1_6_i2v_pro import AtlasKwaivgiKlingV16I2VPro

    required = AtlasKwaivgiKlingV16I2VPro.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert "prompt" in required
    assert AtlasKwaivgiKlingV16I2VPro.RETURN_TYPES == ("STRING", "STRING")


def test_alibaba_wan_2_2_i2v_480p_node_metadata():
    from src.atlascloud_comfyui.nodes.video.alibaba_wan_2_2_i2v_480p import AtlasAlibabaWan22I2V480p

    required = AtlasAlibabaWan22I2V480p.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert "prompt" in required
    assert AtlasAlibabaWan22I2V480p.RETURN_TYPES == ("STRING", "STRING")


def test_alibaba_wan_2_2_i2v_720p_node_metadata():
    from src.atlascloud_comfyui.nodes.video.alibaba_wan_2_2_i2v_720p import AtlasAlibabaWan22I2V720p

    required = AtlasAlibabaWan22I2V720p.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert "prompt" in required
    assert AtlasAlibabaWan22I2V720p.RETURN_TYPES == ("STRING", "STRING")


def test_alibaba_wan_2_2_t2v_480p_node_metadata():
    from src.atlascloud_comfyui.nodes.video.alibaba_wan_2_2_t2v_480p import AtlasAlibabaWan22T2V480p

    required = AtlasAlibabaWan22T2V480p.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert AtlasAlibabaWan22T2V480p.RETURN_TYPES == ("STRING", "STRING")


def test_bytedance_seedance_v1_pro_t2v_720p_node_metadata():
    from src.atlascloud_comfyui.nodes.video.bytedance_seedance_v1_pro_t2v_720p import AtlasBytedanceSeedanceV1ProT2V720p

    required = AtlasBytedanceSeedanceV1ProT2V720p.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert AtlasBytedanceSeedanceV1ProT2V720p.RETURN_TYPES == ("STRING", "STRING")


def test_bytedance_seedance_v1_pro_t2v_480p_node_metadata():
    from src.atlascloud_comfyui.nodes.video.bytedance_seedance_v1_pro_t2v_480p import AtlasBytedanceSeedanceV1ProT2V480p

    required = AtlasBytedanceSeedanceV1ProT2V480p.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert AtlasBytedanceSeedanceV1ProT2V480p.RETURN_TYPES == ("STRING", "STRING")


def test_bytedance_seedance_v1_pro_i2v_720p_node_metadata():
    from src.atlascloud_comfyui.nodes.video.bytedance_seedance_v1_pro_i2v_720p import AtlasBytedanceSeedanceV1ProI2V720p

    required = AtlasBytedanceSeedanceV1ProI2V720p.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert AtlasBytedanceSeedanceV1ProI2V720p.RETURN_TYPES == ("STRING", "STRING")


def test_bytedance_seedance_v1_pro_i2v_480p_node_metadata():
    from src.atlascloud_comfyui.nodes.video.bytedance_seedance_v1_pro_i2v_480p import AtlasBytedanceSeedanceV1ProI2V480p

    required = AtlasBytedanceSeedanceV1ProI2V480p.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert AtlasBytedanceSeedanceV1ProI2V480p.RETURN_TYPES == ("STRING", "STRING")


def test_bytedance_seedance_v1_pro_i2v_1080p_node_metadata():
    from src.atlascloud_comfyui.nodes.video.bytedance_seedance_v1_pro_i2v_1080p import AtlasBytedanceSeedanceV1ProI2V1080p

    required = AtlasBytedanceSeedanceV1ProI2V1080p.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert AtlasBytedanceSeedanceV1ProI2V1080p.RETURN_TYPES == ("STRING", "STRING")


def test_bytedance_seedance_v1_lite_t2v_480p_node_metadata():
    from src.atlascloud_comfyui.nodes.video.bytedance_seedance_v1_lite_t2v_480p import AtlasBytedanceSeedanceV1LiteT2V480p

    required = AtlasBytedanceSeedanceV1LiteT2V480p.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert AtlasBytedanceSeedanceV1LiteT2V480p.RETURN_TYPES == ("STRING", "STRING")


def test_bytedance_seedance_v1_lite_i2v_720p_node_metadata():
    from src.atlascloud_comfyui.nodes.video.bytedance_seedance_v1_lite_i2v_720p import AtlasBytedanceSeedanceV1LiteI2V720p

    required = AtlasBytedanceSeedanceV1LiteI2V720p.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert AtlasBytedanceSeedanceV1LiteI2V720p.RETURN_TYPES == ("STRING", "STRING")


def test_bytedance_seedance_v1_lite_i2v_480p_node_metadata():
    from src.atlascloud_comfyui.nodes.video.bytedance_seedance_v1_lite_i2v_480p import AtlasBytedanceSeedanceV1LiteI2V480p

    required = AtlasBytedanceSeedanceV1LiteI2V480p.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert AtlasBytedanceSeedanceV1LiteI2V480p.RETURN_TYPES == ("STRING", "STRING")
