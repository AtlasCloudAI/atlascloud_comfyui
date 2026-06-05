from __future__ import annotations

from atlascloud_comfyui.nodes.utils.image_encode import comfy_image_to_data_url_png


class AtlasMultiImageToBase64:
    """Build a newline-separated reference list for multi-image inputs like
    Seedance 2.0 Reference-to-Video `reference_images`, Kling R2V `images`,
    Nano Banana / GPT edit `images` (all split on newlines).

    Accepts BOTH kinds of source, treated uniformly:
      - `image_1..image_8` (IMAGE): local/uploaded images -> encoded to base64
      - `refs` (STRING, multiline): existing references passed THROUGH as-is,
        one per line — `asset://atlas-asset-...`, http(s) URLs, or base64.
        AtlasCloud accepts asset:// and URL refs directly (the backend
        resolves/auto-registers them), so there is NO need to download an
        asset/URL back into an image just to re-encode it.

    Output `references` is the combined newline-separated list (refs first,
    then encoded images), ready to wire into the reference/images field.
    """

    CATEGORY = "AtlasCloud/Utils"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "INT")
    RETURN_NAMES = ("references", "count")

    MAX_IMAGES = 8

    @classmethod
    def INPUT_TYPES(cls):
        optional = {
            "refs": ("STRING", {
                "default": "", "multiline": True,
                "tooltip": "Existing references, one per line: asset://... , http(s) URL, or base64. Passed through as-is.",
            }),
        }
        optional.update({
            f"image_{i}": ("IMAGE", {"tooltip": f"Local/uploaded image {i} (encoded to base64)"})
            for i in range(1, cls.MAX_IMAGES + 1)
        })
        return {"required": {}, "optional": optional}

    def run(self, refs: str = "", **kwargs):
        out = []
        # 1) pass-through refs (asset:// / URL / base64), one per line
        for line in (refs or "").splitlines():
            s = line.strip()
            if s:
                out.append(s)
        # 2) encode local IMAGE inputs to base64 (batches expand per-frame)
        for i in range(1, self.MAX_IMAGES + 1):
            img = kwargs.get(f"image_{i}")
            if img is None:
                continue
            try:
                batch = img.shape[0]
            except Exception:
                batch = 1
            for b in range(batch):
                out.append(comfy_image_to_data_url_png(img[b : b + 1]))
        if not out:
            raise RuntimeError("Provide at least one reference: connect an image or fill `refs`")
        return ("\n".join(out), len(out))


NODE_CLASS_MAPPINGS = {"AtlasCloud Multi Image to Base64": AtlasMultiImageToBase64}
NODE_DISPLAY_NAME_MAPPINGS = {"AtlasCloud Multi Image to Base64": "AtlasCloud Multi Image to Base64"}
