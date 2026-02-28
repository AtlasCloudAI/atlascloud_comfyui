#!/usr/bin/env python

"""Tests for `atlascloud_comfyui` package.

Covers:
- AtlasClientNode (auth): INPUT_TYPES, RETURN_NAMES, instantiation.
- Model nodes (video/image): INPUT_TYPES, RETURN_TYPES, instantiation.
  Ensures nodes added by OpenClaw are usable before push.
"""

import pytest
from src.atlascloud_comfyui.nodes.auth.atlas_client_node import AtlasClientNode


@pytest.fixture
def atlas_client_node():
    """Fixture to create an AtlasClientNode instance."""
    return AtlasClientNode()


def test_atlas_client_node_initialization(atlas_client_node):
    """Test that AtlasClientNode can be instantiated."""
    assert isinstance(atlas_client_node, AtlasClientNode)


def test_atlas_client_node_metadata():
    """Test AtlasClientNode INPUT_TYPES and RETURN_NAMES."""
    assert AtlasClientNode.RETURN_NAMES == ("atlas_client",)
    assert AtlasClientNode.INPUT_TYPES() == {
        "required": {
            "api_key": ("STRING", {"default": ""}),
        },
        "optional": {
            "base_url": ("STRING", {"default": "https://api.atlascloud.ai"}),
        },
    }


# Model nodes: ensure INPUT_TYPES and RETURN_TYPES are correct so nodes are usable
def test_wan26_t2v_node_metadata():
    """Test WAN2.6 Text-to-Video node metadata."""
    from src.atlascloud_comfyui.nodes.video.wan26_t2v import AtlasWAN26TextToVideo

    assert "atlas_client" in [k for k, _ in AtlasWAN26TextToVideo.INPUT_TYPES()["required"].items()]
    assert AtlasWAN26TextToVideo.RETURN_TYPES == ("STRING", "STRING")
    assert "video_url" in AtlasWAN26TextToVideo.RETURN_NAMES


def test_flux2_flex_t2i_node_metadata():
    """Test Flux2 Flex Text-to-Image node metadata."""
    from src.atlascloud_comfyui.nodes.image.flux2_flex_t2i import AtlasFlux2FlexTextToImage

    assert "atlas_client" in [k for k, _ in AtlasFlux2FlexTextToImage.INPUT_TYPES()["required"].items()]
    assert AtlasFlux2FlexTextToImage.RETURN_TYPES == ("STRING", "STRING")
