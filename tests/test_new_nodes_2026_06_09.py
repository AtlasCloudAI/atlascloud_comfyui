"""Metadata-only tests for newly added nodes (2026-06-09).

PixVerse C1 / V6 video families (text/image/reference to video).
These tests MUST NOT require ATLASCLOUD_API_KEY.
"""


def test_pixverse_c1_t2v_metadata():
    from src.atlascloud_comfyui.nodes.video.pixverse_c1_t2v import (
        AtlasPixVerseC1TextToVideo,
    )

    required = AtlasPixVerseC1TextToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert AtlasPixVerseC1TextToVideo.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasPixVerseC1TextToVideo.CATEGORY == "AtlasCloud/Video"


def test_pixverse_c1_i2v_metadata():
    from src.atlascloud_comfyui.nodes.video.pixverse_c1_i2v import (
        AtlasPixVerseC1ImageToVideo,
    )

    required = AtlasPixVerseC1ImageToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert "prompt" in required
    assert AtlasPixVerseC1ImageToVideo.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasPixVerseC1ImageToVideo.CATEGORY == "AtlasCloud/Video"


def test_pixverse_c1_r2v_metadata():
    from src.atlascloud_comfyui.nodes.video.pixverse_c1_r2v import (
        AtlasPixVerseC1ReferenceToVideo,
    )

    required = AtlasPixVerseC1ReferenceToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "images" in required
    assert "prompt" in required
    assert AtlasPixVerseC1ReferenceToVideo.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasPixVerseC1ReferenceToVideo.CATEGORY == "AtlasCloud/Video"


def test_pixverse_v6_t2v_metadata():
    from src.atlascloud_comfyui.nodes.video.pixverse_v6_t2v import (
        AtlasPixVerseV6TextToVideo,
    )

    required = AtlasPixVerseV6TextToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert AtlasPixVerseV6TextToVideo.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasPixVerseV6TextToVideo.CATEGORY == "AtlasCloud/Video"


def test_pixverse_v6_i2v_metadata():
    from src.atlascloud_comfyui.nodes.video.pixverse_v6_i2v import (
        AtlasPixVerseV6ImageToVideo,
    )

    required = AtlasPixVerseV6ImageToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert "prompt" in required
    assert AtlasPixVerseV6ImageToVideo.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasPixVerseV6ImageToVideo.CATEGORY == "AtlasCloud/Video"


def test_pixverse_v6_r2v_metadata():
    from src.atlascloud_comfyui.nodes.video.pixverse_v6_r2v import (
        AtlasPixVerseV6ReferenceToVideo,
    )

    required = AtlasPixVerseV6ReferenceToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "images" in required
    assert "prompt" in required
    assert AtlasPixVerseV6ReferenceToVideo.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasPixVerseV6ReferenceToVideo.CATEGORY == "AtlasCloud/Video"


def test_pixverse_new_nodes_registered():
    from src.atlascloud_comfyui.registry import (
        NODE_CLASS_MAPPINGS,
        NODE_DISPLAY_NAME_MAPPINGS,
    )

    for key in (
        "AtlasCloud PixVerse C1 Text-to-Video",
        "AtlasCloud PixVerse C1 Image-to-Video",
        "AtlasCloud PixVerse C1 Reference-to-Video",
        "AtlasCloud PixVerse V6 Text-to-Video",
        "AtlasCloud PixVerse V6 Image-to-Video",
        "AtlasCloud PixVerse V6 Reference-to-Video",
    ):
        assert key in NODE_CLASS_MAPPINGS
        assert key in NODE_DISPLAY_NAME_MAPPINGS


def test_pixverse_new_nodes_model_ids():
    import inspect

    from src.atlascloud_comfyui.nodes.video.pixverse_c1_t2v import AtlasPixVerseC1TextToVideo
    from src.atlascloud_comfyui.nodes.video.pixverse_c1_i2v import AtlasPixVerseC1ImageToVideo
    from src.atlascloud_comfyui.nodes.video.pixverse_c1_r2v import AtlasPixVerseC1ReferenceToVideo
    from src.atlascloud_comfyui.nodes.video.pixverse_v6_t2v import AtlasPixVerseV6TextToVideo
    from src.atlascloud_comfyui.nodes.video.pixverse_v6_i2v import AtlasPixVerseV6ImageToVideo
    from src.atlascloud_comfyui.nodes.video.pixverse_v6_r2v import AtlasPixVerseV6ReferenceToVideo

    expected = {
        AtlasPixVerseC1TextToVideo: "pixverse/c1/text-to-video",
        AtlasPixVerseC1ImageToVideo: "pixverse/c1/image-to-video",
        AtlasPixVerseC1ReferenceToVideo: "pixverse/c1/reference-to-video",
        AtlasPixVerseV6TextToVideo: "pixverse/v6/text-to-video",
        AtlasPixVerseV6ImageToVideo: "pixverse/v6/image-to-video",
        AtlasPixVerseV6ReferenceToVideo: "pixverse/v6/reference-to-video",
    }
    for cls, model_id in expected.items():
        assert model_id in inspect.getsource(cls.run)
