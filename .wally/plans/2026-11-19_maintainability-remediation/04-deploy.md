# 04. Deploy

## 执行状态

- Status: SKIPPED
- Reason: 客户未配置执行方法，自动跳过；未执行或验证。
- Configuration snapshot: `./execution.json` → `deploy`
- Skip decision at task creation: 2026-11-19 15:41:54+08:00


读取本任务 `execution.json` 的 deploy 配置。command 与 guide 都为空时自动 SKIPPED，保留原因与零耗时记录；已配置则按客户方法执行。缺工具/权限/环境或执行失败不能自动跳过。

## 环境与部署范围

资源归属、代码版本、组件、配置、授权范围。

## 缺陷基线（适用时）

热更前 A 的版本、输入状态和留存证据；无法真跑的原因及等价历史证据。

## 执行与生效

实际命令、就绪结果、生效验证、失败处理；使用项目配置中的操作指引。

## 回滚与资源处置

回滚版本、命令、触发条件；环境保留/释放约定。

## 完成结论

SKIPPED：deploy 未配置，未准备环境、未部署、未验证；本任务仅本地工具与文档，无部署对象。
