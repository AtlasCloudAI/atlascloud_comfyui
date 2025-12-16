from atlascloud_comfyui.nodes.auth.atlas_client_node import AtlasClientNode
from atlascloud_comfyui.nodes.video.wan26_t2v import AtlasWAN26TextToVideo
from atlascloud_comfyui.nodes.video.wan25_t2v import AtlasWAN25TextToVideo
from atlascloud_comfyui.nodes.video.wan22_t2v_720p import AtlasWAN22T2V720p
from atlascloud_comfyui.nodes.video.veo31_t2v import AtlasVeo31TextToVideo
from atlascloud_comfyui.nodes.video.kling_v26_pro_t2v import AtlasKlingV26ProTextToVideo
from atlascloud_comfyui.nodes.video.kling_video_o1_t2v import AtlasKlingVideoO1TextToVideo
from atlascloud_comfyui.nodes.video.seedance_v1_pro_t2v_1080p import AtlasSeedanceV1ProT2V1080p
from atlascloud_comfyui.nodes.video.hailuo_23_t2v_pro import AtlasHailuo23T2VPro

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "AtlasCloud Client": AtlasClientNode,
    "AtlasCloud WAN2.5 Text-to-Video": AtlasWAN25TextToVideo,
    "AtlasCloud WAN2.6 Text-to-Video": AtlasWAN26TextToVideo,
    "AtlasCloud WAN2.2 Text-to-Video 720p": AtlasWAN22T2V720p,
    "AtlasCloud VEO3.1 Text-to-Video": AtlasVeo31TextToVideo,
    "AtlasCloud Kling V2.6 Pro Text-to-Video": AtlasKlingV26ProTextToVideo,
    "AtlasCloud Kling Video O1 Text-to-Video": AtlasKlingVideoO1TextToVideo,
    "AtlasCloud Seedance V1 Pro Text-to-Video 1080p": AtlasSeedanceV1ProT2V1080p,
    "AtlasCloud Hailuo 2.3 Pro Text-to-Video": AtlasHailuo23T2VPro,
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "AtlasCloud Client": "AtlasCloud Client (API Key/Base URL)",
    "AtlasCloud WAN2.5 Text-to-Video": "AtlasCloud WAN2.5 Text-to-Video",
    "AtlasCloud WAN2.6 Text-to-Video": "AtlasCloud WAN2.6 Text-to-Video",
    "AtlasCloud WAN2.2 Text-to-Video 720p": "AtlasCloud WAN2.2 Text-to-Video 720p",
    "AtlasCloud VEO3.1 Text-to-Video": "AtlasCloud VEO3.1 Text-to-Video",
    "AtlasCloud Kling V2.6 Pro Text-to-Video": "AtlasCloud Kling V26 Pro Text-to-Video",
    "AtlasCloud Kling Video O1 Text-to-Video": "AtlasCloud Kling Video O1 Text-to-Video",
    "AtlasCloud Seedance V1 Pro Text-to-Video 1080p": "AtlasCloud Seedance V1 Pro Text-to-Video 1080p",
    "AtlasCloud Hailuo 2.3 Pro Text-to-Video": "AtlasCloud Hailuo 23 Pro Text-to-Video",
}
