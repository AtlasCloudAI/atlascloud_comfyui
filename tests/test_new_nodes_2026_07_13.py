"""Metadata-only tests for newly added nodes (2026-07-13).

LTX 2.3 Quality (text-to-video, image-to-video, extend-video).
These tests MUST NOT require ATLASCLOUD_API_KEY.
"""


def test_ltx_23_quality_t2v_metadata():
    from src.atlascloud_comfyui.nodes.video.ltx_2_3_quality_t2v import (
        AtlasLtx23QualityTextToVideo,
    )

    required = AtlasLtx23QualityTextToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert AtlasLtx23QualityTextToVideo.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasLtx23QualityTextToVideo.CATEGORY == "AtlasCloud/Video"


def test_ltx_23_quality_i2v_metadata():
    from src.atlascloud_comfyui.nodes.video.ltx_2_3_quality_i2v import (
        AtlasLtx23QualityImageToVideo,
    )

    required = AtlasLtx23QualityImageToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert "image_url" in required
    assert AtlasLtx23QualityImageToVideo.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasLtx23QualityImageToVideo.CATEGORY == "AtlasCloud/Video"


def test_ltx_23_quality_extend_video_metadata():
    from src.atlascloud_comfyui.nodes.video.ltx_2_3_quality_extend_video import (
        AtlasLtx23QualityExtendVideo,
    )

    required = AtlasLtx23QualityExtendVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert "video_url" in required
    assert AtlasLtx23QualityExtendVideo.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasLtx23QualityExtendVideo.CATEGORY == "AtlasCloud/Video"


def test_new_nodes_2026_07_13_registered():
    from src.atlascloud_comfyui.registry import (
        NODE_CLASS_MAPPINGS,
        NODE_DISPLAY_NAME_MAPPINGS,
    )

    for key in (
        "AtlasCloud LTX 2.3 Quality Text-to-Video",
        "AtlasCloud LTX 2.3 Quality Image-to-Video",
        "AtlasCloud LTX 2.3 Quality Extend Video",
    ):
        assert key in NODE_CLASS_MAPPINGS
        assert key in NODE_DISPLAY_NAME_MAPPINGS


def test_new_nodes_2026_07_13_model_ids():
    import inspect

    from src.atlascloud_comfyui.nodes.video.ltx_2_3_quality_t2v import AtlasLtx23QualityTextToVideo
    from src.atlascloud_comfyui.nodes.video.ltx_2_3_quality_i2v import AtlasLtx23QualityImageToVideo
    from src.atlascloud_comfyui.nodes.video.ltx_2_3_quality_extend_video import AtlasLtx23QualityExtendVideo

    expected = {
        AtlasLtx23QualityTextToVideo: "ltx-2.3-quality/text-to-video",
        AtlasLtx23QualityImageToVideo: "ltx-2.3-quality/image-to-video",
        AtlasLtx23QualityExtendVideo: "ltx-2.3-quality/extend-video",
    }
    for cls, model_id in expected.items():
        src = inspect.getsource(cls.run)
        assert f'"model": "{model_id}"' in src
