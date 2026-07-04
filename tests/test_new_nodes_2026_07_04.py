"""Metadata-only tests for newly added nodes (2026-07-04).

Gemini Omni Flash non-developer video variants (text-to-video, image-to-video,
reference-to-video) plus the new video-edit node.
These tests MUST NOT require ATLASCLOUD_API_KEY.
"""


def test_gemini_omni_flash_t2v_metadata():
    from src.atlascloud_comfyui.nodes.video.google_gemini_omni_flash_t2v import (
        AtlasGeminiOmniFlashTextToVideo,
    )

    required = AtlasGeminiOmniFlashTextToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert AtlasGeminiOmniFlashTextToVideo.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasGeminiOmniFlashTextToVideo.CATEGORY == "AtlasCloud/Video"


def test_gemini_omni_flash_i2v_metadata():
    from src.atlascloud_comfyui.nodes.video.google_gemini_omni_flash_i2v import (
        AtlasGeminiOmniFlashImageToVideo,
    )

    required = AtlasGeminiOmniFlashImageToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert "image" in required
    assert AtlasGeminiOmniFlashImageToVideo.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasGeminiOmniFlashImageToVideo.CATEGORY == "AtlasCloud/Video"


def test_gemini_omni_flash_r2v_metadata():
    from src.atlascloud_comfyui.nodes.video.google_gemini_omni_flash_r2v import (
        AtlasGeminiOmniFlashReferenceToVideo,
    )

    required = AtlasGeminiOmniFlashReferenceToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert "images" in required
    assert AtlasGeminiOmniFlashReferenceToVideo.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasGeminiOmniFlashReferenceToVideo.CATEGORY == "AtlasCloud/Video"


def test_gemini_omni_flash_video_edit_metadata():
    from src.atlascloud_comfyui.nodes.video.google_gemini_omni_flash_video_edit import (
        AtlasGeminiOmniFlashVideoEdit,
    )

    required = AtlasGeminiOmniFlashVideoEdit.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "video" in required
    assert "prompt" in required
    assert AtlasGeminiOmniFlashVideoEdit.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasGeminiOmniFlashVideoEdit.CATEGORY == "AtlasCloud/Video"


def test_new_nodes_2026_07_04_registered():
    from src.atlascloud_comfyui.registry import (
        NODE_CLASS_MAPPINGS,
        NODE_DISPLAY_NAME_MAPPINGS,
    )

    for key in (
        "AtlasCloud Gemini Omni Flash Text-to-Video",
        "AtlasCloud Gemini Omni Flash Image-to-Video",
        "AtlasCloud Gemini Omni Flash Reference-to-Video",
        "AtlasCloud Gemini Omni Flash Video Edit",
    ):
        assert key in NODE_CLASS_MAPPINGS
        assert key in NODE_DISPLAY_NAME_MAPPINGS


def test_new_nodes_2026_07_04_model_ids():
    import inspect

    from src.atlascloud_comfyui.nodes.video.google_gemini_omni_flash_t2v import AtlasGeminiOmniFlashTextToVideo
    from src.atlascloud_comfyui.nodes.video.google_gemini_omni_flash_i2v import AtlasGeminiOmniFlashImageToVideo
    from src.atlascloud_comfyui.nodes.video.google_gemini_omni_flash_r2v import AtlasGeminiOmniFlashReferenceToVideo
    from src.atlascloud_comfyui.nodes.video.google_gemini_omni_flash_video_edit import AtlasGeminiOmniFlashVideoEdit

    expected = {
        AtlasGeminiOmniFlashTextToVideo: "google/gemini-omni-flash/text-to-video",
        AtlasGeminiOmniFlashImageToVideo: "google/gemini-omni-flash/image-to-video",
        AtlasGeminiOmniFlashReferenceToVideo: "google/gemini-omni-flash/reference-to-video",
        AtlasGeminiOmniFlashVideoEdit: "google/gemini-omni-flash/video-edit",
    }
    for cls, model_id in expected.items():
        src = inspect.getsource(cls.run)
        assert f'"model": "{model_id}"' in src
