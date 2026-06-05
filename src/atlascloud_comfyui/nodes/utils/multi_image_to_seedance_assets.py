from __future__ import annotations

import io
from typing import List

from ..auth.atlas_client_node import AtlasClientHandle


def _comfy_image_to_png_bytes(image) -> bytes:
    import numpy as np
    from PIL import Image

    if image is None:
        raise RuntimeError("image is None")

    arr = image[0].detach().cpu().numpy()
    arr = (arr * 255.0).clip(0, 255).astype(np.uint8)
    pil = Image.fromarray(arr, mode="RGB")
    buf = io.BytesIO()
    pil.save(buf, format="PNG")
    return buf.getvalue()


class AtlasMultiImageToSeedanceAssets:
    """Upload local images, register them in the Seedance Asset Library,
    and return newline-separated asset:// refs.
    """

    CATEGORY = "AtlasCloud/Utils"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "INT")
    RETURN_NAMES = ("asset_references", "count")

    MAX_IMAGES = 8

    @classmethod
    def INPUT_TYPES(cls):
        optional = {
            "refs": (
                "STRING",
                {
                    "default": "",
                    "multiline": True,
                    "tooltip": "Existing refs, one per line: asset://... or public http(s) URLs. URLs will be registered as Seedance assets.",
                },
            ),
            "poll_interval_sec": (
                "FLOAT",
                {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Asset polling interval in seconds"},
            ),
            "timeout_sec": (
                "INT",
                {"default": 300, "min": 30, "max": 3600, "tooltip": "Asset registration timeout in seconds"},
            ),
        }
        optional.update(
            {
                f"image_{i}": (
                    "IMAGE",
                    {"tooltip": f"Local/uploaded image {i}; uploaded then registered as a Seedance asset"},
                )
                for i in range(1, cls.MAX_IMAGES + 1)
            }
        )
        return {"required": {"atlas_client": ("ATLAS_CLIENT",)}, "optional": optional}

    def _register_url(self, client, value: str, *, poll_interval_sec: float, timeout_sec: int) -> str:
        asset = client.register_seedance_asset(url=value, asset_type="Image")
        asset_id = str(asset.get("id") or "").strip()
        ready = client.wait_for_seedance_asset_active(
            asset_id,
            poll_interval_sec=float(poll_interval_sec),
            timeout_sec=float(timeout_sec),
        )
        asset_ref_id = (
            str(ready.get("atlas_asset_id") or "").strip()
            or str(ready.get("ark_asset_id") or "").strip()
            or asset_id
        )
        if not asset_ref_id:
            raise RuntimeError(f"Seedance asset registration returned no usable asset id: {ready}")
        return f"asset://{asset_ref_id}"

    def run(
        self,
        atlas_client: AtlasClientHandle,
        refs: str = "",
        poll_interval_sec: float = 2.0,
        timeout_sec: int = 300,
        **kwargs,
    ):
        client = atlas_client.client
        out: List[str] = []

        for line in (refs or "").splitlines():
            value = line.strip()
            if not value:
                continue
            if value.startswith("asset://"):
                out.append(value)
                continue
            if value.startswith("http://") or value.startswith("https://"):
                out.append(
                    self._register_url(
                        client,
                        value,
                        poll_interval_sec=float(poll_interval_sec),
                        timeout_sec=int(timeout_sec),
                    )
                )
                continue
            if value.startswith("data:"):
                raise RuntimeError(
                    "Seedance asset registration does not accept data URLs directly. Connect IMAGE inputs or use public http(s) URLs."
                )
            raise RuntimeError(f"Unsupported ref format for Seedance assets: {value}")

        for i in range(1, self.MAX_IMAGES + 1):
            img = kwargs.get(f"image_{i}")
            if img is None:
                continue
            try:
                batch = img.shape[0]
            except Exception:
                batch = 1

            for b in range(batch):
                png_bytes = _comfy_image_to_png_bytes(img[b : b + 1])
                uploaded = client.upload_media_bytes(
                    png_bytes,
                    filename=f"seedance_ref_{i}_{b + 1}.png",
                    mime_type="image/png",
                )
                download_url = str(uploaded.get("download_url") or "").strip()
                if not download_url:
                    raise RuntimeError(f"uploadMedia returned no download_url: {uploaded}")
                out.append(
                    self._register_url(
                        client,
                        download_url,
                        poll_interval_sec=float(poll_interval_sec),
                        timeout_sec=int(timeout_sec),
                    )
                )

        if not out:
            raise RuntimeError("Provide at least one reference: connect an image, or fill `refs` with asset:// or public URLs")
        return ("\n".join(out), len(out))


NODE_CLASS_MAPPINGS = {
    "AtlasCloud Multi Image to Seedance Assets": AtlasMultiImageToSeedanceAssets,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "AtlasCloud Multi Image to Seedance Assets": "AtlasCloud Multi Image to Seedance Assets",
}
