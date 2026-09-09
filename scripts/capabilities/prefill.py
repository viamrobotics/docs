#!/usr/bin/env python3
"""Phase 1: deterministic seed pass.

Applies the `seeds` globs from data/capabilities.yaml plus a structural
heuristic for section landing pages. Costs no model tokens and covers the
majority of pages with at least a primary capability.

    python3 scripts/capabilities/prefill.py            # write .capabilities-work/seeds.tsv
    python3 scripts/capabilities/prefill.py --stats    # coverage summary only
"""
import os, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
from lib import (load_taxonomy, vocab, all_pages, _match, read_page,
                 split_front_matter, parse_fm, body_words, write_tsv, WORK, EXCLUDE)


def classify_shape(rel, fm, body):
    """Bucket a page by shape before any topic reasoning happens.

    content  a normal page; needs a topic capability
    index    a navigation landing page; section-index + one topic
    stub     a body-less page that redirects to an external canonical URL;
             classify from frontmatter only, or skip by team decision
    """
    words = body_words(body)
    canonical = str(fm.get("canonical") or "")
    if fm.get("empty_node"):
        return "index"
    if words < 30 and canonical.startswith("http"):
        return "stub"
    if os.path.basename(rel) == "_index.md" and words < 250:
        return "index"
    if fm.get("layout") == "empty" and words < 30:
        return "stub"
    return "content"


def main():
    tax = load_taxonomy()
    V = vocab(tax)
    seeds = [(cap, g) for cap, v in tax["capabilities"].items()
             for g in (v.get("seeds") or []) if cap in V]

    rows, stats, shapes = [], collections.Counter(), collections.Counter()
    for rel in all_pages(EXCLUDE):
        fm_text, body = split_front_matter(read_page(rel))
        fm = parse_fm(fm_text)

        caps = []
        for cap, g in seeds:
            if _match(rel, g) and cap not in caps:
                caps.append(cap)

        shape = classify_shape(rel, fm, body)
        shapes[shape] += 1

        # glossary is exclusive except for its docs pairing
        if "glossary" in caps:
            caps = ["glossary", "docs"] if "docs" in caps else ["glossary"]
        elif shape == "index":
            caps = ([c for c in caps if c != "section-index"][:1]) + ["section-index"]

        source = "seed" if caps else "none"
        rows.append({"path": rel, "capabilities": caps, "source": source,
                     "confidence": "high" if caps else "",
                     "note": shape})
        stats[len(caps)] += 1

    write_tsv(os.path.join(WORK, "seeds.tsv"), rows)
    total = len(rows)
    seeded = total - stats[0]
    print(f"{total} pages | {seeded} seeded ({seeded*100//total}%) | {stats[0]} unseeded")
    print(f"  1 cap: {stats[1]}   2 caps: {stats[2]}   3+: {sum(v for k,v in stats.items() if k>=3)}")
    print(f"  shapes: content={shapes['content']} index={shapes['index']} stub={shapes['stub']}")
    print(f"-> {os.path.join(WORK,'seeds.tsv')}")
    if "--stats" in sys.argv:
        by_cap = collections.Counter(c for r in rows for c in r["capabilities"])
        print("\nper capability:")
        for cap in sorted(V):
            print(f"  {by_cap.get(cap,0):4d}  {cap}")


if __name__ == "__main__":
    main()
