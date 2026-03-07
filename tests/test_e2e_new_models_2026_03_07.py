"""End-to-end smoke tests for nodes added on 2026-03-07.

Requires ATLASCLOUD_API_KEY environment variable.
Run:
  ATLASCLOUD_API_KEY=... PYTHONPATH=../ComfyUI pytest tests/test_e2e_new_models_2026_03_07.py -v -s

Notes:
- These tests are designed to be optional in CI (skip if no key).
- Video models can be slow/queue; keep timeouts conservative.
"""

from __future__ import annotations

import os
import time

import pytest

import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

_HAS_KEY = bool(os.getenv("ATLASCLOUD_API_KEY", "").strip())
skip_no_key = pytest.mark.skipif(not _HAS_KEY, reason="ATLASCLOUD_API_KEY not set")

from atlascloud_comfyui.client.atlas_client import AtlasClient
from atlascloud_comfyui.nodes.auth.atlas_client_node import AtlasClientHandle


def make_client() -> AtlasClientHandle:
    client = AtlasClient.from_env()
    return AtlasClientHandle(client=client)


_seedream_v4_image_url: str | None = None


@skip_no_key
def test_seedream_v4_t2i():
    """Seedream V4 text-to-image should return a URL."""
    global _seedream_v4_image_url

    from atlascloud_comfyui.nodes.image.seedream_v4_t2i import AtlasSeedreamV4TextToImage

    node = AtlasSeedreamV4TextToImage()
    handle = make_client()

    start = time.time()
    image_url, prediction_id = node.run(
        atlas_client=handle,
        prompt="A product photo of a glass bottle on a white background",
        size="2048*2048",
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
    assert image_url.startswith("http") or image_url.startswith("data:"), image_url[:80]

    _seedream_v4_image_url = image_url


@skip_no_key
def test_van25_i2v_uses_seedream_image():
    """Van-2.5 image-to-video should work using the Seedream V4 image as input."""
    from atlascloud_comfyui.nodes.video.van25_i2v import AtlasAtlascloudVan25ImageToVideo

    image_url = _seedream_v4_image_url
    if not image_url:
        pytest.skip("No image available (test_seedream_v4_t2i must run first)")

    node = AtlasAtlascloudVan25ImageToVideo()
    handle = make_client()

    start = time.time()
    video_url, prediction_id = node.run(
        atlas_client=handle,
        prompt="The bottle slowly rotates with soft studio lighting",
        image=image_url,
        resolution="720p",
        duration=5,
        enable_prompt_expansion=False,
        seed=-1,
        poll_interval_sec=3.0,
        timeout_sec=600,
    )
    elapsed = time.time() - start

    print(f"\n  prediction_id: {prediction_id}")
    print(f"  video_url:     {video_url[:120]}...")
    print(f"  elapsed:       {elapsed:.1f}s")

    assert prediction_id
    assert video_url
    assert video_url.startswith("http"), video_url[:80]


@skip_no_key
def test_wan25_t2i_smoke():
    """WAN2.5 text-to-image should return a URL."""
    from atlascloud_comfyui.nodes.image.wan25_t2i import AtlasWan25TextToImage

    node = AtlasWan25TextToImage()
    handle = make_client()

    start = time.time()
    image_url, prediction_id = node.run(
        atlas_client=handle,
        prompt="A minimalist icon of a camera on a pastel background",
        size="1024*1024",
        enable_prompt_expansion=False,
        seed=-1,
        poll_interval_sec=2.0,
        timeout_sec=240,
    )
    elapsed = time.time() - start

    print(f"\n  prediction_id: {prediction_id}")
    print(f"  image_url:     {image_url[:120]}...")
    print(f"  elapsed:       {elapsed:.1f}s")

    assert prediction_id
    assert image_url
    assert image_url.startswith("http") or image_url.startswith("data:"), image_url[:80]
