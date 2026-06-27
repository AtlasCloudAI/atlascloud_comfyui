import { app } from "../../../../scripts/app.js";

const PANEL_ID = "atlas-history-panel";
const BUTTON_ID = "atlas-history-button";
const MASK_ID = "atlas-history-mask";

function ensureStyles() {
  if (document.getElementById("atlas-history-style")) return;
  const style = document.createElement("style");
  style.id = "atlas-history-style";
  style.textContent = `
    #${BUTTON_ID} {
      position: fixed;
      right: 20px;
      bottom: 20px;
      z-index: 10000;
      min-width: 128px;
      padding: 12px 16px;
      border: 1px solid rgba(96, 165, 250, 0.35);
      border-radius: 999px;
      background: linear-gradient(135deg, rgba(37, 99, 235, 0.96), rgba(29, 78, 216, 0.96));
      color: #ffffff;
      box-shadow: 0 14px 30px rgba(2, 6, 23, 0.35);
      cursor: pointer;
      font-size: 13px;
      font-weight: 600;
      letter-spacing: 0.2px;
      transition: transform 0.16s ease, box-shadow 0.16s ease;
    }
    #${BUTTON_ID}:hover {
      transform: translateY(-1px);
      box-shadow: 0 18px 34px rgba(2, 6, 23, 0.4);
    }
    #${MASK_ID} {
      position: fixed;
      inset: 0;
      z-index: 9998;
      display: none;
      background: rgba(2, 6, 23, 0.36);
      backdrop-filter: blur(3px);
    }
    #${MASK_ID}.open {
      display: block;
    }
    #${PANEL_ID} {
      position: fixed;
      top: 18px;
      right: 18px;
      width: min(1180px, calc(100vw - 36px));
      height: min(840px, calc(100vh - 36px));
      z-index: 9999;
      display: none;
      overflow: hidden;
      border: 1px solid rgba(148, 163, 184, 0.18);
      border-radius: 18px;
      background:
        radial-gradient(circle at top right, rgba(59, 130, 246, 0.12), transparent 25%),
        linear-gradient(180deg, #0b1220 0%, #0f172a 100%);
      color: #e2e8f0;
      box-shadow: 0 24px 60px rgba(2, 6, 23, 0.55);
    }
    #${PANEL_ID}.open {
      display: grid;
      grid-template-columns: 340px 1fr;
    }
    #${PANEL_ID} * {
      box-sizing: border-box;
    }
    #${PANEL_ID} .atlas-history-sidebar {
      display: flex;
      flex-direction: column;
      min-height: 0;
      border-right: 1px solid rgba(51, 65, 85, 0.85);
      background: rgba(2, 6, 23, 0.42);
    }
    #${PANEL_ID} .atlas-history-main {
      display: flex;
      flex-direction: column;
      min-width: 0;
      min-height: 0;
      background: rgba(15, 23, 42, 0.56);
    }
    #${PANEL_ID} .atlas-history-header,
    #${PANEL_ID} .atlas-history-main-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      padding: 18px 18px 14px;
      border-bottom: 1px solid rgba(51, 65, 85, 0.85);
    }
    #${PANEL_ID} .atlas-history-title-wrap {
      display: flex;
      flex-direction: column;
      gap: 4px;
      min-width: 0;
    }
    #${PANEL_ID} .atlas-history-title {
      color: #f8fafc;
      font-size: 16px;
      font-weight: 700;
    }
    #${PANEL_ID} .atlas-history-subtitle {
      color: #94a3b8;
      font-size: 12px;
    }
    #${PANEL_ID} .atlas-history-toolbar {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }
    #${PANEL_ID} button {
      border: 1px solid rgba(96, 165, 250, 0.22);
      border-radius: 10px;
      background: rgba(37, 99, 235, 0.18);
      color: #e2e8f0;
      padding: 8px 12px;
      cursor: pointer;
      font-size: 12px;
      font-weight: 600;
    }
    #${PANEL_ID} button:hover {
      background: rgba(37, 99, 235, 0.28);
    }
    #${PANEL_ID} button.atlas-secondary {
      border-color: rgba(148, 163, 184, 0.16);
      background: rgba(51, 65, 85, 0.45);
    }
    #${PANEL_ID} .atlas-history-meta {
      padding: 12px 18px 14px;
      color: #94a3b8;
      font-size: 12px;
      border-bottom: 1px solid rgba(51, 65, 85, 0.85);
      word-break: break-all;
    }
    #${PANEL_ID} .atlas-history-search {
      margin: 0 18px 14px;
      padding: 11px 14px;
      border-radius: 12px;
      border: 1px solid rgba(51, 65, 85, 0.85);
      background: rgba(15, 23, 42, 0.8);
      color: #e2e8f0;
      outline: none;
      font-size: 13px;
    }
    #${PANEL_ID} .atlas-history-search::placeholder {
      color: #64748b;
    }
    #${PANEL_ID} .atlas-history-list {
      flex: 1;
      overflow: auto;
      min-height: 0;
      padding: 0 12px 12px;
    }
    #${PANEL_ID} .atlas-history-card {
      margin: 0 6px 10px;
      padding: 14px;
      border-radius: 14px;
      border: 1px solid rgba(51, 65, 85, 0.85);
      background: rgba(15, 23, 42, 0.85);
      cursor: pointer;
      transition: border-color 0.14s ease, background 0.14s ease, transform 0.14s ease;
    }
    #${PANEL_ID} .atlas-history-card:hover {
      transform: translateY(-1px);
      border-color: rgba(96, 165, 250, 0.36);
      background: rgba(15, 23, 42, 0.96);
    }
    #${PANEL_ID} .atlas-history-card.active {
      border-color: rgba(96, 165, 250, 0.8);
      background: linear-gradient(180deg, rgba(30, 41, 59, 0.96), rgba(15, 23, 42, 0.96));
      box-shadow: inset 0 0 0 1px rgba(96, 165, 250, 0.14);
    }
    #${PANEL_ID} .atlas-history-card-title {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      margin-bottom: 8px;
    }
    #${PANEL_ID} .atlas-history-card-name {
      color: #f8fafc;
      font-size: 13px;
      font-weight: 700;
      line-height: 1.4;
    }
    #${PANEL_ID} .atlas-history-card-meta,
    #${PANEL_ID} .atlas-history-card-prompt {
      color: #94a3b8;
      font-size: 12px;
      line-height: 1.5;
    }
    #${PANEL_ID} .atlas-history-card-prompt {
      margin-top: 8px;
      color: #cbd5e1;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }
    #${PANEL_ID} .atlas-history-empty,
    #${PANEL_ID} .atlas-history-empty-main {
      display: flex;
      align-items: center;
      justify-content: center;
      color: #94a3b8;
      font-size: 13px;
      text-align: center;
    }
    #${PANEL_ID} .atlas-history-empty {
      min-height: 180px;
      margin: 12px;
      padding: 24px;
      border: 1px dashed rgba(71, 85, 105, 0.8);
      border-radius: 16px;
      background: rgba(15, 23, 42, 0.4);
    }
    #${PANEL_ID} .atlas-history-empty-main {
      flex: 1;
      padding: 32px;
    }
    #${PANEL_ID} .atlas-status {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 5px 9px;
      border-radius: 999px;
      font-size: 11px;
      font-weight: 700;
      white-space: nowrap;
    }
    #${PANEL_ID} .atlas-status.completed { background: rgba(34, 197, 94, 0.15); color: #86efac; }
    #${PANEL_ID} .atlas-status.processing { background: rgba(59, 130, 246, 0.16); color: #93c5fd; }
    #${PANEL_ID} .atlas-status.failed,
    #${PANEL_ID} .atlas-status.submit_failed { background: rgba(239, 68, 68, 0.16); color: #fca5a5; }
    #${PANEL_ID} .atlas-status.submitted { background: rgba(250, 204, 21, 0.16); color: #fde68a; }
    #${PANEL_ID} .atlas-history-main-content {
      flex: 1;
      overflow-y: auto;
      overflow-x: hidden;
      min-height: 0;
      padding: 18px;
    }
    #${PANEL_ID} .atlas-detail-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 14px;
      margin-bottom: 14px;
    }
    #${PANEL_ID} .atlas-section,
    #${PANEL_ID} .atlas-kpi,
    #${PANEL_ID} .atlas-preview-card {
      border: 1px solid rgba(51, 65, 85, 0.85);
      border-radius: 16px;
      background: rgba(15, 23, 42, 0.82);
    }
    #${PANEL_ID} .atlas-kpi {
      padding: 14px 16px;
    }
    #${PANEL_ID} .atlas-kpi-label {
      color: #94a3b8;
      font-size: 12px;
      margin-bottom: 8px;
    }
    #${PANEL_ID} .atlas-kpi-value {
      color: #f8fafc;
      font-size: 13px;
      font-weight: 700;
      line-height: 1.5;
      word-break: break-word;
    }
    #${PANEL_ID} .atlas-section {
      margin-bottom: 14px;
      overflow: hidden;
    }
    #${PANEL_ID} .atlas-section-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      padding: 14px 16px;
      border-bottom: 1px solid rgba(51, 65, 85, 0.85);
      background: rgba(2, 6, 23, 0.28);
    }
    #${PANEL_ID} .atlas-section-title {
      color: #f8fafc;
      font-size: 13px;
      font-weight: 700;
    }
    #${PANEL_ID} .atlas-section-body {
      padding: 16px;
    }
    #${PANEL_ID} .atlas-prompt {
      white-space: pre-wrap;
      line-height: 1.7;
      color: #e2e8f0;
      word-break: break-word;
    }
    #${PANEL_ID} .atlas-param-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
    }
    #${PANEL_ID} .atlas-param-item {
      padding: 12px 13px;
      border-radius: 12px;
      border: 1px solid rgba(51, 65, 85, 0.8);
      background: rgba(2, 6, 23, 0.2);
      min-width: 0;
    }
    #${PANEL_ID} .atlas-param-key {
      color: #94a3b8;
      font-size: 11px;
      margin-bottom: 6px;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }
    #${PANEL_ID} .atlas-param-value {
      color: #f8fafc;
      font-size: 12px;
      line-height: 1.6;
      white-space: pre-wrap;
      word-break: break-word;
    }
    #${PANEL_ID} .atlas-asset-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
      gap: 14px;
    }
    #${PANEL_ID} .atlas-preview-card {
      padding: 12px;
    }
    #${PANEL_ID} .atlas-preview-meta {
      color: #94a3b8;
      font-size: 11px;
      line-height: 1.5;
      margin-top: 8px;
      word-break: break-word;
    }
    #${PANEL_ID} .atlas-preview-title {
      color: #f8fafc;
      font-size: 12px;
      font-weight: 700;
      margin-bottom: 10px;
      word-break: break-word;
    }
    #${PANEL_ID} .atlas-preview-image,
    #${PANEL_ID} .atlas-preview-video {
      width: 100%;
      max-height: 240px;
      object-fit: contain;
      border-radius: 12px;
      background: rgba(2, 6, 23, 0.55);
    }
    #${PANEL_ID} .atlas-preview-video {
      aspect-ratio: 1 / 1;
    }
    #${PANEL_ID} .atlas-preview-actions {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
      margin-top: 10px;
    }
    #${PANEL_ID} .atlas-preview-link {
      color: #93c5fd;
      text-decoration: none;
      font-size: 12px;
    }
    #${PANEL_ID} details {
      border-top: 1px solid rgba(51, 65, 85, 0.85);
    }
    #${PANEL_ID} summary {
      cursor: pointer;
      padding: 14px 16px;
      color: #cbd5e1;
      font-weight: 600;
      list-style: none;
    }
    #${PANEL_ID} summary::-webkit-details-marker {
      display: none;
    }
    #${PANEL_ID} .atlas-raw-json {
      margin: 0;
      padding: 0 16px 16px;
      color: #cbd5e1;
      white-space: pre-wrap;
      word-break: break-word;
      font-size: 12px;
      line-height: 1.55;
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    }
    @media (max-width: 960px) {
      #${PANEL_ID}.open {
        grid-template-columns: 1fr;
      }
      #${PANEL_ID} .atlas-history-sidebar {
        border-right: none;
        border-bottom: 1px solid rgba(51, 65, 85, 0.85);
        max-height: 42%;
      }
      #${PANEL_ID} .atlas-detail-grid,
      #${PANEL_ID} .atlas-param-grid {
        grid-template-columns: 1fr;
      }
    }
  `;
  document.head.appendChild(style);
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function formatTime(value) {
  if (!value) return "-";
  try {
    return new Date(value).toLocaleString();
  } catch (_) {
    return String(value);
  }
}

function statusClass(status) {
  const normalized = String(status || "").toLowerCase();
  if (normalized.includes("complete") || normalized.includes("succeed")) return "completed";
  if (normalized.includes("process")) return "processing";
  if (normalized.includes("fail")) return "failed";
  if (normalized.includes("submit")) return "submitted";
  return "submitted";
}

function renderStatus(status) {
  const text = String(status || "unknown");
  return `<span class="atlas-status ${statusClass(text)}">${escapeHtml(text)}</span>`;
}

async function fetchJson(url) {
  const resp = await fetch(url);
  if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
  return resp.json();
}

async function postJson(url) {
  const resp = await fetch(url, { method: "POST" });
  if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
  return resp.json();
}

function ensureUi() {
  ensureStyles();

  let mask = document.getElementById(MASK_ID);
  if (!mask) {
    mask = document.createElement("div");
    mask.id = MASK_ID;
    document.body.appendChild(mask);
  }

  let button = document.getElementById(BUTTON_ID);
  if (!button) {
    button = document.createElement("button");
    button.id = BUTTON_ID;
    button.textContent = "Atlas 历史中心";
    document.body.appendChild(button);
  }

  let panel = document.getElementById(PANEL_ID);
  if (!panel) {
    panel = document.createElement("div");
    panel.id = PANEL_ID;
    panel.innerHTML = `
      <div class="atlas-history-sidebar">
        <div class="atlas-history-header">
          <div class="atlas-history-title-wrap">
            <div class="atlas-history-title">Atlas 节点历史</div>
            <div class="atlas-history-subtitle">只展示 Atlas 节点自己的提示词、传参与结果</div>
          </div>
          <div class="atlas-history-toolbar">
            <button id="atlas-history-refresh">刷新</button>
          </div>
        </div>
        <div id="atlas-history-meta" class="atlas-history-meta">加载中...</div>
        <input id="atlas-history-search" class="atlas-history-search" placeholder="搜索模型、节点、prompt、prediction_id" />
        <div id="atlas-history-list" class="atlas-history-list"></div>
      </div>
      <div class="atlas-history-main">
        <div class="atlas-history-main-header">
          <div class="atlas-history-title-wrap">
            <div class="atlas-history-title">历史详情</div>
            <div class="atlas-history-subtitle">结构化查看输入提示词、参数与输出结果预览</div>
          </div>
          <div class="atlas-history-toolbar">
            <button id="atlas-history-close" class="atlas-secondary">关闭</button>
          </div>
        </div>
        <div id="atlas-history-detail" class="atlas-history-main-content atlas-history-empty-main">点击左侧任意一条 Atlas 节点历史查看详情</div>
      </div>
    `;
    document.body.appendChild(panel);
  }

  return {
    mask,
    button,
    panel,
    meta: panel.querySelector("#atlas-history-meta"),
    list: panel.querySelector("#atlas-history-list"),
    detail: panel.querySelector("#atlas-history-detail"),
    refresh: panel.querySelector("#atlas-history-refresh"),
    close: panel.querySelector("#atlas-history-close"),
    search: panel.querySelector("#atlas-history-search"),
  };
}

function getCardTitle(item) {
  return item.node_context?.node_class || item.model || item.prediction_id || "未命名记录";
}

function getSearchText(item) {
  return [
    item.prediction_id,
    item.model,
    item.prompt_preview,
    item.request_kind,
    item.latest_status,
    item.node_context?.node_class,
  ]
    .filter(Boolean)
    .join(" ")
    .toLowerCase();
}

function renderList(container, items, selectedPredictionId, onSelect) {
  container.innerHTML = "";
  if (!items.length) {
    container.innerHTML = `<div class="atlas-history-empty">暂无 Atlas 节点历史记录</div>`;
    return;
  }

  for (const item of items) {
    const card = document.createElement("div");
    card.className = "atlas-history-card";
    if (item.prediction_id === selectedPredictionId) {
      card.classList.add("active");
    }
    card.innerHTML = `
      <div class="atlas-history-card-title">
        <div class="atlas-history-card-name">${escapeHtml(getCardTitle(item))}</div>
        ${renderStatus(item.latest_status)}
      </div>
      <div class="atlas-history-card-meta">${escapeHtml(item.request_kind || "")} · ${escapeHtml(formatTime(item.submitted_at))}</div>
      <div class="atlas-history-card-meta">本地文件 ${escapeHtml(item.local_asset_count || 0)} · ${escapeHtml(item.prediction_id || "")}</div>
      <div class="atlas-history-card-prompt">${escapeHtml(item.prompt_preview || "无 prompt")}</div>
    `;
    card.addEventListener("click", () => onSelect(item.prediction_id));
    container.appendChild(card);
  }
}

function formatValue(value) {
  if (value === null || value === undefined || value === "") return "-";
  if (typeof value === "string") return value;
  if (typeof value === "number" || typeof value === "boolean") return String(value);
  return JSON.stringify(value, null, 2);
}

function renderParamGrid(payload) {
  const entries = Object.entries(payload || {});
  if (!entries.length) {
    return `<div class="atlas-history-empty">暂无结构化参数</div>`;
  }
  return `
    <div class="atlas-param-grid">
      ${entries
        .map(
          ([key, value]) => `
            <div class="atlas-param-item">
              <div class="atlas-param-key">${escapeHtml(key)}</div>
              <div class="atlas-param-value">${escapeHtml(formatValue(value))}</div>
            </div>
          `
        )
        .join("")}
    </div>
  `;
}

function inferAssetKind(label, url, mimeType = "") {
  const lowerLabel = String(label || "").toLowerCase();
  const lowerUrl = String(url || "").toLowerCase();
  const lowerMime = String(mimeType || "").toLowerCase();
  if (lowerMime.startsWith("video/") || lowerLabel.includes("video") || lowerUrl.match(/\.(mp4|mov|webm|m4v)$/)) return "video";
  if (lowerMime.startsWith("audio/") || lowerLabel.includes("audio") || lowerUrl.match(/\.(mp3|wav|m4a|aac)$/)) return "audio";
  return "image";
}

function previewMarkup(src, kind) {
  if (!src) return "";
  if (kind === "video") {
    return `<video class="atlas-preview-video" src="${escapeHtml(src)}" controls playsinline></video>`;
  }
  if (kind === "audio") {
    return `<audio style="width:100%;" src="${escapeHtml(src)}" controls></audio>`;
  }
  return `<img class="atlas-preview-image" src="${escapeHtml(src)}" />`;
}

function renderInputAssets(item) {
  const inputAssets = Array.isArray(item.input_downloaded_assets) ? item.input_downloaded_assets : [];

  if (!inputAssets.length) {
    return `<div class="atlas-history-empty">暂无输入素材预览</div>`;
  }

  return `
    <div class="atlas-asset-grid">
      ${inputAssets
        .map(
          (asset) => `
            <div class="atlas-preview-card">
              <div class="atlas-preview-title">${escapeHtml(asset.label || asset.filename || "input")}</div>
              ${asset.status === "downloaded" ? previewMarkup(asset.serve_path, inferAssetKind(asset.filename || asset.label, asset.serve_path, asset.mime_type)) : ""}
              <div class="atlas-preview-actions">
                ${asset.status === "downloaded" ? `<a class="atlas-preview-link" href="${escapeHtml(asset.serve_path)}" target="_blank">打开本地素材</a>` : ""}
              </div>
              <div class="atlas-preview-meta">${asset.status === "downloaded" ? `本地路径: ${escapeHtml(asset.local_path || "-")}` : `下载失败: ${escapeHtml(asset.error || "")}`}</div>
              ${asset.source_url ? `<div class="atlas-preview-meta">来源: ${escapeHtml(asset.source_url)}</div>` : ""}
            </div>
          `
        )
        .join("")}
    </div>
  `;
}

function renderOutputAssets(item) {
  const downloadedAssets = Array.isArray(item.downloaded_assets) ? item.downloaded_assets : [];
  if (!downloadedAssets.length) {
    return `<div class="atlas-history-empty">暂无本地输出文件，可点击“补下载本地文件”</div>`;
  }

  return `
    <div class="atlas-asset-grid">
      ${downloadedAssets
        .map((asset) => {
          if (asset.status !== "downloaded") {
            return `
              <div class="atlas-preview-card">
                <div class="atlas-preview-title">文件 ${escapeHtml(asset.index)}</div>
                <div class="atlas-preview-meta">下载失败: ${escapeHtml(asset.error || "")}</div>
              </div>
            `;
          }

          const kind = inferAssetKind(asset.filename, asset.serve_path, asset.mime_type);
          return `
            <div class="atlas-preview-card">
              <div class="atlas-preview-title">${escapeHtml(asset.filename || `文件 ${asset.index}`)}</div>
              ${previewMarkup(asset.serve_path, kind)}
              <div class="atlas-preview-actions">
                <a class="atlas-preview-link" href="${escapeHtml(asset.serve_path)}" target="_blank">预览本地文件</a>
              </div>
              <div class="atlas-preview-meta">本地路径: ${escapeHtml(asset.local_path || "-")}</div>
              <div class="atlas-preview-meta">大小: ${escapeHtml(asset.size_bytes || "-")} bytes</div>
            </div>
          `;
        })
        .join("")}
    </div>
  `;
}

function renderDetail(item) {
  const payload = item.payload || {};
  const prompt = payload.prompt || "";
  const negativePrompt = payload.negative_prompt || "";
  const nodeClass = item.node_context?.node_class || "-";
  const model = payload.model || item.model || "-";
  const status = item.latest_status || "-";
  return `
    <div>
      <div class="atlas-detail-grid">
        <div class="atlas-kpi">
          <div class="atlas-kpi-label">节点</div>
          <div class="atlas-kpi-value">${escapeHtml(nodeClass)}</div>
        </div>
        <div class="atlas-kpi">
          <div class="atlas-kpi-label">模型</div>
          <div class="atlas-kpi-value">${escapeHtml(model)}</div>
        </div>
        <div class="atlas-kpi">
          <div class="atlas-kpi-label">状态</div>
          <div class="atlas-kpi-value">${renderStatus(status)}</div>
        </div>
        <div class="atlas-kpi">
          <div class="atlas-kpi-label">prediction_id</div>
          <div class="atlas-kpi-value">${escapeHtml(item.prediction_id || "-")}</div>
        </div>
        <div class="atlas-kpi">
          <div class="atlas-kpi-label">提交时间</div>
          <div class="atlas-kpi-value">${escapeHtml(formatTime(item.submitted_at))}</div>
        </div>
        <div class="atlas-kpi">
          <div class="atlas-kpi-label">完成时间</div>
          <div class="atlas-kpi-value">${escapeHtml(formatTime(item.completed_at))}</div>
        </div>
      </div>

      <div class="atlas-section">
        <div class="atlas-section-header">
          <div class="atlas-section-title">提示词</div>
          <div class="atlas-history-toolbar">
            ${item.prompt_file?.serve_path ? `<a class="atlas-preview-link" href="${escapeHtml(item.prompt_file.serve_path)}" target="_blank">打开本地 prompt.txt</a>` : ""}
          </div>
        </div>
        <div class="atlas-section-body">
          <div class="atlas-prompt">${escapeHtml(prompt || "无正向提示词")}</div>
          ${negativePrompt ? `<div class="atlas-prompt" style="margin-top:12px;color:#94a3b8;">负向提示词: ${escapeHtml(negativePrompt)}</div>` : ""}
          ${item.prompt_file?.local_path ? `<div class="atlas-preview-meta" style="margin-top:12px;">本地提示词文件: ${escapeHtml(item.prompt_file.local_path)}</div>` : ""}
        </div>
      </div>

      <div class="atlas-section">
        <div class="atlas-section-header">
          <div class="atlas-section-title">结构化传参</div>
        </div>
        <div class="atlas-section-body">
          ${renderParamGrid(payload)}
        </div>
      </div>

      <div class="atlas-section">
        <div class="atlas-section-header">
          <div class="atlas-section-title">输入素材预览</div>
        </div>
        <div class="atlas-section-body">
          ${renderInputAssets(item)}
        </div>
      </div>

      <div class="atlas-section">
        <div class="atlas-section-header">
          <div class="atlas-section-title">输出结果预览</div>
          <div class="atlas-history-toolbar">
            <button id="atlas-history-refresh-assets">补下载本地文件</button>
          </div>
        </div>
        <div class="atlas-section-body">
          ${renderOutputAssets(item)}
        </div>
      </div>

      <div class="atlas-section">
        <details>
          <summary>查看原始 JSON</summary>
          <pre class="atlas-raw-json">${escapeHtml(JSON.stringify(item, null, 2))}</pre>
        </details>
      </div>
    </div>
  `;
}

app.registerExtension({
  name: "AtlasCloud.LocalHistoryPanel",
  async setup() {
    const ui = ensureUi();
    const state = {
      items: [],
      filteredItems: [],
      selectedPredictionId: "",
    };

    function closePanel() {
      ui.panel.classList.remove("open");
      ui.mask.classList.remove("open");
    }

    function applyFilter() {
      const keyword = String(ui.search.value || "").trim().toLowerCase();
      state.filteredItems = keyword
        ? state.items.filter((item) => getSearchText(item).includes(keyword))
        : [...state.items];
      if (state.selectedPredictionId && !state.filteredItems.some((item) => item.prediction_id === state.selectedPredictionId)) {
        state.selectedPredictionId = state.filteredItems[0]?.prediction_id || "";
      }
      renderList(ui.list, state.filteredItems, state.selectedPredictionId, loadDetail);
    }

    async function loadList() {
      ui.meta.textContent = "加载中...";
      try {
        const data = await fetchJson("/api/atlas/history/runs?limit=80");
        state.items = Array.isArray(data.items) ? data.items : [];
        state.selectedPredictionId ||= state.items[0]?.prediction_id || "";
        ui.meta.textContent = `本地目录: ${data.history_dir || ""}`;
        applyFilter();
        if (state.selectedPredictionId) {
          await loadDetail(state.selectedPredictionId);
        } else {
          ui.detail.innerHTML = `<div class="atlas-history-empty-main">还没有 Atlas 节点历史，先跑一个 Atlas 节点任务再回来查看。</div>`;
        }
      } catch (error) {
        ui.meta.textContent = `加载失败: ${error}`;
        state.items = [];
        state.filteredItems = [];
        renderList(ui.list, [], "", loadDetail);
        ui.detail.innerHTML = `<div class="atlas-history-empty-main">接口不可用，请先重启 ComfyUI。</div>`;
      }
    }

    async function loadDetail(predictionId) {
      state.selectedPredictionId = predictionId;
      renderList(ui.list, state.filteredItems, state.selectedPredictionId, loadDetail);
      ui.detail.innerHTML = `<div class="atlas-history-empty-main">详情加载中...</div>`;
      try {
        const data = await fetchJson(`/api/atlas/history/runs/${encodeURIComponent(predictionId)}`);
        ui.detail.innerHTML = renderDetail(data.item || {});
        const refreshAssetsButton = ui.detail.querySelector("#atlas-history-refresh-assets");
        if (refreshAssetsButton) {
          refreshAssetsButton.addEventListener("click", async () => {
            refreshAssetsButton.disabled = true;
            refreshAssetsButton.textContent = "补下载中...";
            try {
              const refreshed = await postJson(`/api/atlas/history/runs/${encodeURIComponent(predictionId)}/refresh-assets`);
              ui.detail.innerHTML = renderDetail(refreshed.item || {});
              const index = state.items.findIndex((item) => item.prediction_id === predictionId);
              if (index >= 0) {
                state.items[index].local_asset_count = (refreshed.item?.downloaded_assets || []).filter((asset) => asset.status === "downloaded").length;
                applyFilter();
              }
            } catch (error) {
              ui.detail.insertAdjacentHTML(
                "afterbegin",
                `<div class="atlas-history-empty" style="margin-bottom:14px;color:#fca5a5;">补下载失败: ${escapeHtml(error)}</div>`
              );
            }
          });
        }
      } catch (error) {
        ui.detail.innerHTML = `<div class="atlas-history-empty-main">加载详情失败: ${escapeHtml(error)}</div>`;
      }
    }

    ui.button.addEventListener("click", async () => {
      const shouldOpen = !ui.panel.classList.contains("open");
      ui.panel.classList.toggle("open", shouldOpen);
      ui.mask.classList.toggle("open", shouldOpen);
      if (shouldOpen) {
        await loadList();
      }
    });

    ui.refresh.addEventListener("click", loadList);
    ui.close.addEventListener("click", closePanel);
    ui.mask.addEventListener("click", closePanel);
    ui.search.addEventListener("input", applyFilter);

    console.log("[AtlasCloud] LocalHistoryPanel ready");
  },
});
