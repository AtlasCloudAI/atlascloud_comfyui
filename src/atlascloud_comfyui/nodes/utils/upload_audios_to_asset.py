from __future__ import annotations

import os

from atlascloud_comfyui.nodes.auth.atlas_client_node import AtlasClientHandle

_AUDIO_EXTS = (".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac")
_MIME = {
    ".mp3": "audio/mpeg", ".wav": "audio/wav", ".m4a": "audio/mp4",
    ".aac": "audio/aac", ".ogg": "audio/ogg", ".flac": "audio/flac",
}


def _input_audios():
    try:
        import folder_paths
        d = folder_paths.get_input_directory()
        return sorted([f for f in os.listdir(d) if f.lower().endswith(_AUDIO_EXTS)])
    except Exception:
        return []


class AtlasUploadAudiosToAsset:
    """Upload up to 3 LOCAL audio files and return them as a newline-separated
    list of public URLs — ready to wire into Seedance 2.0 Reference-to-Video
    `reference_audios` for multi-character voice cloning (up to 3 voices).

    Each audio_N slot supports file upload (mp3/wav). Files land in ComfyUI/input,
    then get uploaded to AtlasCloud and the download URLs are emitted.
    """

    CATEGORY = "AtlasCloud/Utils"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "INT")
    RETURN_NAMES = ("audio_urls", "count")
    MAX = 3

    NONE = "(none)"
    PLACEHOLDER = "(upload an audio file)"

    @classmethod
    def INPUT_TYPES(cls):
        auds = _input_audios()
        required = {
            "atlas_client": ("ATLAS_CLIENT", {"tooltip": "Connect from AtlasCloud Client"}),
            "audio_1": (auds or [cls.PLACEHOLDER], {"audio_upload": True, "tooltip": "Upload reference audio 1 (voice clone source)"}),
        }
        optional = {
            f"audio_{i}": ([cls.NONE] + auds, {"audio_upload": True, "tooltip": f"Upload reference audio {i} (optional)"})
            for i in range(2, cls.MAX + 1)
        }
        return {"required": required, "optional": optional}

    @classmethod
    def IS_CHANGED(cls, atlas_client=None, audio_1=None, **kw):
        try:
            import folder_paths
            d = folder_paths.get_input_directory()
            sig = []
            for nm in [audio_1] + [kw.get(f"audio_{i}") for i in range(2, cls.MAX + 1)]:
                if nm:
                    try:
                        sig.append(f"{nm}:{os.path.getmtime(os.path.join(d, nm))}")
                    except Exception:
                        sig.append(str(nm))
            return ";".join(sig)
        except Exception:
            return float("nan")

    def run(self, atlas_client: AtlasClientHandle, audio_1, **kwargs):
        import folder_paths
        d = folder_paths.get_input_directory()
        client = atlas_client.client
        names = [audio_1] + [kwargs.get(f"audio_{i}") for i in range(2, self.MAX + 1)]
        urls = []
        for nm in names:
            if not nm or nm == self.NONE or nm == self.PLACEHOLDER:
                continue
            path = os.path.join(d, nm)
            if not os.path.isfile(path):
                raise RuntimeError(f"audio not found in input dir: {nm}")
            content = open(path, "rb").read()
            mime = _MIME.get(os.path.splitext(nm)[1].lower(), "audio/mpeg")
            up = client.upload_media_bytes(content, filename=nm, mime_type=mime)
            url = (up.get("download_url") or up.get("url") or "").strip()
            if not url:
                raise RuntimeError(f"uploadMedia returned no download_url: {up}")
            urls.append(url)
        if not urls:
            raise RuntimeError("Upload at least one audio file")
        return ("\n".join(urls), len(urls))


NODE_CLASS_MAPPINGS = {"AtlasCloud Upload Audios to Asset": AtlasUploadAudiosToAsset}
NODE_DISPLAY_NAME_MAPPINGS = {"AtlasCloud Upload Audios to Asset": "AtlasCloud Upload Audios to Asset"}
