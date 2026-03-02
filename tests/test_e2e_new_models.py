"""End-to-end tests for newly added WAN2.6 + Kling Video O3 nodes.

Requires ATLASCLOUD_API_KEY environment variable.
Run:
  ATLASCLOUD_API_KEY=... PYTHONPATH=../ComfyUI pytest tests/test_e2e_new_models.py -v -s

Notes:
- These tests are designed to be optional in CI (will skip if no key).
- Some nodes require user-provided assets (video URLs, reference videos). Those tests are included but skipped unless env vars are provided.
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


# Module-level cache so I2V tests can reuse the T2I output
_wan26_t2i_image_url: str | None = None


@skip_no_key
def test_wan26_t2i():
    """WAN2.6 text-to-image should return a URL."""
    global _wan26_t2i_image_url

    from atlascloud_comfyui.nodes.image.wan26_t2i import AtlasWAN26TextToImage

    node = AtlasWAN26TextToImage()
    handle = make_client()

    start = time.time()
    image_url, prediction_id = node.run(
        atlas_client=handle,
        prompt="A minimalist product photo of a ceramic mug on a wooden table",
        size="1024*1024",
        enable_prompt_expansion=False,
        poll_interval_sec=2.0,
        timeout_sec=180,
    )
    elapsed = time.time() - start

    print(f"\n  prediction_id: {prediction_id}")
    print(f"  image_url:     {image_url[:120]}...")
    print(f"  elapsed:       {elapsed:.1f}s")

    assert prediction_id
    assert image_url
    assert image_url.startswith("http") or image_url.startswith("data:"), image_url[:80]

    _wan26_t2i_image_url = image_url


@skip_no_key
def test_kling_video_o3_pro_t2v():
    """Kling Video O3 Pro text-to-video should return a video URL."""
    from atlascloud_comfyui.nodes.video.kling_video_o3_pro_t2v import AtlasKlingVideoO3ProTextToVideo

    node = AtlasKlingVideoO3ProTextToVideo()
    handle = make_client()

    start = time.time()
    video_url, prediction_id = node.run(
        atlas_client=handle,
        prompt="A cat wearing sunglasses rides a skateboard down a sunny street",
        aspect_ratio="16:9",
        duration=5,
        sound=False,
        poll_interval_sec=3.0,
        timeout_sec=420,
    )
    elapsed = time.time() - start

    print(f"\n  prediction_id: {prediction_id}")
    print(f"  video_url:     {video_url[:120]}...")
    print(f"  elapsed:       {elapsed:.1f}s")

    assert prediction_id
    assert video_url
    assert video_url.startswith("http"), video_url[:80]


@skip_no_key
def test_kling_video_o3_std_t2v():
    """Kling Video O3 Std text-to-video should return a video URL."""
    from atlascloud_comfyui.nodes.video.kling_video_o3_std_t2v import AtlasKlingVideoO3StdTextToVideo

    node = AtlasKlingVideoO3StdTextToVideo()
    handle = make_client()

    start = time.time()
    video_url, prediction_id = node.run(
        atlas_client=handle,
        prompt="A drone shot flying over a forest in early morning fog",
        aspect_ratio="16:9",
        duration=5,
        sound=False,
        poll_interval_sec=3.0,
        timeout_sec=420,
    )
    elapsed = time.time() - start

    print(f"\n  prediction_id: {prediction_id}")
    print(f"  video_url:     {video_url[:120]}...")
    print(f"  elapsed:       {elapsed:.1f}s")

    assert prediction_id
    assert video_url
    assert video_url.startswith("http"), video_url[:80]


@skip_no_key
def test_wan26_i2v_flash():
    """WAN2.6 image-to-video-flash should work using the WAN2.6 T2I image as input."""
    from atlascloud_comfyui.nodes.video.wan26_i2v_flash import AtlasWAN26ImageToVideoFlash

    image_url = _wan26_t2i_image_url
    if not image_url:
        pytest.skip("No image available (test_wan26_t2i must run first)")

    node = AtlasWAN26ImageToVideoFlash()
    handle = make_client()

    start = time.time()
    video_url, prediction_id = node.run(
        atlas_client=handle,
        image=image_url,
        prompt="The mug slowly rotates on the table with soft studio lighting",
        resolution="720p",
        duration=5,
        enable_prompt_expansion=True,
        shot_type="single",
        generate_audio=False,
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
def test_kling_video_o3_pro_i2v():
    """Kling Video O3 Pro image-to-video should work using the WAN2.6 T2I image as input."""
    from atlascloud_comfyui.nodes.video.kling_video_o3_pro_i2v import AtlasKlingVideoO3ProImageToVideo

    image_url = _wan26_t2i_image_url
    if not image_url:
        pytest.skip("No image available (test_wan26_t2i must run first)")

    node = AtlasKlingVideoO3ProImageToVideo()
    handle = make_client()

    start = time.time()
    video_url, prediction_id = node.run(
        atlas_client=handle,
        prompt="The mug gently slides into frame and the camera pulls focus",
        image=image_url,
        duration=5,
        generate_audio=False,
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


# Optional: requires a user-provided video URL (<=10s). Set env var to enable.
@skip_no_key
def test_kling_video_o3_video_edit_requires_input_video():
    """Video-edit needs a real video URL; skip unless provided."""
    video = os.getenv("ATLASCLOUD_E2E_VIDEO_URL", "").strip()
    if not video:
        pytest.skip("Set ATLASCLOUD_E2E_VIDEO_URL to run video-edit E2E")

    from atlascloud_comfyui.nodes.video.kling_video_o3_std_video_edit import AtlasKlingVideoO3StdVideoEdit

    node = AtlasKlingVideoO3StdVideoEdit()
    handle = make_client()

    start = time.time()
    video_url, prediction_id = node.run(
        atlas_client=handle,
        prompt="Remove the background and add a subtle cinematic color grade",
        video=video,
        images="",
        keep_original_sound=True,
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
