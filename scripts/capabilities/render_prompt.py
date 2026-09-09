#!/usr/bin/env python3
"""Render the classifier prompt from data/capabilities.yaml.

The prompt is generated, never hand-written, so the vocabulary the model sees
can never drift from the vocabulary the validator enforces.

    python3 scripts/capabilities/render_prompt.py > .capabilities-work/CLASSIFIER.md
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from lib import load_taxonomy, vocab

tax = load_taxonomy()
V = vocab(tax)
r = tax["rules"]

lines = []
for cap in sorted(V):
    v = tax["capabilities"][cap]
    s = f"- **{cap}** — {v['summary']}"
    if v.get("covers"):
        s += f" Covers: {'; '.join(v['covers'])}."
    if v.get("not"):
        s += f" NOT: {' '.join(str(v['not']).split())}"
    lines.append(s)

print(f"""# Capability classifier

You are labelling pages of the Viam public docs with capability tags. A tag
answers "what can a reader DO after reading this page", so that someone
filtering the docs by capability finds the pages that actually teach it.

## Input

One JSON object per line. Each is an evidence pack for one page:

`path`, `title`, `description`, `shape`, `seed`, `headings`, `opening`,
`links_to`, `code_langs`, and sometimes `frontmatter_hints` / `resource_kind`.

- `seed` is a deterministic path-rule guess. **Trust it as the primary tag
  unless the evidence clearly contradicts it.** Your main job is to confirm it
  and decide whether a second or third tag is warranted.
- `frontmatter_hints` are derived from the page's `viamresources` field. These
  over-report: a tutorial lists every resource it touches. Treat them as
  candidates to consider, never as answers.
- `shape` is `content`, `index`, or `stub`.

## The rule that matters most

**Tag what the page teaches you to do, not every noun it mentions.**

A motion-planning page that shows one `viam` CLI command is not `cli`. A data
page that mentions a camera is not `hw-camera`. If a reader filtering on tag X
would open this page and feel misled, do not apply X.

Apply a second tag only when the page genuinely serves two capabilities — for
example a page that both configures data capture and sets up a pipeline over
it. Most pages get one tag. Roughly a third get two. Three is rare.

## Rules

1. {r['min_per_page']} to {r['max_per_page']} tags per page, most important first.
2. Use only the vocabulary below. Never invent a tag, never guess at a spelling.
3. `glossary` stands alone — never combine it with anything.
4. `section-index` takes at most {r['structural_pairing']} topic tag: the subject of the section it fronts.
5. `shape: stub` pages have no body; judge from title, description and hints alone.
6. If you cannot get to `high` or `medium` confidence, output `low` and say why
   in the note. Low-confidence rows go to a human — that is a working outcome,
   not a failure.

## Vocabulary

{chr(10).join(lines)}

## Output

Tab-separated, one line per input page, in input order. No preamble, no
commentary, no code fence, no header row. Five columns:

```
path\tcap1,cap2\tllm\tconfidence\tshort reason
```

- column 3 is the literal string `llm`
- confidence is `high`, `medium`, or `low`
- the reason is at most 12 words, and must justify the *primary* tag

Emit exactly one line for every input line. Do not edit any file.
""")
