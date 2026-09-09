# Capability tagging playbook

Adding a `capabilities:` frontmatter key to every page under `docs/`.

The naive version of this job — hand Claude Code the tag list and 531 markdown
files — costs roughly 1.5M input tokens, produces tags that drift between
sections because each context window sees a different slice of the corpus, and
leaves you with no way to tell a considered tag from a guess. This playbook
does the same job for about a tenth of that, and every tag arrives with a
source and a confidence attached.

Three ideas carry it:

1. **Most pages are decided by their path, not their prose.** `docs/` is
   organised by subject already. A glob pass assigns a correct primary tag to
   83% of pages for free.
2. **Classification and file-writing are separate jobs.** Models classify and
   emit a TSV. A deterministic script writes frontmatter. A model never edits a
   `.md` file, so a bad batch costs you a re-run and not a dirty tree.
3. **Judgment runs on evidence packs, not pages.** A 200-token digest — title,
   description, headings, opening lines, outbound links, seeded guess — is
   enough to tag a page. Full pages get read only to settle a specific
   low-confidence row.

## Current state of the corpus

| | count |
|---|---|
| pages under `docs/` (excluding two templates) | 531 |
| seeded deterministically by path rule | 444 (83%) |
| needing full judgment | 87 |
| normal content pages | 426 |
| navigation landing pages | 78 |
| body-less stubs redirecting to codelabs/blog | 27 |
| evidence packs for the whole corpus | ~108k tokens (~203/page) |

## Files

| file | what it is |
|---|---|
| `data/capabilities.yaml` | the vocabulary. Single source of truth for the prompt, the seeds, and the validator |
| `scripts/capabilities/prefill.py` | phase 1 — path-glob seeds plus page-shape detection |
| `scripts/capabilities/evidence.py` | phase 2 — compact per-page evidence packs |
| `scripts/capabilities/render_prompt.py` | generates the classifier prompt from the taxonomy |
| `scripts/capabilities/merge.py` | phase 3.5 — precedence merge: manual > llm > seed |
| `scripts/capabilities/apply.py` | phase 4 — the only thing that writes frontmatter |
| `scripts/capabilities/validate.py` | phase 5 — the QA gate |
| `.claude/commands/tag-capabilities.md` | `/tag-capabilities <section>` — the run loop |

Everything intermediate lands in `.capabilities-work/` (gitignored).

## The taxonomy file

Each capability carries a `summary`, what it `covers`, a `not` field, and its
`seeds` globs. The `not` field is the one that does the work — it is where the
tie-breakers live, and it is injected verbatim into the classifier prompt:

```yaml
data-capture:
  summary: Capture and sync from the machine.
  not: Anything about data already in the cloud is data-storage.
  seeds: ["data/capture-sync/**/*.md", "data/filter-at-the-edge.md"]
```

When a review pass finds a systematic mistake, the fix goes in the `not` field,
not into a one-off correction. That is what stops the same confusion recurring
in the next section.

Also in the file: `status: undefined` marks a capability that cannot be used
yet. `rdk-activity` has it, because the definition is blank.

## Running it

Per section, via `/tag-capabilities <section>`:

```
prefill  ──▶  evidence  ──▶  N subagents  ──▶  merge  ──▶  validate  ──▶  apply  ──▶  validate
   │             │              │                                          │
 seeds.tsv   batch-NN.jsonl   llm-*.tsv                              frontmatter
```

Batch at 25 pages: about 5k tokens of evidence plus the 2.3k prompt in, ~1k
out. All batches for a section dispatch in one message so they run
concurrently. A full pass over all 531 pages is roughly 165k in / 25k out.

Section order matters. Run in this sequence, reviewing between each:

1. **`reference/`** (210 pages) — highest seed coverage, most mechanical.
   Confirms the seeds are right before you rely on them elsewhere.
2. **`data/`, `fleet/`, `organization/`, `cli/`, `monitor/`** — the tie-breaker
   pairs live here (`data-capture`/`data-storage`/`data-pipelines`,
   `machine-config`/`fleet-deployment`). Expect to edit `not` fields.
3. **`hardware/`, `motion-planning/`, `vision/`, `train/`, `visualization/`** —
   mostly seeded, secondary tags need judgment.
4. **`build-apps/`, `build-modules/`, `set-up-a-machine/`** — the unseeded
   remainder.
5. **`tutorials/`, `try/`** — last, and only after the open questions below are
   settled. These are the pages where the taxonomy fits worst.

## Quality gates

`validate.py` runs against the TSV before writing and against the repo after.
It fails the build on: a page with no capability, an unknown or `undefined`
capability, a duplicate, or `glossary` paired with anything. It warns on: more
than three tags, and `section-index` with more than one topic tag.

It also reports three things that are not errors but are how you find
systematic problems:

- **Unused capabilities.** Expected for features not yet public. If something
  you thought was documented shows zero pages, either the tag is wrong or the
  docs gap is real.
- **Oversized capabilities.** Anything over 20% of the corpus usually means a
  tie-breaker is too permissive and the tag is absorbing its neighbours.
- **Sibling drift.** A page sharing no capability with any sibling in its
  directory. Sometimes correct, usually a mistake.

Beyond the automated gate, two human passes are worth the time: read every
`low`-confidence row (the pilot ran 12%), and spot-check ten `high`-confidence
rows per section — high-confidence errors are the ones that survive to
production.

Wire the validator into CI once the first section lands, so new pages cannot
ship untagged:

```yaml
- run: python3 scripts/capabilities/validate.py
```

## What the pilot found

25 pages, stratified across unseeded content, seeded content, landing pages and
stubs. 16 high / 6 medium / 3 low confidence. The model kept the seeded primary
on 12 of 13 seeded rows.

The single override was a real bug, not a model error: a seed glob was pointing
`build-apps/tasks/handle-connection-state.md` at `machine-connectivity`, but the
page is about SDK reconnection in application code, not machine-to-machine
comms. Fixed in the taxonomy. **This is the argument for the pilot** — one
mistagged glob would have silently produced a wrong tag on every page it
matched, and no amount of careful per-page classification would have caught it.

Frontmatter output is a single line, placed after `description:`, and survives
`prettier@3.2.5 --check` untouched:

```yaml
capabilities: ["vision-service", "hw-camera"]
```

## Open questions — settle these before the tutorials run

1. **`rdk-activity` has no definition.** It is `status: undefined` and the
   validator rejects it. Define it or delete it.
2. **`try/` has no home in the taxonomy.** 18 pages about rover reservations,
   Gazebo simulation setup and a guided inspection walkthrough. Both pilot rows
   from this section came back `low`. Either add a capability for guided
   onboarding, or exclude the section.
3. **Multi-subject landing pages strain the one-topic rule.** `monitor/_index.md`
   fronts dashboards, alerts, teleop and logs equally; picking one topic tag is
   arbitrary. Either raise `structural_pairing` to 2 for `_index.md`, or accept
   `section-index` alone for these.
4. **The 27 external stubs.** Body-less pages whose canonical URL points at
   codelabs.viam.com. They can be tagged from frontmatter alone, but the tag
   describes content that lives off-site. Tag them or skip them.
5. **`mobile-app`, `sequences`, `surface-finishing` seeded zero pages.** Confirm
   these are genuinely not in public docs yet rather than tags whose pages exist
   under names the seeds missed.
6. **Should `capabilities` become a Hugo taxonomy?** Registering it in
   `config.toml` alongside `tags` gives you `/capabilities/<id>/` listing pages
   and makes the tagging visible to readers, not just to search. Worth deciding
   before the tags land, because it affects whether tag names need to be
   presentable.

## Extending it

New capability: add it to `data/capabilities.yaml` with a `not` field and any
obvious `seeds`, re-run `prefill.py`, and re-run only the affected sections.
The prompt regenerates itself, so nothing else needs touching.

New page: CI catches it as an error. Tag it by hand, or run the command for
that one section.
