#!/usr/bin/env python3
"""Validate capabilities: and diataxis: frontmatter on docs/ pages.

Fails (exit 1) when a page is missing either field or uses a value outside
the accepted taxonomy:

  * data/capabilities.yaml - capabilities: is a non-empty list of these tags.
  * data/diataxis.yaml     - diataxis: is exactly one of these modes.

This module is also the single definition of which pages those rules apply
to. The docs-health metrics build (viamrobotics/docs-health) imports it from
its docs checkout instead of keeping its own copy, so "passes this check" and
"won't fail the daily metrics run" mean the same thing. Keep the public
functions below (load_front_matter, exclusion_reason, validate) stable, or
update docs-health in the same change.

Which pages are checked:

  * Drafts (draft: true, a real boolean, the way Hugo reads it) are skipped
    entirely. Hugo doesn't publish them, so nothing reads them. This covers
    the page templates, which carry empty placeholder fields.
  * capabilities: is required on every other page, including redirect stubs
    and glossary terms.
  * diataxis: is additionally skipped on two kinds of page with no prose of
    their own to classify:
      - Glossary terms (tagged capabilities: [glossary]). The term files in
        docs/reference/glossary/ are page resources inlined into one page.
      - Redirect and empty-node stubs. A page carrying manualLink,
        manualLinkRelref, canonical, or empty_node renders no content of its
        own. Removing one of those keys turns the page into a real page that
        needs a diataxis: mode.

Usage:
    python3 scripts/frontmatter_rules.py                      # scan docs/
    python3 scripts/frontmatter_rules.py path/to/page.md ...  # scan named files
"""
import argparse
import os
import pathlib
import sys

import yaml

DOCS_ROOT = pathlib.Path(__file__).resolve().parent.parent
CAPABILITIES_FILE = "data/capabilities.yaml"
DIATAXIS_FILE = "data/diataxis.yaml"
STUB_KEYS = ("manualLink", "manualLinkRelref", "canonical", "empty_node")


class FrontMatterError(Exception):
    """The file has no parseable YAML frontmatter block."""


def load_taxonomies(docs_root=DOCS_ROOT):
    """Return (accepted capability tags, accepted Diataxis modes)."""
    root = pathlib.Path(docs_root)
    caps = yaml.safe_load((root / CAPABILITIES_FILE).read_text(encoding="utf-8"))
    modes = yaml.safe_load((root / DIATAXIS_FILE).read_text(encoding="utf-8"))
    return set(caps["capabilities"]), set(modes["diataxis"])


def load_front_matter(text):
    """Parse a page's leading YAML frontmatter block into a dict.

    Raises FrontMatterError instead of returning {} for a missing, unclosed,
    or unparseable block: a page whose frontmatter can't be read must fail
    the check, not be skipped as if it had nothing to check.
    """
    text = text.replace("\r\n", "\n")
    if not text.startswith("---\n"):
        raise FrontMatterError("no YAML frontmatter block (file must start with ---)")
    end = text.find("\n---", 4)
    if end == -1:
        raise FrontMatterError("frontmatter block is never closed with ---")
    try:
        front_matter = yaml.safe_load(text[4:end])
    except yaml.YAMLError as err:
        raise FrontMatterError(f"frontmatter is not valid YAML: {err}") from err
    if front_matter is None:
        return {}
    if not isinstance(front_matter, dict):
        raise FrontMatterError("frontmatter is not a YAML mapping")
    return front_matter


def is_draft(front_matter):
    # `is True`, not truthiness: Hugo treats only a real boolean as a draft
    # flag, and draft: "false" (a truthy string) is published.
    return front_matter.get("draft") is True


def is_glossary(front_matter):
    caps = front_matter.get("capabilities")
    return isinstance(caps, list) and "glossary" in caps


def is_redirect_stub(front_matter):
    return any(front_matter.get(key) for key in STUB_KEYS)


def exclusion_reason(front_matter):
    """Why a page has no diataxis: requirement, or None if it has one.

    Returns "draft", "glossary", or "redirect". docs-health excludes exactly
    these pages from scoring; every other page is in its corpus.
    """
    if is_draft(front_matter):
        return "draft"
    if is_glossary(front_matter):
        return "glossary"
    if is_redirect_stub(front_matter):
        return "redirect"
    return None


def validate(front_matter, accepted_caps, accepted_modes):
    """Return a list of error messages for one page's frontmatter."""
    if is_draft(front_matter):
        return []
    errors = []

    caps = front_matter.get("capabilities")
    if caps is None or caps == []:
        errors.append(
            "missing capabilities: frontmatter. Add a list of one or more tags "
            f"from {CAPABILITIES_FILE}, for example capabilities: [\"machine-config\"]"
        )
    elif not isinstance(caps, list):
        errors.append(
            f"capabilities: must be a list, got {caps!r}. "
            f"Write it as capabilities: [\"{caps}\"]"
        )
    else:
        bad = [tag for tag in caps if tag not in accepted_caps]
        if bad:
            errors.append(
                f"capability tag(s) not in {CAPABILITIES_FILE}: {', '.join(map(str, bad))}. "
                f"Use an existing tag, or see CLAUDE.md before adding a new one"
            )

    if exclusion_reason(front_matter) is None:
        mode = front_matter.get("diataxis")
        modes = ", ".join(sorted(accepted_modes))
        if not mode:
            errors.append(
                f"missing diataxis: frontmatter. Add exactly one mode from "
                f"{DIATAXIS_FILE}: {modes}"
            )
        elif isinstance(mode, list):
            errors.append(
                f"diataxis: must be a single mode, got a list: {mode}. "
                f"A page that needs two modes should be split"
            )
        elif mode not in accepted_modes:
            errors.append(f"unknown diataxis: mode {mode!r}. Use one of: {modes}")

    return errors


def check_file(path, accepted_caps, accepted_modes):
    try:
        front_matter = load_front_matter(path.read_text(encoding="utf-8"))
    except FrontMatterError as err:
        return [str(err)]
    return validate(front_matter, accepted_caps, accepted_modes)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("paths", nargs="*", help="files to check (default: every docs/**/*.md)")
    args = parser.parse_args(argv)

    # Resolve named files against the caller's directory before moving to the
    # repo root, so annotations carry the repo-relative paths Actions expects.
    named = [pathlib.Path(p).resolve() for p in args.paths]
    os.chdir(DOCS_ROOT)
    accepted_caps, accepted_modes = load_taxonomies()
    if named:
        paths = [pathlib.Path(os.path.relpath(p, DOCS_ROOT)) for p in named]
    else:
        paths = sorted(pathlib.Path("docs").rglob("*.md"))

    failures = 0
    for path in paths:
        errors = check_file(path, accepted_caps, accepted_modes)
        for error in errors:
            # GitHub Actions turns this into an annotation on the file.
            print(f"::error file={path.as_posix()},line=1::{path.as_posix()}: {error}")
        failures += bool(errors)

    if failures:
        print(
            f"\n{failures} page(s) have missing or invalid capabilities:/diataxis: "
            "frontmatter. The docs-health metrics build reads these fields and "
            "fails when a published page is missing them."
        )
        return 1
    print(f"All {len(paths)} checked page(s) have valid capabilities: and diataxis: frontmatter.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
