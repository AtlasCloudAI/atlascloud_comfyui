"""Metadata-only tests for nodes added in the 2026-03-03 sync.

These tests MUST NOT require ATLASCLOUD_API_KEY.
They only validate node metadata (INPUT_TYPES / RETURN_TYPES) so CI can run safely.
"""

from __future__ import annotations


def test_vidu_q3_t2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.vidu_q3_t2v import AtlasViduQ3TextToVideo

    assert "atlas_client" in AtlasViduQ3TextToVideo.INPUT_TYPES()["required"]
    assert "prompt" in AtlasViduQ3TextToVideo.INPUT_TYPES()["required"]
    assert AtlasViduQ3TextToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_vidu_q3_i2v_v2_node_metadata():
    from src.atlascloud_comfyui.nodes.video.vidu_q3_i2v_v2 import AtlasViduQ3ImageToVideoV2

    assert "atlas_client" in AtlasViduQ3ImageToVideoV2.INPUT_TYPES()["required"]
    assert "image" in AtlasViduQ3ImageToVideoV2.INPUT_TYPES()["required"]
    assert AtlasViduQ3ImageToVideoV2.RETURN_TYPES == ("STRING", "STRING")


def test_veo31_fast_t2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.google_veo31_fast_t2v import AtlasVeo31FastTextToVideo

    assert "atlas_client" in AtlasVeo31FastTextToVideo.INPUT_TYPES()["required"]
    assert "prompt" in AtlasVeo31FastTextToVideo.INPUT_TYPES()["required"]
    assert AtlasVeo31FastTextToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_veo31_fast_i2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.google_veo31_fast_i2v import AtlasVeo31FastImageToVideo

    assert "atlas_client" in AtlasVeo31FastImageToVideo.INPUT_TYPES()["required"]
    assert "prompt" in AtlasVeo31FastImageToVideo.INPUT_TYPES()["required"]
    assert "image" in AtlasVeo31FastImageToVideo.INPUT_TYPES()["required"]
    assert AtlasVeo31FastImageToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_veo31_reference_to_video_node_metadata():
    from src.atlascloud_comfyui.nodes.video.google_veo31_r2v import AtlasVeo31ReferenceToVideo

    assert "atlas_client" in AtlasVeo31ReferenceToVideo.INPUT_TYPES()["required"]
    assert "prompt" in AtlasVeo31ReferenceToVideo.INPUT_TYPES()["required"]
    assert "images" in AtlasVeo31ReferenceToVideo.INPUT_TYPES()["required"]
    assert AtlasVeo31ReferenceToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_seedream_v50_lite_sequential_t2i_node_metadata():
    from src.atlascloud_comfyui.nodes.image.seedream_v50_lite_sequential_t2i import AtlasSeedreamV50LiteSequentialTextToImage

    assert "atlas_client" in AtlasSeedreamV50LiteSequentialTextToImage.INPUT_TYPES()["required"]
    assert "prompt" in AtlasSeedreamV50LiteSequentialTextToImage.INPUT_TYPES()["required"]
    assert AtlasSeedreamV50LiteSequentialTextToImage.RETURN_TYPES == ("STRING", "STRING")


def test_seedream_v50_lite_edit_sequential_node_metadata():
    from src.atlascloud_comfyui.nodes.image.seedream_v50_lite_edit_sequential import AtlasSeedreamV50LiteEditSequential

    assert "atlas_client" in AtlasSeedreamV50LiteEditSequential.INPUT_TYPES()["required"]
    assert "prompt" in AtlasSeedreamV50LiteEditSequential.INPUT_TYPES()["required"]
    assert "images" in AtlasSeedreamV50LiteEditSequential.INPUT_TYPES()["required"]
    assert AtlasSeedreamV50LiteEditSequential.RETURN_TYPES == ("STRING", "STRING")


def test_wan26_image_to_video_node_metadata():
    from src.atlascloud_comfyui.nodes.video.wan26_i2v import AtlasWAN26ImageToVideo

    assert "atlas_client" in AtlasWAN26ImageToVideo.INPUT_TYPES()["required"]
    assert "image" in AtlasWAN26ImageToVideo.INPUT_TYPES()["required"]
    assert "prompt" in AtlasWAN26ImageToVideo.INPUT_TYPES()["required"]
    assert "resolution" in AtlasWAN26ImageToVideo.INPUT_TYPES()["required"]
    assert AtlasWAN26ImageToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_wan26_image_edit_node_metadata():
    from src.atlascloud_comfyui.nodes.image.wan26_image_edit import AtlasWAN26ImageEdit

    assert "atlas_client" in AtlasWAN26ImageEdit.INPUT_TYPES()["required"]
    assert "images" in AtlasWAN26ImageEdit.INPUT_TYPES()["required"]
    assert "prompt" in AtlasWAN26ImageEdit.INPUT_TYPES()["required"]
    assert AtlasWAN26ImageEdit.RETURN_TYPES == ("STRING", "STRING")


def test_qwen_image_edit_plus_20251215_node_metadata():
    from src.atlascloud_comfyui.nodes.image.qwen_image_edit_plus_20251215 import AtlasQwenImageEditPlus20251215

    assert "atlas_client" in AtlasQwenImageEditPlus20251215.INPUT_TYPES()["required"]
    assert "images" in AtlasQwenImageEditPlus20251215.INPUT_TYPES()["required"]
    assert "prompt" in AtlasQwenImageEditPlus20251215.INPUT_TYPES()["required"]
    assert AtlasQwenImageEditPlus20251215.RETURN_TYPES == ("STRING", "STRING")
