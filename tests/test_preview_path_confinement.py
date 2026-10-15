import os
import sys
import types

import pytest

from atlascloud_comfyui.nodes.utils import video_previewer
from atlascloud_comfyui.nodes.utils.video_previewer import AtlasVideoPreviewer
from atlascloud_comfyui.path_safety import confine, safe_filename_part, safe_relative_dir


@pytest.fixture
def out_dir(tmp_path, monkeypatch):
    out = tmp_path / "output"
    out.mkdir()
    fake = types.ModuleType("folder_paths")
    fake.get_output_directory = lambda: str(out)
    monkeypatch.setitem(sys.modules, "folder_paths", fake)
    monkeypatch.setattr(video_previewer, "_download_file", lambda url, dst, timeout_sec=120: open(dst, "wb").write(b"x"))
    return out


def _run(**kw):
    args = dict(video_url="https://example.com/a.mp4", subfolder="atlascloud", filename_prefix="V")
    args.update(kw)
    return AtlasVideoPreviewer().run(**args)


def test_video_normal_save_stays_inside(out_dir):
    res = _run(subfolder="a/b")
    assert os.path.realpath(res["result"][0]).startswith(os.path.realpath(out_dir) + os.sep)


@pytest.mark.parametrize("sub", ["..", "../x", "a/../../x", "a\\..\\..\\x", "/etc", "\\etc", "C:\\x"])
def test_video_rejects_bad_subfolder(out_dir, sub):
    with pytest.raises(RuntimeError):
        _run(subfolder=sub)
    assert not (out_dir.parent / "x").exists()


@pytest.mark.parametrize("prefix", ["../../evil", "..", "a/b", "a\\b"])
def test_video_rejects_bad_prefix(out_dir, prefix):
    with pytest.raises(RuntimeError):
        _run(filename_prefix=prefix)
    assert not list(out_dir.parent.glob("evil*"))


def test_video_rejects_symlink_escape(out_dir, tmp_path):
    outside = tmp_path / "outside"
    outside.mkdir()
    os.symlink(outside, out_dir / "link")
    with pytest.raises(RuntimeError):
        _run(subfolder="link")
    assert not list(outside.iterdir())


def test_helpers():
    assert safe_relative_dir("") == ""
    assert safe_relative_dir("a//b/./c") == "a/b/c"
    assert safe_filename_part("") == ""
    with pytest.raises(RuntimeError):
        confine("/tmp/../etc", "/tmp/nonexistent-base")


def _png_data_url():
    import base64
    import io

    from PIL import Image

    buf = io.BytesIO()
    Image.new("RGB", (2, 2)).save(buf, "PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def test_image_preview_confinement(out_dir):
    pytest.importorskip("torch")
    pytest.importorskip("PIL")
    from atlascloud_comfyui.nodes.utils.image_preview import AtlasImagePreviewURL

    node = AtlasImagePreviewURL()
    src = _png_data_url()
    res = node.run(source=src, subfolder="ok", filename_prefix="I")
    assert res["ui"]["images"][0]["subfolder"] == "ok"
    for kw in ({"subfolder": "../x"}, {"subfolder": "/abs"}, {"filename_prefix": "../../e"}):
        with pytest.raises(RuntimeError):
            node.run(source=src, **kw)
    assert not (out_dir.parent / "x").exists()
