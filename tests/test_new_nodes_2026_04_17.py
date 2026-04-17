"""Metadata-only tests for newly added nodes (2026-04-17).

These tests MUST NOT require ATLASCLOUD_API_KEY.
"""


def test_vidu_q1_t2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.vidu_q1_t2v import AtlasViduQ1TextToVideo

    required = AtlasViduQ1TextToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert AtlasViduQ1TextToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_vidu_q1_i2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.vidu_q1_i2v import AtlasViduQ1ImageToVideo

    required = AtlasViduQ1ImageToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert "image" in required
    assert AtlasViduQ1ImageToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_vidu_q1_start_end_node_metadata():
    from src.atlascloud_comfyui.nodes.video.vidu_q1_start_end import AtlasViduQ1StartEndToVideo

    required = AtlasViduQ1StartEndToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert "image" in required
    assert "end_image" in required
    assert AtlasViduQ1StartEndToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_vidu_q1_r2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.vidu_q1_r2v import AtlasViduQ1ReferenceToVideo

    required = AtlasViduQ1ReferenceToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert "images" in required
    assert AtlasViduQ1ReferenceToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_vidu_q2_t2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.vidu_q2_t2v import AtlasViduQ2TextToVideo

    required = AtlasViduQ2TextToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert AtlasViduQ2TextToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_vidu_q2_r2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.vidu_q2_r2v import AtlasViduQ2ReferenceToVideo

    required = AtlasViduQ2ReferenceToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert "images" in required
    assert AtlasViduQ2ReferenceToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_vidu_q2_pro_i2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.vidu_q2_pro_i2v import AtlasViduQ2ProImageToVideo

    required = AtlasViduQ2ProImageToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert "image" in required
    assert AtlasViduQ2ProImageToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_vidu_q2_pro_start_end_node_metadata():
    from src.atlascloud_comfyui.nodes.video.vidu_q2_pro_start_end import AtlasViduQ2ProStartEndToVideo

    required = AtlasViduQ2ProStartEndToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert "image" in required
    assert "end_image" in required
    assert AtlasViduQ2ProStartEndToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_vidu_q2_pro_r2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.vidu_q2_pro_r2v import AtlasViduQ2ProReferenceToVideo

    required = AtlasViduQ2ProReferenceToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert "images" in required
    assert AtlasViduQ2ProReferenceToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_vidu_q2_pro_fast_i2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.vidu_q2_pro_fast_i2v import AtlasViduQ2ProFastImageToVideo

    required = AtlasViduQ2ProFastImageToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert "image" in required
    assert AtlasViduQ2ProFastImageToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_vidu_q2_pro_fast_start_end_node_metadata():
    from src.atlascloud_comfyui.nodes.video.vidu_q2_pro_fast_start_end import AtlasViduQ2ProFastStartEndToVideo

    required = AtlasViduQ2ProFastStartEndToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert "image" in required
    assert "end_image" in required
    assert AtlasViduQ2ProFastStartEndToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_vidu_q2_turbo_i2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.vidu_q2_turbo_i2v import AtlasViduQ2TurboImageToVideo

    required = AtlasViduQ2TurboImageToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert "image" in required
    assert AtlasViduQ2TurboImageToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_vidu_q2_turbo_start_end_node_metadata():
    from src.atlascloud_comfyui.nodes.video.vidu_q2_turbo_start_end import AtlasViduQ2TurboStartEndToVideo

    required = AtlasViduQ2TurboStartEndToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert "image" in required
    assert "end_image" in required
    assert AtlasViduQ2TurboStartEndToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_infinitetalk_a2v_node_metadata():
    from src.atlascloud_comfyui.nodes.video.atlascloud_infinitetalk_a2v import AtlasInfiniteTalkAudioToVideo

    required = AtlasInfiniteTalkAudioToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert "audio" in required
    assert AtlasInfiniteTalkAudioToVideo.RETURN_TYPES == ("STRING", "STRING")
