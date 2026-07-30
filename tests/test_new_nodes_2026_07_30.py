"""Metadata-only tests for newly added nodes (2026-07-30).

New model: Wan 2.7 Spicy Reference-to-Video.
These tests MUST NOT require ATLASCLOUD_API_KEY.
"""

import inspect

import pytest


def test_wan27_spicy_r2v_metadata():
    from src.atlascloud_comfyui.nodes.video.atlascloud_wan_2_7_spicy_r2v import (
        AtlasWan27SpicyReferenceToVideo,
    )

    inputs = AtlasWan27SpicyReferenceToVideo.INPUT_TYPES()
    required = inputs["required"]
    optional = inputs["optional"]
    assert "atlas_client" in required
    assert "reference_images" in required
    assert "prompt" in required
    assert optional["resolution"][0] == ["720P", "1080P", "1080P-SR", "1440P-SR"]
    assert optional["aspect_ratio"][0] == ["auto", "16:9", "9:16", "4:3", "3:4", "1:1"]
    assert optional["duration"][1]["min"] == 2
    assert optional["duration"][1]["max"] == 15
    assert AtlasWan27SpicyReferenceToVideo.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasWan27SpicyReferenceToVideo.RETURN_NAMES == ("video_url", "prediction_id")
    assert AtlasWan27SpicyReferenceToVideo.CATEGORY == "AtlasCloud/Video"


@pytest.mark.parametrize("bad_images", ["", "   \n  \n"])
def test_wan27_spicy_r2v_requires_reference_images(bad_images):
    from src.atlascloud_comfyui.nodes.video.atlascloud_wan_2_7_spicy_r2v import (
        AtlasWan27SpicyReferenceToVideo,
    )

    with pytest.raises(RuntimeError, match="reference_images is required"):
        AtlasWan27SpicyReferenceToVideo().run(None, bad_images, "a prompt")


def test_wan27_spicy_r2v_rejects_more_than_four_images():
    from src.atlascloud_comfyui.nodes.video.atlascloud_wan_2_7_spicy_r2v import (
        AtlasWan27SpicyReferenceToVideo,
    )

    images = "\n".join(f"https://example.com/{i}.png" for i in range(5))
    with pytest.raises(RuntimeError, match="At most 4 reference images"):
        AtlasWan27SpicyReferenceToVideo().run(None, images, "a prompt")


def test_wan27_spicy_r2v_requires_prompt():
    from src.atlascloud_comfyui.nodes.video.atlascloud_wan_2_7_spicy_r2v import (
        AtlasWan27SpicyReferenceToVideo,
    )

    with pytest.raises(RuntimeError, match="prompt is required"):
        AtlasWan27SpicyReferenceToVideo().run(None, "https://example.com/1.png", "   ")


def test_new_nodes_2026_07_30_registered():
    from src.atlascloud_comfyui.registry import (
        NODE_CLASS_MAPPINGS,
        NODE_DISPLAY_NAME_MAPPINGS,
    )

    key = "AtlasCloud WAN2.7 Spicy Reference-to-Video"
    assert key in NODE_CLASS_MAPPINGS
    assert key in NODE_DISPLAY_NAME_MAPPINGS


def test_new_nodes_2026_07_30_model_ids():
    from src.atlascloud_comfyui.nodes.video.atlascloud_wan_2_7_spicy_r2v import (
        AtlasWan27SpicyReferenceToVideo,
    )

    source = inspect.getsource(AtlasWan27SpicyReferenceToVideo.run)
    assert '"model": "atlascloud/wan-2.7-spicy/reference-to-video"' in source
