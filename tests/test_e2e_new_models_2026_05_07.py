"""End-to-end (opt-in) smoke tests for nodes added on 2026-05-07.

Models:
- atlascloud/wan-2.2-turbo/infinite-image-to-video
- atlascloud/wan-2.2-turbo/infinite-image-to-video-lora
- atlascloud/wan-2.2-turbo-spicy/infinite-image-to-video
- atlascloud/wan-2.2-turbo-spicy/infinite-image-to-video-lora

Notes:
- These tests are optional in CI (skip if no key).
- Infinite I2V models may queue; keep this suite opt-in to avoid hangs.

Run locally (opt-in):
  ATLASCLOUD_API_KEY=... ATLASCLOUD_RUN_WAN22_INFINITE_E2E=1 PYTHONPATH=../ComfyUI \
    pytest tests/test_e2e_new_models_2026_05_07.py -v -s
"""

from __future__ import annotations

import os
import time
import sys

import pytest

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

_HAS_KEY = bool(os.getenv("ATLASCLOUD_API_KEY", "").strip())
_OPT_IN = bool(os.getenv("ATLASCLOUD_RUN_WAN22_INFINITE_E2E", "").strip())

skip_no_key = pytest.mark.skipif(not _HAS_KEY, reason="ATLASCLOUD_API_KEY not set")
skip_no_opt_in = pytest.mark.skipif(
    not _OPT_IN,
    reason="Set ATLASCLOUD_RUN_WAN22_INFINITE_E2E=1 to run (avoid queue/credit hangs by default)",
)

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
        prompt="A clean studio photo of a cute cat plush toy on a white background",
        aspect_ratio="1:1",
        num_images=1,
        enable_base64_output=False,
        poll_interval_sec=2.0,
        timeout_sec=180,
    )
    elapsed = time.time() - start

    print(f"\n  prediction_id: {prediction_id}")
    print(f"  image_url:     {image_url[:120]}...")
    print(f"  elapsed:       {elapsed:.1f}s")

    assert image_url
    _image_url = image_url


@skip_no_key
@skip_no_opt_in
def test_wan22_turbo_infinite_i2v_smoke():
    from atlascloud_comfyui.nodes.video.atlascloud_wan_2_2_turbo_infinite_i2v import (
        AtlasWan22TurboInfiniteImageToVideo,
    )

    if not _image_url:
        pytest.skip("No image available (setup test must run first)")

    node = AtlasWan22TurboInfiniteImageToVideo()
    handle = make_client()

    start = time.time()
    video_url, prediction_id = node.run(
        atlas_client=handle,
        image=_image_url,
        prompt="A cat plush toy slowly rotates\nSoft studio lighting",
        duration=3,
        resolution="480p",
        seed=-1,
        poll_interval_sec=3.0,
        timeout_sec=240,
    )
    elapsed = time.time() - start

    print(f"\n  prediction_id: {prediction_id}")
    print(f"  video_url:     {video_url[:120]}...")
    print(f"  elapsed:       {elapsed:.1f}s")

    assert video_url.startswith("http")


@skip_no_key
@skip_no_opt_in
def test_wan22_turbo_spicy_infinite_i2v_smoke():
    from atlascloud_comfyui.nodes.video.atlascloud_wan_2_2_turbo_spicy_infinite_i2v import (
        AtlasWan22TurboSpicyInfiniteImageToVideo,
    )

    if not _image_url:
        pytest.skip("No image available (setup test must run first)")

    node = AtlasWan22TurboSpicyInfiniteImageToVideo()
    handle = make_client()

    start = time.time()
    video_url, prediction_id = node.run(
        atlas_client=handle,
        image=_image_url,
        prompt="A cat plush toy blinks\nCute stop-motion style",
        duration=3,
        resolution="480p",
        seed=-1,
        poll_interval_sec=3.0,
        timeout_sec=240,
    )
    elapsed = time.time() - start

    print(f"\n  prediction_id: {prediction_id}")
    print(f"  video_url:     {video_url[:120]}...")
    print(f"  elapsed:       {elapsed:.1f}s")

    assert video_url.startswith("http")
