"""Path-containment regression tests for the local history store.

The original implementation validated `asset_path` with
`relative_to(assets_dir / prediction_id)` — a base derived from the caller's
own input, so the base moved with the attacker and the check always passed.
These routes are reachable over HTTP, so that allowed reads (and, through
refresh-assets, writes) outside the history directory.
"""

import tempfile
from pathlib import Path

import pytest

from atlascloud_comfyui.history.local_history import LocalHistoryRecorder


@pytest.fixture()
def store(tmp_path: Path) -> LocalHistoryRecorder:
    return LocalHistoryRecorder(base_dir=str(tmp_path / "atlas_history"))


def test_legitimate_asset_is_served(store: LocalHistoryRecorder) -> None:
    asset_dir = store.assets_dir / "pred123"
    asset_dir.mkdir(parents=True)
    (asset_dir / "out.png").write_bytes(b"x")
    assert store.asset_path("pred123", "out.png") is not None


@pytest.mark.parametrize(
    "prediction_id,filename",
    [
        ("../../outside", "config.json"),
        ("..", "config.json"),
        ("..%2f..%2foutside", "config.json"),
        ("pred123", "../../../outside/config.json"),
        ("pred123", ".."),
        ("a/b", "out.png"),
    ],
)
def test_traversal_is_rejected(
    store: LocalHistoryRecorder, tmp_path: Path, prediction_id: str, filename: str
) -> None:
    outside = tmp_path / "outside"
    outside.mkdir(exist_ok=True)
    (outside / "config.json").write_text("API_KEY=secret")

    assert store.asset_path(prediction_id, filename) is None
    assert store.input_asset_path(prediction_id, filename) is None


@pytest.mark.parametrize("prediction_id", ["../../outside", "..", "a/b", "", "."])
def test_write_paths_refuse_unsafe_ids(
    store: LocalHistoryRecorder, prediction_id: str
) -> None:
    """_run_path and the per-run dirs feed writes, not just reads."""
    for builder in (
        store._run_path,
        store._asset_dir,
        store._input_dir,
        store._prompt_dir,
    ):
        with pytest.raises(ValueError):
            builder(prediction_id)


def test_safe_segment_predicate() -> None:
    from atlascloud_comfyui.history.local_history import _is_safe_path_segment

    assert _is_safe_path_segment("pred-123_ABC")
    for bad in ["", ".", "..", "a/b", "a\\b", "a%2fb", "a%5cb", "a\x00b"]:
        assert not _is_safe_path_segment(bad), bad
