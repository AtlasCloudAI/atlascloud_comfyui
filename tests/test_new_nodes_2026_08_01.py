"""Metadata-only tests for newly added nodes (2026-08-01).

New models: Grok Imagine Video v1.5 (T2V / R2V).
These tests MUST NOT require ATLASCLOUD_API_KEY.
"""

import inspect

import pytest


def test_grok_imagine_video_v15_t2v_metadata():
    from src.atlascloud_comfyui.nodes.video.xai_grok_imagine_video_v15_t2v import (
        AtlasGrokImagineVideoV15TextToVideo,
    )

    inputs = AtlasGrokImagineVideoV15TextToVideo.INPUT_TYPES()
    required = inputs["required"]
    optional = inputs["optional"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert optional["resolution"][0] == ["480p", "720p", "1080p"]
    assert optional["resolution"][1]["default"] == "720p"
    assert optional["aspect_ratio"][0] == ["1:1", "16:9", "9:16", "4:3", "3:4", "3:2", "2:3"]
    assert optional["duration"][1]["min"] == 1
    assert optional["duration"][1]["max"] == 15
    assert optional["duration"][1]["default"] == 8
    assert AtlasGrokImagineVideoV15TextToVideo.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasGrokImagineVideoV15TextToVideo.RETURN_NAMES == ("video_url", "prediction_id")
    assert AtlasGrokImagineVideoV15TextToVideo.CATEGORY == "AtlasCloud/Video"


@pytest.mark.parametrize("bad_prompt", ["", "   "])
def test_grok_imagine_video_v15_t2v_requires_prompt(bad_prompt):
    from src.atlascloud_comfyui.nodes.video.xai_grok_imagine_video_v15_t2v import (
        AtlasGrokImagineVideoV15TextToVideo,
    )

    with pytest.raises(RuntimeError, match="prompt is required"):
        AtlasGrokImagineVideoV15TextToVideo().run(None, bad_prompt)


def test_grok_imagine_video_v15_r2v_metadata():
    from src.atlascloud_comfyui.nodes.video.xai_grok_imagine_video_v15_r2v import (
        VOICE_IDS,
        AtlasGrokImagineVideoV15ReferenceToVideo,
    )

    inputs = AtlasGrokImagineVideoV15ReferenceToVideo.INPUT_TYPES()
    required = inputs["required"]
    optional = inputs["optional"]
    assert "prompt" in required
    assert "image_urls" in required
    assert "voice_ids" in optional
    assert optional["resolution"][0] == ["480p", "720p"]
    assert optional["duration"][1]["max"] == 15
    assert len(VOICE_IDS) == 26
    assert "altair" in VOICE_IDS and "zenith" in VOICE_IDS
    assert AtlasGrokImagineVideoV15ReferenceToVideo.RETURN_NAMES == ("video_url", "prediction_id")
    assert AtlasGrokImagineVideoV15ReferenceToVideo.CATEGORY == "AtlasCloud/Video"


def test_grok_imagine_video_v15_r2v_requires_prompt():
    from src.atlascloud_comfyui.nodes.video.xai_grok_imagine_video_v15_r2v import (
        AtlasGrokImagineVideoV15ReferenceToVideo,
    )

    with pytest.raises(RuntimeError, match="prompt is required"):
        AtlasGrokImagineVideoV15ReferenceToVideo().run(None, "  ", "https://example.com/a.png")


@pytest.mark.parametrize("bad_urls", ["", "  \n \n"])
def test_grok_imagine_video_v15_r2v_requires_image_urls(bad_urls):
    from src.atlascloud_comfyui.nodes.video.xai_grok_imagine_video_v15_r2v import (
        AtlasGrokImagineVideoV15ReferenceToVideo,
    )

    with pytest.raises(RuntimeError, match="image_urls is required"):
        AtlasGrokImagineVideoV15ReferenceToVideo().run(None, "a prompt", bad_urls)


def test_grok_imagine_video_v15_r2v_rejects_too_many_images():
    from src.atlascloud_comfyui.nodes.video.xai_grok_imagine_video_v15_r2v import (
        AtlasGrokImagineVideoV15ReferenceToVideo,
    )

    urls = "\n".join(f"https://example.com/{i}.png" for i in range(8))
    with pytest.raises(RuntimeError, match="image_urls maxItems is 7"):
        AtlasGrokImagineVideoV15ReferenceToVideo().run(None, "a prompt", urls)


def test_grok_imagine_video_v15_r2v_rejects_too_many_voices():
    from src.atlascloud_comfyui.nodes.video.xai_grok_imagine_video_v15_r2v import (
        AtlasGrokImagineVideoV15ReferenceToVideo,
    )

    with pytest.raises(RuntimeError, match="voice_ids maxItems is 3"):
        AtlasGrokImagineVideoV15ReferenceToVideo().run(
            None,
            "a prompt",
            "https://example.com/a.png",
            "altair\nara\natlas\ncarina",
        )


def test_grok_imagine_video_v15_r2v_rejects_unknown_voice():
    from src.atlascloud_comfyui.nodes.video.xai_grok_imagine_video_v15_r2v import (
        AtlasGrokImagineVideoV15ReferenceToVideo,
    )

    with pytest.raises(RuntimeError, match="Unknown voice_ids"):
        AtlasGrokImagineVideoV15ReferenceToVideo().run(
            None,
            "a prompt",
            "https://example.com/a.png",
            "not-a-voice",
        )


def test_grok_imagine_video_v15_r2v_voice_ids_optional_in_payload():
    from src.atlascloud_comfyui.nodes.video.xai_grok_imagine_video_v15_r2v import (
        AtlasGrokImagineVideoV15ReferenceToVideo,
    )

    source = inspect.getsource(AtlasGrokImagineVideoV15ReferenceToVideo.run)
    assert 'payload["voice_ids"] = voices' in source
    assert "if voices:" in source


def test_new_nodes_2026_08_01_registered():
    from src.atlascloud_comfyui.registry import (
        NODE_CLASS_MAPPINGS,
        NODE_DISPLAY_NAME_MAPPINGS,
    )

    keys = [
        "AtlasCloud Grok Imagine Video v1.5 Text-to-Video",
        "AtlasCloud Grok Imagine Video v1.5 Reference-to-Video",
    ]
    for key in keys:
        assert key in NODE_CLASS_MAPPINGS
        assert key in NODE_DISPLAY_NAME_MAPPINGS


def test_new_nodes_2026_08_01_model_ids():
    from src.atlascloud_comfyui.nodes.video.xai_grok_imagine_video_v15_r2v import (
        AtlasGrokImagineVideoV15ReferenceToVideo,
    )
    from src.atlascloud_comfyui.nodes.video.xai_grok_imagine_video_v15_t2v import (
        AtlasGrokImagineVideoV15TextToVideo,
    )

    expected = [
        (AtlasGrokImagineVideoV15TextToVideo, "xai/grok-imagine-video-v1.5/text-to-video"),
        (AtlasGrokImagineVideoV15ReferenceToVideo, "xai/grok-imagine-video-v1.5/reference-to-video"),
    ]
    for cls, model_id in expected:
        source = inspect.getsource(cls.run)
        assert f'"model": "{model_id}"' in source
