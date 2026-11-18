# 01. Clarify

## 目标与成功判据

产出「Octop 整体架构」的可视化说明，供人阅读与评审：

- 在已有权威文档 `docs/architecture.md` 中补充系统上下文（C4-L1）与组件视图（C4-L2）的 Mermaid 图，并与现有分层、进程模型、交互面、存储章节相互引用，不新建重复文档（避免双轨）。
- 图形与文字必须来自本仓库实际代码与既有文档，不臆造组件、端口、外部依赖。
- 对话中给出中文解读，说明入口、运行时对象树、请求路径、扩展面与边界。

成功判据：

1. `docs/architecture.md` 新增图与正文一致，Mermaid 语法可渲染，无悬空链接。
2. 图中每个组件都能在 `src/octop/` 或 `dashboard/` 找到对应实现位置，关键路径在 Plan/Implement 中给出文件级依据。
3. 仅文档变更，不改变运行行为、接口、配置与数据结构。

## 范围、约束与依赖

- 范围：`docs/architecture.md`；必要时在 Overview/README 索引处同步一行链接（若已有索引缺失）。
- 非范围：代码、API、配置、数据库迁移、构建脚本、`AGENTS.md` 规则正文。
- 约束：沿用仓库文档语言（英文）与既有章节结构；不得复制 AGENTS.md 的 agent 规则手册内容。
- 依赖：`docs/architecture.md`、`AGENTS.md` 模块边界、`src/octop/infra/server.py`、`src/octop/launch.py`、`src/octop/api/app.py`、`src/octop/infra/gateway/`、`dashboard/src/`。

## 问题与决策

| # | 问题 | 决策 | 依据 |
|---|------|------|------|
| 1 | 交付形态：仅对话解释 / 新增文档 / 更新现有权威文档 | 更新 `docs/architecture.md` 并在对话中中文解读 | 该文件已是 human-readable overview；新增文档会形成双轨，违反「更新权威文档，避免双轨」 |
| 2 | 文档语言 | 英文（与 `docs/` 其他文件一致），对话中文 | 安装语言 zh 只约束 SOP 产物，不改变仓库既有文档语言 |
| 3 | 图的形式 | Mermaid 代码块（GitHub 可渲染），辅以文字说明 | 无新增依赖、可 diff、可评审 |
| 4 | 是否包含部署拓扑 | 仅说明单进程/单 wheel 与可选反向代理位置，不虚构生产拓扑 | 仓库未声明具体部署环境，`.wally/config.json` 的 deploy/it 均为空 |

未决问题：无阻塞项。若用户需要单独的 PPT/图片版架构图，属于新需求，需另行授权。

## 缺陷 / 性能输入（适用时）

不适用：非 Bug、非性能任务。

## 完成结论

目标可验证（文档图与代码位置一致、仅文档 diff）；关键假设已记录；风险为「描述与实现漂移」，通过 Plan 中的文件级核对缓解。
