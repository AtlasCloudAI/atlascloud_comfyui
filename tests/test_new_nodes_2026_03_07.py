"""Metadata-only tests for newly added nodes (2026-03-07).

These tests MUST NOT require ATLASCLOUD_API_KEY.
"""


def test_wan25_t2i_node_metadata():
    from src.atlascloud_comfyui.nodes.image.wan25_t2i import AtlasWan25TextToImage

    required = AtlasWan25TextToImage.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert "size" in required
    assert AtlasWan25TextToImage.RETURN_TYPES == ("STRING", "STRING")


def test_atlascloud_qwen_image_t2i_node_metadata():
    from src.atlascloud_comfyui.nodes.image.qwen_image_t2i_atlascloud import AtlasAtlascloudQwenImageTextToImage

    required = AtlasAtlascloudQwenImageTextToImage.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert "size" in required
    assert AtlasAtlascloudQwenImageTextToImage.RETURN_TYPES == ("STRING", "STRING")


def test_alibaba_qwen_image_edit_node_metadata():
    from src.atlascloud_comfyui.nodes.image.qwen_image_edit_alibaba import AtlasAlibabaQwenImageEdit

    required = AtlasAlibabaQwenImageEdit.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert "images" in required
    assert AtlasAlibabaQwenImageEdit.RETURN_TYPES == ("STRING", "STRING")


def test_alibaba_qwen_image_edit_plus_node_metadata():
    from src.atlascloud_comfyui.nodes.image.qwen_image_edit_plus_alibaba import AtlasAlibabaQwenImageEditPlus

    required = AtlasAlibabaQwenImageEditPlus.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert "images" in required
    assert "size" in required
    assert AtlasAlibabaQwenImageEditPlus.RETURN_TYPES == ("STRING", "STRING")


def test_seedream_v4_t2i_node_metadata():
    from src.atlascloud_comfyui.nodes.image.seedream_v4_t2i import AtlasSeedreamV4TextToImage

    required = AtlasSeedreamV4TextToImage.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert "size" in required
    assert AtlasSeedreamV4TextToImage.RETURN_TYPES == ("STRING", "STRING")


def test_seedream_v4_sequential_t2i_node_metadata():
    from src.atlascloud_comfyui.nodes.image.seedream_v4_sequential_t2i import AtlasSeedreamV4SequentialTextToImage

    required = AtlasSeedreamV4SequentialTextToImage.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert "size" in required
    assert AtlasSeedreamV4SequentialTextToImage.RETURN_TYPES == ("STRING", "STRING")


def test_seedream_v4_edit_node_metadata():
    from src.atlascloud_comfyui.nodes.image.seedream_v4_edit import AtlasSeedreamV4Edit

    required = AtlasSeedreamV4Edit.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert "images" in required
    assert "size" in required
    assert AtlasSeedreamV4Edit.RETURN_TYPES == ("STRING", "STRING")


def test_seedream_v4_edit_sequential_node_metadata():
    from src.atlascloud_comfyui.nodes.image.seedream_v4_edit_sequential import AtlasSeedreamV4EditSequential

    required = AtlasSeedreamV4EditSequential.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert "images" in required
    assert "size" in required
    assert AtlasSeedreamV4EditSequential.RETURN_TYPES == ("STRING", "STRING")


def test_flux_dev_t2i_node_metadata():
    from src.atlascloud_comfyui.nodes.image.flux_dev_t2i import AtlasFluxDevTextToImage

    required = AtlasFluxDevTextToImage.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert "image" in required
    assert "size" in required
    assert AtlasFluxDevTextToImage.RETURN_TYPES == ("STRING", "STRING")


def test_flux_dev_lora_t2i_node_metadata():
    from src.atlascloud_comfyui.nodes.image.flux_dev_lora_t2i import AtlasFluxDevLoraTextToImage

    required = AtlasFluxDevLoraTextToImage.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert "image" in required
    assert "size" in required
    assert AtlasFluxDevLoraTextToImage.RETURN_TYPES == ("STRING", "STRING")


def test_van25_t2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.van25_t2v import AtlasAtlascloudVan25TextToVideo

    required = AtlasAtlascloudVan25TextToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert "size" in required
    assert AtlasAtlascloudVan25TextToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_van25_i2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.van25_i2v import AtlasAtlascloudVan25ImageToVideo

    required = AtlasAtlascloudVan25ImageToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert "image" in required
    assert "resolution" in required
    assert AtlasAtlascloudVan25ImageToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_wan22_animate_mix_node_metadata():
    from src.atlascloud_comfyui.nodes.video.wan22_animate_mix import AtlasWan22AnimateMix

    required = AtlasWan22AnimateMix.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert "video" in required
    assert "mode" in required
    assert AtlasWan22AnimateMix.RETURN_TYPES == ("STRING", "STRING")


def test_wan22_animate_move_node_metadata():
    from src.atlascloud_comfyui.nodes.video.wan22_animate_move import AtlasWan22AnimateMove

    required = AtlasWan22AnimateMove.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert "video" in required
    assert "mode" in required
    assert AtlasWan22AnimateMove.RETURN_TYPES == ("STRING", "STRING")


def test_kling_v21_i2v_standard_node_metadata():
    from src.atlascloud_comfyui.nodes.video.kwaivgi_kling_v2_1_i2v_standard import AtlasKwaivgiKlingV21I2VStandard

    required = AtlasKwaivgiKlingV21I2VStandard.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert "image" in required
    assert AtlasKwaivgiKlingV21I2VStandard.RETURN_TYPES == ("STRING", "STRING")
