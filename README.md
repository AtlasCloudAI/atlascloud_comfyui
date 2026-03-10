# AtlasCloud_ComfyUI

AtlasCloud official custom nodes v1.0.0 for **ComfyUI**.
[AtlasCloud Website](https://atlascloud.ai/?utm_source=github&utm_medium=readme&utm_campaign=comfyui/)
With these nodes you can call AtlasCloud’s hosted models directly inside ComfyUI workflows.

---

## Requirements

-   **ComfyUI** (Desktop app or source install)

-   Python dependencies are handled by ComfyUI’s own environment (recommended)

-   An **AtlasCloud API Key** [AtlasCloud Website](https://atlascloud.ai/?utm_source=github&utm_medium=readme&utm_campaign=comfyui/)

> Tip: If you’re using **ComfyUI Desktop**, you should install dependencies into ComfyUI’s bundled venv (not your system Python).

---

## Installation

### Option A — ComfyUI Desktop (Recommended)

1. Quit ComfyUI Desktop completely.
2. Open a terminal and go to your ComfyUI custom nodes folder:

    ```bash
    cd ~/Documents/ComfyUI/custom_nodes
    ```

3. Clone the repo:
    ```
    git clone https://github.com/AtlascloudAI/atlascloud_comfyui.git
    ```
4. Install dependencies into ComfyUI Desktop venv:

    ```
    cd atlascloud_comfyui
    ~/Documents/ComfyUI/.venv/bin/python -m pip install -r requirements.txt
    ```

5. Launch ComfyUI Desktop again. You should see AtlasCloud nodes under:
   **Node Library → AtlasCloud**

### Option B — ComfyUI Source Installation (Recommended)

1. Go to your ComfyUI `custom_nodes` directory:
   `cd /path/to/ComfyUI/custom_nodes`

2. Clone the repo:
   `git clone https://github.com/AtlascloudAI/atlascloud_comfyui.git`
3. Install dependencies using the same Python environment you use to run ComfyUI:
    ```
    cd atlascloud_comfyui
    python -m pip install -r requirements.txt
    ```
4. Restart ComfyUI.

---

## Available Nodes

> Note: Some nodes are kept for **backward compatibility** even if their model id is no longer returned by AtlasCloud `/api/v1/models`. These nodes are marked as **Deprecated** and will raise an error at runtime unless you set `ATLAS_ALLOW_DEPRECATED_MODELS=1`.

### Common

-   **AtlasCloud Client** — Stores your API key and base URL for all AtlasCloud nodes.
-   **Image Previewer** — Preview generated images in ComfyUI.
-   **Video Previewer** — Preview generated videos in ComfyUI.

### Text-to-Video (T2V)

| Node | Model |
|------|-------|
| AtlasCloud VEO3 Text-to-Video | google/veo3 |
| AtlasCloud VEO3 Fast Text-to-Video | google/veo3-fast |
| AtlasCloud VEO3.1 Text-to-Video | google/veo3.1/text-to-video |
| AtlasCloud VEO3.1 Fast Text-to-Video | google/veo3.1-fast/text-to-video |
| AtlasCloud VEO2 Text-to-Video | google/veo2 |
| AtlasCloud WAN2.6 Text-to-Video | alibaba/wan-2.6/text-to-video |
| AtlasCloud WAN2.6 Video-to-Video | alibaba/wan-2.6/video-to-video |
| AtlasCloud Kling Video O3 Pro Text-to-Video | kwaivgi/kling-video-o3-pro/text-to-video |
| AtlasCloud Kling Video O3 Std Text-to-Video | kwaivgi/kling-video-o3-std/text-to-video |
| AtlasCloud WAN2.5 Text-to-Video | alibaba/wan-2.5/text-to-video |
| AtlasCloud WAN2.5 Text-to-Video Fast | alibaba/wan-2.5/text-to-video-fast |
| AtlasCloud Van-2.6 Text-to-Video | atlascloud/van-2.6/text-to-video |
| AtlasCloud Seedance V1 Pro Fast Text-to-Video | bytedance/seedance-v1-pro-fast/text-to-video |
| AtlasCloud Kling V2.1 T2V Master | kwaivgi/kling-v2.1-t2v-master |
| AtlasCloud Kling V2.0 T2V Master | kwaivgi/kling-v2.0-t2v-master |
| AtlasCloud WAN2.2 Text-to-Video 720p | alibaba/wan-2.2/text-to-video-720p |
| AtlasCloud WAN2.2 Text-to-Video 480p | alibaba/wan-2.2/t2v-480p |
| AtlasCloud Luma Ray 2 Text-to-Video | luma/ray-2-t2v |
| AtlasCloud Luma Ray 2 Flash Text-to-Video | luma/ray-2-flash-t2v |
| AtlasCloud Pika V2.2 Text-to-Video | pika/v2.2-t2v |
| AtlasCloud Pika V2.0 Turbo Text-to-Video | pika/v2.0-turbo-t2v |
| AtlasCloud PixVerse V4.5 Text-to-Video | pixverse/pixverse-v4.5-t2v |
| AtlasCloud Hailuo 02 T2V Pro | minimax/hailuo-02/t2v-pro |
| AtlasCloud Hailuo 02 T2V Standard | minimax/hailuo-02/t2v-standard |
| AtlasCloud Hailuo 02 Pro | minimax/hailuo-02/pro |
| AtlasCloud Hailuo 02 Fast | minimax/hailuo-02/fast |
| AtlasCloud Hailuo 2.3 Pro Text-to-Video | minimax/hailuo-2.3-pro/text-to-video |
| AtlasCloud Hailuo 2.3 T2V Standard | minimax/hailuo-2.3/t2v-standard |
| AtlasCloud Sora 2 Text-to-Video | openai/sora-2/text-to-video |
| AtlasCloud Sora 2 Text-to-Video Pro | openai/sora-2/text-to-video-pro |
| AtlasCloud Kling V3.0 Pro Text-to-Video | kwaivgi/kling-v3.0-pro/text-to-video |
| AtlasCloud Kling V3.0 Std Text-to-Video | kwaivgi/kling-v3.0-std/text-to-video |
| AtlasCloud Kling V2.6 Pro Text-to-Video | kwaivgi/kling-v2.6-pro/text-to-video |
| AtlasCloud Kling V2.6 Pro Avatar | kwaivgi/kling-v2.6-pro/avatar |
| AtlasCloud Kling V2.6 Std Avatar | kwaivgi/kling-v2.6-std/avatar |
| AtlasCloud Kling V2.6 Pro Motion-Control | kwaivgi/kling-v2.6-pro/motion-control |
| AtlasCloud Kling V2.6 Std Motion-Control | kwaivgi/kling-v2.6-std/motion-control |
| AtlasCloud Kling V2.5 Turbo Pro Text-to-Video | kwaivgi/kling-v2.5-turbo-pro/text-to-video |
| AtlasCloud Kling Video O1 Text-to-Video | kwaivgi/kling-video-o1/text-to-video |
| AtlasCloud Seedance V1 Pro Text-to-Video 1080p | bytedance/seedance-v1-pro/text-to-video-1080p |
| AtlasCloud Seedance V1 Pro Text-to-Video 720p | bytedance/seedance-v1-pro-t2v-720p |
| AtlasCloud Seedance V1 Pro Text-to-Video 480p | bytedance/seedance-v1-pro-t2v-480p |
| AtlasCloud Seedance V1 Lite Text-to-Video 480p | bytedance/seedance-v1-lite-t2v-480p |
| AtlasCloud Seedance V1 Lite T2V 1080p | bytedance/seedance-v1-lite-t2v-1080p |
| AtlasCloud Seedance V1 Lite T2V 720p | bytedance/seedance-v1-lite-t2v-720p |
| AtlasCloud Seedance V1.5 Pro Text-to-Video | bytedance/seedance-v1.5-pro/text-to-video |
| AtlasCloud Seedance V1.5 Pro Text-to-Video Fast | bytedance/seedance-v1.5-pro/text-to-video-fast |
| AtlasCloud Hunyuan Text-to-Video | atlascloud/hunyuan-video/t2v |

### Image-to-Video (I2V)

| Node | Model |
|------|-------|
| AtlasCloud VEO3 Image-to-Video | google/veo3/image-to-video |
| AtlasCloud VEO3 Fast Image-to-Video | google/veo3-fast/image-to-video |
| AtlasCloud VEO3.1 Fast Image-to-Video | google/veo3.1-fast/image-to-video |
| AtlasCloud VEO3.1 Reference-to-Video | google/veo3.1/reference-to-video |
| AtlasCloud VEO3.1 Image-to-Video | google/veo3.1/image-to-video |
| AtlasCloud VEO2 Image-to-Video | google/veo2/image-to-video |
| AtlasCloud WAN2.5 Image-to-Video | alibaba/wan-2.5/image-to-video |
| AtlasCloud WAN2.5 Image-to-Video Fast | alibaba/wan-2.5/image-to-video-fast |
| AtlasCloud Van-2.5 Text-to-Video | atlascloud/van-2.5/text-to-video |
| AtlasCloud Van-2.5 Image-to-Video | atlascloud/van-2.5/image-to-video |
| AtlasCloud Kling V2.1 I2V Standard | kwaivgi/kling-v2.1-i2v-standard |
| AtlasCloud WAN2.2 Animate Mix | alibaba/wan-2.2/animate-mix |
| AtlasCloud WAN2.2 Animate Move | alibaba/wan-2.2/animate-move |
| AtlasCloud WAN2.2 Image-to-Video 720p | alibaba/wan-2.2/i2v-720p |
| AtlasCloud WAN2.2 Image-to-Video 480p | alibaba/wan-2.2/i2v-480p |
| AtlasCloud Van-2.6 Image-to-Video | atlascloud/van-2.6/image-to-video |
| AtlasCloud Seedance V1 Pro Fast Image-to-Video | bytedance/seedance-v1-pro-fast/image-to-video |
| AtlasCloud Seedance V1 Pro I2V 1080p | bytedance/seedance-v1-pro-i2v-1080p |
| AtlasCloud Seedance V1 Pro I2V 720p | bytedance/seedance-v1-pro-i2v-720p |
| AtlasCloud Seedance V1 Pro I2V 480p | bytedance/seedance-v1-pro-i2v-480p |
| AtlasCloud Vidu Reference-to-Video Q1 | vidu/reference-to-video-q1 |
| AtlasCloud Vidu Reference-to-Video 2.0 | vidu/reference-to-video-2.0 |
| AtlasCloud Vidu Start-End-to-Video 2.0 | vidu/start-end-to-video-2.0 |
| AtlasCloud Kling V2.0 I2V Master | kwaivgi/kling-v2.0-i2v-master |
| AtlasCloud Kling V2.1 I2V Master | kwaivgi/kling-v2.1-i2v-master |
| AtlasCloud Kling V2.1 I2V Pro (Start/End Frame) | kwaivgi/kling-v2.1-i2v-pro/start-end-frame |
| AtlasCloud Kling V2.1 I2V Pro | kwaivgi/kling-v2.1-i2v-pro |
| AtlasCloud Kling V1.6 Multi I2V Pro | kwaivgi/kling-v1.6-multi-i2v-pro |
| AtlasCloud Kling V1.6 Multi I2V Standard | kwaivgi/kling-v1.6-multi-i2v-standard |
| AtlasCloud Kling V1.6 I2V Pro | kwaivgi/kling-v1.6-i2v-pro |
| AtlasCloud Kling V1.6 I2V Standard | kwaivgi/kling-v1.6-i2v-standard |
| AtlasCloud Kling Effects | kwaivgi/kling-effects |
| AtlasCloud WAN2.6 Image-to-Video | alibaba/wan-2.6/image-to-video |
| AtlasCloud WAN2.6 Image-to-Video Flash | alibaba/wan-2.6/image-to-video-flash |
| AtlasCloud Kling Video O3 Pro Image-to-Video | kwaivgi/kling-video-o3-pro/image-to-video |
| AtlasCloud Kling Video O3 Std Image-to-Video | kwaivgi/kling-video-o3-std/image-to-video |
| AtlasCloud Kling Video O3 Pro Reference-to-Video | kwaivgi/kling-video-o3-pro/reference-to-video |
| AtlasCloud Kling Video O3 Std Reference-to-Video | kwaivgi/kling-video-o3-std/reference-to-video |
| AtlasCloud Luma Ray 2 Image-to-Video | luma/ray-2-i2v |
| AtlasCloud Pika V2.1 Image-to-Video | pika/v2.1-i2v |
| AtlasCloud PixVerse V4.5 Image-to-Video | pixverse/pixverse-v4.5-i2v |
| AtlasCloud Hailuo 02 I2V Pro | minimax/hailuo-02/i2v-pro |
| AtlasCloud Hailuo 02 I2V Standard | minimax/hailuo-02/i2v-standard |
| AtlasCloud Hailuo 02 Standard | minimax/hailuo-02/standard |
| AtlasCloud Hailuo 2.3 I2V Standard | minimax/hailuo-2.3/i2v-standard |
| AtlasCloud Hailuo 2.3 I2V Pro | minimax/hailuo-2.3/i2v-pro |
| AtlasCloud Hailuo 2.3 Fast | minimax/hailuo-2.3/fast |
| AtlasCloud Sora 2 Image-to-Video | openai/sora-2/image-to-video |
| AtlasCloud Sora 2 Image-to-Video Pro | openai/sora-2/image-to-video-pro |
| AtlasCloud Kling V3.0 Pro Image-to-Video | kwaivgi/kling-v3.0-pro/image-to-video |
| AtlasCloud Kling V3.0 Std Image-to-Video | kwaivgi/kling-v3.0-std/image-to-video |
| AtlasCloud Kling V2.6 Pro Image-to-Video | kwaivgi/kling-v2.6-pro/image-to-video |
| AtlasCloud Kling Video O1 Image-to-Video | kwaivgi/kling-video-o1/image-to-video |
| AtlasCloud Seedance V1.5 Pro Image-to-Video | bytedance/seedance-v1.5-pro/image-to-video |
| AtlasCloud Seedance V1 Lite I2V 1080p | bytedance/seedance-v1-lite-i2v-1080p |
| AtlasCloud Seedance V1 Lite I2V 720p | bytedance/seedance-v1-lite-i2v-720p |
| AtlasCloud Seedance V1 Lite I2V 480p | bytedance/seedance-v1-lite-i2v-480p |
| AtlasCloud Seedance V1.5 Pro Image-to-Video Fast | bytedance/seedance-v1.5-pro/image-to-video-fast |
| AtlasCloud Kling V2.5 Turbo Pro Image-to-Video | kwaivgi/kling-v2.5-turbo-pro/image-to-video |
| AtlasCloud Vidu Q3 Text-to-Video | vidu/q3/text-to-video |
| AtlasCloud Vidu Q3-Pro Text-to-Video | vidu/q3-pro/text-to-video |
| AtlasCloud Vidu Q3 Image-to-Video | vidu/image-to-video-2.0 |
| AtlasCloud Vidu Q3 Image-to-Video (Q3 API) | vidu/q3/image-to-video |
| AtlasCloud Vidu Q3-Pro Image-to-Video | vidu/q3-pro/image-to-video |
| AtlasCloud WAN2.2 Spicy Image-to-Video | alibaba/wan-2.2-spicy/image-to-video |
| AtlasCloud WAN2.2 Spicy Image-to-Video LoRA | alibaba/wan-2.2-spicy/image-to-video-lora |
| AtlasCloud Hunyuan Image-to-Video | atlascloud/hunyuan-video/i2v |

### Text-to-Image (T2I)

| Node | Model |
|------|-------|
| AtlasCloud WAN2.6 Text-to-Image | alibaba/wan-2.6/text-to-image |
| AtlasCloud WAN2.5 Text-to-Image | alibaba/wan-2.5/text-to-image |
| AtlasCloud Imagen4 Text-to-Image | google/imagen4 |
| AtlasCloud Imagen4 Fast Text-to-Image | google/imagen4-fast |
| AtlasCloud Imagen4 Ultra Text-to-Image | google/imagen4-ultra |
| AtlasCloud Imagen3 Text-to-Image | google/imagen3 |
| AtlasCloud Imagen3 Fast Text-to-Image | google/imagen3-fast |
| AtlasCloud Nano Banana 2 Text-to-Image | google/nano-banana-2/text-to-image |
| AtlasCloud Nano Banana 2 Text-to-Image Developer | google/nano-banana-2/text-to-image-developer |
| AtlasCloud Nano Banana Pro Text-to-Image Ultra | google/nano-banana-pro/text-to-image-ultra |
| AtlasCloud Nano Banana Pro Text-to-Image | google/nano-banana-pro/text-to-image |
| AtlasCloud Nano Banana Pro Text-to-Image Developer | google/nano-banana-pro/text-to-image-developer |
| AtlasCloud Nano Banana Text-to-Image | google/nano-banana/text-to-image |
| AtlasCloud Nano Banana Text-to-Image Developer | google/nano-banana/text-to-image-developer |
| AtlasCloud Seedream V5.0 Lite Text-to-Image | bytedance/seedream-v5.0-lite |
| AtlasCloud Seedream V5.0 Lite Sequential Text-to-Image | bytedance/seedream-v5.0-lite/sequential |
| AtlasCloud Seedream V4 Text-to-Image | bytedance/seedream-v4 |
| AtlasCloud Seedream V4 Sequential Text-to-Image | bytedance/seedream-v4/sequential |
| AtlasCloud Seedream V4.5 Text-to-Image | bytedance/seedream-v4.5 |
| AtlasCloud Seedream V4.5 Sequential Text-to-Image | bytedance/seedream-v4.5/sequential |
| AtlasCloud ZImage Turbo Text-to-Image | z-image/turbo |
| AtlasCloud Ideogram V3 Quality Text-to-Image | ideogram-ai/ideogram-v3-quality |
| AtlasCloud Ideogram V3 Turbo Text-to-Image | ideogram-ai/ideogram-v3-turbo |
| AtlasCloud Luma Photon Text-to-Image | luma/photon |
| AtlasCloud Luma Photon Flash Text-to-Image | luma/photon-flash |
| AtlasCloud Recraft V3 Text-to-Image | recraft-ai/recraft-v3 |
| AtlasCloud Flux2 Flex Text-to-Image | flux2/flex |
| AtlasCloud Flux Dev Text-to-Image | black-forest-labs/flux-dev |
| AtlasCloud Flux Dev LoRA Text-to-Image | black-forest-labs/flux-dev-lora |
| AtlasCloud Flux Schnell Text-to-Image | black-forest-labs/flux-schnell |
| AtlasCloud ZImage Turbo Lora Text-to-Image | z-image/turbo-lora |
| AtlasCloud Qwen Image Text-to-Image Plus | alibaba/qwen-image/text-to-image-plus |
| AtlasCloud Qwen Image Text-to-Image Max | alibaba/qwen-image/text-to-image-max |

### Video Edit

| Node | Model |
|------|-------|
| AtlasCloud Kling Video O3 Pro Video-Edit | kwaivgi/kling-video-o3-pro/video-edit |
| AtlasCloud Kling Video O3 Std Video-Edit | kwaivgi/kling-video-o3-std/video-edit |

### Image Edit

| Node | Model |
|------|-------|
| AtlasCloud Nano Banana 2 Edit | google/nano-banana-2/edit |
| AtlasCloud Nano Banana 2 Edit Developer | google/nano-banana-2/edit-developer |
| AtlasCloud Seedream V5.0 Lite Edit | bytedance/seedream-v5.0-lite/edit |
| AtlasCloud Seedream V5.0 Lite Edit Sequential | bytedance/seedream-v5.0-lite/edit-sequential |
| AtlasCloud WAN2.6 Image-Edit | alibaba/wan-2.6/image-edit |
| AtlasCloud WAN2.5 Image-Edit | alibaba/wan-2.5/image-edit |
| AtlasCloud Seedream V4 Edit | bytedance/seedream-v4/edit |
| AtlasCloud Seedream V4 Edit Sequential | bytedance/seedream-v4/edit-sequential |
| AtlasCloud Seedream V4.5 Edit | bytedance/seedream-v4.5/edit |
| AtlasCloud Seedream V4.5 Edit Sequential | bytedance/seedream-v4.5/edit-sequential |
| AtlasCloud Qwen Image Edit | atlascloud/qwen-image/edit |
| AtlasCloud Qwen Image Edit (Alibaba) | alibaba/qwen-image/edit |
| AtlasCloud Qwen Image Edit Plus (Alibaba) | alibaba/qwen-image/edit-plus |
| AtlasCloud Nano Banana Pro Edit | google/nano-banana-pro/edit |
| AtlasCloud Nano Banana Pro Edit Developer | google/nano-banana-pro/edit-developer |
| AtlasCloud Nano Banana Edit | google/nano-banana/edit |
| AtlasCloud Nano Banana Edit Developer | google/nano-banana/edit-developer |
| AtlasCloud Flux Kontext Dev Edit | black-forest-labs/flux-kontext-dev |
| AtlasCloud Flux Kontext Dev LoRA Edit | black-forest-labs/flux-kontext-dev-lora |
| AtlasCloud Qwen Image Edit Plus 20251215 | alibaba/qwen-image/edit-plus-20251215 |

> Nodes are continuously expanded as new models are added to AtlasCloud.

---

## Troubleshooting

### Nodes not showing up

-   Make sure the repo is placed under:

    -   `ComfyUI/custom_nodes/atlascloud_comfyui`

-   Restart ComfyUI completely (quit and reopen for Desktop).

-   Check logs for import errors:

    -   macOS (Desktop): ~/Library/Logs/ComfyUI/comfyui.log

### Dependency / module not found

Install dependencies into the same Python ComfyUI uses.

-   Desktop default venv:
    ```
    ~/Documents/ComfyUI/.venv/bin/python -m pip install -r requirements.txt
    ```

### API request fails

-   Verify your API key is valid.

-   Check network access and firewall/proxy restrictions.

-   If the API returns an error message, it will appear in the ComfyUI console/log.

---

## Support

GitHub Issues: use the repo Issues page to report bugs and request features.

Please include:

-   your ComfyUI version

-   OS and hardware

-   the model node you used

-   the error traceback from logs

---

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Deprecated / Legacy Models

| Model id | Status |
|---|---|
| `atlascloud/hunyuan-video/i2v` | Deprecated (not in `/api/v1/models`) |
| `atlascloud/hunyuan-video/t2v` | Deprecated (not in `/api/v1/models`) |
| `black-forest-labs/flux-2-flex/text-to-image` | Deprecated (not in `/api/v1/models`) |
| `google/nano-banana-pro/text-to-image-ultra` | Deprecated (not in `/api/v1/models`) |
| `ideogram-ai/ideogram-v3-quality` | Deprecated (not in `/api/v1/models`) |
| `ideogram-ai/ideogram-v3-turbo` | Deprecated (not in `/api/v1/models`) |
| `luma/photon` | Deprecated (not in `/api/v1/models`) |
| `luma/photon-flash` | Deprecated (not in `/api/v1/models`) |
| `luma/ray-2-flash-t2v` | Deprecated (not in `/api/v1/models`) |
| `luma/ray-2-i2v` | Deprecated (not in `/api/v1/models`) |
| `luma/ray-2-t2v` | Deprecated (not in `/api/v1/models`) |
| `openai/sora-2/image-to-video` | Deprecated (not in `/api/v1/models`) |
| `openai/sora-2/image-to-video-pro` | Deprecated (not in `/api/v1/models`) |
| `openai/sora-2/text-to-video` | Deprecated (not in `/api/v1/models`) |
| `openai/sora-2/text-to-video-pro` | Deprecated (not in `/api/v1/models`) |
| `pika/v2.0-turbo-t2v` | Deprecated (not in `/api/v1/models`) |
| `pika/v2.1-i2v` | Deprecated (not in `/api/v1/models`) |
| `pika/v2.2-t2v` | Deprecated (not in `/api/v1/models`) |
| `pixverse/pixverse-v4.5-i2v` | Deprecated (not in `/api/v1/models`) |
| `pixverse/pixverse-v4.5-t2v` | Deprecated (not in `/api/v1/models`) |
| `recraft-ai/recraft-v3` | Deprecated (not in `/api/v1/models`) |
| `z-image/turbo-lora` | Deprecated (not in `/api/v1/models`) |
