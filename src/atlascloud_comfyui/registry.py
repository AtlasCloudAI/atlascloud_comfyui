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
from atlascloud_comfyui.nodes.legacy.nodes import Example as LegacyExample
from atlascloud_comfyui.nodes.auth.atlas_client_node import AtlasClientNode

from atlascloud_comfyui.nodes.video.wan26_t2v import AtlasWAN26TextToVideo
from atlascloud_comfyui.nodes.video.wan25_t2v import AtlasWAN25TextToVideo
from atlascloud_comfyui.nodes.video.wan22_t2v_720p import AtlasWAN22T2V720p
from atlascloud_comfyui.nodes.video.veo31_t2v import AtlasVeo31TextToVideo
from atlascloud_comfyui.nodes.video.kling_v26_pro_t2v import AtlasKlingV26ProTextToVideo
from atlascloud_comfyui.nodes.video.kling_video_o1_t2v import AtlasKlingVideoO1TextToVideo
from atlascloud_comfyui.nodes.video.seedance_v1_pro_t2v_1080p import AtlasSeedanceV1ProT2V1080p
from atlascloud_comfyui.nodes.video.hailuo_23_t2v_pro import AtlasHailuo23T2VPro
from atlascloud_comfyui.nodes.video.sora2_t2v_pro import AtlasSora2TextToVideoPro
from atlascloud_comfyui.nodes.video.seedance_v15_pro_t2v import AtlasSeedanceV15ProTextToVideo
from atlascloud_comfyui.nodes.video.kling_v30_pro_t2v import AtlasKlingV30ProTextToVideo
from atlascloud_comfyui.nodes.video.kling_v30_std_t2v import AtlasKlingV30StdTextToVideo
from atlascloud_comfyui.nodes.video.kling_v30_std_i2v import AtlasKlingV30StdImageToVideo
from atlascloud_comfyui.nodes.video.kling_v30_pro_i2v import AtlasKlingV30ProImageToVideo
from atlascloud_comfyui.nodes.video.veo3_t2v import AtlasVeo3TextToVideo
from atlascloud_comfyui.nodes.video.luma_ray2_t2v import AtlasLumaRay2TextToVideo
from atlascloud_comfyui.nodes.video.luma_ray2_i2v import AtlasLumaRay2ImageToVideo
from atlascloud_comfyui.nodes.video.pika_v22_t2v import AtlasPikaV22TextToVideo
from atlascloud_comfyui.nodes.video.pixverse_v45_t2v import AtlasPixVerseV45TextToVideo
from atlascloud_comfyui.nodes.video.hailuo_02_t2v_pro import AtlasHailuo02T2VPro
from atlascloud_comfyui.nodes.video.sora2_i2v import AtlasSora2ImageToVideo
from atlascloud_comfyui.nodes.video.kling_v25_turbo_pro_t2v import AtlasKlingV25TurboProTextToVideo
from atlascloud_comfyui.nodes.video.hunyuan_t2v import AtlasHunyuanTextToVideo
from atlascloud_comfyui.nodes.video.vidu_q3_i2v import AtlasViduQ3ImageToVideo
from atlascloud_comfyui.nodes.video.veo3_fast_t2v import AtlasVeo3FastTextToVideo
from atlascloud_comfyui.nodes.video.veo31_i2v import AtlasVeo31ImageToVideo
from atlascloud_comfyui.nodes.video.veo3_i2v import AtlasVeo3ImageToVideo
from atlascloud_comfyui.nodes.video.veo2_t2v import AtlasVeo2TextToVideo
from atlascloud_comfyui.nodes.video.veo2_i2v import AtlasVeo2ImageToVideo
from atlascloud_comfyui.nodes.video.luma_ray2_flash_t2v import AtlasLumaRay2FlashTextToVideo
from atlascloud_comfyui.nodes.video.pika_v20_turbo_t2v import AtlasPikaV20TurboTextToVideo
from atlascloud_comfyui.nodes.video.pika_v21_i2v import AtlasPikaV21ImageToVideo
from atlascloud_comfyui.nodes.video.pixverse_v45_i2v import AtlasPixVerseV45ImageToVideo
from atlascloud_comfyui.nodes.video.hailuo_02_i2v_pro import AtlasHailuo02I2VPro
from atlascloud_comfyui.nodes.video.sora2_i2v_pro import AtlasSora2ImageToVideoPro
from atlascloud_comfyui.nodes.video.sora2_t2v import AtlasSora2TextToVideo
from atlascloud_comfyui.nodes.video.kling_v25_turbo_pro_i2v import AtlasKlingV25TurboProImageToVideo
from atlascloud_comfyui.nodes.video.hunyuan_i2v import AtlasHunyuanImageToVideo
from atlascloud_comfyui.nodes.video.wan25_i2v import AtlasWAN25ImageToVideo

from atlascloud_comfyui.nodes.image.seedream_v45_t2i import AtlasSeedreamV45TextToImage
from atlascloud_comfyui.nodes.image.zimage_turbo_lora_t2i import AtlasZImageTurboLoraTextToImage
from atlascloud_comfyui.nodes.image.nano_banana_pro_t2i_ultra import AtlasNanoBananaProTextToImageUltra
from atlascloud_comfyui.nodes.image.flux2_flex_t2i import AtlasFlux2FlexTextToImage
from atlascloud_comfyui.nodes.image.nano_banana2_t2i import AtlasNanoBanana2TextToImage
from atlascloud_comfyui.nodes.image.nano_banana2_t2i_dev import AtlasNanoBanana2TextToImageDev
from atlascloud_comfyui.nodes.image.nano_banana2_edit import AtlasNanoBanana2Edit
from atlascloud_comfyui.nodes.image.nano_banana2_edit_dev import AtlasNanoBanana2EditDev
from atlascloud_comfyui.nodes.image.seedream_v50_lite_t2i import AtlasSeedreamV50LiteTextToImage
from atlascloud_comfyui.nodes.image.seedream_v50_lite_edit import AtlasSeedreamV50LiteEdit
from atlascloud_comfyui.nodes.image.imagen4_t2i import AtlasImagen4TextToImage
from atlascloud_comfyui.nodes.image.imagen4_fast_t2i import AtlasImagen4FastTextToImage
from atlascloud_comfyui.nodes.image.imagen4_ultra_t2i import AtlasImagen4UltraTextToImage
from atlascloud_comfyui.nodes.image.imagen3_t2i import AtlasImagen3TextToImage
from atlascloud_comfyui.nodes.image.ideogram_v3_quality_t2i import AtlasIdeogramV3QualityTextToImage
from atlascloud_comfyui.nodes.image.ideogram_v3_turbo_t2i import AtlasIdeogramV3TurboTextToImage
from atlascloud_comfyui.nodes.image.luma_photon_t2i import AtlasLumaPhotonTextToImage
from atlascloud_comfyui.nodes.image.luma_photon_flash_t2i import AtlasLumaPhotonFlashTextToImage
from atlascloud_comfyui.nodes.image.recraft_v3_t2i import AtlasRecraftV3TextToImage

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
    "AtlasCloud Sora 2 Text-to-Video Pro": AtlasSora2TextToVideoPro,
    "AtlasCloud Seedance V1.5 Pro Text-to-Video": AtlasSeedanceV15ProTextToVideo,
    "AtlasCloud Seedream V4.5 Text-to-Image": AtlasSeedreamV45TextToImage,
    "AtlasCloud ZImage Turbo Lora Text-to-Image": AtlasZImageTurboLoraTextToImage,
    "AtlasCloud Nano Banana Pro Text-to-Image Ultra": AtlasNanoBananaProTextToImageUltra,
    "AtlasCloud Flux2 Flex Text-to-Image": AtlasFlux2FlexTextToImage,
    "AtlasCloud Image Preview": AtlasImagePreviewURL,
    "AtlasCloud Video Preview": AtlasVideoPreviewer,
    "AtlasCloud Kling V3.0 Pro Text-to-Video": AtlasKlingV30ProTextToVideo,
    "AtlasCloud Kling V3.0 Std Text-to-Video": AtlasKlingV30StdTextToVideo,
    "AtlasCloud Kling V3.0 Std Image-to-Video": AtlasKlingV30StdImageToVideo,
    "AtlasCloud Kling V3.0 Pro Image-to-Video": AtlasKlingV30ProImageToVideo,
    "AtlasCloud Nano Banana 2 Text-to-Image": AtlasNanoBanana2TextToImage,
    "AtlasCloud Nano Banana 2 Text-to-Image Developer": AtlasNanoBanana2TextToImageDev,
    "AtlasCloud Nano Banana 2 Edit": AtlasNanoBanana2Edit,
    "AtlasCloud Nano Banana 2 Edit Developer": AtlasNanoBanana2EditDev,
    "AtlasCloud Seedream V5.0 Lite Text-to-Image": AtlasSeedreamV50LiteTextToImage,
    "AtlasCloud Seedream V5.0 Lite Edit": AtlasSeedreamV50LiteEdit,
    "AtlasCloud Vidu Q3 Image-to-Video": AtlasViduQ3ImageToVideo,
    "AtlasCloud VEO3 Text-to-Video": AtlasVeo3TextToVideo,
    "AtlasCloud Imagen4 Text-to-Image": AtlasImagen4TextToImage,
    "AtlasCloud Imagen4 Fast Text-to-Image": AtlasImagen4FastTextToImage,
    "AtlasCloud Luma Ray 2 Text-to-Video": AtlasLumaRay2TextToVideo,
    "AtlasCloud Luma Ray 2 Image-to-Video": AtlasLumaRay2ImageToVideo,
    "AtlasCloud Pika V2.2 Text-to-Video": AtlasPikaV22TextToVideo,
    "AtlasCloud PixVerse V4.5 Text-to-Video": AtlasPixVerseV45TextToVideo,
    "AtlasCloud Hailuo 02 T2V Pro": AtlasHailuo02T2VPro,
    "AtlasCloud Sora 2 Image-to-Video": AtlasSora2ImageToVideo,
    "AtlasCloud Kling V2.5 Turbo Pro Text-to-Video": AtlasKlingV25TurboProTextToVideo,
    "AtlasCloud Hunyuan Text-to-Video": AtlasHunyuanTextToVideo,
    "AtlasCloud VEO3 Fast Text-to-Video": AtlasVeo3FastTextToVideo,
    "AtlasCloud VEO3.1 Image-to-Video": AtlasVeo31ImageToVideo,
    "AtlasCloud VEO3 Image-to-Video": AtlasVeo3ImageToVideo,
    "AtlasCloud VEO2 Text-to-Video": AtlasVeo2TextToVideo,
    "AtlasCloud VEO2 Image-to-Video": AtlasVeo2ImageToVideo,
    "AtlasCloud Luma Ray 2 Flash Text-to-Video": AtlasLumaRay2FlashTextToVideo,
    "AtlasCloud Pika V2.0 Turbo Text-to-Video": AtlasPikaV20TurboTextToVideo,
    "AtlasCloud Pika V2.1 Image-to-Video": AtlasPikaV21ImageToVideo,
    "AtlasCloud PixVerse V4.5 Image-to-Video": AtlasPixVerseV45ImageToVideo,
    "AtlasCloud Hailuo 02 I2V Pro": AtlasHailuo02I2VPro,
    "AtlasCloud Sora 2 Image-to-Video Pro": AtlasSora2ImageToVideoPro,
    "AtlasCloud Sora 2 Text-to-Video": AtlasSora2TextToVideo,
    "AtlasCloud Kling V2.5 Turbo Pro Image-to-Video": AtlasKlingV25TurboProImageToVideo,
    "AtlasCloud Hunyuan Image-to-Video": AtlasHunyuanImageToVideo,
    "AtlasCloud WAN2.5 Image-to-Video": AtlasWAN25ImageToVideo,
    "AtlasCloud Imagen4 Ultra Text-to-Image": AtlasImagen4UltraTextToImage,
    "AtlasCloud Imagen3 Text-to-Image": AtlasImagen3TextToImage,
    "AtlasCloud Ideogram V3 Quality Text-to-Image": AtlasIdeogramV3QualityTextToImage,
    "AtlasCloud Ideogram V3 Turbo Text-to-Image": AtlasIdeogramV3TurboTextToImage,
    "AtlasCloud Luma Photon Text-to-Image": AtlasLumaPhotonTextToImage,
    "AtlasCloud Luma Photon Flash Text-to-Image": AtlasLumaPhotonFlashTextToImage,
    "AtlasCloud Recraft V3 Text-to-Image": AtlasRecraftV3TextToImage,
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
    "AtlasCloud Sora 2 Text-to-Video Pro": "AtlasCloud Sora 2 Text-to-Video Pro",
    "AtlasCloud Seedance V1.5 Pro Text-to-Video": "AtlasCloud Seedance V1.5 Pro Text-to-Video",
    "AtlasCloud Seedream V4.5 Text-to-Image": "AtlasCloud Seedream V4.5 Text-to-Image",
    "AtlasCloud Image Preview": "AtlasCloud Image Preview",
    "AtlasCloud ZImage Turbo Lora Text-to-Image": "AtlasCloud ZImage Turbo Lora Text-to-Image",
    "AtlasCloud Nano Banana Pro Text-to-Image Ultra": "AtlasCloud Nano Banana Pro Text-to-Image Ultra",
    "AtlasCloud Flux2 Flex Text-to-Image": "AtlasCloud Flux2 Flex Text-to-Image",
    "AtlasCloud Video Preview": "AtlasCloud Video Preview",
    "AtlasCloud Kling V3.0 Pro Text-to-Video": "AtlasCloud Kling V3.0 Pro Text-to-Video",
    "AtlasCloud Kling V3.0 Std Text-to-Video": "AtlasCloud Kling V3.0 Std Text-to-Video",
    "AtlasCloud Kling V3.0 Std Image-to-Video": "AtlasCloud Kling V3.0 Std Image-to-Video",
    "AtlasCloud Kling V3.0 Pro Image-to-Video": "AtlasCloud Kling V3.0 Pro Image-to-Video",
    "AtlasCloud Nano Banana 2 Text-to-Image": "AtlasCloud Nano Banana 2 Text-to-Image",
    "AtlasCloud Nano Banana 2 Text-to-Image Developer": "AtlasCloud Nano Banana 2 Text-to-Image Developer",
    "AtlasCloud Nano Banana 2 Edit": "AtlasCloud Nano Banana 2 Edit",
    "AtlasCloud Nano Banana 2 Edit Developer": "AtlasCloud Nano Banana 2 Edit Developer",
    "AtlasCloud Seedream V5.0 Lite Text-to-Image": "AtlasCloud Seedream V5.0 Lite Text-to-Image",
    "AtlasCloud Seedream V5.0 Lite Edit": "AtlasCloud Seedream V5.0 Lite Edit",
    "AtlasCloud Vidu Q3 Image-to-Video": "AtlasCloud Vidu Q3 Image-to-Video",
    "AtlasCloud VEO3 Text-to-Video": "AtlasCloud VEO3 Text-to-Video",
    "AtlasCloud Imagen4 Text-to-Image": "AtlasCloud Imagen4 Text-to-Image",
    "AtlasCloud Imagen4 Fast Text-to-Image": "AtlasCloud Imagen4 Fast Text-to-Image",
    "AtlasCloud Luma Ray 2 Text-to-Video": "AtlasCloud Luma Ray 2 Text-to-Video",
    "AtlasCloud Luma Ray 2 Image-to-Video": "AtlasCloud Luma Ray 2 Image-to-Video",
    "AtlasCloud Pika V2.2 Text-to-Video": "AtlasCloud Pika V2.2 Text-to-Video",
    "AtlasCloud PixVerse V4.5 Text-to-Video": "AtlasCloud PixVerse V4.5 Text-to-Video",
    "AtlasCloud Hailuo 02 T2V Pro": "AtlasCloud Hailuo 02 T2V Pro",
    "AtlasCloud Sora 2 Image-to-Video": "AtlasCloud Sora 2 Image-to-Video",
    "AtlasCloud Kling V2.5 Turbo Pro Text-to-Video": "AtlasCloud Kling V2.5 Turbo Pro Text-to-Video",
    "AtlasCloud Hunyuan Text-to-Video": "AtlasCloud Hunyuan Text-to-Video",
    "AtlasCloud VEO3 Fast Text-to-Video": "AtlasCloud VEO3 Fast Text-to-Video",
    "AtlasCloud VEO3.1 Image-to-Video": "AtlasCloud VEO3.1 Image-to-Video",
    "AtlasCloud VEO3 Image-to-Video": "AtlasCloud VEO3 Image-to-Video",
    "AtlasCloud VEO2 Text-to-Video": "AtlasCloud VEO2 Text-to-Video",
    "AtlasCloud VEO2 Image-to-Video": "AtlasCloud VEO2 Image-to-Video",
    "AtlasCloud Luma Ray 2 Flash Text-to-Video": "AtlasCloud Luma Ray 2 Flash Text-to-Video",
    "AtlasCloud Pika V2.0 Turbo Text-to-Video": "AtlasCloud Pika V2.0 Turbo Text-to-Video",
    "AtlasCloud Pika V2.1 Image-to-Video": "AtlasCloud Pika V2.1 Image-to-Video",
    "AtlasCloud PixVerse V4.5 Image-to-Video": "AtlasCloud PixVerse V4.5 Image-to-Video",
    "AtlasCloud Hailuo 02 I2V Pro": "AtlasCloud Hailuo 02 I2V Pro",
    "AtlasCloud Sora 2 Image-to-Video Pro": "AtlasCloud Sora 2 Image-to-Video Pro",
    "AtlasCloud Sora 2 Text-to-Video": "AtlasCloud Sora 2 Text-to-Video",
    "AtlasCloud Kling V2.5 Turbo Pro Image-to-Video": "AtlasCloud Kling V2.5 Turbo Pro Image-to-Video",
    "AtlasCloud Hunyuan Image-to-Video": "AtlasCloud Hunyuan Image-to-Video",
    "AtlasCloud WAN2.5 Image-to-Video": "AtlasCloud WAN2.5 Image-to-Video",
    "AtlasCloud Imagen4 Ultra Text-to-Image": "AtlasCloud Imagen4 Ultra Text-to-Image",
    "AtlasCloud Imagen3 Text-to-Image": "AtlasCloud Imagen3 Text-to-Image",
    "AtlasCloud Ideogram V3 Quality Text-to-Image": "AtlasCloud Ideogram V3 Quality Text-to-Image",
    "AtlasCloud Ideogram V3 Turbo Text-to-Image": "AtlasCloud Ideogram V3 Turbo Text-to-Image",
    "AtlasCloud Luma Photon Text-to-Image": "AtlasCloud Luma Photon Text-to-Image",
    "AtlasCloud Luma Photon Flash Text-to-Image": "AtlasCloud Luma Photon Flash Text-to-Image",
    "AtlasCloud Recraft V3 Text-to-Image": "AtlasCloud Recraft V3 Text-to-Image",
}

NODE_CLASS_MAPPINGS["Example"] = LegacyExample
NODE_DISPLAY_NAME_MAPPINGS["Example"] = "Example (Deprecated)"
