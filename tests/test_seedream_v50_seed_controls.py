import pytest
from unittest.mock import MagicMock

from src.atlascloud_comfyui.nodes.image.seedream_v50_lite_edit import AtlasSeedreamV50LiteEdit
from src.atlascloud_comfyui.nodes.image.seedream_v50_lite_edit_sequential import AtlasSeedreamV50LiteEditSequential
from src.atlascloud_comfyui.nodes.image.seedream_v50_lite_sequential_t2i import AtlasSeedreamV50LiteSequentialTextToImage
from src.atlascloud_comfyui.nodes.image.seedream_v50_lite_t2i import AtlasSeedreamV50LiteTextToImage
from src.atlascloud_comfyui.nodes.image.seedream_v50_pro_edit import AtlasSeedreamV50ProEdit
from src.atlascloud_comfyui.nodes.image.seedream_v50_pro_layer_decomposition import AtlasSeedreamV50ProLayerDecomposition
from src.atlascloud_comfyui.nodes.image.seedream_v50_pro_t2i import AtlasSeedreamV50ProTextToImage


SEEDREAM_V50_NODE_CLASSES = [
    AtlasSeedreamV50LiteEdit,
    AtlasSeedreamV50LiteEditSequential,
    AtlasSeedreamV50LiteSequentialTextToImage,
    AtlasSeedreamV50LiteTextToImage,
    AtlasSeedreamV50ProEdit,
    AtlasSeedreamV50ProLayerDecomposition,
    AtlasSeedreamV50ProTextToImage,
]


@pytest.mark.parametrize("node_cls", SEEDREAM_V50_NODE_CLASSES)
def test_seedream_v50_seed_input_spec(node_cls):
    input_types = node_cls.INPUT_TYPES()
    assert "seed" in input_types["required"]
    seed_spec = input_types["required"]["seed"]

    assert seed_spec[0] == "INT"
    options = seed_spec[1]
    assert options.get("default") == 0
    assert options.get("min") == 0
    assert options.get("max") == 0xFFFFFFFFFFFFFFFF
    assert options.get("control_after_generate") is True
    assert options.get("tooltip") == "Change to run the node again (not sent to the API)"


def test_seedream_v50_lite_edit_payload_omits_seed():
    mock_handle = MagicMock()
    mock_client = MagicMock()
    mock_handle.client = mock_client
    mock_client.generate_image.return_value = "pred_123"
    mock_client.poll_prediction.return_value = {"data": {"outputs": ["http://example.com/out.png"]}}

    node = AtlasSeedreamV50LiteEdit()
    url, pred_id = node.run(
        mock_handle,
        image="http://example.com/input.png",
        prompt="A photo of a cat",
        seed=1234567890123456789,
        width=1024,
        height=1024,
        enable_base64_output=False,
    )

    assert url == "http://example.com/out.png"
    assert pred_id == "pred_123"
    mock_client.generate_image.assert_called_once()
    payload = mock_client.generate_image.call_args[0][0]
    assert "seed" not in payload
    assert payload["model"] == "bytedance/seedream-v5.0-lite/edit"


def test_seedream_v50_lite_edit_sequential_payload_omits_seed():
    mock_handle = MagicMock()
    mock_client = MagicMock()
    mock_handle.client = mock_client
    mock_client.generate_image.return_value = "pred_seq_1"
    mock_client.poll_prediction.return_value = {"data": {"outputs": ["http://example.com/seq_out.png"]}}

    node = AtlasSeedreamV50LiteEditSequential()
    url, pred_id = node.run(
        mock_handle,
        prompt="Sequential edit prompt",
        images="http://example.com/img1.png\nhttp://example.com/img2.png",
        seed=987654321,
        size="2048*2048",
        max_images=2,
        output_format="png",
    )

    assert url == "http://example.com/seq_out.png"
    assert pred_id == "pred_seq_1"
    payload = mock_client.generate_image.call_args[0][0]
    assert "seed" not in payload
    assert payload["model"] == "bytedance/seedream-v5.0-lite/edit-sequential"


def test_seedream_v50_lite_sequential_t2i_payload_omits_seed():
    mock_handle = MagicMock()
    mock_client = MagicMock()
    mock_handle.client = mock_client
    mock_client.generate_image.return_value = "pred_seq_t2i"
    mock_client.poll_prediction.return_value = {"data": {"outputs": ["http://example.com/seq_t2i.png"]}}

    node = AtlasSeedreamV50LiteSequentialTextToImage()
    url, pred_id = node.run(
        mock_handle,
        prompt="Sequential t2i prompt",
        seed=42,
        size="2048*2048",
        max_images=1,
        output_format="jpeg",
    )

    assert url == "http://example.com/seq_t2i.png"
    assert pred_id == "pred_seq_t2i"
    payload = mock_client.generate_image.call_args[0][0]
    assert "seed" not in payload
    assert payload["model"] == "bytedance/seedream-v5.0-lite/sequential"


def test_seedream_v50_lite_t2i_payload_omits_seed():
    mock_handle = MagicMock()
    mock_client = MagicMock()
    mock_handle.client = mock_client
    mock_client.generate_image.return_value = "pred_lite_t2i"
    mock_client.poll_prediction.return_value = {"data": {"outputs": ["http://example.com/lite_t2i.png"]}}

    node = AtlasSeedreamV50LiteTextToImage()
    url, pred_id = node.run(
        mock_handle,
        prompt="Lite t2i prompt",
        seed=9999,
        width=1024,
        height=1024,
        enable_base64_output=False,
    )

    assert url == "http://example.com/lite_t2i.png"
    assert pred_id == "pred_lite_t2i"
    payload = mock_client.generate_image.call_args[0][0]
    assert "seed" not in payload
    assert payload["model"] == "bytedance/seedream-v5.0-lite"


def test_seedream_v50_pro_edit_payload_omits_seed():
    mock_handle = MagicMock()
    mock_client = MagicMock()
    mock_handle.client = mock_client
    mock_client.generate_image.return_value = "pred_pro_edit"
    mock_client.poll_prediction.return_value = {"data": {"outputs": ["http://example.com/pro_edit.png"]}}

    node = AtlasSeedreamV50ProEdit()
    url, pred_id = node.run(
        mock_handle,
        images="http://example.com/img1.png",
        prompt="Pro edit prompt",
        seed=777,
        size="2048*2048",
        output_format="jpeg",
        enable_base64_output=False,
    )

    assert url == "http://example.com/pro_edit.png"
    assert pred_id == "pred_pro_edit"
    payload = mock_client.generate_image.call_args[0][0]
    assert "seed" not in payload
    assert payload["model"] == "bytedance/seedream-v5.0-pro/edit"


def test_seedream_v50_pro_layer_decomposition_payload_omits_seed():
    mock_handle = MagicMock()
    mock_client = MagicMock()
    mock_handle.client = mock_client
    mock_client.generate_image.return_value = "pred_layer"
    mock_client.poll_prediction.return_value = {
        "data": {"outputs": ["http://example.com/base.png", "http://example.com/layer1.png"]}
    }

    node = AtlasSeedreamV50ProLayerDecomposition()
    base_url, layer_urls, pred_id = node.run(
        mock_handle,
        image="http://example.com/source.png",
        seed=55555,
        size="auto",
        output_format="jpeg",
        enable_base64_output=False,
        prompt="foreground layer",
    )

    assert base_url == "http://example.com/base.png"
    assert layer_urls == "http://example.com/layer1.png"
    assert pred_id == "pred_layer"
    payload = mock_client.generate_image.call_args[0][0]
    assert "seed" not in payload
    assert payload["model"] == "bytedance/seedream-v5.0-pro/layer-decomposition"
    assert payload["prompt"] == "foreground layer"


def test_seedream_v50_pro_t2i_payload_omits_seed():
    mock_handle = MagicMock()
    mock_client = MagicMock()
    mock_handle.client = mock_client
    mock_client.generate_image.return_value = "pred_pro_t2i"
    mock_client.poll_prediction.return_value = {"data": {"outputs": ["http://example.com/pro_t2i.png"]}}

    node = AtlasSeedreamV50ProTextToImage()
    url, pred_id = node.run(
        mock_handle,
        prompt="Pro t2i prompt",
        seed=1000000000000,
        size="2048*2048",
        output_format="png",
        enable_base64_output=False,
    )

    assert url == "http://example.com/pro_t2i.png"
    assert pred_id == "pred_pro_t2i"
    payload = mock_client.generate_image.call_args[0][0]
    assert "seed" not in payload
    assert payload["model"] == "bytedance/seedream-v5.0-pro/text-to-image"
