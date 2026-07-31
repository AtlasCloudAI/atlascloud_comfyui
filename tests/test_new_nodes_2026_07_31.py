"""Metadata-only tests for newly added nodes (2026-07-31).

New models: MiniMax H3 (T2V / I2V / R2V), Tencent Image Upscaler,
Tencent Video Upscaler, BytePlus Video Upscaler.
These tests MUST NOT require ATLASCLOUD_API_KEY.
"""

import inspect

import pytest


def test_minimax_h3_t2v_metadata():
    from src.atlascloud_comfyui.nodes.video.minimax_h3_t2v import AtlasMinimaxH3TextToVideo

    inputs = AtlasMinimaxH3TextToVideo.INPUT_TYPES()
    required = inputs["required"]
    optional = inputs["optional"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert optional["resolution"][0] == ["2K"]
    assert optional["ratio"][0] == ["21:9", "16:9", "4:3", "1:1", "3:4", "9:16"]
    assert optional["ratio"][1]["default"] == "1:1"
    assert optional["duration"][1]["min"] == 5
    assert optional["duration"][1]["max"] == 15
    assert AtlasMinimaxH3TextToVideo.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasMinimaxH3TextToVideo.RETURN_NAMES == ("video_url", "prediction_id")
    assert AtlasMinimaxH3TextToVideo.CATEGORY == "AtlasCloud/Video"


def test_minimax_h3_t2v_requires_prompt():
    from src.atlascloud_comfyui.nodes.video.minimax_h3_t2v import AtlasMinimaxH3TextToVideo

    with pytest.raises(RuntimeError, match="prompt is required"):
        AtlasMinimaxH3TextToVideo().run(None, "   ")


def test_minimax_h3_i2v_metadata():
    from src.atlascloud_comfyui.nodes.video.minimax_h3_i2v import AtlasMinimaxH3ImageToVideo

    inputs = AtlasMinimaxH3ImageToVideo.INPUT_TYPES()
    required = inputs["required"]
    optional = inputs["optional"]
    assert "image" in required
    assert "prompt" in required
    assert "end_image" in optional
    assert optional["ratio"][0] == ["adaptive", "21:9", "16:9", "4:3", "1:1", "3:4", "9:16"]
    assert optional["ratio"][1]["default"] == "adaptive"
    assert AtlasMinimaxH3ImageToVideo.RETURN_NAMES == ("video_url", "prediction_id")


@pytest.mark.parametrize("bad_image", ["", "   "])
def test_minimax_h3_i2v_requires_image(bad_image):
    from src.atlascloud_comfyui.nodes.video.minimax_h3_i2v import AtlasMinimaxH3ImageToVideo

    with pytest.raises(RuntimeError, match="image is required"):
        AtlasMinimaxH3ImageToVideo().run(None, bad_image, "a prompt")


def test_minimax_h3_i2v_requires_prompt():
    from src.atlascloud_comfyui.nodes.video.minimax_h3_i2v import AtlasMinimaxH3ImageToVideo

    with pytest.raises(RuntimeError, match="prompt is required"):
        AtlasMinimaxH3ImageToVideo().run(None, "https://example.com/a.png", "  ")


def test_minimax_h3_r2v_metadata():
    from src.atlascloud_comfyui.nodes.video.minimax_h3_r2v import AtlasMinimaxH3ReferenceToVideo

    inputs = AtlasMinimaxH3ReferenceToVideo.INPUT_TYPES()
    assert "refers" in inputs["required"]
    assert "prompt" in inputs["required"]
    assert inputs["optional"]["duration"][1]["default"] == 8
    assert AtlasMinimaxH3ReferenceToVideo.CATEGORY == "AtlasCloud/Video"


@pytest.mark.parametrize("bad_refers", ["", "  \n \n"])
def test_minimax_h3_r2v_requires_refers(bad_refers):
    from src.atlascloud_comfyui.nodes.video.minimax_h3_r2v import AtlasMinimaxH3ReferenceToVideo

    with pytest.raises(RuntimeError, match="refers is required"):
        AtlasMinimaxH3ReferenceToVideo().run(None, bad_refers, "a prompt")


def test_minimax_h3_r2v_wraps_refers_as_objects():
    from src.atlascloud_comfyui.nodes.video.minimax_h3_r2v import AtlasMinimaxH3ReferenceToVideo

    source = inspect.getsource(AtlasMinimaxH3ReferenceToVideo.run)
    assert '"refers": [{"url": u} for u in urls]' in source


def test_tencent_image_upscaler_metadata():
    from src.atlascloud_comfyui.nodes.image.tencent_image_upscaler import AtlasTencentImageUpscaler

    inputs = AtlasTencentImageUpscaler.INPUT_TYPES()
    optional = inputs["optional"]
    assert "image_url" in inputs["required"]
    assert optional["type"][0] == ["standard", "super", "ultra", "fidelity"]
    assert optional["mode"][0] == ["percent", "aspect", "fixed"]
    assert optional["encode_format"][0] == ["JPEG", "PNG", "WEBP", "BMP"]
    assert AtlasTencentImageUpscaler.CATEGORY == "AtlasCloud/Image"
    assert AtlasTencentImageUpscaler.RETURN_NAMES == ("image_url", "prediction_id")


def test_tencent_image_upscaler_requires_image_url():
    from src.atlascloud_comfyui.nodes.image.tencent_image_upscaler import AtlasTencentImageUpscaler

    with pytest.raises(RuntimeError, match="image_url is required"):
        AtlasTencentImageUpscaler().run(None, "  ")


def test_tencent_video_upscaler_metadata():
    from src.atlascloud_comfyui.nodes.video.tencent_video_upscaler import (
        TEMPLATES,
        AtlasTencentVideoUpscaler,
    )

    inputs = AtlasTencentVideoUpscaler.INPUT_TYPES()
    optional = inputs["optional"]
    assert "video_url" in inputs["required"]
    assert optional["template"][0] == TEMPLATES
    assert optional["template"][1]["default"] == "anime-enhance-4k"
    assert len(TEMPLATES) == 24
    assert optional["keep_metadata"][1]["default"] is True


def test_tencent_video_upscaler_requires_video_url():
    from src.atlascloud_comfyui.nodes.video.tencent_video_upscaler import AtlasTencentVideoUpscaler

    with pytest.raises(RuntimeError, match="video_url is required"):
        AtlasTencentVideoUpscaler().run(None, "")


def test_byteplus_video_upscaler_metadata():
    from src.atlascloud_comfyui.nodes.video.byteplus_video_upscaler import AtlasBytePlusVideoUpscaler

    inputs = AtlasBytePlusVideoUpscaler.INPUT_TYPES()
    optional = inputs["optional"]
    assert "video_url" in inputs["required"]
    assert optional["tool_version"][0] == ["standard", "professional"]
    assert optional["scene"][0] == ["common", "ugc", "short_series", "aigc", "old_film"]
    assert optional["resolution"][0] == ["240p", "360p", "480p", "540p", "720p", "1080p", "2k", "4k", "8k"]
    assert optional["bitrate_level"][0] == ["low", "medium", "high"]
    assert optional["bit_depth"][0] == [8, 10, 12]


def test_byteplus_video_upscaler_requires_video_url():
    from src.atlascloud_comfyui.nodes.video.byteplus_video_upscaler import AtlasBytePlusVideoUpscaler

    with pytest.raises(RuntimeError, match="video_url is required"):
        AtlasBytePlusVideoUpscaler().run(None, "   ")


def test_new_nodes_2026_07_31_registered():
    from src.atlascloud_comfyui.registry import (
        NODE_CLASS_MAPPINGS,
        NODE_DISPLAY_NAME_MAPPINGS,
    )

    keys = [
        "AtlasCloud MiniMax H3 Text-to-Video",
        "AtlasCloud MiniMax H3 Image-to-Video",
        "AtlasCloud MiniMax H3 Reference-to-Video",
        "AtlasCloud Tencent Image Upscaler",
        "AtlasCloud Tencent Video Upscaler",
        "AtlasCloud BytePlus Video Upscaler",
    ]
    for key in keys:
        assert key in NODE_CLASS_MAPPINGS
        assert key in NODE_DISPLAY_NAME_MAPPINGS


def test_new_nodes_2026_07_31_model_ids():
    from src.atlascloud_comfyui.nodes.image.tencent_image_upscaler import AtlasTencentImageUpscaler
    from src.atlascloud_comfyui.nodes.video.byteplus_video_upscaler import AtlasBytePlusVideoUpscaler
    from src.atlascloud_comfyui.nodes.video.minimax_h3_i2v import AtlasMinimaxH3ImageToVideo
    from src.atlascloud_comfyui.nodes.video.minimax_h3_r2v import AtlasMinimaxH3ReferenceToVideo
    from src.atlascloud_comfyui.nodes.video.minimax_h3_t2v import AtlasMinimaxH3TextToVideo
    from src.atlascloud_comfyui.nodes.video.tencent_video_upscaler import AtlasTencentVideoUpscaler

    expected = [
        (AtlasMinimaxH3TextToVideo, "minimax/h3/text-to-video"),
        (AtlasMinimaxH3ImageToVideo, "minimax/h3/image-to-video"),
        (AtlasMinimaxH3ReferenceToVideo, "minimax/h3/reference-to-video"),
        (AtlasTencentImageUpscaler, "tencent/image/upscaler"),
        (AtlasTencentVideoUpscaler, "tencent/video/upscaler"),
        (AtlasBytePlusVideoUpscaler, "byteplus/video/upscaler"),
    ]
    for cls, model_id in expected:
        source = inspect.getsource(cls.run)
        assert f'"model": "{model_id}"' in source
