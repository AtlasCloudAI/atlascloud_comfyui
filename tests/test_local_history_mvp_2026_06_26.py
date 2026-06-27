import json
import os
import sys
import types

import pytest

from atlascloud_comfyui.client.atlas_client import AtlasClient
from atlascloud_comfyui.history import local_history as local_history_module


class _FakeResponse:
    def __init__(self, payload, status_code=200, text=""):
        self._payload = payload
        self.status_code = status_code
        self.text = text or json.dumps(payload)

    def raise_for_status(self):
        if self.status_code >= 400:
            raise _FakeRequests.RequestException(self.text, response=self)

    def json(self):
        return self._payload


class _FakeRequests:
    class RequestException(Exception):
        def __init__(self, message, response=None):
            super().__init__(message)
            self.response = response

    def __init__(self):
        self.poll_count = 0

    def post(self, url, headers=None, json=None, params=None, timeout=None):
        return _FakeResponse({"data": {"id": "pred-test-123"}})

    def get(self, url, headers=None, params=None, timeout=None):
        self.poll_count += 1
        if self.poll_count == 1:
            return _FakeResponse({"data": {"status": "processing"}})
        return _FakeResponse(
            {
                "data": {
                    "status": "completed",
                    "outputs": ["https://example.com/output.png?signature=secret"],
                }
            }
        )


def test_local_history_writes_run_file(tmp_path, monkeypatch):
    monkeypatch.setenv("ATLASCLOUD_HISTORY_DIR", str(tmp_path / "history"))
    monkeypatch.setenv("ATLASCLOUD_HISTORY_ENABLED", "1")

    fake_requests = _FakeRequests()
    monkeypatch.setitem(sys.modules, "requests", fake_requests)

    client = AtlasClient(api_key="test-key")
    prediction_id = client.generate_image(
        {
            "model": "example/model",
            "prompt": "a small orange cat",
            "image_url": "https://example.com/input.png?token=secret",
        }
    )
    result = client.poll_prediction(prediction_id, poll_interval_sec=0, timeout_sec=1)

    run_path = tmp_path / "history" / "runs" / "pred-test-123.json"
    assert run_path.exists()

    doc = json.loads(run_path.read_text(encoding="utf-8"))
    assert doc["prediction_id"] == "pred-test-123"
    assert doc["request_kind"] == "image"
    assert doc["payload"]["prompt"] == "a small orange cat"
    assert doc["payload"]["image_url"] == "https://example.com/input.png"
    assert doc["latest_status"] == "completed"
    assert doc["outputs"] == ["https://example.com/output.png"]
    assert result["data"]["status"] == "completed"


class _FailedPredictionRequests(_FakeRequests):
    def get(self, url, headers=None, params=None, timeout=None):
        return _FakeResponse(
            {
                "data": {
                    "status": "failed",
                    "error": "duration must be between 3 and 15 seconds, got 1",
                }
            },
            status_code=500,
        )


def test_poll_prediction_surfaces_failed_status_from_http_error(tmp_path, monkeypatch):
    monkeypatch.setenv("ATLASCLOUD_HISTORY_DIR", str(tmp_path / "history"))
    monkeypatch.setenv("ATLASCLOUD_HISTORY_ENABLED", "1")

    fake_requests = _FailedPredictionRequests()
    monkeypatch.setitem(sys.modules, "requests", fake_requests)

    client = AtlasClient(api_key="test-key")
    prediction_id = client.generate_video({"model": "example/video-model", "prompt": "short clip"})

    with pytest.raises(Exception, match="duration must be between 3 and 15 seconds, got 1"):
        client.poll_prediction(prediction_id, poll_interval_sec=0, timeout_sec=1)

    run_path = tmp_path / "history" / "runs" / "pred-test-123.json"
    doc = json.loads(run_path.read_text(encoding="utf-8"))
    assert doc["latest_status"] == "failed"
    assert doc["error_message"] == "duration must be between 3 and 15 seconds, got 1"


def test_local_history_migrates_legacy_repo_dir(tmp_path, monkeypatch):
    legacy_dir = tmp_path / "legacy_local_history"
    (legacy_dir / "runs").mkdir(parents=True)
    (legacy_dir / "runs" / "legacy.json").write_text('{"prediction_id":"legacy"}', encoding="utf-8")

    target_dir = tmp_path / "standard_local_history"
    monkeypatch.setattr(local_history_module, "_legacy_history_dir", lambda: legacy_dir)

    recorder = local_history_module.LocalHistoryRecorder(base_dir=str(target_dir))
    recorder.ensure_ready()

    assert (target_dir / "runs" / "legacy.json").exists()
