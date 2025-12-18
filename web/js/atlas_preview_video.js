import { app, ANIM_PREVIEW_WIDGET } from "../../../../scripts/app.js";
import { createImageHost } from "../../../../scripts/ui/imagePreview.js";

const BASE_SIZE = 768;

function setVideoDimensions(videoElement, width, height) {
    videoElement.style.width = `${width}px`;
    videoElement.style.height = `${height}px`;
}

export function resizeVideoAspectRatio(videoElement, maxWidth, maxHeight) {
    const aspectRatio = videoElement.videoWidth / videoElement.videoHeight;
    let newWidth, newHeight;

    if (
        videoElement.videoWidth / maxWidth >
        videoElement.videoHeight / maxHeight
    ) {
        newWidth = maxWidth;
        newHeight = newWidth / aspectRatio;
    } else {
        newHeight = maxHeight;
        newWidth = newHeight * aspectRatio;
    }

    setVideoDimensions(videoElement, newWidth, newHeight);
}

export function chainCallback(object, property, callback) {
    if (object == undefined) {
        console.error("Tried to add callback to non-existant object");
        return;
    }
    if (property in object) {
        const callback_orig = object[property];
        object[property] = function () {
            const r = callback_orig.apply(this, arguments);
            callback.apply(this, arguments);
            return r;
        };
    } else {
        object[property] = callback;
    }
}

export function addVideoPreview(nodeType) {
    const createVideoNode = (url) => {
        return new Promise((cb) => {
            const videoEl = document.createElement("video");

            videoEl.addEventListener("loadedmetadata", () => {
                videoEl.controls = true;
                videoEl.loop = true;
                videoEl.muted = true; // autoplay policy
                videoEl.playsInline = true;

                videoEl.addEventListener("click", () => {
                    if (videoEl.muted) {
                        videoEl.muted = false;
                        videoEl.play();
                    }
                });

                resizeVideoAspectRatio(videoEl, BASE_SIZE, BASE_SIZE);
                cb(videoEl);
            });

            videoEl.addEventListener("error", () => cb());

            videoEl.src = url;
        });
    };

    nodeType.prototype.onDrawBackground = function () {
        if (this.flags.collapsed) return;

        const urls = this.images ?? [];
        let changed = false;

        if (JSON.stringify(this.displayingImages) !== JSON.stringify(urls)) {
            this.displayingImages = urls;
            changed = true;
        }
        if (!changed) return;

        if (!urls.length) {
            this.imgs = null;
            this.animatedImages = false;
            return;
        }

        Promise.all(urls.map((u) => createVideoNode(u)))
            .then((imgs) => {
                this.imgs = imgs.filter(Boolean);
            })
            .then(() => {
                if (!this.imgs?.length) return;

                this.animatedImages = true;
                const widgetIdx = this.widgets?.findIndex(
                    (w) => w.name === ANIM_PREVIEW_WIDGET
                );

                this.size[0] = BASE_SIZE;
                this.size[1] = BASE_SIZE;

                if (widgetIdx > -1) {
                    const widget = this.widgets[widgetIdx];
                    widget.options.host.updateImages(this.imgs);
                } else {
                    const host = createImageHost(this);
                    const widget = this.addDOMWidget(
                        ANIM_PREVIEW_WIDGET,
                        "img",
                        host.el,
                        {
                            host,
                            getHeight: host.getHeight,
                            onDraw: host.onDraw,
                            hideOnZoom: false,
                        }
                    );
                    widget.serializeValue = () => ({ height: BASE_SIZE });
                    widget.options.host.updateImages(this.imgs);
                }

                this.imgs.forEach((el) => {
                    if (el instanceof HTMLVideoElement) {
                        el.muted = true;
                        el.autoplay = true;
                        const p = el.play();
                        if (p?.catch) p.catch(() => {});
                    }
                });

                this.setDirtyCanvas(true, true);
            });
    };

    chainCallback(nodeType.prototype, "onExecuted", function (message) {
        // Our python node returns: {"ui": {"video_url": [url]}}
        if (message?.video_url) {
            this.images = message.video_url; // should be an array
            this.setDirtyCanvas(true);
        }
    });
}

app.registerExtension({
    name: "AtlasCloudPreviewVideo",
    async beforeRegisterNodeDef(nodeType, nodeData) {
        // ✅ MUST match your python node name (registry key)
        if (nodeData.name !== "AtlasCloud Video Preview") return;
        addVideoPreview(nodeType);
    },
});

console.log("[AtlasCloudPreviewVideo] loaded");
