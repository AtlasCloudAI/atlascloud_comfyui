"""E2E tests for nodes added in 2026-05-08 sync.

Requires ATLASCLOUD_API_KEY environment variable.
Run:
  ATLASCLOUD_API_KEY=... PYTHONPATH=../ComfyUI pytest tests/test_e2e_new_models_2026_05_08.py -v -s

Notes:
- Designed to skip automatically when ATLASCLOUD_API_KEY is not set.
- WAN2.2 Turbo I2V should be fairly fast; keep timeout conservative to avoid hanging.
"""

from __future__ import annotations

import os
import sys
import time

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

_HAS_KEY = bool(os.getenv("ATLASCLOUD_API_KEY", "").strip())
skip_no_key = pytest.mark.skipif(not _HAS_KEY, reason="ATLASCLOUD_API_KEY not set")

from atlascloud_comfyui.client.atlas_client import AtlasClient
from atlascloud_comfyui.nodes.auth.atlas_client_node import AtlasClientHandle


def make_client() -> AtlasClientHandle:
    client = AtlasClient.from_env()
    return AtlasClientHandle(client=client)


_image_url: str | None = None


@skip_no_key
def test_setup_image_fixture_imagen4_fast_t2i():
    """Generate an image that can be used as input for I2V tests."""

    global _image_url

    from atlascloud_comfyui.nodes.image.imagen4_fast_t2i import AtlasImagen4FastTextToImage

    node = AtlasImagen4FastTextToImage()
    handle = make_client()

    start = time.time()
    image_url, prediction_id = node.run(
        atlas_client=handle,
        prompt="A clean studio photo of a toy car on a white background",
        aspect_ratio="1:1",
        num_images=1,
        enable_base64_output=False,
        poll_interval_sec=2.0,
        timeout_sec=240,
    )
    elapsed = time.time() - start

    print(f"\n  prediction_id: {prediction_id}")
    print(f"  image_url:     {image_url[:120]}...")
    print(f"  elapsed:       {elapsed:.1f}s")

    assert prediction_id
    assert image_url

    _image_url = image_url


@skip_no_key
def test_wan22_turbo_i2v_smoke():
    """WAN2.2 Turbo Image-to-Video should return a video URL."""

    image_url = _image_url
    if not image_url:
        pytest.skip("No image available (test_setup_image_fixture_imagen4_fast_t2i must run first)")

    from atlascloud_comfyui.nodes.video.wan22_turbo_i2v import AtlasWan22TurboImageToVideo

    node = AtlasWan22TurboImageToVideo()
    handle = make_client()

    start = time.time()
    video_url, prediction_id = node.run(
        atlas_client=handle,
        image=image_url,
        prompt="The toy car slowly rolls forward on the table, cinematic lighting",
        resolution="720p",
        duration=5,
        seed=-1,
        poll_interval_sec=2.5,
        timeout_sec=600,
    )
    elapsed = time.time() - start

    print(f"\n  prediction_id: {prediction_id}")
    print(f"  video_url:     {video_url[:120]}...")
    print(f"  elapsed:       {elapsed:.1f}s")

    assert prediction_id
    assert video_url
    assert video_url.startswith("http"), video_url[:80]
