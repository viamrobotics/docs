"""
Shared helpers for the docs build's Markdown-generation scripts
(generate-markdown-mirror.py, generate-llms-files.py). Not a script itself.
"""

import csv
import io
import re
import subprocess
import sys
import tomllib
from pathlib import Path
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parent.parent
PUBLIC_DIR = REPO_ROOT / "public"
BASE_URL = "https://docs.viam.com/"

FRONTMATTER_RE = re.compile(r"\A---\n(.*?\n)---\n?", re.DOTALL)


def permalink_path(permalink):
    """The path portion of a permalink, independent of scheme/host, e.g.
    "https://docs.viam.com/data/" -> "/data/". Use this instead of
    assuming BASE_URL: Hugo's configured baseURL varies by build context
    (production, PR preview, local dev)."""
    return urlparse(permalink).path


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
    path = permalink_path(permalink).strip("/")
    if not path:
        return PUBLIC_DIR / "index.md"
    segments = path.split("/")
    parent = PUBLIC_DIR.joinpath(*segments[:-1])
    return parent / f"{segments[-1]}.md"


def md_url_for_permalink(permalink):
    """The .md mirror *URL* for a page's permalink (same logic as
    output_file_for_permalink, but a URL, not a filesystem path). Used so
    a mirror linking to another mirror (e.g. a redirect pointer) points at
    its .md variant, not its HTML page."""
    parsed = urlparse(permalink)
    path = parsed.path.strip("/")
    segments = path.split("/") if path else []
    new_path = "/" + "/".join(segments[:-1] + [f"{segments[-1] if segments else 'index'}.md"])
    return f"{parsed.scheme}://{parsed.netloc}{new_path}"


def _normalize_path(path):
    """Ensures a site-relative path ends in "/", matching Hugo's own
    permalink format -- so a redirect rule written without a trailing
    slash (e.g. `from = "/data"`) still matches instead of silently never
    being detected at all."""
    return path if path.endswith("/") else path + "/"


def netlify_force_redirects():
    """Returns {from_path: to_path} for every internal, force=true redirect
    in netlify.toml. force=true means the 301 fires even if a real file
    exists at `from`, so that page's own body is never seen by a visitor.
    Mirroring it would be misleading, not just thin."""
    with open(REPO_ROOT / "netlify.toml", "rb") as f:
        config = tomllib.load(f)
    redirects = {}
    for r in config.get("redirects", []):
        from_path, to_path = r.get("from", ""), r.get("to", "")
        if r.get("force") and from_path.startswith("/") and to_path.startswith("/") and "*" not in from_path:
            redirects[_normalize_path(from_path)] = _normalize_path(to_path)
    return redirects


def alias_redirects():
    """Returns {from_path: to_path} parsed from Hugo's generated
    public/_redirects (built from page `aliases:` frontmatter, see
    layouts/docs/index.redir). Needed because a netlify.toml redirect's
    target can itself be one of these, not a real page."""
    redirects_file = PUBLIC_DIR / "_redirects"
    redirects = {}
    if not redirects_file.is_file():
        return redirects
    for line in redirects_file.read_text().splitlines():
        parts = line.split()
        if len(parts) >= 2 and parts[0].startswith("/") and parts[1].startswith("/"):
            redirects[_normalize_path(parts[0])] = _normalize_path(parts[1])
    return redirects


def resolve_redirect_chain(start_path, rows_by_path, max_hops=10):
    """Follows netlify.toml + alias redirects from start_path to their
    final destination. Stops only at a page that's both real *and* not
    itself force-redirected elsewhere (chained force-redirects exist).
    Matches Netlify's precedence, where force=true beats an existing file
    but a plain redirect never does. Returns the final path.

    A cycle or excessive chain length is a hard failure: nothing else
    validates netlify.toml/aliases against each other, so this is the
    only place either would be caught."""
    force = netlify_force_redirects()
    combined = {**alias_redirects(), **force}
    current = start_path
    seen = {current}
    for _ in range(max_hops):
        if current in rows_by_path and current not in force:
            return current
        nxt = combined.get(current)
        if nxt is None:
            return current
        if nxt in seen:
            sys.exit(f"generate-markdown-mirror: redirect cycle detected starting at {start_path} (loops back to {nxt})")
        seen.add(nxt)
        current = nxt
    sys.exit(f"generate-markdown-mirror: redirect chain from {start_path} exceeded {max_hops} hops, stopping at {current}")


def read_frontmatter(source_path):
    """Returns (frontmatter_text, body) for a content file."""
    text = source_path.read_text()
    m = FRONTMATTER_RE.match(text)
    if not m:
        return "", text
    return m.group(1), text[m.end() :]


def frontmatter_field(fm_text, key):
    """Extract a single simple (single-line, optionally quoted) frontmatter
    field by regex to avoid a PyYAML dependency. Works because every field
    these scripts read (title, description, updated, date) is authored as
    a plain single-line scalar throughout this repo -- would silently miss
    a multi-line or nested value."""
    m = re.search(rf'^{key}:\s*"?(.*?)"?\s*$', fm_text, re.MULTILINE)
    return m.group(1) if m else None
