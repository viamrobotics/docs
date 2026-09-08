#!/usr/bin/env python3
"""
Generate public/llms.txt and public/llms-full.txt at build time, so neither
can drift from the pages they describe.

llms-full.txt is assembled by concatenating the already-generated Tier 2
.md mirrors (see generate-markdown-mirror.py) for the pages listed in
data/agent_pages.yaml -- no shortcode-resolution logic of its own, it just
reads files that script already produced. Run this after
generate-markdown-mirror.py.

llms.txt is scripts/llms-txt-template.md with the {{AGENT_PAGES}}
placeholder replaced by one generated bullet per data/agent_pages.yaml
entry (title and description pulled from the page's own frontmatter). The
rest of the template (Reference, Guides) is hand-curated prose, not
generated -- see the freshness-policy discussion on #5298 for why: which
sections exist is editorial judgment, not a list of paths, so automating
it away would lose the thing that makes it useful. A lightweight
broken-link/coverage check for that hand-curated part is separate,
follow-up work.

Neither file is checked into static/ -- like sitetree.json, they're pure
build output, so staleness isn't possible by construction.

Usage: python3 scripts/generate-llms-files.py
(intended to run as a build step after generate-markdown-mirror.py, see
the Makefile)
"""

import sys
from pathlib import Path

from _docs_build import (
    BASE_URL,
    PUBLIC_DIR,
    REPO_ROOT,
    frontmatter_field,
    hugo_list_published,
    output_file_for_permalink,
    permalink_path,
    read_frontmatter,
)

AGENT_PAGES_FILE = REPO_ROOT / "data" / "agent_pages.yaml"
TEMPLATE_FILE = Path(__file__).resolve().parent / "llms-txt-template.md"


def load_agent_page_paths():
    """Minimal parser for the flat YAML list in agent_pages.yaml (comments
    and blank lines skipped, each remaining line is `- /some/path/`) --
    avoids adding a YAML dependency for a one-field list of strings."""
    paths = []
    for line in AGENT_PAGES_FILE.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("- "):
            paths.append(line[2:].strip().strip('"').strip("'"))
    return paths


def main():
    if not PUBLIC_DIR.is_dir():
        sys.exit("public/ not found -- run `hugo` before this script")

    paths = load_agent_page_paths()
    # Keyed by path, not the full permalink -- Hugo's actual configured
    # baseURL varies by build context (production vs. a PR preview vs.
    # local dev), so matching on path is what makes this work regardless
    # of which build produced the current public/.
    rows_by_path = {permalink_path(row["permalink"]): row for row in hugo_list_published()}

    bullets = []
    full_sections = []
    for path in paths:
        normalized = "/" + path.strip("/") + "/"
        row = rows_by_path.get(normalized)
        if row is None:
            sys.exit(f"generate-llms-files: {path!r} in agent_pages.yaml is not a published page")

        source_path = REPO_ROOT / row["path"]
        fm_text, _ = read_frontmatter(source_path)
        title = frontmatter_field(fm_text, "title") or row["title"]
        description = frontmatter_field(fm_text, "description") or ""

        # llms.txt is a hand-curated document describing the real production
        # site, so its links are always the canonical production URL --
        # even when this script runs against a PR-preview or local build.
        canonical_link = BASE_URL + path.strip("/") + "/"
        bullets.append(f"- [{title}]({canonical_link}){': ' + description if description else ''}")

        # ...but the mirror file to *read* is the one this build actually
        # produced, at whatever permalink this build actually used.
        mirror_file = output_file_for_permalink(row["permalink"])
        if not mirror_file.is_file():
            sys.exit(f"generate-llms-files: expected mirror file not found: {mirror_file} "
                      "(run generate-markdown-mirror.py first)")
        full_sections.append(mirror_file.read_text().rstrip("\n"))

    llms_txt = TEMPLATE_FILE.read_text().replace("{{AGENT_PAGES}}", "\n".join(bullets))
    (PUBLIC_DIR / "llms.txt").write_text(llms_txt)

    llms_full_intro = (
        "# Viam — agent-facing pages, full text\n\n"
        "> The full text of the pages linked under \"Start here for agents\" in\n"
        "> [llms.txt](https://docs.viam.com/llms.txt), inlined here so an agent can\n"
        "> read all of them in a single fetch instead of following each link\n"
        "> separately.\n"
    )
    llms_full_txt = llms_full_intro + "\n---\n\n" + "\n\n---\n\n".join(full_sections) + "\n"
    (PUBLIC_DIR / "llms-full.txt").write_text(llms_full_txt)

    print(f"generate-llms-files: wrote public/llms.txt and public/llms-full.txt ({len(paths)} agent pages)")


if __name__ == "__main__":
    main()
