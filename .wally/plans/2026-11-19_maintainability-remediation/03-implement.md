# 03. Implement + UT + Docs

## 实际改动与 Plan 差异

| 文件 | 状态 | 行数 |
|------|------|------|
| `scripts/check_module_size.py` | 新增 | 90 |
| `tests/unit/test_module_size.py` | 新增 | 75 |
| `docs/tech-debt.md` | 新增 | 75 |
| `AGENTS.md` | +14 行（§5 新增 Module size budget） | — |
| `Makefile` | +7 行（`check-module-size` + `lint` 接入） | — |

与 Plan 差异：无。未拆分任何业务模块，未改运行时逻辑。

## Red → Green → Refactor

**Red**（先写测试 + 空实现 `collect_violations` 返回 `[]`）：

```
python3 -m unittest tests.unit.test_module_size -v
FAIL: test_one_over_threshold_fails / test_allowlisted_file_growing_fails
AssertionError: 0 != 1
Ran 7 tests — FAILED (failures=2), exit 1
```

失败来自预期断言（应报违规却返回 0），不是导入/语法错误。

**Green**（实现扫描、白名单冻结、排除规则）：

```
python3 -m unittest tests.unit.test_module_size -v
Ran 7 tests in 0.016s
OK, exit 0
```

**Refactor**：未做，实现已是最小结构；无重复逻辑。

## UT 与增量覆盖率

- 用例：U1 小文件通过、U2 恰好 1000 行通过、U3 1001 行失败、U4 白名单内通过、U5 白名单增长失败、U6 library 排除、U7 当前仓库自检通过。全部通过。
- 入口：标准库 `unittest`（项目 pytest 不可用，见环境限制）；pytest 可收集同类用例。
- 覆盖率数值：**未验证**（宿主无 pytest/pytest-cov/coverage，无法生成增量报告）。已用 U1–U7 覆盖脚本的全部分支：阈值比较两侧、白名单命中/未命中/增长、排除路径、真实仓库路径；未测 `--root` 参数错误路径。
- 回归：未触碰业务代码，无既有行为回归面；脚本对当前仓库输出 `OK`，说明白名单与真实行数一致。

补充命令证据（2026-11-19）：

```
$ python3 scripts/check_module_size.py
OK: no module exceeds 1000 lines (or its frozen budget). exit 0

$ python3 scripts/check_module_size.py --root /tmp/guard-demo   # 新增 1001 行文件
FAIL: src/octop/new_mod.py has 1001 lines (limit 1000); ... exit 1

# 同目录再加入 2000 行 library 文件后，仍只报告上面一条 → 排除生效
```

## 缺陷回归（适用时）

对应体检 GAP：模块规模无阈值、无债登记。回归断言：

- 新增超限文件 → 退出 1（U3 + 手工 demo）。
- 存量白名单增长 → 退出 1（U5）。
- 当前仓库（含三个存量文件）→ 退出 0（U7 + `make check-module-size`）。

`make -n lint` 显示执行顺序：ruff check → ruff format --check → `python3 scripts/check_module_size.py`，确认已接入 CI 使用的 `make lint`。

限制：完整 `make lint` 未通过，原因是仓库既有的 `ruff format --check` 在本地 ruff 0.16.3 下有 60 个文件待格式化（uv.lock 锁定 0.15.20），与本次改动无关，见上一轮体检记录 `quality.style` unverified。

## Docs

- 新增 `docs/tech-debt.md`：TD-001/002/003，各含 owner、目标日期、暂缓理由、验收、冻结上限；与脚本 `ALLOWANCES` 一一对应。
- `AGENTS.md` §5 增加阈值与豁免规则，并链接债登记。
- 未更新 README/CHANGELOG：无用户可见行为变化，工具门禁属开发流程；按 CONTRIBUTING，仅用户可见变更需改 CHANGELOG。

## 增量 CR

- 规则：`AGENTS.md` 模块边界、`CONTRIBUTING.md` PR 要求、体检验收条件。
- diff 范围：5 个文件，+240 行，无删除、无依赖变更。
- 自查：脚本只读、无网络、无写文件；路径使用 POSIX 相对路径，Windows 可运行；排除目录避免误伤生成/第三方内容；白名单上限与 `wc -l` 实测一致。
- 发现并修复：无。首版实现即按排序输出与 POSIX 相对路径处理；复核未发现需修改项。
- 未解决风险：owner 为角色占位、目标日期待确认；覆盖率数值未测。

## 完成结论

- TDD：通过（真实断言 Red → Green）。
- 覆盖率：未验证（工具缺失），已说明覆盖分支与缺口。
- Docs：通过（债登记 + 规则）。
- 增量 CR：通过（单一批次、5 文件、无运行时改动）。
- 无适用门禁失败；Deploy/IT 按配置自动 SKIPPED。
