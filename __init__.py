"""Top-level package for atlascloud_comfyui."""

import os
import sys

# 让 ComfyUI 能 import 到 src/ 里的包
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(THIS_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)


__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
]

__author__ = """AtlasCloud"""
__email__ = "irene.chen@atlascloud.ai"
__version__ = "0.0.1"

from atlascloud_comfyui.registry import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS
