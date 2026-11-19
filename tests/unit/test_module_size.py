"""Unit tests for the module-size budget guard (stdlib unittest, pytest-compatible)."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import check_module_size as guard  # noqa: E402


def _write(root: Path, rel: str, lines: int) -> Path:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("x = 1\n" * lines, encoding="utf-8")
    return path


class ModuleSizeGuardTest(unittest.TestCase):
    def test_small_file_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write(root, "src/octop/small.py", 3)
            self.assertEqual(guard.collect_violations(root), [])

    def test_exactly_at_threshold_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write(root, "src/octop/edge.py", guard.DEFAULT_THRESHOLD)
            self.assertEqual(guard.collect_violations(root), [])

    def test_one_over_threshold_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write(root, "src/octop/big.py", guard.DEFAULT_THRESHOLD + 1)
            violations = guard.collect_violations(root)
            self.assertEqual(len(violations), 1)
            self.assertIn("big.py", violations[0].path)
            self.assertEqual(violations[0].limit, guard.DEFAULT_THRESHOLD)

    def test_allowlisted_file_within_ceiling_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rel = "src/octop/legacy.py"
            allowances = {rel: 1500}
            _write(root, rel, 1484)
            self.assertEqual(guard.collect_violations(root, allowances=allowances), [])

    def test_allowlisted_file_growing_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rel = "src/octop/legacy.py"
            allowances = {rel: 1500}
            _write(root, rel, 1501)
            violations = guard.collect_violations(root, allowances=allowances)
            self.assertEqual(len(violations), 1)
            self.assertEqual(violations[0].limit, 1500)

    def test_generated_library_is_excluded(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write(root, "src/octop/infra/agents/experts/library/big.py", 2000)
            _write(root, "src/octop/infra/agents/subagents/library/big.py", 2000)
            self.assertEqual(guard.collect_violations(root), [])

    def test_current_repository_passes(self) -> None:
        self.assertEqual(guard.collect_violations(REPO_ROOT), [])


if __name__ == "__main__":
    unittest.main()
