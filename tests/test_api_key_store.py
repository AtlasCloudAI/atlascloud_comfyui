"""The API key is read from the environment or a local file, never from the workflow."""

import os

import pytest

from src.atlascloud_comfyui.client import api_key_store
from src.atlascloud_comfyui.client.atlas_client import AtlasClient, AtlasError
from src.atlascloud_comfyui.nodes.auth.atlas_client_node import AtlasClientNode


@pytest.fixture
def key_file(tmp_path, monkeypatch):
    path = tmp_path / "__atlascloud" / "api_key"
    monkeypatch.setattr(api_key_store, "key_file_path", lambda: str(path))
    monkeypatch.delenv("ATLASCLOUD_API_KEY", raising=False)
    return path


def test_no_key_configured(key_file):
    assert api_key_store.load_api_key() == ""
    assert api_key_store.api_key_status() == {"configured": False, "source": None, "hint": ""}
    with pytest.raises(AtlasError, match="Set API key"):
        AtlasClient.from_env()


def test_saved_key_is_used_and_only_hinted(key_file):
    api_key_store.save_api_key("  sk-secret-1234 \n")
    assert key_file.read_text(encoding="utf-8") == "sk-secret-1234"
    assert api_key_store.api_key_status() == {"configured": True, "source": "file", "hint": "1234"}

    handle = AtlasClientNode().create()[0]
    assert handle.client.api_key == "sk-secret-1234"


@pytest.mark.skipif(os.name == "nt", reason="POSIX permissions")
def test_saved_key_is_private(key_file):
    api_key_store.save_api_key("sk-secret-1234")
    assert (key_file.stat().st_mode & 0o777) == 0o600


def test_env_var_wins_over_file(key_file, monkeypatch):
    api_key_store.save_api_key("sk-file-1111")
    monkeypatch.setenv("ATLASCLOUD_API_KEY", "sk-env-2222")
    assert api_key_store.load_api_key() == "sk-env-2222"
    assert api_key_store.api_key_status()["source"] == "env"


def test_empty_save_removes_key(key_file):
    api_key_store.save_api_key("sk-secret-1234")
    api_key_store.save_api_key("")
    assert not key_file.exists()
    assert api_key_store.load_api_key() == ""


def test_widget_key_still_works_for_api_users(key_file):
    handle = AtlasClientNode().create(api_key="sk-from-prompt")[0]
    assert handle.client.api_key == "sk-from-prompt"


def test_outside_comfyui_has_no_key_file(monkeypatch):
    monkeypatch.setitem(__import__("sys").modules, "folder_paths", None)
    assert api_key_store.key_file_path() is None
