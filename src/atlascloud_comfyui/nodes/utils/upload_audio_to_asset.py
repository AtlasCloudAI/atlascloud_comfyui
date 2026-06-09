from __future__ import annotations

import os

from atlascloud_comfyui.nodes.auth.atlas_client_node import AtlasClientHandle

_AUDIO_EXTS = (".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg")
_MIME = {".mp3": "audio/mpeg", ".wav": "audio/wav", ".m4a": "audio/mp4",
         ".aac": "audio/aac", ".flac": "audio/flac", ".ogg": "audio/ogg"}


def _input_audios():
    try:
        import folder_paths
        d = folder_paths.get_input_directory()
        return sorted([f for f in os.listdir(d) if f.lower().endswith(_AUDIO_EXTS)])
    except Exception:
        return []


class AtlasUploadAudioToAsset:
    """Upload a LOCAL audio file (with the ComfyUI upload button) and return its
    public URL — ready to wire into Seedance 2.0 Reference-to-Video
    `reference_audio` (voice/timbre reference). Seedance accepts an audio URL.
    """

    CATEGORY = "AtlasCloud/Utils"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("audio_url",)

    PLACEHOLDER = "(upload an audio file)"

    @classmethod
    def INPUT_TYPES(cls):
        # An EMPTY combo list makes ComfyUI's frontend fail to instantiate the
        # node ("can search it but can't add it"). Always keep at least one
        # placeholder entry so the node is addable even when the input dir has
        # no audio yet; the audio_upload control still lets the user upload one.
        auds = _input_audios() or [cls.PLACEHOLDER]
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT", {"tooltip": "Connect from AtlasCloud Client"}),
                "audio": (auds, {"audio_upload": True, "tooltip": "Upload reference audio (voice/timbre)"}),
            }
        }

    @classmethod
    def IS_CHANGED(cls, atlas_client=None, audio=None):
        try:
            import folder_paths
            d = folder_paths.get_input_directory()
            return f"{audio}:{os.path.getmtime(os.path.join(d, audio))}" if audio else "none"
        except Exception:
            return float("nan")

    def run(self, atlas_client: AtlasClientHandle, audio):
        import folder_paths
        d = folder_paths.get_input_directory()
        if not audio or audio == self.PLACEHOLDER:
            raise RuntimeError("请先用本节点的上传按钮上传一个音频文件")
        path = os.path.join(d, audio)
        if not os.path.isfile(path):
            raise RuntimeError(f"audio not found in input dir: {audio}")
        content = open(path, "rb").read()
        mime = _MIME.get(os.path.splitext(audio)[1].lower(), "audio/mpeg")
        up = atlas_client.client.upload_media_bytes(content, filename=audio, mime_type=mime)
        url = (up.get("download_url") or up.get("url") or "").strip()
        if not url:
            raise RuntimeError(f"uploadMedia returned no download_url: {up}")
        return (url,)


NODE_CLASS_MAPPINGS = {"AtlasCloud Upload Audio to Asset": AtlasUploadAudioToAsset}
NODE_DISPLAY_NAME_MAPPINGS = {"AtlasCloud Upload Audio to Asset": "AtlasCloud Upload Audio to Asset"}
