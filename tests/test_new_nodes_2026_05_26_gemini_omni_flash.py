"""Lightweight tests for Gemini Omni Flash developer video nodes.

These tests MUST NOT require ATLASCLOUD_API_KEY.
"""

from src.atlascloud_comfyui.nodes.auth.atlas_client_node import AtlasClientHandle
from src.atlascloud_comfyui.nodes.video.google_gemini_omni_flash_i2v_dev import (
    AtlasGeminiOmniFlashDeveloperImageToVideo,
)
from src.atlascloud_comfyui.nodes.video.google_gemini_omni_flash_t2v_dev import (
    AtlasGeminiOmniFlashDeveloperTextToVideo,
)


class _FakeClient:
    def __init__(self):
        self.payload = None
        self.prediction_id = "pred_test_123"

    def generate_video(self, payload):
        self.payload = payload
        return self.prediction_id

    def poll_prediction(self, prediction_id, **_kwargs):
        assert prediction_id == self.prediction_id
        return {"data": {"outputs": ["https://example.com/video.mp4"]}}


def test_gemini_omni_flash_t2v_node_metadata():
    required = AtlasGeminiOmniFlashDeveloperTextToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "prompt" in required
    assert AtlasGeminiOmniFlashDeveloperTextToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_gemini_omni_flash_i2v_node_metadata():
    required = AtlasGeminiOmniFlashDeveloperImageToVideo.INPUT_TYPES()["required"]
    assert "atlas_client" in required
    assert "image" in required
    assert "prompt" in required
    assert AtlasGeminiOmniFlashDeveloperImageToVideo.RETURN_TYPES == ("STRING", "STRING")


def test_gemini_omni_flash_t2v_payload():
    client = _FakeClient()
    node = AtlasGeminiOmniFlashDeveloperTextToVideo()

    video_url, prediction_id = node.run(
        atlas_client=AtlasClientHandle(client=client),
        prompt="make a deer come alive",
        duration=10,
        aspect_ratio="16:9",
        resolution="720p",
        seed=-1,
    )

    assert video_url == "https://example.com/video.mp4"
    assert prediction_id == "pred_test_123"
    assert client.payload == {
        "model": "google/gemini-omni-flash/text-to-video-developer",
        "prompt": "make a deer come alive",
        "duration": 10,
        "aspect_ratio": "16:9",
        "resolution": "720p",
    }


def test_gemini_omni_flash_i2v_payload():
    client = _FakeClient()
    node = AtlasGeminiOmniFlashDeveloperImageToVideo()

    video_url, prediction_id = node.run(
        atlas_client=AtlasClientHandle(client=client),
        image="https://static.atlascloud.ai/demo.jpg",
        prompt="kick the ball into the net",
        duration=6,
        aspect_ratio="16:9",
        resolution="4k",
        seed=7,
    )

    assert video_url == "https://example.com/video.mp4"
    assert prediction_id == "pred_test_123"
    assert client.payload == {
        "model": "google/gemini-omni-flash/image-to-video-developer",
        "images": ["https://static.atlascloud.ai/demo.jpg"],
        "prompt": "kick the ball into the net",
        "duration": 6,
        "aspect_ratio": "16:9",
        "resolution": "4k",
        "seed": 7,
    }


def test_gemini_omni_flash_nodes_registered():
    from src.atlascloud_comfyui.registry import NODE_CLASS_MAPPINGS

    assert "AtlasCloud Gemini Omni Flash Developer Text-to-Video" in NODE_CLASS_MAPPINGS
    assert "AtlasCloud Gemini Omni Flash Developer Image-to-Video" in NODE_CLASS_MAPPINGS
