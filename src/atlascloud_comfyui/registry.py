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
from atlascloud_comfyui.nodes.video.wan26_i2v_flash import AtlasWAN26ImageToVideoFlash
from atlascloud_comfyui.nodes.video.wan26_i2v import AtlasWAN26ImageToVideo
from atlascloud_comfyui.nodes.video.wan26_v2v import AtlasWAN26VideoToVideo
from atlascloud_comfyui.nodes.image.wan26_t2i import AtlasWAN26TextToImage
from atlascloud_comfyui.nodes.image.wan26_image_edit import AtlasWAN26ImageEdit

from atlascloud_comfyui.nodes.video.kling_video_o3_pro_t2v import AtlasKlingVideoO3ProTextToVideo
from atlascloud_comfyui.nodes.video.kling_video_o3_pro_i2v import AtlasKlingVideoO3ProImageToVideo
from atlascloud_comfyui.nodes.video.kling_video_o3_pro_r2v import AtlasKlingVideoO3ProReferenceToVideo
from atlascloud_comfyui.nodes.video.kling_video_o3_pro_video_edit import AtlasKlingVideoO3ProVideoEdit

from atlascloud_comfyui.nodes.video.kling_video_o3_std_t2v import AtlasKlingVideoO3StdTextToVideo
from atlascloud_comfyui.nodes.video.kling_video_o3_std_i2v import AtlasKlingVideoO3StdImageToVideo
from atlascloud_comfyui.nodes.video.kling_video_o3_std_r2v import AtlasKlingVideoO3StdReferenceToVideo
from atlascloud_comfyui.nodes.video.kling_video_o3_std_video_edit import AtlasKlingVideoO3StdVideoEdit
from atlascloud_comfyui.nodes.video.wan25_t2v import AtlasWAN25TextToVideo
from atlascloud_comfyui.nodes.video.wan22_t2v_720p import AtlasWAN22T2V720p
from atlascloud_comfyui.nodes.video.alibaba_wan_2_2_t2v_480p import AtlasAlibabaWan22T2V480p
from atlascloud_comfyui.nodes.video.alibaba_wan_2_2_i2v_720p import AtlasAlibabaWan22I2V720p
from atlascloud_comfyui.nodes.video.alibaba_wan_2_2_i2v_480p import AtlasAlibabaWan22I2V480p
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
from atlascloud_comfyui.nodes.video.vidu_q3_i2v_v2 import AtlasViduQ3ImageToVideoV2
from atlascloud_comfyui.nodes.video.vidu_q3_t2v import AtlasViduQ3TextToVideo
from atlascloud_comfyui.nodes.video.vidu_q3_pro_t2v import AtlasViduQ3ProTextToVideo
from atlascloud_comfyui.nodes.video.vidu_q3_pro_i2v import AtlasViduQ3ProImageToVideo
from atlascloud_comfyui.nodes.video.wan22_spicy_i2v import AtlasWan22SpicyImageToVideo
from atlascloud_comfyui.nodes.video.wan22_spicy_i2v_lora import AtlasWan22SpicyImageToVideoLora
from atlascloud_comfyui.nodes.video.veo3_fast_t2v import AtlasVeo3FastTextToVideo
from atlascloud_comfyui.nodes.video.veo31_i2v import AtlasVeo31ImageToVideo
from atlascloud_comfyui.nodes.video.google_veo31_fast_t2v import AtlasVeo31FastTextToVideo
from atlascloud_comfyui.nodes.video.google_veo31_fast_i2v import AtlasVeo31FastImageToVideo
from atlascloud_comfyui.nodes.video.google_veo31_r2v import AtlasVeo31ReferenceToVideo
from atlascloud_comfyui.nodes.video.veo3_i2v import AtlasVeo3ImageToVideo
from atlascloud_comfyui.nodes.video.veo2_t2v import AtlasVeo2TextToVideo
from atlascloud_comfyui.nodes.video.veo2_i2v import AtlasVeo2ImageToVideo
from atlascloud_comfyui.nodes.video.luma_ray2_flash_t2v import AtlasLumaRay2FlashTextToVideo
from atlascloud_comfyui.nodes.video.pika_v20_turbo_t2v import AtlasPikaV20TurboTextToVideo
from atlascloud_comfyui.nodes.video.pika_v21_i2v import AtlasPikaV21ImageToVideo
from atlascloud_comfyui.nodes.video.pixverse_v45_i2v import AtlasPixVerseV45ImageToVideo
from atlascloud_comfyui.nodes.video.hailuo_02_i2v_pro import AtlasHailuo02I2VPro
from atlascloud_comfyui.nodes.video.minimax_hailuo_02_i2v_standard import AtlasMinimaxHailuo02I2VStandard
from atlascloud_comfyui.nodes.video.hailuo_02_i2v_standard import AtlasHailuo02I2VStandard
from atlascloud_comfyui.nodes.video.sora2_i2v_pro import AtlasSora2ImageToVideoPro
from atlascloud_comfyui.nodes.video.sora2_t2v import AtlasSora2TextToVideo
from atlascloud_comfyui.nodes.video.kling_v25_turbo_pro_i2v import AtlasKlingV25TurboProImageToVideo
from atlascloud_comfyui.nodes.video.hunyuan_i2v import AtlasHunyuanImageToVideo
from atlascloud_comfyui.nodes.video.wan25_i2v import AtlasWAN25ImageToVideo

from atlascloud_comfyui.nodes.video.kling_v26_pro_avatar import AtlasKlingV26ProAvatar
from atlascloud_comfyui.nodes.video.kling_v26_std_avatar import AtlasKlingV26StdAvatar
from atlascloud_comfyui.nodes.video.kling_v26_pro_motion_control import AtlasKlingV26ProMotionControl
from atlascloud_comfyui.nodes.video.kling_v26_std_motion_control import AtlasKlingV26StdMotionControl
from atlascloud_comfyui.nodes.video.seedance_v15_pro_i2v import AtlasSeedanceV15ProImageToVideo
from atlascloud_comfyui.nodes.video.seedance_v15_pro_i2v_fast import AtlasSeedanceV15ProImageToVideoFast
from atlascloud_comfyui.nodes.video.seedance_v15_pro_t2v_fast import AtlasSeedanceV15ProTextToVideoFast
from atlascloud_comfyui.nodes.video.kling_video_o1_i2v import AtlasKlingVideoO1ImageToVideo
from atlascloud_comfyui.nodes.video.kling_v26_pro_i2v import AtlasKlingV26ProImageToVideo

from atlascloud_comfyui.nodes.image.seedream_v45_t2i import AtlasSeedreamV45TextToImage
from atlascloud_comfyui.nodes.image.seedream_v45_edit import AtlasSeedreamV45Edit
from atlascloud_comfyui.nodes.image.seedream_v45_sequential_t2i import AtlasSeedreamV45SequentialTextToImage
from atlascloud_comfyui.nodes.image.seedream_v45_edit_sequential import AtlasSeedreamV45EditSequential
from atlascloud_comfyui.nodes.image.seedream_v4_t2i import AtlasSeedreamV4TextToImage
from atlascloud_comfyui.nodes.image.seedream_v4_sequential_t2i import AtlasSeedreamV4SequentialTextToImage
from atlascloud_comfyui.nodes.image.seedream_v4_edit import AtlasSeedreamV4Edit
from atlascloud_comfyui.nodes.image.seedream_v4_edit_sequential import AtlasSeedreamV4EditSequential
from atlascloud_comfyui.nodes.image.zimage_turbo_lora_t2i import AtlasZImageTurboLoraTextToImage
from atlascloud_comfyui.nodes.image.zimage_turbo_t2i import AtlasZImageTurboTextToImage
from atlascloud_comfyui.nodes.image.qwen_image_edit import AtlasQwenImageEdit
from atlascloud_comfyui.nodes.image.qwen_image_edit_alibaba import AtlasAlibabaQwenImageEdit
from atlascloud_comfyui.nodes.image.qwen_image_edit_plus_alibaba import AtlasAlibabaQwenImageEditPlus
from atlascloud_comfyui.nodes.image.qwen_image_t2i_atlascloud import AtlasAtlascloudQwenImageTextToImage
from atlascloud_comfyui.nodes.image.nano_banana_pro_t2i_ultra import AtlasNanoBananaProTextToImageUltra
from atlascloud_comfyui.nodes.image.nano_banana_pro_t2i import AtlasNanoBananaProTextToImage
from atlascloud_comfyui.nodes.image.nano_banana_pro_edit import AtlasNanoBananaProEdit
from atlascloud_comfyui.nodes.image.flux2_flex_t2i import AtlasFlux2FlexTextToImage
from atlascloud_comfyui.nodes.image.flux_dev_t2i import AtlasFluxDevTextToImage
from atlascloud_comfyui.nodes.image.flux_dev_lora_t2i import AtlasFluxDevLoraTextToImage
from atlascloud_comfyui.nodes.image.nano_banana2_t2i import AtlasNanoBanana2TextToImage
from atlascloud_comfyui.nodes.image.nano_banana2_t2i_dev import AtlasNanoBanana2TextToImageDev
from atlascloud_comfyui.nodes.image.nano_banana2_edit import AtlasNanoBanana2Edit
from atlascloud_comfyui.nodes.image.nano_banana2_edit_dev import AtlasNanoBanana2EditDev
from atlascloud_comfyui.nodes.image.seedream_v50_lite_t2i import AtlasSeedreamV50LiteTextToImage
from atlascloud_comfyui.nodes.image.seedream_v50_lite_edit import AtlasSeedreamV50LiteEdit
from atlascloud_comfyui.nodes.image.seedream_v50_lite_sequential_t2i import AtlasSeedreamV50LiteSequentialTextToImage
from atlascloud_comfyui.nodes.image.seedream_v50_lite_edit_sequential import AtlasSeedreamV50LiteEditSequential
from atlascloud_comfyui.nodes.image.imagen4_t2i import AtlasImagen4TextToImage
from atlascloud_comfyui.nodes.image.imagen4_fast_t2i import AtlasImagen4FastTextToImage
from atlascloud_comfyui.nodes.image.imagen4_ultra_t2i import AtlasImagen4UltraTextToImage
from atlascloud_comfyui.nodes.image.imagen3_t2i import AtlasImagen3TextToImage
from atlascloud_comfyui.nodes.image.imagen3_fast_t2i import AtlasImagen3FastTextToImage
from atlascloud_comfyui.nodes.image.wan25_t2i import AtlasWan25TextToImage
from atlascloud_comfyui.nodes.image.wan25_image_edit import AtlasWan25ImageEdit
from atlascloud_comfyui.nodes.image.nano_banana_t2i import AtlasNanoBananaTextToImage
from atlascloud_comfyui.nodes.image.nano_banana_t2i_dev import AtlasNanoBananaTextToImageDeveloper
from atlascloud_comfyui.nodes.image.nano_banana_edit import AtlasNanoBananaEdit
from atlascloud_comfyui.nodes.image.nano_banana_edit_dev import AtlasNanoBananaEditDeveloper
from atlascloud_comfyui.nodes.image.nano_banana_pro_t2i_dev import AtlasNanoBananaProTextToImageDeveloper
from atlascloud_comfyui.nodes.image.nano_banana_pro_edit_dev import AtlasNanoBananaProEditDeveloper
from atlascloud_comfyui.nodes.image.flux_kontext_dev_edit import AtlasFluxKontextDevEdit
from atlascloud_comfyui.nodes.image.flux_kontext_dev_lora_edit import AtlasFluxKontextDevLoraEdit
from atlascloud_comfyui.nodes.image.flux_schnell_t2i import AtlasFluxSchnellTextToImage
from atlascloud_comfyui.nodes.image.ideogram_v3_quality_t2i import AtlasIdeogramV3QualityTextToImage
from atlascloud_comfyui.nodes.image.ideogram_v3_turbo_t2i import AtlasIdeogramV3TurboTextToImage
from atlascloud_comfyui.nodes.image.luma_photon_t2i import AtlasLumaPhotonTextToImage
from atlascloud_comfyui.nodes.image.luma_photon_flash_t2i import AtlasLumaPhotonFlashTextToImage
from atlascloud_comfyui.nodes.image.recraft_v3_t2i import AtlasRecraftV3TextToImage
from atlascloud_comfyui.nodes.image.qwen_image_edit_plus_20251215 import AtlasQwenImageEditPlus20251215
from atlascloud_comfyui.nodes.image.qwen_image_t2i_plus import AtlasQwenImageTextToImagePlus
from atlascloud_comfyui.nodes.image.qwen_image_t2i_max import AtlasQwenImageTextToImageMax

from atlascloud_comfyui.nodes.video.seedance_v1_pro_fast_t2v import AtlasSeedanceV1ProFastTextToVideo
from atlascloud_comfyui.nodes.video.seedance_v1_pro_fast_i2v import AtlasSeedanceV1ProFastImageToVideo
from atlascloud_comfyui.nodes.video.wan25_fast_t2v import AtlasWAN25TextToVideoFast
from atlascloud_comfyui.nodes.video.wan25_fast_i2v import AtlasWAN25ImageToVideoFast
from atlascloud_comfyui.nodes.video.wan22_animate_mix import AtlasWan22AnimateMix
from atlascloud_comfyui.nodes.video.wan22_animate_move import AtlasWan22AnimateMove
from atlascloud_comfyui.nodes.video.van25_t2v import AtlasAtlascloudVan25TextToVideo
from atlascloud_comfyui.nodes.video.van25_i2v import AtlasAtlascloudVan25ImageToVideo
from atlascloud_comfyui.nodes.video.van26_t2v import AtlasVan26TextToVideo
from atlascloud_comfyui.nodes.video.van26_i2v import AtlasVan26ImageToVideo
from atlascloud_comfyui.nodes.video.vidu_reference_to_video_q1 import AtlasViduReferenceToVideoQ1
from atlascloud_comfyui.nodes.video.vidu_reference_to_video_v2 import AtlasViduReferenceToVideoV2
from atlascloud_comfyui.nodes.video.vidu_start_end_to_video_v2 import AtlasViduStartEndToVideoV2
from atlascloud_comfyui.nodes.video.kling_v20_i2v_master import AtlasKlingV20I2VMaster
from atlascloud_comfyui.nodes.video.veo3_fast_i2v import AtlasVeo3FastImageToVideo
from atlascloud_comfyui.nodes.video.kling_v21_t2v_master import AtlasKlingV21T2VMaster
from atlascloud_comfyui.nodes.video.kling_v21_i2v_master import AtlasKlingV21I2VMaster
from atlascloud_comfyui.nodes.video.kling_v21_i2v_pro_start_end_frame import AtlasKlingV21I2VProStartEndFrame
from atlascloud_comfyui.nodes.video.kwaivgi_kling_v2_1_i2v_pro import AtlasKwaivgiKlingV21I2VPro
from atlascloud_comfyui.nodes.video.kwaivgi_kling_v2_1_i2v_standard import AtlasKwaivgiKlingV21I2VStandard
from atlascloud_comfyui.nodes.video.kling_v16_multi_i2v_pro import AtlasKlingV16MultiI2VPro
from atlascloud_comfyui.nodes.video.kling_v16_multi_i2v_standard import AtlasKlingV16MultiI2VStandard
from atlascloud_comfyui.nodes.video.kling_v16_i2v_standard import AtlasKlingV16I2VStandard
from atlascloud_comfyui.nodes.video.kling_effects import AtlasKlingEffects
from atlascloud_comfyui.nodes.video.kwaivgi_kling_v1_6_t2v_standard import AtlasKwaivgiKlingV16T2VStandard
from atlascloud_comfyui.nodes.video.kwaivgi_kling_v1_6_i2v_pro import AtlasKwaivgiKlingV16I2VPro

from atlascloud_comfyui.nodes.video.hailuo_23_t2v_standard import AtlasHailuo23T2VStandard
from atlascloud_comfyui.nodes.video.hailuo_23_i2v_standard import AtlasHailuo23I2VStandard
from atlascloud_comfyui.nodes.video.hailuo_23_i2v_pro import AtlasHailuo23I2VPro
from atlascloud_comfyui.nodes.video.hailuo_23_fast import AtlasHailuo23Fast
from atlascloud_comfyui.nodes.video.hailuo_02_fast import AtlasHailuo02Fast
from atlascloud_comfyui.nodes.video.hailuo_02_pro import AtlasHailuo02Pro
from atlascloud_comfyui.nodes.video.hailuo_02_t2v_standard import AtlasHailuo02T2VStandard

from atlascloud_comfyui.nodes.video.seedance_v1_lite_t2v_1080p import AtlasSeedanceV1LiteT2V1080p
from atlascloud_comfyui.nodes.video.seedance_v1_lite_t2v_720p import AtlasSeedanceV1LiteT2V720p
from atlascloud_comfyui.nodes.video.seedance_v1_lite_i2v_1080p import AtlasSeedanceV1LiteI2V1080p
from atlascloud_comfyui.nodes.video.bytedance_seedance_v1_lite_t2v_480p import AtlasBytedanceSeedanceV1LiteT2V480p
from atlascloud_comfyui.nodes.video.bytedance_seedance_v1_lite_i2v_720p import AtlasBytedanceSeedanceV1LiteI2V720p
from atlascloud_comfyui.nodes.video.bytedance_seedance_v1_lite_i2v_480p import AtlasBytedanceSeedanceV1LiteI2V480p
from atlascloud_comfyui.nodes.video.bytedance_seedance_v1_pro_t2v_720p import AtlasBytedanceSeedanceV1ProT2V720p
from atlascloud_comfyui.nodes.video.bytedance_seedance_v1_pro_t2v_480p import AtlasBytedanceSeedanceV1ProT2V480p
from atlascloud_comfyui.nodes.video.bytedance_seedance_v1_pro_i2v_1080p import AtlasBytedanceSeedanceV1ProI2V1080p
from atlascloud_comfyui.nodes.video.bytedance_seedance_v1_pro_i2v_720p import AtlasBytedanceSeedanceV1ProI2V720p
from atlascloud_comfyui.nodes.video.bytedance_seedance_v1_pro_i2v_480p import AtlasBytedanceSeedanceV1ProI2V480p

from atlascloud_comfyui.nodes.video.kling_v20_t2v_master import AtlasKlingV20T2VMaster

from atlascloud_comfyui.nodes.utils.image_preview import AtlasImagePreviewURL
from atlascloud_comfyui.nodes.utils.video_previewer import AtlasVideoPreviewer


NODE_CLASS_MAPPINGS: Dict[str, Type[Any]] = {
    "AtlasCloud Client": AtlasClientNode,
    "AtlasCloud WAN2.5 Text-to-Video": AtlasWAN25TextToVideo,
    "AtlasCloud WAN2.6 Text-to-Video": AtlasWAN26TextToVideo,
    "AtlasCloud WAN2.6 Text-to-Image": AtlasWAN26TextToImage,
    "AtlasCloud WAN2.5 Text-to-Image": AtlasWan25TextToImage,
    "AtlasCloud WAN2.5 Image-Edit": AtlasWan25ImageEdit,
    "AtlasCloud WAN2.6 Image-Edit": AtlasWAN26ImageEdit,
    "AtlasCloud WAN2.6 Image-to-Video": AtlasWAN26ImageToVideo,
    "AtlasCloud WAN2.6 Image-to-Video Flash": AtlasWAN26ImageToVideoFlash,
    "AtlasCloud WAN2.6 Video-to-Video": AtlasWAN26VideoToVideo,

    "AtlasCloud Kling Video O3 Pro Text-to-Video": AtlasKlingVideoO3ProTextToVideo,
    "AtlasCloud Kling Video O3 Pro Image-to-Video": AtlasKlingVideoO3ProImageToVideo,
    "AtlasCloud Kling Video O3 Pro Reference-to-Video": AtlasKlingVideoO3ProReferenceToVideo,
    "AtlasCloud Kling Video O3 Pro Video-Edit": AtlasKlingVideoO3ProVideoEdit,

    "AtlasCloud Kling Video O3 Std Text-to-Video": AtlasKlingVideoO3StdTextToVideo,
    "AtlasCloud Kling Video O3 Std Image-to-Video": AtlasKlingVideoO3StdImageToVideo,
    "AtlasCloud Kling Video O3 Std Reference-to-Video": AtlasKlingVideoO3StdReferenceToVideo,
    "AtlasCloud Kling Video O3 Std Video-Edit": AtlasKlingVideoO3StdVideoEdit,
    "AtlasCloud WAN2.2 Text-to-Video 720p": AtlasWAN22T2V720p,
    "AtlasCloud WAN2.2 Text-to-Video 480p": AtlasAlibabaWan22T2V480p,
    "AtlasCloud VEO3.1 Text-to-Video": AtlasVeo31TextToVideo,
    "AtlasCloud Kling V2.6 Pro Text-to-Video": AtlasKlingV26ProTextToVideo,
    "AtlasCloud Kling V2.6 Pro Avatar": AtlasKlingV26ProAvatar,
    "AtlasCloud Kling V2.6 Std Avatar": AtlasKlingV26StdAvatar,
    "AtlasCloud Kling V2.6 Pro Motion-Control": AtlasKlingV26ProMotionControl,
    "AtlasCloud Kling V2.6 Std Motion-Control": AtlasKlingV26StdMotionControl,
    "AtlasCloud Kling V2.6 Pro Image-to-Video": AtlasKlingV26ProImageToVideo,
    "AtlasCloud Kling Video O1 Text-to-Video": AtlasKlingVideoO1TextToVideo,
    "AtlasCloud Kling Video O1 Image-to-Video": AtlasKlingVideoO1ImageToVideo,
    "AtlasCloud Seedance V1 Pro Text-to-Video 1080p": AtlasSeedanceV1ProT2V1080p,
    "AtlasCloud Seedance V1 Pro Text-to-Video 720p": AtlasBytedanceSeedanceV1ProT2V720p,
    "AtlasCloud Seedance V1 Pro Text-to-Video 480p": AtlasBytedanceSeedanceV1ProT2V480p,
    "AtlasCloud Seedance V1 Lite Text-to-Video 480p": AtlasBytedanceSeedanceV1LiteT2V480p,
    "AtlasCloud Hailuo 2.3 Pro Text-to-Video": AtlasHailuo23T2VPro,
    "AtlasCloud Sora 2 Text-to-Video Pro": AtlasSora2TextToVideoPro,
    "AtlasCloud Seedance V1.5 Pro Text-to-Video": AtlasSeedanceV15ProTextToVideo,
    "AtlasCloud Seedance V1.5 Pro Text-to-Video Fast": AtlasSeedanceV15ProTextToVideoFast,
    "AtlasCloud Seedance V1.5 Pro Image-to-Video": AtlasSeedanceV15ProImageToVideo,
    "AtlasCloud Seedance V1.5 Pro Image-to-Video Fast": AtlasSeedanceV15ProImageToVideoFast,
    "AtlasCloud Seedream V4 Text-to-Image": AtlasSeedreamV4TextToImage,
    "AtlasCloud Seedream V4 Sequential Text-to-Image": AtlasSeedreamV4SequentialTextToImage,
    "AtlasCloud Seedream V4 Edit": AtlasSeedreamV4Edit,
    "AtlasCloud Seedream V4 Edit Sequential": AtlasSeedreamV4EditSequential,
    "AtlasCloud Seedream V4.5 Text-to-Image": AtlasSeedreamV45TextToImage,
    "AtlasCloud Seedream V4.5 Edit": AtlasSeedreamV45Edit,
    "AtlasCloud Seedream V4.5 Sequential Text-to-Image": AtlasSeedreamV45SequentialTextToImage,
    "AtlasCloud Seedream V4.5 Edit Sequential": AtlasSeedreamV45EditSequential,
    "AtlasCloud ZImage Turbo Lora Text-to-Image": AtlasZImageTurboLoraTextToImage,
    "AtlasCloud ZImage Turbo Text-to-Image": AtlasZImageTurboTextToImage,
    "AtlasCloud Nano Banana Pro Text-to-Image Ultra": AtlasNanoBananaProTextToImageUltra,
    "AtlasCloud Flux2 Flex Text-to-Image": AtlasFlux2FlexTextToImage,
    "AtlasCloud Flux Dev Text-to-Image": AtlasFluxDevTextToImage,
    "AtlasCloud Flux Dev LoRA Text-to-Image": AtlasFluxDevLoraTextToImage,
    "AtlasCloud Flux Schnell Text-to-Image": AtlasFluxSchnellTextToImage,
    "AtlasCloud Flux Kontext Dev Edit": AtlasFluxKontextDevEdit,
    "AtlasCloud Flux Kontext Dev LoRA Edit": AtlasFluxKontextDevLoraEdit,
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
    "AtlasCloud Seedream V5.0 Lite Sequential Text-to-Image": AtlasSeedreamV50LiteSequentialTextToImage,
    "AtlasCloud Seedream V5.0 Lite Edit": AtlasSeedreamV50LiteEdit,
    "AtlasCloud Seedream V5.0 Lite Edit Sequential": AtlasSeedreamV50LiteEditSequential,
    "AtlasCloud Vidu Q3 Text-to-Video": AtlasViduQ3TextToVideo,
    "AtlasCloud Vidu Q3 Image-to-Video": AtlasViduQ3ImageToVideo,
    "AtlasCloud Vidu Q3 Image-to-Video (Q3 API)": AtlasViduQ3ImageToVideoV2,
    "AtlasCloud Vidu Q3-Pro Text-to-Video": AtlasViduQ3ProTextToVideo,
    "AtlasCloud Vidu Q3-Pro Image-to-Video": AtlasViduQ3ProImageToVideo,
    "AtlasCloud WAN2.2 Spicy Image-to-Video": AtlasWan22SpicyImageToVideo,
    "AtlasCloud WAN2.2 Spicy Image-to-Video LoRA": AtlasWan22SpicyImageToVideoLora,
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
    "AtlasCloud VEO3.1 Fast Text-to-Video": AtlasVeo31FastTextToVideo,
    "AtlasCloud VEO3.1 Fast Image-to-Video": AtlasVeo31FastImageToVideo,
    "AtlasCloud VEO3.1 Reference-to-Video": AtlasVeo31ReferenceToVideo,
    "AtlasCloud VEO3.1 Image-to-Video": AtlasVeo31ImageToVideo,
    "AtlasCloud VEO3 Image-to-Video": AtlasVeo3ImageToVideo,
    "AtlasCloud VEO2 Text-to-Video": AtlasVeo2TextToVideo,
    "AtlasCloud VEO2 Image-to-Video": AtlasVeo2ImageToVideo,
    "AtlasCloud Luma Ray 2 Flash Text-to-Video": AtlasLumaRay2FlashTextToVideo,
    "AtlasCloud Pika V2.0 Turbo Text-to-Video": AtlasPikaV20TurboTextToVideo,
    "AtlasCloud Pika V2.1 Image-to-Video": AtlasPikaV21ImageToVideo,
    "AtlasCloud PixVerse V4.5 Image-to-Video": AtlasPixVerseV45ImageToVideo,
    "AtlasCloud Hailuo 02 I2V Pro": AtlasHailuo02I2VPro,
    "AtlasCloud Hailuo 02 I2V Standard": AtlasMinimaxHailuo02I2VStandard,
    "AtlasCloud Hailuo 02 Standard": AtlasHailuo02I2VStandard,
    "AtlasCloud Sora 2 Image-to-Video Pro": AtlasSora2ImageToVideoPro,
    "AtlasCloud Sora 2 Text-to-Video": AtlasSora2TextToVideo,
    "AtlasCloud Kling V2.5 Turbo Pro Image-to-Video": AtlasKlingV25TurboProImageToVideo,
    "AtlasCloud Hunyuan Image-to-Video": AtlasHunyuanImageToVideo,
    "AtlasCloud WAN2.5 Image-to-Video": AtlasWAN25ImageToVideo,
    "AtlasCloud WAN2.2 Image-to-Video 720p": AtlasAlibabaWan22I2V720p,
    "AtlasCloud WAN2.2 Image-to-Video 480p": AtlasAlibabaWan22I2V480p,
    "AtlasCloud WAN2.2 Animate Mix": AtlasWan22AnimateMix,
    "AtlasCloud WAN2.2 Animate Move": AtlasWan22AnimateMove,
    "AtlasCloud Imagen4 Ultra Text-to-Image": AtlasImagen4UltraTextToImage,
    "AtlasCloud Imagen3 Text-to-Image": AtlasImagen3TextToImage,
    "AtlasCloud Imagen3 Fast Text-to-Image": AtlasImagen3FastTextToImage,
    "AtlasCloud Ideogram V3 Quality Text-to-Image": AtlasIdeogramV3QualityTextToImage,
    "AtlasCloud Ideogram V3 Turbo Text-to-Image": AtlasIdeogramV3TurboTextToImage,
    "AtlasCloud Luma Photon Text-to-Image": AtlasLumaPhotonTextToImage,
    "AtlasCloud Luma Photon Flash Text-to-Image": AtlasLumaPhotonFlashTextToImage,
    "AtlasCloud Recraft V3 Text-to-Image": AtlasRecraftV3TextToImage,
    "AtlasCloud Qwen Image Edit": AtlasQwenImageEdit,
    "AtlasCloud Qwen Image Text-to-Image (AtlasCloud)": AtlasAtlascloudQwenImageTextToImage,
    "AtlasCloud Qwen Image Edit (Alibaba)": AtlasAlibabaQwenImageEdit,
    "AtlasCloud Qwen Image Edit Plus (Alibaba)": AtlasAlibabaQwenImageEditPlus,
    "AtlasCloud Nano Banana Pro Text-to-Image": AtlasNanoBananaProTextToImage,
    "AtlasCloud Nano Banana Pro Text-to-Image Developer": AtlasNanoBananaProTextToImageDeveloper,
    "AtlasCloud Nano Banana Pro Edit": AtlasNanoBananaProEdit,
    "AtlasCloud Nano Banana Pro Edit Developer": AtlasNanoBananaProEditDeveloper,
    "AtlasCloud Nano Banana Text-to-Image": AtlasNanoBananaTextToImage,
    "AtlasCloud Nano Banana Text-to-Image Developer": AtlasNanoBananaTextToImageDeveloper,
    "AtlasCloud Nano Banana Edit": AtlasNanoBananaEdit,
    "AtlasCloud Nano Banana Edit Developer": AtlasNanoBananaEditDeveloper,
    "AtlasCloud Qwen Image Edit Plus 20251215": AtlasQwenImageEditPlus20251215,
    "AtlasCloud Qwen Image Text-to-Image Plus": AtlasQwenImageTextToImagePlus,
    "AtlasCloud Qwen Image Text-to-Image Max": AtlasQwenImageTextToImageMax,

    "AtlasCloud Seedance V1 Pro Fast Text-to-Video": AtlasSeedanceV1ProFastTextToVideo,
    "AtlasCloud Seedance V1 Pro Fast Image-to-Video": AtlasSeedanceV1ProFastImageToVideo,
    "AtlasCloud Seedance V1 Pro Image-to-Video 1080p": AtlasBytedanceSeedanceV1ProI2V1080p,
    "AtlasCloud Seedance V1 Pro Image-to-Video 720p": AtlasBytedanceSeedanceV1ProI2V720p,
    "AtlasCloud Seedance V1 Pro Image-to-Video 480p": AtlasBytedanceSeedanceV1ProI2V480p,
    "AtlasCloud Seedance V1 Lite Image-to-Video 720p": AtlasBytedanceSeedanceV1LiteI2V720p,
    "AtlasCloud Seedance V1 Lite Image-to-Video 480p": AtlasBytedanceSeedanceV1LiteI2V480p,
    "AtlasCloud WAN2.5 Text-to-Video Fast": AtlasWAN25TextToVideoFast,
    "AtlasCloud WAN2.5 Image-to-Video Fast": AtlasWAN25ImageToVideoFast,
    "AtlasCloud Van-2.5 Text-to-Video": AtlasAtlascloudVan25TextToVideo,
    "AtlasCloud Van-2.5 Image-to-Video": AtlasAtlascloudVan25ImageToVideo,
    "AtlasCloud Van-2.6 Text-to-Video": AtlasVan26TextToVideo,
    "AtlasCloud Van-2.6 Image-to-Video": AtlasVan26ImageToVideo,
    "AtlasCloud Vidu Reference-to-Video Q1": AtlasViduReferenceToVideoQ1,
    "AtlasCloud Vidu Reference-to-Video 2.0": AtlasViduReferenceToVideoV2,
    "AtlasCloud Vidu Start-End-to-Video 2.0": AtlasViduStartEndToVideoV2,
    "AtlasCloud Kling V2.0 I2V Master": AtlasKlingV20I2VMaster,
    "AtlasCloud VEO3 Fast Image-to-Video": AtlasVeo3FastImageToVideo,
    "AtlasCloud Kling V2.1 T2V Master": AtlasKlingV21T2VMaster,
    "AtlasCloud Kling V2.1 I2V Master": AtlasKlingV21I2VMaster,
    "AtlasCloud Kling V2.1 I2V Pro (Start/End Frame)": AtlasKlingV21I2VProStartEndFrame,
    "AtlasCloud Kling V2.1 I2V Pro": AtlasKwaivgiKlingV21I2VPro,
    "AtlasCloud Kling V2.1 I2V Standard": AtlasKwaivgiKlingV21I2VStandard,
    "AtlasCloud Kling V1.6 Multi I2V Pro": AtlasKlingV16MultiI2VPro,
    "AtlasCloud Kling V1.6 Multi I2V Standard": AtlasKlingV16MultiI2VStandard,
    "AtlasCloud Kling V1.6 I2V Standard": AtlasKlingV16I2VStandard,
    "AtlasCloud Kling V1.6 T2V Standard": AtlasKwaivgiKlingV16T2VStandard,
    "AtlasCloud Kling V1.6 I2V Pro": AtlasKwaivgiKlingV16I2VPro,
    "AtlasCloud Kling Effects": AtlasKlingEffects,

    "AtlasCloud Hailuo 2.3 T2V Standard": AtlasHailuo23T2VStandard,
    "AtlasCloud Hailuo 2.3 I2V Standard": AtlasHailuo23I2VStandard,
    "AtlasCloud Hailuo 2.3 I2V Pro": AtlasHailuo23I2VPro,
    "AtlasCloud Hailuo 2.3 Fast": AtlasHailuo23Fast,

    "AtlasCloud Hailuo 02 Fast": AtlasHailuo02Fast,
    "AtlasCloud Hailuo 02 Pro": AtlasHailuo02Pro,
    "AtlasCloud Hailuo 02 T2V Standard": AtlasHailuo02T2VStandard,

    "AtlasCloud Seedance V1 Lite T2V 1080p": AtlasSeedanceV1LiteT2V1080p,
    "AtlasCloud Seedance V1 Lite T2V 720p": AtlasSeedanceV1LiteT2V720p,
    "AtlasCloud Seedance V1 Lite I2V 1080p": AtlasSeedanceV1LiteI2V1080p,

    "AtlasCloud Kling V2.0 T2V Master": AtlasKlingV20T2VMaster,
}


NODE_DISPLAY_NAME_MAPPINGS: Dict[str, str] = {
    "AtlasCloud Client": "AtlasCloud Client (API Key/Base URL)",
    "AtlasCloud WAN2.5 Text-to-Video": "AtlasCloud WAN2.5 Text-to-Video",
    "AtlasCloud WAN2.6 Text-to-Video": "AtlasCloud WAN2.6 Text-to-Video",
    "AtlasCloud WAN2.6 Text-to-Image": "AtlasCloud WAN2.6 Text-to-Image",
    "AtlasCloud WAN2.5 Text-to-Image": "AtlasCloud WAN2.5 Text-to-Image",
    "AtlasCloud WAN2.5 Image-Edit": "AtlasCloud WAN2.5 Image-Edit",
    "AtlasCloud WAN2.6 Image-Edit": "AtlasCloud WAN2.6 Image-Edit",
    "AtlasCloud WAN2.6 Image-to-Video": "AtlasCloud WAN2.6 Image-to-Video",
    "AtlasCloud WAN2.6 Image-to-Video Flash": "AtlasCloud WAN2.6 Image-to-Video Flash",
    "AtlasCloud WAN2.6 Video-to-Video": "AtlasCloud WAN2.6 Video-to-Video",

    "AtlasCloud Kling Video O3 Pro Text-to-Video": "AtlasCloud Kling Video O3 Pro Text-to-Video",
    "AtlasCloud Kling Video O3 Pro Image-to-Video": "AtlasCloud Kling Video O3 Pro Image-to-Video",
    "AtlasCloud Kling Video O3 Pro Reference-to-Video": "AtlasCloud Kling Video O3 Pro Reference-to-Video",
    "AtlasCloud Kling Video O3 Pro Video-Edit": "AtlasCloud Kling Video O3 Pro Video-Edit",

    "AtlasCloud Kling Video O3 Std Text-to-Video": "AtlasCloud Kling Video O3 Std Text-to-Video",
    "AtlasCloud Kling Video O3 Std Image-to-Video": "AtlasCloud Kling Video O3 Std Image-to-Video",
    "AtlasCloud Kling Video O3 Std Reference-to-Video": "AtlasCloud Kling Video O3 Std Reference-to-Video",
    "AtlasCloud Kling Video O3 Std Video-Edit": "AtlasCloud Kling Video O3 Std Video-Edit",
    "AtlasCloud WAN2.2 Text-to-Video 720p": "AtlasCloud WAN2.2 Text-to-Video 720p",
    "AtlasCloud WAN2.2 Text-to-Video 480p": "AtlasCloud WAN2.2 Text-to-Video 480p",
    "AtlasCloud VEO3.1 Text-to-Video": "AtlasCloud VEO3.1 Text-to-Video",
    "AtlasCloud Kling V2.6 Pro Text-to-Video": "AtlasCloud Kling V2.6 Pro Text-to-Video",
    "AtlasCloud Kling V2.6 Pro Avatar": "AtlasCloud Kling V2.6 Pro Avatar",
    "AtlasCloud Kling V2.6 Std Avatar": "AtlasCloud Kling V2.6 Std Avatar",
    "AtlasCloud Kling V2.6 Pro Motion-Control": "AtlasCloud Kling V2.6 Pro Motion-Control",
    "AtlasCloud Kling V2.6 Std Motion-Control": "AtlasCloud Kling V2.6 Std Motion-Control",
    "AtlasCloud Kling V2.6 Pro Image-to-Video": "AtlasCloud Kling V2.6 Pro Image-to-Video",
    "AtlasCloud Kling Video O1 Text-to-Video": "AtlasCloud Kling Video O1 Text-to-Video",
    "AtlasCloud Kling Video O1 Image-to-Video": "AtlasCloud Kling Video O1 Image-to-Video",
    "AtlasCloud Seedance V1 Pro Text-to-Video 1080p": "AtlasCloud Seedance V1 Pro Text-to-Video 1080p",
    "AtlasCloud Seedance V1 Pro Text-to-Video 720p": "AtlasCloud Seedance V1 Pro Text-to-Video 720p",
    "AtlasCloud Seedance V1 Pro Text-to-Video 480p": "AtlasCloud Seedance V1 Pro Text-to-Video 480p",
    "AtlasCloud Seedance V1 Lite Text-to-Video 480p": "AtlasCloud Seedance V1 Lite Text-to-Video 480p",
    "AtlasCloud Hailuo 2.3 Pro Text-to-Video": "AtlasCloud Hailuo 2.3 Pro Text-to-Video",
    "AtlasCloud Sora 2 Text-to-Video Pro": "AtlasCloud Sora 2 Text-to-Video Pro",
    "AtlasCloud Seedance V1.5 Pro Text-to-Video": "AtlasCloud Seedance V1.5 Pro Text-to-Video",
    "AtlasCloud Seedance V1.5 Pro Text-to-Video Fast": "AtlasCloud Seedance V1.5 Pro Text-to-Video Fast",
    "AtlasCloud Seedance V1.5 Pro Image-to-Video": "AtlasCloud Seedance V1.5 Pro Image-to-Video",
    "AtlasCloud Seedance V1.5 Pro Image-to-Video Fast": "AtlasCloud Seedance V1.5 Pro Image-to-Video Fast",
    "AtlasCloud Seedream V4 Text-to-Image": "AtlasCloud Seedream V4 Text-to-Image",
    "AtlasCloud Seedream V4 Sequential Text-to-Image": "AtlasCloud Seedream V4 Sequential Text-to-Image",
    "AtlasCloud Seedream V4 Edit": "AtlasCloud Seedream V4 Edit",
    "AtlasCloud Seedream V4 Edit Sequential": "AtlasCloud Seedream V4 Edit Sequential",
    "AtlasCloud Seedream V4.5 Text-to-Image": "AtlasCloud Seedream V4.5 Text-to-Image",
    "AtlasCloud Seedream V4.5 Edit": "AtlasCloud Seedream V4.5 Edit",
    "AtlasCloud Seedream V4.5 Sequential Text-to-Image": "AtlasCloud Seedream V4.5 Sequential Text-to-Image",
    "AtlasCloud Seedream V4.5 Edit Sequential": "AtlasCloud Seedream V4.5 Edit Sequential",
    "AtlasCloud Image Preview": "AtlasCloud Image Preview",
    "AtlasCloud ZImage Turbo Lora Text-to-Image": "AtlasCloud ZImage Turbo Lora Text-to-Image",
    "AtlasCloud ZImage Turbo Text-to-Image": "AtlasCloud ZImage Turbo Text-to-Image",
    "AtlasCloud Nano Banana Pro Text-to-Image Ultra": "AtlasCloud Nano Banana Pro Text-to-Image Ultra",
    "AtlasCloud Flux2 Flex Text-to-Image": "AtlasCloud Flux2 Flex Text-to-Image",
    "AtlasCloud Flux Dev Text-to-Image": "AtlasCloud Flux Dev Text-to-Image",
    "AtlasCloud Flux Dev LoRA Text-to-Image": "AtlasCloud Flux Dev LoRA Text-to-Image",
    "AtlasCloud Flux Schnell Text-to-Image": "AtlasCloud Flux Schnell Text-to-Image",
    "AtlasCloud Flux Kontext Dev Edit": "AtlasCloud Flux Kontext Dev Edit",
    "AtlasCloud Flux Kontext Dev LoRA Edit": "AtlasCloud Flux Kontext Dev LoRA Edit",
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
    "AtlasCloud Seedream V5.0 Lite Sequential Text-to-Image": "AtlasCloud Seedream V5.0 Lite Sequential Text-to-Image",
    "AtlasCloud Seedream V5.0 Lite Edit": "AtlasCloud Seedream V5.0 Lite Edit",
    "AtlasCloud Seedream V5.0 Lite Edit Sequential": "AtlasCloud Seedream V5.0 Lite Edit Sequential",
    "AtlasCloud Vidu Q3 Text-to-Video": "AtlasCloud Vidu Q3 Text-to-Video",
    "AtlasCloud Vidu Q3 Image-to-Video": "AtlasCloud Vidu Q3 Image-to-Video",
    "AtlasCloud Vidu Q3 Image-to-Video (Q3 API)": "AtlasCloud Vidu Q3 Image-to-Video (Q3 API)",
    "AtlasCloud Vidu Q3-Pro Text-to-Video": "AtlasCloud Vidu Q3-Pro Text-to-Video",
    "AtlasCloud Vidu Q3-Pro Image-to-Video": "AtlasCloud Vidu Q3-Pro Image-to-Video",
    "AtlasCloud WAN2.2 Spicy Image-to-Video": "AtlasCloud WAN2.2 Spicy Image-to-Video",
    "AtlasCloud WAN2.2 Spicy Image-to-Video LoRA": "AtlasCloud WAN2.2 Spicy Image-to-Video LoRA",
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
    "AtlasCloud VEO3.1 Fast Text-to-Video": "AtlasCloud VEO3.1 Fast Text-to-Video",
    "AtlasCloud VEO3.1 Fast Image-to-Video": "AtlasCloud VEO3.1 Fast Image-to-Video",
    "AtlasCloud VEO3.1 Reference-to-Video": "AtlasCloud VEO3.1 Reference-to-Video",
    "AtlasCloud VEO3.1 Image-to-Video": "AtlasCloud VEO3.1 Image-to-Video",
    "AtlasCloud VEO3 Image-to-Video": "AtlasCloud VEO3 Image-to-Video",
    "AtlasCloud VEO2 Text-to-Video": "AtlasCloud VEO2 Text-to-Video",
    "AtlasCloud VEO2 Image-to-Video": "AtlasCloud VEO2 Image-to-Video",
    "AtlasCloud Luma Ray 2 Flash Text-to-Video": "AtlasCloud Luma Ray 2 Flash Text-to-Video",
    "AtlasCloud Pika V2.0 Turbo Text-to-Video": "AtlasCloud Pika V2.0 Turbo Text-to-Video",
    "AtlasCloud Pika V2.1 Image-to-Video": "AtlasCloud Pika V2.1 Image-to-Video",
    "AtlasCloud PixVerse V4.5 Image-to-Video": "AtlasCloud PixVerse V4.5 Image-to-Video",
    "AtlasCloud Hailuo 02 I2V Pro": "AtlasCloud Hailuo 02 I2V Pro",
    "AtlasCloud Hailuo 02 I2V Standard": "AtlasCloud Hailuo 02 I2V Standard",
    "AtlasCloud Hailuo 02 Standard": "AtlasCloud Hailuo 02 Standard",
    "AtlasCloud Sora 2 Image-to-Video Pro": "AtlasCloud Sora 2 Image-to-Video Pro",
    "AtlasCloud Sora 2 Text-to-Video": "AtlasCloud Sora 2 Text-to-Video",
    "AtlasCloud Kling V2.5 Turbo Pro Image-to-Video": "AtlasCloud Kling V2.5 Turbo Pro Image-to-Video",
    "AtlasCloud Hunyuan Image-to-Video": "AtlasCloud Hunyuan Image-to-Video",
    "AtlasCloud WAN2.5 Image-to-Video": "AtlasCloud WAN2.5 Image-to-Video",
    "AtlasCloud WAN2.2 Image-to-Video 720p": "AtlasCloud WAN2.2 Image-to-Video 720p",
    "AtlasCloud WAN2.2 Image-to-Video 480p": "AtlasCloud WAN2.2 Image-to-Video 480p",
    "AtlasCloud WAN2.2 Animate Mix": "AtlasCloud WAN2.2 Animate Mix",
    "AtlasCloud WAN2.2 Animate Move": "AtlasCloud WAN2.2 Animate Move",
    "AtlasCloud Imagen4 Ultra Text-to-Image": "AtlasCloud Imagen4 Ultra Text-to-Image",
    "AtlasCloud Imagen3 Text-to-Image": "AtlasCloud Imagen3 Text-to-Image",
    "AtlasCloud Imagen3 Fast Text-to-Image": "AtlasCloud Imagen3 Fast Text-to-Image",
    "AtlasCloud Ideogram V3 Quality Text-to-Image": "AtlasCloud Ideogram V3 Quality Text-to-Image",
    "AtlasCloud Ideogram V3 Turbo Text-to-Image": "AtlasCloud Ideogram V3 Turbo Text-to-Image",
    "AtlasCloud Luma Photon Text-to-Image": "AtlasCloud Luma Photon Text-to-Image",
    "AtlasCloud Luma Photon Flash Text-to-Image": "AtlasCloud Luma Photon Flash Text-to-Image",
    "AtlasCloud Recraft V3 Text-to-Image": "AtlasCloud Recraft V3 Text-to-Image",
    "AtlasCloud Qwen Image Edit": "AtlasCloud Qwen Image Edit",
    "AtlasCloud Qwen Image Text-to-Image (AtlasCloud)": "AtlasCloud Qwen Image Text-to-Image (AtlasCloud)",
    "AtlasCloud Qwen Image Edit (Alibaba)": "AtlasCloud Qwen Image Edit (Alibaba)",
    "AtlasCloud Qwen Image Edit Plus (Alibaba)": "AtlasCloud Qwen Image Edit Plus (Alibaba)",
    "AtlasCloud Nano Banana Pro Text-to-Image": "AtlasCloud Nano Banana Pro Text-to-Image",
    "AtlasCloud Nano Banana Pro Text-to-Image Developer": "AtlasCloud Nano Banana Pro Text-to-Image Developer",
    "AtlasCloud Nano Banana Pro Edit": "AtlasCloud Nano Banana Pro Edit",
    "AtlasCloud Nano Banana Pro Edit Developer": "AtlasCloud Nano Banana Pro Edit Developer",
    "AtlasCloud Nano Banana Text-to-Image": "AtlasCloud Nano Banana Text-to-Image",
    "AtlasCloud Nano Banana Text-to-Image Developer": "AtlasCloud Nano Banana Text-to-Image Developer",
    "AtlasCloud Nano Banana Edit": "AtlasCloud Nano Banana Edit",
    "AtlasCloud Nano Banana Edit Developer": "AtlasCloud Nano Banana Edit Developer",
    "AtlasCloud Qwen Image Edit Plus 20251215": "AtlasCloud Qwen Image Edit Plus 20251215",
    "AtlasCloud Qwen Image Text-to-Image Plus": "AtlasCloud Qwen Image Text-to-Image Plus",
    "AtlasCloud Qwen Image Text-to-Image Max": "AtlasCloud Qwen Image Text-to-Image Max",

    "AtlasCloud Seedance V1 Pro Fast Text-to-Video": "AtlasCloud Seedance V1 Pro Fast Text-to-Video",
    "AtlasCloud Seedance V1 Pro Fast Image-to-Video": "AtlasCloud Seedance V1 Pro Fast Image-to-Video",
    "AtlasCloud Seedance V1 Pro Image-to-Video 1080p": "AtlasCloud Seedance V1 Pro Image-to-Video 1080p",
    "AtlasCloud Seedance V1 Pro Image-to-Video 720p": "AtlasCloud Seedance V1 Pro Image-to-Video 720p",
    "AtlasCloud Seedance V1 Pro Image-to-Video 480p": "AtlasCloud Seedance V1 Pro Image-to-Video 480p",
    "AtlasCloud Seedance V1 Lite Image-to-Video 720p": "AtlasCloud Seedance V1 Lite Image-to-Video 720p",
    "AtlasCloud Seedance V1 Lite Image-to-Video 480p": "AtlasCloud Seedance V1 Lite Image-to-Video 480p",
    "AtlasCloud WAN2.5 Text-to-Video Fast": "AtlasCloud WAN2.5 Text-to-Video Fast",
    "AtlasCloud WAN2.5 Image-to-Video Fast": "AtlasCloud WAN2.5 Image-to-Video Fast",
    "AtlasCloud Van-2.5 Text-to-Video": "AtlasCloud Van-2.5 Text-to-Video",
    "AtlasCloud Van-2.5 Image-to-Video": "AtlasCloud Van-2.5 Image-to-Video",
    "AtlasCloud Van-2.6 Text-to-Video": "AtlasCloud Van-2.6 Text-to-Video",
    "AtlasCloud Van-2.6 Image-to-Video": "AtlasCloud Van-2.6 Image-to-Video",
    "AtlasCloud Vidu Reference-to-Video Q1": "AtlasCloud Vidu Reference-to-Video Q1",
    "AtlasCloud Vidu Reference-to-Video 2.0": "AtlasCloud Vidu Reference-to-Video 2.0",
    "AtlasCloud Vidu Start-End-to-Video 2.0": "AtlasCloud Vidu Start-End-to-Video 2.0",
    "AtlasCloud Kling V2.0 I2V Master": "AtlasCloud Kling V2.0 I2V Master",
    "AtlasCloud VEO3 Fast Image-to-Video": "AtlasCloud VEO3 Fast Image-to-Video",
    "AtlasCloud Kling V2.1 T2V Master": "AtlasCloud Kling V2.1 T2V Master",
    "AtlasCloud Kling V2.1 I2V Master": "AtlasCloud Kling V2.1 I2V Master",
    "AtlasCloud Kling V2.1 I2V Pro (Start/End Frame)": "AtlasCloud Kling V2.1 I2V Pro (Start/End Frame)",
    "AtlasCloud Kling V2.1 I2V Pro": "AtlasCloud Kling V2.1 I2V Pro",
    "AtlasCloud Kling V2.1 I2V Standard": "AtlasCloud Kling V2.1 I2V Standard",
    "AtlasCloud Kling V1.6 Multi I2V Pro": "AtlasCloud Kling V1.6 Multi I2V Pro",
    "AtlasCloud Kling V1.6 Multi I2V Standard": "AtlasCloud Kling V1.6 Multi I2V Standard",
    "AtlasCloud Kling V1.6 I2V Standard": "AtlasCloud Kling V1.6 I2V Standard",
    "AtlasCloud Kling V1.6 T2V Standard": "AtlasCloud Kling V1.6 T2V Standard",
    "AtlasCloud Kling V1.6 I2V Pro": "AtlasCloud Kling V1.6 I2V Pro",
    "AtlasCloud Kling Effects": "AtlasCloud Kling Effects",

    "AtlasCloud Hailuo 2.3 T2V Standard": "AtlasCloud Hailuo 2.3 T2V Standard",
    "AtlasCloud Hailuo 2.3 I2V Standard": "AtlasCloud Hailuo 2.3 I2V Standard",
    "AtlasCloud Hailuo 2.3 I2V Pro": "AtlasCloud Hailuo 2.3 I2V Pro",
    "AtlasCloud Hailuo 2.3 Fast": "AtlasCloud Hailuo 2.3 Fast",

    "AtlasCloud Hailuo 02 Fast": "AtlasCloud Hailuo 02 Fast",
    "AtlasCloud Hailuo 02 Pro": "AtlasCloud Hailuo 02 Pro",
    "AtlasCloud Hailuo 02 T2V Standard": "AtlasCloud Hailuo 02 T2V Standard",

    "AtlasCloud Seedance V1 Lite T2V 1080p": "AtlasCloud Seedance V1 Lite T2V 1080p",
    "AtlasCloud Seedance V1 Lite T2V 720p": "AtlasCloud Seedance V1 Lite T2V 720p",
    "AtlasCloud Seedance V1 Lite I2V 1080p": "AtlasCloud Seedance V1 Lite I2V 1080p",

    "AtlasCloud Kling V2.0 T2V Master": "AtlasCloud Kling V2.0 T2V Master",
}


NODE_CLASS_MAPPINGS["Example"] = LegacyExample
NODE_DISPLAY_NAME_MAPPINGS["Example"] = "Example (Deprecated)"
