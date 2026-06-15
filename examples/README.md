# Example Workflows

Ready-to-run graphs. Drag the `.json` onto the ComfyUI canvas (or **Workflow → Open**),
open the **AtlasCloud Client** node, and replace `PASTE_YOUR_ATLASCLOUD_API_KEY` with your
[free API key](https://www.atlascloud.ai/console/api-keys?utm_source=github&utm_campaign=atlascloud_comfyui). Then hit **Run** — no local GPU or model weights needed.

| File | What it does | Models | Nodes |
|------|--------------|--------|-------|
| [`01-text-to-image.json`](01-text-to-image.json) | Prompt → image | Nano Banana Pro | 3 |
| [`02-image-to-video.json`](02-image-to-video.json) | Image → ~5s video | Seedance 2 (image-to-video) | 5 |
| [`03-multi-reference-video.json`](03-multi-reference-video.json) | Up to 8 reference images → video | Seedance 2 (reference-to-video) + Multi Image to Base64 | 7 |

## Steps

1. Install the nodes — see the [root README](../README.md#installation).
2. Get a free [API key](https://www.atlascloud.ai/console/api-keys?utm_source=github&utm_campaign=atlascloud_comfyui).
3. Open a workflow, click the **AtlasCloud Client** node, paste your key.
4. Run.

> **Tip:** Seedance reference / image-to-video inputs reject real-person photos — use objects or scenes, or switch to a Kling node for people. Image inputs must be ≥ ~768×768.

_More example workflows are added as new models land. Want a specific pipeline? Open an issue._
