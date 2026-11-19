from __future__ import annotations

from typing import Any, Dict

from .local_history import LocalHistoryRecorder, _is_safe_path_segment

_REGISTERED = False

try:
    from aiohttp import web
    from server import PromptServer
except Exception:  # pragma: no cover - only available inside ComfyUI runtime
    PromptServer = None
    web = None


def _is_local_request(request) -> bool:
    """Whether the request came from the loopback interface.

    ComfyUI ships no token auth: its own protection for state-changing routes
    is ``create_origin_only_middleware`` plus ``is_loopback`` (server.py), and
    that middleware is skipped entirely when the user passes
    ``--enable-cors-header``. This route downloads and writes files, so it
    applies the same loopback rule directly rather than relying on a
    middleware that may be disabled. Falls back to allowing the request only
    when ComfyUI's own helper is unavailable, so behaviour never becomes
    stricter than the host it runs in.
    """
    try:
        from server import is_loopback  # type: ignore
    except Exception:
        return True
    peer = request.transport.get_extra_info("peername") if request.transport else None
    host = peer[0] if peer else None
    if host is None:
        forwarded = request.headers.get("X-Forwarded-For")
        host = forwarded.split(",")[0].strip() if forwarded else None
    return bool(host) and bool(is_loopback(host))


def _json_response(data: Dict[str, Any], status: int = 200):
    if web is None:
        raise RuntimeError("aiohttp is unavailable")
    return web.json_response(data, status=status)


def register_history_routes() -> bool:
    global _REGISTERED
    if PromptServer is None or web is None:
        return False

    if _REGISTERED:
        return True

    routes = PromptServer.instance.routes

    recorder = LocalHistoryRecorder.from_env()

    @routes.get("/atlas/history/runs")
    async def atlas_history_runs(request):
        limit_raw = request.rel_url.query.get("limit", "50")
        try:
            limit = max(1, min(200, int(limit_raw)))
        except Exception:
            limit = 50
        return _json_response(
            {
                "items": recorder.list_runs(limit=limit),
                "history_dir": recorder.history_dir(),
            }
        )

    @routes.get("/atlas/history/runs/{prediction_id}")
    async def atlas_history_run_detail(request):
        prediction_id = (request.match_info.get("prediction_id") or "").strip()
        if not prediction_id:
            return _json_response({"error": "prediction_id is required"}, status=400)
        if not _is_safe_path_segment(prediction_id):
            return _json_response({"error": "invalid prediction_id"}, status=400)
        doc = recorder.get_run(prediction_id)
        if doc is None:
            return _json_response({"error": "run not found", "prediction_id": prediction_id}, status=404)
        return _json_response({"item": doc, "history_dir": recorder.history_dir()})

    @routes.get("/atlas/history/assets/{prediction_id}/{filename}")
    async def atlas_history_asset(request):
        prediction_id = (request.match_info.get("prediction_id") or "").strip()
        filename = (request.match_info.get("filename") or "").strip()
        if not prediction_id or not filename:
            return _json_response({"error": "prediction_id and filename are required"}, status=400)
        if not _is_safe_path_segment(prediction_id) or not _is_safe_path_segment(filename):
            return _json_response({"error": "invalid prediction_id or filename"}, status=400)
        path = recorder.asset_path(prediction_id, filename)
        if path is None:
            return _json_response({"error": "asset not found", "prediction_id": prediction_id, "filename": filename}, status=404)
        return web.FileResponse(path)

    @routes.get("/atlas/history/input-assets/{prediction_id}/{filename}")
    async def atlas_history_input_asset(request):
        prediction_id = (request.match_info.get("prediction_id") or "").strip()
        filename = (request.match_info.get("filename") or "").strip()
        if not prediction_id or not filename:
            return _json_response({"error": "prediction_id and filename are required"}, status=400)
        if not _is_safe_path_segment(prediction_id) or not _is_safe_path_segment(filename):
            return _json_response({"error": "invalid prediction_id or filename"}, status=400)
        path = recorder.input_asset_path(prediction_id, filename)
        if path is None:
            return _json_response({"error": "input asset not found", "prediction_id": prediction_id, "filename": filename}, status=404)
        return web.FileResponse(path)

    @routes.get("/atlas/history/prompts/{prediction_id}/prompt.txt")
    async def atlas_history_prompt_file(request):
        prediction_id = (request.match_info.get("prediction_id") or "").strip()
        if not prediction_id:
            return _json_response({"error": "prediction_id is required"}, status=400)
        if not _is_safe_path_segment(prediction_id):
            return _json_response({"error": "invalid prediction_id"}, status=400)
        doc = recorder.get_run(prediction_id)
        if doc is None:
            return _json_response({"error": "run not found", "prediction_id": prediction_id}, status=404)
        prompt_file = (doc.get("prompt_file") or {}).get("local_path")
        if not prompt_file:
            return _json_response({"error": "prompt file not found", "prediction_id": prediction_id}, status=404)
        return web.FileResponse(prompt_file)

    @routes.post("/atlas/history/runs/{prediction_id}/refresh-assets")
    async def atlas_history_refresh_assets(request):
        # Downloads remote assets and writes them to disk: keep it to local
        # callers, matching ComfyUI's own rule for state-changing routes.
        if not _is_local_request(request):
            return _json_response({"error": "forbidden"}, status=403)
        prediction_id = (request.match_info.get("prediction_id") or "").strip()
        if not prediction_id:
            return _json_response({"error": "prediction_id is required"}, status=400)
        if not _is_safe_path_segment(prediction_id):
            return _json_response({"error": "invalid prediction_id"}, status=400)
        doc = recorder.refresh_downloaded_assets(prediction_id)
        if doc is None:
            return _json_response({"error": "run not found", "prediction_id": prediction_id}, status=404)
        return _json_response({"item": doc, "history_dir": recorder.history_dir()})

    _REGISTERED = True
    return True


register_history_routes()
