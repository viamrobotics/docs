#!/usr/bin/env python3
"""
Check docs for known-wrong UI labels that don't match the Viam app source.

Each rule in RULES is a label error found during UI-flow verification. The
authoritative labels live in flow documents under ~/viam/code-map/ui-flows/.

Usage:
    python3 scripts/check-ui-labels.py                      # scan docs/
    python3 scripts/check-ui-labels.py path/to/page.md ...  # scan named files
    python3 scripts/check-ui-labels.py --staged             # scan staged .md files

Escape hatch: add `<!-- ui-check-ignore -->` to the end of a line to suppress
the check on that line. Use only when the line is referencing the wrong label
on purpose (for example, a common-mistakes callout).

Exit 0 when clean, 1 when violations found.
"""

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Rule:
    """A single UI-label rule.

    pattern: regex applied to each line (case-sensitive unless ignore_case)
    reason: short explanation including the correct label
    context: optional regex that must also match within [-3, +3] lines of the
             hit to reduce false positives (e.g., 'GetPointCloud' is a valid
             camera API method but wrong as a data-capture Method value)
    """

    pattern: str
    reason: str
    context: str | None = None
    ignore_case: bool = False


RULES: list[Rule] = [
    # --- configure-trigger flow ---
    Rule(
        pattern=r"\bnotification frequency\b",
        reason='UI label is "Alert frequency" (ALERT OPTIONS section on the trigger card). Flow: configure-trigger.md',
        ignore_case=True,
    ),
    Rule(
        pattern=r"\bNOTIFICATIONS\b\s+section",
        reason='Trigger card section is "ALERT OPTIONS", not "NOTIFICATIONS". Flow: configure-trigger.md',
    ),
    Rule(
        pattern=r"\bTrigger type\b",
        reason='Trigger-card field label is just "Type" (inside the EVENT section). Flow: configure-trigger.md',
        context=r"\b(Set|select|dropdown|EVENT section|field)\b",
    ),
    Rule(
        pattern=r"\bData type\b(?!s)",
        reason='Trigger-card field label is "Data Types" (plural). Flow: configure-trigger.md',
        context=r"\btrigger|EVENT section|PART_DATA_INGESTED|Data has been synced\b",
        ignore_case=False,
    ),
    Rule(
        pattern=r"\bData ingested\b",
        reason='Trigger type label is "Data has been synced to the cloud", not "Data ingested". Flow: configure-trigger.md',
    ),
    Rule(
        pattern=r"\bCloud sync\b",
        reason='Trigger type label is "Data has been synced to the cloud", not "Cloud sync". Flow: configure-trigger.md',
        context=r"\btrigger\b",
        ignore_case=True,
    ),
    # --- connect-and-get-api-keys flow ---
    Rule(
        pattern=r"\bGenerate machine key\b",
        reason='Button label is "Generate API key", not "Generate machine key". Flow: connect-and-get-api-keys.md',
    ),
    # --- add-configuration-block flow ---
    Rule(
        pattern=r"\*\*Component or service\*\*",
        reason='Menu item is "Configuration block", not "Component or service" (retired label). Flow: add-configuration-block.md',
    ),
    Rule(
        pattern=r"vision / mlmodel|vision / detectionsToSegments",
        reason='Result card displays resource names as "{subtype}/{name}" with no spaces around the slash. Flow: add-configuration-block.md',
    ),
    # --- upload-model-file flow ---
    Rule(
        pattern=r"\bImage classification\b",
        reason='Task type has no "Image classification" option. Valid values: "Single label classification", "Multi label classification", "Object detection", "Other". Flow: upload-model-file.md',
    ),
    # --- test-panel flow ---
    Rule(
        pattern=r"click\s+\*\*Test\*\*\s+to\s+expand|\*\*TEST\*\*\s+to\s+expand",
        reason='"TEST" is an uppercase section title, not a button. Users open the resource card; the TEST section is part of that card. Flow: test-panel-vision-service.md',
        ignore_case=True,
    ),
    # --- run-inference-on-stored-image flow ---
    Rule(
        pattern=r"\bActions\s+tab\b",
        reason='Expanded-image side panel has only "Labels" and "Details" tabs. No Actions tab. Flow: run-inference-on-stored-image.md',
        context=r"expanded image|inference|predictions|Auto-prediction",
        ignore_case=False,
    ),
    # --- data capture flow ---
    Rule(
        pattern=r"\bGetPointCloud\b",
        reason='Data-capture dropdown uses "NextPointCloud" for cameras (the camera API method is GetPointCloud). Flow: configure-data-capture.md. If referring to the camera API, add <!-- ui-check-ignore -->.',
        context=r"\b(data capture|capture method|Method dropdown|capture frequency|Frequency \(hz\))\b",
        ignore_case=False,
    ),
    Rule(
        pattern=r"\bcapture\s+type\b",
        reason='Data-capture field label is "Method", not "type". Flow: configure-data-capture.md',
        ignore_case=True,
    ),
]


def get_staged_markdown_files(repo_root: Path) -> list[Path]:
    """Return markdown files that this commit introduces changes in.

    For a normal commit, that's every staged .md file. For a merge commit,
    we filter out files whose staged blob matches either parent (HEAD or
    MERGE_HEAD) — those are inherited unchanged from one side and aren't
    the merge author's work. Without this filter, merge commits that pull
    in files from upstream trip on pre-existing style issues in content
    the merge author never touched.
    """
    result = subprocess.run(
        ["git", "-C", str(repo_root), "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        check=True,
        capture_output=True,
        text=True,
    )
    candidates = [
        repo_root / line
        for line in result.stdout.splitlines()
        if line.endswith(".md") and (repo_root / line).exists()
    ]

    # Detect a merge in progress: .git/MERGE_HEAD exists during merge resolution.
    git_dir_result = subprocess.run(
        ["git", "-C", str(repo_root), "rev-parse", "--git-dir"],
        check=True,
        capture_output=True,
        text=True,
    )
    git_dir = Path(git_dir_result.stdout.strip())
    if not git_dir.is_absolute():
        git_dir = repo_root / git_dir
    if not (git_dir / "MERGE_HEAD").exists():
        return candidates

    def differs_from(ref: str, path: Path) -> bool:
        """True if the staged blob for `path` differs from `ref`'s blob."""
        rel = path.relative_to(repo_root)
        diff = subprocess.run(
            ["git", "-C", str(repo_root), "diff", "--cached", ref, "--", str(rel)],
            capture_output=True,
            text=True,
        )
        return bool(diff.stdout.strip())

    return [
        p for p in candidates
        if differs_from("HEAD", p) and differs_from("MERGE_HEAD", p)
    ]


def find_repo_root(start: Path) -> Path:
    for parent in [start, *start.parents]:
        if (parent / ".git").exists():
            return parent
    return start


def default_files(repo_root: Path) -> list[Path]:
    docs_dir = repo_root / "docs"
    if not docs_dir.is_dir():
        return []
    return sorted(docs_dir.rglob("*.md"))


def check_file(path: Path, compiled_rules: list[tuple[Rule, re.Pattern, re.Pattern | None]]) -> list[str]:
    violations: list[str] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError) as err:
        return [f"{path}: could not read file: {err}"]

    for lineno, line in enumerate(lines, start=1):
        if "ui-check-ignore" in line:
            continue
        for rule, pat, ctx_pat in compiled_rules:
            m = pat.search(line)
            if not m:
                continue
            if ctx_pat is not None:
                lo = max(0, lineno - 4)
                hi = min(len(lines), lineno + 3)
                window = "\n".join(lines[lo:hi])
                if not ctx_pat.search(window):
                    continue
            violations.append(
                f"{path}:{lineno}: {m.group(0)!r} — {rule.reason}"
            )
    return violations


def compile_rules() -> list[tuple[Rule, re.Pattern, re.Pattern | None]]:
    compiled = []
    for rule in RULES:
        flags = re.IGNORECASE if rule.ignore_case else 0
        pat = re.compile(rule.pattern, flags)
        ctx_pat = re.compile(rule.context, re.IGNORECASE) if rule.context else None
        compiled.append((rule, pat, ctx_pat))
    return compiled


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("files", nargs="*", type=Path, help="Markdown files to check. Default: docs/**/*.md")
    parser.add_argument("--staged", action="store_true", help="Check staged .md files only (for git pre-commit hook use)")
    args = parser.parse_args()

    repo_root = find_repo_root(Path.cwd())

    if args.staged:
        targets = get_staged_markdown_files(repo_root)
    elif args.files:
        targets = [p for p in args.files if p.is_file()]
    else:
        targets = default_files(repo_root)

    if not targets:
        return 0

    compiled = compile_rules()
    all_violations: list[str] = []
    for path in targets:
        all_violations.extend(check_file(path, compiled))

    if all_violations:
        print("UI-label violations found:\n", file=sys.stderr)
        for v in all_violations:
            print(f"  {v}", file=sys.stderr)
        print(
            f"\n{len(all_violations)} violation(s). See ~/viam/code-map/ui-flows/ for canonical labels.",
            file=sys.stderr,
        )
        print(
            "To suppress a specific line, add '<!-- ui-check-ignore -->' at the end.",
            file=sys.stderr,
        )
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
