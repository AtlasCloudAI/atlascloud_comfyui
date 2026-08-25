"""Metadata-only tests for newly added nodes (2026-08-25).

New models: the Alibaba Wan-3.0-Prime family (Text/Image/Reference-to-Video).
Its schema mirrors plain Wan-3.0, so these tests also pin the model ids to make
sure the Prime nodes do not silently fall back to the non-Prime endpoints.
These tests MUST NOT require ATLASCLOUD_API_KEY.
"""

import inspect

import pytest

from src.atlascloud_comfyui.nodes.video.alibaba_wan_3_0_prime_i2v import (
    AtlasWan30PrimeImageToVideo,
)
from src.atlascloud_comfyui.nodes.video.alibaba_wan_3_0_prime_r2v import (
    AtlasWan30PrimeReferenceToVideo,
)
from src.atlascloud_comfyui.nodes.video.alibaba_wan_3_0_prime_t2v import (
    AtlasWan30PrimeTextToVideo,
)

_PRIME_CLASSES = [
    AtlasWan30PrimeTextToVideo,
    AtlasWan30PrimeImageToVideo,
    AtlasWan30PrimeReferenceToVideo,
]

_PRIME_MODEL_IDS = {
    AtlasWan30PrimeTextToVideo: "alibaba/wan-3.0-prime/text-to-video",
    AtlasWan30PrimeImageToVideo: "alibaba/wan-3.0-prime/image-to-video",
    AtlasWan30PrimeReferenceToVideo: "alibaba/wan-3.0-prime/reference-to-video",
}


@pytest.mark.parametrize("cls", _PRIME_CLASSES)
def test_prime_node_shape(cls):
    inputs = cls.INPUT_TYPES()
    assert "atlas_client" in inputs["required"]
    assert "poll_interval_sec" in inputs["optional"]
    assert "timeout_sec" in inputs["optional"]
    assert cls.RETURN_TYPES == ("STRING", "STRING")
    assert cls.RETURN_NAMES == ("video_url", "prediction_id")
    assert cls.CATEGORY == "AtlasCloud/Video"
    assert cls.FUNCTION == "run"


@pytest.mark.parametrize("cls", _PRIME_CLASSES)
def test_prime_model_id(cls):
    source = inspect.getsource(cls.run)
    assert f'"model": "{_PRIME_MODEL_IDS[cls]}"' in source


@pytest.mark.parametrize("cls", _PRIME_CLASSES)
def test_prime_common_options(cls):
    optional = cls.INPUT_TYPES()["optional"]
    assert optional["resolution"][0] == ["1080P", "720P", "480P"]
    assert optional["resolution"][1]["default"] == "1080P"
    # -1 is the schema's "smart duration" sentinel, so min must allow it.
    assert optional["duration"][1]["min"] == -1
    assert optional["duration"][1]["max"] == 30
    assert optional["duration"][1]["default"] == 5
    assert optional["audio"][0] == "BOOLEAN"
    assert optional["audio"][1]["default"] is True
    assert optional["seed"][1]["min"] == -1


def test_prime_t2v_metadata():
    inputs = AtlasWan30PrimeTextToVideo.INPUT_TYPES()
    assert "prompt" in inputs["required"]
    ratio = inputs["optional"]["ratio"]
    assert ratio[0] == ["adaptive", "16:9", "4:3", "1:1", "3:4", "9:16"]
    assert ratio[1]["default"] == "adaptive"


@pytest.mark.parametrize("bad_prompt", ["", "   "])
def test_prime_t2v_requires_prompt(bad_prompt):
    with pytest.raises(RuntimeError, match="prompt is required"):
        AtlasWan30PrimeTextToVideo().run(None, bad_prompt)


def test_prime_i2v_metadata():
    inputs = AtlasWan30PrimeImageToVideo.INPUT_TYPES()
    assert "prompt" in inputs["required"]
    assert "image" in inputs["required"]
    assert "last_image" in inputs["optional"]
    # image-to-video derives the aspect ratio from the first frame.
    assert "ratio" not in inputs["optional"]


def test_prime_i2v_requires_prompt():
    with pytest.raises(RuntimeError, match="prompt is required"):
        AtlasWan30PrimeImageToVideo().run(None, "  ", "https://example.com/a.png")


@pytest.mark.parametrize("bad_image", ["", "   "])
def test_prime_i2v_requires_image(bad_image):
    with pytest.raises(RuntimeError, match="image is required"):
        AtlasWan30PrimeImageToVideo().run(None, "a prompt", bad_image)


def test_prime_i2v_omits_empty_last_image():
    source = inspect.getsource(AtlasWan30PrimeImageToVideo.run)
    assert 'payload["last_image"] = li' in source


def test_prime_r2v_metadata():
    inputs = AtlasWan30PrimeReferenceToVideo.INPUT_TYPES()
    assert "prompt" in inputs["required"]
    assert "reference_images" in inputs["required"]
    optional = inputs["optional"]
    assert "reference_videos" in optional
    assert "reference_audios" in optional
    assert optional["enable_thinking"][1]["default"] is True


def test_prime_r2v_requires_prompt():
    with pytest.raises(RuntimeError, match="prompt is required"):
        AtlasWan30PrimeReferenceToVideo().run(None, " ", "https://example.com/a.png")


@pytest.mark.parametrize("bad_refs", ["", "  \n \n"])
def test_prime_r2v_requires_at_least_one_reference(bad_refs):
    with pytest.raises(RuntimeError, match="at least one reference"):
        AtlasWan30PrimeReferenceToVideo().run(None, "a prompt", bad_refs)


def test_prime_r2v_rejects_too_many_images():
    urls = "\n".join(f"https://example.com/{i}.png" for i in range(11))
    with pytest.raises(RuntimeError, match="reference_images maxItems is 10"):
        AtlasWan30PrimeReferenceToVideo().run(None, "a prompt", urls)


def test_prime_r2v_rejects_too_many_videos():
    urls = "\n".join(f"https://example.com/{i}.mp4" for i in range(6))
    with pytest.raises(RuntimeError, match="reference_videos maxItems is 5"):
        AtlasWan30PrimeReferenceToVideo().run(None, "a prompt", "", urls)


def test_prime_r2v_rejects_too_many_audios():
    urls = "\n".join(f"https://example.com/{i}.mp3" for i in range(6))
    with pytest.raises(RuntimeError, match="reference_audios maxItems is 5"):
        AtlasWan30PrimeReferenceToVideo().run(None, "a prompt", "", "", urls)


def test_prime_r2v_tags_refers_by_kind():
    source = inspect.getsource(AtlasWan30PrimeReferenceToVideo.run)
    for kind in ("image", "video", "audio"):
        assert f'"type": "{kind}"' in source


def test_prime_nodes_registered():
    from src.atlascloud_comfyui.registry import (
        NODE_CLASS_MAPPINGS,
        NODE_DISPLAY_NAME_MAPPINGS,
    )

    for key, cls in (
        ("AtlasCloud WAN3.0-Prime Text-to-Video", AtlasWan30PrimeTextToVideo),
        ("AtlasCloud WAN3.0-Prime Image-to-Video", AtlasWan30PrimeImageToVideo),
        ("AtlasCloud WAN3.0-Prime Reference-to-Video", AtlasWan30PrimeReferenceToVideo),
    ):
        # registry.py imports under the `atlascloud_comfyui.*` path while the
        # tests import under `src.atlascloud_comfyui.*`, so compare by name.
        assert NODE_CLASS_MAPPINGS[key].__name__ == cls.__name__
        assert NODE_DISPLAY_NAME_MAPPINGS[key] == key
