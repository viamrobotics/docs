"""Shared helpers for the capability tagging toolchain."""
import os, re, sys, glob, yaml

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DOCS = os.path.join(REPO, "docs")
TAXONOMY = os.path.join(REPO, "data", "capabilities.yaml")
WORK = os.path.join(REPO, ".capabilities-work")

# Template scaffolding, never tagged: not real pages, just phase/topic skeletons
# authors copy to start a new tutorial. Shared so prefill.py and validate.py
# agree on what's out of scope.
EXCLUDE = ["*_phase-template.md", "tutorials/template.md"]

FM_RE = re.compile(r"\A---\n(.*?)\n---\n?", re.S)


def load_taxonomy():
    with open(TAXONOMY) as f:
        return yaml.safe_load(f)


def vocab(tax, include_undefined=False):
    return {
        k for k, v in tax["capabilities"].items()
        if include_undefined or v.get("status", "active") == "active"
    }


def all_pages(exclude_globs=()):
    out = []
    for root, dirs, files in os.walk(DOCS):
        dirs[:] = [d for d in dirs if d not in (".git", "node_modules")]
        for fn in files:
            if not fn.endswith(".md"):
                continue
            rel = os.path.relpath(os.path.join(root, fn), DOCS)
            if any(_match(rel, g) for g in exclude_globs):
                continue
            out.append(rel)
    return sorted(out)


def _match(rel, pattern):
    import fnmatch
    if "**" in pattern:
        head = pattern.split("**")[0]
        tail = pattern.split("**")[-1].lstrip("/")
        return rel.startswith(head) and fnmatch.fnmatch(os.path.basename(rel), tail or "*")
    return fnmatch.fnmatch(rel, pattern)


def split_front_matter(text):
    """Return (frontmatter_text_or_None, body)."""
    m = FM_RE.match(text)
    if not m:
        return None, text
    return m.group(1), text[m.end():]


def read_page(rel):
    with open(os.path.join(DOCS, rel), encoding="utf-8") as f:
        return f.read()


def parse_fm(fm_text):
    if fm_text is None:
        return {}
    try:
        return yaml.safe_load(fm_text) or {}
    except Exception:
        return {}


def body_words(body):
    stripped = re.sub(r"\{\{[<%].*?[%>]\}\}", " ", body, flags=re.S)
    stripped = re.sub(r"```.*?```", " ", stripped, flags=re.S)
    stripped = re.sub(r"<[^>]+>", " ", stripped)
    return len(stripped.split())


def read_tsv(path):
    rows = []
    if not os.path.exists(path):
        return rows
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            while len(parts) < 5:
                parts.append("")
            rows.append({
                "path": parts[0],
                "capabilities": [c for c in parts[1].split(",") if c],
                "source": parts[2],
                "confidence": parts[3],
                "note": parts[4],
            })
    return rows


def write_tsv(path, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("# path\tcapabilities\tsource\tconfidence\tnote\n")
        for r in rows:
            f.write("\t".join([
                r["path"], ",".join(r["capabilities"]),
                r.get("source", ""), str(r.get("confidence", "")),
                (r.get("note", "") or "").replace("\t", " "),
            ]) + "\n")
