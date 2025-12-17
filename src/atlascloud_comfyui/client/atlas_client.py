from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


class AtlasError(RuntimeError):
    pass


@dataclass
class AtlasClient:
    api_key: str
    base_url: str = "https://api.atlascloud.ai"

    @classmethod
    def from_env(cls, *, base_url: Optional[str] = None) -> "AtlasClient":
        api_key = os.getenv("ATLASCLOUD_API_KEY", "").strip()
        if not api_key:
            raise AtlasError("Missing ATLASCLOUD_API_KEY environment variable.")
        return cls(api_key=api_key, base_url=base_url or os.getenv("ATLASCLOUD_BASE_URL", "https://api.atlascloud.ai"))

    def _auth_headers(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self.api_key}"}

    def generate_video(self, payload: Dict[str, Any]) -> str:
        url = f"{self.base_url}/api/v1/model/generateVideo"
        headers = {"Content-Type": "application/json", **self._auth_headers()}
        r = requests.post(url, headers=headers, json=payload, timeout=120)
        r.raise_for_status()
        data = r.json()
        try:
            return data["data"]["id"]
        except Exception as e:
            raise AtlasError(f"Unexpected generateVideo response: {data}") from e

    def generate_image(self, payload: dict) -> str:
        url = f"{self.base_url}/api/v1/model/generateImage"
        headers = {"Content-Type": "application/json", **self._auth_headers()}
        r = requests.post(url, headers=headers, json=payload, timeout=120)
        r.raise_for_status()
        data = r.json()
        try:
            return data["data"]["id"]
        except Exception as e:
            raise AtlasError(f"Unexpected generateImage response: {data}") from e


    def poll_prediction(self, prediction_id: str, *, poll_interval_sec: float = 2.0, timeout_sec: float = 900) -> dict:
        import requests

        try:
            from comfy.utils import ProgressBar

            print("[AtlasCloud] ProgressBar OK:", ProgressBar)
        except Exception as e:
            print("[AtlasCloud] ProgressBar import FAILED:", repr(e))
            ProgressBar = None

        url = f"{self.base_url}/api/v1/model/prediction/{prediction_id}"
        start = time.time()

        pbar = ProgressBar(100) if ProgressBar else None
        last_pct = 0

        while True:
            r = requests.get(url, headers=self._auth_headers(), timeout=60)
            r.raise_for_status()
            data = r.json()
            status = (data.get("data") or {}).get("status")

            if status in ("completed", "succeeded"):
                if pbar:
                    pbar.update(100 - last_pct)  # 直接拉满
                return data

            if status == "failed":
                err = (data.get("data") or {}).get("error") or "Generation failed"
                raise AtlasError(err)

            elapsed = time.time() - start
            pct = int(min(99, (elapsed / timeout_sec) * 100))  # 0~99，完成时再到100

            if pbar and pct > last_pct:
                pbar.update(pct - last_pct)
                last_pct = pct

            if elapsed > timeout_sec:
                raise AtlasError(f"Timed out waiting for prediction {prediction_id} (last status={status})")

            time.sleep(poll_interval_sec)
