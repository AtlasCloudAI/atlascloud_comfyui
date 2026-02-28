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
| AtlasCloud VEO2 Text-to-Video | google/veo2 |
| AtlasCloud WAN2.6 Text-to-Video | alibaba/wan-2.6/text-to-video |
| AtlasCloud WAN2.5 Text-to-Video | alibaba/wan-2.5/text-to-video |
| AtlasCloud WAN2.2 Text-to-Video 720p | alibaba/wan-2.2/text-to-video-720p |
| AtlasCloud Luma Ray 2 Text-to-Video | luma/ray-2-t2v |
| AtlasCloud Luma Ray 2 Flash Text-to-Video | luma/ray-2-flash-t2v |
| AtlasCloud Pika V2.2 Text-to-Video | pika/v2.2-t2v |
| AtlasCloud Pika V2.0 Turbo Text-to-Video | pika/v2.0-turbo-t2v |
| AtlasCloud PixVerse V4.5 Text-to-Video | pixverse/pixverse-v4.5-t2v |
| AtlasCloud Hailuo 02 T2V Pro | minimax/hailuo-02/t2v-pro |
| AtlasCloud Hailuo 2.3 Pro Text-to-Video | minimax/hailuo-2.3-pro/text-to-video |
| AtlasCloud Sora 2 Text-to-Video | openai/sora-2/text-to-video |
| AtlasCloud Sora 2 Text-to-Video Pro | openai/sora-2/text-to-video-pro |
| AtlasCloud Kling V3.0 Pro Text-to-Video | kwaivgi/kling-v3.0-pro/text-to-video |
| AtlasCloud Kling V3.0 Std Text-to-Video | kwaivgi/kling-v3.0-std/text-to-video |
| AtlasCloud Kling V2.6 Pro Text-to-Video | kwaivgi/kling-v2.6-pro/text-to-video |
| AtlasCloud Kling V2.5 Turbo Pro Text-to-Video | kwaivgi/kling-v2.5-turbo-pro/text-to-video |
| AtlasCloud Kling Video O1 Text-to-Video | kwaivgi/kling-video-o1/text-to-video |
| AtlasCloud Seedance V1 Pro Text-to-Video 1080p | bytedance/seedance-v1-pro/text-to-video-1080p |
| AtlasCloud Seedance V1.5 Pro Text-to-Video | bytedance/seedance-v1.5-pro/text-to-video |
| AtlasCloud Hunyuan Text-to-Video | atlascloud/hunyuan-video/t2v |

### Image-to-Video (I2V)

| Node | Model |
|------|-------|
| AtlasCloud VEO3 Image-to-Video | google/veo3/image-to-video |
| AtlasCloud VEO3.1 Image-to-Video | google/veo3.1/image-to-video |
| AtlasCloud VEO2 Image-to-Video | google/veo2/image-to-video |
| AtlasCloud WAN2.5 Image-to-Video | alibaba/wan-2.5/image-to-video |
| AtlasCloud Luma Ray 2 Image-to-Video | luma/ray-2-i2v |
| AtlasCloud Pika V2.1 Image-to-Video | pika/v2.1-i2v |
| AtlasCloud PixVerse V4.5 Image-to-Video | pixverse/pixverse-v4.5-i2v |
| AtlasCloud Hailuo 02 I2V Pro | minimax/hailuo-02/i2v-pro |
| AtlasCloud Sora 2 Image-to-Video | openai/sora-2/image-to-video |
| AtlasCloud Sora 2 Image-to-Video Pro | openai/sora-2/image-to-video-pro |
| AtlasCloud Kling V3.0 Pro Image-to-Video | kwaivgi/kling-v3.0-pro/image-to-video |
| AtlasCloud Kling V3.0 Std Image-to-Video | kwaivgi/kling-v3.0-std/image-to-video |
| AtlasCloud Kling V2.5 Turbo Pro Image-to-Video | kwaivgi/kling-v2.5-turbo-pro/image-to-video |
| AtlasCloud Vidu Q3 Image-to-Video | vidu/image-to-video-2.0 |
| AtlasCloud Hunyuan Image-to-Video | atlascloud/hunyuan-video/i2v |

### Text-to-Image (T2I)

| Node | Model |
|------|-------|
| AtlasCloud Imagen4 Text-to-Image | google/imagen4 |
| AtlasCloud Imagen4 Fast Text-to-Image | google/imagen4-fast |
| AtlasCloud Imagen4 Ultra Text-to-Image | google/imagen4-ultra |
| AtlasCloud Imagen3 Text-to-Image | google/imagen3 |
| AtlasCloud Nano Banana 2 Text-to-Image | google/nano-banana-2/text-to-image |
| AtlasCloud Nano Banana 2 Text-to-Image Developer | google/nano-banana-2/text-to-image-developer |
| AtlasCloud Nano Banana Pro Text-to-Image Ultra | google/nano-banana-pro/text-to-image-ultra |
| AtlasCloud Seedream V5.0 Lite Text-to-Image | bytedance/seedream-v5.0-lite |
| AtlasCloud Seedream V4.5 Text-to-Image | bytedance/seedream-v4.5 |
| AtlasCloud Ideogram V3 Quality Text-to-Image | ideogram-ai/ideogram-v3-quality |
| AtlasCloud Ideogram V3 Turbo Text-to-Image | ideogram-ai/ideogram-v3-turbo |
| AtlasCloud Luma Photon Text-to-Image | luma/photon |
| AtlasCloud Luma Photon Flash Text-to-Image | luma/photon-flash |
| AtlasCloud Recraft V3 Text-to-Image | recraft-ai/recraft-v3 |
| AtlasCloud Flux2 Flex Text-to-Image | flux2/flex |
| AtlasCloud ZImage Turbo Lora Text-to-Image | z-image/turbo-lora |

### Image Edit

| Node | Model |
|------|-------|
| AtlasCloud Nano Banana 2 Edit | google/nano-banana-2/edit |
| AtlasCloud Nano Banana 2 Edit Developer | google/nano-banana-2/edit-developer |
| AtlasCloud Seedream V5.0 Lite Edit | bytedance/seedream-v5.0-lite/edit |

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
