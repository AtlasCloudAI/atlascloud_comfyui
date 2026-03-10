"""End-to-end smoke tests for nodes added on 2026-03-10.

Models:
- vidu/q3-pro/text-to-video
- vidu/q3-pro/image-to-video
- alibaba/wan-2.2-spicy/image-to-video
- alibaba/wan-2.2-spicy/image-to-video-lora

Requires ATLASCLOUD_API_KEY environment variable.

Run locally:
  ATLASCLOUD_API_KEY=... PYTHONPATH=../ComfyUI pytest tests/test_e2e_new_models_2026_03_10.py -v -s

Notes:
- These tests are optional in CI (skip if no key).
- Video models can queue; keep timeouts conservative.
- The LoRA variant test is opt-in (requires user-provided LoRA URLs).
"""

from __future__ import annotations

import os
import time

import pytest

# Add src to path
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

_HAS_KEY = bool(os.getenv("ATLASCLOUD_API_KEY", "").strip())
skip_no_key = pytest.mark.skipif(not _HAS_KEY, reason="ATLASCLOUD_API_KEY not set")

from atlascloud_comfyui.client.atlas_client import AtlasClient
from atlascloud_comfyui.nodes.auth.atlas_client_node import AtlasClientHandle


def make_client() -> AtlasClientHandle:
    client = AtlasClient.from_env()
    return AtlasClientHandle(client=client)


# Reuse an image URL so we don't need local assets.
# Generate it once via an inexpensive T2I model (Imagen4-fast).
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
        prompt="A clean product photo of a sneaker on a white background",
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
    assert image_url.startswith("http") or image_url.startswith("data:"), image_url[:80]

    _image_url = image_url


@skip_no_key
def test_vidu_q3_pro_t2v_smoke():
    """Vidu Q3-Pro text-to-video should return a URL."""

    from atlascloud_comfyui.nodes.video.vidu_q3_pro_t2v import AtlasViduQ3ProTextToVideo

    node = AtlasViduQ3ProTextToVideo()
    handle = make_client()

    start = time.time()
    video_url, prediction_id = node.run(
        atlas_client=handle,
        prompt="A slow cinematic pan across a modern kitchen countertop",
        style="general",
        resolution="540p",
        duration=5,
        aspect_ratio="16:9",
        movement_amplitude="small",
        generate_audio=False,
        bgm=False,
        seed=-1,
        poll_interval_sec=2.5,
        timeout_sec=900,
    )
    elapsed = time.time() - start

    print(f"\n  prediction_id: {prediction_id}")
    print(f"  video_url:     {video_url[:120]}...")
    print(f"  elapsed:       {elapsed:.1f}s")

    assert prediction_id
    assert video_url
    assert video_url.startswith("http"), video_url[:80]


@skip_no_key
def test_vidu_q3_pro_i2v_smoke_uses_generated_image():
    """Vidu Q3-Pro image-to-video should work using the generated image as input."""

    from atlascloud_comfyui.nodes.video.vidu_q3_pro_i2v import AtlasViduQ3ProImageToVideo

    image_url = _image_url
    if not image_url:
        pytest.skip("No image available (test_setup_image_fixture_imagen4_fast_t2i must run first)")

    node = AtlasViduQ3ProImageToVideo()
    handle = make_client()

    start = time.time()
    video_url, prediction_id = node.run(
        atlas_client=handle,
        image=image_url,
        prompt="The camera slowly zooms in, with soft natural lighting",
        resolution="540p",
        duration=5,
        movement_amplitude="small",
        generate_audio=False,
        bgm=False,
        seed=-1,
        poll_interval_sec=2.5,
        timeout_sec=900,
    )
    elapsed = time.time() - start

    print(f"\n  prediction_id: {prediction_id}")
    print(f"  video_url:     {video_url[:120]}...")
    print(f"  elapsed:       {elapsed:.1f}s")

    assert prediction_id
    assert video_url
    assert video_url.startswith("http"), video_url[:80]


@skip_no_key
def test_wan22_spicy_i2v_smoke_uses_generated_image():
    """WAN2.2 Spicy image-to-video should return a URL."""

    from atlascloud_comfyui.nodes.video.wan22_spicy_i2v import AtlasWan22SpicyImageToVideo

    image_url = _image_url
    if not image_url:
        pytest.skip("No image available (test_setup_image_fixture_imagen4_fast_t2i must run first)")

    node = AtlasWan22SpicyImageToVideo()
    handle = make_client()

    start = time.time()
    video_url, prediction_id = node.run(
        atlas_client=handle,
        image=image_url,
        prompt="The sneaker rotates slowly on a turntable with studio lighting",
        resolution="480p",
        duration=5,
        seed=-1,
        poll_interval_sec=3.0,
        timeout_sec=900,
    )
    elapsed = time.time() - start

    print(f"\n  prediction_id: {prediction_id}")
    print(f"  video_url:     {video_url[:120]}...")
    print(f"  elapsed:       {elapsed:.1f}s")

    assert prediction_id
    assert video_url
    assert video_url.startswith("http"), video_url[:80]


@skip_no_key
def test_wan22_spicy_i2v_lora_opt_in():
    """WAN2.2 Spicy LoRA image-to-video is opt-in.

    Needs LoRA URLs that the backend can fetch. Provide JSON arrays via env:
      ATLASCLOUD_WAN22_SPICY_LORAS_JSON
      ATLASCLOUD_WAN22_SPICY_LOW_NOISE_LORAS_JSON
      ATLASCLOUD_WAN22_SPICY_HIGH_NOISE_LORAS_JSON

    If not set, the test is skipped.
    """

    loras_json = os.getenv("ATLASCLOUD_WAN22_SPICY_LORAS_JSON", "").strip()
    low_noise = os.getenv("ATLASCLOUD_WAN22_SPICY_LOW_NOISE_LORAS_JSON", "").strip()
    high_noise = os.getenv("ATLASCLOUD_WAN22_SPICY_HIGH_NOISE_LORAS_JSON", "").strip()

    if not (loras_json or low_noise or high_noise):
        pytest.skip(
            "Set ATLASCLOUD_WAN22_SPICY_LORAS_JSON and/or ATLASCLOUD_WAN22_SPICY_LOW_NOISE_LORAS_JSON/"
            "ATLASCLOUD_WAN22_SPICY_HIGH_NOISE_LORAS_JSON to run this test"
        )

    from atlascloud_comfyui.nodes.video.wan22_spicy_i2v_lora import AtlasWan22SpicyImageToVideoLora

    image_url = _image_url
    if not image_url:
        pytest.skip("No image available (test_setup_image_fixture_imagen4_fast_t2i must run first)")

    node = AtlasWan22SpicyImageToVideoLora()
    handle = make_client()

    start = time.time()
    video_url, prediction_id = node.run(
        atlas_client=handle,
        image=image_url,
        prompt="The sneaker rotates slowly; add a subtle film grain aesthetic",
        resolution="480p",
        duration=5,
        seed=-1,
        loras_json=loras_json or "[]",
        low_noise_loras_json=low_noise or "[]",
        high_noise_loras_json=high_noise or "[]",
        poll_interval_sec=3.0,
        timeout_sec=900,
    )
    elapsed = time.time() - start

    print(f"\n  prediction_id: {prediction_id}")
    print(f"  video_url:     {video_url[:120]}...")
    print(f"  elapsed:       {elapsed:.1f}s")

    assert prediction_id
    assert video_url
    assert video_url.startswith("http"), video_url[:80]
