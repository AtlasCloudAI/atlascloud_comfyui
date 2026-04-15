from __future__ import annotations

from atlascloud_comfyui.nodes.utils.image_encode import comfy_image_to_data_url_png


class AtlasImageToBase64:
    """Convert a ComfyUI IMAGE tensor to a base64 data URL string for AtlasCloud API nodes."""

    CATEGORY = "AtlasCloud/Utils"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("image_base64",)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE", {"tooltip": "Image from Load Image or any IMAGE output"}),
            }
        }

    def run(self, image) -> tuple[str]:
        return (comfy_image_to_data_url_png(image),)
