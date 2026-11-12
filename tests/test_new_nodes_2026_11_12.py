"""Tests for nodes added/updated on 2026-11-12.

New models: Seedream V5.5 (text-to-image, edit, layer decomposition), Seedream V5.0 Flash
(text-to-image, edit, layer decomposition) and Seedance 2.5 Draft Complete.
Updated: Seedance 2.5 draft/resolution options, Seedream V5.0 Pro thinking options.
These tests MUST NOT require ATLASCLOUD_API_KEY.
"""

from unittest.mock import MagicMock

import pytest

from src.atlascloud_comfyui.nodes.image.seedream_v50_flash_edit import AtlasSeedreamV50FlashEdit
from src.atlascloud_comfyui.nodes.image.seedream_v50_flash_layer_decomposition import AtlasSeedreamV50FlashLayerDecomposition
from src.atlascloud_comfyui.nodes.image.seedream_v50_flash_t2i import AtlasSeedreamV50FlashTextToImage
from src.atlascloud_comfyui.nodes.image.seedream_v50_pro_t2i import AtlasSeedreamV50ProTextToImage
from src.atlascloud_comfyui.nodes.image.seedream_v55_edit import AtlasSeedreamV55Edit
from src.atlascloud_comfyui.nodes.image.seedream_v55_layer_decomposition import AtlasSeedreamV55LayerDecomposition
from src.atlascloud_comfyui.nodes.image.seedream_v55_t2i import AtlasSeedreamV55TextToImage
from src.atlascloud_comfyui.nodes.video.bytedance_seedance_2_5_draft_complete import AtlasSeedance25DraftComplete
from src.atlascloud_comfyui.nodes.video.bytedance_seedance_2_5_r2v import AtlasSeedance25ReferenceToVideo
from src.atlascloud_comfyui.nodes.video.bytedance_seedance_2_5_t2v import AtlasSeedance25TextToVideo


def _mock_handle(outputs):
    handle = MagicMock()
    handle.client.generate_image.return_value = "pred_img"
    handle.client.generate_video.return_value = "pred_vid"
    handle.client.poll_prediction.return_value = {"data": {"outputs": outputs}}
    return handle


@pytest.mark.parametrize(
    "cls",
    [
        AtlasSeedreamV55TextToImage,
        AtlasSeedreamV55Edit,
        AtlasSeedreamV55LayerDecomposition,
        AtlasSeedreamV50FlashTextToImage,
        AtlasSeedreamV50FlashEdit,
        AtlasSeedreamV50FlashLayerDecomposition,
    ],
)
def test_new_seedream_metadata(cls):
    required = cls.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert required["seed"][0] == "INT"
    assert required["seed"][1]["control_after_generate"] is True
    assert cls.CATEGORY == "AtlasCloud/Image"
    assert cls.RETURN_TYPES[0] == "STRING"


def test_seedream_v55_t2i_payload():
    handle = _mock_handle(["http://example.com/out.png"])
    url, pred = AtlasSeedreamV55TextToImage().run(
        handle, prompt="a fox", seed=5, size="1568*672", output_format="png", background="transparent", enable_base64_output=False
    )
    assert (url, pred) == ("http://example.com/out.png", "pred_img")
    payload = handle.client.generate_image.call_args[0][0]
    assert payload == {
        "model": "bytedance/seedream-v5.5/text-to-image",
        "prompt": "a fox",
        "size": "1568*672",
        "output_format": "png",
        "background": "transparent",
        "enable_base64_output": False,
    }


def test_seedream_v55_edit_sends_reference_images():
    handle = _mock_handle(["http://example.com/out.png"])
    AtlasSeedreamV55Edit().run(
        handle,
        reference_images="http://a.png\n\nhttp://b.png",
        prompt="swap the sky",
        seed=1,
        size="2048*2048",
        output_format="png",
        background="auto",
        enable_base64_output=False,
    )
    payload = handle.client.generate_image.call_args[0][0]
    assert payload["model"] == "bytedance/seedream-v5.5/edit"
    assert payload["reference_images"] == ["http://a.png", "http://b.png"]
    assert "seed" not in payload


@pytest.mark.parametrize("cls,key", [(AtlasSeedreamV55Edit, "reference_images"), (AtlasSeedreamV50FlashEdit, "images")])
def test_new_seedream_edit_requires_images(cls, key):
    kwargs = {key: "  ", "prompt": "x", "seed": 0, "size": "2048*2048", "output_format": "png", "background": "opaque", "enable_base64_output": False}
    with pytest.raises(RuntimeError, match=f"{key} is required"):
        cls().run(None, **kwargs)


def test_seedream_v55_layer_decomposition_payload():
    handle = _mock_handle(["http://base.png", "http://l1.png", "http://l2.png"])
    base, layers, pred = AtlasSeedreamV55LayerDecomposition().run(
        handle,
        image="http://src.png",
        seed=0,
        resolution="2k",
        num_images=10,
        enable_text_recognition=True,
        output_format="png",
        enable_base64_output=False,
    )
    assert base == "http://base.png"
    assert layers == "http://l1.png\nhttp://l2.png"
    payload = handle.client.generate_image.call_args[0][0]
    assert payload["model"] == "bytedance/seedream-v5.5/layer-decomposition"
    assert payload["resolution"] == "2k"
    assert payload["num_images"] == 10
    assert payload["enable_text_recognition"] is True
    assert "prompt" not in payload


def test_seedream_v50_flash_layer_decomposition_requires_image():
    with pytest.raises(RuntimeError, match="image is required"):
        AtlasSeedreamV50FlashLayerDecomposition().run(None, image="", seed=0, size="auto", output_format="jpeg", enable_base64_output=False)


def test_seedream_v50_pro_t2i_thinking_options():
    optional = AtlasSeedreamV50ProTextToImage.INPUT_TYPES()["optional"]
    assert optional["thinking"][0] == ["enabled", "disabled"]
    assert optional["prompt_optimization_mode"][0] == ["standard", "fast"]


def test_seedance_25_draft_only_sent_when_enabled():
    handle = _mock_handle(["http://example.com/out.mp4"])
    AtlasSeedance25TextToVideo().run(handle, "a cat")
    assert "draft" not in handle.client.generate_video.call_args[0][0]

    AtlasSeedance25TextToVideo().run(handle, "a cat", draft=True)
    assert handle.client.generate_video.call_args[0][0]["draft"] is True


def test_seedance_25_r2v_accepts_audio_only_reference():
    handle = _mock_handle(["http://example.com/out.mp4"])
    AtlasSeedance25ReferenceToVideo().run(handle, "", "", reference_audios="http://beat.mp3")
    payload = handle.client.generate_video.call_args[0][0]
    assert payload["reference_audios"] == ["http://beat.mp3"]
    assert "omni_reference_task_type" not in payload


def test_seedance_25_draft_complete_payload():
    handle = _mock_handle(["http://example.com/final.mp4"])
    url, pred = AtlasSeedance25DraftComplete().run(handle, " pred_draft ")
    assert (url, pred) == ("http://example.com/final.mp4", "pred_vid")
    assert handle.client.generate_video.call_args[0][0] == {
        "model": "bytedance/seedance-2.5/draft-complete",
        "draft_id": "pred_draft",
        "watermark": False,
        "return_last_frame": False,
        "output_format": "mp4",
    }


def test_seedance_25_draft_complete_requires_draft_id():
    with pytest.raises(RuntimeError, match="draft_id is required"):
        AtlasSeedance25DraftComplete().run(None, "  ")


def test_new_nodes_2026_11_12_registered():
    from src.atlascloud_comfyui.registry import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

    expected = {
        "AtlasCloud Seedream V5.5 Text-to-Image": AtlasSeedreamV55TextToImage,
        "AtlasCloud Seedream V5.5 Edit": AtlasSeedreamV55Edit,
        "AtlasCloud Seedream V5.5 Layer Decomposition": AtlasSeedreamV55LayerDecomposition,
        "AtlasCloud Seedream V5.0 Flash Text-to-Image": AtlasSeedreamV50FlashTextToImage,
        "AtlasCloud Seedream V5.0 Flash Edit": AtlasSeedreamV50FlashEdit,
        "AtlasCloud Seedream V5.0 Flash Layer Decomposition": AtlasSeedreamV50FlashLayerDecomposition,
        "AtlasCloud Seedance 2.5 Draft Complete": AtlasSeedance25DraftComplete,
    }
    for name, cls in expected.items():
        assert NODE_CLASS_MAPPINGS[name].__name__ == cls.__name__
        assert NODE_DISPLAY_NAME_MAPPINGS[name] == name
