from __future__ import annotations

from dataclasses import dataclass

from ...client.atlas_client import AtlasClient


@dataclass(frozen=True)
class AtlasClientHandle:
    """A small wrapper so downstream nodes can accept a single typed input."""

    client: AtlasClient


class AtlasClientNode:
    CATEGORY = "AtlasCloud/Auth"
    FUNCTION = "create"
    RETURN_TYPES = ("ATLAS_CLIENT",)
    RETURN_NAMES = ("atlas_client",)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                # NOTE: this will likely be stored in workflow JSON if entered here.
                # Consider leaving it blank and using env var instead.
                "api_key": ("STRING", {"default": ""}),
            },
            "optional": {
                "base_url": ("STRING", {"default": "https://api.atlascloud.ai"}),
            },
        }

    def create(self, api_key: str, base_url: str = "https://api.atlascloud.ai"):
        api_key = (api_key or "").strip()

        # Safer fallback: if empty, use env var ATLASCLOUD_API_KEY
        if not api_key:
            client = AtlasClient.from_env(base_url=base_url)
        else:
            client = AtlasClient(api_key=api_key, base_url=base_url)

        return (AtlasClientHandle(client=client),)
