# 02. Plan

## 方案与改动范围

| 文件 | 改动 |
|------|------|
| `scripts/check_module_size.py`（新增） | 标准库扫描器：统计 `src/octop/**/*.py` 行数；超过 1000 行且不在白名单则报错；白名单模块超过冻结上限（只减不增）也报错；退出码 1 |
| `tests/unit/test_module_size.py`（新增） | unittest 用例，覆盖阈值边界、白名单冻结、排除目录、当前仓库自检 |
| `Makefile` | 新增 `check-module-size` target，并挂到 `lint` 的 ruff 之后 |
| `AGENTS.md` §5 | 新增 “Module size budget”：1000 行阈值、超限须在 PR 说明并登记 `docs/tech-debt.md`、白名单只减不增 |
| `docs/tech-debt.md`（新增） | 三个存量模块的债条目：owner、目标日期、暂缓拆分理由、验收、守卫上限 |

风险等级：**低-中**。新增构建门禁可能因误判阻断 lint；通过排除目录、按仓库根解析、单测覆盖边界缓解。可逆：删除 target 即可恢复，不影响运行时代码。

## 调用链与兼容性

- `make lint`：`ruff check` → `ruff format --check` → `python3 scripts/check_module_size.py`。任一步非零则 make 失败，符合现有 fail-fast 语义。
- CI 无需改动：`.github/workflows/ci.yml` 已执行 `make lint`。
- 脚本无网络、无写入、只读源码；无协议/数据/配置变更。
- 白名单按仓库相对路径匹配（`/` 分隔），在 Linux/macOS/Windows 一致；CI 的 Windows job 同样可运行。
- 回滚：`git revert` 单个提交即可；不影响产物。

## UT 设计

测试位置：`tests/unit/test_module_size.py`，`python3 -m unittest` 可直接运行（不依赖第三方库），pytest 亦可收集。

| 编号 | 输入 | 预期 |
|------|------|------|
| U1 | 3 行文件，阈值 1000 | 无 violation，退出 0 |
| U2 | 1000 行文件（等于阈值） | 通过（边界含等号） |
| U3 | 1001 行新文件 | 1 条 violation，退出 1 |
| U4 | 白名单文件 1484 行，上限 1484 | 通过 |
| U5 | 白名单文件 1485 行（增长） | violation，退出 1 |
| U6 | `infra/agents/experts/library/x.py` 2000 行 | 排除，通过 |
| U7 | 当前仓库真实根目录 | 无 violation（存量与白名单一致） |

Unicode：路径与输出均为 ASCII/UTF-8，不涉及用户数据；不额外设计 Unicode 用例。

## IT 设计（六步适用）

`execution.json` 的 `it.command`/`it.guard` 为空 → 自动 SKIPPED。U1–U7 属于单元/脚本级验证，不替代集成测试。复检修复版本由体检流程完成，不在本任务内执行外部评分器。

## 风险与完成结论

- 关键决定：登记债优先于拆分；白名单固化当前行数，防止“边登记边增长”。
- 未覆盖边界：未拆分业务模块；`feishu_bot_creator.py` 等仍超 1000 行，属已接受存量。
- 待确认：`docs/tech-debt.md` 的具名 owner 与目标日期（当前为角色 + 2026-12-31），Review 时请用户确认。
- 授权：仅本地修改与测试；Commit/Push 需另行授权。
- 测试设计先于实现：是（U1–U7 在实现前固定）。
