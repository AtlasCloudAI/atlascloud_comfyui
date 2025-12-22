"""Top-level package for atlascloud_comfyui."""

import os
import sys
import pkgutil

# 让 ComfyUI 能 import 到 src/ 里的包
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(THIS_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

WEB_DIRECTORY = "./web"

# Important: this repo is itself named `atlascloud_comfyui` and also contains
# the real package at `src/atlascloud_comfyui`. When `atlascloud_comfyui` is
# imported from the repo root (e.g. tests), Python will treat this directory
# as the package and submodule imports will only search `__path__`.
# Extend `__path__` so `atlascloud_comfyui.registry` resolves to the src package.
__path__ = pkgutil.extend_path(__path__, __name__)  # type: ignore[name-defined]
SRC_PKG_DIR = os.path.join(SRC_DIR, "atlascloud_comfyui")
if os.path.isdir(SRC_PKG_DIR) and SRC_PKG_DIR not in __path__:
    __path__.append(SRC_PKG_DIR)

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]

__author__ = """AtlasCloud"""
__email__ = "irene.chen@atlascloud.ai"
__version__ = "0.0.1"

try:
    from atlascloud_comfyui.registry import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS
except Exception as e:
    # Keep variables defined so tooling doesn't crash, but surface why it failed
    print("[AtlasCloud] Failed to import registry:", repr(e))
    NODE_CLASS_MAPPINGS = {}
    NODE_DISPLAY_NAME_MAPPINGS = {}
