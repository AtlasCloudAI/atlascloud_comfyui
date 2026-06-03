from __future__ import annotations

from atlascloud_comfyui.nodes.utils.image_encode import comfy_image_to_data_url_png


class AtlasMultiImageToBase64:
    """Convert up to 8 IMAGE inputs (each may be a batch) into a newline-separated
    list of base64 data URLs — ready to feed multi-image inputs like Seedance 2.0
    Reference-to-Video `reference_images`, Kling Reference-to-Video `images`, or
    Nano Banana / GPT edit `images` (all of which split on newlines).

    Connect one Load Image per reference. Empty/unconnected inputs are skipped.
    Batched IMAGE inputs are expanded frame-by-frame, one base64 per line.
    """

    CATEGORY = "AtlasCloud/Utils"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "INT")
    RETURN_NAMES = ("images_base64", "count")

    MAX_IMAGES = 8

    @classmethod
    def INPUT_TYPES(cls):
        required = {"image_1": ("IMAGE", {"tooltip": "Reference image 1 (required)"})}
        optional = {
            f"image_{i}": ("IMAGE", {"tooltip": f"Reference image {i} (optional)"})
            for i in range(2, cls.MAX_IMAGES + 1)
        }
        return {"required": required, "optional": optional}

    def run(self, image_1, **kwargs):
        ordered = [image_1] + [kwargs.get(f"image_{i}") for i in range(2, self.MAX_IMAGES + 1)]
        urls = []
        for img in ordered:
            if img is None:
                continue
            # img: torch tensor [B,H,W,3]; expand each frame to its own base64
            try:
                batch = img.shape[0]
            except Exception:
                batch = 1
            for b in range(batch):
                urls.append(comfy_image_to_data_url_png(img[b : b + 1]))
        if not urls:
            raise RuntimeError("At least one image is required")
        return ("\n".join(urls), len(urls))


NODE_CLASS_MAPPINGS = {"AtlasCloud Multi Image to Base64": AtlasMultiImageToBase64}
NODE_DISPLAY_NAME_MAPPINGS = {"AtlasCloud Multi Image to Base64": "AtlasCloud Multi Image to Base64"}
