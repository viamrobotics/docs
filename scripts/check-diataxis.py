#!/usr/bin/env python3
"""Warn (but don't fail CI) about docs/ pages with missing or invalid
diataxis: frontmatter.

data/diataxis.yaml is the accepted taxonomy. This script flags pages that
ship without a diataxis: field, pages that use a mode not in that taxonomy,
and pages that supply a list where a single mode is required.

Two classes of file are skipped rather than reported, because they have no
prose of their own to classify:

  * Glossary term files. docs/reference/glossary/ is a Hugo leaf bundle; the
    term files beside its index.md are page resources inlined into that one
    page, not pages in their own right. They have no permalink.
  * Redirect and empty-node stubs. A page carrying manualLink,
    manualLinkRelref, canonical, or empty_node renders no content of its own
    - it routes the reader elsewhere. Real hub pages, which do render, are
    expected to carry diataxis: overview.

That second rule is what keeps "intentionally unset" from reading as "someone
forgot": don't drop it without replacing it with something equivalent, or
every stub in the tree turns into a warning nobody can action.
"""
import pathlib
import sys

import yaml

DOCS_DIR = pathlib.Path("docs")
DIATAXIS_FILE = pathlib.Path("data/diataxis.yaml")
GLOSSARY_DIR = "docs/reference/glossary/"
STUB_KEYS = ("manualLink", "manualLinkRelref", "canonical", "empty_node")
EXCLUDE = {"docs/tutorials/template.md", "docs/tutorials/pick-and-place/_phase-template.md"}


def load_accepted_modes():
    data = yaml.safe_load(DIATAXIS_FILE.read_text(encoding="utf-8"))
    return set(data["diataxis"])


def is_skipped(rel, front_matter):
    if rel in EXCLUDE:
        return True
    # Glossary page resources, but not the bundle's own index.md.
    if rel.startswith(GLOSSARY_DIR) and not rel.endswith("/index.md"):
        return True
    return any(front_matter.get(key) for key in STUB_KEYS)


def main():
    accepted = load_accepted_modes()

    missing = []
    invalid = []  # (path, reason)
    skipped = 0

    for path in sorted(DOCS_DIR.rglob("*.md")):
        rel = path.as_posix()
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            continue
        end = text.find("\n---", 4)
        front_matter = yaml.safe_load(text[4:end]) or {}

        if is_skipped(rel, front_matter):
            skipped += 1
            continue

        mode = front_matter.get("diataxis")
        if not mode:
            missing.append(rel)
        elif isinstance(mode, list):
            invalid.append((rel, f"expected a single mode, got a list: {mode}"))
        elif mode not in accepted:
            invalid.append((rel, f"unknown mode: {mode}"))

    if missing:
        print(f"::warning::{len(missing)} docs/ page(s) missing diataxis: frontmatter")
        for rel in missing:
            print(f"  {rel}")

    if invalid:
        print(f"::warning::{len(invalid)} docs/ page(s) have an invalid diataxis: value")
        for rel, reason in invalid:
            print(f"  {rel}: {reason}")

    if not missing and not invalid:
        print(f"All docs/ pages have valid diataxis: frontmatter ({skipped} skipped).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
