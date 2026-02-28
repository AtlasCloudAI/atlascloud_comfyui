#!/usr/bin/env python

"""Tests for `atlascloud_comfyui` package.

Covers:
- AtlasClientNode (auth): INPUT_TYPES, RETURN_NAMES, instantiation.
- Model nodes (video/image): INPUT_TYPES, RETURN_TYPES, instantiation.
  Ensures nodes added by OpenClaw are usable before push.
"""

import pytest
from src.atlascloud_comfyui.nodes.auth.atlas_client_node import AtlasClientNode


@pytest.fixture
def atlas_client_node():
    """Fixture to create an AtlasClientNode instance."""
    return AtlasClientNode()


def test_atlas_client_node_initialization(atlas_client_node):
    """Test that AtlasClientNode can be instantiated."""
    assert isinstance(atlas_client_node, AtlasClientNode)


def test_atlas_client_node_metadata():
    """Test AtlasClientNode INPUT_TYPES and RETURN_NAMES."""
    assert AtlasClientNode.RETURN_NAMES == ("atlas_client",)
    assert AtlasClientNode.INPUT_TYPES() == {
        "required": {
            "api_key": ("STRING", {"default": ""}),
        },
        "optional": {
            "base_url": ("STRING", {"default": "https://api.atlascloud.ai"}),
        },
    }


# Model nodes: ensure INPUT_TYPES and RETURN_TYPES are correct so nodes are usable
def test_wan26_t2v_node_metadata():
    """Test WAN2.6 Text-to-Video node metadata."""
    from src.atlascloud_comfyui.nodes.video.wan26_t2v import AtlasWAN26TextToVideo

    assert "atlas_client" in [k for k, _ in AtlasWAN26TextToVideo.INPUT_TYPES()["required"].items()]
    assert AtlasWAN26TextToVideo.RETURN_TYPES == ("STRING", "STRING")
    assert "video_url" in AtlasWAN26TextToVideo.RETURN_NAMES


def test_flux2_flex_t2i_node_metadata():
    """Test Flux2 Flex Text-to-Image node metadata."""
    from src.atlascloud_comfyui.nodes.image.flux2_flex_t2i import AtlasFlux2FlexTextToImage

    assert "atlas_client" in [k for k, _ in AtlasFlux2FlexTextToImage.INPUT_TYPES()["required"].items()]
    assert AtlasFlux2FlexTextToImage.RETURN_TYPES == ("STRING", "STRING")


# --- Batch 1: Newest models (NEW badge) ---


def test_nano_banana2_t2i_node_metadata():
    from src.atlascloud_comfyui.nodes.image.nano_banana2_t2i import AtlasNanoBanana2TextToImage

    assert "atlas_client" in AtlasNanoBanana2TextToImage.INPUT_TYPES()["required"]
    assert AtlasNanoBanana2TextToImage.RETURN_TYPES == ("STRING", "STRING")
    assert "image_url" in AtlasNanoBanana2TextToImage.RETURN_NAMES


def test_nano_banana2_t2i_dev_node_metadata():
    from src.atlascloud_comfyui.nodes.image.nano_banana2_t2i_dev import AtlasNanoBanana2TextToImageDev

    assert "atlas_client" in AtlasNanoBanana2TextToImageDev.INPUT_TYPES()["required"]
    assert AtlasNanoBanana2TextToImageDev.RETURN_TYPES == ("STRING", "STRING")
    assert "image_url" in AtlasNanoBanana2TextToImageDev.RETURN_NAMES


def test_nano_banana2_edit_node_metadata():
    from src.atlascloud_comfyui.nodes.image.nano_banana2_edit import AtlasNanoBanana2Edit

    assert "atlas_client" in AtlasNanoBanana2Edit.INPUT_TYPES()["required"]
    assert "image" in AtlasNanoBanana2Edit.INPUT_TYPES()["required"]
    assert AtlasNanoBanana2Edit.RETURN_TYPES == ("STRING", "STRING")


def test_nano_banana2_edit_dev_node_metadata():
    from src.atlascloud_comfyui.nodes.image.nano_banana2_edit_dev import AtlasNanoBanana2EditDev

    assert "atlas_client" in AtlasNanoBanana2EditDev.INPUT_TYPES()["required"]
    assert "image" in AtlasNanoBanana2EditDev.INPUT_TYPES()["required"]
    assert AtlasNanoBanana2EditDev.RETURN_TYPES == ("STRING", "STRING")


def test_seedream_v50_lite_t2i_node_metadata():
    from src.atlascloud_comfyui.nodes.image.seedream_v50_lite_t2i import AtlasSeedreamV50LiteTextToImage

    assert "atlas_client" in AtlasSeedreamV50LiteTextToImage.INPUT_TYPES()["required"]
    assert AtlasSeedreamV50LiteTextToImage.RETURN_TYPES == ("STRING", "STRING")
    assert "image_url" in AtlasSeedreamV50LiteTextToImage.RETURN_NAMES


def test_seedream_v50_lite_edit_node_metadata():
    from src.atlascloud_comfyui.nodes.image.seedream_v50_lite_edit import AtlasSeedreamV50LiteEdit

    assert "atlas_client" in AtlasSeedreamV50LiteEdit.INPUT_TYPES()["required"]
    assert "image" in AtlasSeedreamV50LiteEdit.INPUT_TYPES()["required"]
    assert AtlasSeedreamV50LiteEdit.RETURN_TYPES == ("STRING", "STRING")


def test_vidu_q3_i2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.vidu_q3_i2v import AtlasViduQ3ImageToVideo

    assert "atlas_client" in AtlasViduQ3ImageToVideo.INPUT_TYPES()["required"]
    assert "image" in AtlasViduQ3ImageToVideo.INPUT_TYPES()["required"]
    assert AtlasViduQ3ImageToVideo.RETURN_TYPES == ("STRING", "STRING")
    assert "video_url" in AtlasViduQ3ImageToVideo.RETURN_NAMES


# --- Batch 2: Recent HOT models ---


def test_veo3_t2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.veo3_t2v import AtlasVeo3TextToVideo

    assert "atlas_client" in AtlasVeo3TextToVideo.INPUT_TYPES()["required"]
    assert AtlasVeo3TextToVideo.RETURN_TYPES == ("STRING", "STRING")
    assert "video_url" in AtlasVeo3TextToVideo.RETURN_NAMES


def test_imagen4_t2i_node_metadata():
    from src.atlascloud_comfyui.nodes.image.imagen4_t2i import AtlasImagen4TextToImage

    assert "atlas_client" in AtlasImagen4TextToImage.INPUT_TYPES()["required"]
    assert AtlasImagen4TextToImage.RETURN_TYPES == ("STRING", "STRING")
    assert "image_url" in AtlasImagen4TextToImage.RETURN_NAMES


def test_imagen4_fast_t2i_node_metadata():
    from src.atlascloud_comfyui.nodes.image.imagen4_fast_t2i import AtlasImagen4FastTextToImage

    assert "atlas_client" in AtlasImagen4FastTextToImage.INPUT_TYPES()["required"]
    assert AtlasImagen4FastTextToImage.RETURN_TYPES == ("STRING", "STRING")
    assert "image_url" in AtlasImagen4FastTextToImage.RETURN_NAMES


def test_luma_ray2_t2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.luma_ray2_t2v import AtlasLumaRay2TextToVideo

    assert "atlas_client" in AtlasLumaRay2TextToVideo.INPUT_TYPES()["required"]
    assert AtlasLumaRay2TextToVideo.RETURN_TYPES == ("STRING", "STRING")
    assert "video_url" in AtlasLumaRay2TextToVideo.RETURN_NAMES


def test_luma_ray2_i2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.luma_ray2_i2v import AtlasLumaRay2ImageToVideo

    assert "atlas_client" in AtlasLumaRay2ImageToVideo.INPUT_TYPES()["required"]
    assert "image" in AtlasLumaRay2ImageToVideo.INPUT_TYPES()["required"]
    assert AtlasLumaRay2ImageToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_pika_v22_t2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.pika_v22_t2v import AtlasPikaV22TextToVideo

    assert "atlas_client" in AtlasPikaV22TextToVideo.INPUT_TYPES()["required"]
    assert AtlasPikaV22TextToVideo.RETURN_TYPES == ("STRING", "STRING")
    assert "video_url" in AtlasPikaV22TextToVideo.RETURN_NAMES


def test_pixverse_v45_t2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.pixverse_v45_t2v import AtlasPixVerseV45TextToVideo

    assert "atlas_client" in AtlasPixVerseV45TextToVideo.INPUT_TYPES()["required"]
    assert AtlasPixVerseV45TextToVideo.RETURN_TYPES == ("STRING", "STRING")
    assert "video_url" in AtlasPixVerseV45TextToVideo.RETURN_NAMES


def test_hailuo_02_t2v_pro_node_metadata():
    from src.atlascloud_comfyui.nodes.video.hailuo_02_t2v_pro import AtlasHailuo02T2VPro

    assert "atlas_client" in AtlasHailuo02T2VPro.INPUT_TYPES()["required"]
    assert AtlasHailuo02T2VPro.RETURN_TYPES == ("STRING", "STRING")
    assert "video_url" in AtlasHailuo02T2VPro.RETURN_NAMES


def test_sora2_i2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.sora2_i2v import AtlasSora2ImageToVideo

    assert "atlas_client" in AtlasSora2ImageToVideo.INPUT_TYPES()["required"]
    assert "image" in AtlasSora2ImageToVideo.INPUT_TYPES()["required"]
    assert AtlasSora2ImageToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_kling_v25_turbo_pro_t2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.kling_v25_turbo_pro_t2v import AtlasKlingV25TurboProTextToVideo

    assert "atlas_client" in AtlasKlingV25TurboProTextToVideo.INPUT_TYPES()["required"]
    assert AtlasKlingV25TurboProTextToVideo.RETURN_TYPES == ("STRING", "STRING")
    assert "video_url" in AtlasKlingV25TurboProTextToVideo.RETURN_NAMES


def test_hunyuan_t2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.hunyuan_t2v import AtlasHunyuanTextToVideo

    assert "atlas_client" in AtlasHunyuanTextToVideo.INPUT_TYPES()["required"]
    assert AtlasHunyuanTextToVideo.RETURN_TYPES == ("STRING", "STRING")
    assert "video_url" in AtlasHunyuanTextToVideo.RETURN_NAMES


# --- Batch 3: Additional models ---


def test_veo3_fast_t2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.veo3_fast_t2v import AtlasVeo3FastTextToVideo

    assert "atlas_client" in AtlasVeo3FastTextToVideo.INPUT_TYPES()["required"]
    assert AtlasVeo3FastTextToVideo.RETURN_TYPES == ("STRING", "STRING")
    assert "video_url" in AtlasVeo3FastTextToVideo.RETURN_NAMES


def test_veo31_i2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.veo31_i2v import AtlasVeo31ImageToVideo

    assert "atlas_client" in AtlasVeo31ImageToVideo.INPUT_TYPES()["required"]
    assert "image" in AtlasVeo31ImageToVideo.INPUT_TYPES()["required"]
    assert AtlasVeo31ImageToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_veo3_i2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.veo3_i2v import AtlasVeo3ImageToVideo

    assert "atlas_client" in AtlasVeo3ImageToVideo.INPUT_TYPES()["required"]
    assert "image" in AtlasVeo3ImageToVideo.INPUT_TYPES()["required"]
    assert AtlasVeo3ImageToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_veo2_t2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.veo2_t2v import AtlasVeo2TextToVideo

    assert "atlas_client" in AtlasVeo2TextToVideo.INPUT_TYPES()["required"]
    assert AtlasVeo2TextToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_veo2_i2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.veo2_i2v import AtlasVeo2ImageToVideo

    assert "atlas_client" in AtlasVeo2ImageToVideo.INPUT_TYPES()["required"]
    assert "image" in AtlasVeo2ImageToVideo.INPUT_TYPES()["required"]
    assert AtlasVeo2ImageToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_luma_ray2_flash_t2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.luma_ray2_flash_t2v import AtlasLumaRay2FlashTextToVideo

    assert "atlas_client" in AtlasLumaRay2FlashTextToVideo.INPUT_TYPES()["required"]
    assert AtlasLumaRay2FlashTextToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_pika_v20_turbo_t2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.pika_v20_turbo_t2v import AtlasPikaV20TurboTextToVideo

    assert "atlas_client" in AtlasPikaV20TurboTextToVideo.INPUT_TYPES()["required"]
    assert AtlasPikaV20TurboTextToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_pika_v21_i2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.pika_v21_i2v import AtlasPikaV21ImageToVideo

    assert "atlas_client" in AtlasPikaV21ImageToVideo.INPUT_TYPES()["required"]
    assert "image" in AtlasPikaV21ImageToVideo.INPUT_TYPES()["required"]
    assert AtlasPikaV21ImageToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_pixverse_v45_i2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.pixverse_v45_i2v import AtlasPixVerseV45ImageToVideo

    assert "atlas_client" in AtlasPixVerseV45ImageToVideo.INPUT_TYPES()["required"]
    assert "image" in AtlasPixVerseV45ImageToVideo.INPUT_TYPES()["required"]
    assert AtlasPixVerseV45ImageToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_hailuo_02_i2v_pro_node_metadata():
    from src.atlascloud_comfyui.nodes.video.hailuo_02_i2v_pro import AtlasHailuo02I2VPro

    assert "atlas_client" in AtlasHailuo02I2VPro.INPUT_TYPES()["required"]
    assert "image" in AtlasHailuo02I2VPro.INPUT_TYPES()["required"]
    assert AtlasHailuo02I2VPro.RETURN_TYPES == ("STRING", "STRING")


def test_sora2_i2v_pro_node_metadata():
    from src.atlascloud_comfyui.nodes.video.sora2_i2v_pro import AtlasSora2ImageToVideoPro

    assert "atlas_client" in AtlasSora2ImageToVideoPro.INPUT_TYPES()["required"]
    assert "image" in AtlasSora2ImageToVideoPro.INPUT_TYPES()["required"]
    assert AtlasSora2ImageToVideoPro.RETURN_TYPES == ("STRING", "STRING")


def test_sora2_t2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.sora2_t2v import AtlasSora2TextToVideo

    assert "atlas_client" in AtlasSora2TextToVideo.INPUT_TYPES()["required"]
    assert AtlasSora2TextToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_kling_v25_turbo_pro_i2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.kling_v25_turbo_pro_i2v import AtlasKlingV25TurboProImageToVideo

    assert "atlas_client" in AtlasKlingV25TurboProImageToVideo.INPUT_TYPES()["required"]
    assert "image" in AtlasKlingV25TurboProImageToVideo.INPUT_TYPES()["required"]
    assert AtlasKlingV25TurboProImageToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_hunyuan_i2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.hunyuan_i2v import AtlasHunyuanImageToVideo

    assert "atlas_client" in AtlasHunyuanImageToVideo.INPUT_TYPES()["required"]
    assert "image" in AtlasHunyuanImageToVideo.INPUT_TYPES()["required"]
    assert AtlasHunyuanImageToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_wan25_i2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.wan25_i2v import AtlasWAN25ImageToVideo

    assert "atlas_client" in AtlasWAN25ImageToVideo.INPUT_TYPES()["required"]
    assert "image" in AtlasWAN25ImageToVideo.INPUT_TYPES()["required"]
    assert AtlasWAN25ImageToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_imagen4_ultra_t2i_node_metadata():
    from src.atlascloud_comfyui.nodes.image.imagen4_ultra_t2i import AtlasImagen4UltraTextToImage

    assert "atlas_client" in AtlasImagen4UltraTextToImage.INPUT_TYPES()["required"]
    assert AtlasImagen4UltraTextToImage.RETURN_TYPES == ("STRING", "STRING")


def test_imagen3_t2i_node_metadata():
    from src.atlascloud_comfyui.nodes.image.imagen3_t2i import AtlasImagen3TextToImage

    assert "atlas_client" in AtlasImagen3TextToImage.INPUT_TYPES()["required"]
    assert AtlasImagen3TextToImage.RETURN_TYPES == ("STRING", "STRING")


def test_ideogram_v3_quality_t2i_node_metadata():
    from src.atlascloud_comfyui.nodes.image.ideogram_v3_quality_t2i import AtlasIdeogramV3QualityTextToImage

    assert "atlas_client" in AtlasIdeogramV3QualityTextToImage.INPUT_TYPES()["required"]
    assert AtlasIdeogramV3QualityTextToImage.RETURN_TYPES == ("STRING", "STRING")


def test_ideogram_v3_turbo_t2i_node_metadata():
    from src.atlascloud_comfyui.nodes.image.ideogram_v3_turbo_t2i import AtlasIdeogramV3TurboTextToImage

    assert "atlas_client" in AtlasIdeogramV3TurboTextToImage.INPUT_TYPES()["required"]
    assert AtlasIdeogramV3TurboTextToImage.RETURN_TYPES == ("STRING", "STRING")


def test_luma_photon_t2i_node_metadata():
    from src.atlascloud_comfyui.nodes.image.luma_photon_t2i import AtlasLumaPhotonTextToImage

    assert "atlas_client" in AtlasLumaPhotonTextToImage.INPUT_TYPES()["required"]
    assert AtlasLumaPhotonTextToImage.RETURN_TYPES == ("STRING", "STRING")


def test_luma_photon_flash_t2i_node_metadata():
    from src.atlascloud_comfyui.nodes.image.luma_photon_flash_t2i import AtlasLumaPhotonFlashTextToImage

    assert "atlas_client" in AtlasLumaPhotonFlashTextToImage.INPUT_TYPES()["required"]
    assert AtlasLumaPhotonFlashTextToImage.RETURN_TYPES == ("STRING", "STRING")


def test_recraft_v3_t2i_node_metadata():
    from src.atlascloud_comfyui.nodes.image.recraft_v3_t2i import AtlasRecraftV3TextToImage

    assert "atlas_client" in AtlasRecraftV3TextToImage.INPUT_TYPES()["required"]
    assert AtlasRecraftV3TextToImage.RETURN_TYPES == ("STRING", "STRING")
