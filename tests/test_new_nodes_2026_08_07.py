"""Metadata-only tests for newly added nodes (2026-08-07).

New models: Seedance 2.5 (text-to-video, image-to-video, reference-to-video) and
Seedream V5.0 Pro Layer Decomposition.
These tests MUST NOT require ATLASCLOUD_API_KEY.
"""

import inspect

import pytest

_DURATIONS = [-1, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]


def _seedance_25_common_assertions(cls):
    inputs = cls.INPUT_TYPES()
    optional = inputs["optional"]
    assert "atlas_client" in inputs["required"]
    assert optional["duration"][0] == _DURATIONS
    assert optional["duration"][1]["default"] == 5
    assert optional["resolution"][0] == ["480p", "720p"]
    assert optional["resolution"][1]["default"] == "720p"
    assert optional["generate_audio"][0] == "BOOLEAN"
    assert optional["generate_audio"][1]["default"] is True
    assert optional["output_format"][0] == ["mp4", "mov"]
    assert optional["output_format"][1]["default"] == "mp4"
    assert cls.RETURN_TYPES == ("STRING", "STRING")
    assert cls.RETURN_NAMES == ("video_url", "prediction_id")
    assert cls.CATEGORY == "AtlasCloud/Video"


def test_seedance_25_t2v_metadata():
    from src.atlascloud_comfyui.nodes.video.bytedance_seedance_2_5_t2v import (
        AtlasSeedance25TextToVideo,
    )

    _seedance_25_common_assertions(AtlasSeedance25TextToVideo)
    inputs = AtlasSeedance25TextToVideo.INPUT_TYPES()
    assert "prompt" in inputs["required"]
    assert inputs["optional"]["ratio"][0] == ["16:9", "4:3", "1:1", "3:4", "9:16", "21:9", "adaptive"]


@pytest.mark.parametrize("bad_prompt", ["", "   "])
def test_seedance_25_t2v_requires_prompt(bad_prompt):
    from src.atlascloud_comfyui.nodes.video.bytedance_seedance_2_5_t2v import (
        AtlasSeedance25TextToVideo,
    )

    with pytest.raises(RuntimeError, match="prompt is required"):
        AtlasSeedance25TextToVideo().run(None, bad_prompt)


def test_seedance_25_i2v_metadata():
    from src.atlascloud_comfyui.nodes.video.bytedance_seedance_2_5_i2v import (
        AtlasSeedance25ImageToVideo,
    )

    _seedance_25_common_assertions(AtlasSeedance25ImageToVideo)
    inputs = AtlasSeedance25ImageToVideo.INPUT_TYPES()
    assert "image" in inputs["required"]
    assert "prompt" in inputs["optional"]
    assert "last_image" in inputs["optional"]
    # The API only accepts "adaptive" for image-to-video.
    assert inputs["optional"]["ratio"][0] == ["adaptive"]


@pytest.mark.parametrize("bad_image", ["", "  "])
def test_seedance_25_i2v_requires_image(bad_image):
    from src.atlascloud_comfyui.nodes.video.bytedance_seedance_2_5_i2v import (
        AtlasSeedance25ImageToVideo,
    )

    with pytest.raises(RuntimeError, match="image is required"):
        AtlasSeedance25ImageToVideo().run(None, bad_image)


def test_seedance_25_r2v_metadata():
    from src.atlascloud_comfyui.nodes.video.bytedance_seedance_2_5_r2v import (
        AtlasSeedance25ReferenceToVideo,
    )

    _seedance_25_common_assertions(AtlasSeedance25ReferenceToVideo)
    inputs = AtlasSeedance25ReferenceToVideo.INPUT_TYPES()
    assert "reference_images" in inputs["required"]
    assert "reference_videos" in inputs["required"]
    assert "reference_audios" in inputs["optional"]


@pytest.mark.parametrize("images,videos", [("", ""), ("   ", "\n  \n")])
def test_seedance_25_r2v_requires_a_reference(images, videos):
    from src.atlascloud_comfyui.nodes.video.bytedance_seedance_2_5_r2v import (
        AtlasSeedance25ReferenceToVideo,
    )

    with pytest.raises(RuntimeError, match="at least one reference image or reference video"):
        AtlasSeedance25ReferenceToVideo().run(None, images, videos)


def test_seedream_v50_pro_layer_decomposition_metadata():
    from src.atlascloud_comfyui.nodes.image.seedream_v50_pro_layer_decomposition import (
        AtlasSeedreamV50ProLayerDecomposition,
    )

    cls = AtlasSeedreamV50ProLayerDecomposition
    inputs = cls.INPUT_TYPES()
    required = inputs["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert required["size"][0] == ["auto", "1K", "1.5K", "2K"]
    assert required["size"][1]["default"] == "auto"
    assert required["output_format"][0] == ["jpeg", "png"]
    assert required["output_format"][1]["default"] == "jpeg"
    assert required["enable_base64_output"][0] == "BOOLEAN"
    assert "prompt" in inputs["optional"]
    assert cls.RETURN_TYPES == ("STRING", "STRING", "STRING")
    assert cls.RETURN_NAMES == ("image_url", "layer_urls", "prediction_id")
    assert cls.CATEGORY == "AtlasCloud/Image"


@pytest.mark.parametrize("bad_image", ["", "  "])
def test_seedream_v50_pro_layer_decomposition_requires_image(bad_image):
    from src.atlascloud_comfyui.nodes.image.seedream_v50_pro_layer_decomposition import (
        AtlasSeedreamV50ProLayerDecomposition,
    )

    with pytest.raises(RuntimeError, match="image is required"):
        AtlasSeedreamV50ProLayerDecomposition().run(None, bad_image, "auto", "jpeg", False)


def test_new_nodes_2026_08_07_registered():
    from src.atlascloud_comfyui.registry import (
        NODE_CLASS_MAPPINGS,
        NODE_DISPLAY_NAME_MAPPINGS,
    )

    keys = [
        "AtlasCloud Seedance 2.5 Text-to-Video",
        "AtlasCloud Seedance 2.5 Image-to-Video",
        "AtlasCloud Seedance 2.5 Reference-to-Video",
        "AtlasCloud Seedream V5.0 Pro Layer Decomposition",
    ]
    for key in keys:
        assert key in NODE_CLASS_MAPPINGS
        assert key in NODE_DISPLAY_NAME_MAPPINGS


def test_new_nodes_2026_08_07_model_ids():
    from src.atlascloud_comfyui.nodes.image.seedream_v50_pro_layer_decomposition import (
        AtlasSeedreamV50ProLayerDecomposition,
    )
    from src.atlascloud_comfyui.nodes.video.bytedance_seedance_2_5_i2v import (
        AtlasSeedance25ImageToVideo,
    )
    from src.atlascloud_comfyui.nodes.video.bytedance_seedance_2_5_r2v import (
        AtlasSeedance25ReferenceToVideo,
    )
    from src.atlascloud_comfyui.nodes.video.bytedance_seedance_2_5_t2v import (
        AtlasSeedance25TextToVideo,
    )

    expected = [
        (AtlasSeedance25TextToVideo, "bytedance/seedance-2.5/text-to-video"),
        (AtlasSeedance25ImageToVideo, "bytedance/seedance-2.5/image-to-video"),
        (AtlasSeedance25ReferenceToVideo, "bytedance/seedance-2.5/reference-to-video"),
        (
            AtlasSeedreamV50ProLayerDecomposition,
            "bytedance/seedream-v5.0-pro/layer-decomposition",
        ),
    ]
    for cls, model_id in expected:
        source = inspect.getsource(cls.run)
        assert f'"model": "{model_id}"' in source
