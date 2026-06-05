#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
import time
from typing import List

import requests


API_BASE = "https://api.atlascloud.ai/api/v1"
CONSOLE_BASE = "https://console.atlascloud.ai/api/v1"
IMAGE_PATHS = [
    "/Users/zby/Downloads/image-1780655868163.jpg",
    "/Users/zby/Downloads/image-1780655872692.webp",
    "/Users/zby/Downloads/image-1780655876014.jpg",
    "/Users/zby/Downloads/image-1780655878816.jpg",
]
PROMPT = (
    "image_1作为场景；image_2是赵二叔；image_3是医生；image_4是赵二婶。"
    "赵二叔一边和医生握手一边说着：“医生你可算来了”，赵二婶在旁边看着医生。"
)


def require_api_key() -> str:
    api_key = os.getenv("ATLASCLOUD_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("Missing ATLASCLOUD_API_KEY environment variable.")
    return api_key


def upload_media(api_key: str, path: str) -> str:
    with open(path, "rb") as fh:
        response = requests.post(
            f"{API_BASE}/model/uploadMedia",
            headers={"Authorization": f"Bearer {api_key}"},
            files={"file": (os.path.basename(path), fh)},
            timeout=120,
        )
    response.raise_for_status()
    data = response.json()["data"]
    download_url = data["download_url"]
    print(f"uploaded {os.path.basename(path)} -> {download_url}")
    return download_url


def register_asset(api_key: str, download_url: str) -> dict:
    response = requests.post(
        f"{CONSOLE_BASE}/sd/assets",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"type": "Image", "url": download_url},
        timeout=120,
    )
    response.raise_for_status()
    data = response.json()["data"]
    print(f"registered asset id={data.get('id')} atlas_asset_id={data.get('atlas_asset_id')} status={data.get('status')}")
    return data


def wait_asset_active(api_key: str, asset_id: str, timeout_sec: int = 300) -> dict:
    deadline = time.time() + timeout_sec
    while time.time() < deadline:
        response = requests.get(
            f"{CONSOLE_BASE}/sd/assets/{asset_id}",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=60,
        )
        response.raise_for_status()
        data = response.json()["data"]
        status = str(data.get("status") or "")
        if status.lower() == "active":
            print(f"asset active {asset_id} -> {data.get('atlas_asset_id')}")
            return data
        if status.lower() == "failed":
            raise RuntimeError(
                f"asset failed {asset_id}: error_code={data.get('error_code')} error_message={data.get('error_message')}"
            )
        print(f"asset {asset_id} status={status}")
        time.sleep(2)
    raise TimeoutError(f"Timed out waiting for asset {asset_id} to become Active")


def build_asset_refs(api_key: str, paths: List[str]) -> List[str]:
    refs: List[str] = []
    for path in paths:
        download_url = upload_media(api_key, path)
        created = register_asset(api_key, download_url)
        ready = wait_asset_active(api_key, str(created["id"]))
        asset_ref_id = (
            str(ready.get("atlas_asset_id") or "").strip()
            or str(ready.get("ark_asset_id") or "").strip()
            or str(ready.get("id") or "").strip()
        )
        refs.append(f"asset://{asset_ref_id}")
    return refs


def submit_generation(api_key: str, asset_refs: List[str]) -> str:
    payload = {
        "model": "bytedance/seedance-2.0/reference-to-video",
        "reference_images": asset_refs,
        "prompt": PROMPT,
        "duration": 5,
        "resolution": "720p",
        "ratio": "adaptive",
        "generate_audio": True,
        "watermark": False,
        "return_last_frame": False,
    }
    response = requests.post(
        f"{API_BASE}/model/generateVideo",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=120,
    )
    print("submit status:", response.status_code)
    print(response.text[:1000])
    response.raise_for_status()
    return response.json()["data"]["id"]


def poll_prediction(api_key: str, prediction_id: str, timeout_sec: int = 900) -> dict:
    deadline = time.time() + timeout_sec
    while time.time() < deadline:
        response = requests.get(
            f"{API_BASE}/model/prediction/{prediction_id}",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=60,
        )
        print("poll status:", response.status_code)
        print(response.text[:1500])
        response.raise_for_status()
        data = response.json()["data"]
        status = data.get("status")
        if status in ("completed", "succeeded"):
            return data
        if status == "failed":
            raise RuntimeError(json.dumps(data, ensure_ascii=False))
        time.sleep(5)
    raise TimeoutError(f"Timed out waiting for prediction {prediction_id}")


def main() -> int:
    api_key = require_api_key()
    refs = build_asset_refs(api_key, IMAGE_PATHS)
    print("asset refs:")
    print(json.dumps(refs, ensure_ascii=False, indent=2))
    prediction_id = submit_generation(api_key, refs)
    print("prediction:", prediction_id)
    result = poll_prediction(api_key, prediction_id)
    print("final result:")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
