from __future__ import annotations

import hashlib
import base64
import mimetypes
import json
import os
import shutil
import sys
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import urlsplit, urlunsplit
from urllib.request import urlopen


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _default_history_dir() -> Path:
    home = Path.home()
    if sys.platform == "darwin":
        base_dir = Path(os.getenv("XDG_DATA_HOME") or (home / "Library" / "Application Support"))
    elif os.name == "nt":
        base_dir = Path(os.getenv("APPDATA") or os.getenv("LOCALAPPDATA") or (home / "AppData" / "Roaming"))
    else:
        base_dir = Path(os.getenv("XDG_DATA_HOME") or (home / ".local" / "share"))
    return base_dir / "AtlasCloud" / "ComfyUI" / "local_history"


def _legacy_history_dir() -> Path:
    repo_root = Path(__file__).resolve().parents[3]
    return repo_root / "local_history"


def _has_history_data(path: Path) -> bool:
    if not path.exists():
        return False
    for child in path.iterdir():
        if child.is_dir():
            return True
        if child.is_file():
            return True
    return False


def _sanitize_url(url: str) -> str:
    parts = urlsplit(url)
    return urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))


def _guess_extension_from_url(url: str, default_ext: str = ".bin") -> str:
    path = urlsplit(url).path
    ext = Path(path).suffix.lower()
    return ext or default_ext


def _default_extension(request_kind: str, payload: Dict[str, Any]) -> str:
    output_format = str(payload.get("output_format") or "").strip().lower()
    if output_format:
        return "." + output_format.lstrip(".")
    return ".png" if request_kind == "image" else ".mp4"


def _sanitize_value(key: str, value: Any) -> Any:
    lowered_key = (key or "").lower()

    if isinstance(value, dict):
        return {k: _sanitize_value(str(k), v) for k, v in value.items()}
    if isinstance(value, list):
        return [_sanitize_value(lowered_key, item) for item in value]
    if isinstance(value, tuple):
        return [_sanitize_value(lowered_key, item) for item in value]
    if not isinstance(value, str):
        return value

    if any(token in lowered_key for token in ("api_key", "authorization", "token", "cookie", "secret", "password")):
        return "***"

    if value.startswith("data:") or len(value) > 4000:
        digest = hashlib.sha256(value.encode("utf-8", errors="ignore")).hexdigest()[:16]
        return {"kind": "large_string", "sha256_16": digest, "length": len(value)}

    if value.startswith(("http://", "https://")):
        return _sanitize_url(value)

    if lowered_key.endswith("url") or lowered_key.endswith("uri"):
        return _sanitize_url(value)

    return value


class LocalHistoryRecorder:
    def __init__(self, base_dir: Optional[str] = None, *, enabled: bool = True) -> None:
        self.enabled = enabled
        self.base_dir = Path(base_dir).expanduser() if base_dir else _default_history_dir()
        self.runs_dir = self.base_dir / "runs"
        self.failed_dir = self.base_dir / "failed_submissions"
        self.assets_dir = self.base_dir / "assets"
        self.inputs_dir = self.base_dir / "inputs"
        self.prompts_dir = self.base_dir / "prompts"
        self._lock = threading.Lock()

    @classmethod
    def from_env(cls) -> "LocalHistoryRecorder":
        enabled = os.getenv("ATLASCLOUD_HISTORY_ENABLED", "1").strip().lower() not in {"0", "false", "no", "off"}
        base_dir = os.getenv("ATLASCLOUD_HISTORY_DIR", "").strip() or None
        return cls(base_dir=base_dir, enabled=enabled)

    def ensure_ready(self) -> None:
        if not self.enabled:
            return
        self._migrate_legacy_history_if_needed()
        self.runs_dir.mkdir(parents=True, exist_ok=True)
        self.failed_dir.mkdir(parents=True, exist_ok=True)
        self.assets_dir.mkdir(parents=True, exist_ok=True)
        self.inputs_dir.mkdir(parents=True, exist_ok=True)
        self.prompts_dir.mkdir(parents=True, exist_ok=True)

    def history_dir(self) -> str:
        return str(self.base_dir)

    def _migrate_legacy_history_if_needed(self) -> None:
        legacy_dir = _legacy_history_dir()
        try:
            if legacy_dir.resolve() == self.base_dir.resolve():
                return
        except Exception:
            pass

        if _has_history_data(self.base_dir):
            return
        if not _has_history_data(legacy_dir):
            return

        self.base_dir.parent.mkdir(parents=True, exist_ok=True)
        try:
            shutil.copytree(legacy_dir, self.base_dir, dirs_exist_ok=True)
        except Exception as exc:
            print(f"[AtlasHistory] failed to migrate legacy history from {legacy_dir} to {self.base_dir}: {exc}", flush=True)

    def list_runs(self, *, limit: int = 50) -> List[Dict[str, Any]]:
        if not self.enabled:
            return []
        try:
            self.ensure_ready()
            files = sorted(self.runs_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
            items: List[Dict[str, Any]] = []
            for path in files[: max(1, int(limit))]:
                doc = json.loads(path.read_text(encoding="utf-8"))
                items.append(
                    {
                        "prediction_id": doc.get("prediction_id") or path.stem,
                        "request_kind": doc.get("request_kind") or "",
                        "submitted_at": doc.get("submitted_at") or "",
                        "updated_at": doc.get("updated_at") or "",
                        "latest_status": doc.get("latest_status") or "",
                        "node_context": doc.get("node_context") or {},
                        "model": ((doc.get("payload") or {}).get("model") if isinstance(doc.get("payload"), dict) else ""),
                        "prompt_preview": self._prompt_preview(doc),
                        "output_preview": self._output_preview(doc),
                        "local_asset_count": len(doc.get("downloaded_assets") or []),
                        "local_input_count": len(doc.get("input_downloaded_assets") or []),
                    }
                )
            return items
        except Exception as exc:
            print(f"[AtlasHistory] failed to list runs: {exc}", flush=True)
            return []

    def get_run(self, prediction_id: str) -> Optional[Dict[str, Any]]:
        return self._safe_load_run(prediction_id)

    def refresh_downloaded_assets(self, prediction_id: str) -> Optional[Dict[str, Any]]:
        doc = self._safe_load_run(prediction_id)
        if not doc:
            return None
        payload = doc.get("payload") if isinstance(doc.get("payload"), dict) else {}
        doc["prompt_text"] = self._extract_prompt_text(payload)
        doc["prompt_file"] = self._write_prompt_file(prediction_id, doc["prompt_text"])
        doc["input_downloaded_assets"] = self._download_input_assets(prediction_id=prediction_id, payload=payload)
        outputs = doc.get("outputs") if isinstance(doc.get("outputs"), list) else []
        if self._needs_output_recovery(outputs):
            recovered_outputs = self._recover_outputs_from_prediction(doc)
            if recovered_outputs:
                outputs = recovered_outputs
        if not outputs:
            doc["updated_at"] = _utc_now()
            self._safe_write_run(prediction_id, doc)
            return doc
        doc["downloaded_assets"] = self._download_outputs(
            prediction_id=prediction_id,
            request_kind=str(doc.get("request_kind") or ""),
            payload=payload,
            outputs=outputs,
        )
        doc["updated_at"] = _utc_now()
        self._safe_write_run(prediction_id, doc)
        return doc

    def asset_path(self, prediction_id: str, filename: str) -> Optional[Path]:
        path = (self.assets_dir / prediction_id / filename).resolve()
        try:
            path.relative_to((self.assets_dir / prediction_id).resolve())
        except Exception:
            return None
        return path if path.exists() else None

    def input_asset_path(self, prediction_id: str, filename: str) -> Optional[Path]:
        path = (self.inputs_dir / prediction_id / filename).resolve()
        try:
            path.relative_to((self.inputs_dir / prediction_id).resolve())
        except Exception:
            return None
        return path if path.exists() else None

    def record_submission(
        self,
        *,
        prediction_id: str,
        request_kind: str,
        payload: Dict[str, Any],
        node_context: Optional[Dict[str, Any]] = None,
        tracking_params: Optional[Dict[str, str]] = None,
        base_url: Optional[str] = None,
    ) -> None:
        doc = {
            "history_version": 1,
            "run_id": str(uuid.uuid4()),
            "prediction_id": prediction_id,
            "request_kind": request_kind,
            "submitted_at": _utc_now(),
            "updated_at": _utc_now(),
            "node_context": node_context or {},
            "tracking_params": dict(tracking_params or {}),
            "base_url": base_url or "",
            "payload": _sanitize_value("payload", payload),
            "status_history": [{"status": "submitted", "timestamp": _utc_now()}],
            "latest_status": "submitted",
        }
        doc["prompt_text"] = self._extract_prompt_text(payload)
        doc["prompt_file"] = self._write_prompt_file(prediction_id, doc["prompt_text"])
        doc["input_downloaded_assets"] = self._download_input_assets(prediction_id=prediction_id, payload=payload)
        self._safe_write_run(prediction_id, doc)

    def record_submission_error(
        self,
        *,
        request_kind: str,
        payload: Dict[str, Any],
        error_message: str,
        node_context: Optional[Dict[str, Any]] = None,
        tracking_params: Optional[Dict[str, str]] = None,
        base_url: Optional[str] = None,
    ) -> None:
        self._safe_write_failed(
            {
                "history_version": 1,
                "run_id": str(uuid.uuid4()),
                "request_kind": request_kind,
                "failed_at": _utc_now(),
                "node_context": node_context or {},
                "tracking_params": dict(tracking_params or {}),
                "base_url": base_url or "",
                "payload": _sanitize_value("payload", payload),
                "error_message": error_message,
                "latest_status": "submit_failed",
            }
        )

    def record_poll_status(self, prediction_id: str, status: str, response_data: Optional[Dict[str, Any]] = None) -> None:
        doc = self._safe_load_run(prediction_id)
        if not doc:
            return
        if doc.get("latest_status") == status:
            return
        status_history = list(doc.get("status_history") or [])
        status_history.append({"status": status, "timestamp": _utc_now()})
        doc["status_history"] = status_history
        doc["latest_status"] = status
        doc["updated_at"] = _utc_now()
        if response_data is not None:
            doc["latest_response"] = _sanitize_value("response", response_data)
        self._safe_write_run(prediction_id, doc)

    def record_completion(self, prediction_id: str, response_data: Optional[Dict[str, Any]] = None) -> None:
        doc = self._safe_load_run(prediction_id)
        if not doc:
            return
        data = (response_data or {}).get("data") if isinstance(response_data, dict) else {}
        doc["completed_at"] = _utc_now()
        doc["updated_at"] = _utc_now()
        doc["latest_status"] = str((data or {}).get("status") or "completed")
        doc["outputs"] = _sanitize_value("outputs", (data or {}).get("outputs") or [])
        doc["result"] = _sanitize_value("response", response_data or {})
        doc["downloaded_assets"] = self._download_outputs(
            prediction_id=prediction_id,
            request_kind=str(doc.get("request_kind") or ""),
            payload=doc.get("payload") if isinstance(doc.get("payload"), dict) else {},
            outputs=(data or {}).get("outputs") or [],
        )
        self._safe_write_run(prediction_id, doc)

    def record_failure(
        self,
        prediction_id: str,
        *,
        error_message: str,
        response_data: Optional[Dict[str, Any]] = None,
    ) -> None:
        doc = self._safe_load_run(prediction_id)
        if not doc:
            return
        doc["failed_at"] = _utc_now()
        doc["updated_at"] = _utc_now()
        doc["latest_status"] = "failed"
        doc["error_message"] = error_message
        if response_data is not None:
            doc["result"] = _sanitize_value("response", response_data)
        self._safe_write_run(prediction_id, doc)

    def _run_path(self, prediction_id: str) -> Path:
        return self.runs_dir / f"{prediction_id}.json"

    def _asset_dir(self, prediction_id: str) -> Path:
        return self.assets_dir / prediction_id

    def _input_dir(self, prediction_id: str) -> Path:
        return self.inputs_dir / prediction_id

    def _prompt_dir(self, prediction_id: str) -> Path:
        return self.prompts_dir / prediction_id

    @staticmethod
    def _prompt_preview(doc: Dict[str, Any]) -> str:
        payload = doc.get("payload") if isinstance(doc, dict) else {}
        prompt = ""
        if isinstance(payload, dict):
            prompt = str(payload.get("prompt") or payload.get("negative_prompt") or "").strip()
        return prompt[:120]

    @staticmethod
    def _output_preview(doc: Dict[str, Any]) -> str:
        downloaded_assets = doc.get("downloaded_assets")
        if isinstance(downloaded_assets, list) and downloaded_assets:
            local_rel = str((downloaded_assets[0] or {}).get("local_relpath") or "").strip()
            if local_rel:
                return local_rel
        outputs = doc.get("outputs")
        if isinstance(outputs, list) and outputs:
            return str(outputs[0])
        return ""

    def _download_outputs(
        self,
        *,
        prediction_id: str,
        request_kind: str,
        payload: Dict[str, Any],
        outputs: List[Any],
    ) -> List[Dict[str, Any]]:
        assets: List[Dict[str, Any]] = []
        if not isinstance(outputs, list):
            return assets

        asset_dir = self._asset_dir(prediction_id)
        asset_dir.mkdir(parents=True, exist_ok=True)

        for index, output in enumerate(outputs):
            try:
                asset = self._download_single_output(
                    asset_dir=asset_dir,
                    prediction_id=prediction_id,
                    index=index,
                    output=output,
                    request_kind=request_kind,
                    payload=payload,
                )
                if asset:
                    assets.append(asset)
            except Exception as exc:
                assets.append(
                    {
                        "index": index,
                        "status": "failed",
                        "error": str(exc),
                    }
                )
        return assets

    @staticmethod
    def _needs_output_recovery(outputs: List[Any]) -> bool:
        if not outputs:
            return False
        return all(isinstance(item, dict) and item.get("kind") == "large_string" for item in outputs)

    def _recover_outputs_from_prediction(self, doc: Dict[str, Any]) -> List[Any]:
        prediction_id = str(doc.get("prediction_id") or "").strip()
        if not prediction_id:
            return []

        api_key = os.getenv("ATLASCLOUD_API_KEY", "").strip()
        if not api_key:
            return []

        base_url = str(doc.get("base_url") or "https://api.atlascloud.ai").rstrip("/")
        tracking_params = doc.get("tracking_params") if isinstance(doc.get("tracking_params"), dict) else {}
        try:
            import requests

            response = requests.get(
                f"{base_url}/api/v1/model/prediction/{prediction_id}",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "X-Atlas-Client": "comfyui",
                    "X-Atlas-Source": "github-readme",
                },
                params=tracking_params,
                timeout=60,
            )
            response.raise_for_status()
            data = response.json()
            outputs = ((data.get("data") or {}).get("outputs") or [])
            if isinstance(outputs, list):
                return outputs
        except Exception as exc:
            print(f"[AtlasHistory] failed to recover outputs for {prediction_id}: {exc}", flush=True)
        return []

    def _download_input_assets(self, *, prediction_id: str, payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        assets: List[Dict[str, Any]] = []
        input_dir = self._input_dir(prediction_id)
        input_dir.mkdir(parents=True, exist_ok=True)

        candidates: List[tuple[str, str, str]] = []
        def push_asset(label: str, value: Any, mime_hint: str = "") -> None:
            if isinstance(value, str) and value.strip():
                candidates.append((label, value.strip(), mime_hint))

        push_asset("image_url", payload.get("image_url"), "image/png")
        push_asset("video_url", payload.get("video_url"), "video/mp4")
        push_asset("audio_url", payload.get("audio_url"), "audio/mpeg")
        for index, url in enumerate(payload.get("images") or []):
            push_asset(f"images_{index}", url, "image/png")
        for index, url in enumerate(payload.get("videos") or []):
            push_asset(f"videos_{index}", url, "video/mp4")
        for index, url in enumerate(payload.get("audios") or []):
            push_asset(f"audios_{index}", url, "audio/mpeg")

        for index, (label, url, mime_hint) in enumerate(candidates):
            try:
                ext = _guess_extension_from_url(url, mimetypes.guess_extension(mime_hint or "") or ".bin")
                filename = f"{index:02d}_{label}{ext}"
                local_path = input_dir / filename
                with urlopen(url, timeout=120) as response:
                    content = response.read()
                    mime_type = response.headers.get_content_type() if hasattr(response.headers, "get_content_type") else mime_hint
                local_path.write_bytes(content)
                assets.append(
                    {
                        "index": index,
                        "label": label,
                        "status": "downloaded",
                        "source_type": "url",
                        "source_url": _sanitize_url(url),
                        "mime_type": mime_type,
                        "size_bytes": len(content),
                        "filename": filename,
                        "local_path": str(local_path),
                        "local_relpath": str(local_path.relative_to(self.base_dir)),
                        "serve_path": f"/api/atlas/history/input-assets/{prediction_id}/{filename}",
                    }
                )
            except Exception as exc:
                assets.append(
                    {
                        "index": index,
                        "label": label,
                        "status": "failed",
                        "error": str(exc),
                        "source_url": _sanitize_url(url),
                    }
                )
        return assets

    def _download_single_output(
        self,
        *,
        asset_dir: Path,
        prediction_id: str,
        index: int,
        output: Any,
        request_kind: str,
        payload: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        ext = _default_extension(request_kind, payload)
        filename = f"{index:02d}{ext}"

        if isinstance(output, str) and output.startswith(("http://", "https://")):
            ext = _guess_extension_from_url(output, ext)
            filename = f"{index:02d}{ext}"
            local_path = asset_dir / filename
            with urlopen(output, timeout=120) as response:
                content = response.read()
                mime_type = response.headers.get_content_type() if hasattr(response.headers, "get_content_type") else ""
            local_path.write_bytes(content)
            return {
                "index": index,
                "status": "downloaded",
                "source_type": "url",
                "source_url": _sanitize_url(output),
                "mime_type": mime_type,
                "size_bytes": len(content),
                "filename": filename,
                "local_path": str(local_path),
                "local_relpath": str(local_path.relative_to(self.base_dir)),
                "serve_path": f"/api/atlas/history/assets/{prediction_id}/{filename}",
            }

        if isinstance(output, str):
            mime_type, raw_bytes = self._decode_output_string(output, request_kind, payload)
            guessed_ext = mimetypes.guess_extension(mime_type or "") or ext
            filename = f"{index:02d}{guessed_ext}"
            local_path = asset_dir / filename
            local_path.write_bytes(raw_bytes)
            return {
                "index": index,
                "status": "downloaded",
                "source_type": "inline",
                "mime_type": mime_type,
                "size_bytes": len(raw_bytes),
                "filename": filename,
                "local_path": str(local_path),
                "local_relpath": str(local_path.relative_to(self.base_dir)),
                "serve_path": f"/api/atlas/history/assets/{prediction_id}/{filename}",
            }

        return None

    @staticmethod
    def _decode_output_string(output: str, request_kind: str, payload: Dict[str, Any]) -> tuple[str, bytes]:
        if output.startswith("data:"):
            header, encoded = output.split(",", 1)
            mime_type = header.split(";")[0][5:] or ("image/png" if request_kind == "image" else "video/mp4")
            return mime_type, base64.b64decode(encoded)

        mime_type = mimetypes.guess_type("file" + _default_extension(request_kind, payload))[0] or (
            "image/png" if request_kind == "image" else "video/mp4"
        )
        return mime_type, base64.b64decode(output)

    @staticmethod
    def _extract_prompt_text(payload: Dict[str, Any]) -> str:
        parts: List[str] = []
        prompt = str(payload.get("prompt") or "").strip()
        negative_prompt = str(payload.get("negative_prompt") or "").strip()
        if prompt:
            parts.append(f"Prompt:\n{prompt}")
        if negative_prompt:
            parts.append(f"Negative Prompt:\n{negative_prompt}")
        return "\n\n".join(parts)

    def _write_prompt_file(self, prediction_id: str, prompt_text: str) -> Dict[str, Any]:
        prompt_dir = self._prompt_dir(prediction_id)
        prompt_dir.mkdir(parents=True, exist_ok=True)
        local_path = prompt_dir / "prompt.txt"
        local_path.write_text(prompt_text or "", encoding="utf-8")
        return {
            "filename": "prompt.txt",
            "local_path": str(local_path),
            "local_relpath": str(local_path.relative_to(self.base_dir)),
            "serve_path": f"/api/atlas/history/prompts/{prediction_id}/prompt.txt",
        }

    def _safe_load_run(self, prediction_id: str) -> Optional[Dict[str, Any]]:
        if not self.enabled:
            return None
        try:
            self.ensure_ready()
            path = self._run_path(prediction_id)
            if not path.exists():
                return None
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            print(f"[AtlasHistory] failed to load run {prediction_id}: {exc}", flush=True)
            return None

    def _safe_write_run(self, prediction_id: str, doc: Dict[str, Any]) -> None:
        if not self.enabled:
            return
        try:
            self.ensure_ready()
            with self._lock:
                path = self._run_path(prediction_id)
                path.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception as exc:
            print(f"[AtlasHistory] failed to write run {prediction_id}: {exc}", flush=True)

    def _safe_write_failed(self, doc: Dict[str, Any]) -> None:
        if not self.enabled:
            return
        try:
            self.ensure_ready()
            filename = f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}_{doc['run_id']}.json"
            with self._lock:
                path = self.failed_dir / filename
                path.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception as exc:
            print(f"[AtlasHistory] failed to write failed submission: {exc}", flush=True)
