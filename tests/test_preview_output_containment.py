"""Preview nodes must not write outside ComfyUI's output directory.

`subfolder` and `filename_prefix` come from workflow widget values; they used to
be joined onto the output root with only leading/trailing slashes stripped, so
``../..`` climbed out and the downloaded bytes landed at an arbitrary path.
"""

import sys
import types
from pathlib import Path

import pytest

from atlascloud_comfyui.nodes.utils import video_previewer
from atlascloud_comfyui.nodes.utils.safe_paths import resolve_output_subdir, safe_filename_prefix


@pytest.fixture()
def out_root(tmp_path: Path, monkeypatch) -> Path:
    root = tmp_path / "output"
    root.mkdir()
    fp = types.SimpleNamespace(get_output_directory=lambda: str(root))
    monkeypatch.setitem(sys.modules, "folder_paths", fp)
    return root


@pytest.mark.parametrize("sub", ["../escape", "a/../../escape", "..", "/abs/path", "\\\\srv\\share", "a/\x00b", "C:/x"])
def test_resolve_rejects_traversal(out_root: Path, sub: str) -> None:
    with pytest.raises(RuntimeError):
        resolve_output_subdir(str(out_root), sub)


def test_resolve_allows_nested_relative(out_root: Path) -> None:
    sub, path = resolve_output_subdir(str(out_root), "atlas/videos/")
    assert sub == "atlas/videos"
    assert Path(path) == (out_root / "atlas" / "videos").resolve()


def test_resolve_rejects_symlink_escape(out_root: Path, tmp_path: Path) -> None:
    outside = tmp_path / "outside"
    outside.mkdir()
    (out_root / "link").symlink_to(outside, target_is_directory=True)
    with pytest.raises(RuntimeError):
        resolve_output_subdir(str(out_root), "link/x")


@pytest.mark.parametrize("prefix", ["../x", "a/b", "a\\b", "..", "x\x00"])
def test_prefix_rejects_separators(prefix: str) -> None:
    with pytest.raises(RuntimeError):
        safe_filename_prefix(prefix)


def test_video_node_writes_nothing_outside_root(out_root: Path, tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(video_previewer, "_download_file", lambda url, dst, timeout_sec=120: Path(dst).write_bytes(b"x"))
    node = video_previewer.AtlasVideoPreviewer()
    with pytest.raises(RuntimeError):
        node.run("https://example.com/v.mp4", "../../escape", "AtlasVideo")
    with pytest.raises(RuntimeError):
        node.run("https://example.com/v.mp4", "ok", "../../evil")
    assert not (tmp_path / "escape").exists()
    ok = node.run("https://example.com/v.mp4", "ok/sub", "AtlasVideo")
    assert Path(ok["result"][0]).resolve().is_relative_to(out_root.resolve())
