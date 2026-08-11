"""Metadata-only tests for newly added nodes (2026-08-11).

New models: xAI Grok Imagine Image 2.0 (text-to-image, edit).
These tests MUST NOT require ATLASCLOUD_API_KEY.
"""

import inspect

import pytest

_T2I_RATIOS = ["1:1", "3:4", "4:3", "9:16", "16:9", "2:3", "3:2", "9:19.5", "19.5:9", "9:20", "20:9", "1:2", "2:1"]


def _grok_image_20_common_assertions(cls):
    inputs = cls.INPUT_TYPES()
    required = inputs["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert required["resolution"][0] == ["1k", "2k"]
    assert required["resolution"][1]["default"] == "1k"
    assert required["quality"][0] == ["low", "medium"]
    assert required["quality"][1]["default"] == "medium"
    assert required["num_images"][0] == [1, 2, 3, 4]
    assert required["enable_base64_output"][0] == "BOOLEAN"
    assert "poll_interval_sec" in inputs["optional"]
    assert "timeout_sec" in inputs["optional"]
    assert cls.RETURN_TYPES == ("STRING", "STRING")
    assert cls.RETURN_NAMES == ("image_url", "prediction_id")
    assert cls.CATEGORY == "AtlasCloud/Image"


def test_grok_imagine_image_20_t2i_metadata():
    from src.atlascloud_comfyui.nodes.image.xai_grok_imagine_image_20_t2i import (
        AtlasGrokImagineImage20TextToImage,
    )

    _grok_image_20_common_assertions(AtlasGrokImagineImage20TextToImage)
    inputs = AtlasGrokImagineImage20TextToImage.INPUT_TYPES()
    assert inputs["required"]["aspect_ratio"][0] == _T2I_RATIOS
    assert inputs["required"]["aspect_ratio"][1]["default"] == "1:1"


def test_grok_imagine_image_20_edit_metadata():
    from src.atlascloud_comfyui.nodes.image.xai_grok_imagine_image_20_edit import (
        AtlasGrokImagineImage20Edit,
    )

    _grok_image_20_common_assertions(AtlasGrokImagineImage20Edit)
    inputs = AtlasGrokImagineImage20Edit.INPUT_TYPES()
    assert "image_urls" in inputs["required"]
    # The edit endpoint adds an "auto" ratio on top of the text-to-image set.
    assert inputs["required"]["aspect_ratio"][0] == ["auto"] + _T2I_RATIOS
    assert inputs["required"]["aspect_ratio"][1]["default"] == "auto"


@pytest.mark.parametrize("bad_urls", ["", "   ", "\n  \n"])
def test_grok_imagine_image_20_edit_requires_image_urls(bad_urls):
    from src.atlascloud_comfyui.nodes.image.xai_grok_imagine_image_20_edit import (
        AtlasGrokImagineImage20Edit,
    )

    with pytest.raises(RuntimeError, match="image_urls is required"):
        AtlasGrokImagineImage20Edit().run(None, "edit it", bad_urls, "1k", "medium", "auto", 1, False)


def test_grok_imagine_image_20_edit_rejects_more_than_three_images():
    from src.atlascloud_comfyui.nodes.image.xai_grok_imagine_image_20_edit import (
        AtlasGrokImagineImage20Edit,
    )

    urls = "\n".join(f"https://example.com/{i}.png" for i in range(4))
    with pytest.raises(RuntimeError, match="maxItems is 3"):
        AtlasGrokImagineImage20Edit().run(None, "edit it", urls, "1k", "medium", "auto", 1, False)


def test_new_nodes_2026_08_11_registered():
    from src.atlascloud_comfyui.registry import (
        NODE_CLASS_MAPPINGS,
        NODE_DISPLAY_NAME_MAPPINGS,
    )

    keys = [
        "AtlasCloud Grok Imagine Image 2.0 Text-to-Image",
        "AtlasCloud Grok Imagine Image 2.0 Edit",
    ]
    for key in keys:
        assert key in NODE_CLASS_MAPPINGS
        assert key in NODE_DISPLAY_NAME_MAPPINGS


def test_new_nodes_2026_08_11_model_ids():
    from src.atlascloud_comfyui.nodes.image.xai_grok_imagine_image_20_edit import (
        AtlasGrokImagineImage20Edit,
    )
    from src.atlascloud_comfyui.nodes.image.xai_grok_imagine_image_20_t2i import (
        AtlasGrokImagineImage20TextToImage,
    )

    expected = [
        (AtlasGrokImagineImage20TextToImage, "xai/grok-imagine-image-2.0/text-to-image"),
        (AtlasGrokImagineImage20Edit, "xai/grok-imagine-image-2.0/edit"),
    ]
    for cls, model_id in expected:
        source = inspect.getsource(cls.run)
        assert f'"model": "{model_id}"' in source
        assert '"quality": quality' in source
