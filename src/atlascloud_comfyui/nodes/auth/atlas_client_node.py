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
            "required": {},
            "optional": {
                # Kept so old workflows still load; the web extension hides it, moves any key
                # found in it to local storage and always saves it blank.
                "api_key": (
                    "STRING",
                    {"default": "", "tooltip": "Leave blank: use the Set API key button or ATLASCLOUD_API_KEY"},
                ),
                "base_url": ("STRING", {"default": "https://api.atlascloud.ai"}),
            },
        }

    def create(self, api_key: str = "", base_url: str = "https://api.atlascloud.ai"):
        api_key = (api_key or "").strip()

        if not api_key:
            client = AtlasClient.from_env(base_url=base_url)
        else:
            client = AtlasClient(api_key=api_key, base_url=base_url)

        return (AtlasClientHandle(client=client),)
