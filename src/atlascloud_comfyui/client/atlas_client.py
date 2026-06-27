from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
import inspect
from typing import Any, Dict, Optional
from urllib.parse import urlsplit, urlunsplit

from ..history import LocalHistoryRecorder


class AtlasError(RuntimeError):
    pass


@dataclass
class AtlasClient:
    api_key: str
    base_url: str = "https://api.atlascloud.ai"
    history: LocalHistoryRecorder = field(init=False, repr=False)

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
        self.history = LocalHistoryRecorder.from_env()

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

    def _console_base_url(self) -> str:
        parts = urlsplit(self.base_url)
        host = parts.netloc
        if host.startswith("api."):
            host = "console." + host[len("api.") :]
        elif host == "atlascloud.ai":
            host = "console.atlascloud.ai"
        return urlunsplit((parts.scheme or "https", host, "", "", "")).rstrip("/")

    def history_directory(self) -> str:
        return self.history.history_dir()

    def _infer_node_context(self) -> Dict[str, Any]:
        for frame_info in inspect.stack()[2:]:
            filename = (frame_info.filename or "").replace("\\", "/")
            if "/src/atlascloud_comfyui/nodes/" not in filename:
                continue
            self_obj = frame_info.frame.f_locals.get("self")
            node_class = self_obj.__class__.__name__ if self_obj is not None else None
            return {
                "node_class": node_class or "",
                "function": frame_info.function,
                "file_path": frame_info.filename,
            }
        return {}

    def _record_submission_error(self, request_kind: str, payload: Dict[str, Any], node_context: Dict[str, Any], error: Exception) -> None:
        self.history.record_submission_error(
            request_kind=request_kind,
            payload=payload,
            error_message=str(error),
            node_context=node_context,
            tracking_params=self.tracking_params,
            base_url=self.base_url,
        )

    def _generate(self, endpoint: str, payload: Dict[str, Any], *, request_kind: str) -> str:
        import requests

        url = f"{self.base_url}{endpoint}"
        headers = {"Content-Type": "application/json", **self._auth_headers()}
        node_context = self._infer_node_context()

        try:
            r = requests.post(url, headers=headers, json=payload, params=self.tracking_params, timeout=120)
            r.raise_for_status()
            data = r.json()
            prediction_id = data["data"]["id"]
        except Exception as exc:
            self._record_submission_error(request_kind, payload, node_context, exc)
            raise

        self.history.record_submission(
            prediction_id=prediction_id,
            request_kind=request_kind,
            payload=payload,
            node_context=node_context,
            tracking_params=self.tracking_params,
            base_url=self.base_url,
        )
        return prediction_id

    def generate_video(self, payload: Dict[str, Any]) -> str:
        try:
            return self._generate("/api/v1/model/generateVideo", payload, request_kind="video")
        except KeyError as e:
            raise AtlasError("Unexpected generateVideo response: missing data.id") from e

    def generate_image(self, payload: Dict[str, Any]) -> str:
        try:
            return self._generate("/api/v1/model/generateImage", payload, request_kind="image")
        except KeyError as e:
            raise AtlasError("Unexpected generateImage response: missing data.id") from e

    def upload_media_bytes(self, content: bytes, *, filename: str, mime_type: str = "application/octet-stream") -> Dict[str, Any]:
        import requests

        url = f"{self.base_url}/api/v1/model/uploadMedia"
        headers = self._auth_headers()
        files = {"file": (filename, content, mime_type)}
        r = requests.post(url, headers=headers, files=files, timeout=120)
        r.raise_for_status()
        data = r.json()
        payload = data.get("data")
        if not isinstance(payload, dict):
            raise AtlasError(f"Unexpected uploadMedia response: {data}")
        return payload

    def register_seedance_asset(self, *, url: str, asset_type: str = "Image") -> Dict[str, Any]:
        import requests

        body = {"type": asset_type, "url": url}
        endpoint = f"{self._console_base_url()}/api/v1/sd/assets"
        headers = {"Content-Type": "application/json", **self._auth_headers()}
        r = requests.post(endpoint, headers=headers, json=body, timeout=120)
        r.raise_for_status()
        data = r.json()
        payload = data.get("data")
        if not isinstance(payload, dict):
            raise AtlasError(f"Unexpected asset register response: {data}")
        return payload

    def get_seedance_asset(self, asset_id: str) -> Dict[str, Any]:
        import requests

        endpoint = f"{self._console_base_url()}/api/v1/sd/assets/{asset_id}"
        r = requests.get(endpoint, headers=self._auth_headers(), timeout=60)
        r.raise_for_status()
        data = r.json()
        payload = data.get("data")
        if not isinstance(payload, dict):
            raise AtlasError(f"Unexpected asset lookup response: {data}")
        return payload

    def wait_for_seedance_asset_active(
        self,
        asset_id: str,
        *,
        poll_interval_sec: float = 2.0,
        timeout_sec: float = 300.0,
    ) -> Dict[str, Any]:
        start = time.time()
        last_status: Optional[str] = None
        last_error: Optional[str] = None

        while True:
            elapsed = time.time() - start
            if elapsed > float(timeout_sec):
                extra = f" last_status={last_status!r} last_error={last_error!r}" if last_status or last_error else ""
                raise AtlasError(f"Timed out waiting for asset {asset_id} to become Active.{extra}")

            payload = self.get_seedance_asset(asset_id)
            status = str(payload.get("status") or "").strip()
            last_status = status

            if status.lower() == "active":
                return payload
            if status.lower() == "failed":
                last_error = (
                    str(payload.get("error_message") or "").strip()
                    or str(payload.get("error") or "").strip()
                    or "Asset preprocessing failed"
                )
                code = str(payload.get("error_code") or "").strip()
                raise AtlasError(f"{last_error} (error_code={code})" if code else last_error)

            time.sleep(float(poll_interval_sec))

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
                self.history.record_failure(
                    prediction_id,
                    error_message=f"Timed out waiting for prediction {prediction_id}.{extra}",
                )
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

                    response_json: Optional[Dict[str, Any]] = None
                    try:
                        parsed = r.json()
                        if isinstance(parsed, dict):
                            response_json = parsed
                    except Exception:
                        response_json = None

                    response_status = str(((response_json or {}).get("data") or {}).get("status") or "").strip().lower()
                    if response_status in ("completed", "succeeded"):
                        data = response_json
                        got_response = True
                        break
                    if response_status == "failed":
                        err = (response_json.get("data") or {}).get("error") or "Generation failed"
                        code = (response_json.get("data") or {}).get("error_code")
                        got_response = True
                        self.history.record_failure(
                            prediction_id,
                            error_message=f"{err} (error_code={code})" if code else str(err),
                            response_data=response_json,
                        )
                        raise AtlasError(f"{err} (error_code={code})" if code else str(err))

                    # ✅ 401/403/422：不可重试，立即抛出，避免认证失败等错误被隐藏到超时
                    if r.status_code in (401, 403, 422):
                        body = (r.text or "")[:800]
                        self.history.record_failure(
                            prediction_id,
                            error_message=f"Prediction query failed (http={r.status_code}) url={url} body={body}",
                        )
                        raise AtlasError(f"Prediction query failed (http={r.status_code}) url={url} body={body}")

                    # ✅ 400/404：很多异步系统刚创建会短暂查不到，warmup 内继续轮询
                    if r.status_code in (400, 404):
                        got_response = True
                        last_http = r.status_code
                        last_body = (r.text or "")[:800]
                        if elapsed <= float(warmup_grace_sec):
                            continue  # try next candidate / keep polling
                        # warmup 过了仍然 400/404 才报错，并打印 body
                        self.history.record_failure(
                            prediction_id,
                            error_message=f"Prediction query failed (http={r.status_code}) url={url} body={last_body}",
                        )
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
                        self.history.record_failure(
                            prediction_id,
                            error_message=f"Prediction query failed (http={last_http}) url={url} body={last_body}",
                        )
                        raise AtlasError(f"Prediction query failed (http={last_http}) url={url} body={last_body}")
                    continue

            if not got_response or not isinstance(data, dict):
                time.sleep(float(poll_interval_sec))
                continue

            status = (data.get("data") or {}).get("status")
            if status:
                self.history.record_poll_status(prediction_id, str(status), response_data=data)

            if status in ("completed", "succeeded"):
                if pbar:
                    pbar.update(100 - last_pct)
                self.history.record_completion(prediction_id, response_data=data)
                return data

            if status == "failed":
                err = (data.get("data") or {}).get("error") or "Generation failed"
                code = (data.get("data") or {}).get("error_code")
                self.history.record_failure(
                    prediction_id,
                    error_message=f"{err} (error_code={code})" if code else str(err),
                    response_data=data,
                )
                raise AtlasError(f"{err} (error_code={code})" if code else err)

            time.sleep(float(poll_interval_sec))
