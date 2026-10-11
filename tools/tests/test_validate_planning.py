"""Exercise valid planning and intentional failures in disposable copies."""

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from validate_planning import validate


class PlanningValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repo"
        source = Path(__file__).resolve().parents[2]
        shutil.copytree(source, self.root, ignore=shutil.ignore_patterns(".git", "__pycache__"))

    def change_registry(self, before, after):
        path = self.root / "TASK_REGISTRY.md"
        text = path.read_text(encoding="utf-8")
        self.assertIn(before, text)
        path.write_text(text.replace(before, after, 1), encoding="utf-8")

    def assert_error(self, fragment):
        self.assertTrue(any(fragment in error for error in validate(self.root)))

    def test_valid_foundation(self):
        self.assertEqual(validate(self.root), [])

    def test_missing_document_and_broken_link(self):
        (self.root / "docs/SECURITY.md").unlink()
        self.assert_error("Missing required file: docs/SECURITY.md")
        self.assert_error("Broken local link")

    def test_link_cannot_escape_repository(self):
        with (self.root / "README.md").open("a", encoding="utf-8") as handle:
            handle.write("\n[escape](../outside.md)\n")
        self.assert_error("Link escapes repository")

    def test_duplicate_task(self):
        path = self.root / "TASK_REGISTRY.md"
        row = next(line for line in path.read_text().splitlines() if line.startswith("| NS-020 |"))
        with path.open("a") as handle:
            handle.write("\n" + row + "\n")
        self.assert_error("Duplicate task ID: NS-020")

    def test_unknown_dependency(self):
        self.change_registry("| NS-011 | Login/recovery", "| NS-999 | Login/recovery")
        self.assert_error("Unknown dependency: NS-020 -> NS-999")

    def test_dependency_cycle(self):
        self.change_registry("| NS-010 | Extension available", "| NS-020 | Extension available")
        self.assert_error("Dependency cycle")

    def test_completion_requires_evidence_and_dependencies(self):
        self.change_registry("| planned | unassigned | NS-011 |", "| verified_complete | unassigned | NS-011 |")
        self.assert_error("Completed task lacks evidence: NS-020")
        self.assert_error("Completed task has unfinished dependency: NS-020")

    def test_invalid_status(self):
        self.change_registry("| planned | unassigned | NS-011 |", "| done | unassigned | NS-011 |")
        self.assert_error("Invalid status: NS-020: done")

    def test_feature_coverage(self):
        self.change_registry("| AI integration |", "| Placeholder |")
        self.assert_error("Missing feature coverage: NS-060")

    def test_roadmap_reference(self):
        with (self.root / "docs/ROADMAP.md").open("a") as handle:
            handle.write("\nNS-999\n")
        self.assert_error("Roadmap references unknown task: NS-999")


if __name__ == "__main__":
    unittest.main()
