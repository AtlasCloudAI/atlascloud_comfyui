"""Metadata-only tests for newly added nodes (2026-07-03).

HiDream O1 1.5 (text-to-image + edit) and lipsync nodes (sync/lipsync-v3, veed/lipsync).
These tests MUST NOT require ATLASCLOUD_API_KEY.
"""


def test_hidream_o1_15_t2i_metadata():
    from src.atlascloud_comfyui.nodes.image.hidream_o1_15_t2i import (
        AtlasHiDreamO115TextToImage,
    )

    required = AtlasHiDreamO115TextToImage.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert AtlasHiDreamO115TextToImage.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasHiDreamO115TextToImage.CATEGORY == "AtlasCloud/Image"


def test_hidream_o1_15_edit_metadata():
    from src.atlascloud_comfyui.nodes.image.hidream_o1_15_edit import (
        AtlasHiDreamO115Edit,
    )

    required = AtlasHiDreamO115Edit.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert "prompt" in required
    assert AtlasHiDreamO115Edit.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasHiDreamO115Edit.CATEGORY == "AtlasCloud/Image"


def test_sync_lipsync_v3_metadata():
    from src.atlascloud_comfyui.nodes.video.sync_lipsync_v3 import AtlasSyncLipsyncV3

    required = AtlasSyncLipsyncV3.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "video" in required
    assert "audio" in required
    assert "sync_mode" in required
    assert AtlasSyncLipsyncV3.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasSyncLipsyncV3.CATEGORY == "AtlasCloud/Video"


def test_veed_lipsync_metadata():
    from src.atlascloud_comfyui.nodes.video.veed_lipsync import AtlasVeedLipsync

    required = AtlasVeedLipsync.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "video" in required
    assert "audio" in required
    assert AtlasVeedLipsync.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasVeedLipsync.CATEGORY == "AtlasCloud/Video"


def test_new_nodes_2026_07_03_registered():
    from src.atlascloud_comfyui.registry import (
        NODE_CLASS_MAPPINGS,
        NODE_DISPLAY_NAME_MAPPINGS,
    )

    for key in (
        "AtlasCloud HiDream O1 1.5 Text-to-Image",
        "AtlasCloud HiDream O1 1.5 Edit",
        "AtlasCloud Sync Lipsync v3",
        "AtlasCloud VEED Lipsync",
    ):
        assert key in NODE_CLASS_MAPPINGS
        assert key in NODE_DISPLAY_NAME_MAPPINGS


def test_new_nodes_2026_07_03_model_ids():
    import inspect

    from src.atlascloud_comfyui.nodes.image.hidream_o1_15_t2i import AtlasHiDreamO115TextToImage
    from src.atlascloud_comfyui.nodes.image.hidream_o1_15_edit import AtlasHiDreamO115Edit
    from src.atlascloud_comfyui.nodes.video.sync_lipsync_v3 import AtlasSyncLipsyncV3
    from src.atlascloud_comfyui.nodes.video.veed_lipsync import AtlasVeedLipsync

    expected = {
        AtlasHiDreamO115TextToImage: "hidream-o1-1.5/text-to-image",
        AtlasHiDreamO115Edit: "hidream-o1-1.5/edit",
        AtlasSyncLipsyncV3: "sync/lipsync-v3",
        AtlasVeedLipsync: "veed/lipsync",
    }
    for cls, model_id in expected.items():
        assert model_id in inspect.getsource(cls.run)
