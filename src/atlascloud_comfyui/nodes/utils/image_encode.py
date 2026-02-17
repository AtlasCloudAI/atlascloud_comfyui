from __future__ import annotations

import base64
import io


def comfy_image_to_data_url_png(image) -> str:
    """
    image: torch tensor [1,H,W,3] float32 in [0,1]
    returns: data:image/png;base64,...
    """
    # runtime-only imports (CI-safe)
    import numpy as np
    from PIL import Image

    if image is None:
        raise RuntimeError("image is None")

    arr = image[0].detach().cpu().numpy()
    arr = (arr * 255.0).clip(0, 255).astype(np.uint8)
    pil = Image.fromarray(arr, mode="RGB")

    buf = io.BytesIO()
    pil.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{b64}"
