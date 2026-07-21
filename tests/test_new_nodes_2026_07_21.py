"""Metadata-only tests for newly added nodes (2026-07-21).

New models: Reve 2.1 Text-to-Image, Reve 2.1 Edit, Reve 2.1 Remix.
These tests MUST NOT require ATLASCLOUD_API_KEY.
"""


def test_reve_21_t2i_metadata():
    from src.atlascloud_comfyui.nodes.image.reve_21_t2i import (
        AtlasReve21TextToImage,
    )

    required = AtlasReve21TextToImage.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert "aspect_ratio" in required
    assert AtlasReve21TextToImage.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasReve21TextToImage.CATEGORY == "AtlasCloud/Image"


def test_reve_21_edit_metadata():
    from src.atlascloud_comfyui.nodes.image.reve_21_edit import AtlasReve21Edit

    required = AtlasReve21Edit.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert "prompt" in required
    assert AtlasReve21Edit.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasReve21Edit.CATEGORY == "AtlasCloud/Image"


def test_reve_21_remix_metadata():
    from src.atlascloud_comfyui.nodes.image.reve_21_remix import AtlasReve21Remix

    required = AtlasReve21Remix.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "images" in required
    assert "prompt" in required
    assert AtlasReve21Remix.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasReve21Remix.CATEGORY == "AtlasCloud/Image"


def test_new_nodes_2026_07_21_registered():
    from src.atlascloud_comfyui.registry import (
        NODE_CLASS_MAPPINGS,
        NODE_DISPLAY_NAME_MAPPINGS,
    )

    for key in (
        "AtlasCloud Reve 2.1 Text-to-Image",
        "AtlasCloud Reve 2.1 Edit",
        "AtlasCloud Reve 2.1 Remix",
    ):
        assert key in NODE_CLASS_MAPPINGS
        assert key in NODE_DISPLAY_NAME_MAPPINGS


def test_new_nodes_2026_07_21_model_ids():
    import inspect

    from src.atlascloud_comfyui.nodes.image.reve_21_t2i import AtlasReve21TextToImage
    from src.atlascloud_comfyui.nodes.image.reve_21_edit import AtlasReve21Edit
    from src.atlascloud_comfyui.nodes.image.reve_21_remix import AtlasReve21Remix

    assert '"model": "reve-ai/reve-2.1/text-to-image"' in inspect.getsource(AtlasReve21TextToImage.run)
    assert '"model": "reve-ai/reve-2.1/edit"' in inspect.getsource(AtlasReve21Edit.run)
    assert '"model": "reve-ai/reve-2.1/remix"' in inspect.getsource(AtlasReve21Remix.run)
