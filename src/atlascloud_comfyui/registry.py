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

from atlascloud_comfyui.nodes.image.seedream_v45_t2i import AtlasSeedreamV45TextToImage
from atlascloud_comfyui.nodes.image.zimage_turbo_lora_t2i import AtlasZImageTurboLoraTextToImage
from atlascloud_comfyui.nodes.image.nano_banana_pro_t2i_ultra import AtlasNanoBananaProTextToImageUltra
from atlascloud_comfyui.nodes.image.flux2_flex_t2i import AtlasFlux2FlexTextToImage

from atlascloud_comfyui.nodes.utils.image_preview import AtlasImagePreviewURL
from atlascloud_comfyui.nodes.utils.video_previewer import AtlasVideoPreviewer


from atlascloud_comfyui.nodes.image.google_nano_banana_2_text_to_image_developer_t2i import AtlasGoogleNanoBanana2TextToImageDeveloper

from atlascloud_comfyui.nodes.image.google_nano_banana_2_text_to_image_t2i import AtlasGoogleNanoBanana2TextToImage

from atlascloud_comfyui.nodes.image.bytedance_seedream_v5_0_lite_sequential_t2i import AtlasBytedanceSeedreamV50LiteSequential

from atlascloud_comfyui.nodes.image.bytedance_seedream_v5_0_lite_t2i import AtlasBytedanceSeedreamV50Lite

from atlascloud_comfyui.nodes.video.vidu_q3_image_to_video_i2v import AtlasViduQ3ImageToVideo

from atlascloud_comfyui.nodes.video.vidu_q3_text_to_video_t2v import AtlasViduQ3TextToVideo

from atlascloud_comfyui.nodes.video.kwaivgi_kling_v2_6_pro_avatar_i2v import AtlasKwaivgiKlingV26ProAvatar

from atlascloud_comfyui.nodes.video.kwaivgi_kling_v2_6_std_avatar_i2v import AtlasKwaivgiKlingV26StdAvatar

from atlascloud_comfyui.nodes.video.kwaivgi_kling_v2_6_pro_motion_control_i2v import AtlasKwaivgiKlingV26ProMotionControl

from atlascloud_comfyui.nodes.video.kwaivgi_kling_v2_6_std_motion_control_i2v import AtlasKwaivgiKlingV26StdMotionControl

from atlascloud_comfyui.nodes.video.alibaba_wan_2_6_image_to_video_flash_i2v import AtlasAlibabaWan26ImageToVideoFlash

from atlascloud_comfyui.nodes.video.bytedance_seedance_v1_5_pro_image_to_video_i2v import AtlasBytedanceSeedanceV15ProImageToVideo

from atlascloud_comfyui.nodes.video.bytedance_seedance_v1_5_pro_image_to_video_fast_i2v import AtlasBytedanceSeedanceV15ProImageToVideoFast

from atlascloud_comfyui.nodes.video.alibaba_wan_2_6_image_to_video_i2v import AtlasAlibabaWan26ImageToVideo

from atlascloud_comfyui.nodes.image.z_image_turbo_t2i import AtlasZImageTurbo

from atlascloud_comfyui.nodes.video.kwaivgi_kling_video_o3_pro_reference_to_video_i2v import AtlasKwaivgiKlingVideoO3ProReferenceToVideo

from atlascloud_comfyui.nodes.video.kwaivgi_kling_video_o3_pro_image_to_video_i2v import AtlasKwaivgiKlingVideoO3ProImageToVideo

from atlascloud_comfyui.nodes.video.kwaivgi_kling_video_o3_pro_text_to_video_t2v import AtlasKwaivgiKlingVideoO3ProTextToVideo

from atlascloud_comfyui.nodes.video.bytedance_seedance_v1_5_pro_text_to_video_fast_t2v import AtlasBytedanceSeedanceV15ProTextToVideoFast

from atlascloud_comfyui.nodes.video.kwaivgi_kling_v2_6_pro_image_to_video_i2v import AtlasKwaivgiKlingV26ProImageToVideo

from atlascloud_comfyui.nodes.video.kwaivgi_kling_video_o3_std_reference_to_video_i2v import AtlasKwaivgiKlingVideoO3StdReferenceToVideo

from atlascloud_comfyui.nodes.video.kwaivgi_kling_video_o3_std_image_to_video_i2v import AtlasKwaivgiKlingVideoO3StdImageToVideo

from atlascloud_comfyui.nodes.video.kwaivgi_kling_video_o3_std_text_to_video_t2v import AtlasKwaivgiKlingVideoO3StdTextToVideo

from atlascloud_comfyui.nodes.image.bytedance_seedream_v4_5_sequential_t2i import AtlasBytedanceSeedreamV45Sequential

from atlascloud_comfyui.nodes.video.kwaivgi_kling_video_o1_image_to_video_i2v import AtlasKwaivgiKlingVideoO1ImageToVideo

from atlascloud_comfyui.nodes.image.google_nano_banana_pro_text_to_image_t2i import AtlasGoogleNanoBananaProTextToImage

from atlascloud_comfyui.nodes.image.alibaba_qwen_image_text_to_image_max_t2i import AtlasAlibabaQwenImageTextToImageMax

from atlascloud_comfyui.nodes.image.alibaba_qwen_image_text_to_image_plus_t2i import AtlasAlibabaQwenImageTextToImagePlus

from atlascloud_comfyui.nodes.video.lightricks_ltx_2_fast_image_to_video_i2v import AtlasLightricksLtx2FastImageToVideo

from atlascloud_comfyui.nodes.video.lightricks_ltx_2_fast_text_to_video_t2v import AtlasLightricksLtx2FastTextToVideo

from atlascloud_comfyui.nodes.video.lightricks_ltx_2_pro_image_to_video_i2v import AtlasLightricksLtx2ProImageToVideo

from atlascloud_comfyui.nodes.video.lightricks_ltx_2_pro_text_to_video_t2v import AtlasLightricksLtx2ProTextToVideo

from atlascloud_comfyui.nodes.video.alibaba_wan_2_5_video_extend_fast_t2v import AtlasAlibabaWan25VideoExtendFast

from atlascloud_comfyui.nodes.video.alibaba_wan_2_5_video_extend_t2v import AtlasAlibabaWan25VideoExtend

from atlascloud_comfyui.nodes.video.minimax_hailuo_2_3_t2v_standard_t2v import AtlasMinimaxHailuo23T2vStandard

from atlascloud_comfyui.nodes.video.minimax_hailuo_2_3_i2v_standard_i2v import AtlasMinimaxHailuo23I2vStandard

from atlascloud_comfyui.nodes.video.minimax_hailuo_2_3_i2v_pro_i2v import AtlasMinimaxHailuo23I2vPro

from atlascloud_comfyui.nodes.video.minimax_hailuo_2_3_fast_i2v import AtlasMinimaxHailuo23Fast

from atlascloud_comfyui.nodes.video.bytedance_seedance_v1_pro_fast_text_to_video_t2v import AtlasBytedanceSeedanceV1ProFastTextToVideo

from atlascloud_comfyui.nodes.video.bytedance_seedance_v1_pro_fast_image_to_video_i2v import AtlasBytedanceSeedanceV1ProFastImageToVideo

from atlascloud_comfyui.nodes.video.google_veo3_1_reference_to_video_i2v import AtlasGoogleVeo31ReferenceToVideo

from atlascloud_comfyui.nodes.video.google_veo3_1_image_to_video_i2v import AtlasGoogleVeo31ImageToVideo

from atlascloud_comfyui.nodes.video.google_veo3_1_fast_text_to_video_t2v import AtlasGoogleVeo31FastTextToVideo

from atlascloud_comfyui.nodes.video.google_veo3_1_fast_image_to_video_i2v import AtlasGoogleVeo31FastImageToVideo

from atlascloud_comfyui.nodes.video.kwaivgi_kling_v2_5_turbo_pro_text_to_video_t2v import AtlasKwaivgiKlingV25TurboProTextToVideo

from atlascloud_comfyui.nodes.video.kwaivgi_kling_v2_5_turbo_pro_image_to_video_i2v import AtlasKwaivgiKlingV25TurboProImageToVideo

from atlascloud_comfyui.nodes.video.kwaivgi_kling_v2_1_i2v_pro_start_end_frame_i2v import AtlasKwaivgiKlingV21I2vProStartEndFrame

from atlascloud_comfyui.nodes.video.kwaivgi_kling_v1_6_multi_i2v_pro_i2v import AtlasKwaivgiKlingV16MultiI2vPro

from atlascloud_comfyui.nodes.video.kwaivgi_kling_v1_6_multi_i2v_standard_i2v import AtlasKwaivgiKlingV16MultiI2vStandard

from atlascloud_comfyui.nodes.video.kwaivgi_kling_effects_i2v import AtlasKwaivgiKlingEffects

from atlascloud_comfyui.nodes.video.openai_sora_t2v import AtlasOpenaiSora

from atlascloud_comfyui.nodes.video.atlascloud_van_2_6_text_to_video_t2v import AtlasAtlascloudVan26TextToVideo

from atlascloud_comfyui.nodes.video.alibaba_wan_2_5_text_to_video_fast_t2v import AtlasAlibabaWan25TextToVideoFast

from atlascloud_comfyui.nodes.video.alibaba_wan_2_5_image_to_video_i2v import AtlasAlibabaWan25ImageToVideo

from atlascloud_comfyui.nodes.video.atlascloud_van_2_6_image_to_video_i2v import AtlasAtlascloudVan26ImageToVideo

from atlascloud_comfyui.nodes.video.alibaba_wan_2_5_image_to_video_fast_i2v import AtlasAlibabaWan25ImageToVideoFast

from atlascloud_comfyui.nodes.video.atlascloud_ltx_video_v097_i2v_720p_i2v import AtlasAtlascloudLtxVideoV097I2v720p

from atlascloud_comfyui.nodes.video.alibaba_wan_2_1_t2v_720p_lora_ultra_fast_t2v import AtlasAlibabaWan21T2v720pLoraUltraFast

from atlascloud_comfyui.nodes.video.atlascloud_magi_1_24b_i2v import AtlasAtlascloudMagi124b

from atlascloud_comfyui.nodes.video.atlascloud_hunyuan_video_t2v_t2v import AtlasAtlascloudHunyuanVideoT2v

from atlascloud_comfyui.nodes.video.vidu_reference_to_video_q1_i2v import AtlasViduReferenceToVideoQ1

from atlascloud_comfyui.nodes.video.vidu_reference_to_video_2_0_i2v import AtlasViduReferenceToVideo20

from atlascloud_comfyui.nodes.video.video_effects_zoom_out_i2v import AtlasVideoEffectsZoomOut

from atlascloud_comfyui.nodes.video.video_effects_shake_dance_i2v import AtlasVideoEffectsShakeDance

from atlascloud_comfyui.nodes.video.video_effects_love_drop_i2v import AtlasVideoEffectsLoveDrop

from atlascloud_comfyui.nodes.video.video_effects_jiggle_up_i2v import AtlasVideoEffectsJiggleUp

from atlascloud_comfyui.nodes.video.video_effects_hulk_i2v import AtlasVideoEffectsHulk

from atlascloud_comfyui.nodes.video.video_effects_gender_swap_i2v import AtlasVideoEffectsGenderSwap

from atlascloud_comfyui.nodes.video.video_effects_flying_i2v import AtlasVideoEffectsFlying

from atlascloud_comfyui.nodes.video.video_effects_fishermen_i2v import AtlasVideoEffectsFishermen

from atlascloud_comfyui.nodes.video.pixverse_pixverse_v4_5_t2v_t2v import AtlasPixversePixverseV45T2v

from atlascloud_comfyui.nodes.video.pixverse_pixverse_v4_5_i2v_fast_i2v import AtlasPixversePixverseV45I2vFast

from atlascloud_comfyui.nodes.video.pika_v2_2_t2v_t2v import AtlasPikaV22T2v

from atlascloud_comfyui.nodes.video.pika_v2_1_i2v_i2v import AtlasPikaV21I2v

from atlascloud_comfyui.nodes.video.pika_v2_0_turbo_t2v_t2v import AtlasPikaV20TurboT2v

from atlascloud_comfyui.nodes.video.pika_v2_0_turbo_i2v_i2v import AtlasPikaV20TurboI2v

from atlascloud_comfyui.nodes.video.luma_ray_2_t2v_t2v import AtlasLumaRay2T2v

from atlascloud_comfyui.nodes.video.luma_ray_2_i2v_i2v import AtlasLumaRay2I2v

from atlascloud_comfyui.nodes.video.luma_ray_2_flash_t2v_t2v import AtlasLumaRay2FlashT2v

from atlascloud_comfyui.nodes.video.kwaivgi_kling_v2_0_i2v_master_i2v import AtlasKwaivgiKlingV20I2vMaster

from atlascloud_comfyui.nodes.video.google_veo3_t2v import AtlasGoogleVeo3

from atlascloud_comfyui.nodes.video.google_veo3_image_to_video_i2v import AtlasGoogleVeo3ImageToVideo

from atlascloud_comfyui.nodes.video.google_veo2_t2v import AtlasGoogleVeo2

from atlascloud_comfyui.nodes.video.google_veo2_image_to_video_i2v import AtlasGoogleVeo2ImageToVideo

from atlascloud_comfyui.nodes.video.kwaivgi_kling_lipsync_text_to_video_t2v import AtlasKwaivgiKlingLipsyncTextToVideo

from atlascloud_comfyui.nodes.video.minimax_hailuo_02_t2v_pro_i2v import AtlasMinimaxHailuo02T2vPro

from atlascloud_comfyui.nodes.video.alibaba_wan_2_1_t2v_720p_ultra_fast_t2v import AtlasAlibabaWan21T2v720pUltraFast

from atlascloud_comfyui.nodes.video.alibaba_wan_2_1_t2v_720p_lora_t2v import AtlasAlibabaWan21T2v720pLora

from atlascloud_comfyui.nodes.video.alibaba_wan_2_1_t2v_480p_ultra_fast_t2v import AtlasAlibabaWan21T2v480pUltraFast

from atlascloud_comfyui.nodes.video.alibaba_wan_2_1_t2v_480p_lora_ultra_fast_t2v import AtlasAlibabaWan21T2v480pLoraUltraFast

from atlascloud_comfyui.nodes.video.alibaba_wan_2_2_t2v_5b_720p_lora_t2v import AtlasAlibabaWan22T2v5b720pLora

from atlascloud_comfyui.nodes.video.google_veo3_fast_image_to_video_i2v import AtlasGoogleVeo3FastImageToVideo

from atlascloud_comfyui.nodes.video.vidu_start_end_to_video_2_0_i2v import AtlasViduStartEndToVideo20

from atlascloud_comfyui.nodes.video.video_effects_sexy_me_i2v import AtlasVideoEffectsSexyMe

from atlascloud_comfyui.nodes.video.kwaivgi_kling_v2_1_t2v_master_t2v import AtlasKwaivgiKlingV21T2vMaster

from atlascloud_comfyui.nodes.video.kwaivgi_kling_v2_0_t2v_master_t2v import AtlasKwaivgiKlingV20T2vMaster

from atlascloud_comfyui.nodes.video.alibaba_wan_2_2_i2v_5b_720p_lora_i2v import AtlasAlibabaWan22I2v5b720pLora

from atlascloud_comfyui.nodes.video.atlascloud_framepack_i2v import AtlasAtlascloudFramepack

from atlascloud_comfyui.nodes.video.video_effects_body_shake_i2v import AtlasVideoEffectsBodyShake

from atlascloud_comfyui.nodes.video.bytedance_lipsync_audio_to_video_t2v import AtlasBytedanceLipsyncAudioToVideo

from atlascloud_comfyui.nodes.video.alibaba_wan_2_2_t2v_480p_lora_ultra_fast_t2v import AtlasAlibabaWan22T2v480pLoraUltraFast

from atlascloud_comfyui.nodes.video.alibaba_wan_2_1_t2v_720p_t2v import AtlasAlibabaWan21T2v720p

from atlascloud_comfyui.nodes.video.atlascloud_multitalk_i2v import AtlasAtlascloudMultitalk

from atlascloud_comfyui.nodes.video.vidu_image_to_video_2_0_i2v import AtlasViduImageToVideo20

from atlascloud_comfyui.nodes.video.video_effects_french_kiss_i2v import AtlasVideoEffectsFrenchKiss

from atlascloud_comfyui.nodes.video.minimax_video_02_i2v import AtlasMinimaxVideo02

from atlascloud_comfyui.nodes.video.minimax_video_01_i2v import AtlasMinimaxVideo01

from atlascloud_comfyui.nodes.video.minimax_hailuo_02_fast_i2v import AtlasMinimaxHailuo02Fast

from atlascloud_comfyui.nodes.video.kwaivgi_kling_lipsync_audio_to_video_t2v import AtlasKwaivgiKlingLipsyncAudioToVideo

from atlascloud_comfyui.nodes.video.bytedance_seedance_v1_lite_t2v_1080p_t2v import AtlasBytedanceSeedanceV1LiteT2v1080p

from atlascloud_comfyui.nodes.video.alibaba_wan_flf2v_i2v import AtlasAlibabaWanFlf2v

from atlascloud_comfyui.nodes.video.alibaba_wan_2_2_i2v_720p_ultra_fast_i2v import AtlasAlibabaWan22I2v720pUltraFast

from atlascloud_comfyui.nodes.video.alibaba_wan_2_2_i2v_720p_lora_ultra_fast_i2v import AtlasAlibabaWan22I2v720pLoraUltraFast

from atlascloud_comfyui.nodes.video.alibaba_wan_2_2_i2v_480p_ultra_fast_i2v import AtlasAlibabaWan22I2v480pUltraFast

from atlascloud_comfyui.nodes.video.alibaba_wan_2_2_i2v_480p_lora_ultra_fast_i2v import AtlasAlibabaWan22I2v480pLoraUltraFast

from atlascloud_comfyui.nodes.video.alibaba_wan_2_1_i2v_720p_ultra_fast_i2v import AtlasAlibabaWan21I2v720pUltraFast

from atlascloud_comfyui.nodes.video.alibaba_wan_2_1_i2v_480p_ultra_fast_i2v import AtlasAlibabaWan21I2v480pUltraFast

from atlascloud_comfyui.nodes.video.alibaba_wan_2_1_14b_vace_i2v import AtlasAlibabaWan2114bVace

from atlascloud_comfyui.nodes.video.minimax_hailuo_02_pro_i2v import AtlasMinimaxHailuo02Pro

from atlascloud_comfyui.nodes.video.kwaivgi_kling_v2_1_i2v_master_i2v import AtlasKwaivgiKlingV21I2vMaster

from atlascloud_comfyui.nodes.video.bytedance_seedance_v1_lite_t2v_720p_t2v import AtlasBytedanceSeedanceV1LiteT2v720p

from atlascloud_comfyui.nodes.video.bytedance_seedance_v1_lite_i2v_1080p_i2v import AtlasBytedanceSeedanceV1LiteI2v1080p

from atlascloud_comfyui.nodes.video.bytedance_avatar_omni_human_i2v import AtlasBytedanceAvatarOmniHuman

from atlascloud_comfyui.nodes.video.alibaba_wan_2_2_spicy_image_to_video_lora_i2v import AtlasAlibabaWan22SpicyImageToVideoLora

from atlascloud_comfyui.nodes.video.alibaba_wan_2_2_spicy_image_to_video_i2v import AtlasAlibabaWan22SpicyImageToVideo

from atlascloud_comfyui.nodes.video.alibaba_wan_2_2_t2v_480p_ultra_fast_t2v import AtlasAlibabaWan22T2v480pUltraFast

from atlascloud_comfyui.nodes.video.alibaba_wan_2_2_t2v_5b_720p_t2v import AtlasAlibabaWan22T2v5b720p

from atlascloud_comfyui.nodes.video.alibaba_wan_2_2_i2v_5b_720p_i2v import AtlasAlibabaWan22I2v5b720p

from atlascloud_comfyui.nodes.video.atlascloud_hunyuan_video_i2v_i2v import AtlasAtlascloudHunyuanVideoI2v

from atlascloud_comfyui.nodes.video.pixverse_pixverse_v4_5_i2v_i2v import AtlasPixversePixverseV45I2v

from atlascloud_comfyui.nodes.video.minimax_hailuo_02_t2v_standard_t2v import AtlasMinimaxHailuo02T2vStandard

from atlascloud_comfyui.nodes.video.minimax_hailuo_02_i2v_standard_i2v import AtlasMinimaxHailuo02I2vStandard

from atlascloud_comfyui.nodes.video.minimax_hailuo_02_i2v_pro_i2v import AtlasMinimaxHailuo02I2vPro

from atlascloud_comfyui.nodes.video.kwaivgi_kling_v2_1_i2v_pro_i2v import AtlasKwaivgiKlingV21I2vPro

from atlascloud_comfyui.nodes.video.kwaivgi_kling_v1_6_t2v_standard_t2v import AtlasKwaivgiKlingV16T2vStandard

from atlascloud_comfyui.nodes.video.kwaivgi_kling_v1_6_i2v_pro_i2v import AtlasKwaivgiKlingV16I2vPro

from atlascloud_comfyui.nodes.video.google_veo3_fast_t2v import AtlasGoogleVeo3Fast

from atlascloud_comfyui.nodes.video.alibaba_wan_2_2_i2v_480p_i2v import AtlasAlibabaWan22I2v480p

from atlascloud_comfyui.nodes.video.alibaba_wan_2_2_i2v_720p_i2v import AtlasAlibabaWan22I2v720p

from atlascloud_comfyui.nodes.video.alibaba_wan_2_2_t2v_480p_t2v import AtlasAlibabaWan22T2v480p

from atlascloud_comfyui.nodes.video.alibaba_wan_2_1_t2v_480p_lora_t2v import AtlasAlibabaWan21T2v480pLora

from atlascloud_comfyui.nodes.video.alibaba_wan_2_1_i2v_720p_lora_ultra_fast_i2v import AtlasAlibabaWan21I2v720pLoraUltraFast

from atlascloud_comfyui.nodes.video.alibaba_wan_2_1_i2v_720p_lora_i2v import AtlasAlibabaWan21I2v720pLora

from atlascloud_comfyui.nodes.video.alibaba_wan_2_1_i2v_720p_i2v import AtlasAlibabaWan21I2v720p

from atlascloud_comfyui.nodes.video.alibaba_wan_2_1_i2v_480p_lora_ultra_fast_i2v import AtlasAlibabaWan21I2v480pLoraUltraFast

from atlascloud_comfyui.nodes.video.alibaba_wan_2_1_i2v_480p_lora_i2v import AtlasAlibabaWan21I2v480pLora

from atlascloud_comfyui.nodes.video.alibaba_wan_2_1_i2v_480p_i2v import AtlasAlibabaWan21I2v480p

from atlascloud_comfyui.nodes.video.bytedance_seedance_v1_pro_t2v_720p_t2v import AtlasBytedanceSeedanceV1ProT2v720p

from atlascloud_comfyui.nodes.video.bytedance_seedance_v1_pro_t2v_480p_t2v import AtlasBytedanceSeedanceV1ProT2v480p

from atlascloud_comfyui.nodes.video.bytedance_seedance_v1_pro_i2v_720p_i2v import AtlasBytedanceSeedanceV1ProI2v720p

from atlascloud_comfyui.nodes.video.bytedance_seedance_v1_pro_i2v_480p_i2v import AtlasBytedanceSeedanceV1ProI2v480p

from atlascloud_comfyui.nodes.video.bytedance_seedance_v1_pro_i2v_1080p_i2v import AtlasBytedanceSeedanceV1ProI2v1080p

from atlascloud_comfyui.nodes.video.bytedance_seedance_v1_lite_t2v_480p_t2v import AtlasBytedanceSeedanceV1LiteT2v480p

from atlascloud_comfyui.nodes.video.bytedance_seedance_v1_lite_i2v_720p_i2v import AtlasBytedanceSeedanceV1LiteI2v720p

from atlascloud_comfyui.nodes.video.bytedance_seedance_v1_lite_i2v_480p_i2v import AtlasBytedanceSeedanceV1LiteI2v480p

from atlascloud_comfyui.nodes.video.kwaivgi_kling_v2_1_i2v_standard_i2v import AtlasKwaivgiKlingV21I2vStandard

from atlascloud_comfyui.nodes.video.kwaivgi_kling_v1_6_i2v_standard_i2v import AtlasKwaivgiKlingV16I2vStandard

from atlascloud_comfyui.nodes.video.minimax_hailuo_02_standard_i2v import AtlasMinimaxHailuo02Standard

from atlascloud_comfyui.nodes.image.atlascloud_hunyuan_image_3_t2i import AtlasAtlascloudHunyuanImage3

from atlascloud_comfyui.nodes.image.alibaba_wan_2_5_text_to_image_t2i import AtlasAlibabaWan25TextToImage

from atlascloud_comfyui.nodes.image.bytedance_seedream_v4_t2i import AtlasBytedanceSeedreamV4

from atlascloud_comfyui.nodes.image.bytedance_seedream_v4_sequential_t2i import AtlasBytedanceSeedreamV4Sequential

from atlascloud_comfyui.nodes.image.google_nano_banana_pro_text_to_image_developer_t2i import AtlasGoogleNanoBananaProTextToImageDeveloper

from atlascloud_comfyui.nodes.image.google_nano_banana_text_to_image_developer_t2i import AtlasGoogleNanoBananaTextToImageDeveloper

from atlascloud_comfyui.nodes.video.atlascloud_van_2_5_image_to_video_i2v import AtlasAtlascloudVan25ImageToVideo

from atlascloud_comfyui.nodes.video.alibaba_wan_2_2_animate_mix_i2v import AtlasAlibabaWan22AnimateMix

from atlascloud_comfyui.nodes.video.alibaba_wan_2_2_animate_move_i2v import AtlasAlibabaWan22AnimateMove

from atlascloud_comfyui.nodes.image.alibaba_wan_2_6_text_to_image_t2i import AtlasAlibabaWan26TextToImage

from atlascloud_comfyui.nodes.video.atlascloud_van_2_5_text_to_video_t2v import AtlasAtlascloudVan25TextToVideo

from atlascloud_comfyui.nodes.image.google_nano_banana_text_to_image_t2i import AtlasGoogleNanoBananaTextToImage

from atlascloud_comfyui.nodes.image.bytedance_seedream_v3_1_t2i import AtlasBytedanceSeedreamV31

from atlascloud_comfyui.nodes.image.atlascloud_neta_lumina_t2i import AtlasAtlascloudNetaLumina

from atlascloud_comfyui.nodes.image.recraft_ai_recraft_v3_svg_t2i import AtlasRecraftAiRecraftV3Svg

from atlascloud_comfyui.nodes.image.recraft_ai_recraft_20b_t2i import AtlasRecraftAiRecraft20b

from atlascloud_comfyui.nodes.image.recraft_ai_recraft_20b_svg_t2i import AtlasRecraftAiRecraft20bSvg

from atlascloud_comfyui.nodes.image.ideogram_ai_ideogram_v2a_turbo_t2i import AtlasIdeogramAiIdeogramV2aTurbo

from atlascloud_comfyui.nodes.image.ideogram_ai_ideogram_v2_t2i import AtlasIdeogramAiIdeogramV2

from atlascloud_comfyui.nodes.image.ideogram_ai_ideogram_v2_turbo_t2i import AtlasIdeogramAiIdeogramV2Turbo

from atlascloud_comfyui.nodes.image.luma_photon_t2i import AtlasLumaPhoton

from atlascloud_comfyui.nodes.image.google_imagen3_t2i import AtlasGoogleImagen3

from atlascloud_comfyui.nodes.image.luma_photon_flash_t2i import AtlasLumaPhotonFlash

from atlascloud_comfyui.nodes.image.ideogram_ai_ideogram_v3_balanced_t2i import AtlasIdeogramAiIdeogramV3Balanced

from atlascloud_comfyui.nodes.image.google_imagen3_fast_t2i import AtlasGoogleImagen3Fast

from atlascloud_comfyui.nodes.image.atlascloud_qwen_image_text_to_image_t2i import AtlasAtlascloudQwenImageTextToImage

from atlascloud_comfyui.nodes.image.atlascloud_imagen4_t2i import AtlasAtlascloudImagen4

from atlascloud_comfyui.nodes.image.black_forest_labs_flux_1_1_pro_t2i import AtlasBlackForestLabsFlux11Pro

from atlascloud_comfyui.nodes.image.black_forest_labs_flux_1_1_pro_ultra_t2i import AtlasBlackForestLabsFlux11ProUltra

from atlascloud_comfyui.nodes.image.recraft_ai_recraft_v3_t2i import AtlasRecraftAiRecraftV3

from atlascloud_comfyui.nodes.image.ideogram_ai_ideogram_v3_turbo_t2i import AtlasIdeogramAiIdeogramV3Turbo

from atlascloud_comfyui.nodes.image.google_imagen4_fast_t2i import AtlasGoogleImagen4Fast

from atlascloud_comfyui.nodes.image.black_forest_labs_flux_dev_t2i import AtlasBlackForestLabsFluxDev

from atlascloud_comfyui.nodes.image.black_forest_labs_flux_dev_lora_ultra_fast_t2i import AtlasBlackForestLabsFluxDevLoraUltraFast

from atlascloud_comfyui.nodes.image.black_forest_labs_flux_dev_lora_t2i import AtlasBlackForestLabsFluxDevLora

from atlascloud_comfyui.nodes.image.black_forest_labs_flux_dev_ultra_fast_t2i import AtlasBlackForestLabsFluxDevUltraFast

from atlascloud_comfyui.nodes.image.ideogram_ai_ideogram_v3_quality_t2i import AtlasIdeogramAiIdeogramV3Quality

from atlascloud_comfyui.nodes.image.google_imagen4_ultra_t2i import AtlasGoogleImagen4Ultra

from atlascloud_comfyui.nodes.image.google_imagen4_t2i import AtlasGoogleImagen4

from atlascloud_comfyui.nodes.image.black_forest_labs_flux_kontext_pro_text_to_image_t2i import AtlasBlackForestLabsFluxKontextProTextToImage

from atlascloud_comfyui.nodes.image.black_forest_labs_flux_kontext_max_text_to_image_t2i import AtlasBlackForestLabsFluxKontextMaxTextToImage

from atlascloud_comfyui.nodes.image.atlascloud_hidream_i1_full_t2i import AtlasAtlascloudHidreamI1Full

from atlascloud_comfyui.nodes.image.atlascloud_hidream_i1_dev_t2i import AtlasAtlascloudHidreamI1Dev

from atlascloud_comfyui.nodes.image.black_forest_labs_flux_schnell_lora_t2i import AtlasBlackForestLabsFluxSchnellLora

from atlascloud_comfyui.nodes.image.alibaba_wan_2_1_text_to_image_t2i import AtlasAlibabaWan21TextToImage

from atlascloud_comfyui.nodes.image.black_forest_labs_flux_schnell_t2i import AtlasBlackForestLabsFluxSchnell

from atlascloud_comfyui.nodes.image.bytedance_seedream_v3_t2i import AtlasBytedanceSeedreamV3

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
}

from atlascloud_comfyui.nodes.image.google_nano_banana_2_text_to_image_developer_t2i import AtlasGoogleNanoBanana2TextToImageDeveloper
    "AtlasCloud Nano Banana 2 Text-to-Image Developer": AtlasGoogleNanoBanana2TextToImageDeveloper,

from atlascloud_comfyui.nodes.image.google_nano_banana_2_text_to_image_t2i import AtlasGoogleNanoBanana2TextToImage
    "AtlasCloud Nano Banana 2 Text-to-Image": AtlasGoogleNanoBanana2TextToImage,

from atlascloud_comfyui.nodes.image.bytedance_seedream_v5_0_lite_sequential_t2i import AtlasBytedanceSeedreamV50LiteSequential
    "AtlasCloud Seedream v5.0 Lite Sequential": AtlasBytedanceSeedreamV50LiteSequential,

from atlascloud_comfyui.nodes.image.bytedance_seedream_v5_0_lite_t2i import AtlasBytedanceSeedreamV50Lite
    "AtlasCloud Seedream v5.0 Lite": AtlasBytedanceSeedreamV50Lite,

from atlascloud_comfyui.nodes.video.vidu_q3_image_to_video_i2v import AtlasViduQ3ImageToVideo
    "AtlasCloud Vidu Q3 Image-to-video": AtlasViduQ3ImageToVideo,

from atlascloud_comfyui.nodes.video.vidu_q3_text_to_video_t2v import AtlasViduQ3TextToVideo
    "AtlasCloud Vidu Q3 Text-to-video": AtlasViduQ3TextToVideo,

from atlascloud_comfyui.nodes.video.kwaivgi_kling_v2_6_pro_avatar_i2v import AtlasKwaivgiKlingV26ProAvatar
    "AtlasCloud Kling v2.6 Pro Avatar": AtlasKwaivgiKlingV26ProAvatar,

from atlascloud_comfyui.nodes.video.kwaivgi_kling_v2_6_std_avatar_i2v import AtlasKwaivgiKlingV26StdAvatar
    "AtlasCloud Kling v2.6 Std Avatar": AtlasKwaivgiKlingV26StdAvatar,

from atlascloud_comfyui.nodes.video.kwaivgi_kling_v2_6_pro_motion_control_i2v import AtlasKwaivgiKlingV26ProMotionControl
    "AtlasCloud Kling v2.6 Pro Motion Control": AtlasKwaivgiKlingV26ProMotionControl,

from atlascloud_comfyui.nodes.video.kwaivgi_kling_v2_6_std_motion_control_i2v import AtlasKwaivgiKlingV26StdMotionControl
    "AtlasCloud Kling v2.6 Std Motion Control": AtlasKwaivgiKlingV26StdMotionControl,

from atlascloud_comfyui.nodes.video.alibaba_wan_2_6_image_to_video_flash_i2v import AtlasAlibabaWan26ImageToVideoFlash
    "AtlasCloud Wan-2.6 Image-to-video Flash": AtlasAlibabaWan26ImageToVideoFlash,

from atlascloud_comfyui.nodes.video.bytedance_seedance_v1_5_pro_image_to_video_i2v import AtlasBytedanceSeedanceV15ProImageToVideo
    "AtlasCloud Seedance v1.5 Pro Image-to-Video": AtlasBytedanceSeedanceV15ProImageToVideo,

from atlascloud_comfyui.nodes.video.bytedance_seedance_v1_5_pro_image_to_video_fast_i2v import AtlasBytedanceSeedanceV15ProImageToVideoFast
    "AtlasCloud Seedance v1.5 Pro Image-to-Video Fast": AtlasBytedanceSeedanceV15ProImageToVideoFast,

from atlascloud_comfyui.nodes.video.alibaba_wan_2_6_image_to_video_i2v import AtlasAlibabaWan26ImageToVideo
    "AtlasCloud Wan-2.6 Image-to-video": AtlasAlibabaWan26ImageToVideo,

from atlascloud_comfyui.nodes.image.z_image_turbo_t2i import AtlasZImageTurbo
    "AtlasCloud Z-Image Turbo": AtlasZImageTurbo,

from atlascloud_comfyui.nodes.video.kwaivgi_kling_video_o3_pro_reference_to_video_i2v import AtlasKwaivgiKlingVideoO3ProReferenceToVideo
    "AtlasCloud Kling Video O3 Pro Reference-to-Video": AtlasKwaivgiKlingVideoO3ProReferenceToVideo,

from atlascloud_comfyui.nodes.video.kwaivgi_kling_video_o3_pro_image_to_video_i2v import AtlasKwaivgiKlingVideoO3ProImageToVideo
    "AtlasCloud Kling Video O3 Pro Image-to-Video": AtlasKwaivgiKlingVideoO3ProImageToVideo,

from atlascloud_comfyui.nodes.video.kwaivgi_kling_video_o3_pro_text_to_video_t2v import AtlasKwaivgiKlingVideoO3ProTextToVideo
    "AtlasCloud Kling Video O3 Pro Text-to-Video": AtlasKwaivgiKlingVideoO3ProTextToVideo,

from atlascloud_comfyui.nodes.video.bytedance_seedance_v1_5_pro_text_to_video_fast_t2v import AtlasBytedanceSeedanceV15ProTextToVideoFast
    "AtlasCloud Seedance v1.5 Pro Text-to-Video Fast": AtlasBytedanceSeedanceV15ProTextToVideoFast,

from atlascloud_comfyui.nodes.video.kwaivgi_kling_v2_6_pro_image_to_video_i2v import AtlasKwaivgiKlingV26ProImageToVideo
    "AtlasCloud Kling v2.6 Pro Image-to-Video": AtlasKwaivgiKlingV26ProImageToVideo,

from atlascloud_comfyui.nodes.video.kwaivgi_kling_video_o3_std_reference_to_video_i2v import AtlasKwaivgiKlingVideoO3StdReferenceToVideo
    "AtlasCloud Kling Video O3 Std Reference-to-Video": AtlasKwaivgiKlingVideoO3StdReferenceToVideo,

from atlascloud_comfyui.nodes.video.kwaivgi_kling_video_o3_std_image_to_video_i2v import AtlasKwaivgiKlingVideoO3StdImageToVideo
    "AtlasCloud Kling Video O3 Std Image-to-Video": AtlasKwaivgiKlingVideoO3StdImageToVideo,

from atlascloud_comfyui.nodes.video.kwaivgi_kling_video_o3_std_text_to_video_t2v import AtlasKwaivgiKlingVideoO3StdTextToVideo
    "AtlasCloud Kling Video O3 Std Text-to-Video": AtlasKwaivgiKlingVideoO3StdTextToVideo,

from atlascloud_comfyui.nodes.image.bytedance_seedream_v4_5_sequential_t2i import AtlasBytedanceSeedreamV45Sequential
    "AtlasCloud Seedream v4.5 Sequential": AtlasBytedanceSeedreamV45Sequential,

from atlascloud_comfyui.nodes.video.kwaivgi_kling_video_o1_image_to_video_i2v import AtlasKwaivgiKlingVideoO1ImageToVideo
    "AtlasCloud Kling Video O1 Image-to-video": AtlasKwaivgiKlingVideoO1ImageToVideo,

from atlascloud_comfyui.nodes.image.google_nano_banana_pro_text_to_image_t2i import AtlasGoogleNanoBananaProTextToImage
    "AtlasCloud Nano Banana Pro Text-to-image": AtlasGoogleNanoBananaProTextToImage,

from atlascloud_comfyui.nodes.image.alibaba_qwen_image_text_to_image_max_t2i import AtlasAlibabaQwenImageTextToImageMax
    "AtlasCloud Qwen-Image Text-to-image Max": AtlasAlibabaQwenImageTextToImageMax,

from atlascloud_comfyui.nodes.image.alibaba_qwen_image_text_to_image_plus_t2i import AtlasAlibabaQwenImageTextToImagePlus
    "AtlasCloud Qwen-Image Text-to-image Plus": AtlasAlibabaQwenImageTextToImagePlus,

from atlascloud_comfyui.nodes.video.lightricks_ltx_2_fast_image_to_video_i2v import AtlasLightricksLtx2FastImageToVideo
    "AtlasCloud Ltx-2 Fast Image-to-video": AtlasLightricksLtx2FastImageToVideo,

from atlascloud_comfyui.nodes.video.lightricks_ltx_2_fast_text_to_video_t2v import AtlasLightricksLtx2FastTextToVideo
    "AtlasCloud Ltx-2 Fast Text-to-video": AtlasLightricksLtx2FastTextToVideo,

from atlascloud_comfyui.nodes.video.lightricks_ltx_2_pro_image_to_video_i2v import AtlasLightricksLtx2ProImageToVideo
    "AtlasCloud Ltx-2 Pro Image-to-video": AtlasLightricksLtx2ProImageToVideo,

from atlascloud_comfyui.nodes.video.lightricks_ltx_2_pro_text_to_video_t2v import AtlasLightricksLtx2ProTextToVideo
    "AtlasCloud Ltx-2 Pro Text-to-video": AtlasLightricksLtx2ProTextToVideo,

from atlascloud_comfyui.nodes.video.alibaba_wan_2_5_video_extend_fast_t2v import AtlasAlibabaWan25VideoExtendFast
    "AtlasCloud Wan-2.5 Video Extend Fast": AtlasAlibabaWan25VideoExtendFast,

from atlascloud_comfyui.nodes.video.alibaba_wan_2_5_video_extend_t2v import AtlasAlibabaWan25VideoExtend
    "AtlasCloud Wan-2.5 Video Extend": AtlasAlibabaWan25VideoExtend,

from atlascloud_comfyui.nodes.video.minimax_hailuo_2_3_t2v_standard_t2v import AtlasMinimaxHailuo23T2vStandard
    "AtlasCloud Hailuo-2.3 t2v Standard": AtlasMinimaxHailuo23T2vStandard,

from atlascloud_comfyui.nodes.video.minimax_hailuo_2_3_i2v_standard_i2v import AtlasMinimaxHailuo23I2vStandard
    "AtlasCloud Hailuo-2.3 i2v Standard": AtlasMinimaxHailuo23I2vStandard,

from atlascloud_comfyui.nodes.video.minimax_hailuo_2_3_i2v_pro_i2v import AtlasMinimaxHailuo23I2vPro
    "AtlasCloud Hailuo-2.3 i2v Pro": AtlasMinimaxHailuo23I2vPro,

from atlascloud_comfyui.nodes.video.minimax_hailuo_2_3_fast_i2v import AtlasMinimaxHailuo23Fast
    "AtlasCloud Hailuo-2.3 Fast": AtlasMinimaxHailuo23Fast,

from atlascloud_comfyui.nodes.video.bytedance_seedance_v1_pro_fast_text_to_video_t2v import AtlasBytedanceSeedanceV1ProFastTextToVideo
    "AtlasCloud Seedance v1 Pro Fast Text-to-video": AtlasBytedanceSeedanceV1ProFastTextToVideo,

from atlascloud_comfyui.nodes.video.bytedance_seedance_v1_pro_fast_image_to_video_i2v import AtlasBytedanceSeedanceV1ProFastImageToVideo
    "AtlasCloud Seedance v1 Pro Fast Image-to-video": AtlasBytedanceSeedanceV1ProFastImageToVideo,

from atlascloud_comfyui.nodes.video.google_veo3_1_reference_to_video_i2v import AtlasGoogleVeo31ReferenceToVideo
    "AtlasCloud Veo3.1 Reference-to-video": AtlasGoogleVeo31ReferenceToVideo,

from atlascloud_comfyui.nodes.video.google_veo3_1_image_to_video_i2v import AtlasGoogleVeo31ImageToVideo
    "AtlasCloud Veo3.1 Image-to-video": AtlasGoogleVeo31ImageToVideo,

from atlascloud_comfyui.nodes.video.google_veo3_1_fast_text_to_video_t2v import AtlasGoogleVeo31FastTextToVideo
    "AtlasCloud Veo3.1 Fast Text-to-video": AtlasGoogleVeo31FastTextToVideo,

from atlascloud_comfyui.nodes.video.google_veo3_1_fast_image_to_video_i2v import AtlasGoogleVeo31FastImageToVideo
    "AtlasCloud Veo3.1 Fast Image-to-video": AtlasGoogleVeo31FastImageToVideo,

from atlascloud_comfyui.nodes.video.kwaivgi_kling_v2_5_turbo_pro_text_to_video_t2v import AtlasKwaivgiKlingV25TurboProTextToVideo
    "AtlasCloud Kling v2.5 Turbo Pro Text-to-video": AtlasKwaivgiKlingV25TurboProTextToVideo,

from atlascloud_comfyui.nodes.video.kwaivgi_kling_v2_5_turbo_pro_image_to_video_i2v import AtlasKwaivgiKlingV25TurboProImageToVideo
    "AtlasCloud Kling v2.5 Turbo Pro Image-to-video": AtlasKwaivgiKlingV25TurboProImageToVideo,

from atlascloud_comfyui.nodes.video.kwaivgi_kling_v2_1_i2v_pro_start_end_frame_i2v import AtlasKwaivgiKlingV21I2vProStartEndFrame
    "AtlasCloud Kling v2.1 i2v Pro Start-end-frame": AtlasKwaivgiKlingV21I2vProStartEndFrame,

from atlascloud_comfyui.nodes.video.kwaivgi_kling_v1_6_multi_i2v_pro_i2v import AtlasKwaivgiKlingV16MultiI2vPro
    "AtlasCloud Kling v1.6 Multi i2v Pro": AtlasKwaivgiKlingV16MultiI2vPro,

from atlascloud_comfyui.nodes.video.kwaivgi_kling_v1_6_multi_i2v_standard_i2v import AtlasKwaivgiKlingV16MultiI2vStandard
    "AtlasCloud Kling v1.6 Multi i2v Standard": AtlasKwaivgiKlingV16MultiI2vStandard,

from atlascloud_comfyui.nodes.video.kwaivgi_kling_effects_i2v import AtlasKwaivgiKlingEffects
    "AtlasCloud Kling Effects": AtlasKwaivgiKlingEffects,

from atlascloud_comfyui.nodes.video.openai_sora_t2v import AtlasOpenaiSora
    "AtlasCloud Sora": AtlasOpenaiSora,

from atlascloud_comfyui.nodes.video.atlascloud_van_2_6_text_to_video_t2v import AtlasAtlascloudVan26TextToVideo
    "AtlasCloud Van-2.6 Text-to-video": AtlasAtlascloudVan26TextToVideo,

from atlascloud_comfyui.nodes.video.alibaba_wan_2_5_text_to_video_fast_t2v import AtlasAlibabaWan25TextToVideoFast
    "AtlasCloud Wan-2.5 Text-to-video Fast": AtlasAlibabaWan25TextToVideoFast,

from atlascloud_comfyui.nodes.video.alibaba_wan_2_5_image_to_video_i2v import AtlasAlibabaWan25ImageToVideo
    "AtlasCloud Wan-2.5 Image-to-video": AtlasAlibabaWan25ImageToVideo,

from atlascloud_comfyui.nodes.video.atlascloud_van_2_6_image_to_video_i2v import AtlasAtlascloudVan26ImageToVideo
    "AtlasCloud Van-2.6 Image-to-video": AtlasAtlascloudVan26ImageToVideo,

from atlascloud_comfyui.nodes.video.alibaba_wan_2_5_image_to_video_fast_i2v import AtlasAlibabaWan25ImageToVideoFast
    "AtlasCloud Wan-2.5 Image-to-video Fast": AtlasAlibabaWan25ImageToVideoFast,

from atlascloud_comfyui.nodes.video.atlascloud_ltx_video_v097_i2v_720p_i2v import AtlasAtlascloudLtxVideoV097I2v720p
    "AtlasCloud Ltx-Video v097 i2v 720p": AtlasAtlascloudLtxVideoV097I2v720p,

from atlascloud_comfyui.nodes.video.alibaba_wan_2_1_t2v_720p_lora_ultra_fast_t2v import AtlasAlibabaWan21T2v720pLoraUltraFast
    "AtlasCloud Wan-2.1 t2v 720p Lora Ultra Fast": AtlasAlibabaWan21T2v720pLoraUltraFast,

from atlascloud_comfyui.nodes.video.atlascloud_magi_1_24b_i2v import AtlasAtlascloudMagi124b
    "AtlasCloud Magi-1 24b": AtlasAtlascloudMagi124b,

from atlascloud_comfyui.nodes.video.atlascloud_hunyuan_video_t2v_t2v import AtlasAtlascloudHunyuanVideoT2v
    "AtlasCloud Hunyuan Video t2v": AtlasAtlascloudHunyuanVideoT2v,

from atlascloud_comfyui.nodes.video.vidu_reference_to_video_q1_i2v import AtlasViduReferenceToVideoQ1
    "AtlasCloud Vidu Reference-to-Video Q1": AtlasViduReferenceToVideoQ1,

from atlascloud_comfyui.nodes.video.vidu_reference_to_video_2_0_i2v import AtlasViduReferenceToVideo20
    "AtlasCloud Vidu Reference-to-Video 2.0": AtlasViduReferenceToVideo20,

from atlascloud_comfyui.nodes.video.video_effects_zoom_out_i2v import AtlasVideoEffectsZoomOut
    "AtlasCloud Zoom Out": AtlasVideoEffectsZoomOut,

from atlascloud_comfyui.nodes.video.video_effects_shake_dance_i2v import AtlasVideoEffectsShakeDance
    "AtlasCloud Shake Dance": AtlasVideoEffectsShakeDance,

from atlascloud_comfyui.nodes.video.video_effects_love_drop_i2v import AtlasVideoEffectsLoveDrop
    "AtlasCloud Love Drop": AtlasVideoEffectsLoveDrop,

from atlascloud_comfyui.nodes.video.video_effects_jiggle_up_i2v import AtlasVideoEffectsJiggleUp
    "AtlasCloud Jiggle Up": AtlasVideoEffectsJiggleUp,

from atlascloud_comfyui.nodes.video.video_effects_hulk_i2v import AtlasVideoEffectsHulk
    "AtlasCloud Hulk": AtlasVideoEffectsHulk,

from atlascloud_comfyui.nodes.video.video_effects_gender_swap_i2v import AtlasVideoEffectsGenderSwap
    "AtlasCloud Gender Swap": AtlasVideoEffectsGenderSwap,

from atlascloud_comfyui.nodes.video.video_effects_flying_i2v import AtlasVideoEffectsFlying
    "AtlasCloud Flying": AtlasVideoEffectsFlying,

from atlascloud_comfyui.nodes.video.video_effects_fishermen_i2v import AtlasVideoEffectsFishermen
    "AtlasCloud Fishermen": AtlasVideoEffectsFishermen,

from atlascloud_comfyui.nodes.video.pixverse_pixverse_v4_5_t2v_t2v import AtlasPixversePixverseV45T2v
    "AtlasCloud Pixverse v4.5 t2v": AtlasPixversePixverseV45T2v,

from atlascloud_comfyui.nodes.video.pixverse_pixverse_v4_5_i2v_fast_i2v import AtlasPixversePixverseV45I2vFast
    "AtlasCloud Pixverse v4.5 i2v Fast": AtlasPixversePixverseV45I2vFast,

from atlascloud_comfyui.nodes.video.pika_v2_2_t2v_t2v import AtlasPikaV22T2v
    "AtlasCloud Pika v2.2 t2v": AtlasPikaV22T2v,

from atlascloud_comfyui.nodes.video.pika_v2_1_i2v_i2v import AtlasPikaV21I2v
    "AtlasCloud Pika v2.1 i2v": AtlasPikaV21I2v,

from atlascloud_comfyui.nodes.video.pika_v2_0_turbo_t2v_t2v import AtlasPikaV20TurboT2v
    "AtlasCloud Pika v2.0 Turbo t2v": AtlasPikaV20TurboT2v,

from atlascloud_comfyui.nodes.video.pika_v2_0_turbo_i2v_i2v import AtlasPikaV20TurboI2v
    "AtlasCloud Pika v2.0 Turbo i2v": AtlasPikaV20TurboI2v,

from atlascloud_comfyui.nodes.video.luma_ray_2_t2v_t2v import AtlasLumaRay2T2v
    "AtlasCloud Ray 2 t2v": AtlasLumaRay2T2v,

from atlascloud_comfyui.nodes.video.luma_ray_2_i2v_i2v import AtlasLumaRay2I2v
    "AtlasCloud Ray 2 i2v": AtlasLumaRay2I2v,

from atlascloud_comfyui.nodes.video.luma_ray_2_flash_t2v_t2v import AtlasLumaRay2FlashT2v
    "AtlasCloud Ray 2 Flash t2v": AtlasLumaRay2FlashT2v,

from atlascloud_comfyui.nodes.video.kwaivgi_kling_v2_0_i2v_master_i2v import AtlasKwaivgiKlingV20I2vMaster
    "AtlasCloud kling v2.0 i2v Master": AtlasKwaivgiKlingV20I2vMaster,

from atlascloud_comfyui.nodes.video.google_veo3_t2v import AtlasGoogleVeo3
    "AtlasCloud Veo3": AtlasGoogleVeo3,

from atlascloud_comfyui.nodes.video.google_veo3_image_to_video_i2v import AtlasGoogleVeo3ImageToVideo
    "AtlasCloud Veo3 Image-to-Video": AtlasGoogleVeo3ImageToVideo,

from atlascloud_comfyui.nodes.video.google_veo2_t2v import AtlasGoogleVeo2
    "AtlasCloud Veo2": AtlasGoogleVeo2,

from atlascloud_comfyui.nodes.video.google_veo2_image_to_video_i2v import AtlasGoogleVeo2ImageToVideo
    "AtlasCloud Veo2 Image-to-Video": AtlasGoogleVeo2ImageToVideo,

from atlascloud_comfyui.nodes.video.kwaivgi_kling_lipsync_text_to_video_t2v import AtlasKwaivgiKlingLipsyncTextToVideo
    "AtlasCloud Kling Lipsync Text-to-Video": AtlasKwaivgiKlingLipsyncTextToVideo,

from atlascloud_comfyui.nodes.video.minimax_hailuo_02_t2v_pro_i2v import AtlasMinimaxHailuo02T2vPro
    "AtlasCloud Hailuo-02 t2v Pro": AtlasMinimaxHailuo02T2vPro,

from atlascloud_comfyui.nodes.video.alibaba_wan_2_1_t2v_720p_ultra_fast_t2v import AtlasAlibabaWan21T2v720pUltraFast
    "AtlasCloud Wan-2.1 t2v 720p Ultra Fast": AtlasAlibabaWan21T2v720pUltraFast,

from atlascloud_comfyui.nodes.video.alibaba_wan_2_1_t2v_720p_lora_t2v import AtlasAlibabaWan21T2v720pLora
    "AtlasCloud Wan-2.1 t2v 720p Lora": AtlasAlibabaWan21T2v720pLora,

from atlascloud_comfyui.nodes.video.alibaba_wan_2_1_t2v_480p_ultra_fast_t2v import AtlasAlibabaWan21T2v480pUltraFast
    "AtlasCloud Wan-2.1 t2v 480p Ultra Fast": AtlasAlibabaWan21T2v480pUltraFast,

from atlascloud_comfyui.nodes.video.alibaba_wan_2_1_t2v_480p_lora_ultra_fast_t2v import AtlasAlibabaWan21T2v480pLoraUltraFast
    "AtlasCloud Wan-2.1 t2v 480p Lora Ultra Fast": AtlasAlibabaWan21T2v480pLoraUltraFast,

from atlascloud_comfyui.nodes.video.alibaba_wan_2_2_t2v_5b_720p_lora_t2v import AtlasAlibabaWan22T2v5b720pLora
    "AtlasCloud Wan-2.2 t2v 5b 720p Lora": AtlasAlibabaWan22T2v5b720pLora,

from atlascloud_comfyui.nodes.video.google_veo3_fast_image_to_video_i2v import AtlasGoogleVeo3FastImageToVideo
    "AtlasCloud Veo3 Fast Image-to-video": AtlasGoogleVeo3FastImageToVideo,

from atlascloud_comfyui.nodes.video.vidu_start_end_to_video_2_0_i2v import AtlasViduStartEndToVideo20
    "AtlasCloud Vidu Start-End-to-Video 2.0": AtlasViduStartEndToVideo20,

from atlascloud_comfyui.nodes.video.video_effects_sexy_me_i2v import AtlasVideoEffectsSexyMe
    "AtlasCloud Sexy Me": AtlasVideoEffectsSexyMe,

from atlascloud_comfyui.nodes.video.kwaivgi_kling_v2_1_t2v_master_t2v import AtlasKwaivgiKlingV21T2vMaster
    "AtlasCloud Kling v2.1 t2v Master": AtlasKwaivgiKlingV21T2vMaster,

from atlascloud_comfyui.nodes.video.kwaivgi_kling_v2_0_t2v_master_t2v import AtlasKwaivgiKlingV20T2vMaster
    "AtlasCloud Kling v2.0 t2v Master": AtlasKwaivgiKlingV20T2vMaster,

from atlascloud_comfyui.nodes.video.alibaba_wan_2_2_i2v_5b_720p_lora_i2v import AtlasAlibabaWan22I2v5b720pLora
    "AtlasCloud Wan-2.2 i2v 5b 720p Lora": AtlasAlibabaWan22I2v5b720pLora,

from atlascloud_comfyui.nodes.video.atlascloud_framepack_i2v import AtlasAtlascloudFramepack
    "AtlasCloud Framepack": AtlasAtlascloudFramepack,

from atlascloud_comfyui.nodes.video.video_effects_body_shake_i2v import AtlasVideoEffectsBodyShake
    "AtlasCloud Body Shake": AtlasVideoEffectsBodyShake,

from atlascloud_comfyui.nodes.video.bytedance_lipsync_audio_to_video_t2v import AtlasBytedanceLipsyncAudioToVideo
    "AtlasCloud Lipsync Audio-to-video": AtlasBytedanceLipsyncAudioToVideo,

from atlascloud_comfyui.nodes.video.alibaba_wan_2_2_t2v_480p_lora_ultra_fast_t2v import AtlasAlibabaWan22T2v480pLoraUltraFast
    "AtlasCloud Wan-2.2 t2v 480p Lora Ultra Fast": AtlasAlibabaWan22T2v480pLoraUltraFast,

from atlascloud_comfyui.nodes.video.alibaba_wan_2_1_t2v_720p_t2v import AtlasAlibabaWan21T2v720p
    "AtlasCloud Wan-2.1 t2v 720p": AtlasAlibabaWan21T2v720p,

from atlascloud_comfyui.nodes.video.atlascloud_multitalk_i2v import AtlasAtlascloudMultitalk
    "AtlasCloud Multitalk": AtlasAtlascloudMultitalk,

from atlascloud_comfyui.nodes.video.vidu_image_to_video_2_0_i2v import AtlasViduImageToVideo20
    "AtlasCloud Image-to-video-2.0": AtlasViduImageToVideo20,

from atlascloud_comfyui.nodes.video.video_effects_french_kiss_i2v import AtlasVideoEffectsFrenchKiss
    "AtlasCloud French Kiss": AtlasVideoEffectsFrenchKiss,

from atlascloud_comfyui.nodes.video.minimax_video_02_i2v import AtlasMinimaxVideo02
    "AtlasCloud Video-02": AtlasMinimaxVideo02,

from atlascloud_comfyui.nodes.video.minimax_video_01_i2v import AtlasMinimaxVideo01
    "AtlasCloud Video-01": AtlasMinimaxVideo01,

from atlascloud_comfyui.nodes.video.minimax_hailuo_02_fast_i2v import AtlasMinimaxHailuo02Fast
    "AtlasCloud Hailuo-02 Fast": AtlasMinimaxHailuo02Fast,

from atlascloud_comfyui.nodes.video.kwaivgi_kling_lipsync_audio_to_video_t2v import AtlasKwaivgiKlingLipsyncAudioToVideo
    "AtlasCloud Kling Lipsync audio-to-video": AtlasKwaivgiKlingLipsyncAudioToVideo,

from atlascloud_comfyui.nodes.video.bytedance_seedance_v1_lite_t2v_1080p_t2v import AtlasBytedanceSeedanceV1LiteT2v1080p
    "AtlasCloud Seedance v1 Lite t2v 1080p": AtlasBytedanceSeedanceV1LiteT2v1080p,

from atlascloud_comfyui.nodes.video.alibaba_wan_flf2v_i2v import AtlasAlibabaWanFlf2v
    "AtlasCloud Wan Flf2v": AtlasAlibabaWanFlf2v,

from atlascloud_comfyui.nodes.video.alibaba_wan_2_2_i2v_720p_ultra_fast_i2v import AtlasAlibabaWan22I2v720pUltraFast
    "AtlasCloud Wan-2.2 i2v 720p Ultra Fast": AtlasAlibabaWan22I2v720pUltraFast,

from atlascloud_comfyui.nodes.video.alibaba_wan_2_2_i2v_720p_lora_ultra_fast_i2v import AtlasAlibabaWan22I2v720pLoraUltraFast
    "AtlasCloud Wan-2.2 i2v 720p Lora Ultra Fast": AtlasAlibabaWan22I2v720pLoraUltraFast,

from atlascloud_comfyui.nodes.video.alibaba_wan_2_2_i2v_480p_ultra_fast_i2v import AtlasAlibabaWan22I2v480pUltraFast
    "AtlasCloud Wan-2.2 i2v 480p Ultra Fast": AtlasAlibabaWan22I2v480pUltraFast,

from atlascloud_comfyui.nodes.video.alibaba_wan_2_2_i2v_480p_lora_ultra_fast_i2v import AtlasAlibabaWan22I2v480pLoraUltraFast
    "AtlasCloud Wan-2.2 i2v 480p Lora Ultra Fast": AtlasAlibabaWan22I2v480pLoraUltraFast,

from atlascloud_comfyui.nodes.video.alibaba_wan_2_1_i2v_720p_ultra_fast_i2v import AtlasAlibabaWan21I2v720pUltraFast
    "AtlasCloud Wan-2.1 i2v 720p Ultra Fast": AtlasAlibabaWan21I2v720pUltraFast,

from atlascloud_comfyui.nodes.video.alibaba_wan_2_1_i2v_480p_ultra_fast_i2v import AtlasAlibabaWan21I2v480pUltraFast
    "AtlasCloud Wan-2.1 i2v 480p Ultra Fast": AtlasAlibabaWan21I2v480pUltraFast,

from atlascloud_comfyui.nodes.video.alibaba_wan_2_1_14b_vace_i2v import AtlasAlibabaWan2114bVace
    "AtlasCloud Wan-2.1 14b Vace": AtlasAlibabaWan2114bVace,

from atlascloud_comfyui.nodes.video.minimax_hailuo_02_pro_i2v import AtlasMinimaxHailuo02Pro
    "AtlasCloud Hailuo 02 Pro": AtlasMinimaxHailuo02Pro,

from atlascloud_comfyui.nodes.video.kwaivgi_kling_v2_1_i2v_master_i2v import AtlasKwaivgiKlingV21I2vMaster
    "AtlasCloud Kling v2.1 i2v Master": AtlasKwaivgiKlingV21I2vMaster,

from atlascloud_comfyui.nodes.video.bytedance_seedance_v1_lite_t2v_720p_t2v import AtlasBytedanceSeedanceV1LiteT2v720p
    "AtlasCloud Seedance v1 Lite t2v 720p": AtlasBytedanceSeedanceV1LiteT2v720p,

from atlascloud_comfyui.nodes.video.bytedance_seedance_v1_lite_i2v_1080p_i2v import AtlasBytedanceSeedanceV1LiteI2v1080p
    "AtlasCloud Seedance v1 Lite i2v 1080p": AtlasBytedanceSeedanceV1LiteI2v1080p,

from atlascloud_comfyui.nodes.video.bytedance_avatar_omni_human_i2v import AtlasBytedanceAvatarOmniHuman
    "AtlasCloud Avatar Omni Human": AtlasBytedanceAvatarOmniHuman,

from atlascloud_comfyui.nodes.video.alibaba_wan_2_2_spicy_image_to_video_lora_i2v import AtlasAlibabaWan22SpicyImageToVideoLora
    "AtlasCloud Wan-2.2-spicy Image-to-video Lora": AtlasAlibabaWan22SpicyImageToVideoLora,

from atlascloud_comfyui.nodes.video.alibaba_wan_2_2_spicy_image_to_video_i2v import AtlasAlibabaWan22SpicyImageToVideo
    "AtlasCloud Wan-2.2-spicy Image-to-video": AtlasAlibabaWan22SpicyImageToVideo,

from atlascloud_comfyui.nodes.video.alibaba_wan_2_2_t2v_480p_ultra_fast_t2v import AtlasAlibabaWan22T2v480pUltraFast
    "AtlasCloud Wan-2.2 t2v 480p Ultra Fast": AtlasAlibabaWan22T2v480pUltraFast,

from atlascloud_comfyui.nodes.video.alibaba_wan_2_2_t2v_5b_720p_t2v import AtlasAlibabaWan22T2v5b720p
    "AtlasCloud Wan-2.2 t2v 5b 720p": AtlasAlibabaWan22T2v5b720p,

from atlascloud_comfyui.nodes.video.alibaba_wan_2_2_i2v_5b_720p_i2v import AtlasAlibabaWan22I2v5b720p
    "AtlasCloud Wan-2.2 i2v 5b 720p": AtlasAlibabaWan22I2v5b720p,

from atlascloud_comfyui.nodes.video.atlascloud_hunyuan_video_i2v_i2v import AtlasAtlascloudHunyuanVideoI2v
    "AtlasCloud Hunyuan Video i2v": AtlasAtlascloudHunyuanVideoI2v,

from atlascloud_comfyui.nodes.video.pixverse_pixverse_v4_5_i2v_i2v import AtlasPixversePixverseV45I2v
    "AtlasCloud Pixverse v4.5 i2v": AtlasPixversePixverseV45I2v,

from atlascloud_comfyui.nodes.video.minimax_hailuo_02_t2v_standard_t2v import AtlasMinimaxHailuo02T2vStandard
    "AtlasCloud Hailuo 02 t2v Standard": AtlasMinimaxHailuo02T2vStandard,

from atlascloud_comfyui.nodes.video.minimax_hailuo_02_i2v_standard_i2v import AtlasMinimaxHailuo02I2vStandard
    "AtlasCloud Hailuo 02 i2v Standard": AtlasMinimaxHailuo02I2vStandard,

from atlascloud_comfyui.nodes.video.minimax_hailuo_02_i2v_pro_i2v import AtlasMinimaxHailuo02I2vPro
    "AtlasCloud Hailuo 02 i2v Pro": AtlasMinimaxHailuo02I2vPro,

from atlascloud_comfyui.nodes.video.kwaivgi_kling_v2_1_i2v_pro_i2v import AtlasKwaivgiKlingV21I2vPro
    "AtlasCloud Kling v2.1 i2v Pro": AtlasKwaivgiKlingV21I2vPro,

from atlascloud_comfyui.nodes.video.kwaivgi_kling_v1_6_t2v_standard_t2v import AtlasKwaivgiKlingV16T2vStandard
    "AtlasCloud Kling v1.6 t2v Standard": AtlasKwaivgiKlingV16T2vStandard,

from atlascloud_comfyui.nodes.video.kwaivgi_kling_v1_6_i2v_pro_i2v import AtlasKwaivgiKlingV16I2vPro
    "AtlasCloud Kling v1.6 i2v Pro": AtlasKwaivgiKlingV16I2vPro,

from atlascloud_comfyui.nodes.video.google_veo3_fast_t2v import AtlasGoogleVeo3Fast
    "AtlasCloud Veo3 Fast": AtlasGoogleVeo3Fast,

from atlascloud_comfyui.nodes.video.alibaba_wan_2_2_i2v_480p_i2v import AtlasAlibabaWan22I2v480p
    "AtlasCloud Wan-2.2 i2v 480p": AtlasAlibabaWan22I2v480p,

from atlascloud_comfyui.nodes.video.alibaba_wan_2_2_i2v_720p_i2v import AtlasAlibabaWan22I2v720p
    "AtlasCloud Wan-2.2 i2v 720p": AtlasAlibabaWan22I2v720p,

from atlascloud_comfyui.nodes.video.alibaba_wan_2_2_t2v_480p_t2v import AtlasAlibabaWan22T2v480p
    "AtlasCloud Wan-2.2 t2v 480p": AtlasAlibabaWan22T2v480p,

from atlascloud_comfyui.nodes.video.alibaba_wan_2_1_t2v_480p_lora_t2v import AtlasAlibabaWan21T2v480pLora
    "AtlasCloud Wan-2.1 t2v 480p lora": AtlasAlibabaWan21T2v480pLora,

from atlascloud_comfyui.nodes.video.alibaba_wan_2_1_i2v_720p_lora_ultra_fast_i2v import AtlasAlibabaWan21I2v720pLoraUltraFast
    "AtlasCloud Wan-2.1 i2v 720p Lora Ultra Fast": AtlasAlibabaWan21I2v720pLoraUltraFast,

from atlascloud_comfyui.nodes.video.alibaba_wan_2_1_i2v_720p_lora_i2v import AtlasAlibabaWan21I2v720pLora
    "AtlasCloud Wan-2.1 i2v 720p lora": AtlasAlibabaWan21I2v720pLora,

from atlascloud_comfyui.nodes.video.alibaba_wan_2_1_i2v_720p_i2v import AtlasAlibabaWan21I2v720p
    "AtlasCloud Wan-2.1 i2v 720p": AtlasAlibabaWan21I2v720p,

from atlascloud_comfyui.nodes.video.alibaba_wan_2_1_i2v_480p_lora_ultra_fast_i2v import AtlasAlibabaWan21I2v480pLoraUltraFast
    "AtlasCloud Wan-2.1 i2v 480p Lora Ultra Fast": AtlasAlibabaWan21I2v480pLoraUltraFast,

from atlascloud_comfyui.nodes.video.alibaba_wan_2_1_i2v_480p_lora_i2v import AtlasAlibabaWan21I2v480pLora
    "AtlasCloud Wan-2.1 i2v 480p lora": AtlasAlibabaWan21I2v480pLora,

from atlascloud_comfyui.nodes.video.alibaba_wan_2_1_i2v_480p_i2v import AtlasAlibabaWan21I2v480p
    "AtlasCloud Wan-2.1 i2v 480p": AtlasAlibabaWan21I2v480p,

from atlascloud_comfyui.nodes.video.bytedance_seedance_v1_pro_t2v_720p_t2v import AtlasBytedanceSeedanceV1ProT2v720p
    "AtlasCloud Seedance v1 Pro t2v 720p": AtlasBytedanceSeedanceV1ProT2v720p,

from atlascloud_comfyui.nodes.video.bytedance_seedance_v1_pro_t2v_480p_t2v import AtlasBytedanceSeedanceV1ProT2v480p
    "AtlasCloud Seedance v1 Pro t2v 480p": AtlasBytedanceSeedanceV1ProT2v480p,

from atlascloud_comfyui.nodes.video.bytedance_seedance_v1_pro_i2v_720p_i2v import AtlasBytedanceSeedanceV1ProI2v720p
    "AtlasCloud Seedance v1 Pro i2v 720p": AtlasBytedanceSeedanceV1ProI2v720p,

from atlascloud_comfyui.nodes.video.bytedance_seedance_v1_pro_i2v_480p_i2v import AtlasBytedanceSeedanceV1ProI2v480p
    "AtlasCloud Seedance v1 Pro i2v 480p": AtlasBytedanceSeedanceV1ProI2v480p,

from atlascloud_comfyui.nodes.video.bytedance_seedance_v1_pro_i2v_1080p_i2v import AtlasBytedanceSeedanceV1ProI2v1080p
    "AtlasCloud Seedance v1 Pro i2v 1080p": AtlasBytedanceSeedanceV1ProI2v1080p,

from atlascloud_comfyui.nodes.video.bytedance_seedance_v1_lite_t2v_480p_t2v import AtlasBytedanceSeedanceV1LiteT2v480p
    "AtlasCloud Seedance v1 Lite t2v 480p": AtlasBytedanceSeedanceV1LiteT2v480p,

from atlascloud_comfyui.nodes.video.bytedance_seedance_v1_lite_i2v_720p_i2v import AtlasBytedanceSeedanceV1LiteI2v720p
    "AtlasCloud Seedance v1 Lite i2v 720p": AtlasBytedanceSeedanceV1LiteI2v720p,

from atlascloud_comfyui.nodes.video.bytedance_seedance_v1_lite_i2v_480p_i2v import AtlasBytedanceSeedanceV1LiteI2v480p
    "AtlasCloud Seedance v1 Lite i2v 480p": AtlasBytedanceSeedanceV1LiteI2v480p,

from atlascloud_comfyui.nodes.video.kwaivgi_kling_v2_1_i2v_standard_i2v import AtlasKwaivgiKlingV21I2vStandard
    "AtlasCloud Kling v2.1 i2v Standard": AtlasKwaivgiKlingV21I2vStandard,

from atlascloud_comfyui.nodes.video.kwaivgi_kling_v1_6_i2v_standard_i2v import AtlasKwaivgiKlingV16I2vStandard
    "AtlasCloud Kling v1.6 i2v Standard": AtlasKwaivgiKlingV16I2vStandard,

from atlascloud_comfyui.nodes.video.minimax_hailuo_02_standard_i2v import AtlasMinimaxHailuo02Standard
    "AtlasCloud Hailuo 02 Standard": AtlasMinimaxHailuo02Standard,

from atlascloud_comfyui.nodes.image.atlascloud_hunyuan_image_3_t2i import AtlasAtlascloudHunyuanImage3
    "AtlasCloud Hunyuan Image 3": AtlasAtlascloudHunyuanImage3,

from atlascloud_comfyui.nodes.image.alibaba_wan_2_5_text_to_image_t2i import AtlasAlibabaWan25TextToImage
    "AtlasCloud Wan-2.5 Text-to-image": AtlasAlibabaWan25TextToImage,

from atlascloud_comfyui.nodes.image.bytedance_seedream_v4_t2i import AtlasBytedanceSeedreamV4
    "AtlasCloud Seedream v4": AtlasBytedanceSeedreamV4,

from atlascloud_comfyui.nodes.image.bytedance_seedream_v4_sequential_t2i import AtlasBytedanceSeedreamV4Sequential
    "AtlasCloud Seedream v4 Sequential": AtlasBytedanceSeedreamV4Sequential,

from atlascloud_comfyui.nodes.image.google_nano_banana_pro_text_to_image_developer_t2i import AtlasGoogleNanoBananaProTextToImageDeveloper
    "AtlasCloud Nano Banana Pro Text-to-image Developer": AtlasGoogleNanoBananaProTextToImageDeveloper,

from atlascloud_comfyui.nodes.image.google_nano_banana_text_to_image_developer_t2i import AtlasGoogleNanoBananaTextToImageDeveloper
    "AtlasCloud Nano Banana Text-to-image Developer": AtlasGoogleNanoBananaTextToImageDeveloper,

from atlascloud_comfyui.nodes.video.atlascloud_van_2_5_image_to_video_i2v import AtlasAtlascloudVan25ImageToVideo
    "AtlasCloud Van-2.5 Image-to-video": AtlasAtlascloudVan25ImageToVideo,

from atlascloud_comfyui.nodes.video.alibaba_wan_2_2_animate_mix_i2v import AtlasAlibabaWan22AnimateMix
    "AtlasCloud Wan-2.2 Video Character Swap": AtlasAlibabaWan22AnimateMix,

from atlascloud_comfyui.nodes.video.alibaba_wan_2_2_animate_move_i2v import AtlasAlibabaWan22AnimateMove
    "AtlasCloud Wan-2.2 Image To Animation": AtlasAlibabaWan22AnimateMove,

from atlascloud_comfyui.nodes.image.alibaba_wan_2_6_text_to_image_t2i import AtlasAlibabaWan26TextToImage
    "AtlasCloud Wan-2.6 Text-to-image": AtlasAlibabaWan26TextToImage,

from atlascloud_comfyui.nodes.video.atlascloud_van_2_5_text_to_video_t2v import AtlasAtlascloudVan25TextToVideo
    "AtlasCloud Van-2.5 Text-to-video": AtlasAtlascloudVan25TextToVideo,

from atlascloud_comfyui.nodes.image.google_nano_banana_text_to_image_t2i import AtlasGoogleNanoBananaTextToImage
    "AtlasCloud Nano Banana Text-to-image": AtlasGoogleNanoBananaTextToImage,

from atlascloud_comfyui.nodes.image.bytedance_seedream_v3_1_t2i import AtlasBytedanceSeedreamV31
    "AtlasCloud Seedream v3.1": AtlasBytedanceSeedreamV31,

from atlascloud_comfyui.nodes.image.atlascloud_neta_lumina_t2i import AtlasAtlascloudNetaLumina
    "AtlasCloud Neta Lumina": AtlasAtlascloudNetaLumina,

from atlascloud_comfyui.nodes.image.recraft_ai_recraft_v3_svg_t2i import AtlasRecraftAiRecraftV3Svg
    "AtlasCloud Recraft v3 Svg": AtlasRecraftAiRecraftV3Svg,

from atlascloud_comfyui.nodes.image.recraft_ai_recraft_20b_t2i import AtlasRecraftAiRecraft20b
    "AtlasCloud Recraft 20b": AtlasRecraftAiRecraft20b,

from atlascloud_comfyui.nodes.image.recraft_ai_recraft_20b_svg_t2i import AtlasRecraftAiRecraft20bSvg
    "AtlasCloud Recraft 20b Svg": AtlasRecraftAiRecraft20bSvg,

from atlascloud_comfyui.nodes.image.ideogram_ai_ideogram_v2a_turbo_t2i import AtlasIdeogramAiIdeogramV2aTurbo
    "AtlasCloud Ideogram v2a Turbo": AtlasIdeogramAiIdeogramV2aTurbo,

from atlascloud_comfyui.nodes.image.ideogram_ai_ideogram_v2_t2i import AtlasIdeogramAiIdeogramV2
    "AtlasCloud Ideogram v2": AtlasIdeogramAiIdeogramV2,

from atlascloud_comfyui.nodes.image.ideogram_ai_ideogram_v2_turbo_t2i import AtlasIdeogramAiIdeogramV2Turbo
    "AtlasCloud Ideogram v2 Turbo": AtlasIdeogramAiIdeogramV2Turbo,

from atlascloud_comfyui.nodes.image.luma_photon_t2i import AtlasLumaPhoton
    "AtlasCloud Photon": AtlasLumaPhoton,

from atlascloud_comfyui.nodes.image.google_imagen3_t2i import AtlasGoogleImagen3
    "AtlasCloud Imagen3": AtlasGoogleImagen3,

from atlascloud_comfyui.nodes.image.luma_photon_flash_t2i import AtlasLumaPhotonFlash
    "AtlasCloud Photon Flash": AtlasLumaPhotonFlash,

from atlascloud_comfyui.nodes.image.ideogram_ai_ideogram_v3_balanced_t2i import AtlasIdeogramAiIdeogramV3Balanced
    "AtlasCloud Ideogram v3 Balanced": AtlasIdeogramAiIdeogramV3Balanced,

from atlascloud_comfyui.nodes.image.google_imagen3_fast_t2i import AtlasGoogleImagen3Fast
    "AtlasCloud Image3 Fast": AtlasGoogleImagen3Fast,

from atlascloud_comfyui.nodes.image.atlascloud_qwen_image_text_to_image_t2i import AtlasAtlascloudQwenImageTextToImage
    "AtlasCloud Qwen Image Text-to-image": AtlasAtlascloudQwenImageTextToImage,

from atlascloud_comfyui.nodes.image.atlascloud_imagen4_t2i import AtlasAtlascloudImagen4
    "AtlasCloud Imagen4": AtlasAtlascloudImagen4,

from atlascloud_comfyui.nodes.image.black_forest_labs_flux_1_1_pro_t2i import AtlasBlackForestLabsFlux11Pro
    "AtlasCloud Flux 1.1 Pro": AtlasBlackForestLabsFlux11Pro,

from atlascloud_comfyui.nodes.image.black_forest_labs_flux_1_1_pro_ultra_t2i import AtlasBlackForestLabsFlux11ProUltra
    "AtlasCloud Flux 1.1 Pro Ultra": AtlasBlackForestLabsFlux11ProUltra,

from atlascloud_comfyui.nodes.image.recraft_ai_recraft_v3_t2i import AtlasRecraftAiRecraftV3
    "AtlasCloud Recraft v3": AtlasRecraftAiRecraftV3,

from atlascloud_comfyui.nodes.image.ideogram_ai_ideogram_v3_turbo_t2i import AtlasIdeogramAiIdeogramV3Turbo
    "AtlasCloud Ideogram v3 Turbo": AtlasIdeogramAiIdeogramV3Turbo,

from atlascloud_comfyui.nodes.image.google_imagen4_fast_t2i import AtlasGoogleImagen4Fast
    "AtlasCloud Imagen4 Fast": AtlasGoogleImagen4Fast,

from atlascloud_comfyui.nodes.image.black_forest_labs_flux_dev_t2i import AtlasBlackForestLabsFluxDev
    "AtlasCloud Flux Dev": AtlasBlackForestLabsFluxDev,

from atlascloud_comfyui.nodes.image.black_forest_labs_flux_dev_lora_ultra_fast_t2i import AtlasBlackForestLabsFluxDevLoraUltraFast
    "AtlasCloud Flux Dev Lora Ultra Fast": AtlasBlackForestLabsFluxDevLoraUltraFast,

from atlascloud_comfyui.nodes.image.black_forest_labs_flux_dev_lora_t2i import AtlasBlackForestLabsFluxDevLora
    "AtlasCloud Flux Dev Lora": AtlasBlackForestLabsFluxDevLora,

from atlascloud_comfyui.nodes.image.black_forest_labs_flux_dev_ultra_fast_t2i import AtlasBlackForestLabsFluxDevUltraFast
    "AtlasCloud Flux Dev Ultra Fast": AtlasBlackForestLabsFluxDevUltraFast,

from atlascloud_comfyui.nodes.image.ideogram_ai_ideogram_v3_quality_t2i import AtlasIdeogramAiIdeogramV3Quality
    "AtlasCloud Ideogram v3 Quality": AtlasIdeogramAiIdeogramV3Quality,

from atlascloud_comfyui.nodes.image.google_imagen4_ultra_t2i import AtlasGoogleImagen4Ultra
    "AtlasCloud Imagen4 Ultra": AtlasGoogleImagen4Ultra,

from atlascloud_comfyui.nodes.image.google_imagen4_t2i import AtlasGoogleImagen4
    "AtlasCloud Imagen4": AtlasGoogleImagen4,

from atlascloud_comfyui.nodes.image.black_forest_labs_flux_kontext_pro_text_to_image_t2i import AtlasBlackForestLabsFluxKontextProTextToImage
    "AtlasCloud Flux Kontext Pro Text-to-Image": AtlasBlackForestLabsFluxKontextProTextToImage,

from atlascloud_comfyui.nodes.image.black_forest_labs_flux_kontext_max_text_to_image_t2i import AtlasBlackForestLabsFluxKontextMaxTextToImage
    "AtlasCloud Flux Kontext Max Text-to-Image": AtlasBlackForestLabsFluxKontextMaxTextToImage,

from atlascloud_comfyui.nodes.image.atlascloud_hidream_i1_full_t2i import AtlasAtlascloudHidreamI1Full
    "AtlasCloud Hidream i1 Full": AtlasAtlascloudHidreamI1Full,

from atlascloud_comfyui.nodes.image.atlascloud_hidream_i1_dev_t2i import AtlasAtlascloudHidreamI1Dev
    "AtlasCloud Hidream i1 Dev": AtlasAtlascloudHidreamI1Dev,

from atlascloud_comfyui.nodes.image.black_forest_labs_flux_schnell_lora_t2i import AtlasBlackForestLabsFluxSchnellLora
    "AtlasCloud Flux Schnell Lora": AtlasBlackForestLabsFluxSchnellLora,

from atlascloud_comfyui.nodes.image.alibaba_wan_2_1_text_to_image_t2i import AtlasAlibabaWan21TextToImage
    "AtlasCloud Wan-2.1 Text-to-Image": AtlasAlibabaWan21TextToImage,

from atlascloud_comfyui.nodes.image.black_forest_labs_flux_schnell_t2i import AtlasBlackForestLabsFluxSchnell
    "AtlasCloud Flux Schnell": AtlasBlackForestLabsFluxSchnell,

from atlascloud_comfyui.nodes.image.bytedance_seedream_v3_t2i import AtlasBytedanceSeedreamV3
    "AtlasCloud Seedream V3": AtlasBytedanceSeedreamV3,

NODE_CLASS_MAPPINGS["Example"] = LegacyExample    "AtlasCloud Nano Banana 2 Text-to-Image Developer": "AtlasCloud Nano Banana 2 Text-to-Image Developer",
    "AtlasCloud Nano Banana 2 Text-to-Image": "AtlasCloud Nano Banana 2 Text-to-Image",
    "AtlasCloud Seedream v5.0 Lite Sequential": "AtlasCloud Seedream v5.0 Lite Sequential",
    "AtlasCloud Seedream v5.0 Lite": "AtlasCloud Seedream v5.0 Lite",
    "AtlasCloud Vidu Q3 Image-to-video": "AtlasCloud Vidu Q3 Image-to-video",
    "AtlasCloud Vidu Q3 Text-to-video": "AtlasCloud Vidu Q3 Text-to-video",
    "AtlasCloud Kling v2.6 Pro Avatar": "AtlasCloud Kling v2.6 Pro Avatar",
    "AtlasCloud Kling v2.6 Std Avatar": "AtlasCloud Kling v2.6 Std Avatar",
    "AtlasCloud Kling v2.6 Pro Motion Control": "AtlasCloud Kling v2.6 Pro Motion Control",
    "AtlasCloud Kling v2.6 Std Motion Control": "AtlasCloud Kling v2.6 Std Motion Control",
    "AtlasCloud Wan-2.6 Image-to-video Flash": "AtlasCloud Wan-2.6 Image-to-video Flash",
    "AtlasCloud Seedance v1.5 Pro Image-to-Video": "AtlasCloud Seedance v1.5 Pro Image-to-Video",
    "AtlasCloud Seedance v1.5 Pro Image-to-Video Fast": "AtlasCloud Seedance v1.5 Pro Image-to-Video Fast",
    "AtlasCloud Wan-2.6 Image-to-video": "AtlasCloud Wan-2.6 Image-to-video",
    "AtlasCloud Z-Image Turbo": "AtlasCloud Z-Image Turbo",
    "AtlasCloud Kling Video O3 Pro Reference-to-Video": "AtlasCloud Kling Video O3 Pro Reference-to-Video",
    "AtlasCloud Kling Video O3 Pro Image-to-Video": "AtlasCloud Kling Video O3 Pro Image-to-Video",
    "AtlasCloud Kling Video O3 Pro Text-to-Video": "AtlasCloud Kling Video O3 Pro Text-to-Video",
    "AtlasCloud Seedance v1.5 Pro Text-to-Video Fast": "AtlasCloud Seedance v1.5 Pro Text-to-Video Fast",
    "AtlasCloud Kling v2.6 Pro Image-to-Video": "AtlasCloud Kling v2.6 Pro Image-to-Video",
    "AtlasCloud Kling Video O3 Std Reference-to-Video": "AtlasCloud Kling Video O3 Std Reference-to-Video",
    "AtlasCloud Kling Video O3 Std Image-to-Video": "AtlasCloud Kling Video O3 Std Image-to-Video",
    "AtlasCloud Kling Video O3 Std Text-to-Video": "AtlasCloud Kling Video O3 Std Text-to-Video",
    "AtlasCloud Seedream v4.5 Sequential": "AtlasCloud Seedream v4.5 Sequential",
    "AtlasCloud Kling Video O1 Image-to-video": "AtlasCloud Kling Video O1 Image-to-video",
    "AtlasCloud Nano Banana Pro Text-to-image": "AtlasCloud Nano Banana Pro Text-to-image",
    "AtlasCloud Qwen-Image Text-to-image Max": "AtlasCloud Qwen-Image Text-to-image Max",
    "AtlasCloud Qwen-Image Text-to-image Plus": "AtlasCloud Qwen-Image Text-to-image Plus",
    "AtlasCloud Ltx-2 Fast Image-to-video": "AtlasCloud Ltx-2 Fast Image-to-video",
    "AtlasCloud Ltx-2 Fast Text-to-video": "AtlasCloud Ltx-2 Fast Text-to-video",
    "AtlasCloud Ltx-2 Pro Image-to-video": "AtlasCloud Ltx-2 Pro Image-to-video",
    "AtlasCloud Ltx-2 Pro Text-to-video": "AtlasCloud Ltx-2 Pro Text-to-video",
    "AtlasCloud Wan-2.5 Video Extend Fast": "AtlasCloud Wan-2.5 Video Extend Fast",
    "AtlasCloud Wan-2.5 Video Extend": "AtlasCloud Wan-2.5 Video Extend",
    "AtlasCloud Hailuo-2.3 t2v Standard": "AtlasCloud Hailuo-2.3 t2v Standard",
    "AtlasCloud Hailuo-2.3 i2v Standard": "AtlasCloud Hailuo-2.3 i2v Standard",
    "AtlasCloud Hailuo-2.3 i2v Pro": "AtlasCloud Hailuo-2.3 i2v Pro",
    "AtlasCloud Hailuo-2.3 Fast": "AtlasCloud Hailuo-2.3 Fast",
    "AtlasCloud Seedance v1 Pro Fast Text-to-video": "AtlasCloud Seedance v1 Pro Fast Text-to-video",
    "AtlasCloud Seedance v1 Pro Fast Image-to-video": "AtlasCloud Seedance v1 Pro Fast Image-to-video",
    "AtlasCloud Veo3.1 Reference-to-video": "AtlasCloud Veo3.1 Reference-to-video",
    "AtlasCloud Veo3.1 Image-to-video": "AtlasCloud Veo3.1 Image-to-video",
    "AtlasCloud Veo3.1 Fast Text-to-video": "AtlasCloud Veo3.1 Fast Text-to-video",
    "AtlasCloud Veo3.1 Fast Image-to-video": "AtlasCloud Veo3.1 Fast Image-to-video",
    "AtlasCloud Kling v2.5 Turbo Pro Text-to-video": "AtlasCloud Kling v2.5 Turbo Pro Text-to-video",
    "AtlasCloud Kling v2.5 Turbo Pro Image-to-video": "AtlasCloud Kling v2.5 Turbo Pro Image-to-video",
    "AtlasCloud Kling v2.1 i2v Pro Start-end-frame": "AtlasCloud Kling v2.1 i2v Pro Start-end-frame",
    "AtlasCloud Kling v1.6 Multi i2v Pro": "AtlasCloud Kling v1.6 Multi i2v Pro",
    "AtlasCloud Kling v1.6 Multi i2v Standard": "AtlasCloud Kling v1.6 Multi i2v Standard",
    "AtlasCloud Kling Effects": "AtlasCloud Kling Effects",
    "AtlasCloud Sora": "AtlasCloud Sora",
    "AtlasCloud Van-2.6 Text-to-video": "AtlasCloud Van-2.6 Text-to-video",
    "AtlasCloud Wan-2.5 Text-to-video Fast": "AtlasCloud Wan-2.5 Text-to-video Fast",
    "AtlasCloud Wan-2.5 Image-to-video": "AtlasCloud Wan-2.5 Image-to-video",
    "AtlasCloud Van-2.6 Image-to-video": "AtlasCloud Van-2.6 Image-to-video",
    "AtlasCloud Wan-2.5 Image-to-video Fast": "AtlasCloud Wan-2.5 Image-to-video Fast",
    "AtlasCloud Ltx-Video v097 i2v 720p": "AtlasCloud Ltx-Video v097 i2v 720p",
    "AtlasCloud Wan-2.1 t2v 720p Lora Ultra Fast": "AtlasCloud Wan-2.1 t2v 720p Lora Ultra Fast",
    "AtlasCloud Magi-1 24b": "AtlasCloud Magi-1 24b",
    "AtlasCloud Hunyuan Video t2v": "AtlasCloud Hunyuan Video t2v",
    "AtlasCloud Vidu Reference-to-Video Q1": "AtlasCloud Vidu Reference-to-Video Q1",
    "AtlasCloud Vidu Reference-to-Video 2.0": "AtlasCloud Vidu Reference-to-Video 2.0",
    "AtlasCloud Zoom Out": "AtlasCloud Zoom Out",
    "AtlasCloud Shake Dance": "AtlasCloud Shake Dance",
    "AtlasCloud Love Drop": "AtlasCloud Love Drop",
    "AtlasCloud Jiggle Up": "AtlasCloud Jiggle Up",
    "AtlasCloud Hulk": "AtlasCloud Hulk",
    "AtlasCloud Gender Swap": "AtlasCloud Gender Swap",
    "AtlasCloud Flying": "AtlasCloud Flying",
    "AtlasCloud Fishermen": "AtlasCloud Fishermen",
    "AtlasCloud Pixverse v4.5 t2v": "AtlasCloud Pixverse v4.5 t2v",
    "AtlasCloud Pixverse v4.5 i2v Fast": "AtlasCloud Pixverse v4.5 i2v Fast",
    "AtlasCloud Pika v2.2 t2v": "AtlasCloud Pika v2.2 t2v",
    "AtlasCloud Pika v2.1 i2v": "AtlasCloud Pika v2.1 i2v",
    "AtlasCloud Pika v2.0 Turbo t2v": "AtlasCloud Pika v2.0 Turbo t2v",
    "AtlasCloud Pika v2.0 Turbo i2v": "AtlasCloud Pika v2.0 Turbo i2v",
    "AtlasCloud Ray 2 t2v": "AtlasCloud Ray 2 t2v",
    "AtlasCloud Ray 2 i2v": "AtlasCloud Ray 2 i2v",
    "AtlasCloud Ray 2 Flash t2v": "AtlasCloud Ray 2 Flash t2v",
    "AtlasCloud kling v2.0 i2v Master": "AtlasCloud kling v2.0 i2v Master",
    "AtlasCloud Veo3": "AtlasCloud Veo3",
    "AtlasCloud Veo3 Image-to-Video": "AtlasCloud Veo3 Image-to-Video",
    "AtlasCloud Veo2": "AtlasCloud Veo2",
    "AtlasCloud Veo2 Image-to-Video": "AtlasCloud Veo2 Image-to-Video",
    "AtlasCloud Kling Lipsync Text-to-Video": "AtlasCloud Kling Lipsync Text-to-Video",
    "AtlasCloud Hailuo-02 t2v Pro": "AtlasCloud Hailuo-02 t2v Pro",
    "AtlasCloud Wan-2.1 t2v 720p Ultra Fast": "AtlasCloud Wan-2.1 t2v 720p Ultra Fast",
    "AtlasCloud Wan-2.1 t2v 720p Lora": "AtlasCloud Wan-2.1 t2v 720p Lora",
    "AtlasCloud Wan-2.1 t2v 480p Ultra Fast": "AtlasCloud Wan-2.1 t2v 480p Ultra Fast",
    "AtlasCloud Wan-2.1 t2v 480p Lora Ultra Fast": "AtlasCloud Wan-2.1 t2v 480p Lora Ultra Fast",
    "AtlasCloud Wan-2.2 t2v 5b 720p Lora": "AtlasCloud Wan-2.2 t2v 5b 720p Lora",
    "AtlasCloud Veo3 Fast Image-to-video": "AtlasCloud Veo3 Fast Image-to-video",
    "AtlasCloud Vidu Start-End-to-Video 2.0": "AtlasCloud Vidu Start-End-to-Video 2.0",
    "AtlasCloud Sexy Me": "AtlasCloud Sexy Me",
    "AtlasCloud Kling v2.1 t2v Master": "AtlasCloud Kling v2.1 t2v Master",
    "AtlasCloud Kling v2.0 t2v Master": "AtlasCloud Kling v2.0 t2v Master",
    "AtlasCloud Wan-2.2 i2v 5b 720p Lora": "AtlasCloud Wan-2.2 i2v 5b 720p Lora",
    "AtlasCloud Framepack": "AtlasCloud Framepack",
    "AtlasCloud Body Shake": "AtlasCloud Body Shake",
    "AtlasCloud Lipsync Audio-to-video": "AtlasCloud Lipsync Audio-to-video",
    "AtlasCloud Wan-2.2 t2v 480p Lora Ultra Fast": "AtlasCloud Wan-2.2 t2v 480p Lora Ultra Fast",
    "AtlasCloud Wan-2.1 t2v 720p": "AtlasCloud Wan-2.1 t2v 720p",
    "AtlasCloud Multitalk": "AtlasCloud Multitalk",
    "AtlasCloud Image-to-video-2.0": "AtlasCloud Image-to-video-2.0",
    "AtlasCloud French Kiss": "AtlasCloud French Kiss",
    "AtlasCloud Video-02": "AtlasCloud Video-02",
    "AtlasCloud Video-01": "AtlasCloud Video-01",
    "AtlasCloud Hailuo-02 Fast": "AtlasCloud Hailuo-02 Fast",
    "AtlasCloud Kling Lipsync audio-to-video": "AtlasCloud Kling Lipsync audio-to-video",
    "AtlasCloud Seedance v1 Lite t2v 1080p": "AtlasCloud Seedance v1 Lite t2v 1080p",
    "AtlasCloud Wan Flf2v": "AtlasCloud Wan Flf2v",
    "AtlasCloud Wan-2.2 i2v 720p Ultra Fast": "AtlasCloud Wan-2.2 i2v 720p Ultra Fast",
    "AtlasCloud Wan-2.2 i2v 720p Lora Ultra Fast": "AtlasCloud Wan-2.2 i2v 720p Lora Ultra Fast",
    "AtlasCloud Wan-2.2 i2v 480p Ultra Fast": "AtlasCloud Wan-2.2 i2v 480p Ultra Fast",
    "AtlasCloud Wan-2.2 i2v 480p Lora Ultra Fast": "AtlasCloud Wan-2.2 i2v 480p Lora Ultra Fast",
    "AtlasCloud Wan-2.1 i2v 720p Ultra Fast": "AtlasCloud Wan-2.1 i2v 720p Ultra Fast",
    "AtlasCloud Wan-2.1 i2v 480p Ultra Fast": "AtlasCloud Wan-2.1 i2v 480p Ultra Fast",
    "AtlasCloud Wan-2.1 14b Vace": "AtlasCloud Wan-2.1 14b Vace",
    "AtlasCloud Hailuo 02 Pro": "AtlasCloud Hailuo 02 Pro",
    "AtlasCloud Kling v2.1 i2v Master": "AtlasCloud Kling v2.1 i2v Master",
    "AtlasCloud Seedance v1 Lite t2v 720p": "AtlasCloud Seedance v1 Lite t2v 720p",
    "AtlasCloud Seedance v1 Lite i2v 1080p": "AtlasCloud Seedance v1 Lite i2v 1080p",
    "AtlasCloud Avatar Omni Human": "AtlasCloud Avatar Omni Human",
    "AtlasCloud Wan-2.2-spicy Image-to-video Lora": "AtlasCloud Wan-2.2-spicy Image-to-video Lora",
    "AtlasCloud Wan-2.2-spicy Image-to-video": "AtlasCloud Wan-2.2-spicy Image-to-video",
    "AtlasCloud Wan-2.2 t2v 480p Ultra Fast": "AtlasCloud Wan-2.2 t2v 480p Ultra Fast",
    "AtlasCloud Wan-2.2 t2v 5b 720p": "AtlasCloud Wan-2.2 t2v 5b 720p",
    "AtlasCloud Wan-2.2 i2v 5b 720p": "AtlasCloud Wan-2.2 i2v 5b 720p",
    "AtlasCloud Hunyuan Video i2v": "AtlasCloud Hunyuan Video i2v",
    "AtlasCloud Pixverse v4.5 i2v": "AtlasCloud Pixverse v4.5 i2v",
    "AtlasCloud Hailuo 02 t2v Standard": "AtlasCloud Hailuo 02 t2v Standard",
    "AtlasCloud Hailuo 02 i2v Standard": "AtlasCloud Hailuo 02 i2v Standard",
    "AtlasCloud Hailuo 02 i2v Pro": "AtlasCloud Hailuo 02 i2v Pro",
    "AtlasCloud Kling v2.1 i2v Pro": "AtlasCloud Kling v2.1 i2v Pro",
    "AtlasCloud Kling v1.6 t2v Standard": "AtlasCloud Kling v1.6 t2v Standard",
    "AtlasCloud Kling v1.6 i2v Pro": "AtlasCloud Kling v1.6 i2v Pro",
    "AtlasCloud Veo3 Fast": "AtlasCloud Veo3 Fast",
    "AtlasCloud Wan-2.2 i2v 480p": "AtlasCloud Wan-2.2 i2v 480p",
    "AtlasCloud Wan-2.2 i2v 720p": "AtlasCloud Wan-2.2 i2v 720p",
    "AtlasCloud Wan-2.2 t2v 480p": "AtlasCloud Wan-2.2 t2v 480p",
    "AtlasCloud Wan-2.1 t2v 480p lora": "AtlasCloud Wan-2.1 t2v 480p lora",
    "AtlasCloud Wan-2.1 i2v 720p Lora Ultra Fast": "AtlasCloud Wan-2.1 i2v 720p Lora Ultra Fast",
    "AtlasCloud Wan-2.1 i2v 720p lora": "AtlasCloud Wan-2.1 i2v 720p lora",
    "AtlasCloud Wan-2.1 i2v 720p": "AtlasCloud Wan-2.1 i2v 720p",
    "AtlasCloud Wan-2.1 i2v 480p Lora Ultra Fast": "AtlasCloud Wan-2.1 i2v 480p Lora Ultra Fast",
    "AtlasCloud Wan-2.1 i2v 480p lora": "AtlasCloud Wan-2.1 i2v 480p lora",
    "AtlasCloud Wan-2.1 i2v 480p": "AtlasCloud Wan-2.1 i2v 480p",
    "AtlasCloud Seedance v1 Pro t2v 720p": "AtlasCloud Seedance v1 Pro t2v 720p",
    "AtlasCloud Seedance v1 Pro t2v 480p": "AtlasCloud Seedance v1 Pro t2v 480p",
    "AtlasCloud Seedance v1 Pro i2v 720p": "AtlasCloud Seedance v1 Pro i2v 720p",
    "AtlasCloud Seedance v1 Pro i2v 480p": "AtlasCloud Seedance v1 Pro i2v 480p",
    "AtlasCloud Seedance v1 Pro i2v 1080p": "AtlasCloud Seedance v1 Pro i2v 1080p",
    "AtlasCloud Seedance v1 Lite t2v 480p": "AtlasCloud Seedance v1 Lite t2v 480p",
    "AtlasCloud Seedance v1 Lite i2v 720p": "AtlasCloud Seedance v1 Lite i2v 720p",
    "AtlasCloud Seedance v1 Lite i2v 480p": "AtlasCloud Seedance v1 Lite i2v 480p",
    "AtlasCloud Kling v2.1 i2v Standard": "AtlasCloud Kling v2.1 i2v Standard",
    "AtlasCloud Kling v1.6 i2v Standard": "AtlasCloud Kling v1.6 i2v Standard",
    "AtlasCloud Hailuo 02 Standard": "AtlasCloud Hailuo 02 Standard",
    "AtlasCloud Hunyuan Image 3": "AtlasCloud Hunyuan Image 3",
    "AtlasCloud Wan-2.5 Text-to-image": "AtlasCloud Wan-2.5 Text-to-image",
    "AtlasCloud Seedream v4": "AtlasCloud Seedream v4",
    "AtlasCloud Seedream v4 Sequential": "AtlasCloud Seedream v4 Sequential",
    "AtlasCloud Nano Banana Pro Text-to-image Developer": "AtlasCloud Nano Banana Pro Text-to-image Developer",
    "AtlasCloud Nano Banana Text-to-image Developer": "AtlasCloud Nano Banana Text-to-image Developer",
    "AtlasCloud Van-2.5 Image-to-video": "AtlasCloud Van-2.5 Image-to-video",
    "AtlasCloud Wan-2.2 Video Character Swap": "AtlasCloud Wan-2.2 Video Character Swap",
    "AtlasCloud Wan-2.2 Image To Animation": "AtlasCloud Wan-2.2 Image To Animation",
    "AtlasCloud Wan-2.6 Text-to-image": "AtlasCloud Wan-2.6 Text-to-image",
    "AtlasCloud Van-2.5 Text-to-video": "AtlasCloud Van-2.5 Text-to-video",
    "AtlasCloud Nano Banana Text-to-image": "AtlasCloud Nano Banana Text-to-image",
    "AtlasCloud Seedream v3.1": "AtlasCloud Seedream v3.1",
    "AtlasCloud Neta Lumina": "AtlasCloud Neta Lumina",
    "AtlasCloud Recraft v3 Svg": "AtlasCloud Recraft v3 Svg",
    "AtlasCloud Recraft 20b": "AtlasCloud Recraft 20b",
    "AtlasCloud Recraft 20b Svg": "AtlasCloud Recraft 20b Svg",
    "AtlasCloud Ideogram v2a Turbo": "AtlasCloud Ideogram v2a Turbo",
    "AtlasCloud Ideogram v2": "AtlasCloud Ideogram v2",
    "AtlasCloud Ideogram v2 Turbo": "AtlasCloud Ideogram v2 Turbo",
    "AtlasCloud Photon": "AtlasCloud Photon",
    "AtlasCloud Imagen3": "AtlasCloud Imagen3",
    "AtlasCloud Photon Flash": "AtlasCloud Photon Flash",
    "AtlasCloud Ideogram v3 Balanced": "AtlasCloud Ideogram v3 Balanced",
    "AtlasCloud Image3 Fast": "AtlasCloud Image3 Fast",
    "AtlasCloud Qwen Image Text-to-image": "AtlasCloud Qwen Image Text-to-image",
    "AtlasCloud Imagen4": "AtlasCloud Imagen4",
    "AtlasCloud Flux 1.1 Pro": "AtlasCloud Flux 1.1 Pro",
    "AtlasCloud Flux 1.1 Pro Ultra": "AtlasCloud Flux 1.1 Pro Ultra",
    "AtlasCloud Recraft v3": "AtlasCloud Recraft v3",
    "AtlasCloud Ideogram v3 Turbo": "AtlasCloud Ideogram v3 Turbo",
    "AtlasCloud Imagen4 Fast": "AtlasCloud Imagen4 Fast",
    "AtlasCloud Flux Dev": "AtlasCloud Flux Dev",
    "AtlasCloud Flux Dev Lora Ultra Fast": "AtlasCloud Flux Dev Lora Ultra Fast",
    "AtlasCloud Flux Dev Lora": "AtlasCloud Flux Dev Lora",
    "AtlasCloud Flux Dev Ultra Fast": "AtlasCloud Flux Dev Ultra Fast",
    "AtlasCloud Ideogram v3 Quality": "AtlasCloud Ideogram v3 Quality",
    "AtlasCloud Imagen4 Ultra": "AtlasCloud Imagen4 Ultra",
    "AtlasCloud Flux Kontext Pro Text-to-Image": "AtlasCloud Flux Kontext Pro Text-to-Image",
    "AtlasCloud Flux Kontext Max Text-to-Image": "AtlasCloud Flux Kontext Max Text-to-Image",
    "AtlasCloud Hidream i1 Full": "AtlasCloud Hidream i1 Full",
    "AtlasCloud Hidream i1 Dev": "AtlasCloud Hidream i1 Dev",
    "AtlasCloud Flux Schnell Lora": "AtlasCloud Flux Schnell Lora",
    "AtlasCloud Wan-2.1 Text-to-Image": "AtlasCloud Wan-2.1 Text-to-Image",
    "AtlasCloud Flux Schnell": "AtlasCloud Flux Schnell",
    "AtlasCloud Seedream V3": "AtlasCloud Seedream V3",

NODE_DISPLAY_NAME_MAPPINGS["Example"] = "Example (Deprecated)"
