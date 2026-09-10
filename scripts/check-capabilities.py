#!/usr/bin/env python3
"""Warn (but don't fail CI) about docs/ pages missing capabilities: frontmatter.

Capability tags were backfilled once across docs/; see data/capabilities.yaml
for the taxonomy. This just flags pages that ship without one added by hand.
"""
import pathlib
import sys

DOCS_DIR = pathlib.Path("docs")
EXCLUDE = {"docs/tutorials/template.md", "docs/tutorials/pick-and-place/_phase-template.md"}


def main():
    missing = []
    for path in sorted(DOCS_DIR.rglob("*.md")):
        rel = path.as_posix()
        if rel in EXCLUDE:
            continue
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            continue
        end = text.find("\n---", 4)
        front_matter = text[:end]
        if "capabilities:" not in front_matter:
            missing.append(rel)

    if missing:
        print(f"::warning::{len(missing)} docs/ page(s) missing capabilities: frontmatter")
        for rel in missing:
            print(f"  {rel}")
    else:
        print("All docs/ pages have capabilities: frontmatter.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
