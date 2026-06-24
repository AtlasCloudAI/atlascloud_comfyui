"""Metadata-only tests for newly added nodes (2026-06-24).

Youchuan V8.1 family (text-to-image, image-to-image, blend, style-transfer,
remove-background, image-to-video).
These tests MUST NOT require ATLASCLOUD_API_KEY.
"""


def test_youchuan_v81_t2i_metadata():
    from src.atlascloud_comfyui.nodes.image.youchuan_v81_t2i import (
        AtlasYouchuanV81TextToImage,
    )

    required = AtlasYouchuanV81TextToImage.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert AtlasYouchuanV81TextToImage.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasYouchuanV81TextToImage.CATEGORY == "AtlasCloud/Image"


def test_youchuan_v81_i2i_metadata():
    from src.atlascloud_comfyui.nodes.image.youchuan_v81_i2i import (
        AtlasYouchuanV81ImageToImage,
    )

    required = AtlasYouchuanV81ImageToImage.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert "prompt" in required
    assert AtlasYouchuanV81ImageToImage.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasYouchuanV81ImageToImage.CATEGORY == "AtlasCloud/Image"


def test_youchuan_v81_blend_metadata():
    from src.atlascloud_comfyui.nodes.image.youchuan_v81_blend import (
        AtlasYouchuanV81Blend,
    )

    required = AtlasYouchuanV81Blend.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "images" in required
    assert AtlasYouchuanV81Blend.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasYouchuanV81Blend.CATEGORY == "AtlasCloud/Image"


def test_youchuan_v81_style_transfer_metadata():
    from src.atlascloud_comfyui.nodes.image.youchuan_v81_style_transfer import (
        AtlasYouchuanV81StyleTransfer,
    )

    required = AtlasYouchuanV81StyleTransfer.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert "prompt" in required
    assert AtlasYouchuanV81StyleTransfer.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasYouchuanV81StyleTransfer.CATEGORY == "AtlasCloud/Image"


def test_youchuan_v81_remove_bg_metadata():
    from src.atlascloud_comfyui.nodes.image.youchuan_v81_remove_bg import (
        AtlasYouchuanV81RemoveBackground,
    )

    required = AtlasYouchuanV81RemoveBackground.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert AtlasYouchuanV81RemoveBackground.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasYouchuanV81RemoveBackground.CATEGORY == "AtlasCloud/Image"


def test_youchuan_v81_i2v_metadata():
    from src.atlascloud_comfyui.nodes.video.youchuan_v81_i2v import (
        AtlasYouchuanV81ImageToVideo,
    )

    required = AtlasYouchuanV81ImageToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert AtlasYouchuanV81ImageToVideo.RETURN_TYPES == ("STRING", "STRING")
    assert AtlasYouchuanV81ImageToVideo.CATEGORY == "AtlasCloud/Video"


def test_new_nodes_2026_06_24_registered():
    from src.atlascloud_comfyui.registry import (
        NODE_CLASS_MAPPINGS,
        NODE_DISPLAY_NAME_MAPPINGS,
    )

    for key in (
        "AtlasCloud Youchuan V8.1 Text-to-Image",
        "AtlasCloud Youchuan V8.1 Image-to-Image",
        "AtlasCloud Youchuan V8.1 Blend",
        "AtlasCloud Youchuan V8.1 Style Transfer",
        "AtlasCloud Youchuan V8.1 Remove Background",
        "AtlasCloud Youchuan V8.1 Image-to-Video",
    ):
        assert key in NODE_CLASS_MAPPINGS
        assert key in NODE_DISPLAY_NAME_MAPPINGS


def test_new_nodes_2026_06_24_model_ids():
    import inspect

    from src.atlascloud_comfyui.nodes.image.youchuan_v81_blend import AtlasYouchuanV81Blend
    from src.atlascloud_comfyui.nodes.image.youchuan_v81_i2i import AtlasYouchuanV81ImageToImage
    from src.atlascloud_comfyui.nodes.image.youchuan_v81_remove_bg import AtlasYouchuanV81RemoveBackground
    from src.atlascloud_comfyui.nodes.image.youchuan_v81_style_transfer import AtlasYouchuanV81StyleTransfer
    from src.atlascloud_comfyui.nodes.image.youchuan_v81_t2i import AtlasYouchuanV81TextToImage
    from src.atlascloud_comfyui.nodes.video.youchuan_v81_i2v import AtlasYouchuanV81ImageToVideo

    expected = {
        AtlasYouchuanV81TextToImage: "youchuan/v8.1/text-to-image",
        AtlasYouchuanV81ImageToImage: "youchuan/v8.1/image-to-image",
        AtlasYouchuanV81Blend: "youchuan/v8.1/blend",
        AtlasYouchuanV81StyleTransfer: "youchuan/v8.1/style-transfer",
        AtlasYouchuanV81RemoveBackground: "youchuan/v8.1/remove-background",
        AtlasYouchuanV81ImageToVideo: "youchuan/v8.1/image-to-video",
    }
    for cls, model_id in expected.items():
        assert model_id in inspect.getsource(cls.run)
