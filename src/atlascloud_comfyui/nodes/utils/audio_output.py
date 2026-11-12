from __future__ import annotations

import io
import urllib.request
from typing import Any, Dict, List, Tuple

from ..auth.atlas_client_node import AtlasClientHandle

SEED_INPUT = (
    "INT",
    {
        "default": 0,
        "min": 0,
        "max": 0xFFFFFFFFFFFFFFFF,
        "control_after_generate": True,
        "tooltip": "Change to run the node again (not sent to the API)",
    },
)


def generate_audio_outputs(
    atlas_client: AtlasClientHandle,
    payload: Dict[str, Any],
    *,
    poll_interval_sec: float,
    timeout_sec: int,
) -> Tuple[List[Any], str]:
    client = atlas_client.client
    prediction_id = client.generate_audio(payload)
    result = client.poll_prediction(
        prediction_id,
        poll_interval_sec=float(poll_interval_sec),
        timeout_sec=float(timeout_sec),
    )

    outputs = (result.get("data") or {}).get("outputs") or []
    if not outputs:
        raise RuntimeError(f"No outputs returned for prediction {prediction_id}: {result}")
    return outputs, prediction_id


def decode_audio_bytes(data: bytes) -> Dict[str, Any]:
    """Encoded audio file bytes -> ComfyUI AUDIO ({waveform: [1, C, T] float32, sample_rate: int})."""
    import av
    import numpy as np
    import torch

    with av.open(io.BytesIO(data)) as container:
        if not container.streams.audio:
            raise RuntimeError("Downloaded file has no audio stream")
        stream = container.streams.audio[0]
        resampler = av.AudioResampler(format="fltp", layout=stream.layout, rate=stream.rate)
        chunks = []
        for frame in container.decode(stream):
            chunks.extend(f.to_ndarray() for f in resampler.resample(frame))
        chunks.extend(f.to_ndarray() for f in resampler.resample(None))
        sample_rate = stream.rate

    if not chunks:
        raise RuntimeError("No audio frames decoded")
    waveform = torch.from_numpy(np.concatenate(chunks, axis=1)).unsqueeze(0)
    return {"waveform": waveform, "sample_rate": sample_rate}


def load_audio_url(url: str, timeout_sec: int = 120) -> Dict[str, Any]:
    req = urllib.request.Request(url, headers={"User-Agent": "atlascloud-comfyui/1.0"})
    with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
        return decode_audio_bytes(resp.read())
