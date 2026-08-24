"""Metadata-only tests for newly added nodes (2026-08-24).

New models: Alibaba Wan-3.0 (Text/Image/Reference-to-Video) and the AtlasCloud
Studio family (Product Visuals, Food Motion, Virtual Try-On, UGC Ad, Trend
Remix, TVC Maker).
These tests MUST NOT require ATLASCLOUD_API_KEY.
"""

import inspect

import pytest

from src.atlascloud_comfyui.nodes.image.atlascloud_studio_product_visuals import (
    AtlasStudioProductVisuals,
)
from src.atlascloud_comfyui.nodes.video.alibaba_wan_3_0_i2v import AtlasWan30ImageToVideo
from src.atlascloud_comfyui.nodes.video.alibaba_wan_3_0_r2v import AtlasWan30ReferenceToVideo
from src.atlascloud_comfyui.nodes.video.alibaba_wan_3_0_t2v import AtlasWan30TextToVideo
from src.atlascloud_comfyui.nodes.video.atlascloud_studio_food_motion import AtlasStudioFoodMotion
from src.atlascloud_comfyui.nodes.video.atlascloud_studio_trend_remix import AtlasStudioTrendRemix
from src.atlascloud_comfyui.nodes.video.atlascloud_studio_tvc_maker import AtlasStudioTvcMaker
from src.atlascloud_comfyui.nodes.video.atlascloud_studio_ugc_ad import AtlasStudioUgcAd
from src.atlascloud_comfyui.nodes.video.atlascloud_studio_virtual_try_on import (
    AtlasStudioVirtualTryOn,
)

_VIDEO_CLASSES = [
    AtlasWan30TextToVideo,
    AtlasWan30ImageToVideo,
    AtlasWan30ReferenceToVideo,
    AtlasStudioFoodMotion,
    AtlasStudioVirtualTryOn,
    AtlasStudioUgcAd,
    AtlasStudioTrendRemix,
    AtlasStudioTvcMaker,
]

_WAN30_CLASSES = [AtlasWan30TextToVideo, AtlasWan30ImageToVideo, AtlasWan30ReferenceToVideo]

_STUDIO_VIDEO_CLASSES = [
    AtlasStudioFoodMotion,
    AtlasStudioVirtualTryOn,
    AtlasStudioUgcAd,
    AtlasStudioTrendRemix,
    AtlasStudioTvcMaker,
]


@pytest.mark.parametrize("cls", _VIDEO_CLASSES)
def test_video_node_shape(cls):
    inputs = cls.INPUT_TYPES()
    assert "atlas_client" in inputs["required"]
    assert "poll_interval_sec" in inputs["optional"]
    assert "timeout_sec" in inputs["optional"]
    assert cls.RETURN_TYPES == ("STRING", "STRING")
    assert cls.RETURN_NAMES == ("video_url", "prediction_id")
    assert cls.CATEGORY == "AtlasCloud/Video"
    assert cls.FUNCTION == "run"


@pytest.mark.parametrize("cls", _WAN30_CLASSES)
def test_wan30_common_options(cls):
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


def test_wan30_t2v_metadata():
    inputs = AtlasWan30TextToVideo.INPUT_TYPES()
    assert "prompt" in inputs["required"]
    ratio = inputs["optional"]["ratio"]
    assert ratio[0] == ["adaptive", "16:9", "4:3", "1:1", "3:4", "9:16"]
    assert ratio[1]["default"] == "adaptive"


@pytest.mark.parametrize("bad_prompt", ["", "   "])
def test_wan30_t2v_requires_prompt(bad_prompt):
    with pytest.raises(RuntimeError, match="prompt is required"):
        AtlasWan30TextToVideo().run(None, bad_prompt)


def test_wan30_i2v_metadata():
    inputs = AtlasWan30ImageToVideo.INPUT_TYPES()
    assert "prompt" in inputs["required"]
    assert "image" in inputs["required"]
    assert "last_image" in inputs["optional"]
    # image-to-video derives the aspect ratio from the first frame.
    assert "ratio" not in inputs["optional"]


def test_wan30_i2v_requires_prompt():
    with pytest.raises(RuntimeError, match="prompt is required"):
        AtlasWan30ImageToVideo().run(None, "  ", "https://example.com/a.png")


@pytest.mark.parametrize("bad_image", ["", "   "])
def test_wan30_i2v_requires_image(bad_image):
    with pytest.raises(RuntimeError, match="image is required"):
        AtlasWan30ImageToVideo().run(None, "a prompt", bad_image)


def test_wan30_i2v_omits_empty_last_image():
    source = inspect.getsource(AtlasWan30ImageToVideo.run)
    assert 'payload["last_image"] = li' in source


def test_wan30_r2v_metadata():
    inputs = AtlasWan30ReferenceToVideo.INPUT_TYPES()
    assert "prompt" in inputs["required"]
    assert "reference_images" in inputs["required"]
    optional = inputs["optional"]
    assert "reference_videos" in optional
    assert "reference_audios" in optional
    assert optional["enable_thinking"][1]["default"] is True


def test_wan30_r2v_requires_prompt():
    with pytest.raises(RuntimeError, match="prompt is required"):
        AtlasWan30ReferenceToVideo().run(None, " ", "https://example.com/a.png")


@pytest.mark.parametrize("bad_refs", ["", "  \n \n"])
def test_wan30_r2v_requires_at_least_one_reference(bad_refs):
    with pytest.raises(RuntimeError, match="at least one reference"):
        AtlasWan30ReferenceToVideo().run(None, "a prompt", bad_refs)


def test_wan30_r2v_rejects_too_many_images():
    urls = "\n".join(f"https://example.com/{i}.png" for i in range(11))
    with pytest.raises(RuntimeError, match="reference_images maxItems is 10"):
        AtlasWan30ReferenceToVideo().run(None, "a prompt", urls)


def test_wan30_r2v_rejects_too_many_videos():
    urls = "\n".join(f"https://example.com/{i}.mp4" for i in range(6))
    with pytest.raises(RuntimeError, match="reference_videos maxItems is 5"):
        AtlasWan30ReferenceToVideo().run(None, "a prompt", "", urls)


def test_wan30_r2v_rejects_too_many_audios():
    urls = "\n".join(f"https://example.com/{i}.mp3" for i in range(6))
    with pytest.raises(RuntimeError, match="reference_audios maxItems is 5"):
        AtlasWan30ReferenceToVideo().run(None, "a prompt", "", "", urls)


def test_wan30_r2v_tags_refers_by_kind():
    source = inspect.getsource(AtlasWan30ReferenceToVideo.run)
    for kind in ("image", "video", "audio"):
        assert f'"type": "{kind}"' in source


@pytest.mark.parametrize("cls", _STUDIO_VIDEO_CLASSES)
def test_studio_video_common_options(cls):
    optional = cls.INPUT_TYPES()["optional"]
    assert optional["resolution"][0] == ["480p", "720p", "720p-esr", "1080p-esr", "1440p-esr", "4k-esr"]
    assert optional["resolution"][1]["default"] == "720p"
    assert optional["generate_audio"][0] == ["yes", "no"]
    assert optional["generate_audio"][1]["default"] == "yes"
    assert optional["count"][1]["min"] == 1
    assert optional["count"][1]["max"] == 2


@pytest.mark.parametrize("cls", _STUDIO_VIDEO_CLASSES)
def test_studio_video_requires_product_image(cls):
    inputs = cls.INPUT_TYPES()
    assert "product_image" in inputs["required"]
    assert "user_prompt" in inputs["required"]


def test_studio_food_motion_requires_inputs():
    with pytest.raises(RuntimeError, match="product_image is required"):
        AtlasStudioFoodMotion().run(None, "  ", "a prompt")
    with pytest.raises(RuntimeError, match="user_prompt is required"):
        AtlasStudioFoodMotion().run(None, "https://example.com/a.png", " ")


def test_studio_virtual_try_on_requires_inputs():
    with pytest.raises(RuntimeError, match="product_image is required"):
        AtlasStudioVirtualTryOn().run(None, "", "a prompt")
    with pytest.raises(RuntimeError, match="user_prompt is required"):
        AtlasStudioVirtualTryOn().run(None, "https://example.com/a.png", "")
    # Fashion clips default to vertical.
    assert AtlasStudioVirtualTryOn.INPUT_TYPES()["optional"]["ratio"][1]["default"] == "9:16"


def test_studio_ugc_ad_metadata_and_validation():
    optional = AtlasStudioUgcAd.INPUT_TYPES()["optional"]
    assert optional["ad_type"][0] == ["creator_recommendation", "before_after", "unboxing"]
    assert optional["ad_type"][1]["default"] == "creator_recommendation"
    assert optional["ratio"][1]["default"] == "9:16"
    with pytest.raises(RuntimeError, match="product_image is required"):
        AtlasStudioUgcAd().run(None, "", "a prompt")
    with pytest.raises(RuntimeError, match="user_prompt is required"):
        AtlasStudioUgcAd().run(None, "https://example.com/a.png", "")


def test_studio_trend_remix_requires_reference_video():
    inputs = AtlasStudioTrendRemix.INPUT_TYPES()
    assert "reference_video" in inputs["required"]
    # 0 means "match the reference video length" and is sent as an omitted duration.
    assert inputs["optional"]["duration"][1]["default"] == 0
    with pytest.raises(RuntimeError, match="product_image is required"):
        AtlasStudioTrendRemix().run(None, "", "https://example.com/v.mp4", "a prompt")
    with pytest.raises(RuntimeError, match="reference_video is required"):
        AtlasStudioTrendRemix().run(None, "https://example.com/a.png", "  ", "a prompt")
    with pytest.raises(RuntimeError, match="user_prompt is required"):
        AtlasStudioTrendRemix().run(None, "https://example.com/a.png", "https://example.com/v.mp4", "")


def test_studio_trend_remix_omits_auto_duration():
    source = inspect.getsource(AtlasStudioTrendRemix.run)
    assert "if int(duration) > 0:" in source


def test_studio_tvc_maker_metadata_and_validation():
    optional = AtlasStudioTvcMaker.INPUT_TYPES()["optional"]
    assert optional["duration"][1]["min"] == 4
    assert optional["duration"][1]["max"] == 30
    with pytest.raises(RuntimeError, match="product_image is required"):
        AtlasStudioTvcMaker().run(None, "", "a prompt")
    with pytest.raises(RuntimeError, match="user_prompt is required"):
        AtlasStudioTvcMaker().run(None, "https://example.com/a.png", "")


def test_studio_product_visuals_metadata():
    inputs = AtlasStudioProductVisuals.INPUT_TYPES()
    required = inputs["required"]
    optional = inputs["optional"]
    assert "product_image" in required
    assert "user_prompt" in required
    assert optional["visual_type"][0] == ["product_hero", "product_detail", "promo_poster"]
    assert optional["visual_type"][1]["default"] == "product_hero"
    assert optional["resolution"][0] == ["1k", "2k", "4k"]
    assert optional["resolution"][1]["default"] == "2k"
    assert optional["format"][0] == ["png", "jpeg"]
    assert optional["count"][1]["max"] == 4
    assert AtlasStudioProductVisuals.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasStudioProductVisuals.RETURN_NAMES == ("image_url", "prediction_id")
    assert AtlasStudioProductVisuals.CATEGORY == "AtlasCloud/Image"


def test_studio_product_visuals_validation():
    with pytest.raises(RuntimeError, match="product_image is required"):
        AtlasStudioProductVisuals().run(None, "  ", "a prompt")
    with pytest.raises(RuntimeError, match="user_prompt is required"):
        AtlasStudioProductVisuals().run(None, "https://example.com/a.png", " ")


def test_new_nodes_2026_08_24_registered():
    from src.atlascloud_comfyui.registry import (
        NODE_CLASS_MAPPINGS,
        NODE_DISPLAY_NAME_MAPPINGS,
    )

    keys = [
        "AtlasCloud WAN3.0 Text-to-Video",
        "AtlasCloud WAN3.0 Image-to-Video",
        "AtlasCloud WAN3.0 Reference-to-Video",
        "AtlasCloud Studio Product Visuals",
        "AtlasCloud Studio Food Motion",
        "AtlasCloud Studio Virtual Try-On",
        "AtlasCloud Studio UGC Ad",
        "AtlasCloud Studio Trend Remix",
        "AtlasCloud Studio TVC Maker",
    ]
    for key in keys:
        assert key in NODE_CLASS_MAPPINGS
        assert key in NODE_DISPLAY_NAME_MAPPINGS


def test_new_nodes_2026_08_24_model_ids():
    expected = [
        (AtlasWan30TextToVideo, "alibaba/wan-3.0/text-to-video"),
        (AtlasWan30ImageToVideo, "alibaba/wan-3.0/image-to-video"),
        (AtlasWan30ReferenceToVideo, "alibaba/wan-3.0/reference-to-video"),
        (AtlasStudioProductVisuals, "atlascloud/studio/product-visuals"),
        (AtlasStudioFoodMotion, "atlascloud/studio/food-motion"),
        (AtlasStudioVirtualTryOn, "atlascloud/studio/virtual-try-on"),
        (AtlasStudioUgcAd, "atlascloud/studio/ugc-ad"),
        (AtlasStudioTrendRemix, "atlascloud/studio/trend-remix"),
        (AtlasStudioTvcMaker, "atlascloud/studio/tvc-maker"),
    ]
    for cls, model_id in expected:
        source = inspect.getsource(cls.run)
        assert f'"model": "{model_id}"' in source
