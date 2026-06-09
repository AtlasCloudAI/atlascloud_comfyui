from __future__ import annotations

import io
import wave

from atlascloud_comfyui.nodes.auth.atlas_client_node import AtlasClientHandle


def _audio_to_wav_bytes(audio) -> bytes:
    """ComfyUI AUDIO ({waveform:[B,C,T] float tensor, sample_rate:int}) -> wav bytes.
    Uses stdlib wave + numpy only (no torchaudio dependency)."""
    import numpy as np

    waveform = audio["waveform"]
    sr = int(audio["sample_rate"])
    arr = waveform[0].detach().cpu().numpy()  # [C, T]
    if arr.ndim == 1:
        arr = arr[None, :]
    arr = np.clip(arr, -1.0, 1.0)
    pcm = (arr * 32767.0).astype(np.int16)        # [C, T]
    interleaved = pcm.T.reshape(-1)               # [T, C] -> flat
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(arr.shape[0])
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(interleaved.tobytes())
    return buf.getvalue()


class AtlasUploadAudioToAsset:
    """Upload a reference audio (voice/timbre) to AtlasCloud and return its URL,
    ready for Seedance 2.0 Reference-to-Video `reference_audio`.

    IMPORTANT: takes an AUDIO input (connect a core **Load Audio** node), NOT a
    built-in `audio_upload` widget. The frontend's audio_upload control attaches
    an `audioUI` preview widget whose `updateUIWidget` crashes on custom nodes
    ("Cannot read properties of undefined (reading 'element')"), making the node
    un-instantiable. Using Load Audio for the upload UI avoids that entirely and
    is rock solid (it's a core node).
    """

    CATEGORY = "AtlasCloud/Utils"
    FUNCTION = "run"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("audio_url",)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "atlas_client": ("ATLAS_CLIENT", {"tooltip": "Connect from AtlasCloud Client"}),
                "audio": ("AUDIO", {"tooltip": "Connect a core 'Load Audio' node (which has the upload button)"}),
            }
        }

    def run(self, atlas_client: AtlasClientHandle, audio):
        if not audio or "waveform" not in audio:
            raise RuntimeError("Connect a Load Audio node to the `audio` input")
        content = _audio_to_wav_bytes(audio)
        up = atlas_client.client.upload_media_bytes(content, filename="ref_audio.wav", mime_type="audio/wav")
        url = (up.get("download_url") or up.get("url") or "").strip()
        if not url:
            raise RuntimeError(f"uploadMedia returned no download_url: {up}")
        return (url,)


NODE_CLASS_MAPPINGS = {"AtlasCloud Upload Audio to Asset": AtlasUploadAudioToAsset}
NODE_DISPLAY_NAME_MAPPINGS = {"AtlasCloud Upload Audio to Asset": "AtlasCloud Upload Audio to Asset"}
