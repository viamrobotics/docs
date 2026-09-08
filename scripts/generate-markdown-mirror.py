#!/usr/bin/env python3
"""
Generate a clean-Markdown mirror of each published docs page into public/,
served alongside the HTML at the same path with a .md suffix (e.g.
/hardware/configure-hardware/ -> /hardware/configure-hardware.md).

Run after `hugo` has already built public/ (this script writes into it, it
does not run Hugo's own template pipeline -- Hugo's Goldmark renderer only
converts Markdown to HTML, so there's no way to get clean Markdown back out
of Hugo itself for pages that use shortcodes).

The three file-include shortcodes (readfile, read-code-snippet, snippet)
are parsed in from shortcodes to ensure that all technical information is
included in the served Markdown. Other Hugo shortcodes (alert, tabs, card,
table, etc.) are left as literal `{{< shortcode >}}` syntax in the output
at present -- this is not expected to be an obstacle to LLM comprehension.

Usage: python3 scripts/generate-markdown-mirror.py
(intended to run as a build step after `hugo`, see the Makefile)

Every failure mode below is a hard build failure (sys.exit), not a
warning: this script runs unattended as part of every deploy, and a
soft warning printed to a build log nobody is watching is equivalent to
no signal at all. Human reviewers: this means a single bad include path,
redirect cycle, or stale netlify.toml target blocks the *entire* site's
deploy until fixed, not just that one page's mirror -- deliberate, since
each of these conditions indicates something structurally broken (a
bug in this script's own path logic, or a real, previously-invisible
site bug) rather than routine content drift. If that trade-off ever
stops making sense for a specific case, downgrade it deliberately, not
by accident.
"""

import re
import sys

from _docs_build import (
    REPO_ROOT,
    PUBLIC_DIR,
    frontmatter_field,
    hugo_list_published,
    md_url_for_permalink,
    netlify_force_redirects,
    output_file_for_permalink,
    permalink_path,
    read_frontmatter,
    resolve_redirect_chain,
)

# The three file-include shortcodes. Everything else ships as raw shortcode
# syntax -- see module docstring.
INCLUDE_SHORTCODE_RE = re.compile(
    r"\{\{[<%]\s*(readfile|read-code-snippet|snippet)\s+(.*?)\s*[%>]\}\}"
)

PARAM_RE = re.compile(r'(\w[\w-]*)="([^"]*)"|"([^"]*)"')


def parse_shortcode_params(raw):
    """Parse a shortcode's parameter string into named args + positionals."""
    named = {}
    positional = []
    for m in PARAM_RE.finditer(raw):
        key, qval, bare = m.groups()
        if key is not None:
            named[key] = qval
        elif bare is not None:
            positional.append(bare)
    return named, positional


def resolve_include_path(shortcode, named, positional, page_dir):
    """Mirrors the path-resolution logic in the corresponding
    layouts/shortcodes/{shortcode}.html template."""
    fparam = named.get("file") or (positional[0] if positional else "")
    if shortcode == "snippet":
        # snippet always resolves under static/include/snippet/, no
        # absolute/relative distinction (see layouts/shortcodes/snippet.html)
        return REPO_ROOT / "static" / "include" / "snippet" / fparam
    if fparam.startswith("/"):
        return REPO_ROOT / fparam.lstrip("/")
    return page_dir / fparam


MAX_INCLUDE_DEPTH = 5


def resolve_includes(body, source_path):
    # Included files can themselves contain include shortcodes (e.g. a
    # troubleshooting snippet that readfile's a test-command snippet), so
    # resolve to a fixed point rather than a single pass. Hugo's own
    # behavior (via .Page.RenderString) keeps relative paths anchored to
    # the *original* page throughout, since .Page doesn't change identity
    # across nested RenderString calls -- so page_dir stays fixed here too,
    # it doesn't need to track per-level directories.
    page_dir = source_path.parent

    def replace(m):
        shortcode, raw_params = m.group(1), m.group(2)
        named, positional = parse_shortcode_params(raw_params)
        target = resolve_include_path(shortcode, named, positional, page_dir)

        if not target.is_file():
            # Hugo's own readfile/read-code-snippet shortcode templates
            # call errorf on a missing target, which already fails Hugo's
            # own build -- so reaching this branch means the *content*
            # path was fine but this script's own resolution logic
            # disagrees with Hugo's, i.e. a bug here, not a content typo.
            sys.exit(f"generate-markdown-mirror: {source_path}: {shortcode} target not found: {target}")

        content = target.read_text().rstrip("\n")

        # read-code-snippet is always code; readfile is code only with
        # code="true" (no current usage sets this, but the shortcode
        # supports it); snippet is never code -- see snippet.html's own
        # comment: "Do not use for code."
        is_code = shortcode == "read-code-snippet" or (
            shortcode == "readfile" and named.get("code") == "true"
        )
        if is_code:
            lang = named.get("lang", "")
            return f"```{lang}\n{content}\n```"
        return content

    for _ in range(MAX_INCLUDE_DEPTH):
        new_body, n = INCLUDE_SHORTCODE_RE.subn(replace, body)
        body = new_body
        if n == 0:
            break
    else:
        sys.exit(f"generate-markdown-mirror: {source_path}: include nesting exceeded {MAX_INCLUDE_DEPTH} levels, possible cycle")

    return body


def build_page(row, redirects, rows_by_path):
    source_path = REPO_ROOT / row["path"]
    if not source_path.is_file():
        # `hugo list published` and this script read the same filesystem
        # moments apart -- reaching this branch means something is
        # seriously inconsistent, not a routine miss.
        sys.exit(f"generate-markdown-mirror: {row['path']}: listed by `hugo list published` but file not found")

    fm_text, body = read_frontmatter(source_path)

    title = frontmatter_field(fm_text, "title") or row["title"]
    description = frontmatter_field(fm_text, "description") or ""
    updated = frontmatter_field(fm_text, "updated") or (row["date"].split("T")[0] if row["date"] else "")
    if updated.startswith("0001-01-01"):
        updated = ""  # Hugo's zero-value date sentinel -- page has no real date
    permalink = row["permalink"]

    # netlify.toml force-redirects some pages away even though Hugo builds a
    # real HTML file for them -- no visitor ever sees that page's own body,
    # so mirroring it here would be actively misleading, not just thin. A
    # short pointer to the real destination instead: no Netlify-specific
    # mechanism involved, so this is fully verifiable locally rather than
    # only by observing production redirect behavior.
    redirect_to = redirects.get(permalink_path(permalink))
    if redirect_to is not None:
        # The first hop can itself be another redirect (e.g. a
        # netlify.toml redirect landing on an alias-based one) rather than
        # a real page -- a visitor's browser just follows both 301s in
        # turn, so follow the whole chain here too instead of stopping
        # after one hop.
        final_path = resolve_redirect_chain(redirect_to, rows_by_path)
        target_row = rows_by_path.get(final_path)
        if target_row is None:
            # The chain ends somewhere that still isn't a published page --
            # a genuinely stale netlify.toml redirect target, exactly the
            # kind of previously-invisible site bug this check exists to
            # catch (nothing else in this pipeline validates netlify.toml
            # against reality). Fail loudly rather than silently degrading
            # to a link a real visitor would also 404 on.
            sys.exit(
                f"generate-markdown-mirror: {permalink}: redirect chain (via {redirect_to!r}) "
                f"ends at {final_path!r}, which is not a published page -- check netlify.toml"
            )
        target_fm_text, _ = read_frontmatter(REPO_ROOT / target_row["path"])
        # linkTitle, not title: the target's title is often identical
        # to this page's own (e.g. both "Manage data"), which reads as
        # a self-link; linkTitle is the more distinguishing nav label
        # ("Overview") authors already write for exactly this purpose.
        target_label = frontmatter_field(target_fm_text, "linkTitle") or target_row["title"]
        target_url = md_url_for_permalink(target_row["permalink"])
        body = f"This page redirects to [{target_label}]({target_url}). See that page for the full content.\n"

    body = resolve_includes(body, source_path)

    header = [f"# {title}", ""]
    if description:
        header += [description, ""]
    meta = f"> Source: {permalink}"
    if updated:
        meta += f" · Last updated: {updated}"
    header += [meta, ""]

    out_text = "\n".join(header) + "\n" + body.lstrip("\n")

    out_file = output_file_for_permalink(permalink)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(out_text)
    return out_file


def main():
    if not PUBLIC_DIR.is_dir():
        sys.exit("public/ not found -- run `hugo` before this script")

    rows = hugo_list_published()
    rows_by_path = {permalink_path(row["permalink"]): row for row in rows}
    redirects = netlify_force_redirects()

    # Two different permalinks could in principle map to the same .md
    # output path (e.g. a page whose own slug happens to end in ".md"
    # colliding with another page's mirror file) -- silently overwriting
    # one page's mirror with another's would be a much worse failure mode
    # than refusing to build, so check explicitly rather than assuming
    # today's data (no collisions, as of writing) always holds.
    seen_output_paths = {}
    for row in rows:
        out_path = output_file_for_permalink(row["permalink"])
        if out_path in seen_output_paths:
            sys.exit(
                f"generate-markdown-mirror: output path collision at {out_path}: "
                f"{seen_output_paths[out_path]!r} and {row['permalink']!r} both map here"
            )
        seen_output_paths[out_path] = row["permalink"]

    for row in rows:
        build_page(row, redirects, rows_by_path)

    print(f"generate-markdown-mirror: wrote {len(rows)} .md files")


if __name__ == "__main__":
    main()
