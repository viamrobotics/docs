#!/usr/bin/env python3
"""
Generate a clean-Markdown mirror of each published docs page into public/,
served alongside the HTML at the same path with a .md suffix (e.g.
/hardware/configure-hardware/ -> /hardware/configure-hardware.md).

Run after `hugo` has already built public/ (this script writes into it, it
does not run Hugo's own template pipeline -- Hugo's Goldmark renderer only
converts Markdown to HTML, so there's no way to get clean Markdown back out
of Hugo itself for pages that use shortcodes).

v0 scope: most Hugo shortcodes (alert, tabs, card, table, etc.)
are left as literal `{{< shortcode >}}` syntax in the output -- LLMs parse
templated syntax like this reasonably well without rendering, and no
information is lost, just polish. The three file-include shortcodes
(readfile, read-code-snippet, snippet) are the exception: left raw, they'd
show an empty shortcode call where a real code example or prose snippet
belongs, which is a missing-information problem, not a polish one -- so
those are resolved by inlining the referenced file's content directly.

Usage: python3 scripts/generate-markdown-mirror.py
(intended to run as a build step after `hugo`, see the Makefile)
"""

import re
import sys

from _docs_build import (
    REPO_ROOT,
    PUBLIC_DIR,
    frontmatter_field,
    hugo_list_published,
    output_file_for_permalink,
    read_frontmatter,
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


def resolve_includes(body, source_path, warnings):
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
            warnings.append(f"{source_path}: {shortcode} target not found: {target}")
            return m.group(0)  # leave the shortcode call rather than dropping content

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
        warnings.append(f"{source_path}: include nesting exceeded {MAX_INCLUDE_DEPTH} levels, possible cycle")

    return body


def build_page(row, warnings):
    source_path = REPO_ROOT / row["path"]
    if not source_path.is_file():
        warnings.append(f"{row['path']}: listed by `hugo list published` but file not found, skipping")
        return None

    fm_text, body = read_frontmatter(source_path)

    title = frontmatter_field(fm_text, "title") or row["title"]
    description = frontmatter_field(fm_text, "description") or ""
    updated = frontmatter_field(fm_text, "updated") or (row["date"].split("T")[0] if row["date"] else "")
    if updated.startswith("0001-01-01"):
        updated = ""  # Hugo's zero-value date sentinel -- page has no real date
    permalink = row["permalink"]

    body = resolve_includes(body, source_path, warnings)

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

    warnings = []
    written = 0
    for row in rows:
        if build_page(row, warnings) is not None:
            written += 1

    for w in warnings:
        print(f"WARNING: {w}", file=sys.stderr)
    print(f"generate-markdown-mirror: wrote {written} .md files ({len(warnings)} warnings)")


if __name__ == "__main__":
    main()
