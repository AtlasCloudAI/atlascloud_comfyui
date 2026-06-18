"""Metadata-only tests for newly added nodes (2026-06-18).

Kling V3.0 Turbo (text/image-to-video).
These tests MUST NOT require ATLASCLOUD_API_KEY.
"""


def test_kling_v30_turbo_t2v_metadata():
    from src.atlascloud_comfyui.nodes.video.kling_v30_turbo_t2v import (
        AtlasKlingV30TurboTextToVideo,
    )

    required = AtlasKlingV30TurboTextToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert AtlasKlingV30TurboTextToVideo.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasKlingV30TurboTextToVideo.CATEGORY == "AtlasCloud/Video"


def test_kling_v30_turbo_i2v_metadata():
    from src.atlascloud_comfyui.nodes.video.kling_v30_turbo_i2v import (
        AtlasKlingV30TurboImageToVideo,
    )

    required = AtlasKlingV30TurboImageToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert AtlasKlingV30TurboImageToVideo.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasKlingV30TurboImageToVideo.CATEGORY == "AtlasCloud/Video"


def test_new_nodes_2026_06_18_registered():
    from src.atlascloud_comfyui.registry import (
        NODE_CLASS_MAPPINGS,
        NODE_DISPLAY_NAME_MAPPINGS,
    )

    for key in (
        "AtlasCloud Kling V3.0 Turbo Image-to-Video",
        "AtlasCloud Kling V3.0 Turbo Text-to-Video",
    ):
        assert key in NODE_CLASS_MAPPINGS
        assert key in NODE_DISPLAY_NAME_MAPPINGS


def test_new_nodes_2026_06_18_model_ids():
    import inspect

    from src.atlascloud_comfyui.nodes.video.kling_v30_turbo_i2v import AtlasKlingV30TurboImageToVideo
    from src.atlascloud_comfyui.nodes.video.kling_v30_turbo_t2v import AtlasKlingV30TurboTextToVideo

    expected = {
        AtlasKlingV30TurboImageToVideo: "kwaivgi/kling-v3.0-turbo/image-to-video",
        AtlasKlingV30TurboTextToVideo: "kwaivgi/kling-v3.0-turbo/text-to-video",
    }
    for cls, model_id in expected.items():
        assert model_id in inspect.getsource(cls.run)
