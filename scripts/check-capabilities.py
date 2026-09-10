#!/usr/bin/env python3
"""Warn (but don't fail CI) about docs/ pages with missing or invalid
capabilities: frontmatter.

data/capabilities.yaml is the accepted taxonomy. This script flags pages
that ship without a capabilities: field, and pages that use a tag not in
that taxonomy.
"""
import pathlib
import sys

import yaml

DOCS_DIR = pathlib.Path("docs")
CAPABILITIES_FILE = pathlib.Path("data/capabilities.yaml")
EXCLUDE = {"docs/tutorials/template.md", "docs/tutorials/pick-and-place/_phase-template.md"}


def load_accepted_capabilities():
    data = yaml.safe_load(CAPABILITIES_FILE.read_text(encoding="utf-8"))
    return set(data["capabilities"])


def main():
    accepted = load_accepted_capabilities()

    missing = []
    invalid = []  # (path, [bad tags])

    for path in sorted(DOCS_DIR.rglob("*.md")):
        rel = path.as_posix()
        if rel in EXCLUDE:
            continue
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            continue
        end = text.find("\n---", 4)
        front_matter = yaml.safe_load(text[4:end])
        tags = (front_matter or {}).get("capabilities")
        if not tags:
            missing.append(rel)
            continue
        bad = [tag for tag in tags if tag not in accepted]
        if bad:
            invalid.append((rel, bad))

    if missing:
        print(f"::warning::{len(missing)} docs/ page(s) missing capabilities: frontmatter")
        for rel in missing:
            print(f"  {rel}")

    if invalid:
        print(f"::warning::{len(invalid)} docs/ page(s) use capability tags not in data/capabilities.yaml")
        for rel, bad in invalid:
            print(f"  {rel}: {', '.join(bad)}")

    if not missing and not invalid:
        print("All docs/ pages have valid capabilities: frontmatter.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
