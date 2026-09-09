#!/usr/bin/env python3
"""Phase 4: write capabilities into frontmatter.

Line-based and idempotent: it inserts or replaces exactly one `capabilities:`
line and leaves every other byte of the file alone. Never let a model edit
these files directly - it emits a TSV, this writes it.

    python3 scripts/capabilities/apply.py --in .capabilities-work/final.tsv --dry-run
    python3 scripts/capabilities/apply.py --in .capabilities-work/final.tsv
"""
import os, re, sys, argparse
sys.path.insert(0, os.path.dirname(__file__))
from lib import read_tsv, DOCS, WORK, load_taxonomy, vocab

CAP_LINE = re.compile(r"^capabilities:.*$")
DESC = re.compile(r"^description:")
TITLE = re.compile(r"^(title|linkTitle):")
KEY = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*:")


def render(caps):
    return "capabilities: [" + ", ".join(f'"{c}"' for c in caps) + "]"


def upsert(text, caps):
    if not text.startswith("---\n"):
        return None, "no frontmatter"
    end = text.index("\n---", 4)
    fm = text[4:end].split("\n")
    rest = text[end:]

    fm = [l for l in fm if not CAP_LINE.match(l)]

    anchor = None
    for i, l in enumerate(fm):
        if DESC.match(l):
            anchor = i
    if anchor is None:
        for i, l in enumerate(fm):
            if TITLE.match(l):
                anchor = i
    if anchor is None:
        fm.append(render(caps))
    else:
        j = anchor + 1
        while j < len(fm) and not KEY.match(fm[j]):   # skip folded/continued values
            j += 1
        fm.insert(j, render(caps))
    return "---\n" + "\n".join(fm) + rest, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="src", default=os.path.join(WORK, "final.tsv"))
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    V = vocab(load_taxonomy())
    rows = read_tsv(a.src)
    written = skipped = 0
    problems = []

    for r in rows:
        caps = r["capabilities"]
        if not caps:
            problems.append((r["path"], "no capabilities"))
            continue
        bad = [c for c in caps if c not in V]
        if bad:
            problems.append((r["path"], "unknown: " + ",".join(bad)))
            continue
        full = os.path.join(DOCS, r["path"])
        if not os.path.exists(full):
            problems.append((r["path"], "missing file"))
            continue
        with open(full, encoding="utf-8") as f:
            text = f.read()
        new, err = upsert(text, caps)
        if err:
            problems.append((r["path"], err))
            continue
        if new == text:
            skipped += 1
            continue
        if not a.dry_run:
            with open(full, "w", encoding="utf-8") as f:
                f.write(new)
        written += 1

    verb = "would write" if a.dry_run else "wrote"
    print(f"{verb} {written} | unchanged {skipped} | problems {len(problems)}")
    for p, why in problems[:40]:
        print(f"  ! {p}: {why}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
