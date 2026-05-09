"""End-to-end tests for newly added HappyHorse-1.0 nodes (2026-04-27).

Requires ATLASCLOUD_API_KEY environment variable.
Run:
  ATLASCLOUD_API_KEY=... PYTHONPATH=../ComfyUI pytest tests/test_e2e_new_models_2026_04_27.py -v -s

Notes:
- Designed to be optional in CI (skips if no key).
- Video-edit is opt-in due to queue/credit variability.
"""

from __future__ import annotations

import os
import time

import pytest

# Add src to path
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

_HAS_KEY = bool(os.getenv("ATLASCLOUD_API_KEY", "").strip())
_SKIP_E2E = os.getenv("ATLASCLOUD_RUN_E2E", "").strip() != "1"
skip_no_key = pytest.mark.skipif(
    (not _HAS_KEY) or _SKIP_E2E,
    reason="E2E disabled (set ATLASCLOUD_RUN_E2E=1) or ATLASCLOUD_API_KEY not set",
)

from atlascloud_comfyui.client.atlas_client import AtlasClient
from atlascloud_comfyui.nodes.auth.atlas_client_node import AtlasClientHandle


def make_client() -> AtlasClientHandle:
    client = AtlasClient.from_env()
    return AtlasClientHandle(client=client)


# Module-level cache so I2V tests can reuse the T2I output
_imagen4_fast_image_url: str | None = None


@skip_no_key
def test_setup_image_fixture_imagen4_fast_t2i():
    """Use a stable T2I model to generate an image for downstream I2V tests."""
    global _imagen4_fast_image_url

    from atlascloud_comfyui.nodes.image.imagen4_fast_t2i import AtlasImagen4FastTextToImage

    node = AtlasImagen4FastTextToImage()
    handle = make_client()

    start = time.time()
    image_url, prediction_id = node.run(
        atlas_client=handle,
        prompt="A clean studio photo of a running horse figurine on a white background",
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

    assert prediction_id
    assert image_url
    assert image_url.startswith("http") or image_url.startswith("data:"), image_url[:80]

    _imagen4_fast_image_url = image_url


@skip_no_key
def test_happyhorse_10_t2v():
    """HappyHorse-1.0 text-to-video should return a video URL."""
    from atlascloud_comfyui.nodes.video.alibaba_happyhorse_1_0_t2v import AtlasHappyHorse10TextToVideo

    node = AtlasHappyHorse10TextToVideo()
    handle = make_client()

    start = time.time()
    video_url, prediction_id = node.run(
        atlas_client=handle,
        prompt="A horse gallops across a grassy field at golden hour, cinematic",
        resolution="720P",
        ratio="16:9",
        duration=5,
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
def test_happyhorse_10_i2v_uses_generated_image():
    """HappyHorse-1.0 image-to-video should work using an Imagen4 Fast image as input."""
    from atlascloud_comfyui.nodes.video.alibaba_happyhorse_1_0_i2v import AtlasHappyHorse10ImageToVideo

    image_url = _imagen4_fast_image_url
    if not image_url:
        pytest.skip("No image available (test_setup_image_fixture_imagen4_fast_t2i must run first)")

    node = AtlasHappyHorse10ImageToVideo()
    handle = make_client()

    start = time.time()
    video_url, prediction_id = node.run(
        atlas_client=handle,
        image=image_url,
        prompt="The horse figurine slowly turns on a rotating display stand",
        resolution="720P",
        duration=5,
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
def test_happyhorse_10_video_edit_opt_in_requires_input_video():
    """Video-edit needs a real video URL; skip unless provided.

    Queueing can be long; treat it as opt-in.
    """

    if os.getenv("ATLASCLOUD_RUN_HAPPYHORSE_VIDEO_EDIT_E2E", "").strip() != "1":
        pytest.skip("Set ATLASCLOUD_RUN_HAPPYHORSE_VIDEO_EDIT_E2E=1 to run HappyHorse Video-Edit E2E")

    video = os.getenv("ATLASCLOUD_E2E_VIDEO_URL", "").strip()
    if not video:
        pytest.skip("Set ATLASCLOUD_E2E_VIDEO_URL to run video-edit E2E")

    if os.getenv("ATLASCLOUD_SKIP_VIDEO_EDIT_E2E", "").strip() == "1":
        pytest.skip("ATLASCLOUD_SKIP_VIDEO_EDIT_E2E=1")

    from atlascloud_comfyui.nodes.video.alibaba_happyhorse_1_0_video_edit import AtlasHappyHorse10VideoEdit

    node = AtlasHappyHorse10VideoEdit()
    handle = make_client()

    start = time.time()
    video_url, prediction_id = node.run(
        atlas_client=handle,
        video=video,
        prompt="Stabilize the clip and enhance the color grading",
        resolution="720P",
        audio_setting="origin",
        poll_interval_sec=3.0,
        timeout_sec=1200,
    )
    elapsed = time.time() - start

    print(f"\n  prediction_id: {prediction_id}")
    print(f"  video_url:     {video_url[:120]}...")
    print(f"  elapsed:       {elapsed:.1f}s")

    assert prediction_id
    assert video_url
    assert video_url.startswith("http"), video_url[:80]
