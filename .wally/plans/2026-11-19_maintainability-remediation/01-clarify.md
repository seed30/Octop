# 01. Clarify

## 目标与成功判据

修复体检项 `quality.maintainability`（target `octop`，原始提交 `89a652f`）。

体检结论：三个非生成模块超过 1100 行，且仓库没有技术债登记、责任人或整改计划。

成功判据（对应体检验收）：

1. 每个 >1000 行的模块要么被拆分，要么有可追踪的债条目，条目包含 owner、目标日期、验收条件。
2. 仓库存在明确的模块规模阈值，新增模块超过阈值必须有理由。
3. 阈值有可重复执行的本地守卫，CI/`make lint` 能拦截新增超限，且不误伤存量豁免。
4. 复检 `quality.maintainability` 可凭本地文件和命令输出判 pass。

## 范围、约束与依赖

- 改动范围：
  - 新增 `docs/tech-debt.md`（三个存量模块的债条目）
  - `AGENTS.md` §5 增加 1000 行阈值与豁免规则
  - 新增 `scripts/check_module_size.py`（标准库，无第三方依赖）
  - `Makefile` 的 `lint` 接入规模检查
  - 新增 `tests/unit/test_module_size.py`（标准库 unittest，可被 pytest 收集）
- 非范围：不拆分三个业务模块（体检验收允许“登记债”路径）；不改业务逻辑、API、依赖。
- 约束：脚本仅标准库；排除 `src/octop/infra/agents/{experts,subagents}/library` 与 `src/octop/dashboard` 等生成/第三方内容；不引入新依赖；不改变现有 lint/CI 失败语义。
- 依赖：现有 `Makefile` 的 `$(PYTHON)`、`src/octop` 目录结构、`AGENTS.md` 边界章节。

## 问题与决策

| # | 问题 | 决策 | 依据 |
|---|------|------|------|
| 1 | 选择拆分还是登记债 | 登记债 + 阈值守卫（最小整改） | 体检验收明确允许二者其一；拆分飞书/技能/Hub 模块需要外部联调回归，超出单次整改最小范围 |
| 2 | 阈值取值 | 1000 行 | 体检以 1000 为“可接受上限”边界，三个文件均超限且被点名 |
| 3 | 存量处理 | 白名单按“只减不增”冻结（1484/1263/1123） | 避免历史文件立即让门禁失败，同时阻止继续增长 |
| 4 | 守卫运行位置 | `make lint` 内调用 + 独立 target | CI 已运行 `make lint`，无需改 workflow 即可生效 |
| 5 | 债条目 owner | 暂记 `octop maintainers`（角色），目标日期 2026-12-31 | 仓库无 CODEOWNERS/具名维护者；需在 Review 时请用户确认具体责任人与日期 |

未决/待确认：具名 owner 与目标日期需用户确认；若用户指定，仅替换 `docs/tech-debt.md` 两列，不改结构。

## 缺陷 / 性能输入（适用时）

问题判据：模块行数 > 1000 且无债登记/守卫。

当前版本复核（2026-11-19，`feature/maintainability-remediation` 起点 `89a652f`）：

```
1484 src/octop/infra/gateway/bot_creators/feishu_bot_creator.py
1263 src/octop/infra/agents/skills_hub.py
1123 src/octop/infra/agents/manager.py
```

`docs/tech-debt.md` 不存在；`AGENTS.md`、`Makefile` 中无 1000 行阈值或 tech-debt 引用。原问题仍存在，未重复修复。

环境限制：宿主 Python 3.11.6，无 uv/pytest 依赖；新增守卫与测试仅使用标准库，可直接用 `python3` 运行。

## 完成结论

目标可验证：文件存在性、阈值文本、脚本正/负用例、`make lint` 接入、复检结论均有本地命令证据。风险：owner/日期为待确认的占位角色信息。
