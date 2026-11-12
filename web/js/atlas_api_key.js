import { app } from "../../../scripts/app.js";
import { api } from "../../../scripts/api.js";

// Keeps the AtlasCloud API key out of workflows, queued prompts and image metadata.
// The key is stored by the server in ComfyUI's user/__atlascloud/ directory (never served
// over HTTP); the node's legacy api_key widget is hidden and always saved blank.

const NODE_NAME = "AtlasCloud Client";
const EXAMPLE_PLACEHOLDER = "PASTE_YOUR_ATLASCLOUD_API_KEY";

function toast(severity, summary, detail) {
    app.extensionManager?.toast?.add({ severity, summary, detail, life: 6000 });
}

async function fetchStatus() {
    const resp = await api.fetchApi("/atlas/api_key");
    return resp.json();
}

async function saveKey(apiKey) {
    const resp = await api.fetchApi("/atlas/api_key", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ api_key: apiKey }),
    });
    if (!resp.ok) {
        throw new Error(`HTTP ${resp.status}`);
    }
    return resp.json();
}

function statusLabel(status) {
    if (!status?.configured) return "🔑 Set API key (none saved)";
    const where = status.source === "env" ? "env var" : "saved locally";
    return `🔑 API key …${status.hint} (${where})`;
}

function askForKey() {
    return new Promise((resolve) => {
        const overlay = document.createElement("div");
        overlay.style.cssText =
            "position:fixed;inset:0;background:rgba(0,0,0,.5);display:flex;align-items:center;justify-content:center;z-index:10000";
        const box = document.createElement("div");
        box.style.cssText =
            "background:var(--comfy-menu-bg,#222);color:var(--fg-color,#ddd);padding:16px;border-radius:8px;width:min(420px,90vw);font:14px sans-serif";
        box.innerHTML = `
            <div style="font-weight:600;margin-bottom:8px">AtlasCloud API key</div>
            <div style="opacity:.8;margin-bottom:10px">Stored on this ComfyUI server only. It is never saved in workflows or images. Leave empty to remove the saved key.</div>
            <input type="password" autocomplete="off" spellcheck="false" style="width:100%;box-sizing:border-box;padding:6px" />
            <div style="display:flex;gap:8px;justify-content:flex-end;margin-top:12px">
                <button data-act="cancel">Cancel</button><button data-act="save">Save</button>
            </div>`;
        overlay.appendChild(box);
        document.body.appendChild(overlay);
        const input = box.querySelector("input");
        // The canvas grabs focus back when the button click finishes; focus on the next tick
        // and keep keystrokes away from ComfyUI's shortcuts while the dialog is open.
        setTimeout(() => input.focus(), 0);
        overlay.addEventListener("keydown", (e) => e.stopPropagation());
        overlay.addEventListener("pointerdown", (e) => e.stopPropagation());

        const close = (value) => {
            overlay.remove();
            resolve(value);
        };
        box.querySelector('[data-act="cancel"]').onclick = () => close(null);
        box.querySelector('[data-act="save"]').onclick = () => close(input.value);
        input.addEventListener("keydown", (e) => {
            if (e.key === "Enter") close(input.value);
            if (e.key === "Escape") close(null);
        });
    });
}

app.registerExtension({
    name: "AtlasCloud.ApiKey",
    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeData.name !== NODE_NAME) return;

        const onNodeCreated = nodeType.prototype.onNodeCreated;
        nodeType.prototype.onNodeCreated = function () {
            const r = onNodeCreated?.apply(this, arguments);

            const keyWidget = this.widgets?.find((w) => w.name === "api_key");
            if (keyWidget) {
                keyWidget.hidden = true;
                keyWidget.serializeValue = () => "";
            }

            const button = this.addWidget(
                "button",
                "atlas_api_key_button",
                null,
                async () => {
                    const value = await askForKey();
                    if (value === null) return;
                    try {
                        const status = await saveKey(value);
                        button.label = statusLabel(status);
                        this.setDirtyCanvas(true, true);
                        toast("success", "AtlasCloud", status.configured ? "API key saved on the server." : "Saved API key removed.");
                    } catch (err) {
                        toast("error", "AtlasCloud", `Could not save the API key: ${err.message}`);
                    }
                },
                { serialize: false }
            );
            button.serialize = false;
            button.label = "🔑 API key: checking…";
            fetchStatus()
                .then((status) => {
                    button.label = statusLabel(status);
                    this.setDirtyCanvas(true, true);
                })
                .catch(() => {
                    button.label = "🔑 Set API key";
                });
            return r;
        };

        const onConfigure = nodeType.prototype.onConfigure;
        nodeType.prototype.onConfigure = function () {
            const r = onConfigure?.apply(this, arguments);

            // Workflows saved before this change carry a key in the widget. Always blank it so the
            // next save drops it. Adopt it only when no key is configured yet: a workflow shared by
            // someone else must never replace your key (your runs would go to their account).
            const keyWidget = this.widgets?.find((w) => w.name === "api_key");
            const legacyKey = (keyWidget?.value || "").trim();
            if (keyWidget && legacyKey) {
                keyWidget.value = "";
                if (legacyKey === EXAMPLE_PLACEHOLDER) return r;
                const updateButton = (status) => {
                    const button = this.widgets?.find((w) => w.name === "atlas_api_key_button");
                    if (button) button.label = statusLabel(status);
                    this.setDirtyCanvas(true, true);
                };
                fetchStatus()
                    .then(async (status) => {
                        if (status.configured) {
                            toast("warn", "AtlasCloud", "This workflow contained an API key. It was removed from the node and not used; save the workflow to drop it from the file.");
                            return;
                        }
                        updateButton(await saveKey(legacyKey));
                        toast("warn", "AtlasCloud", "This workflow contained an API key. It is now stored on the server and removed from the node; save the workflow to drop it from the file.");
                    })
                    .catch((err) => toast("error", "AtlasCloud", `Could not check the API key: ${err.message}`));
            }
            return r;
        };
    },
});
