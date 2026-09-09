#!/usr/bin/env python3
"""Phase 5: QA gate. Run against the repo after apply, and in CI afterwards.

Checks, in order of how often they catch something real:
  1  every page has 1..max_per_page capabilities, all in the vocabulary
  2  no capability marked status: undefined is in use
  3  structural pairing: glossary alone; section-index + at most 1 topic
  4  capabilities with zero pages (fine if the feature is not public yet - listed)
  5  capabilities with a suspiciously large share (usually a bad tie-breaker)
  6  sibling drift: a page whose tags share nothing with any sibling in its dir

    python3 scripts/capabilities/validate.py            # read from the .md files
    python3 scripts/capabilities/validate.py --tsv X    # read from a TSV instead
"""
import os, sys, argparse, collections
sys.path.insert(0, os.path.dirname(__file__))
from lib import (load_taxonomy, vocab, all_pages, read_page, split_front_matter,
                 parse_fm, read_tsv, WORK, EXCLUDE)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tsv")
    ap.add_argument("--max-share", type=float, default=0.20)
    a = ap.parse_args()

    tax = load_taxonomy()
    V = vocab(tax)
    UNDEF = vocab(tax, True) - V
    rules = tax["rules"]

    if a.tsv:
        data = {r["path"]: r["capabilities"] for r in read_tsv(a.tsv)}
    else:
        data = {}
        for rel in all_pages(EXCLUDE):
            fm, _ = split_front_matter(read_page(rel))
            data[rel] = (parse_fm(fm) or {}).get("capabilities") or []

    errors, warnings = [], []

    for rel, caps in sorted(data.items()):
        if not caps:
            errors.append(f"{rel}: no capabilities")
            continue
        for c in caps:
            if c in UNDEF:
                errors.append(f"{rel}: '{c}' is status: undefined")
            elif c not in V:
                errors.append(f"{rel}: unknown capability '{c}'")
        if len(caps) > rules["max_per_page"]:
            warnings.append(f"{rel}: {len(caps)} capabilities (cap is {rules['max_per_page']})")
        if len(set(caps)) != len(caps):
            errors.append(f"{rel}: duplicate capability")
        if "glossary" in caps and any(c not in ("glossary", "docs") for c in caps):
            errors.append(f"{rel}: glossary must stand alone (except pairing with docs)")
        if "section-index" in caps and len(caps) > 1 + rules["structural_pairing"]:
            warnings.append(f"{rel}: section-index with >{rules['structural_pairing']} topic tags")

    counts = collections.Counter(c for caps in data.values() for c in caps)
    total = len(data)
    unused = sorted(V - set(counts))
    over = [(c, n) for c, n in counts.items()
            if c not in ("section-index", "glossary") and n / total > a.max_share]

    bydir = collections.defaultdict(list)
    for rel, caps in data.items():
        bydir[os.path.dirname(rel)].append((rel, set(caps)))
    drift = []
    for d, items in bydir.items():
        if len(items) < 3:
            continue
        for rel, caps in items:
            others = set().union(*[c for r, c in items if r != rel]) if len(items) > 1 else set()
            if caps and not (caps - {"section-index"}) & others:
                drift.append(rel)

    print(f"pages: {total}   distinct capabilities used: {len(counts)}/{len(V)}")
    print(f"errors: {len(errors)}   warnings: {len(warnings)}")
    for e in errors[:40]:
        print("  ERROR  " + e)
    for w in warnings[:20]:
        print("  warn   " + w)
    if unused:
        print(f"\nunused ({len(unused)}) - expected for features not yet in public docs:")
        print("  " + ", ".join(unused))
    if over:
        print("\noversized - check the tie-breaker for these:")
        for c, n in sorted(over, key=lambda x: -x[1]):
            print(f"  {c}: {n} pages ({n*100//total}%)")
    if drift:
        print(f"\nsibling drift ({len(drift)}) - shares no capability with any sibling:")
        for r in drift[:25]:
            print("  " + r)
    print("\nfull distribution:")
    for c, n in counts.most_common():
        print(f"  {n:4d}  {c}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
