"""Metadata-only tests for newly added nodes (2026-08-06).

New models: BLACK FOREST LABS FLUX 3 video family (text-to-video, image-to-video,
first-last-frame-to-video, keyframes-to-video, extend-video) and Kling v3.0
Pro/Std Motion Control.
These tests MUST NOT require ATLASCLOUD_API_KEY.
"""

import inspect
import json

import pytest

_ASPECT_RATIOS = ["auto", "21:9", "2:1", "16:9", "4:3", "1:1", "3:4", "9:16"]


def _flux3_common_assertions(cls):
    inputs = cls.INPUT_TYPES()
    optional = inputs["optional"]
    assert "atlas_client" in inputs["required"]
    assert optional["aspect_ratio"][0] == _ASPECT_RATIOS
    assert optional["aspect_ratio"][1]["default"] == "auto"
    assert optional["resolution"][0] == ["720p", "1080p"]
    assert optional["resolution"][1]["default"] == "720p"
    assert optional["duration"][1]["default"] == 5
    assert optional["duration"][1]["min"] == 5
    assert optional["duration"][1]["max"] == 20
    assert optional["generate_audio"][0] == "BOOLEAN"
    assert optional["generate_audio"][1]["default"] is True
    assert optional["safety_tolerance"][1]["min"] == 0
    assert optional["safety_tolerance"][1]["max"] == 4
    assert optional["safety_tolerance"][1]["default"] == 2
    assert optional["seed"][1]["min"] == -1
    assert cls.RETURN_TYPES == ("STRING", "STRING")
    assert cls.RETURN_NAMES == ("video_url", "prediction_id")
    assert cls.CATEGORY == "AtlasCloud/Video"
    assert "if seed >= 0:" in inspect.getsource(cls.run)


def test_flux3_t2v_metadata():
    from src.atlascloud_comfyui.nodes.video.flux3_t2v import AtlasFlux3TextToVideo

    _flux3_common_assertions(AtlasFlux3TextToVideo)
    assert "prompt" in AtlasFlux3TextToVideo.INPUT_TYPES()["required"]


@pytest.mark.parametrize("bad_prompt", ["", "   "])
def test_flux3_t2v_requires_prompt(bad_prompt):
    from src.atlascloud_comfyui.nodes.video.flux3_t2v import AtlasFlux3TextToVideo

    with pytest.raises(RuntimeError, match="prompt is required"):
        AtlasFlux3TextToVideo().run(None, bad_prompt)


def test_flux3_i2v_metadata():
    from src.atlascloud_comfyui.nodes.video.flux3_i2v import AtlasFlux3ImageToVideo

    _flux3_common_assertions(AtlasFlux3ImageToVideo)
    assert "image_url" in AtlasFlux3ImageToVideo.INPUT_TYPES()["required"]
    assert "prompt" in AtlasFlux3ImageToVideo.INPUT_TYPES()["optional"]


@pytest.mark.parametrize("bad_url", ["", "  "])
def test_flux3_i2v_requires_image_url(bad_url):
    from src.atlascloud_comfyui.nodes.video.flux3_i2v import AtlasFlux3ImageToVideo

    with pytest.raises(RuntimeError, match="image_url is required"):
        AtlasFlux3ImageToVideo().run(None, bad_url)


def test_flux3_first_last_frame_metadata():
    from src.atlascloud_comfyui.nodes.video.flux3_first_last_frame_to_video import (
        AtlasFlux3FirstLastFrameToVideo,
    )

    _flux3_common_assertions(AtlasFlux3FirstLastFrameToVideo)
    required = AtlasFlux3FirstLastFrameToVideo.INPUT_TYPES()["required"]
    assert "start_image_url" in required
    assert "end_image_url" in required


def test_flux3_first_last_frame_requires_both_frames():
    from src.atlascloud_comfyui.nodes.video.flux3_first_last_frame_to_video import (
        AtlasFlux3FirstLastFrameToVideo,
    )

    with pytest.raises(RuntimeError, match="start_image_url is required"):
        AtlasFlux3FirstLastFrameToVideo().run(None, "  ", "https://example.com/b.png")
    with pytest.raises(RuntimeError, match="end_image_url is required"):
        AtlasFlux3FirstLastFrameToVideo().run(None, "https://example.com/a.png", "")


def test_flux3_extend_video_metadata():
    from src.atlascloud_comfyui.nodes.video.flux3_extend_video import AtlasFlux3ExtendVideo

    _flux3_common_assertions(AtlasFlux3ExtendVideo)
    assert "video_url" in AtlasFlux3ExtendVideo.INPUT_TYPES()["required"]


@pytest.mark.parametrize("bad_url", ["", "   "])
def test_flux3_extend_video_requires_video_url(bad_url):
    from src.atlascloud_comfyui.nodes.video.flux3_extend_video import AtlasFlux3ExtendVideo

    with pytest.raises(RuntimeError, match="video_url is required"):
        AtlasFlux3ExtendVideo().run(None, bad_url)


def test_flux3_keyframes_metadata():
    from src.atlascloud_comfyui.nodes.video.flux3_keyframes_to_video import (
        AtlasFlux3KeyframesToVideo,
    )

    _flux3_common_assertions(AtlasFlux3KeyframesToVideo)
    assert "keyframes" in AtlasFlux3KeyframesToVideo.INPUT_TYPES()["required"]


def test_flux3_keyframes_parses_valid_json():
    from src.atlascloud_comfyui.nodes.video.flux3_keyframes_to_video import (
        AtlasFlux3KeyframesToVideo,
    )

    raw = json.dumps(
        [
            {"image_url": " https://example.com/a.png ", "frame_index": 0},
            {"image_url": "https://example.com/b.png", "frame_index": 119},
        ]
    )
    parsed = AtlasFlux3KeyframesToVideo._parse_keyframes(raw, 5)
    assert parsed == [
        {"image_url": "https://example.com/a.png", "frame_index": 0},
        {"image_url": "https://example.com/b.png", "frame_index": 119},
    ]


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("", "keyframes is required"),
        ("not json", "keyframes must be valid JSON"),
        ("[]", "keyframes must be a non-empty JSON array"),
        ('{"image_url": "x", "frame_index": 0}', "keyframes must be a non-empty JSON array"),
        ('[{"frame_index": 0}]', "each keyframe requires image_url"),
        ('[{"image_url": "https://example.com/a.png"}]', "each keyframe requires frame_index"),
        (
            '[{"image_url": "https://example.com/a.png", "frame_index": 121}]',
            r"frame_index must be between 0 and duration \* 24",
        ),
        (
            '[{"image_url": "https://example.com/a.png", "frame_index": 1},'
            ' {"image_url": "https://example.com/b.png", "frame_index": 1}]',
            "frame_index values must be unique",
        ),
    ],
)
def test_flux3_keyframes_rejects_bad_input(raw, expected):
    from src.atlascloud_comfyui.nodes.video.flux3_keyframes_to_video import (
        AtlasFlux3KeyframesToVideo,
    )

    with pytest.raises(RuntimeError, match=expected):
        AtlasFlux3KeyframesToVideo._parse_keyframes(raw, 5)


def test_flux3_keyframes_rejects_too_many():
    from src.atlascloud_comfyui.nodes.video.flux3_keyframes_to_video import (
        AtlasFlux3KeyframesToVideo,
    )

    raw = json.dumps([{"image_url": f"https://example.com/{i}.png", "frame_index": i} for i in range(11)])
    with pytest.raises(RuntimeError, match="keyframes maxItems is 10"):
        AtlasFlux3KeyframesToVideo._parse_keyframes(raw, 5)


@pytest.mark.parametrize(
    "module_name,class_name",
    [
        ("kling_v30_pro_motion_control", "AtlasKlingV30ProMotionControl"),
        ("kling_v30_std_motion_control", "AtlasKlingV30StdMotionControl"),
    ],
)
def test_kling_v30_motion_control_metadata(module_name, class_name):
    module = __import__(
        f"src.atlascloud_comfyui.nodes.video.{module_name}", fromlist=[class_name]
    )
    cls = getattr(module, class_name)

    inputs = cls.INPUT_TYPES()
    required = inputs["required"]
    optional = inputs["optional"]
    assert "atlas_client" in required
    assert "image" in required
    assert "video" in required
    assert required["character_orientation"][0] == ["image", "video"]
    assert required["character_orientation"][1]["default"] == "image"
    assert optional["keep_original_sound"][0] == "BOOLEAN"
    assert optional["keep_original_sound"][1]["default"] is True
    assert cls.RETURN_TYPES == ("STRING", "STRING")
    assert cls.RETURN_NAMES == ("video_url", "prediction_id")
    assert cls.CATEGORY == "AtlasCloud/Video"


@pytest.mark.parametrize(
    "module_name,class_name",
    [
        ("kling_v30_pro_motion_control", "AtlasKlingV30ProMotionControl"),
        ("kling_v30_std_motion_control", "AtlasKlingV30StdMotionControl"),
    ],
)
def test_kling_v30_motion_control_requires_image_and_video(module_name, class_name):
    module = __import__(
        f"src.atlascloud_comfyui.nodes.video.{module_name}", fromlist=[class_name]
    )
    cls = getattr(module, class_name)

    with pytest.raises(RuntimeError, match="image is required"):
        cls().run(None, "  ", "https://example.com/a.mp4")
    with pytest.raises(RuntimeError, match="video is required"):
        cls().run(None, "https://example.com/a.png", "")


def test_new_nodes_2026_08_06_registered():
    from src.atlascloud_comfyui.registry import (
        NODE_CLASS_MAPPINGS,
        NODE_DISPLAY_NAME_MAPPINGS,
    )

    keys = [
        "AtlasCloud FLUX 3 Text-to-Video",
        "AtlasCloud FLUX 3 Image-to-Video",
        "AtlasCloud FLUX 3 First & Last Frame to Video",
        "AtlasCloud FLUX 3 Keyframes to Video",
        "AtlasCloud FLUX 3 Extend Video",
        "AtlasCloud Kling V3.0 Pro Motion Control",
        "AtlasCloud Kling V3.0 Std Motion Control",
    ]
    for key in keys:
        assert key in NODE_CLASS_MAPPINGS
        assert key in NODE_DISPLAY_NAME_MAPPINGS


def test_new_nodes_2026_08_06_model_ids():
    from src.atlascloud_comfyui.nodes.video.flux3_extend_video import AtlasFlux3ExtendVideo
    from src.atlascloud_comfyui.nodes.video.flux3_first_last_frame_to_video import (
        AtlasFlux3FirstLastFrameToVideo,
    )
    from src.atlascloud_comfyui.nodes.video.flux3_i2v import AtlasFlux3ImageToVideo
    from src.atlascloud_comfyui.nodes.video.flux3_keyframes_to_video import (
        AtlasFlux3KeyframesToVideo,
    )
    from src.atlascloud_comfyui.nodes.video.flux3_t2v import AtlasFlux3TextToVideo
    from src.atlascloud_comfyui.nodes.video.kling_v30_pro_motion_control import (
        AtlasKlingV30ProMotionControl,
    )
    from src.atlascloud_comfyui.nodes.video.kling_v30_std_motion_control import (
        AtlasKlingV30StdMotionControl,
    )

    expected = [
        (AtlasFlux3TextToVideo, "black-forest-labs/flux-3/text-to-video"),
        (AtlasFlux3ImageToVideo, "black-forest-labs/flux-3/image-to-video"),
        (AtlasFlux3FirstLastFrameToVideo, "black-forest-labs/flux-3/first-last-frame-to-video"),
        (AtlasFlux3KeyframesToVideo, "black-forest-labs/flux-3/keyframes-to-video"),
        (AtlasFlux3ExtendVideo, "black-forest-labs/flux-3/extend-video"),
        (AtlasKlingV30ProMotionControl, "kwaivgi/kling-v3.0-pro/motion-control"),
        (AtlasKlingV30StdMotionControl, "kwaivgi/kling-v3.0-std/motion-control"),
    ]
    for cls, model_id in expected:
        source = inspect.getsource(cls.run)
        assert f'"model": "{model_id}"' in source
