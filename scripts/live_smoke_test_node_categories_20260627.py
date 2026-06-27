from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Callable, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from atlascloud_comfyui.client.atlas_client import AtlasClient
from atlascloud_comfyui.history.local_history import LocalHistoryRecorder
from atlascloud_comfyui.nodes.auth.atlas_client_node import AtlasClientHandle
from atlascloud_comfyui.nodes.image.atlascloud_image_upscaler import AtlasImageUpscaler
from atlascloud_comfyui.nodes.image.midjourney_v81_i2i import AtlasMidjourneyV81ImageToImage
from atlascloud_comfyui.nodes.image.nano_banana_edit import AtlasNanoBananaEdit
from atlascloud_comfyui.nodes.image.nano_banana_t2i import AtlasNanoBananaTextToImage
from atlascloud_comfyui.nodes.video.alibaba_wan_2_2_spicy_video_extend import AtlasWan22SpicyVideoExtend
from atlascloud_comfyui.nodes.video.alibaba_happyhorse_1_0_i2v import AtlasHappyHorse10ImageToVideo
from atlascloud_comfyui.nodes.video.alibaba_happyhorse_1_0_r2v import AtlasHappyHorse10ReferenceToVideo
from atlascloud_comfyui.nodes.video.alibaba_happyhorse_1_0_t2v import AtlasHappyHorse10TextToVideo
from atlascloud_comfyui.nodes.video.alibaba_happyhorse_1_0_video_edit import AtlasHappyHorse10VideoEdit


def require_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise SystemExit(f"Missing required environment variable: {name}")
    return value


def make_handle() -> AtlasClientHandle:
    api_key = require_env("ATLASCLOUD_API_KEY")
    base_url = os.getenv("ATLASCLOUD_BASE_URL", "https://api.atlascloud.ai").strip()
    os.environ.setdefault("ATLASCLOUD_API_KEY", api_key)
    return AtlasClientHandle(client=AtlasClient(api_key=api_key, base_url=base_url))


def load_run_summary(recorder: LocalHistoryRecorder, prediction_id: str) -> Dict[str, Any]:
    doc = recorder.get_run(prediction_id) or {}
    downloaded_assets = [asset for asset in (doc.get("downloaded_assets") or []) if asset.get("status") == "downloaded"]
    input_assets = [asset for asset in (doc.get("input_downloaded_assets") or []) if asset.get("status") == "downloaded"]
    return {
        "prediction_id": prediction_id,
        "latest_status": doc.get("latest_status"),
        "history_file": str((Path(recorder.history_dir()) / "runs" / f"{prediction_id}.json")),
        "downloaded_asset_count": len(downloaded_assets),
        "input_asset_count": len(input_assets),
        "prompt_file": ((doc.get("prompt_file") or {}).get("local_path")),
    }


def run_case(
    name: str,
    runner: Callable[[], Tuple[str, str]],
    recorder: LocalHistoryRecorder,
) -> Tuple[Dict[str, Any], str]:
    started_at = time.time()
    print(f"[smoke] start {name}", flush=True)
    try:
        output_url, prediction_id = runner()
        duration_sec = round(time.time() - started_at, 2)
        summary = load_run_summary(recorder, prediction_id)
        result = {
            "name": name,
            "status": "passed",
            "duration_sec": duration_sec,
            "output_url": output_url,
            **summary,
        }
        print(f"[smoke] done  {name} -> {prediction_id} ({duration_sec}s)", flush=True)
        return result, output_url
    except Exception as exc:
        duration_sec = round(time.time() - started_at, 2)
        result = {
            "name": name,
            "status": "failed",
            "duration_sec": duration_sec,
            "error": str(exc),
        }
        print(f"[smoke] fail  {name} -> {exc}", flush=True)
        return result, ""


def main() -> int:
    handle = make_handle()
    recorder = handle.client.history
    smoke_only = {part.strip().lower() for part in os.getenv("ATLASCLOUD_SMOKE_ONLY", "").split(",") if part.strip()}
    run_images = not smoke_only or "image" in smoke_only
    run_videos = not smoke_only or "video" in smoke_only
    base_image_url = os.getenv("ATLASCLOUD_BASE_IMAGE_URL", "").strip()
    base_video_url = os.getenv("ATLASCLOUD_BASE_VIDEO_URL", "").strip()

    image_prompt = "A tiny orange cat sitting on a plain studio floor, simple background, clean composition"
    image_edit_prompt = "Keep the same cat and add a small blue scarf"
    image_i2i_prompt = "Keep the same subject, turn it into a soft watercolor illustration"
    video_prompt = "A tiny orange cat blinking once and making a subtle head turn"
    video_extend_prompt = "Continue the same motion naturally for one more second"
    video_edit_prompt = "Keep the same scene and add a slightly warmer cinematic color grade"

    results = []

    if run_images:
        t2i_node = AtlasNanoBananaTextToImage()
        t2i_result, base_image_url = run_case(
            "image_t2i",
            lambda: t2i_node.run(
                handle,
                prompt=image_prompt,
                aspect_ratio="1:1",
                enable_base64_output=False,
                enable_sync_mode=False,
                output_format="png",
                randomize_seed=True,
                poll_interval_sec=2.0,
                timeout_sec=300,
            ),
            recorder,
        )
        results.append(t2i_result)

    if base_image_url:
        if run_images:
            i2i_node = AtlasMidjourneyV81ImageToImage()
            i2i_result, _ = run_case(
                "image_i2i",
                lambda: i2i_node.run(
                    handle,
                    image=base_image_url,
                    prompt=image_i2i_prompt,
                    sref="",
                    aspect_ratio="1:1",
                    hd=False,
                    stylize=0,
                    chaos=0,
                    weird=0,
                    quality=1,
                    seed=-1,
                    enable_base64_output=False,
                    poll_interval_sec=2.0,
                    timeout_sec=300,
                ),
                recorder,
            )
            results.append(i2i_result)

            edit_node = AtlasNanoBananaEdit()
            edit_result, _ = run_case(
                "image_edit",
                lambda: edit_node.run(
                    handle,
                    images=base_image_url,
                    prompt=image_edit_prompt,
                    aspect_ratio="1:1",
                    enable_base64_output=False,
                    enable_sync_mode=False,
                    output_format="png",
                    randomize_seed=True,
                    poll_interval_sec=2.0,
                    timeout_sec=300,
                ),
                recorder,
            )
            results.append(edit_result)

            upscale_node = AtlasImageUpscaler()
            upscale_result, _ = run_case(
                "image_upscale",
                lambda: upscale_node.run(
                    handle,
                    image=base_image_url,
                    outscale=1.0,
                    output_format="jpeg",
                    poll_interval_sec=2.0,
                    timeout_sec=300,
                ),
                recorder,
            )
            results.append(upscale_result)

    if run_videos:
        t2v_node = AtlasHappyHorse10TextToVideo()
        t2v_result, base_video_url = run_case(
            "video_t2v",
            lambda: t2v_node.run(
                handle,
                prompt=video_prompt,
                resolution="720P",
                ratio="16:9",
                duration=3,
                seed=-1,
                poll_interval_sec=2.0,
                timeout_sec=900,
            ),
            recorder,
        )
        results.append(t2v_result)

    if run_videos and base_image_url:
        i2v_node = AtlasHappyHorse10ImageToVideo()
        i2v_result, _ = run_case(
            "video_i2v",
            lambda: i2v_node.run(
                handle,
                image=base_image_url,
                prompt=video_prompt,
                resolution="720P",
                duration=3,
                seed=-1,
                poll_interval_sec=2.0,
                timeout_sec=900,
            ),
            recorder,
        )
        results.append(i2v_result)

        r2v_node = AtlasHappyHorse10ReferenceToVideo()
        r2v_result, _ = run_case(
            "video_r2v",
            lambda: r2v_node.run(
                handle,
                prompt=video_prompt,
                images=base_image_url,
                resolution="720P",
                ratio="16:9",
                duration=3,
                seed=-1,
                poll_interval_sec=2.0,
                timeout_sec=900,
            ),
            recorder,
        )
        results.append(r2v_result)

    if run_videos and base_video_url:
        extend_node = AtlasWan22SpicyVideoExtend()
        extend_result, _ = run_case(
            "video_extend",
            lambda: extend_node.run(
                handle,
                video_url=base_video_url,
                prompt=video_extend_prompt,
                duration=5,
                resolution="480p",
                seed=-1,
                poll_interval_sec=2.0,
                timeout_sec=900,
            ),
            recorder,
        )
        results.append(extend_result)

        edit_video_node = AtlasHappyHorse10VideoEdit()
        edit_video_result, _ = run_case(
            "video_edit",
            lambda: edit_video_node.run(
                handle,
                video=base_video_url,
                prompt=video_edit_prompt,
                images="",
                resolution="720P",
                audio_setting="origin",
                seed=-1,
                poll_interval_sec=2.0,
                timeout_sec=1200,
            ),
            recorder,
        )
        results.append(edit_video_result)

    report_dir = REPO_ROOT / "reports" / "live_smoke"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / "node_categories_2026_06_27.json"
    report = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "history_dir": recorder.history_dir(),
        "results": results,
    }
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[smoke] wrote report: {report_path}", flush=True)

    failed = [item for item in results if item.get("status") != "passed"]
    if failed:
        print(f"[smoke] failures: {len(failed)}", flush=True)
        return 1
    print(f"[smoke] all cases passed: {len(results)}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
