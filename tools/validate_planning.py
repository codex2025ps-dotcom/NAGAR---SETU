"""Offline checks for the planning foundation; not an application/security audit."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

REQUIRED = (
    "README.md", "AGENTS.md", "PROJECT_STATE.md", "TASK_REGISTRY.md",
    "DECISIONS.md", "docs/ARCHITECTURE.md", "docs/ROADMAP.md",
    "docs/SECURITY.md", "docs/CODING_STANDARDS.md", "docs/TESTING.md",
    "docs/OPERATIONS.md", ".gitignore", "tools/validate_planning.py",
    "tools/tests/test_validate_planning.py", ".github/workflows/planning.yml",
)
STATUSES = {"planned", "in_progress", "blocked", "ready_for_review", "verified_complete"}
FEATURES = {
    "NS-010": "backend", "NS-011": "postgis", "NS-020": "authentication",
    "NS-030": "profiles", "NS-031": "discovery", "NS-032": "admin",
    "NS-040": "deals", "NS-050": "mobile", "NS-060": "ai integration",
    "NS-070": "security",
}


def validate(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    texts: dict[str, str] = {}
    for relative in REQUIRED:
        path = root / relative
        if not path.is_file():
            errors.append(f"Missing required file: {relative}")
    for path in sorted(root.rglob("*.md")):
        if any(part in {".git", "node_modules", "work"} for part in path.relative_to(root).parts):
            continue
        relative = str(path.relative_to(root))
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeError:
            errors.append(f"Invalid UTF-8: {relative}")
            continue
        texts[relative] = text
        if not text.strip():
            errors.append(f"Empty document: {relative}")
        # Inline Markdown file links only; fenced examples are not document links.
        prose = re.sub(r"```.*?```", "", text, flags=re.S)
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", prose):
            target = target.strip().split(" ", 1)[0].strip("<>")
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            destination = (path.parent / unquote(parsed.path)).resolve()
            if not destination.is_relative_to(root):
                errors.append(f"Link escapes repository: {relative}: {target}")
            elif not destination.exists():
                errors.append(f"Broken local link: {relative}: {target}")

    rows: dict[str, list[str]] = {}
    for line in texts.get("TASK_REGISTRY.md", "").splitlines():
        if not re.match(r"\|\s*NS-\d+\s*\|", line):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 8:
            errors.append(f"Task row requires 8 columns: {line}")
            continue
        task_id, phase, task, status, owner, deps, acceptance, evidence = cells
        if task_id in rows:
            errors.append(f"Duplicate task ID: {task_id}")
        rows[task_id] = cells
        if status not in STATUSES:
            errors.append(f"Invalid status: {task_id}: {status}")
        if not re.fullmatch(r"P[0-7]", phase):
            errors.append(f"Invalid phase: {task_id}: {phase}")
        if not owner or not acceptance or not task:
            errors.append(f"Missing task metadata: {task_id}")
        if status == "verified_complete" and (
            evidence in {"", "-"} or re.search(r"pending|not run|unverified", evidence, re.I)
        ):
            errors.append(f"Completed task lacks evidence: {task_id}")
    if "NS-001" not in rows:
        errors.append("Missing planning task: NS-001")
    for task_id, keyword in FEATURES.items():
        if task_id not in rows or keyword not in rows[task_id][2].lower():
            errors.append(f"Missing feature coverage: {task_id}: {keyword}")

    graph: dict[str, list[str]] = {}
    for task_id, cells in rows.items():
        dep_text = cells[5]
        deps = [] if dep_text == "-" else [dep.strip() for dep in dep_text.split(",")]
        graph[task_id] = deps
        for dep in deps:
            if dep not in rows:
                errors.append(f"Unknown dependency: {task_id} -> {dep}")
            elif cells[3] == "verified_complete" and rows[dep][3] != "verified_complete":
                errors.append(f"Completed task has unfinished dependency: {task_id} -> {dep}")
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(task_id: str) -> None:
        if task_id in visiting:
            errors.append(f"Dependency cycle at: {task_id}")
            return
        if task_id in visited:
            return
        visiting.add(task_id)
        for dep in graph.get(task_id, []):
            if dep in graph:
                visit(dep)
        visiting.remove(task_id)
        visited.add(task_id)

    for task_id in graph:
        visit(task_id)
    for task_id in set(re.findall(r"NS-\d+", texts.get("docs/ROADMAP.md", ""))):
        if task_id not in rows:
            errors.append(f"Roadmap references unknown task: {task_id}")
    return errors


def main() -> int:
    errors = validate(Path(__file__).resolve().parents[1])
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("PASS: required files, local links, task metadata/dependencies and feature coverage")
    print("Scope: planning consistency only; application and security checks are not implemented.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
