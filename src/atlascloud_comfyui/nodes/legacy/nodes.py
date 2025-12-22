from __future__ import annotations

from inspect import cleandoc


class Example:
    """
    A example node (legacy from template)

    Kept for backward compatibility to satisfy comfy-org/node-diff.
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE", {"tooltip": "This is an image"}),
                "int_field": (
                    "INT",
                    {
                        "default": 0,
                        "min": 0,
                        "max": 4096,
                        "step": 64,
                        "display": "number",
                    },
                ),
                "float_field": (
                    "FLOAT",
                    {
                        "default": 1.0,
                        "min": 0.0,
                        "max": 10.0,
                        "step": 0.01,
                        "round": 0.001,
                        "display": "number",
                    },
                ),
                "print_to_screen": (["enable", "disable"],),
                "string_field": (
                    "STRING",
                    {
                        "multiline": False,
                        "default": "Hello World!",
                    },
                ),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    DESCRIPTION = cleandoc(__doc__)
    FUNCTION = "test"
    CATEGORY = "Example"

    def test(self, image, string_field, int_field, float_field, print_to_screen):
        if print_to_screen == "enable":
            print(
                f"""Your input contains:
                string_field aka input text: {string_field}
                int_field: {int_field}
                float_field: {float_field}
            """
            )
        # invert the image (expects IMAGE tensor in [0,1])
        image = 1.0 - image
        return (image,)


NODE_CLASS_MAPPINGS = {"Example": Example}
NODE_DISPLAY_NAME_MAPPINGS = {"Example": "Example Node"}
