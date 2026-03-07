"""Generate ComfyUI nodes for a curated set of new AtlasCloud models.

This is a one-off helper used by the daily sync job (2026-03-07).
It reads schema URLs from the AtlasCloud models API and emits node modules
that follow the repo's conventions (no comfy/folder_paths/requests at import).

Safe to re-run: it will NOT overwrite existing files.

Usage:
  source .venv/bin/activate
  ATLASCLOUD_API_KEY=... python scripts/generate_nodes_2026_03_07.py
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Tuple

import requests

REPO_ROOT = Path(__file__).resolve().parents[1]
NODES_IMAGE_DIR = REPO_ROOT / "src" / "atlascloud_comfyui" / "nodes" / "image"
NODES_VIDEO_DIR = REPO_ROOT / "src" / "atlascloud_comfyui" / "nodes" / "video"

SELECTED_MODELS: List[str] = [
    "alibaba/qwen-image/edit",
    "alibaba/qwen-image/edit-plus",
    "alibaba/wan-2.5/text-to-image",
    "atlascloud/qwen-image/text-to-image",
    "atlascloud/van-2.5/image-to-video",
    "atlascloud/van-2.5/text-to-video",
    "bytedance/seedream-v4",
    "bytedance/seedream-v4/edit",
    "bytedance/seedream-v4/edit-sequential",
    "bytedance/seedream-v4/sequential",
    "kwaivgi/kling-v2.1-i2v-standard",
    "alibaba/wan-2.2/animate-mix",
    "alibaba/wan-2.2/animate-move",
    "black-forest-labs/flux-dev",
    "black-forest-labs/flux-dev-lora",
]


def slugify_model_id(mid: str) -> str:
    s = mid
    s = s.replace("/", "_")
    s = s.replace("-", "_")
    s = s.replace(".", "_")
    return s


def pascal_from_model(mid: str) -> str:
    parts = [p for p in re.split(r"[/\\\-\.]", mid) if p]

    def cap(token: str) -> str:
        # Keep already-all-caps segments as-is
        if token.isupper():
            return token
        # Split underscores and title-case each
        out = ""
        for t in re.split(r"_+", token):
            if not t:
                continue
            out += t[:1].upper() + t[1:]
        return out

    return "".join(cap(p) for p in parts)


@dataclass
class ModelInfo:
    model: str
    type: str  # "Image" or "Video"
    tags: List[str]
    schema: str


def fetch_models() -> Dict[str, ModelInfo]:
    key = os.environ.get("ATLASCLOUD_API_KEY", "").strip()
    if not key:
        raise RuntimeError("ATLASCLOUD_API_KEY is not set")

    r = requests.get(
        "https://api.atlascloud.ai/api/v1/models",
        headers={"Authorization": f"Bearer {key}"},
        timeout=60,
    )
    r.raise_for_status()
    data = r.json()
    models = data.get("data")
    if not isinstance(models, list):
        raise RuntimeError(f"Unexpected models payload type: {type(models).__name__}")

    out: Dict[str, ModelInfo] = {}
    for m in models:
        mid = m.get("model")
        if not mid:
            continue
        out[mid] = ModelInfo(
            model=mid,
            type=m.get("type") or "",
            tags=list(m.get("tags") or []),
            schema=m.get("schema") or "",
        )
    return out


def fetch_schema(url: str) -> Dict[str, Any]:
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    return r.json()


def schema_input(schema: Dict[str, Any]) -> Tuple[List[str], Dict[str, Any]]:
    comps = (schema.get("components") or {}).get("schemas") or {}
    inp = comps.get("Input") or {}
    req = list(inp.get("required") or [])
    props = dict(inp.get("properties") or {})
    return req, props


def py_literal(obj: Any) -> str:
    # For small dicts/lists/strings, repr() is fine.
    return repr(obj)


def make_image_node(model_id: str, req: List[str], props: Dict[str, Any]) -> Tuple[str, str, str]:
    required = set(req)
    is_edit = ("images" in required) or ("image" in required)

    class_name = f"Atlas{pascal_from_model(model_id)}" + ("Edit" if is_edit else "TextToImage")
    module_name = f"{slugify_model_id(model_id)}.py"

    required_inputs: Dict[str, Any] = {"atlas_client": ("ATLAS_CLIENT",)}
    optional_inputs: Dict[str, Any] = {}

    # prompt is required for all these image models
    required_inputs["prompt"] = ("STRING", {"multiline": True, "tooltip": "Text prompt"})

    if "images" in props:
        required_inputs["images"] = (
            "STRING",
            {"multiline": True, "default": "", "tooltip": "1-10 image URLs/base64, one per line"},
        )
    if "image" in props and "images" not in props:
        required_inputs["image"] = ("STRING", {"default": "", "tooltip": "Input image URL/base64"})

    if "size" in props:
        enum = props["size"].get("enum")
        default = props["size"].get("default")
        if enum:
            required_inputs["size"] = (enum, {"default": default or enum[0], "tooltip": "Output size (WIDTH*HEIGHT)"})
        else:
            required_inputs["size"] = ("STRING", {"default": str(default or ""), "tooltip": "Output size (WIDTH*HEIGHT)"})

    if "aspect_ratio" in props:
        enum = props["aspect_ratio"].get("enum")
        default = props["aspect_ratio"].get("default")
        if enum:
            required_inputs["aspect_ratio"] = (enum, {"default": default or enum[0], "tooltip": "Aspect ratio"})
        else:
            required_inputs["aspect_ratio"] = ("STRING", {"default": str(default or ""), "tooltip": "Aspect ratio"})

    if "resolution" in props:
        enum = props["resolution"].get("enum")
        default = props["resolution"].get("default")
        if enum:
            required_inputs["resolution"] = (enum, {"default": default or enum[0], "tooltip": "Resolution preset"})

    if "negative_prompt" in props:
        optional_inputs["negative_prompt"] = ("STRING", {"multiline": True, "default": "", "tooltip": "Negative prompt"})

    if "num_images" in props:
        p = props["num_images"]
        optional_inputs["num_images"] = (
            "INT",
            {
                "default": int(p.get("default") or 1),
                "min": int(p.get("minimum") or 1),
                "max": int(p.get("maximum") or 6),
                "tooltip": "Number of images",
            },
        )

    if "max_images" in props:
        p = props["max_images"]
        optional_inputs["max_images"] = (
            "INT",
            {
                "default": int(p.get("default") or 1),
                "min": int(p.get("minimum") or 1),
                "max": int(p.get("maximum") or 14),
                "tooltip": "Max images",
            },
        )

    if "prompt_extend" in props:
        optional_inputs["prompt_extend"] = (
            "BOOLEAN",
            {"default": bool(props["prompt_extend"].get("default", False)), "tooltip": "Intelligent prompt rewriting"},
        )

    if "enable_prompt_expansion" in props:
        optional_inputs["enable_prompt_expansion"] = (
            "BOOLEAN",
            {"default": bool(props["enable_prompt_expansion"].get("default", False)), "tooltip": "Enable prompt optimizer"},
        )

    if "strength" in props:
        p = props["strength"]
        optional_inputs["strength"] = (
            "FLOAT",
            {
                "default": float(p.get("default") or 0.8),
                "min": float(p.get("minimum") or 0.0),
                "max": float(p.get("maximum") or 1.0),
                "tooltip": "Strength (image transform)",
            },
        )

    if "num_inference_steps" in props:
        p = props["num_inference_steps"]
        optional_inputs["num_inference_steps"] = (
            "INT",
            {
                "default": int(p.get("default") or 28),
                "min": int(p.get("minimum") or 1),
                "max": int(p.get("maximum") or 50),
                "tooltip": "Inference steps",
            },
        )

    if "guidance_scale" in props:
        p = props["guidance_scale"]
        optional_inputs["guidance_scale"] = (
            "FLOAT",
            {"default": float(p.get("default") or 3.5), "min": 0.0, "max": 20.0, "tooltip": "Guidance scale"},
        )

    if "enable_safety_checker" in props:
        optional_inputs["enable_safety_checker"] = (
            "BOOLEAN",
            {"default": bool(props["enable_safety_checker"].get("default", True)), "tooltip": "Enable safety checker"},
        )

    if "mask_image" in props:
        optional_inputs["mask_image"] = ("STRING", {"default": "", "tooltip": "Mask image URL/base64 (optional)"})

    if "seed" in props:
        optional_inputs["seed"] = (
            "INT",
            {"default": int(props["seed"].get("default", -1)), "min": -1, "max": 2**31 - 1, "tooltip": "Random if -1"},
        )

    if "enable_base64_output" in props:
        optional_inputs["enable_base64_output"] = (
            "BOOLEAN",
            {"default": bool(props["enable_base64_output"].get("default", False)), "tooltip": "Return base64 instead of URL if supported"},
        )

    if "enable_sync_mode" in props:
        optional_inputs["enable_sync_mode"] = (
            "BOOLEAN",
            {"default": bool(props["enable_sync_mode"].get("default", False)), "tooltip": "Try to return synchronously"},
        )

    if "output_format" in props and props["output_format"].get("enum"):
        enum = props["output_format"].get("enum")
        default = props["output_format"].get("default") or enum[0]
        optional_inputs["output_format"] = (enum, {"default": default, "tooltip": "Output format"})

    if "loras" in props:
        optional_inputs["loras_json"] = ("STRING", {"default": "[]", "multiline": True, "tooltip": "JSON array for loras. Example: []"})

    optional_inputs["poll_interval_sec"] = (
        "FLOAT",
        {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"},
    )
    optional_inputs["timeout_sec"] = (
        "INT",
        {"default": 300, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"},
    )

    # --- render file ---
    required_inputs_py = py_literal(required_inputs)
    optional_inputs_py = py_literal(optional_inputs)

    # build run signature (required first, then optional)
    run_args: List[str] = ["atlas_client: AtlasClientHandle", "prompt: str"]
    if "images" in required_inputs:
        run_args.append("images: str")
    if "image" in required_inputs:
        run_args.append("image: str")
    for k in ("size", "aspect_ratio", "resolution"):
        if k in required_inputs:
            run_args.append(f"{k}: str")

    # optionals
    if "negative_prompt" in optional_inputs:
        run_args.append("negative_prompt: str = \"\"")
    if "num_images" in optional_inputs:
        run_args.append("num_images: int = 1")
    if "max_images" in optional_inputs:
        run_args.append("max_images: int = 1")
    if "prompt_extend" in optional_inputs:
        run_args.append("prompt_extend: bool = False")
    if "enable_prompt_expansion" in optional_inputs:
        run_args.append("enable_prompt_expansion: bool = False")
    if "strength" in optional_inputs:
        run_args.append("strength: float = 0.8")
    if "mask_image" in optional_inputs:
        run_args.append("mask_image: str = \"\"")
    if "num_inference_steps" in optional_inputs:
        run_args.append("num_inference_steps: int = 28")
    if "guidance_scale" in optional_inputs:
        run_args.append("guidance_scale: float = 3.5")
    if "enable_safety_checker" in optional_inputs:
        run_args.append("enable_safety_checker: bool = True")
    if "seed" in optional_inputs:
        run_args.append("seed: int = -1")
    if "enable_base64_output" in optional_inputs:
        run_args.append("enable_base64_output: bool = False")
    if "enable_sync_mode" in optional_inputs:
        run_args.append("enable_sync_mode: bool = False")
    if "output_format" in optional_inputs:
        run_args.append("output_format: str = \"png\"")
    if "loras_json" in optional_inputs:
        run_args.append("loras_json: str = \"[]\"")

    run_args.append("poll_interval_sec: float = 2.0")
    run_args.append("timeout_sec: int = 300")

    lines: List[str] = []
    lines.append("from __future__ import annotations")
    lines.append("")
    lines.append("from typing import Any, Dict, List, Tuple")
    lines.append("")
    lines.append("from ..auth.atlas_client_node import AtlasClientHandle")
    lines.append("")
    lines.append("")
    lines.append(f"class {class_name}:")
    lines.append('    CATEGORY = "AtlasCloud/Image"')
    lines.append('    FUNCTION = "run"')
    lines.append('    RETURN_TYPES = ("STRING", "STRING")')
    lines.append('    RETURN_NAMES = ("image_url", "prediction_id")')
    lines.append("")
    lines.append("    @classmethod")
    lines.append("    def INPUT_TYPES(cls):")
    lines.append("        return {")
    lines.append(f"            \"required\": {required_inputs_py},")
    lines.append(f"            \"optional\": {optional_inputs_py},")
    lines.append("        }")
    lines.append("")
    lines.append("    def run(")
    lines.append("        self,")
    for arg in run_args:
        lines.append(f"        {arg},")
    lines.append("    ) -> Tuple[str, str]:")
    lines.append("        client = atlas_client.client")
    lines.append("")
    lines.append("        p = (prompt or '').strip()")
    lines.append("        if not p:")
    lines.append("            raise RuntimeError('prompt is required')")
    lines.append("")

    if "images" in required_inputs:
        lines.append("        image_list: List[str] = [v.strip() for v in (images or '').splitlines() if v.strip()]")
        lines.append("        if not image_list:")
        lines.append("            raise RuntimeError('images is required (1-10 lines)')")
        lines.append("        if len(image_list) > 10:")
        lines.append("            raise RuntimeError('images maxItems is 10')")
        lines.append("")

    if "image" in required_inputs:
        lines.append("        image = (image or '').strip()")
        lines.append("        if not image:")
        lines.append("            raise RuntimeError('image is required (URL or base64)')")
        lines.append("")

    if "loras_json" in optional_inputs:
        lines.append("        import json")
        lines.append("        try:")
        lines.append("            loras = json.loads(loras_json) if (loras_json or '').strip() else []")
        lines.append("            if not isinstance(loras, list):")
        lines.append("                raise ValueError('loras_json must be a JSON array')")
        lines.append("        except Exception as e:")
        lines.append("            raise RuntimeError(f'Invalid loras_json. Must be a JSON array. Error: {e}') from e")
        lines.append("")

    # payload
    lines.append("        payload: Dict[str, Any] = {")
    lines.append(f"            'model': '{model_id}',")
    lines.append("            'prompt': p,")
    if "images" in required_inputs:
        lines.append("            'images': image_list,")
    if "image" in required_inputs:
        lines.append("            'image': image,")
    for k in ("size", "aspect_ratio", "resolution"):
        if k in required_inputs:
            lines.append(f"            '{k}': {k},")

    # optionals (safe defaults)
    if "num_images" in optional_inputs:
        lines.append("            'num_images': int(num_images),")
    if "max_images" in optional_inputs:
        lines.append("            'max_images': int(max_images),")
    if "prompt_extend" in optional_inputs:
        lines.append("            'prompt_extend': bool(prompt_extend),")
    if "enable_prompt_expansion" in optional_inputs:
        lines.append("            'enable_prompt_expansion': bool(enable_prompt_expansion),")
    if "strength" in optional_inputs:
        lines.append("            'strength': float(strength),")
    if "mask_image" in optional_inputs:
        lines.append("            'mask_image': (mask_image or '').strip(),")
    if "num_inference_steps" in optional_inputs:
        lines.append("            'num_inference_steps': int(num_inference_steps),")
    if "guidance_scale" in optional_inputs:
        lines.append("            'guidance_scale': float(guidance_scale),")
    if "enable_safety_checker" in optional_inputs:
        lines.append("            'enable_safety_checker': bool(enable_safety_checker),")
    if "seed" in optional_inputs:
        lines.append("            'seed': int(seed),")
    if "enable_base64_output" in optional_inputs:
        lines.append("            'enable_base64_output': bool(enable_base64_output),")
    if "enable_sync_mode" in optional_inputs:
        lines.append("            'enable_sync_mode': bool(enable_sync_mode),")
    if "output_format" in optional_inputs:
        lines.append("            'output_format': output_format,")
    if "loras_json" in optional_inputs:
        lines.append("            'loras': loras,")
    lines.append("        }")
    lines.append("")

    if "negative_prompt" in optional_inputs:
        lines.append("        neg = (negative_prompt or '').strip()")
        lines.append("        if neg:")
        lines.append("            payload['negative_prompt'] = neg")
        lines.append("")

    if "mask_image" in optional_inputs:
        lines.append("        if not (payload.get('mask_image') or '').strip():")
        lines.append("            payload.pop('mask_image', None)")
        lines.append("")

    lines.append("        prediction_id = client.generate_image(payload)")
    lines.append("        result = client.poll_prediction(prediction_id, poll_interval_sec=poll_interval_sec, timeout_sec=float(timeout_sec))")
    lines.append("")
    lines.append("        outputs = (result.get('data') or {}).get('outputs') or []")
    lines.append("        if not outputs:")
    lines.append("            raise RuntimeError(f'No outputs returned for prediction {prediction_id}: {result}')")
    lines.append("")
    lines.append("        first = outputs[0]")
    lines.append("        if isinstance(first, dict):")
    lines.append("            url = first.get('url') or first.get('image') or first.get('output')")
    lines.append("            if isinstance(url, str) and url.strip():")
    lines.append("                return (url, prediction_id)")
    lines.append("            raise RuntimeError(f'Unexpected output object for prediction {prediction_id}: {first}')")
    lines.append("")
    lines.append("        if not isinstance(first, str):")
    lines.append("            raise RuntimeError(f'Unexpected output type for prediction {prediction_id}: {type(first).__name__} {first!r}')")
    lines.append("")
    lines.append("        return (first, prediction_id)")
    lines.append("")

    return module_name, class_name, "\n".join(lines)


def make_video_node(model_id: str, req: List[str], props: Dict[str, Any]) -> Tuple[str, str, str]:
    required = set(req)

    has_image = "image" in props
    has_video = "video" in props
    has_mode = "mode" in props

    # classify
    is_i2v = "image" in required
    is_animate = model_id.startswith("alibaba/wan-2.2/animate") and has_image and has_video and has_mode

    if is_i2v:
        suffix = "I2V"
    elif is_animate:
        suffix = "ReferenceToVideo"
    else:
        suffix = "TextToVideo"

    class_name = f"Atlas{pascal_from_model(model_id)}{suffix}"
    module_name = f"{slugify_model_id(model_id)}.py"

    required_inputs: Dict[str, Any] = {"atlas_client": ("ATLAS_CLIENT",)}
    optional_inputs: Dict[str, Any] = {}

    if "prompt" in props:
        required_inputs["prompt"] = ("STRING", {"multiline": True, "tooltip": "Text prompt"})

    if "image" in props and "image" in required:
        required_inputs["image"] = ("STRING", {"default": "", "tooltip": "Input image URL/base64"})

    if is_animate:
        required_inputs["image"] = ("STRING", {"default": "", "tooltip": "Input image URL/base64"})
        required_inputs["video"] = ("STRING", {"default": "", "tooltip": "Reference/input video URL"})

        enum = props.get("mode", {}).get("enum")
        default = props.get("mode", {}).get("default")
        if enum:
            required_inputs["mode"] = (enum, {"default": default or enum[0], "tooltip": "Mode"})
        else:
            required_inputs["mode"] = ("STRING", {"default": str(default or ""), "tooltip": "Mode"})

    # van-2.5
    if "resolution" in props and "resolution" in required:
        enum = props["resolution"].get("enum")
        default = props["resolution"].get("default")
        if enum:
            required_inputs["resolution"] = (enum, {"default": default or enum[0], "tooltip": "Resolution"})
        else:
            required_inputs["resolution"] = ("STRING", {"default": str(default or ""), "tooltip": "Resolution"})

    if "size" in props and "size" in required:
        enum = props["size"].get("enum")
        default = props["size"].get("default")
        if enum:
            required_inputs["size"] = (enum, {"default": default or enum[0], "tooltip": "Size (WIDTH*HEIGHT)"})
        else:
            required_inputs["size"] = ("STRING", {"default": str(default or ""), "tooltip": "Size (WIDTH*HEIGHT)"})

    if "negative_prompt" in props:
        optional_inputs["negative_prompt"] = ("STRING", {"multiline": True, "default": "", "tooltip": "Negative prompt"})

    if "duration" in props:
        enum = props["duration"].get("enum")
        default = int(props["duration"].get("default") or 5)
        if enum:
            optional_inputs["duration"] = (enum, {"default": default, "tooltip": "Duration (seconds)"})
        else:
            optional_inputs["duration"] = ("INT", {"default": default, "min": 1, "max": 120, "tooltip": "Duration (seconds)"})

    if "audio" in props:
        optional_inputs["audio"] = ("STRING", {"default": "", "tooltip": "Audio URL (optional)"})

    if "enable_prompt_expansion" in props:
        optional_inputs["enable_prompt_expansion"] = (
            "BOOLEAN",
            {"default": bool(props["enable_prompt_expansion"].get("default", False)), "tooltip": "Enable prompt expansion"},
        )

    if "seed" in props:
        optional_inputs["seed"] = (
            "INT",
            {"default": int(props["seed"].get("default", -1)), "min": -1, "max": 2**31 - 1, "tooltip": "Random if -1"},
        )

    optional_inputs["poll_interval_sec"] = (
        "FLOAT",
        {"default": 2.0, "min": 0.5, "max": 10.0, "tooltip": "Polling interval (seconds)"},
    )
    optional_inputs["timeout_sec"] = (
        "INT",
        {"default": 900, "min": 30, "max": 7200, "tooltip": "Timeout (seconds)"},
    )

    required_inputs_py = py_literal(required_inputs)
    optional_inputs_py = py_literal(optional_inputs)

    run_args: List[str] = ["atlas_client: AtlasClientHandle"]
    if "prompt" in required_inputs:
        run_args.append("prompt: str")
    if "image" in required_inputs:
        run_args.append("image: str")
    if "video" in required_inputs:
        run_args.append("video: str")
    if "mode" in required_inputs:
        run_args.append("mode: str")
    if "resolution" in required_inputs:
        run_args.append("resolution: str")
    if "size" in required_inputs:
        run_args.append("size: str")

    # optionals
    if "negative_prompt" in optional_inputs:
        run_args.append("negative_prompt: str = \"\"")
    if "duration" in optional_inputs:
        run_args.append("duration: int = 5")
    if "audio" in optional_inputs:
        run_args.append("audio: str = \"\"")
    if "enable_prompt_expansion" in optional_inputs:
        run_args.append("enable_prompt_expansion: bool = False")
    if "seed" in optional_inputs:
        run_args.append("seed: int = -1")

    run_args.append("poll_interval_sec: float = 2.0")
    run_args.append("timeout_sec: int = 900")

    lines: List[str] = []
    lines.append("from __future__ import annotations")
    lines.append("")
    lines.append("from typing import Any, Dict, Tuple")
    lines.append("")
    lines.append("from ..auth.atlas_client_node import AtlasClientHandle")
    lines.append("")
    lines.append("")
    lines.append(f"class {class_name}:")
    lines.append('    CATEGORY = "AtlasCloud/Video"')
    lines.append('    FUNCTION = "run"')
    lines.append('    RETURN_TYPES = ("STRING", "STRING")')
    lines.append('    RETURN_NAMES = ("video_url", "prediction_id")')
    lines.append("")
    lines.append("    @classmethod")
    lines.append("    def INPUT_TYPES(cls):")
    lines.append("        return {")
    lines.append(f"            \"required\": {required_inputs_py},")
    lines.append(f"            \"optional\": {optional_inputs_py},")
    lines.append("        }")
    lines.append("")
    lines.append("    def run(")
    lines.append("        self,")
    for arg in run_args:
        lines.append(f"        {arg},")
    lines.append("    ) -> Tuple[str, str]:")
    lines.append("        client = atlas_client.client")
    lines.append("")

    if "image" in required_inputs:
        lines.append("        image = (image or '').strip()")
        lines.append("        if not image:")
        lines.append("            raise RuntimeError('image is required (URL or base64)')")
        lines.append("")

    if "video" in required_inputs:
        lines.append("        video = (video or '').strip()")
        lines.append("        if not video:")
        lines.append("            raise RuntimeError('video is required (URL)')")
        lines.append("")

    # payload
    lines.append("        payload: Dict[str, Any] = {")
    lines.append(f"            'model': '{model_id}',")
    if "prompt" in required_inputs:
        lines.append("            'prompt': prompt,")
    if "mode" in required_inputs:
        lines.append("            'mode': mode,")
    if "resolution" in required_inputs:
        lines.append("            'resolution': resolution,")
    if "size" in required_inputs:
        lines.append("            'size': size,")
    if "duration" in optional_inputs:
        lines.append("            'duration': int(duration),")
    if "enable_prompt_expansion" in optional_inputs:
        lines.append("            'enable_prompt_expansion': bool(enable_prompt_expansion),")
    if "seed" in optional_inputs:
        lines.append("            'seed': int(seed),")
    if "image" in required_inputs:
        lines.append("            'image': image,")
    if "video" in required_inputs:
        lines.append("            'video': video,")
    lines.append("        }")
    lines.append("")

    if "negative_prompt" in optional_inputs:
        lines.append("        neg = (negative_prompt or '').strip()")
        lines.append("        if neg:")
        lines.append("            payload['negative_prompt'] = neg")
        lines.append("")

    if "audio" in optional_inputs:
        lines.append("        a = (audio or '').strip()")
        lines.append("        if a:")
        lines.append("            payload['audio'] = a")
        lines.append("")

    lines.append("        prediction_id = client.generate_video(payload)")
    lines.append("        result = client.poll_prediction(prediction_id, poll_interval_sec=poll_interval_sec, timeout_sec=float(timeout_sec))")
    lines.append("")
    lines.append("        outputs = (result.get('data') or {}).get('outputs') or []")
    lines.append("        if not outputs:")
    lines.append("            raise RuntimeError(f'No outputs returned for prediction {prediction_id}: {result}')")
    lines.append("")
    lines.append("        first = outputs[0]")
    lines.append("        if not isinstance(first, str):")
    lines.append("            raise RuntimeError(f'Unexpected output type for prediction {prediction_id}: {type(first).__name__} {first!r}')")
    lines.append("")
    lines.append("        return (first, prediction_id)")
    lines.append("")

    return module_name, class_name, "\n".join(lines)


def main() -> None:
    models = fetch_models()

    created: List[Tuple[str, str, str]] = []  # (model_id, file, class)

    for mid in SELECTED_MODELS:
        info = models.get(mid)
        if not info:
            raise RuntimeError(f"Model not found in API: {mid}")
        if not info.schema:
            raise RuntimeError(f"Model schema missing: {mid}")

        schema = fetch_schema(info.schema)
        req, props = schema_input(schema)

        if info.type == "Image":
            module_name, class_name, content = make_image_node(mid, req, props)
            out_path = NODES_IMAGE_DIR / module_name
        elif info.type == "Video":
            module_name, class_name, content = make_video_node(mid, req, props)
            out_path = NODES_VIDEO_DIR / module_name
        else:
            continue

        if out_path.exists():
            # Never overwrite
            continue

        out_path.write_text(content, encoding="utf-8")
        created.append((mid, str(out_path.relative_to(REPO_ROOT)), class_name))

    print(f"created={len(created)}")
    for mid, fp, cls in created:
        print(f"- {mid} -> {fp} ({cls})")


if __name__ == "__main__":
    main()
