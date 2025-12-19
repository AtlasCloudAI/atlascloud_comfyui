from __future__ import annotations


class Example:
    """
    Legacy placeholder for backwards compatibility.

    Kept to satisfy Comfy Registry / node-diff (avoids breaking change: node removed).
    """

    CATEGORY = "Example"
    FUNCTION = "run"
    RETURN_TYPES = ()
    RETURN_NAMES = ()
    OUTPUT_NODE = True

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {}}

    def run(self):
        raise RuntimeError("The legacy node 'Example' is deprecated. " "Please use AtlasCloud nodes under 'AtlasCloud/*' categories.")


NODE_CLASS_MAPPINGS = {"Example": Example}
NODE_DISPLAY_NAME_MAPPINGS = {"Example": "Example (Deprecated)"}
