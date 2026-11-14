import { app } from "../../../scripts/app.js";

// The multi-image nodes declare image_1..image_30 in Python. Show only the connected
// image sockets plus one empty one, so a new socket appears each time you connect one.

const NODE_NAMES = new Set(["AtlasCloud Multi Image to Base64", "AtlasCloud Multi Image to Seedance Assets"]);
const MAX_IMAGES = 30;
const IMAGE_INPUT = /^image_(\d+)$/;

function imageNumber(input) {
    const m = IMAGE_INPUT.exec(input?.name ?? "");
    return m ? Number(m[1]) : 0;
}

function syncImageInputs(node) {
    if (node.__atlasSyncing) return;
    node.__atlasSyncing = true;
    try {
        const inputs = node.inputs ?? [];
        let lastConnected = 0;
        for (const input of inputs) {
            const n = imageNumber(input);
            if (n && input.link != null) lastConnected = Math.max(lastConnected, n);
        }
        const keep = Math.min(lastConnected + 1, MAX_IMAGES);

        for (let i = inputs.length - 1; i >= 0; i--) {
            const n = imageNumber(inputs[i]);
            if (n > keep && inputs[i].link == null) node.removeInput(i);
        }
        const present = new Set((node.inputs ?? []).map(imageNumber));
        for (let n = 1; n <= keep; n++) {
            if (!present.has(n)) node.addInput(`image_${n}`, "IMAGE");
        }

        const size = node.computeSize();
        node.setSize([Math.max(node.size[0], size[0]), size[1]]);
        node.setDirtyCanvas?.(true, true);
    } finally {
        node.__atlasSyncing = false;
    }
}

app.registerExtension({
    name: "AtlasCloud.DynamicImageInputs",
    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (!NODE_NAMES.has(nodeData.name)) return;

        const onNodeCreated = nodeType.prototype.onNodeCreated;
        nodeType.prototype.onNodeCreated = function () {
            const r = onNodeCreated?.apply(this, arguments);
            syncImageInputs(this);
            return r;
        };

        const onConfigure = nodeType.prototype.onConfigure;
        nodeType.prototype.onConfigure = function () {
            const r = onConfigure?.apply(this, arguments);
            // Links are restored after configure; sync once the graph has settled.
            queueMicrotask(() => syncImageInputs(this));
            return r;
        };

        const onConnectionsChange = nodeType.prototype.onConnectionsChange;
        nodeType.prototype.onConnectionsChange = function (type) {
            const r = onConnectionsChange?.apply(this, arguments);
            if (type === (globalThis.LiteGraph?.INPUT ?? 1)) syncImageInputs(this);
            return r;
        };
    },
});
