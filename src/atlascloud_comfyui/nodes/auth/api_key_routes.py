from __future__ import annotations

from ...client.api_key_store import api_key_status, save_api_key

try:
    from aiohttp import web
    from server import PromptServer
except Exception:  # pragma: no cover - only available inside ComfyUI runtime
    PromptServer = None
    web = None


def register_api_key_routes() -> bool:
    if PromptServer is None or web is None:
        return False

    routes = PromptServer.instance.routes

    @routes.get("/atlas/api_key")
    async def atlas_api_key_status(request):
        return web.json_response(api_key_status())

    @routes.post("/atlas/api_key")
    async def atlas_api_key_save(request):
        body = await request.json()
        if not isinstance(body, dict) or not isinstance(body.get("api_key"), str):
            return web.json_response({"error": "api_key (string) is required"}, status=400)
        save_api_key(body["api_key"])
        return web.json_response(api_key_status())

    return True
