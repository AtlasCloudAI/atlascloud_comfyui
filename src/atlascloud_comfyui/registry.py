"""
ComfyUI node registry.

Design goal:
- Always expose NODE_CLASS_MAPPINGS for tooling/CI (e.g. comfy-org/node-diff)
- Avoid import-time hard dependency on ComfyUI-only modules (folder_paths/comfy)
  by moving those imports into node.run() where needed.
"""

from __future__ import annotations

from typing import Dict, Type, Any


# --- Import node classes (should be import-safe in CI)
# IMPORTANT: Node modules should NOT import folder_paths/comfy/requests at top-level.
# Move those imports inside run().

from atlascloud_comfyui.nodes.auth.atlas_client_node import AtlasClientNode

from atlascloud_comfyui.nodes.video.wan26_t2v import AtlasWAN26TextToVideo
from atlascloud_comfyui.nodes.video.wan25_t2v import AtlasWAN25TextToVideo
from atlascloud_comfyui.nodes.video.wan22_t2v_720p import AtlasWAN22T2V720p
from atlascloud_comfyui.nodes.video.veo31_t2v import AtlasVeo31TextToVideo
from atlascloud_comfyui.nodes.video.kling_v26_pro_t2v import AtlasKlingV26ProTextToVideo
from atlascloud_comfyui.nodes.video.kling_video_o1_t2v import AtlasKlingVideoO1TextToVideo
from atlascloud_comfyui.nodes.video.seedance_v1_pro_t2v_1080p import AtlasSeedanceV1ProT2V1080p
from atlascloud_comfyui.nodes.video.hailuo_23_t2v_pro import AtlasHailuo23T2VPro

from atlascloud_comfyui.nodes.image.seedream_v45_t2i import AtlasSeedreamV45TextToImage
from atlascloud_comfyui.nodes.image.zimage_turbo_lora_t2i import AtlasZImageTurboLoraTextToImage
from atlascloud_comfyui.nodes.image.nano_banana_pro_t2i_ultra import AtlasNanoBananaProTextToImageUltra
from atlascloud_comfyui.nodes.image.flux2_flex_t2i import AtlasFlux2FlexTextToImage

from atlascloud_comfyui.nodes.utils.image_preview import AtlasImagePreviewURL
from atlascloud_comfyui.nodes.utils.video_previewer import AtlasVideoPreviewer


NODE_CLASS_MAPPINGS: Dict[str, Type[Any]] = {
    "AtlasCloud Client": AtlasClientNode,
    "AtlasCloud WAN2.5 Text-to-Video": AtlasWAN25TextToVideo,
    "AtlasCloud WAN2.6 Text-to-Video": AtlasWAN26TextToVideo,
    "AtlasCloud WAN2.2 Text-to-Video 720p": AtlasWAN22T2V720p,
    "AtlasCloud VEO3.1 Text-to-Video": AtlasVeo31TextToVideo,
    "AtlasCloud Kling V2.6 Pro Text-to-Video": AtlasKlingV26ProTextToVideo,
    "AtlasCloud Kling Video O1 Text-to-Video": AtlasKlingVideoO1TextToVideo,
    "AtlasCloud Seedance V1 Pro Text-to-Video 1080p": AtlasSeedanceV1ProT2V1080p,
    "AtlasCloud Hailuo 2.3 Pro Text-to-Video": AtlasHailuo23T2VPro,
    "AtlasCloud Seedream V4.5 Text-to-Image": AtlasSeedreamV45TextToImage,
    "AtlasCloud ZImage Turbo Lora Text-to-Image": AtlasZImageTurboLoraTextToImage,
    "AtlasCloud Nano Banana Pro Text-to-Image Ultra": AtlasNanoBananaProTextToImageUltra,
    "AtlasCloud Flux2 Flex Text-to-Image": AtlasFlux2FlexTextToImage,
    "AtlasCloud Image Preview": AtlasImagePreviewURL,
    "AtlasCloud Video Preview": AtlasVideoPreviewer,
}

NODE_DISPLAY_NAME_MAPPINGS: Dict[str, str] = {
    "AtlasCloud Client": "AtlasCloud Client (API Key/Base URL)",
    "AtlasCloud WAN2.5 Text-to-Video": "AtlasCloud WAN2.5 Text-to-Video",
    "AtlasCloud WAN2.6 Text-to-Video": "AtlasCloud WAN2.6 Text-to-Video",
    "AtlasCloud WAN2.2 Text-to-Video 720p": "AtlasCloud WAN2.2 Text-to-Video 720p",
    "AtlasCloud VEO3.1 Text-to-Video": "AtlasCloud VEO3.1 Text-to-Video",
    "AtlasCloud Kling V2.6 Pro Text-to-Video": "AtlasCloud Kling V2.6 Pro Text-to-Video",
    "AtlasCloud Kling Video O1 Text-to-Video": "AtlasCloud Kling Video O1 Text-to-Video",
    "AtlasCloud Seedance V1 Pro Text-to-Video 1080p": "AtlasCloud Seedance V1 Pro Text-to-Video 1080p",
    "AtlasCloud Hailuo 2.3 Pro Text-to-Video": "AtlasCloud Hailuo 2.3 Pro Text-to-Video",
    "AtlasCloud Seedream V4.5 Text-to-Image": "AtlasCloud Seedream V4.5 Text-to-Image",
    "AtlasCloud Image Preview": "AtlasCloud Image Preview",
    "AtlasCloud ZImage Turbo Lora Text-to-Image": "AtlasCloud ZImage Turbo Lora Text-to-Image",
    "AtlasCloud Nano Banana Pro Text-to-Image Ultra": "AtlasCloud Nano Banana Pro Text-to-Image Ultra",
    "AtlasCloud Flux2 Flex Text-to-Image": "AtlasCloud Flux2 Flex Text-to-Image",
    "AtlasCloud Video Preview": "AtlasCloud Video Preview",
}
