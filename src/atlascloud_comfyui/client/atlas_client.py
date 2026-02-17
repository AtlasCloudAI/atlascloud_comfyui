from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


class AtlasError(RuntimeError):
    pass


@dataclass
class AtlasClient:
    api_key: str
    base_url: str = "https://api.atlascloud.ai"

    # Used for tracking on "generate" endpoints only (NOT for polling).
    tracking_params: Dict[str, str] = field(
        default_factory=lambda: {
            "utm_source": "github",
            "utm_medium": "readme",
            "utm_campaign": "comfyui",
        }
    )

    def __post_init__(self) -> None:
        # Normalize base_url to avoid double slashes.
        self.base_url = (self.base_url or "").strip().rstrip("/")

    @classmethod
    def from_env(cls, *, base_url: Optional[str] = None) -> "AtlasClient":
        api_key = os.getenv("ATLASCLOUD_API_KEY", "").strip()
        if not api_key:
            raise AtlasError("Missing ATLASCLOUD_API_KEY environment variable.")

        resolved_base = (base_url or os.getenv("ATLASCLOUD_BASE_URL", "https://api.atlascloud.ai")).strip()

        tracking = {
            "utm_source": os.getenv("ATLASCLOUD_UTM_SOURCE", "github"),
            "utm_medium": os.getenv("ATLASCLOUD_UTM_MEDIUM", "readme"),
            "utm_campaign": os.getenv("ATLASCLOUD_UTM_CAMPAIGN", "comfyui"),
        }

        return cls(api_key=api_key, base_url=resolved_base, tracking_params=tracking)

    def _auth_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "X-Atlas-Client": "comfyui",
            "X-Atlas-Source": "github-readme",
        }

    def generate_video(self, payload: Dict[str, Any]) -> str:
        # ✅ runtime import so CI can import nodes without requests installed
        import requests

        url = f"{self.base_url}/api/v1/model/generateVideo"
        headers = {"Content-Type": "application/json", **self._auth_headers()}
        r = requests.post(url, headers=headers, json=payload, params=self.tracking_params, timeout=120)
        r.raise_for_status()
        data = r.json()
        try:
            return data["data"]["id"]
        except Exception as e:
            raise AtlasError(f"Unexpected generateVideo response: {data}") from e

    def generate_image(self, payload: Dict[str, Any]) -> str:
        # ✅ runtime import so CI can import nodes without requests installed
        import requests

        url = f"{self.base_url}/api/v1/model/generateImage"
        headers = {"Content-Type": "application/json", **self._auth_headers()}
        r = requests.post(url, headers=headers, json=payload, params=self.tracking_params, timeout=120)
        r.raise_for_status()
        data = r.json()
        try:
            return data["data"]["id"]
        except Exception as e:
            raise AtlasError(f"Unexpected generateImage response: {data}") from e

    def poll_prediction(
        self,
        prediction_id: str,
        *,
        poll_interval_sec: float = 2.0,
        timeout_sec: float = 900,
        warmup_grace_sec: float = 30.0,  # ✅ 建议 30s：job 刚创建时 prediction 可能暂时查不到
    ):
        import requests

        try:
            from comfy.utils import ProgressBar

            print("[AtlasCloud] ProgressBar OK:", ProgressBar)
        except Exception as e:
            print("[AtlasCloud] ProgressBar import FAILED:", repr(e))
            ProgressBar = None

        prediction_id = (prediction_id or "").strip()
        if not prediction_id:
            raise AtlasError("prediction_id is empty")

        # ✅ 只保留正确的 endpoint（不要再试 /prediction 这种不存在的路径）
        url_candidates = [
            f"{self.base_url}/api/v1/model/prediction/{prediction_id}",
            f"{self.base_url}/api/v1/model/prediction/{prediction_id}/",
        ]

        start = time.time()
        pbar = ProgressBar(100) if ProgressBar else None
        last_pct = 0

        last_http: Optional[int] = None
        last_body: Optional[str] = None

        while True:
            elapsed = time.time() - start

            # time-based progress (0~99), completed -> 100
            pct = int(min(99, (elapsed / float(timeout_sec)) * 100))
            if pbar and pct > last_pct:
                pbar.update(pct - last_pct)
                last_pct = pct

            if elapsed > float(timeout_sec):
                extra = f" last_http={last_http} last_body={last_body!r}" if last_http else ""
                raise AtlasError(f"Timed out waiting for prediction {prediction_id}.{extra}")

            data: Optional[Dict[str, Any]] = None
            got_response = False

            for url in url_candidates:
                try:
                    r = requests.get(
                        url,
                        headers=self._auth_headers(),
                        params=self.tracking_params,  # ✅ utm params OK，但只作为 query
                        timeout=60,
                    )

                    # ✅ 401/403/422：不可重试，立即抛出，避免认证失败等错误被隐藏到超时
                    if r.status_code in (401, 403, 422):
                        body = (r.text or "")[:800]
                        raise AtlasError(f"Prediction query failed (http={r.status_code}) url={url} body={body}")

                    # ✅ 400/404：很多异步系统刚创建会短暂查不到，warmup 内继续轮询
                    if r.status_code in (400, 404):
                        got_response = True
                        last_http = r.status_code
                        last_body = (r.text or "")[:800]
                        if elapsed <= float(warmup_grace_sec):
                            continue  # try next candidate / keep polling
                        # warmup 过了仍然 400/404 才报错，并打印 body
                        raise AtlasError(f"Prediction query failed (http={r.status_code}) url={url} body={last_body}")

                    r.raise_for_status()
                    data = r.json()
                    got_response = True
                    break

                except requests.RequestException as e:
                    got_response = True
                    resp = getattr(e, "response", None)
                    last_http = getattr(resp, "status_code", None)
                    last_body = (getattr(resp, "text", "") or "")[:800] if resp is not None else repr(e)
                    # 401/403/422 不可重试，立即抛出，避免认证失败等错误被隐藏到超时
                    if last_http in (401, 403, 422):
                        raise AtlasError(f"Prediction query failed (http={last_http}) url={url} body={last_body}")
                    continue

            if not got_response or not isinstance(data, dict):
                time.sleep(float(poll_interval_sec))
                continue

            status = (data.get("data") or {}).get("status")

            if status in ("completed", "succeeded"):
                if pbar:
                    pbar.update(100 - last_pct)
                return data

            if status == "failed":
                err = (data.get("data") or {}).get("error") or "Generation failed"
                raise AtlasError(err)

            time.sleep(float(poll_interval_sec))
