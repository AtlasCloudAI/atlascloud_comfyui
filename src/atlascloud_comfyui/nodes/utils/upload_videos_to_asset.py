from __future__ import annotations

import os

from atlascloud_comfyui.nodes.auth.atlas_client_node import AtlasClientHandle

_VIDEO_EXTS = (".mp4", ".mov", ".webm", ".avi", ".mkv", ".m4v")
_MIME = {".mp4": "video/mp4", ".mov": "video/quicktime", ".webm": "video/webm",
         ".avi": "video/x-msvideo", ".mkv": "video/x-matroska", ".m4v": "video/mp4"}


def _input_videos():
    try:
        import folder_paths
        d = folder_paths.get_input_directory()
        return sorted([f for f in os.listdir(d) if f.lower().endswith(_VIDEO_EXTS)])
    except Exception:
        return []


class AtlasUploadVideosToAsset:
    """Upload up to 4 LOCAL video files (with the ComfyUI upload button) and
    return them as a newline-separated list of public URLs — ready to wire into
    Seedance 2.0 Reference-to-Video `reference_videos` (or any video-URL field).

    Each video_N slot has a video upload control: click to upload a local file,
    it lands in ComfyUI/input, then this node uploads it to AtlasCloud and emits
    the download URL. (Seedance accepts video URLs directly.)
    """

    CATEGORY = "AtlasCloud/Utils"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING", "INT")
    RETURN_NAMES = ("video_urls", "count")
    MAX = 4

    NONE = "(none)"

    PLACEHOLDER = "(upload a video file)"

    @classmethod
    def INPUT_TYPES(cls):
        vids = _input_videos()
        # EMPTY combo => frontend can't instantiate the node. Keep a placeholder
        # for the required slot so it stays addable even with no videos yet.
        required = {
            "atlas_client": ("ATLAS_CLIENT", {"tooltip": "Connect from AtlasCloud Client"}),
            "video_1": (vids or [cls.PLACEHOLDER], {"video_upload": True, "tooltip": "Upload reference video 1"}),
        }
        # optional slots default to "(none)" so they are skipped unless a file is picked
        optional = {f"video_{i}": ([cls.NONE] + vids, {"video_upload": True, "tooltip": f"Upload reference video {i} (optional)"})
                    for i in range(2, cls.MAX + 1)}
        return {"required": required, "optional": optional}

    @classmethod
    def IS_CHANGED(cls, atlas_client=None, video_1=None, **kw):
        # Re-run when any selected file changes (by mtime).
        try:
            import folder_paths
            d = folder_paths.get_input_directory()
            sig = []
            for nm in [video_1] + [kw.get(f"video_{i}") for i in range(2, cls.MAX + 1)]:
                if nm:
                    try:
                        sig.append(f"{nm}:{os.path.getmtime(os.path.join(d, nm))}")
                    except Exception:
                        sig.append(str(nm))
            return ";".join(sig)
        except Exception:
            return float("nan")

    def run(self, atlas_client: AtlasClientHandle, video_1, **kwargs):
        import folder_paths
        d = folder_paths.get_input_directory()
        client = atlas_client.client
        names = [video_1] + [kwargs.get(f"video_{i}") for i in range(2, self.MAX + 1)]
        urls = []
        for nm in names:
            if not nm or nm == self.NONE or nm == self.PLACEHOLDER:
                continue
            path = os.path.join(d, nm)
            if not os.path.isfile(path):
                raise RuntimeError(f"video not found in input dir: {nm}")
            content = open(path, "rb").read()
            mime = _MIME.get(os.path.splitext(nm)[1].lower(), "video/mp4")
            up = client.upload_media_bytes(content, filename=nm, mime_type=mime)
            url = (up.get("download_url") or up.get("url") or "").strip()
            if not url:
                raise RuntimeError(f"uploadMedia returned no download_url: {up}")
            urls.append(url)
        if not urls:
            raise RuntimeError("Upload at least one video")
        return ("\n".join(urls), len(urls))


NODE_CLASS_MAPPINGS = {"AtlasCloud Upload Videos to Asset": AtlasUploadVideosToAsset}
NODE_DISPLAY_NAME_MAPPINGS = {"AtlasCloud Upload Videos to Asset": "AtlasCloud Upload Videos to Asset"}
