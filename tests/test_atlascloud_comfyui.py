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

def test_vidu_q3_pro_t2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.vidu_q3_pro_t2v import AtlasViduQ3ProTextToVideo

    assert "atlas_client" in AtlasViduQ3ProTextToVideo.INPUT_TYPES()["required"]
    assert AtlasViduQ3ProTextToVideo.RETURN_TYPES == ("STRING", "STRING")
    assert "video_url" in AtlasViduQ3ProTextToVideo.RETURN_NAMES

def test_vidu_q3_pro_i2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.vidu_q3_pro_i2v import AtlasViduQ3ProImageToVideo

    assert "atlas_client" in AtlasViduQ3ProImageToVideo.INPUT_TYPES()["required"]
    assert "image" in AtlasViduQ3ProImageToVideo.INPUT_TYPES()["required"]
    assert AtlasViduQ3ProImageToVideo.RETURN_TYPES == ("STRING", "STRING")
    assert "video_url" in AtlasViduQ3ProImageToVideo.RETURN_NAMES

def test_vidu_q3_pro_start_end_to_video_node_metadata():
    from src.atlascloud_comfyui.nodes.video.vidu_q3_pro_start_end_to_video import AtlasViduQ3ProStartEndToVideo

    assert "atlas_client" in AtlasViduQ3ProStartEndToVideo.INPUT_TYPES()["required"]
    assert "image" in AtlasViduQ3ProStartEndToVideo.INPUT_TYPES()["required"]
    assert "end_image" in AtlasViduQ3ProStartEndToVideo.INPUT_TYPES()["required"]
    assert AtlasViduQ3ProStartEndToVideo.RETURN_TYPES == ("STRING", "STRING")
    assert "video_url" in AtlasViduQ3ProStartEndToVideo.RETURN_NAMES

def test_vidu_q3_turbo_t2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.vidu_q3_turbo_t2v import AtlasViduQ3TurboTextToVideo

    assert "atlas_client" in AtlasViduQ3TurboTextToVideo.INPUT_TYPES()["required"]
    assert AtlasViduQ3TurboTextToVideo.RETURN_TYPES == ("STRING", "STRING")
    assert "video_url" in AtlasViduQ3TurboTextToVideo.RETURN_NAMES

def test_vidu_q3_turbo_i2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.vidu_q3_turbo_i2v import AtlasViduQ3TurboImageToVideo

    assert "atlas_client" in AtlasViduQ3TurboImageToVideo.INPUT_TYPES()["required"]
    assert "image" in AtlasViduQ3TurboImageToVideo.INPUT_TYPES()["required"]
    assert AtlasViduQ3TurboImageToVideo.RETURN_TYPES == ("STRING", "STRING")
    assert "video_url" in AtlasViduQ3TurboImageToVideo.RETURN_NAMES

def test_vidu_q3_turbo_start_end_to_video_node_metadata():
    from src.atlascloud_comfyui.nodes.video.vidu_q3_turbo_start_end_to_video import AtlasViduQ3TurboStartEndToVideo

    assert "atlas_client" in AtlasViduQ3TurboStartEndToVideo.INPUT_TYPES()["required"]
    assert "image" in AtlasViduQ3TurboStartEndToVideo.INPUT_TYPES()["required"]
    assert "end_image" in AtlasViduQ3TurboStartEndToVideo.INPUT_TYPES()["required"]
    assert AtlasViduQ3TurboStartEndToVideo.RETURN_TYPES == ("STRING", "STRING")
    assert "video_url" in AtlasViduQ3TurboStartEndToVideo.RETURN_NAMES

def test_wan22_spicy_i2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.wan22_spicy_i2v import AtlasWan22SpicyImageToVideo

    assert "atlas_client" in AtlasWan22SpicyImageToVideo.INPUT_TYPES()["required"]
    assert "image" in AtlasWan22SpicyImageToVideo.INPUT_TYPES()["required"]
    assert AtlasWan22SpicyImageToVideo.RETURN_TYPES == ("STRING", "STRING")

def test_wan22_spicy_i2v_lora_node_metadata():
    from src.atlascloud_comfyui.nodes.video.wan22_spicy_i2v_lora import AtlasWan22SpicyImageToVideoLora

    assert "atlas_client" in AtlasWan22SpicyImageToVideoLora.INPUT_TYPES()["required"]
    assert "image" in AtlasWan22SpicyImageToVideoLora.INPUT_TYPES()["required"]
    assert "loras_json" in AtlasWan22SpicyImageToVideoLora.INPUT_TYPES()["required"]
    assert AtlasWan22SpicyImageToVideoLora.RETURN_TYPES == ("STRING", "STRING")

def test_wan22_turbo_spicy_i2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.wan22_turbo_spicy_i2v import AtlasWan22TurboSpicyImageToVideo

    assert "atlas_client" in AtlasWan22TurboSpicyImageToVideo.INPUT_TYPES()["required"]
    assert "image" in AtlasWan22TurboSpicyImageToVideo.INPUT_TYPES()["required"]
    assert AtlasWan22TurboSpicyImageToVideo.RETURN_TYPES == ("STRING", "STRING")

def test_wan22_turbo_spicy_i2v_lora_node_metadata():
    from src.atlascloud_comfyui.nodes.video.wan22_turbo_spicy_i2v_lora import AtlasWan22TurboSpicyImageToVideoLora

    assert "atlas_client" in AtlasWan22TurboSpicyImageToVideoLora.INPUT_TYPES()["required"]
    assert "image" in AtlasWan22TurboSpicyImageToVideoLora.INPUT_TYPES()["required"]
    assert "low_noise_loras_json" in AtlasWan22TurboSpicyImageToVideoLora.INPUT_TYPES()["required"]
    assert "high_noise_loras_json" in AtlasWan22TurboSpicyImageToVideoLora.INPUT_TYPES()["required"]
    assert AtlasWan22TurboSpicyImageToVideoLora.RETURN_TYPES == ("STRING", "STRING")


def test_wan22_spicy_video_extend_lora_node_metadata():
    from src.atlascloud_comfyui.nodes.video.alibaba_wan_2_2_spicy_video_extend_lora import AtlasWan22SpicyVideoExtendLora

    assert "atlas_client" in AtlasWan22SpicyVideoExtendLora.INPUT_TYPES()["required"]
    assert "video" in AtlasWan22SpicyVideoExtendLora.INPUT_TYPES()["required"]
    assert "prompt" in AtlasWan22SpicyVideoExtendLora.INPUT_TYPES()["required"]
    assert AtlasWan22SpicyVideoExtendLora.RETURN_TYPES == ("STRING", "STRING")


def test_wan25_video_extend_node_metadata():
    from src.atlascloud_comfyui.nodes.video.alibaba_wan_2_5_video_extend import AtlasWan25VideoExtend

    assert "atlas_client" in AtlasWan25VideoExtend.INPUT_TYPES()["required"]
    assert "video" in AtlasWan25VideoExtend.INPUT_TYPES()["required"]
    assert "prompt" in AtlasWan25VideoExtend.INPUT_TYPES()["required"]
    assert AtlasWan25VideoExtend.RETURN_TYPES == ("STRING", "STRING")


def test_baidu_ernie_image_turbo_t2i_node_metadata():
    from src.atlascloud_comfyui.nodes.image.baidu_ernie_image_turbo_t2i import AtlasBaiduERNIEImageTurboTextToImage

    assert "atlas_client" in AtlasBaiduERNIEImageTurboTextToImage.INPUT_TYPES()["required"]
    assert "prompt" in AtlasBaiduERNIEImageTurboTextToImage.INPUT_TYPES()["required"]
    assert AtlasBaiduERNIEImageTurboTextToImage.RETURN_TYPES == ("STRING", "STRING")
    assert "image_url" in AtlasBaiduERNIEImageTurboTextToImage.RETURN_NAMES

def test_seedance_v15_pro_i2v_spicy_node_metadata():
    from src.atlascloud_comfyui.nodes.video.seedance_v15_pro_i2v_spicy import AtlasSeedanceV15ProImageToVideoSpicy

    assert "atlas_client" in AtlasSeedanceV15ProImageToVideoSpicy.INPUT_TYPES()["required"]
    assert "image" in AtlasSeedanceV15ProImageToVideoSpicy.INPUT_TYPES()["required"]
    assert AtlasSeedanceV15ProImageToVideoSpicy.RETURN_TYPES == ("STRING", "STRING")


# --- Batch 1.5: API high-priority models (2026-04-08) ---

def test_seedance_20_t2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.bytedance_seedance_2_0_t2v import AtlasSeedance20TextToVideo

    assert "atlas_client" in AtlasSeedance20TextToVideo.INPUT_TYPES()["required"]
    assert AtlasSeedance20TextToVideo.RETURN_TYPES == ("STRING", "STRING")


# --- Batch X: API high-priority visual models (2026-04-23) ---

def test_openai_gpt_image_2_t2i_node_metadata():
    from src.atlascloud_comfyui.nodes.image.openai_gpt_image_2_t2i import AtlasOpenAIGPTImage2TextToImage

    assert "atlas_client" in AtlasOpenAIGPTImage2TextToImage.INPUT_TYPES()["required"]
    assert "prompt" in AtlasOpenAIGPTImage2TextToImage.INPUT_TYPES()["required"]
    assert AtlasOpenAIGPTImage2TextToImage.RETURN_TYPES == ("STRING", "STRING")
    assert "image_url" in AtlasOpenAIGPTImage2TextToImage.RETURN_NAMES


def test_openai_gpt_image_2_edit_node_metadata():
    from src.atlascloud_comfyui.nodes.image.openai_gpt_image_2_edit import AtlasOpenAIGPTImage2Edit

    assert "atlas_client" in AtlasOpenAIGPTImage2Edit.INPUT_TYPES()["required"]
    assert "prompt" in AtlasOpenAIGPTImage2Edit.INPUT_TYPES()["required"]
    assert "images" in AtlasOpenAIGPTImage2Edit.INPUT_TYPES()["required"]
    assert AtlasOpenAIGPTImage2Edit.RETURN_TYPES == ("STRING", "STRING")
    assert "image_url" in AtlasOpenAIGPTImage2Edit.RETURN_NAMES


def test_openai_gpt_image_2_developer_t2i_node_metadata():
    from src.atlascloud_comfyui.nodes.image.openai_gpt_image_2_dev_t2i import (
        AtlasOpenAIGPTImage2DeveloperTextToImage,
    )

    assert "atlas_client" in AtlasOpenAIGPTImage2DeveloperTextToImage.INPUT_TYPES()["required"]
    assert "prompt" in AtlasOpenAIGPTImage2DeveloperTextToImage.INPUT_TYPES()["required"]
    assert AtlasOpenAIGPTImage2DeveloperTextToImage.RETURN_TYPES == ("STRING", "STRING")
    assert "image_url" in AtlasOpenAIGPTImage2DeveloperTextToImage.RETURN_NAMES


def test_openai_gpt_image_2_developer_edit_node_metadata():
    from src.atlascloud_comfyui.nodes.image.openai_gpt_image_2_dev_edit import AtlasOpenAIGPTImage2DeveloperEdit

    assert "atlas_client" in AtlasOpenAIGPTImage2DeveloperEdit.INPUT_TYPES()["required"]
    assert "prompt" in AtlasOpenAIGPTImage2DeveloperEdit.INPUT_TYPES()["required"]
    assert "images" in AtlasOpenAIGPTImage2DeveloperEdit.INPUT_TYPES()["required"]
    assert AtlasOpenAIGPTImage2DeveloperEdit.RETURN_TYPES == ("STRING", "STRING")
    assert "image_url" in AtlasOpenAIGPTImage2DeveloperEdit.RETURN_NAMES


def test_seedance_20_i2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.bytedance_seedance_2_0_i2v import AtlasSeedance20ImageToVideo

    assert "atlas_client" in AtlasSeedance20ImageToVideo.INPUT_TYPES()["required"]
    assert "image" in AtlasSeedance20ImageToVideo.INPUT_TYPES()["required"]
    assert AtlasSeedance20ImageToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_seedance_20_r2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.bytedance_seedance_2_0_r2v import AtlasSeedance20ReferenceToVideo

    assert "atlas_client" in AtlasSeedance20ReferenceToVideo.INPUT_TYPES()["required"]
    assert "reference_images" in AtlasSeedance20ReferenceToVideo.INPUT_TYPES()["required"]
    assert "reference_videos" in AtlasSeedance20ReferenceToVideo.INPUT_TYPES()["required"]


def test_seedance_20_t2v_upscaled_node_metadata():
    from src.atlascloud_comfyui.nodes.video.bytedance_seedance_2_0_t2v_upscaled import (
        AtlasSeedance20TextToVideoUpscaled,
    )

    assert "atlas_client" in AtlasSeedance20TextToVideoUpscaled.INPUT_TYPES()["required"]
    assert "prompt" in AtlasSeedance20TextToVideoUpscaled.INPUT_TYPES()["required"]
    assert AtlasSeedance20TextToVideoUpscaled.RETURN_TYPES == ("STRING", "STRING")


def test_seedance_20_i2v_upscaled_node_metadata():
    from src.atlascloud_comfyui.nodes.video.bytedance_seedance_2_0_i2v_upscaled import (
        AtlasSeedance20ImageToVideoUpscaled,
    )

    assert "atlas_client" in AtlasSeedance20ImageToVideoUpscaled.INPUT_TYPES()["required"]
    assert "image" in AtlasSeedance20ImageToVideoUpscaled.INPUT_TYPES()["required"]
    assert AtlasSeedance20ImageToVideoUpscaled.RETURN_TYPES == ("STRING", "STRING")


def test_seedance_20_r2v_upscaled_node_metadata():
    from src.atlascloud_comfyui.nodes.video.bytedance_seedance_2_0_r2v_upscaled import (
        AtlasSeedance20ReferenceToVideoUpscaled,
    )

    assert "atlas_client" in AtlasSeedance20ReferenceToVideoUpscaled.INPUT_TYPES()["required"]
    assert "reference_images" in AtlasSeedance20ReferenceToVideoUpscaled.INPUT_TYPES()["required"]
    assert "reference_videos" in AtlasSeedance20ReferenceToVideoUpscaled.INPUT_TYPES()["required"]
    assert AtlasSeedance20ReferenceToVideoUpscaled.RETURN_TYPES == ("STRING", "STRING")


def test_seedance_20_fast_t2v_upscaled_node_metadata():
    from src.atlascloud_comfyui.nodes.video.bytedance_seedance_2_0_fast_t2v_upscaled import (
        AtlasSeedance20FastTextToVideoUpscaled,
    )

    assert "atlas_client" in AtlasSeedance20FastTextToVideoUpscaled.INPUT_TYPES()["required"]
    assert "prompt" in AtlasSeedance20FastTextToVideoUpscaled.INPUT_TYPES()["required"]
    assert AtlasSeedance20FastTextToVideoUpscaled.RETURN_TYPES == ("STRING", "STRING")


def test_seedance_20_fast_i2v_upscaled_node_metadata():
    from src.atlascloud_comfyui.nodes.video.bytedance_seedance_2_0_fast_i2v_upscaled import (
        AtlasSeedance20FastImageToVideoUpscaled,
    )

    assert "atlas_client" in AtlasSeedance20FastImageToVideoUpscaled.INPUT_TYPES()["required"]
    assert "image" in AtlasSeedance20FastImageToVideoUpscaled.INPUT_TYPES()["required"]
    assert AtlasSeedance20FastImageToVideoUpscaled.RETURN_TYPES == ("STRING", "STRING")


def test_seedance_20_fast_r2v_upscaled_node_metadata():
    from src.atlascloud_comfyui.nodes.video.bytedance_seedance_2_0_fast_r2v_upscaled import (
        AtlasSeedance20FastReferenceToVideoUpscaled,
    )

    assert "atlas_client" in AtlasSeedance20FastReferenceToVideoUpscaled.INPUT_TYPES()["required"]
    assert "reference_images" in AtlasSeedance20FastReferenceToVideoUpscaled.INPUT_TYPES()["required"]
    assert "reference_videos" in AtlasSeedance20FastReferenceToVideoUpscaled.INPUT_TYPES()["required"]
    assert AtlasSeedance20FastReferenceToVideoUpscaled.RETURN_TYPES == ("STRING", "STRING")


def test_seedance_20_fast_t2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.bytedance_seedance_2_0_fast_t2v import AtlasSeedance20FastTextToVideo

    assert "atlas_client" in AtlasSeedance20FastTextToVideo.INPUT_TYPES()["required"]
    assert "prompt" in AtlasSeedance20FastTextToVideo.INPUT_TYPES()["required"]
    assert AtlasSeedance20FastTextToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_seedance_20_fast_i2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.bytedance_seedance_2_0_fast_i2v import AtlasSeedance20FastImageToVideo

    assert "atlas_client" in AtlasSeedance20FastImageToVideo.INPUT_TYPES()["required"]
    assert "image" in AtlasSeedance20FastImageToVideo.INPUT_TYPES()["required"]
    assert AtlasSeedance20FastImageToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_seedance_20_fast_r2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.bytedance_seedance_2_0_fast_r2v import AtlasSeedance20FastReferenceToVideo

    assert "atlas_client" in AtlasSeedance20FastReferenceToVideo.INPUT_TYPES()["required"]
    assert "reference_images" in AtlasSeedance20FastReferenceToVideo.INPUT_TYPES()["required"]
    assert "reference_videos" in AtlasSeedance20FastReferenceToVideo.INPUT_TYPES()["required"]
    assert AtlasSeedance20FastReferenceToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_wan27_t2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.alibaba_wan_2_7_t2v import AtlasWan27TextToVideo

    assert "atlas_client" in AtlasWan27TextToVideo.INPUT_TYPES()["required"]
    assert "prompt" in AtlasWan27TextToVideo.INPUT_TYPES()["required"]
    assert AtlasWan27TextToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_wan27_i2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.alibaba_wan_2_7_i2v import AtlasWan27ImageToVideo

    assert "atlas_client" in AtlasWan27ImageToVideo.INPUT_TYPES()["required"]
    assert "image" in AtlasWan27ImageToVideo.INPUT_TYPES()["required"]
    assert AtlasWan27ImageToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_wan27_r2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.alibaba_wan_2_7_r2v import AtlasWan27ReferenceToVideo

    assert "atlas_client" in AtlasWan27ReferenceToVideo.INPUT_TYPES()["required"]
    assert "prompt" in AtlasWan27ReferenceToVideo.INPUT_TYPES()["required"]
    assert "images" in AtlasWan27ReferenceToVideo.INPUT_TYPES()["required"]
    assert "videos" in AtlasWan27ReferenceToVideo.INPUT_TYPES()["required"]
    assert AtlasWan27ReferenceToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_wan27_video_edit_node_metadata():
    from src.atlascloud_comfyui.nodes.video.alibaba_wan_2_7_video_edit import AtlasWan27VideoEdit

    assert "atlas_client" in AtlasWan27VideoEdit.INPUT_TYPES()["required"]
    assert "video" in AtlasWan27VideoEdit.INPUT_TYPES()["required"]
    assert AtlasWan27VideoEdit.RETURN_TYPES == ("STRING", "STRING")


# --- Batch Y: API high-priority visual models (2026-04-27) ---

def test_happyhorse_10_t2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.alibaba_happyhorse_1_0_t2v import AtlasHappyHorse10TextToVideo

    assert "atlas_client" in AtlasHappyHorse10TextToVideo.INPUT_TYPES()["required"]
    assert "prompt" in AtlasHappyHorse10TextToVideo.INPUT_TYPES()["required"]
    assert AtlasHappyHorse10TextToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_happyhorse_10_i2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.alibaba_happyhorse_1_0_i2v import AtlasHappyHorse10ImageToVideo

    assert "atlas_client" in AtlasHappyHorse10ImageToVideo.INPUT_TYPES()["required"]
    assert "image" in AtlasHappyHorse10ImageToVideo.INPUT_TYPES()["required"]
    assert AtlasHappyHorse10ImageToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_happyhorse_10_r2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.alibaba_happyhorse_1_0_r2v import AtlasHappyHorse10ReferenceToVideo

    assert "atlas_client" in AtlasHappyHorse10ReferenceToVideo.INPUT_TYPES()["required"]
    assert "prompt" in AtlasHappyHorse10ReferenceToVideo.INPUT_TYPES()["required"]
    assert "images" in AtlasHappyHorse10ReferenceToVideo.INPUT_TYPES()["required"]
    assert AtlasHappyHorse10ReferenceToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_happyhorse_10_video_edit_node_metadata():
    from src.atlascloud_comfyui.nodes.video.alibaba_happyhorse_1_0_video_edit import AtlasHappyHorse10VideoEdit

    assert "atlas_client" in AtlasHappyHorse10VideoEdit.INPUT_TYPES()["required"]
    assert "video" in AtlasHappyHorse10VideoEdit.INPUT_TYPES()["required"]
    assert "prompt" in AtlasHappyHorse10VideoEdit.INPUT_TYPES()["required"]
    assert AtlasHappyHorse10VideoEdit.RETURN_TYPES == ("STRING", "STRING")


def test_veo31_lite_t2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.google_veo31_lite_t2v import AtlasVeo31LiteTextToVideo

    assert "atlas_client" in AtlasVeo31LiteTextToVideo.INPUT_TYPES()["required"]
    assert "prompt" in AtlasVeo31LiteTextToVideo.INPUT_TYPES()["required"]
    assert AtlasVeo31LiteTextToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_veo31_lite_i2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.google_veo31_lite_i2v import AtlasVeo31LiteImageToVideo

    assert "atlas_client" in AtlasVeo31LiteImageToVideo.INPUT_TYPES()["required"]
    assert "prompt" in AtlasVeo31LiteImageToVideo.INPUT_TYPES()["required"]
    assert "image" in AtlasVeo31LiteImageToVideo.INPUT_TYPES()["required"]
    assert AtlasVeo31LiteImageToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_veo31_lite_start_end_frame_node_metadata():
    from src.atlascloud_comfyui.nodes.video.google_veo31_lite_start_end_frame_t2v import AtlasVeo31LiteStartEndFrameToVideo

    assert "atlas_client" in AtlasVeo31LiteStartEndFrameToVideo.INPUT_TYPES()["required"]
    assert "prompt" in AtlasVeo31LiteStartEndFrameToVideo.INPUT_TYPES()["required"]
    assert "image" in AtlasVeo31LiteStartEndFrameToVideo.INPUT_TYPES()["required"]
    assert "last_image" in AtlasVeo31LiteStartEndFrameToVideo.INPUT_TYPES()["required"]
    assert AtlasVeo31LiteStartEndFrameToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_vidu_q3_r2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.vidu_q3_r2v import AtlasViduQ3ReferenceToVideo

    assert "atlas_client" in AtlasViduQ3ReferenceToVideo.INPUT_TYPES()["required"]
    assert "prompt" in AtlasViduQ3ReferenceToVideo.INPUT_TYPES()["required"]
    assert "images" in AtlasViduQ3ReferenceToVideo.INPUT_TYPES()["required"]
    assert AtlasViduQ3ReferenceToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_vidu_q3_mix_r2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.vidu_q3_mix_r2v import AtlasViduQ3MixReferenceToVideo

    assert "atlas_client" in AtlasViduQ3MixReferenceToVideo.INPUT_TYPES()["required"]
    assert "prompt" in AtlasViduQ3MixReferenceToVideo.INPUT_TYPES()["required"]
    assert "images" in AtlasViduQ3MixReferenceToVideo.INPUT_TYPES()["required"]
    assert AtlasViduQ3MixReferenceToVideo.RETURN_TYPES == ("STRING", "STRING")

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

# --- Batch 4: 2026-03-05 sync ---

def test_imagen3_fast_t2i_node_metadata():
    from src.atlascloud_comfyui.nodes.image.imagen3_fast_t2i import AtlasImagen3FastTextToImage

    assert "atlas_client" in AtlasImagen3FastTextToImage.INPUT_TYPES()["required"]
    assert AtlasImagen3FastTextToImage.RETURN_TYPES == ("STRING", "STRING")
    assert "image_url" in AtlasImagen3FastTextToImage.RETURN_NAMES

def test_nano_banana_t2i_node_metadata():
    from src.atlascloud_comfyui.nodes.image.nano_banana_t2i import AtlasNanoBananaTextToImage

    assert "atlas_client" in AtlasNanoBananaTextToImage.INPUT_TYPES()["required"]
    assert AtlasNanoBananaTextToImage.RETURN_TYPES == ("STRING", "STRING")
    assert "image_url" in AtlasNanoBananaTextToImage.RETURN_NAMES

def test_nano_banana_t2i_dev_node_metadata():
    from src.atlascloud_comfyui.nodes.image.nano_banana_t2i_dev import AtlasNanoBananaTextToImageDeveloper

    assert "atlas_client" in AtlasNanoBananaTextToImageDeveloper.INPUT_TYPES()["required"]
    assert AtlasNanoBananaTextToImageDeveloper.RETURN_TYPES == ("STRING", "STRING")

def test_nano_banana_edit_node_metadata():
    from src.atlascloud_comfyui.nodes.image.nano_banana_edit import AtlasNanoBananaEdit

    assert "atlas_client" in AtlasNanoBananaEdit.INPUT_TYPES()["required"]
    assert "images" in AtlasNanoBananaEdit.INPUT_TYPES()["required"]
    assert AtlasNanoBananaEdit.RETURN_TYPES == ("STRING", "STRING")

def test_nano_banana_edit_dev_node_metadata():
    from src.atlascloud_comfyui.nodes.image.nano_banana_edit_dev import AtlasNanoBananaEditDeveloper

    assert "atlas_client" in AtlasNanoBananaEditDeveloper.INPUT_TYPES()["required"]
    assert "images" in AtlasNanoBananaEditDeveloper.INPUT_TYPES()["required"]
    assert AtlasNanoBananaEditDeveloper.RETURN_TYPES == ("STRING", "STRING")

def test_nano_banana_pro_t2i_dev_node_metadata():
    from src.atlascloud_comfyui.nodes.image.nano_banana_pro_t2i_dev import AtlasNanoBananaProTextToImageDeveloper

    assert "atlas_client" in AtlasNanoBananaProTextToImageDeveloper.INPUT_TYPES()["required"]
    assert AtlasNanoBananaProTextToImageDeveloper.RETURN_TYPES == ("STRING", "STRING")

def test_nano_banana_pro_edit_dev_node_metadata():
    from src.atlascloud_comfyui.nodes.image.nano_banana_pro_edit_dev import AtlasNanoBananaProEditDeveloper

    assert "atlas_client" in AtlasNanoBananaProEditDeveloper.INPUT_TYPES()["required"]
    assert "images" in AtlasNanoBananaProEditDeveloper.INPUT_TYPES()["required"]
    assert AtlasNanoBananaProEditDeveloper.RETURN_TYPES == ("STRING", "STRING")

def test_flux_schnell_t2i_node_metadata():
    from src.atlascloud_comfyui.nodes.image.flux_schnell_t2i import AtlasFluxSchnellTextToImage

    assert "atlas_client" in AtlasFluxSchnellTextToImage.INPUT_TYPES()["required"]
    assert AtlasFluxSchnellTextToImage.RETURN_TYPES == ("STRING", "STRING")

def test_flux_kontext_dev_edit_node_metadata():
    from src.atlascloud_comfyui.nodes.image.flux_kontext_dev_edit import AtlasFluxKontextDevEdit

    assert "atlas_client" in AtlasFluxKontextDevEdit.INPUT_TYPES()["required"]
    assert "image" in AtlasFluxKontextDevEdit.INPUT_TYPES()["required"]
    assert AtlasFluxKontextDevEdit.RETURN_TYPES == ("STRING", "STRING")

def test_flux_kontext_dev_lora_edit_node_metadata():
    from src.atlascloud_comfyui.nodes.image.flux_kontext_dev_lora_edit import AtlasFluxKontextDevLoraEdit

    assert "atlas_client" in AtlasFluxKontextDevLoraEdit.INPUT_TYPES()["required"]
    assert "image" in AtlasFluxKontextDevLoraEdit.INPUT_TYPES()["required"]
    assert AtlasFluxKontextDevLoraEdit.RETURN_TYPES == ("STRING", "STRING")

def test_wan25_image_edit_node_metadata():
    from src.atlascloud_comfyui.nodes.image.wan25_image_edit import AtlasWan25ImageEdit

    assert "atlas_client" in AtlasWan25ImageEdit.INPUT_TYPES()["required"]
    assert "images" in AtlasWan25ImageEdit.INPUT_TYPES()["required"]
    assert AtlasWan25ImageEdit.RETURN_TYPES == ("STRING", "STRING")

def test_kling_v16_i2v_standard_node_metadata():
    from src.atlascloud_comfyui.nodes.video.kling_v16_i2v_standard import AtlasKlingV16I2VStandard

    assert "atlas_client" in AtlasKlingV16I2VStandard.INPUT_TYPES()["required"]
    assert "image" in AtlasKlingV16I2VStandard.INPUT_TYPES()["required"]
    assert AtlasKlingV16I2VStandard.RETURN_TYPES == ("STRING", "STRING")

def test_hailuo_02_standard_node_metadata():
    from src.atlascloud_comfyui.nodes.video.hailuo_02_i2v_standard import AtlasHailuo02I2VStandard

    assert "atlas_client" in AtlasHailuo02I2VStandard.INPUT_TYPES()["required"]
    assert "image" in AtlasHailuo02I2VStandard.INPUT_TYPES()["required"]
    assert AtlasHailuo02I2VStandard.RETURN_TYPES == ("STRING", "STRING")

def test_qwen_image_t2i_plus_node_metadata():
    from src.atlascloud_comfyui.nodes.image.qwen_image_t2i_plus import AtlasQwenImageTextToImagePlus

    assert "atlas_client" in AtlasQwenImageTextToImagePlus.INPUT_TYPES()["required"]
    assert AtlasQwenImageTextToImagePlus.RETURN_TYPES == ("STRING", "STRING")
    assert "image_url" in AtlasQwenImageTextToImagePlus.RETURN_NAMES

def test_qwen_image_t2i_max_node_metadata():
    from src.atlascloud_comfyui.nodes.image.qwen_image_t2i_max import AtlasQwenImageTextToImageMax

    assert "atlas_client" in AtlasQwenImageTextToImageMax.INPUT_TYPES()["required"]
    assert AtlasQwenImageTextToImageMax.RETURN_TYPES == ("STRING", "STRING")
    assert "image_url" in AtlasQwenImageTextToImageMax.RETURN_NAMES

def test_seedance_v1_pro_fast_t2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.seedance_v1_pro_fast_t2v import AtlasSeedanceV1ProFastTextToVideo

    assert "atlas_client" in AtlasSeedanceV1ProFastTextToVideo.INPUT_TYPES()["required"]
    assert AtlasSeedanceV1ProFastTextToVideo.RETURN_TYPES == ("STRING", "STRING")
    assert "video_url" in AtlasSeedanceV1ProFastTextToVideo.RETURN_NAMES

def test_seedance_v1_pro_fast_i2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.seedance_v1_pro_fast_i2v import AtlasSeedanceV1ProFastImageToVideo

    assert "atlas_client" in AtlasSeedanceV1ProFastImageToVideo.INPUT_TYPES()["required"]
    assert "image" in AtlasSeedanceV1ProFastImageToVideo.INPUT_TYPES()["required"]
    assert AtlasSeedanceV1ProFastImageToVideo.RETURN_TYPES == ("STRING", "STRING")

def test_wan25_fast_t2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.wan25_fast_t2v import AtlasWAN25TextToVideoFast

    assert "atlas_client" in AtlasWAN25TextToVideoFast.INPUT_TYPES()["required"]
    assert AtlasWAN25TextToVideoFast.RETURN_TYPES == ("STRING", "STRING")

def test_wan25_fast_i2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.wan25_fast_i2v import AtlasWAN25ImageToVideoFast

    assert "atlas_client" in AtlasWAN25ImageToVideoFast.INPUT_TYPES()["required"]
    assert "image" in AtlasWAN25ImageToVideoFast.INPUT_TYPES()["required"]
    assert AtlasWAN25ImageToVideoFast.RETURN_TYPES == ("STRING", "STRING")

def test_van26_t2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.van26_t2v import AtlasVan26TextToVideo

    assert "atlas_client" in AtlasVan26TextToVideo.INPUT_TYPES()["required"]
    assert AtlasVan26TextToVideo.RETURN_TYPES == ("STRING", "STRING")

def test_van26_i2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.van26_i2v import AtlasVan26ImageToVideo

    assert "atlas_client" in AtlasVan26ImageToVideo.INPUT_TYPES()["required"]
    assert "image" in AtlasVan26ImageToVideo.INPUT_TYPES()["required"]
    assert AtlasVan26ImageToVideo.RETURN_TYPES == ("STRING", "STRING")

def test_vidu_reference_to_video_q1_node_metadata():
    from src.atlascloud_comfyui.nodes.video.vidu_reference_to_video_q1 import AtlasViduReferenceToVideoQ1

    assert "atlas_client" in AtlasViduReferenceToVideoQ1.INPUT_TYPES()["required"]
    assert AtlasViduReferenceToVideoQ1.RETURN_TYPES == ("STRING", "STRING")

def test_vidu_reference_to_video_v2_node_metadata():
    from src.atlascloud_comfyui.nodes.video.vidu_reference_to_video_v2 import AtlasViduReferenceToVideoV2

    assert "atlas_client" in AtlasViduReferenceToVideoV2.INPUT_TYPES()["required"]
    assert AtlasViduReferenceToVideoV2.RETURN_TYPES == ("STRING", "STRING")

def test_vidu_start_end_to_video_v2_node_metadata():
    from src.atlascloud_comfyui.nodes.video.vidu_start_end_to_video_v2 import AtlasViduStartEndToVideoV2

    assert "atlas_client" in AtlasViduStartEndToVideoV2.INPUT_TYPES()["required"]
    assert "start_image" in AtlasViduStartEndToVideoV2.INPUT_TYPES()["required"]
    assert "end_image" in AtlasViduStartEndToVideoV2.INPUT_TYPES()["required"]
    assert AtlasViduStartEndToVideoV2.RETURN_TYPES == ("STRING", "STRING")

def test_kling_v20_i2v_master_node_metadata():
    from src.atlascloud_comfyui.nodes.video.kling_v20_i2v_master import AtlasKlingV20I2VMaster

    assert "atlas_client" in AtlasKlingV20I2VMaster.INPUT_TYPES()["required"]
    assert "image" in AtlasKlingV20I2VMaster.INPUT_TYPES()["required"]
    assert AtlasKlingV20I2VMaster.RETURN_TYPES == ("STRING", "STRING")

def test_veo3_fast_i2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.veo3_fast_i2v import AtlasVeo3FastImageToVideo

    assert "atlas_client" in AtlasVeo3FastImageToVideo.INPUT_TYPES()["required"]
    assert "image" in AtlasVeo3FastImageToVideo.INPUT_TYPES()["required"]
    assert AtlasVeo3FastImageToVideo.RETURN_TYPES == ("STRING", "STRING")

def test_kling_v21_t2v_master_node_metadata():
    from src.atlascloud_comfyui.nodes.video.kling_v21_t2v_master import AtlasKlingV21T2VMaster

    assert "atlas_client" in AtlasKlingV21T2VMaster.INPUT_TYPES()["required"]
    assert AtlasKlingV21T2VMaster.RETURN_TYPES == ("STRING", "STRING")

def test_kling_v20_t2v_master_node_metadata():
    from src.atlascloud_comfyui.nodes.video.kling_v20_t2v_master import AtlasKlingV20T2VMaster

    assert "atlas_client" in AtlasKlingV20T2VMaster.INPUT_TYPES()["required"]
    assert AtlasKlingV20T2VMaster.RETURN_TYPES == ("STRING", "STRING")

# --- 2026-03-19: Sync NEW models from /api/v1/models ---

def test_nano_banana_pro_edit_ultra_node_metadata():
    from src.atlascloud_comfyui.nodes.image.nano_banana_pro_edit_ultra import AtlasNanoBananaProEditUltra

    assert "atlas_client" in AtlasNanoBananaProEditUltra.INPUT_TYPES()["required"]
    assert "images" in AtlasNanoBananaProEditUltra.INPUT_TYPES()["required"]
    assert "prompt" in AtlasNanoBananaProEditUltra.INPUT_TYPES()["required"]
    assert AtlasNanoBananaProEditUltra.RETURN_TYPES == ("STRING", "STRING")

def test_vidu_q2_pro_fast_reference_to_video_node_metadata():
    from src.atlascloud_comfyui.nodes.video.vidu_q2_pro_fast_reference_to_video import AtlasViduQ2ProFastReferenceToVideo

    assert "atlas_client" in AtlasViduQ2ProFastReferenceToVideo.INPUT_TYPES()["required"]
    assert "images" in AtlasViduQ2ProFastReferenceToVideo.INPUT_TYPES()["required"]
    assert "prompt" in AtlasViduQ2ProFastReferenceToVideo.INPUT_TYPES()["required"]
    assert AtlasViduQ2ProFastReferenceToVideo.RETURN_TYPES == ("STRING", "STRING")

def test_vidu_q2_pro_fast_reference_to_video_with_audio_node_metadata():
    from src.atlascloud_comfyui.nodes.video.vidu_q2_pro_fast_reference_to_video_with_audio import (
        AtlasViduQ2ProFastReferenceToVideoWithAudio,
    )

    assert "atlas_client" in AtlasViduQ2ProFastReferenceToVideoWithAudio.INPUT_TYPES()["required"]
    assert "images" in AtlasViduQ2ProFastReferenceToVideoWithAudio.INPUT_TYPES()["required"]
    assert "prompt" in AtlasViduQ2ProFastReferenceToVideoWithAudio.INPUT_TYPES()["required"]
    assert AtlasViduQ2ProFastReferenceToVideoWithAudio.RETURN_TYPES == ("STRING", "STRING")

# --- Batch 2026-03-30: GPT Image + Qwen Image 2.0 ---

def test_openai_gpt_image_1_t2i_node_metadata():
    from src.atlascloud_comfyui.nodes.image.openai_gpt_image_1_t2i import AtlasOpenAIGPTImage1TextToImage

    assert "atlas_client" in AtlasOpenAIGPTImage1TextToImage.INPUT_TYPES()["required"]
    assert AtlasOpenAIGPTImage1TextToImage.RETURN_TYPES == ("STRING", "STRING")
    assert "image_url" in AtlasOpenAIGPTImage1TextToImage.RETURN_NAMES

def test_openai_gpt_image_1_edit_node_metadata():
    from src.atlascloud_comfyui.nodes.image.openai_gpt_image_1_edit import AtlasOpenAIGPTImage1Edit

    assert "atlas_client" in AtlasOpenAIGPTImage1Edit.INPUT_TYPES()["required"]
    assert "images" in AtlasOpenAIGPTImage1Edit.INPUT_TYPES()["required"]
    assert AtlasOpenAIGPTImage1Edit.RETURN_TYPES == ("STRING", "STRING")

def test_openai_gpt_image_1_mini_t2i_node_metadata():
    from src.atlascloud_comfyui.nodes.image.openai_gpt_image_1_mini_t2i import AtlasOpenAIGPTImage1MiniTextToImage

    assert "atlas_client" in AtlasOpenAIGPTImage1MiniTextToImage.INPUT_TYPES()["required"]
    assert AtlasOpenAIGPTImage1MiniTextToImage.RETURN_TYPES == ("STRING", "STRING")

def test_openai_gpt_image_1_mini_edit_node_metadata():
    from src.atlascloud_comfyui.nodes.image.openai_gpt_image_1_mini_edit import AtlasOpenAIGPTImage1MiniEdit

    assert "atlas_client" in AtlasOpenAIGPTImage1MiniEdit.INPUT_TYPES()["required"]
    assert "images" in AtlasOpenAIGPTImage1MiniEdit.INPUT_TYPES()["required"]
    assert AtlasOpenAIGPTImage1MiniEdit.RETURN_TYPES == ("STRING", "STRING")

def test_openai_gpt_image_15_t2i_node_metadata():
    from src.atlascloud_comfyui.nodes.image.openai_gpt_image_15_t2i import AtlasOpenAIGPTImage15TextToImage

    assert "atlas_client" in AtlasOpenAIGPTImage15TextToImage.INPUT_TYPES()["required"]
    assert AtlasOpenAIGPTImage15TextToImage.RETURN_TYPES == ("STRING", "STRING")

def test_openai_gpt_image_15_edit_node_metadata():
    from src.atlascloud_comfyui.nodes.image.openai_gpt_image_15_edit import AtlasOpenAIGPTImage15Edit

    assert "atlas_client" in AtlasOpenAIGPTImage15Edit.INPUT_TYPES()["required"]
    assert "images" in AtlasOpenAIGPTImage15Edit.INPUT_TYPES()["required"]
    assert AtlasOpenAIGPTImage15Edit.RETURN_TYPES == ("STRING", "STRING")

def test_qwen_image_20_t2i_node_metadata():
    from src.atlascloud_comfyui.nodes.image.qwen_image_20_t2i import AtlasQwenImage20TextToImage

    assert "atlas_client" in AtlasQwenImage20TextToImage.INPUT_TYPES()["required"]
    assert AtlasQwenImage20TextToImage.RETURN_TYPES == ("STRING", "STRING")

def test_qwen_image_20_edit_node_metadata():
    from src.atlascloud_comfyui.nodes.image.qwen_image_20_edit import AtlasQwenImage20Edit

    assert "atlas_client" in AtlasQwenImage20Edit.INPUT_TYPES()["required"]
    assert "images" in AtlasQwenImage20Edit.INPUT_TYPES()["required"]
    assert AtlasQwenImage20Edit.RETURN_TYPES == ("STRING", "STRING")

def test_qwen_image_20_pro_t2i_node_metadata():
    from src.atlascloud_comfyui.nodes.image.qwen_image_20_pro_t2i import AtlasQwenImage20ProTextToImage

    assert "atlas_client" in AtlasQwenImage20ProTextToImage.INPUT_TYPES()["required"]
    assert AtlasQwenImage20ProTextToImage.RETURN_TYPES == ("STRING", "STRING")

def test_qwen_image_20_pro_edit_node_metadata():
    from src.atlascloud_comfyui.nodes.image.qwen_image_20_pro_edit import AtlasQwenImage20ProEdit

    assert "atlas_client" in AtlasQwenImage20ProEdit.INPUT_TYPES()["required"]
    assert "images" in AtlasQwenImage20ProEdit.INPUT_TYPES()["required"]
    assert AtlasQwenImage20ProEdit.RETURN_TYPES == ("STRING", "STRING")
