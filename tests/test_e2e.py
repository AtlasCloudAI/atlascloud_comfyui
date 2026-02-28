"""End-to-end tests for representative node types (T2I, T2V, I2V).

Requires ATLASCLOUD_API_KEY environment variable.
Usage:
    ATLASCLOUD_API_KEY=... python tests/test_e2e.py
"""

from __future__ import annotations

import os
import sys
import time

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from atlascloud_comfyui.client.atlas_client import AtlasClient
from atlascloud_comfyui.nodes.auth.atlas_client_node import AtlasClientHandle


def make_client() -> AtlasClientHandle:
    client = AtlasClient.from_env()
    return AtlasClientHandle(client=client)


def test_t2i():
    """Test T2I: Luma Photon Flash (minimal params, fast)."""
    from atlascloud_comfyui.nodes.image.luma_photon_flash_t2i import (
        AtlasLumaPhotonFlashTextToImage,
    )

    print("\n=== T2I Test: Luma Photon Flash ===")
    node = AtlasLumaPhotonFlashTextToImage()
    handle = make_client()

    start = time.time()
    result = node.run(
        atlas_client=handle,
        prompt="A cute orange cat sitting on a windowsill",
        enable_base64_output=False,
        poll_interval_sec=2.0,
        timeout_sec=120,
    )
    elapsed = time.time() - start

    image_url, prediction_id = result
    print(f"  prediction_id: {prediction_id}")
    print(f"  image_url:     {image_url[:120]}...")
    print(f"  elapsed:       {elapsed:.1f}s")

    assert prediction_id, "prediction_id should not be empty"
    assert image_url, "image_url should not be empty"
    assert image_url.startswith("http") or image_url.startswith("data:"), f"Unexpected image_url format: {image_url[:80]}"
    print("  PASSED")
    return image_url


def test_t2v():
    """Test T2V: Hailuo 02 T2V Pro (minimal params)."""
    from atlascloud_comfyui.nodes.video.hailuo_02_t2v_pro import AtlasHailuo02T2VPro

    print("\n=== T2V Test: Hailuo 02 T2V Pro ===")
    node = AtlasHailuo02T2VPro()
    handle = make_client()

    start = time.time()
    result = node.run(
        atlas_client=handle,
        prompt="A cat walking across a sunny garden",
        enable_prompt_expansion=False,
        poll_interval_sec=3.0,
        timeout_sec=300,
    )
    elapsed = time.time() - start

    video_url, prediction_id = result
    print(f"  prediction_id: {prediction_id}")
    print(f"  video_url:     {video_url[:120]}...")
    print(f"  elapsed:       {elapsed:.1f}s")

    assert prediction_id, "prediction_id should not be empty"
    assert video_url, "video_url should not be empty"
    assert video_url.startswith("http"), f"Unexpected video_url format: {video_url[:80]}"
    print("  PASSED")


def test_i2v(image_url: str):
    """Test I2V: Hailuo 02 I2V Pro (minimal params)."""
    from atlascloud_comfyui.nodes.video.hailuo_02_i2v_pro import AtlasHailuo02I2VPro

    print("\n=== I2V Test: Hailuo 02 I2V Pro ===")
    node = AtlasHailuo02I2VPro()
    handle = make_client()

    start = time.time()
    result = node.run(
        atlas_client=handle,
        image=image_url,
        prompt="The cat slowly turns its head and blinks",
        enable_prompt_expansion=False,
        poll_interval_sec=3.0,
        timeout_sec=300,
    )
    elapsed = time.time() - start

    video_url, prediction_id = result
    print(f"  prediction_id: {prediction_id}")
    print(f"  video_url:     {video_url[:120]}...")
    print(f"  elapsed:       {elapsed:.1f}s")

    assert prediction_id, "prediction_id should not be empty"
    assert video_url, "video_url should not be empty"
    assert video_url.startswith("http"), f"Unexpected video_url format: {video_url[:80]}"
    print("  PASSED")


if __name__ == "__main__":
    print("=" * 60)
    print("AtlasCloud E2E Tests")
    print("=" * 60)

    passed = 0
    failed = 0
    errors = []

    # 1) T2I
    image_url = None
    try:
        image_url = test_t2i()
        passed += 1
    except Exception as e:
        failed += 1
        errors.append(("T2I", e))
        print(f"  FAILED: {e}")

    # 2) T2V (run in parallel conceptually, but sequential here)
    try:
        test_t2v()
        passed += 1
    except Exception as e:
        failed += 1
        errors.append(("T2V", e))
        print(f"  FAILED: {e}")

    # 3) I2V (needs image from T2I)
    if image_url:
        try:
            test_i2v(image_url)
            passed += 1
        except Exception as e:
            failed += 1
            errors.append(("I2V", e))
            print(f"  FAILED: {e}")
    else:
        print("\n=== I2V Test: SKIPPED (no image from T2I) ===")
        failed += 1
        errors.append(("I2V", "Skipped - T2I failed"))

    # Summary
    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    if errors:
        for name, err in errors:
            print(f"  FAIL {name}: {err}")
    print("=" * 60)

    sys.exit(0 if failed == 0 else 1)
