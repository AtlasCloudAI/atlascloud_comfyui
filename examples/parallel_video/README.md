# 多个视频节点「并行(同时)生成」示例

## 结论：可以并行
同一个工作流里多个**相互独立**的视频节点，可以**同时**调用云端生成，**不是**一个个排队。
实测：3 个节点（这里给的例子）/ 2 个节点都验证过，墙钟总耗时 ≈ **最慢的那一个**，而不是几个相加。

## 前提：视频节点必须是 `async` 的（一次性代码改动，已改好）
ComfyUI 的执行引擎本身支持并发调度 `async` 节点。但插件里的视频节点原来是**同步**的
（`def run` 里直接阻塞式「提交 + 轮询」），同步节点只能一个跑完再跑下一个 = 排队。

改法：把节点的 `run` 改成 `async def run`，把阻塞的「提交 + 轮询」丢进线程池：
```python
async def run(self, atlas_client, prompt, ...):
    import asyncio
    loop = asyncio.get_event_loop()
    # 本协程立即让出事件循环，多个独立视频节点就会被 ComfyUI 并发调度
    return await loop.run_in_executor(None, self._run_sync, atlas_client, prompt, ...)

def _run_sync(self, atlas_client, prompt, ...):
    # 原来的同步逻辑：generate_video(...) + poll_prediction(...)
    ...
```
> 本仓已对 `AtlasCloud Seedance 2.0 Fast Text-to-Video`
> （`nodes/video/bytedance_seedance_2_0_fast_t2v.py`）按此模式改造。
> **其它视频节点照同一模式改即可获得并行能力。**

## 文件
| 文件 | 用途 | 怎么用 |
|---|---|---|
| `3x_parallel_t2v.workflow.json` | **画布格式**（litegraph） | ComfyUI 网页里直接把文件拖进画布 / 菜单 Open |
| `3x_parallel_t2v.api.json` | **API 格式** | `POST /prompt`，见下方 curl |

两个文件都是：1 个 `AtlasCloud Client` → 3 个独立的 `Seedance 2.0 Fast Text-to-Video`（不同 prompt）→ 3 个 `PreviewAny`。

### API 方式直接测
```bash
# 先把 api.json 里的 <把这里换成你们的 AtlasCloud apikey> 替换成真实 apikey
curl -s http://127.0.0.1:8188/prompt \
  -H 'Content-Type: application/json' \
  -d "{\"prompt\": $(cat 3x_parallel_t2v.api.json)}"
```

## 实测证据（看时间戳日志即可判断是否真并行）
节点里加了时间戳日志（`[AtlasParallel]`）。**并行**时几条 `SUBMIT` 会紧挨着出现
（先都提交，再各自等结果）；**串行**则是「一个 DONE 了才下一个 SUBMIT」。

2 节点实测（ComfyUI 控制台日志）：
```
⏱ SUBMIT   红色跑车      ┐ 两个几乎同时提交
⏱ SUBMIT   熊猫          ┘
↑ SUBMITTED 熊猫 (+0.5s)
↑ SUBMITTED 跑车 (+0.6s)
✅ DONE     跑车 total=122.6s
✅ DONE     熊猫 total=123.1s
→ 工作流墙钟总耗时 123.1s ≈ max(122.6, 123.1)，而不是 245s
```

## 扩展到 N 个
照例子加更多「`Client` 输出 → 第 N 个视频节点 → `PreviewAny`」即可，节点之间不要互相连依赖
（一旦 B 的输入接了 A 的输出，B 必须等 A，就退回串行）。

## 注意事项
- **真正的并发上限**取决于：① 你账号在 AtlasCloud 侧的并发配额；② 线程池大小
  （`run_in_executor` 默认线程池，节点很多时建议显式配一个够大的 `ThreadPoolExecutor`）。
- 每个视频节点 = 一次独立的 MaaS 计费；并行只是「同时发起」，不改变计费条数。
- 节点里那段 `[AtlasParallel]` 时间戳 `print` 仅为演示/排查用，正式可降级为 logging 或删掉。
