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
    """The path portion of a permalink, independent of scheme/host -- e.g.
    both "https://docs.viam.com/data/" and
    "https://deploy-preview-1--viam-docs.netlify.app/data/" give "/data/".
    Use this instead of assuming BASE_URL: Hugo's actual configured baseURL
    varies by build context (production vs. a PR preview vs. local dev),
    and permalinks always reflect whatever that build actually used."""
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
    """The .md mirror *URL* for a page's permalink -- same logic as
    output_file_for_permalink, but a URL string rather than a filesystem
    path. Used when one mirror's content needs to link to another mirror
    (e.g. a redirect pointer) and should point at its .md variant rather
    than kicking a markdown-consuming reader back into HTML."""
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
    in netlify.toml (from/to both site-relative paths, not external URLs or
    wildcards). These are 301s Netlify applies even when a real file exists
    at `from` (force=true overrides Netlify's normal serve-existing-file-
    first behavior), so a page at one of these paths is never actually seen
    by a visitor -- mirroring its own (often thin) body would be actively
    misleading, not just incomplete."""
    with open(REPO_ROOT / "netlify.toml", "rb") as f:
        config = tomllib.load(f)
    redirects = {}
    for r in config.get("redirects", []):
        from_path, to_path = r.get("from", ""), r.get("to", "")
        if r.get("force") and from_path.startswith("/") and to_path.startswith("/") and "*" not in from_path:
            redirects[_normalize_path(from_path)] = _normalize_path(to_path)
    return redirects


def alias_redirects():
    """Returns {from_path: to_path} parsed from Hugo's own generated
    public/_redirects (built from every page's `aliases:` frontmatter --
    see layouts/docs/index.redir). A netlify.toml redirect's target can
    itself be one of these rather than a real page (a real visitor's
    browser just follows both 301s in turn), so this is needed to follow a
    redirect chain to its actual destination rather than stopping after
    one hop."""
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
    final destination path, in case a hop lands on another redirect rather
    than a real page. A step stops only when the current path is a real
    published page *and* isn't itself force-redirected elsewhere -- a real
    page can still be force-redirected away by a different rule (chained
    force-redirects), so "it's a real page" alone isn't sufficient to stop;
    matches Netlify's actual precedence, where force=true overrides even an
    existing file but a plain (non-forced) redirect never does. Returns the
    final path reached.

    A cycle or an excessively long chain is a hard failure (sys.exit), not
    a warning -- nothing else in this pipeline validates netlify.toml or
    page aliases against each other, so this is the only place either
    would ever be caught at all."""
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
    field by regex rather than a full YAML parse -- every field these
    scripts read (title, description, updated, date) is authored as a plain
    single-line scalar throughout this repo."""
    m = re.search(rf'^{key}:\s*"?(.*?)"?\s*$', fm_text, re.MULTILINE)
    return m.group(1) if m else None
