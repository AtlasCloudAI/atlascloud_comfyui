"""Multi-image helper nodes accept up to 30 images (sockets are shown on demand by the web extension)."""

from unittest.mock import MagicMock

import pytest
import torch

from src.atlascloud_comfyui.nodes.utils import multi_image_to_seedance_assets
from src.atlascloud_comfyui.nodes.utils.multi_image_to_base64 import AtlasMultiImageToBase64
from src.atlascloud_comfyui.nodes.utils.multi_image_to_seedance_assets import AtlasMultiImageToSeedanceAssets


@pytest.mark.parametrize("cls", [AtlasMultiImageToBase64, AtlasMultiImageToSeedanceAssets])
def test_declares_thirty_image_inputs(cls):
    optional = cls.INPUT_TYPES()["optional"]
    names = [k for k in optional if k.startswith("image_")]
    assert names == [f"image_{i}" for i in range(1, 31)]
    assert all(optional[n][0] == "IMAGE" for n in names)


def test_base64_collects_images_past_eight():
    img = torch.zeros(1, 4, 4, 3)
    refs, count = AtlasMultiImageToBase64().run(refs="http://a.png", image_9=img, image_30=img)
    lines = refs.splitlines()
    assert count == 3
    assert lines[0] == "http://a.png"
    assert all(line.startswith("data:image/png;base64,") for line in lines[1:])


def test_seedance_assets_collects_images_past_eight(monkeypatch):
    monkeypatch.setattr(multi_image_to_seedance_assets, "_comfy_image_to_png_bytes", lambda img: b"png")
    handle = MagicMock()
    handle.client.upload_media_bytes.return_value = {"download_url": "http://up/x.png"}
    handle.client.register_seedance_asset.return_value = {"id": "a1"}
    handle.client.wait_for_seedance_asset_active.return_value = {"atlas_asset_id": "atlas-1"}

    img = torch.zeros(1, 4, 4, 3)
    refs, count = AtlasMultiImageToSeedanceAssets().run(handle, image_12=img, image_25=img)
    assert count == 2
    assert refs.splitlines() == ["asset://atlas-1", "asset://atlas-1"]
