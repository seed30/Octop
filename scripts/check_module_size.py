"""Module size budget guard for Octop source modules.

Enforces a per-file line budget on first-party modules under ``src/octop``.
Existing oversized modules are frozen at their current size (they may shrink
but not grow); anything new above the budget fails ``make lint``.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

DEFAULT_THRESHOLD = 1000
SOURCE_GLOB = "src/octop/**/*.py"

# Relative POSIX paths are stable across platforms and sort orders.
SKIP_PATH_PREFIXES = (
    "src/octop/dashboard/",
    "src/octop/infra/agents/experts/library/",
    "src/octop/infra/agents/subagents/library/",
)

# Frozen debt: current size is the ceiling. Keep in sync with docs/tech-debt.md.
ALLOWANCES: dict[str, int] = {
    "src/octop/infra/gateway/bot_creators/feishu_bot_creator.py": 1484,
    "src/octop/infra/agents/skills_hub.py": 1263,
    "src/octop/infra/agents/manager.py": 1123,
}


@dataclass(frozen=True)
class Violation:
    path: str
    lines: int
    limit: int


def _count_lines(path: Path) -> int:
    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        return sum(1 for _ in handle)


def _is_skipped(rel: str) -> bool:
    return any(rel.startswith(prefix) for prefix in SKIP_PATH_PREFIXES)


def collect_violations(
    root: Path,
    threshold: int = DEFAULT_THRESHOLD,
    allowances: dict[str, int] | None = None,
) -> list[Violation]:
    """Return modules that exceed their budget, sorted by path."""
    limits = ALLOWANCES if allowances is None else allowances
    violations: list[Violation] = []
    for path in sorted((root / "src" / "octop").glob("**/*.py")):
        rel = path.relative_to(root).as_posix()
        if _is_skipped(rel):
            continue
        lines = _count_lines(path)
        limit = limits.get(rel, threshold)
        if lines > limit:
            violations.append(Violation(path=rel, lines=lines, limit=limit))
    return violations


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check Octop module line budgets.")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository root (defaults to the parent of scripts/).",
    )
    args = parser.parse_args(argv)
    violations = collect_violations(args.root)
    if not violations:
        print(f"OK: no module exceeds {DEFAULT_THRESHOLD} lines (or its frozen budget).")
        return 0
    for violation in violations:
        print(
            f"FAIL: {violation.path} has {violation.lines} lines "
            f"(limit {violation.limit}); split it or record it in docs/tech-debt.md."
        )
    return 1


if __name__ == "__main__":
    sys.exit(main())
