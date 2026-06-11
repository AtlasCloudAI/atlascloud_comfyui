"""Metadata-only tests for newly added nodes (2026-06-11).

Microsoft MAI-Image-2.5 family: text-to-image and edit, standard and flash.
These tests MUST NOT require ATLASCLOUD_API_KEY.
"""


def test_mai_image_25_t2i_metadata():
    from src.atlascloud_comfyui.nodes.image.mai_image_25_t2i import (
        AtlasMAIImage25TextToImage,
    )

    required = AtlasMAIImage25TextToImage.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert AtlasMAIImage25TextToImage.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasMAIImage25TextToImage.CATEGORY == "AtlasCloud/Image"


def test_mai_image_25_flash_t2i_metadata():
    from src.atlascloud_comfyui.nodes.image.mai_image_25_flash_t2i import (
        AtlasMAIImage25FlashTextToImage,
    )

    required = AtlasMAIImage25FlashTextToImage.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert AtlasMAIImage25FlashTextToImage.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasMAIImage25FlashTextToImage.CATEGORY == "AtlasCloud/Image"


def test_mai_image_25_edit_metadata():
    from src.atlascloud_comfyui.nodes.image.mai_image_25_edit import (
        AtlasMAIImage25Edit,
    )

    required = AtlasMAIImage25Edit.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert "image" in required
    assert AtlasMAIImage25Edit.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasMAIImage25Edit.CATEGORY == "AtlasCloud/Image"


def test_mai_image_25_flash_edit_metadata():
    from src.atlascloud_comfyui.nodes.image.mai_image_25_flash_edit import (
        AtlasMAIImage25FlashEdit,
    )

    required = AtlasMAIImage25FlashEdit.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert "image" in required
    assert AtlasMAIImage25FlashEdit.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasMAIImage25FlashEdit.CATEGORY == "AtlasCloud/Image"


def test_new_nodes_2026_06_11_registered():
    from src.atlascloud_comfyui.registry import (
        NODE_CLASS_MAPPINGS,
        NODE_DISPLAY_NAME_MAPPINGS,
    )

    for key in (
        "AtlasCloud MAI-Image-2.5 Text-to-Image",
        "AtlasCloud MAI-Image-2.5-Flash Text-to-Image",
        "AtlasCloud MAI-Image-2.5 Edit",
        "AtlasCloud MAI-Image-2.5-Flash Edit",
    ):
        assert key in NODE_CLASS_MAPPINGS
        assert key in NODE_DISPLAY_NAME_MAPPINGS


def test_new_nodes_2026_06_11_model_ids():
    import inspect

    from src.atlascloud_comfyui.nodes.image.mai_image_25_t2i import AtlasMAIImage25TextToImage
    from src.atlascloud_comfyui.nodes.image.mai_image_25_flash_t2i import AtlasMAIImage25FlashTextToImage
    from src.atlascloud_comfyui.nodes.image.mai_image_25_edit import AtlasMAIImage25Edit
    from src.atlascloud_comfyui.nodes.image.mai_image_25_flash_edit import AtlasMAIImage25FlashEdit

    expected = {
        AtlasMAIImage25TextToImage: "microsoft/mai-image-2.5/text-to-image",
        AtlasMAIImage25FlashTextToImage: "microsoft/mai-image-2.5-flash/text-to-image",
        AtlasMAIImage25Edit: "microsoft/mai-image-2.5/edit",
        AtlasMAIImage25FlashEdit: "microsoft/mai-image-2.5-flash/edit",
    }
    for cls, model_id in expected.items():
        assert model_id in inspect.getsource(cls.run)
