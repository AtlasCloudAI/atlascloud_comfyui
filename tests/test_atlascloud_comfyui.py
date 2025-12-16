#!/usr/bin/env python

"""Tests for `atlascloud_comfyui` package."""

import pytest
from src.atlascloud_comfyui.nodes.auth.atlas_client_node import AtlasClientNode


@pytest.fixture
def example_node():
    """Fixture to create an Example node instance."""
    return AtlasClientNode()


def test_example_node_initialization(example_node):
    """Test that the node can be instantiated."""
    assert isinstance(example_node, AtlasClientNode)


def test_return_types():
    """Test the node's metadata."""
    assert AtlasClientNode.RETURN_NAMES == ("atlas_client",)
    assert AtlasClientNode.INPUT_TYPES == {
        "required": {
            "api_key": ("STRING", {"default": ""}),
        },
        "optional": {
            "base_url": ("STRING", {"default": "https://api.atlascloud.ai"}),
        },
    }
