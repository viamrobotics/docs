#!/usr/bin/env python3
"""Phase 3.5: merge classifier output over the deterministic seeds.

Precedence: manual > llm > seed. Rows with no capability from any source are
kept in the output so validate.py reports them instead of silently dropping.

    python3 scripts/capabilities/merge.py                 # merge everything found
    python3 scripts/capabilities/merge.py --section data  # limit to one section
"""
import os, sys, glob, argparse, collections
sys.path.insert(0, os.path.dirname(__file__))
from lib import read_tsv, write_tsv, WORK

ORDER = {"seed": 0, "llm": 1, "manual": 2}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--section")
    ap.add_argument("--out", default=os.path.join(WORK, "final.tsv"))
    a = ap.parse_args()

    best = {}
    files = ([os.path.join(WORK, "seeds.tsv")]
             + sorted(glob.glob(os.path.join(WORK, "llm-*.tsv")))
             + sorted(glob.glob(os.path.join(WORK, "manual-*.tsv"))))
    for fp in files:
        for r in read_tsv(fp):
            if a.section and not r["path"].startswith(a.section.rstrip("/") + "/"):
                continue
            cur = best.get(r["path"])
            if cur is None or ORDER.get(r["source"], 0) >= ORDER.get(cur["source"], 0):
                if r["capabilities"] or cur is None:
                    best[r["path"]] = r

    rows = [best[p] for p in sorted(best)]
    write_tsv(a.out, rows)
    src = collections.Counter(r["source"] for r in rows)
    conf = collections.Counter(r["confidence"] for r in rows if r["source"] == "llm")
    print(f"{len(rows)} rows -> {a.out}")
    print("  by source: " + ", ".join(f"{k}={v}" for k, v in src.most_common()))
    if conf:
        print("  llm confidence: " + ", ".join(f"{k}={v}" for k, v in conf.most_common()))
    empty = [r["path"] for r in rows if not r["capabilities"]]
    if empty:
        print(f"  {len(empty)} rows still have no capability")


if __name__ == "__main__":
    main()
