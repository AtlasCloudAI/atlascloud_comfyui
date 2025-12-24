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

## Available Nodes (v1.0.0)

### Common

-   AtlasCloud Client
    Stores your API key and base URL for all AtlasCloud nodes.
-   Video Previewer
-   Image Previewer

### Text-to-Video（t2v）

-   AtlasCloud WAN2.6 Text-to-Video

-   AtlasCloud WAN2.5 Text-to-Video

-   AtlasCloud WAN2.2 Text-to-Video 720p

-   AtlasCloud VEO3.1 Text-to-Video

-   AtlasCloud Kling V2.6 Pro Text-to-Video

-   AtlasCloud Kling Video O1 Text-to-Video

-   AtlasCloud Seedance V1 Pro Text-to-Video 1080p

-   AtlasCloud Hailuo 2.3 Pro Text-to-Video

-   AtlasCloud Sora 2 Pro Text-to-Video

### Text-to-Image

-   AtlasCloud Seedream V4.5 Text-to-Image

-   AtlasCloud Flux 2 Flex Text-to-Image

-   AtlasCloud Z-Image Turbo LoRA Text-to-Image

-   AtlasCloud Nano Banana Pro Text-to-Image Ultra

### Nodes may expand over time as new models are added.

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
