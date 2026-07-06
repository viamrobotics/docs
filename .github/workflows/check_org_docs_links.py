#!/usr/bin/env python3
"""Scan Viam source repos for docs.viam.com links and verify them.

Walks one or more repository clones, extracts every ``docs.viam.com`` URL from
text files (regardless of context -- godoc comments, error/CLI strings,
markdown, docstrings), and checks each unique URL against the live docs site:

* 4xx / 5xx / connection error  -> ``broken``
* 3xx redirect                  -> ``stale-redirect`` (records the canonical
                                   target so the source link can be updated)
* 2xx with a ``#fragment`` whose ``id`` is absent on the page -> ``broken-anchor``

Findings are written as a grouped markdown report. The script exits non-zero
when there are findings so the workflow's ``if: failure()`` reporting step fires.

Every URL targets a single host (docs.viam.com), so requests are **serialized**
with a small delay and one retry on transient 429/5xx -- a burst against one
host is what caused the historical htmltest 403/429/timeout flakiness.
"""

import argparse
import os
import re
import sys
import time
from urllib.parse import urljoin, urlsplit

import requests

# Repositories to scan. Public repos clone tokenless; private repos (app) need a
# read token supplied at clone time by the workflow. Extend this list to cover
# more repos (e.g. viam-cli, micro-server).
DEFAULT_REPOS = [
    "rdk",
    "app",
    "api",
    "viam-python-sdk",
    "viam-typescript-sdk",
    "viam-flutter-sdk",
]

# Match a docs.viam.com URL, stopping at whitespace or characters that commonly
# delimit a URL in code/markdown (quotes, backticks, brackets, parens, angle
# brackets, pipes, backslashes).
URL_RE = re.compile(r"""https?://docs\.viam\.com/[^\s"'`)>\]}|\\]*""")

# File extensions worth scanning for embedded links.
TEXT_EXT = {
    ".go", ".md", ".mdx", ".txt", ".py", ".ts", ".tsx", ".js", ".jsx",
    ".dart", ".rst", ".proto", ".yaml", ".yml", ".json", ".html", ".sh",
    ".java", ".kt", ".swift", ".rs", ".c", ".cc", ".cpp", ".h",
}

# Directories that never contain first-party source worth checking.
SKIP_DIRS = {
    ".git", "node_modules", "vendor", "dist", "build", "out",
    ".venv", "venv", "__pycache__", "gen", "bin", "target",
}

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0 Safari/537.36 viam-docs-link-checker"
)

# Trailing characters to strip from a captured URL (sentence/markdown punctuation
# the greedy match may absorb).
TRAILING = ".,;:!?"


def strip_url(url):
    """Trim trailing punctuation a greedy match may have absorbed."""
    return url.rstrip(TRAILING)


def extract(base_dir, repos):
    """Return ``{url: sorted[list of 'repo/relpath:lineno']}`` across repos."""
    locations = {}
    for repo in repos:
        repo_root = os.path.join(base_dir, repo)
        if not os.path.isdir(repo_root):
            print(f"  ! skipping {repo}: clone not found at {repo_root}", file=sys.stderr)
            continue
        for dirpath, dirnames, filenames in os.walk(repo_root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for name in filenames:
                if os.path.splitext(name)[1].lower() not in TEXT_EXT:
                    continue
                path = os.path.join(dirpath, name)
                rel = os.path.relpath(path, repo_root)
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as fh:
                        for lineno, line in enumerate(fh, 1):
                            if "docs.viam.com" not in line:
                                continue
                            for match in URL_RE.findall(line):
                                url = strip_url(match)
                                locations.setdefault(url, set()).add(
                                    f"{repo}/{rel}:{lineno}"
                                )
                except OSError as exc:
                    print(f"  ! read error {rel}: {exc}", file=sys.stderr)
    return {u: sorted(locs) for u, locs in locations.items()}


# Hugo emits page aliases as an HTML stub that meta-refreshes to the canonical
# URL -- an HTTP 200, NOT a 3xx. Detect it so an aliased link is treated as a
# (stale) redirect rather than a live page with missing anchors.
META_REFRESH_RE = re.compile(
    r"""<meta[^>]+http-equiv=["']?refresh["']?[^>]+content=["'][^"']*url=([^"'\s]+)""",
    re.IGNORECASE,
)


def anchor_present(html, fragment):
    """True if an ``id``/``name`` matches the fragment (Hugo slug).

    docs.viam.com renders anchors with **unquoted** attributes (e.g.
    ``id=move``), so match quoted and unquoted forms, ending on a delimiter so
    ``move`` does not spuriously match ``moveonglobe``.
    """
    frag = fragment.strip()
    if not frag:
        return True
    pat = re.compile(
        r"""(?:id|name)\s*=\s*["']?""" + re.escape(frag) + r"""(?=["'\s/>])""",
        re.IGNORECASE,
    )
    return bool(pat.search(html))


def same_page(a, b):
    """True if two URLs point at the same page (ignore fragment/query, //-slash)."""
    pa, pb = urlsplit(a), urlsplit(b)
    return (
        pa.scheme == pb.scheme
        and pa.netloc == pb.netloc
        and pa.path.rstrip("/") == pb.path.rstrip("/")
    )


def resolve(url, session, retries=1, max_hops=6):
    """Follow HTTP 3xx and Hugo meta-refresh aliases to the final page.

    Returns ``(final_url, status, html)``. ``status`` is the last HTTP status;
    ``html`` is the final page body (empty on error).
    """
    current = url
    seen = set()
    for _ in range(max_hops):
        if current in seen:
            break
        seen.add(current)

        attempt = 0
        while True:
            try:
                resp = session.get(current, allow_redirects=False, timeout=30)
            except requests.RequestException as exc:
                if attempt < retries:
                    attempt += 1
                    time.sleep(2)
                    continue
                return current, 0, ""
            code = resp.status_code
            if code == 429 or 500 <= code < 600:
                if attempt < retries:
                    attempt += 1
                    time.sleep(2)
                    continue
            break

        if 300 <= code < 400:
            location = resp.headers.get("Location")
            if not location:
                return current, code, resp.text
            current = urljoin(current, location)
            continue

        if code >= 400:
            return current, code, resp.text

        # 2xx: a meta-refresh body means this is an alias stub -> keep following.
        match = META_REFRESH_RE.search(resp.text)
        if match:
            current = urljoin(current, match.group(1).strip())
            continue

        return current, code, resp.text

    return current, 0, ""


def classify(url, session, delay):
    """Return ``(label, detail)`` for one URL, following aliases/redirects."""
    final_url, status, html = resolve(url, session)

    if status == 0:
        return "broken", "unreachable / redirect loop"
    if status >= 400:
        return "broken", f"HTTP {status} (final: {final_url})"

    fragment = urlsplit(url).fragment

    if not same_page(url, final_url):
        # Report only the move; the canonical target is the actionable fix. Any
        # missing anchor on the target surfaces as its own broken-anchor finding
        # once the source is repointed to the canonical URL.
        return "stale-redirect", final_url

    if fragment and not anchor_present(html, fragment):
        return "broken-anchor", f"missing #{fragment}"
    return "ok", f"HTTP {status}"


def rewrite_rule(orig_url, final_url):
    """Describe the path change between two URLs as a ``(from, to)`` substring
    rule, so links that moved the same way group together.

    e.g. ``/dev/reference/apis/services/motion/`` -> ``/reference/apis/services/
    motion/`` yields ``("dev/", "")`` -- the systematic prefix change shared by
    every ``/dev/reference/`` link.
    """
    a = urlsplit(orig_url).path.strip("/").split("/")
    b = urlsplit(final_url).path.strip("/").split("/")
    i = 0
    while i < min(len(a), len(b)) and a[i] == b[i]:
        i += 1
    j = 0
    while j < min(len(a) - i, len(b) - i) and a[-1 - j] == b[-1 - j]:
        j += 1
    frm = "/".join(a[i:len(a) - j])
    to = "/".join(b[i:len(b) - j])
    return frm, to


def build_report(findings, url_locations):
    """Render grouped, summarized markdown for ``{label: [(url, detail)]}``."""
    n_broken = len(findings.get("broken", []))
    n_stale = len(findings.get("stale-redirect", []))
    n_anchor = len(findings.get("broken-anchor", []))
    total = n_broken + n_stale + n_anchor

    lines = ["## docs.viam.com link check findings", ""]
    lines.append(
        f"Found **{total}** link problem(s): "
        f"**{n_broken}** broken, **{n_stale}** stale redirect(s), "
        f"**{n_anchor}** broken anchor(s)."
    )
    lines.append("")

    # Broken links -- unambiguous, highest priority; flat list.
    if n_broken:
        lines.append(f"### Broken links (4xx / 5xx / unreachable) — {n_broken}")
        lines.append("")
        for url, detail in sorted(findings["broken"]):
            lines.append(f"- `{url}` — {detail}")
            for loc in url_locations[url]:
                lines.append(f"  - `{loc}`")
        lines.append("")

    # Stale redirects -- grouped by the shared path-rewrite so a bulk fix is
    # obvious (e.g. "dev/ -> '' (204 links)").
    if n_stale:
        lines.append(
            f"### Stale redirects (works via alias, not canonical) — {n_stale}"
        )
        lines.append("")
        groups = {}
        for url, final_url in findings["stale-redirect"]:
            frm, to = rewrite_rule(url, final_url)
            groups.setdefault((frm, to), []).append((url, final_url))
        for (frm, to), items in sorted(groups.items(), key=lambda kv: -len(kv[1])):
            frm_disp = frm or "∅"
            to_disp = to or "∅"
            lines.append(
                f"#### Replace `{frm_disp}` → `{to_disp}` — {len(items)} link(s)"
            )
            lines.append("")
            for url, final_url in sorted(items):
                loc_count = len(url_locations[url])
                lines.append(
                    f"- `{url}` → `{final_url}` "
                    f"({loc_count} source location(s))"
                )
                for loc in url_locations[url]:
                    lines.append(f"  - `{loc}`")
            lines.append("")

    # Broken anchors -- lower-confidence tier (rendering-dependent); flat list.
    if n_anchor:
        lines.append(
            f"### Broken anchors (page exists, #fragment absent) — {n_anchor}"
        )
        lines.append("")
        lines.append(
            "_Lower confidence: anchor rendering varies by page; verify before "
            "acting._"
        )
        lines.append("")
        for url, detail in sorted(findings["broken-anchor"]):
            lines.append(f"- `{url}` — {detail}")
            for loc in url_locations[url]:
                lines.append(f"  - `{loc}`")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base-dir", default="repos",
        help="Directory containing the repo clones (default: repos).",
    )
    parser.add_argument(
        "--repos", nargs="*", default=None,
        help="Override the repo list (default: the built-in DEFAULT_REPOS).",
    )
    parser.add_argument(
        "--out", default="link-findings.md",
        help="Path to write the findings markdown report.",
    )
    parser.add_argument(
        "--delay", type=float, default=0.3,
        help="Seconds to sleep between requests (single-host rate limiting).",
    )
    args = parser.parse_args()

    repos = args.repos if args.repos else DEFAULT_REPOS

    print(f"Extracting docs.viam.com links from: {', '.join(repos)}")
    url_locations = extract(args.base_dir, repos)
    print(f"Found {len(url_locations)} unique docs.viam.com URL(s).")

    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT

    findings = {}
    ok = 0
    for i, url in enumerate(sorted(url_locations), 1):
        time.sleep(args.delay)
        label, detail = classify(url, session, args.delay)
        if label == "ok":
            ok += 1
        else:
            findings.setdefault(label, []).append((url, detail))
            print(f"  [{label}] {url}  ({detail})")
        if i % 25 == 0:
            print(f"  ...checked {i}/{len(url_locations)}")

    total_findings = sum(len(v) for v in findings.values())
    print(f"\nDone: {ok} ok, {total_findings} problem(s).")

    report = build_report(findings, url_locations) if total_findings else ""
    if report:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(report)
        print(f"Wrote findings to {args.out}")

    # Emit a workflow output flag when running in GitHub Actions.
    gh_out = os.environ.get("GITHUB_OUTPUT")
    if gh_out:
        with open(gh_out, "a", encoding="utf-8") as fh:
            fh.write(f"findings={'true' if total_findings else 'false'}\n")

    # Non-zero exit on findings so the workflow's if: failure() reporting fires.
    return 1 if total_findings else 0


if __name__ == "__main__":
    sys.exit(main())
