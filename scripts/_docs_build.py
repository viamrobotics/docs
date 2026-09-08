"""
Shared helpers for the docs build's Markdown-generation scripts
(generate-markdown-mirror.py, generate-llms-files.py). Not a script itself.
"""

import csv
import io
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PUBLIC_DIR = REPO_ROOT / "public"
BASE_URL = "https://docs.viam.com/"

FRONTMATTER_RE = re.compile(r"\A---\n(.*?\n)---\n?", re.DOTALL)


def hugo_list_published():
    """Runs `hugo list published` (using the same config as `make
    build-prod`) and returns its rows as dicts. This is the source of truth
    for each page's real permalink -- Hugo's own routing (pretty URLs,
    aliases, leaf bundles, slug/url overrides) is too much to safely
    re-derive by hand from file paths."""
    result = subprocess.run(
        ["hugo", "list", "published", "--config", "config.toml,config_prod.toml", "-e", "production"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        sys.exit(f"`hugo list published` failed:\n{result.stderr}")
    return list(csv.DictReader(io.StringIO(result.stdout)))


def output_file_for_permalink(permalink):
    """The .md mirror path for a page's permalink, e.g.
    https://docs.viam.com/hardware/configure-hardware/ ->
    public/hardware/configure-hardware.md (a sibling of Hugo's own
    public/hardware/configure-hardware/index.html)."""
    path = permalink[len(BASE_URL) :].strip("/") if permalink.startswith(BASE_URL) else permalink.strip("/")
    if not path:
        return PUBLIC_DIR / "index.md"
    segments = path.split("/")
    parent = PUBLIC_DIR.joinpath(*segments[:-1])
    return parent / f"{segments[-1]}.md"


def read_frontmatter(source_path):
    """Returns (frontmatter_text, body) for a content file."""
    text = source_path.read_text()
    m = FRONTMATTER_RE.match(text)
    if not m:
        return "", text
    return m.group(1), text[m.end() :]


def frontmatter_field(fm_text, key):
    """Extract a single simple (single-line, optionally quoted) frontmatter
    field by regex rather than a full YAML parse -- every field these
    scripts read (title, description, updated, date) is authored as a plain
    single-line scalar throughout this repo."""
    m = re.search(rf'^{key}:\s*"?(.*?)"?\s*$', fm_text, re.MULTILINE)
    return m.group(1) if m else None
