"""Metadata-only tests for newly added nodes (2026-09-07).

New models: the MiniMax H3 Fast video trio (Text-/Image-/Reference-to-Video),
the Grok Imagine Image 2.0 Developer pair (Text-to-Image / Edit) and the Grok
Imagine Video v1.5 Developer trio. Each new node mirrors the request schema of
its non-fast / non-developer sibling, so these tests mainly pin the model ids
and the required-input validation so the new nodes cannot silently fall back to
the sibling tier.
These tests MUST NOT require ATLASCLOUD_API_KEY.
"""

import inspect

import pytest

from src.atlascloud_comfyui.nodes.image.xai_grok_imagine_image_20_developer_edit import (
    AtlasGrokImagineImage20DeveloperEdit,
)
from src.atlascloud_comfyui.nodes.image.xai_grok_imagine_image_20_developer_t2i import (
    AtlasGrokImagineImage20DeveloperTextToImage,
)
from src.atlascloud_comfyui.nodes.video.minimax_h3_fast_i2v import (
    AtlasMinimaxH3FastImageToVideo,
)
from src.atlascloud_comfyui.nodes.video.minimax_h3_fast_r2v import (
    AtlasMinimaxH3FastReferenceToVideo,
)
from src.atlascloud_comfyui.nodes.video.minimax_h3_fast_t2v import (
    AtlasMinimaxH3FastTextToVideo,
)
from src.atlascloud_comfyui.nodes.video.xai_grok_imagine_video_v15_developer_i2v import (
    AtlasGrokImagineVideoV15DeveloperImageToVideo,
)
from src.atlascloud_comfyui.nodes.video.xai_grok_imagine_video_v15_developer_r2v import (
    AtlasGrokImagineVideoV15DeveloperReferenceToVideo,
)
from src.atlascloud_comfyui.nodes.video.xai_grok_imagine_video_v15_developer_t2v import (
    AtlasGrokImagineVideoV15DeveloperTextToVideo,
)

_MODEL_IDS = {
    AtlasMinimaxH3FastTextToVideo: "minimax/h3-fast/text-to-video",
    AtlasMinimaxH3FastImageToVideo: "minimax/h3-fast/image-to-video",
    AtlasMinimaxH3FastReferenceToVideo: "minimax/h3-fast/reference-to-video",
    AtlasGrokImagineImage20DeveloperTextToImage: "xai/grok-imagine-image-2.0-developer/text-to-image",
    AtlasGrokImagineImage20DeveloperEdit: "xai/grok-imagine-image-2.0-developer/edit",
    AtlasGrokImagineVideoV15DeveloperTextToVideo: "xai/grok-imagine-video-v1.5-developer/text-to-video",
    AtlasGrokImagineVideoV15DeveloperImageToVideo: "xai/grok-imagine-video-v1.5-developer/image-to-video",
    AtlasGrokImagineVideoV15DeveloperReferenceToVideo: "xai/grok-imagine-video-v1.5-developer/reference-to-video",
}

_CLASSES = list(_MODEL_IDS)

_VIDEO_CLASSES = [
    AtlasMinimaxH3FastTextToVideo,
    AtlasMinimaxH3FastImageToVideo,
    AtlasMinimaxH3FastReferenceToVideo,
    AtlasGrokImagineVideoV15DeveloperTextToVideo,
    AtlasGrokImagineVideoV15DeveloperImageToVideo,
    AtlasGrokImagineVideoV15DeveloperReferenceToVideo,
]

_IMAGE_CLASSES = [
    AtlasGrokImagineImage20DeveloperTextToImage,
    AtlasGrokImagineImage20DeveloperEdit,
]


@pytest.mark.parametrize("cls", _CLASSES)
def test_node_shape(cls):
    inputs = cls.INPUT_TYPES()
    assert "atlas_client" in inputs["required"]
    assert "prompt" in inputs["required"]
    assert "poll_interval_sec" in inputs["optional"]
    assert "timeout_sec" in inputs["optional"]
    assert cls.RETURN_TYPES == ("STRING", "STRING")
    assert cls.FUNCTION == "run"


@pytest.mark.parametrize("cls", _VIDEO_CLASSES)
def test_video_node_category(cls):
    assert cls.CATEGORY == "AtlasCloud/Video"
    assert cls.RETURN_NAMES == ("video_url", "prediction_id")


@pytest.mark.parametrize("cls", _IMAGE_CLASSES)
def test_image_node_category(cls):
    assert cls.CATEGORY == "AtlasCloud/Image"
    assert cls.RETURN_NAMES == ("image_url", "prediction_id")


@pytest.mark.parametrize("cls", _CLASSES)
def test_model_id(cls):
    source = inspect.getsource(cls.run)
    assert f'"model": "{_MODEL_IDS[cls]}"' in source


@pytest.mark.parametrize(
    "cls, sibling_prefixes",
    [
        (AtlasMinimaxH3FastTextToVideo, ('"model": "minimax/h3/', '"model": "minimax/h3-max/')),
        (AtlasMinimaxH3FastImageToVideo, ('"model": "minimax/h3/', '"model": "minimax/h3-max/')),
        (AtlasMinimaxH3FastReferenceToVideo, ('"model": "minimax/h3/', '"model": "minimax/h3-max/')),
        (AtlasGrokImagineImage20DeveloperTextToImage, ('"model": "xai/grok-imagine-image-2.0/',)),
        (AtlasGrokImagineImage20DeveloperEdit, ('"model": "xai/grok-imagine-image-2.0/',)),
        (AtlasGrokImagineVideoV15DeveloperTextToVideo, ('"model": "xai/grok-imagine-video-v1.5/',)),
        (AtlasGrokImagineVideoV15DeveloperImageToVideo, ('"model": "xai/grok-imagine-video-v1.5/',)),
        (AtlasGrokImagineVideoV15DeveloperReferenceToVideo, ('"model": "xai/grok-imagine-video-v1.5/',)),
    ],
)
def test_does_not_fall_back_to_sibling_tier(cls, sibling_prefixes):
    source = inspect.getsource(cls.run)
    for prefix in sibling_prefixes:
        assert prefix not in source


@pytest.mark.parametrize("cls", [AtlasMinimaxH3FastTextToVideo, AtlasMinimaxH3FastReferenceToVideo])
def test_h3_fast_resolution_is_480p_only(cls):
    resolution = cls.INPUT_TYPES()["optional"]["resolution"]
    assert resolution[0] == ["480P"]
    assert resolution[1]["default"] == "480P"


def test_h3_fast_i2v_ratio_is_adaptive_only():
    ratio = AtlasMinimaxH3FastImageToVideo.INPUT_TYPES()["optional"]["ratio"]
    assert ratio[0] == ["adaptive"]
    assert ratio[1]["default"] == "adaptive"


def test_h3_fast_r2v_ratio_default_is_16_9():
    ratio = AtlasMinimaxH3FastReferenceToVideo.INPUT_TYPES()["optional"]["ratio"]
    assert ratio[1]["default"] == "16:9"


@pytest.mark.parametrize("bad_prompt", ["", "  \n \n"])
def test_h3_fast_t2v_requires_prompt(bad_prompt):
    with pytest.raises(RuntimeError, match="prompt is required"):
        AtlasMinimaxH3FastTextToVideo().run(None, bad_prompt)


@pytest.mark.parametrize("bad_image", ["", "   "])
def test_h3_fast_i2v_requires_image(bad_image):
    with pytest.raises(RuntimeError, match="image is required"):
        AtlasMinimaxH3FastImageToVideo().run(None, bad_image, "a prompt")


@pytest.mark.parametrize("bad_refers", ["", "  \n \n"])
def test_h3_fast_r2v_requires_refers(bad_refers):
    with pytest.raises(RuntimeError, match="refers is required"):
        AtlasMinimaxH3FastReferenceToVideo().run(None, bad_refers, "a prompt")


@pytest.mark.parametrize("bad_prompt", ["", "  \n \n"])
def test_grok_video_developer_requires_prompt(bad_prompt):
    with pytest.raises(RuntimeError, match="prompt is required"):
        AtlasGrokImagineVideoV15DeveloperTextToVideo().run(None, bad_prompt)
    with pytest.raises(RuntimeError, match="prompt is required"):
        AtlasGrokImagineVideoV15DeveloperImageToVideo().run(None, bad_prompt, "https://example.com/a.png")
    with pytest.raises(RuntimeError, match="prompt is required"):
        AtlasGrokImagineVideoV15DeveloperReferenceToVideo().run(None, bad_prompt, "https://example.com/a.png")


@pytest.mark.parametrize("bad_image", ["", "   "])
def test_grok_video_developer_i2v_requires_image_url(bad_image):
    with pytest.raises(RuntimeError, match="image_url is required"):
        AtlasGrokImagineVideoV15DeveloperImageToVideo().run(None, "a prompt", bad_image)


def test_grok_video_developer_r2v_image_urls_bounds():
    node = AtlasGrokImagineVideoV15DeveloperReferenceToVideo()
    with pytest.raises(RuntimeError, match="image_urls is required"):
        node.run(None, "a prompt", "   \n  ")
    too_many = "\n".join(f"https://example.com/{i}.png" for i in range(8))
    with pytest.raises(RuntimeError, match="image_urls maxItems is 7"):
        node.run(None, "a prompt", too_many)


def test_grok_video_developer_r2v_voice_ids_validation():
    node = AtlasGrokImagineVideoV15DeveloperReferenceToVideo()
    urls = "https://example.com/0.png"
    with pytest.raises(RuntimeError, match="voice_ids maxItems is 3"):
        node.run(None, "a prompt", urls, "atlas\nara\nleo\nluna")
    with pytest.raises(RuntimeError, match="Unknown voice_ids"):
        node.run(None, "a prompt", urls, "not-a-voice")


def test_grok_video_developer_i2v_supports_1080p():
    resolution = AtlasGrokImagineVideoV15DeveloperImageToVideo.INPUT_TYPES()["optional"]["resolution"]
    assert resolution[0] == ["480p", "720p", "1080p"]


def test_grok_video_developer_r2v_capped_at_720p():
    resolution = AtlasGrokImagineVideoV15DeveloperReferenceToVideo.INPUT_TYPES()["optional"]["resolution"]
    assert resolution[0] == ["480p", "720p"]


def test_grok_image_developer_edit_image_urls_bounds():
    node = AtlasGrokImagineImage20DeveloperEdit()
    args = ("1k", "medium", "auto", 1, False)
    with pytest.raises(RuntimeError, match="image_urls is required"):
        node.run(None, "a prompt", "   \n ", *args)
    too_many = "\n".join(f"https://example.com/{i}.png" for i in range(4))
    with pytest.raises(RuntimeError, match="image_urls maxItems is 3"):
        node.run(None, "a prompt", too_many, *args)


def test_grok_image_developer_edit_aspect_ratio_has_auto():
    aspect_ratio = AtlasGrokImagineImage20DeveloperEdit.INPUT_TYPES()["required"]["aspect_ratio"]
    assert aspect_ratio[0][0] == "auto"
    assert aspect_ratio[1]["default"] == "auto"


def test_grok_image_developer_t2i_has_no_image_input():
    inputs = AtlasGrokImagineImage20DeveloperTextToImage.INPUT_TYPES()
    assert "image_urls" not in inputs["required"]
    assert "image_urls" not in inputs["optional"]


def test_new_nodes_registered():
    from src.atlascloud_comfyui.registry import (
        NODE_CLASS_MAPPINGS,
        NODE_DISPLAY_NAME_MAPPINGS,
    )

    for key, cls in (
        ("AtlasCloud MiniMax H3 Fast Text-to-Video", AtlasMinimaxH3FastTextToVideo),
        ("AtlasCloud MiniMax H3 Fast Image-to-Video", AtlasMinimaxH3FastImageToVideo),
        ("AtlasCloud MiniMax H3 Fast Reference-to-Video", AtlasMinimaxH3FastReferenceToVideo),
        ("AtlasCloud Grok Imagine Image 2.0 Developer Text-to-Image", AtlasGrokImagineImage20DeveloperTextToImage),
        ("AtlasCloud Grok Imagine Image 2.0 Developer Edit", AtlasGrokImagineImage20DeveloperEdit),
        ("AtlasCloud Grok Imagine Video v1.5 Developer Text-to-Video", AtlasGrokImagineVideoV15DeveloperTextToVideo),
        ("AtlasCloud Grok Imagine Video v1.5 Developer Image-to-Video", AtlasGrokImagineVideoV15DeveloperImageToVideo),
        (
            "AtlasCloud Grok Imagine Video v1.5 Developer Reference-to-Video",
            AtlasGrokImagineVideoV15DeveloperReferenceToVideo,
        ),
    ):
        # registry.py imports under the `atlascloud_comfyui.*` path while the
        # tests import under `src.atlascloud_comfyui.*`, so compare by name.
        assert NODE_CLASS_MAPPINGS[key].__name__ == cls.__name__
        assert NODE_DISPLAY_NAME_MAPPINGS[key] == key
