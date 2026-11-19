# Technical Debt Register

Tracked debt items that are accepted for now and guarded in CI. This register
is the source of truth for the module-size allowance list in
`scripts/check_module_size.py`; keep both in sync.

Rules:

- Every entry has an owner, a target date, and written acceptance criteria.
- A listed module is frozen at the recorded size: it may shrink, never grow.
- Debt is reviewed at each release; completed items move to "Resolved" and are
  removed from the allowance list.

## Open items

### TD-001 · `feishu_bot_creator.py` exceeds the 1000-line budget

| Field | Value |
|-------|-------|
| Module | `src/octop/infra/gateway/bot_creators/feishu_bot_creator.py` |
| Current size | 1484 lines (2026-11-19, commit `89a652f`) |
| Owner | octop maintainers (named owner to be confirmed) |
| Target date | 2026-12-31 |
| Status | Accepted, frozen ceiling 1484 |

Why defer: the module mixes Feishu app provisioning, avatar/greeting side
effects, progress event emission and local state persistence. Splitting it
needs a live Feishu sandbox to re-verify bot creation, which is outside the
scope of the maintainability remediation batch.

Acceptance: extract the pure helpers (state file, logging/event emission,
HTTP calls) into `feishu_bot_steps.py` or similar, leaving the orchestrator
under 1000 lines; `make check-module-size` passes without an allowance entry;
existing bot-creation tests still pass.

### TD-002 · `skills_hub.py` exceeds the 1000-line budget

| Field | Value |
|-------|-------|
| Module | `src/octop/infra/agents/skills_hub.py` |
| Current size | 1263 lines (2026-11-19, commit `89a652f`) |
| Owner | octop maintainers (named owner to be confirmed) |
| Target date | 2026-12-31 |
| Status | Accepted, frozen ceiling 1263 |

Why defer: the module combines the HTTP client (timeout/retry/backoff, URL
building) with bundle resolution, tree sanitisation and local skill
installation. The client half has no dependency on agent state and can move
without behavioural change, but it needs its own test pass.

Acceptance: split the HTTP client and URL/backoff helpers into a dedicated
module, leaving `skills_hub.py` under 1000 lines; no allowance entry; skill
search/install tests still pass.

### TD-003 · `agents/manager.py` exceeds the 1000-line budget

| Field | Value |
|-------|-------|
| Module | `src/octop/infra/agents/manager.py` |
| Current size | 1123 lines (2026-11-19, commit `89a652f`) |
| Owner | octop maintainers (named owner to be confirmed) |
| Target date | 2026-12-31 |
| Status | Accepted, frozen ceiling 1123 |

Why defer: `AgentManager` is the process-wide registry and its methods touch
the harness runtime, repos, providers, security and ACP settings. Extracting
CRUD or runtime access needs a careful pass over its lock/ordering semantics.

Acceptance: move runtime access (`get_agent`, `stream`, `call`, HITL resume)
into a collaborator object or mixin, leaving the registry under 1000 lines;
no allowance entry; agent CRUD/stream tests still pass.

## Resolved

_None yet._
