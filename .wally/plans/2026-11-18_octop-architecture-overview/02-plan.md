# 02. Plan

## 方案与改动范围

目标文件：`docs/architecture.md`（唯一生产文档改动）。

新增两个章节（编号接在现有 6 之后，避免重排既有章节与外部锚点）：

- `## 7. System context (C4-L1)`：Mermaid `flowchart`，画用户/浏览器/IM 平台/LLM Provider/本地文件系统与 `Octop` 单进程边界；标注所有外部依赖。
- `## 8. Component view (C4-L2)`：Mermaid `flowchart`，画进程内组件：`launch.run_foreground_blocking` → `api/app.build_app` → `OctopServer.start()` 启动的 `AppRuntime`（AgentManager / Gateway / CronManager / UserManager / ProactiveCareScheduler），gateway 下的 `ChannelManager`、`WebSocketHub`、`GlobalProcessor`、`SlashDispatcher`，以及 `SharedServices`→SQLite、`BackendWorkspace`→文件/远端存储。
- 可选 `## 9. Request path`：一条 WebSocket 聊天请求的时序（`sequenceDiagram`），从 dashboard 到 `AgentManager.stream` → `HarnessAgent` → `GlobalProcessor` → WS 回推。

文件级依据（均已在本任务阅读）：

| 组件 | 位置 |
|------|------|
| 进程编排/singleton 装配 | `src/octop/infra/server.py:43` `OctopServer`，`:32` `AppRuntime` |
| HTTP/WS app 构建 | `src/octop/api/app.py:52` `build_app` |
| 路由挂载 | `src/octop/api/routers/*`（41 个模块，见目录） |
| Gateway 外观 | `src/octop/infra/gateway/gateway.py:83` `Gateway`（`ws_hub`/`cli_hub`/`channel_manager`/`slash_dispatcher`/`processor`） |
| Agent 注册表 | `src/octop/infra/agents/manager.py:94` `AgentManager`（`get_agent` → `HarnessAgent`，`stream`/`call`） |
| 库依赖 | `pyproject.toml`：`fastapi`、`uvicorn`、`apscheduler`、`orcakit-harness-agent`、`harness-gateway` |
| Dashboard | `dashboard/src/routes/index.tsx`、`dashboard/src/pages/*` |
| CLI | `src/octop/cli/main.py`、`src/octop/cli/commands/*` |

风险等级：**低**。纯文档、可逆、不改外部契约、不改数据结构。依据：diff 仅 Markdown。

## 调用链与兼容性

- 无状态机/重试/副作用挂点改动；无协议、schema、配置变更。
- 兼容性：不删除、不重排既有章节；仅追加章节，现有锚点与外部链接保持有效。新图引用的路径必须已存在。
- 回滚：`git checkout -- docs/architecture.md` 即可完全回滚。

## UT 设计

不适用（文档任务）。按 gates「文档类任务不伪造 Red/Green」，不生成 Red→Green 记录。

替代验证（静态、可复核）：

| 编号 | 检查 | 命令 | 预期 |
|------|------|------|------|
| D1 | Mermaid 围栏成对 | `grep -c '^```mermaid'` == `grep -c '^```$'` 的对应数量 | 围栏闭合 |
| D2 | 图内引用的代码路径存在 | 对每个 `src/...`/`dashboard/...` 路径 `test -e` | 全部存在 |
| D3 | 无悬空相对链接 | 提取 `](./...)` 链接并 `test -e` | 全部存在 |
| D4 | 变更范围 | `git diff --stat` | 仅 `docs/architecture.md`（任务产物除外） |

## IT 设计（六步适用）

按 `execution.json`：`it.command` 与 `it.guide` 均为空 → 自动 SKIPPED，不准备环境、不执行 runner、不做环境级 A/B。D1–D4 属于文档静态校验，在 Implement 阶段执行，不替代 IT。

## 风险与完成结论

- 主要风险：架构描述与实现漂移。缓解：只写已核对的文件/类；图与现有正文交叉引用；不虚构部署拓扑。
- 未覆盖边界：不包含每个 router 的端点清单（见 `docs/api.md`）、不包含 harness 库内部实现（外部依赖，仅画边界）。
- 授权：仅本地文档编辑；Commit/Push 未授权，Review 阶段只做提交准备。
- 测试设计先于实现：是（D1–D4 在写文档前确定）。
