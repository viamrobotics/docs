#!/usr/bin/env python3
"""Phase 2: build compact evidence packs.

A pack is everything a classifier needs to judge a page without reading it:
title, description, seeded guess, frontmatter hints, headings, opening lines,
and where the page links to. ~250-400 tokens each instead of 1-6k for the
full page.

    python3 scripts/capabilities/evidence.py                       # all pages
    python3 scripts/capabilities/evidence.py --section data        # one section
    python3 scripts/capabilities/evidence.py --only unseeded       # 0-capability pages
    python3 scripts/capabilities/evidence.py --batch-size 20       # split into batches
"""
import os, re, sys, json, argparse, collections
sys.path.insert(0, os.path.dirname(__file__))
from lib import (read_page, split_front_matter, parse_fm, read_tsv, WORK, DOCS)

HEAD_RE = re.compile(r"^(#{2,3})\s+(.+)$", re.M)
LINK_RE = re.compile(r"\]\((/[a-z0-9\-/]+)")
FENCE_RE = re.compile(r"^```(\w+)", re.M)
SHORTCODE_RE = re.compile(r"\{\{[<%]\s*([a-z\-]+)")

# frontmatter viamresources -> capability hint (a hint, never an auto-assignment:
# tutorials list every resource they touch)
RESOURCE_HINT = {
    "arm": "hw-arm", "base": "hw-mobility", "board": "hw-compute",
    "camera": "hw-camera", "encoder": "hw-sensing", "gantry": "hw-gantry",
    "gripper": "hw-actuation", "input_controller": "hw-sensing",
    "motor": "hw-actuation", "movement_sensor": "hw-sensing",
    "sensor": "hw-sensing", "sensors": "hw-sensing", "servo": "hw-actuation",
    "data_manager": "data-capture", "motion": "motion-planning",
    "frame_system": "frame-system", "mlmodel": "ml-models",
    "navigation": "navigation", "base_remote_control": "hw-mobility",
    "slam": "slam", "vision": "vision-service",
}


def opening(body, n=60):
    text = re.sub(r"\{\{[<%].*?[%>]\}\}", " ", body, flags=re.S)
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"[#*_>`]", "", text)
    return " ".join(text.split()[:n])


def pack(rel, seed_row):
    fm_text, body = split_front_matter(read_page(rel))
    fm = parse_fm(fm_text)
    links = collections.Counter(
        "/".join(m.strip("/").split("/")[:2]) for m in LINK_RE.findall(body)
    )
    hints = sorted({RESOURCE_HINT[r] for r in (fm.get("viamresources") or [])
                    if r in RESOURCE_HINT})
    p = {
        "path": rel,
        "title": fm.get("title") or fm.get("linkTitle") or "",
        "description": fm.get("description") or fm.get("short_description") or "",
        "shape": (seed_row or {}).get("note", "content"),
        "seed": (seed_row or {}).get("capabilities", []),
        "headings": [h[1].strip() for h in HEAD_RE.findall(body)][:12],
        "opening": opening(body),
        "links_to": [k for k, _ in links.most_common(8)],
        "code_langs": sorted(set(FENCE_RE.findall(body)))[:6],
    }
    if hints:
        p["frontmatter_hints"] = hints
    if fm.get("resource"):
        p["resource_kind"] = fm["resource"]
    return p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--section", help="top-level docs/ dir to limit to")
    ap.add_argument("--only", choices=["unseeded", "seeded", "content", "stub", "index"])
    ap.add_argument("--batch-size", type=int, default=0)
    ap.add_argument("--out", default=os.path.join(WORK, "evidence"))
    a = ap.parse_args()

    seeds = {r["path"]: r for r in read_tsv(os.path.join(WORK, "seeds.tsv"))}
    rels = sorted(seeds)
    if a.section:
        rels = [r for r in rels if r.startswith(a.section.rstrip("/") + "/")]
    if a.only == "unseeded":
        rels = [r for r in rels if not seeds[r]["capabilities"]]
    elif a.only == "seeded":
        rels = [r for r in rels if seeds[r]["capabilities"]]
    elif a.only in ("content", "stub", "index"):
        rels = [r for r in rels if seeds[r]["note"] == a.only]

    packs = [pack(r, seeds.get(r)) for r in rels]
    os.makedirs(a.out, exist_ok=True)
    size = a.batch_size or len(packs) or 1
    for i in range(0, len(packs), size):
        name = f"batch-{i//size:02d}.jsonl" if a.batch_size else "all.jsonl"
        with open(os.path.join(a.out, name), "w", encoding="utf-8") as f:
            for p in packs[i:i+size]:
                f.write(json.dumps(p, ensure_ascii=False) + "\n")
    chars = sum(len(json.dumps(p)) for p in packs)
    print(f"{len(packs)} packs -> {a.out}  (~{chars//4} tokens, ~{chars//4//max(len(packs),1)}/page)")


if __name__ == "__main__":
    main()
