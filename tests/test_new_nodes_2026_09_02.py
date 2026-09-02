"""Metadata-only tests for newly added nodes (2026-09-02).

New models: the Gemini Omni 1.1 Flash video family (Text-to-Video /
Image-to-Video / Reference-to-Video / Video Edit / Video Extend). The 1.1 tier
differs from the existing `google/gemini-omni-flash/*` nodes: resolutions go up
to 4k, the reference payload keys are `reference_images`/`reference_videos`
(not `images`), image-to-video gained a `last_image` interpolation frame, and
video-extend is a brand-new capability — so these tests pin the model ids, the
enums and the payload keys.
These tests MUST NOT require ATLASCLOUD_API_KEY.
"""

import inspect

import pytest

from src.atlascloud_comfyui.nodes.video.google_gemini_omni_1_1_flash_i2v import (
    AtlasGeminiOmni11FlashImageToVideo,
)
from src.atlascloud_comfyui.nodes.video.google_gemini_omni_1_1_flash_r2v import (
    AtlasGeminiOmni11FlashReferenceToVideo,
)
from src.atlascloud_comfyui.nodes.video.google_gemini_omni_1_1_flash_t2v import (
    AtlasGeminiOmni11FlashTextToVideo,
)
from src.atlascloud_comfyui.nodes.video.google_gemini_omni_1_1_flash_video_edit import (
    AtlasGeminiOmni11FlashVideoEdit,
)
from src.atlascloud_comfyui.nodes.video.google_gemini_omni_1_1_flash_video_extend import (
    AtlasGeminiOmni11FlashVideoExtend,
)

_OMNI_11_MODEL_IDS = {
    AtlasGeminiOmni11FlashTextToVideo: "google/gemini-omni-1.1-flash/text-to-video",
    AtlasGeminiOmni11FlashImageToVideo: "google/gemini-omni-1.1-flash/image-to-video",
    AtlasGeminiOmni11FlashReferenceToVideo: "google/gemini-omni-1.1-flash/reference-to-video",
    AtlasGeminiOmni11FlashVideoEdit: "google/gemini-omni-1.1-flash/video-edit",
    AtlasGeminiOmni11FlashVideoExtend: "google/gemini-omni-1.1-flash/video-extend",
}

_OMNI_11_CLASSES = list(_OMNI_11_MODEL_IDS)

# video-edit takes no duration/resolution controls in its schema
_RESOLUTION_CLASSES = [c for c in _OMNI_11_CLASSES if c is not AtlasGeminiOmni11FlashVideoEdit]
# only text/image/reference-to-video expose an aspect ratio
_ASPECT_RATIO_CLASSES = [
    AtlasGeminiOmni11FlashTextToVideo,
    AtlasGeminiOmni11FlashImageToVideo,
    AtlasGeminiOmni11FlashReferenceToVideo,
]


@pytest.mark.parametrize("cls", _OMNI_11_CLASSES)
def test_omni_11_node_shape(cls):
    inputs = cls.INPUT_TYPES()
    assert "atlas_client" in inputs["required"]
    assert "prompt" in inputs["required"]
    assert "thinking_level" in inputs["optional"]
    assert "poll_interval_sec" in inputs["optional"]
    assert "timeout_sec" in inputs["optional"]
    assert cls.RETURN_TYPES == ("STRING", "STRING")
    assert cls.RETURN_NAMES == ("video_url", "prediction_id")
    assert cls.CATEGORY == "AtlasCloud/Video"
    assert cls.FUNCTION == "run"


@pytest.mark.parametrize("cls", _OMNI_11_CLASSES)
def test_omni_11_model_id(cls):
    source = inspect.getsource(cls.run)
    assert f'"model": "{_OMNI_11_MODEL_IDS[cls]}"' in source
    # must not fall back to the 1.0 tier or its developer variants
    assert '"model": "google/gemini-omni-flash/' not in source


@pytest.mark.parametrize("cls", _OMNI_11_CLASSES)
def test_omni_11_thinking_level(cls):
    thinking_level = cls.INPUT_TYPES()["optional"]["thinking_level"]
    assert thinking_level[0] == ["default", "high", "low"]
    assert thinking_level[1]["default"] == "default"


@pytest.mark.parametrize("cls", _RESOLUTION_CLASSES)
def test_omni_11_resolution_and_duration(cls):
    optional = cls.INPUT_TYPES()["optional"]
    resolution = optional["resolution"]
    assert resolution[0] == ["360p", "720p", "1080p", "4k"]
    assert resolution[1]["default"] == "720p"
    duration = optional["duration"]
    assert duration[0] == "INT"
    assert duration[1]["default"] == 10
    assert duration[1]["min"] == 3
    assert duration[1]["max"] == 10


@pytest.mark.parametrize("cls", _ASPECT_RATIO_CLASSES)
def test_omni_11_aspect_ratio(cls):
    aspect_ratio = cls.INPUT_TYPES()["optional"]["aspect_ratio"]
    assert aspect_ratio[0] == ["16:9", "9:16"]
    assert aspect_ratio[1]["default"] == "16:9"


def test_omni_11_video_edit_has_no_resolution_or_duration():
    optional = AtlasGeminiOmni11FlashVideoEdit.INPUT_TYPES()["optional"]
    assert "resolution" not in optional
    assert "duration" not in optional
    assert "aspect_ratio" not in optional


@pytest.mark.parametrize("cls", _OMNI_11_CLASSES)
def test_omni_11_seed_only_sent_when_non_negative(cls):
    source = inspect.getsource(cls.run)
    assert "if int(seed) >= 0:" in source
    assert 'payload["seed"] = int(seed)' in source


@pytest.mark.parametrize("bad_prompt", ["", "  \n \n"])
def test_omni_11_t2v_requires_prompt(bad_prompt):
    with pytest.raises(RuntimeError, match="prompt is required"):
        AtlasGeminiOmni11FlashTextToVideo().run(None, bad_prompt)


def test_omni_11_t2v_has_no_media_inputs():
    inputs = AtlasGeminiOmni11FlashTextToVideo.INPUT_TYPES()
    for key in ("image", "last_image", "video", "reference_images", "reference_videos"):
        assert key not in inputs["required"]
        assert key not in inputs["optional"]


def test_omni_11_i2v_image_inputs():
    inputs = AtlasGeminiOmni11FlashImageToVideo.INPUT_TYPES()
    assert "image" in inputs["required"]
    assert "last_image" in inputs["optional"]


@pytest.mark.parametrize("bad_image", ["", "   "])
def test_omni_11_i2v_requires_image(bad_image):
    with pytest.raises(RuntimeError, match="image is required"):
        AtlasGeminiOmni11FlashImageToVideo().run(None, "a prompt", bad_image)


def test_omni_11_i2v_requires_prompt():
    with pytest.raises(RuntimeError, match="prompt is required"):
        AtlasGeminiOmni11FlashImageToVideo().run(None, "  ", "https://example.com/a.png")


def test_omni_11_i2v_last_image_is_optional_in_payload():
    source = inspect.getsource(AtlasGeminiOmni11FlashImageToVideo.run)
    assert 'payload["last_image"] = last_image' in source


def test_omni_11_r2v_reference_inputs():
    inputs = AtlasGeminiOmni11FlashReferenceToVideo.INPUT_TYPES()
    assert "reference_images" in inputs["required"]
    assert "reference_videos" in inputs["optional"]
    # the 1.0 node used a flat `images` key; 1.1 renamed it
    source = inspect.getsource(AtlasGeminiOmni11FlashReferenceToVideo.run)
    assert '"reference_images": image_list' in source
    assert '"images":' not in source


@pytest.mark.parametrize("bad_images", ["", "   \n\n  "])
def test_omni_11_r2v_requires_reference_images(bad_images):
    with pytest.raises(RuntimeError, match="reference_images is required"):
        AtlasGeminiOmni11FlashReferenceToVideo().run(None, "a prompt", bad_images)


def test_omni_11_r2v_rejects_more_than_ten_images():
    images = "\n".join(f"https://example.com/{i}.png" for i in range(11))
    with pytest.raises(RuntimeError, match="reference_images maxItems is 10"):
        AtlasGeminiOmni11FlashReferenceToVideo().run(None, "a prompt", images)


def test_omni_11_r2v_rejects_more_than_three_videos():
    videos = "\n".join(f"https://example.com/{i}.mp4" for i in range(4))
    with pytest.raises(RuntimeError, match="reference_videos maxItems is 3"):
        AtlasGeminiOmni11FlashReferenceToVideo().run(
            None, "a prompt", "https://example.com/a.png", videos
        )


@pytest.mark.parametrize(
    "cls", [AtlasGeminiOmni11FlashVideoEdit, AtlasGeminiOmni11FlashVideoExtend]
)
def test_omni_11_video_ops_require_video(cls):
    with pytest.raises(RuntimeError, match="video is required"):
        cls().run(None, "  ", "a prompt")


@pytest.mark.parametrize(
    "cls", [AtlasGeminiOmni11FlashVideoEdit, AtlasGeminiOmni11FlashVideoExtend]
)
def test_omni_11_video_ops_require_prompt(cls):
    with pytest.raises(RuntimeError, match="prompt is required"):
        cls().run(None, "https://example.com/a.mp4", "   ")


@pytest.mark.parametrize(
    "cls", [AtlasGeminiOmni11FlashVideoEdit, AtlasGeminiOmni11FlashVideoExtend]
)
def test_omni_11_video_ops_reference_images_optional(cls):
    inputs = cls.INPUT_TYPES()
    assert "video" in inputs["required"]
    assert "reference_images" in inputs["optional"]
    source = inspect.getsource(cls.run)
    assert 'payload["reference_images"] = image_list' in source


@pytest.mark.parametrize(
    "cls", [AtlasGeminiOmni11FlashVideoEdit, AtlasGeminiOmni11FlashVideoExtend]
)
def test_omni_11_video_ops_reject_more_than_ten_images(cls):
    images = "\n".join(f"https://example.com/{i}.png" for i in range(11))
    with pytest.raises(RuntimeError, match="reference_images maxItems is 10"):
        cls().run(None, "https://example.com/a.mp4", "a prompt", images)


def test_omni_11_nodes_registered():
    from src.atlascloud_comfyui.registry import (
        NODE_CLASS_MAPPINGS,
        NODE_DISPLAY_NAME_MAPPINGS,
    )

    for key, cls in (
        ("AtlasCloud Gemini Omni 1.1 Flash Text-to-Video", AtlasGeminiOmni11FlashTextToVideo),
        ("AtlasCloud Gemini Omni 1.1 Flash Image-to-Video", AtlasGeminiOmni11FlashImageToVideo),
        (
            "AtlasCloud Gemini Omni 1.1 Flash Reference-to-Video",
            AtlasGeminiOmni11FlashReferenceToVideo,
        ),
        ("AtlasCloud Gemini Omni 1.1 Flash Video Edit", AtlasGeminiOmni11FlashVideoEdit),
        ("AtlasCloud Gemini Omni 1.1 Flash Video Extend", AtlasGeminiOmni11FlashVideoExtend),
    ):
        # registry.py imports under the `atlascloud_comfyui.*` path while the
        # tests import under `src.atlascloud_comfyui.*`, so compare by name.
        assert NODE_CLASS_MAPPINGS[key].__name__ == cls.__name__
        assert NODE_DISPLAY_NAME_MAPPINGS[key] == key
