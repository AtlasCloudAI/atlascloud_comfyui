"""Metadata-only tests for newly added nodes (2026-07-20).

New model: Krea-2 Turbo Text-to-Image.
These tests MUST NOT require ATLASCLOUD_API_KEY.
"""


def test_krea_2_turbo_t2i_metadata():
    from src.atlascloud_comfyui.nodes.image.krea_2_turbo_t2i import (
        AtlasKrea2TurboTextToImage,
    )

    required = AtlasKrea2TurboTextToImage.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert "image_size" in required
    assert AtlasKrea2TurboTextToImage.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasKrea2TurboTextToImage.CATEGORY == "AtlasCloud/Image"


def test_new_nodes_2026_07_20_registered():
    from src.atlascloud_comfyui.registry import (
        NODE_CLASS_MAPPINGS,
        NODE_DISPLAY_NAME_MAPPINGS,
    )

    key = "AtlasCloud Krea-2 Turbo Text-to-Image"
    assert key in NODE_CLASS_MAPPINGS
    assert key in NODE_DISPLAY_NAME_MAPPINGS


def test_new_nodes_2026_07_20_model_ids():
    import inspect

    from src.atlascloud_comfyui.nodes.image.krea_2_turbo_t2i import AtlasKrea2TurboTextToImage

    src = inspect.getsource(AtlasKrea2TurboTextToImage.run)
    assert '"model": "krea-2-turbo/text-to-image"' in src
