---
description: Tag docs pages with capability frontmatter, one section at a time
argument-hint: "<section> (e.g. data, motion-planning, reference/components)"
allowed-tools: Bash, Read, Write, Edit, Task
---

Tag the pages in `docs/$1` with capabilities. Follow this exactly; do not
improvise a shortcut.

## Ground rules

- **You never edit a `.md` file directly.** Classification produces a TSV.
  `scripts/capabilities/apply.py` is the only thing that writes frontmatter.
- **Never read whole pages to classify them.** Evidence packs exist for this.
  Read a full page only to resolve a specific low-confidence row.
- The vocabulary is `data/capabilities.yaml` and nothing else.

## Steps

1. Refresh the deterministic seeds and the classifier prompt:

   ```bash
   python3 scripts/capabilities/prefill.py
   python3 scripts/capabilities/render_prompt.py > .capabilities-work/CLASSIFIER.md
   python3 scripts/capabilities/evidence.py --section "$1" --batch-size 25 \
     --out .capabilities-work/ev-$(echo "$1" | tr / -)
   ```

2. For each batch file produced, dispatch one `Task` subagent. Give it the
   full text of `.capabilities-work/CLASSIFIER.md` followed by the batch's
   JSONL lines. Dispatch all batches for the section in a single message so
   they run concurrently. Each subagent returns TSV text only — it must not
   touch the filesystem.

3. Concatenate the returned TSV into
   `.capabilities-work/llm-$(echo "$1" | tr / -).tsv`. Confirm the line count
   equals the pack count. A short subagent reply means a dropped page: re-run
   that batch rather than accepting the gap.

4. Merge over the seeds, keeping the LLM row wherever one exists, and validate
   before writing anything:

   ```bash
   python3 scripts/capabilities/merge.py --section "$1"
   python3 scripts/capabilities/validate.py --tsv .capabilities-work/final.tsv
   ```

   Fix errors in the TSV, not in the validator.

5. Review the low-confidence rows yourself. For each one, read the actual page
   and either correct the row or leave it and mark it in the summary for a
   human. Do not silently promote a `low` to `high`.

6. Write and check:

   ```bash
   python3 scripts/capabilities/apply.py --in .capabilities-work/final.tsv --dry-run
   python3 scripts/capabilities/apply.py --in .capabilities-work/final.tsv
   npx prettier@3.2.5 --check "docs/$1/**/*.md"
   python3 scripts/capabilities/validate.py
   ```

7. Report back: pages tagged, the capability distribution for the section, how
   many seeds the model overrode (and which), and every row still at `low`
   confidence with its path and reason. Do not commit.
