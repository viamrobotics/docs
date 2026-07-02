# Design: Restructure + Author the Pick-and-Place Workshop to the Finalized Self-Serve Plan

**Date:** 2026-07-02
**Status:** Approved (brainstorm complete; ready for implementation planning)
**Author:** nick.hehr (with Claude Code)
**Branch:** `workshop-format-pick-and-place`
**Related:**

- `../pick-and-place/pick-n-place-tutorial-plan.md` — the finalized content spec (source of truth for page content)
- `../pick-and-place/tutorial-review-notes.md` — per-phase self-serve decision log
- `../pick-and-place/docs/plans/2026-07-01-self-serve-tutorial-review-fixes.md` — the upstream plan that produced the finalized spec (explicitly defers "authoring the Hugo content pages" to this effort)
- `plans/2026-06-30-tutorials-featured-index-and-workshop-nav-design.md` — landing/index/sidebar work already on this branch (unchanged by this effort)

## Context

The multi-page pick-and-place workshop lives at `docs/tutorials/pick-and-place/`
(Hugo + Docsy). It currently has **five** phase pages, of which only Phase 3 is
substantially authored; Phases 1, 2, 4, 5 are structured stubs (headings +
`<!-- TODO -->` markers). The pages were written against an **earlier,
facilitated-workshop** version of the plan.

Meanwhile the plan has been finalized as a **self-serve** tutorial
(`pick-n-place-tutorial-plan.md`), incorporating a full review pass
(`tutorial-review-notes.md`). The upstream review-fixes plan updated the spec
and explicitly deferred authoring the Hugo pages — **that deferred authoring is
this effort.**

The companion code repo is published at
<https://github.com/viam-devrel/pick-and-place> (local working copy at
`../pick-and-place/`), containing `scripts/starter-script.py`,
`scripts/reference-solution.py`, `scripts/pyproject.toml`,
`config/machine-fragment.json`, `config/obstacles-template.json`, and
`setup/frame-calibration-worksheet.md`. All code and JSON in the authored pages
is grounded in this repo, not invented.

## The gap (why this is more than "fill the TODOs")

The finalized plan differs from what is on the branch in three ways:

1. **Structural (5 → 6 phases).** Perception splits out of Phase 4 into a
   dedicated Phase 5; the inline module moves to Phase 6; Phase 4 is renamed
   from "Local Python script" to "Control the robot from Python" and covers the
   static sequence only.
2. **Voice (facilitated → self-serve).** The already-authored `_index.md` and
   Phase 3 actively contradict the finalized plan and must be rewritten, not
   just extended. Examples on the branch today:
   - `_index.md`: "Hardware pre-provisioned for you… if you are in a guided
     workshop" — the plan wants self-serve two-milestone + prerequisites-gate
     framing.
   - `03-static-positions.md`: "Your workshop facilitator provides the table and
     bin dimensions" and "the machine is already configured with
     arm-position-saver switches… pre-loaded configuration" — the plan
     overturns both (measure your own workspace; configure every resource by
     hand; `machine-fragment.json` is a check-your-work reference, not an
     import).
3. **Net-new content.** Every TODO section across the phases must be authored to
   the plan's per-page spec, grounded in the companion code.

## Goals

1. Ship a six-phase, self-serve pick-and-place workshop whose content matches
   `pick-n-place-tutorial-plan.md` and whose code/JSON is verified against the
   published companion repo.
2. Preserve the branch's established house style and the landing/index/sidebar
   work already done — the sidebar/nav shortcodes are load-bearing and must keep
   working.
3. Keep the build green at every commit.

## Non-goals

- No changes to the landing page, `/tutorials/all/` archive, `tutorial-card`,
  `tutorial-hero`, or `sidebar.html` work from the 2026-06-30 design.
- No new shortcodes. Author with the existing
  `workshop-phases` / `workshop-nav` / `checkpoint` / `alert` shortcodes. The
  plan's speculative `code-file` shortcode and `data/tutorials.yaml` stay
  deferred; code is shown as inline fenced blocks with links to the companion
  repo.
- No companion-repo changes and no separate hardware-setup guide in this effort
  (the plan references both; they are downstream). The `_index` links to the
  setup guide as "forthcoming."
- No edits to the facilitated workshop slides.

## House style (authoring must follow the branch, not the plan's speculative schema)

The finalized plan sketches a speculative frontmatter/shortcode schema
(`tutorial:`, `difficulty:`, `checkpoint.html`, `content/`). **Ignore it** in
favor of the conventions the branch actually uses:

- **Directory:** `docs/tutorials/pick-and-place/` (this repo uses `docs/`, not
  `content/`).
- **Frontmatter keys:** `title`, `linkTitle` (numbered, e.g. `"4. Control from
  Python"`), `type: "docs"`, `slug`, `weight`, `description`, `workshop:
  "pick-and-place"`, `toc_hide: true`, `phase`, `phase_total`, `time_estimate`,
  `prev`, `next`, `languages`.
- **Shortcodes:** `{{< workshop-phases >}}` (top of body), `{{< checkpoint >}}`,
  `{{< alert title="…" color="note" >}}`, `{{< workshop-nav >}}` (bottom).
- **Companion links:** real `https://github.com/viam-devrel/pick-and-place`
  URLs.
- **Prose rules:** enforced by prettier, markdownlint (`.markdownlint.yaml`),
  and vale (no em dashes, sentence-case headings, no parenthetical plurals,
  etc.).

## Design

### Part 1 — Restructure (single prep commit; mechanical; build stays green)

| Action | File | Key frontmatter |
| --- | --- | --- |
| Keep | `01-platform-mental-model.md` | `phase: 1`, `phase_total: 6`, `weight: 10`, slug `platform-mental-model` |
| Keep | `02-configure-resources.md` | `phase: 2`, `phase_total: 6`, `weight: 20`, slug `configure-resources` |
| Keep | `03-static-positions.md` | `phase: 3`, `phase_total: 6`, `weight: 30`, slug `static-positions` |
| Rename + strip perception | `04-local-python-script.md` → `04-control-the-robot-from-python.md` | title "Phase 4: Control the robot from Python", slug `control-the-robot-from-python`, `phase: 4`, `phase_total: 6`, `weight: 40` |
| New file | `05-perception-guided-picking.md` | title "Phase 5: Perception-guided picking", slug `perception-guided-picking`, `phase: 5`, `phase_total: 6`, `weight: 50` |
| Renumber | `05-inline-module.md` → `06-inline-module.md` | title "Phase 6: Inline module", slug `inline-module`, `phase: 6`, `phase_total: 6`, `weight: 60` |

Also in this commit:

- Bump `phase_total: 6` on every phase page.
- Rewire the `prev`/`next` chain to:
  `platform-mental-model` → `configure-resources` → `static-positions` →
  `control-the-robot-from-python` → `perception-guided-picking` →
  `inline-module`.
- Rebuild the `_index.md` phase list to six entries with the plan's time
  estimates (15 / 20 / 20 / 15 / 22 / 20 min) and corrected links/titles.
- Move the perception-related TODO scaffolding out of Phase 4 and into the new
  Phase 5 stub so Phase 4 covers the static sequence only.

The `workshop-phases` / `workshop-nav` shortcodes derive phase order from
`section.RegularPages.ByWeight`, so the new Phase 5 page auto-slots once its
`weight` is set. No aliases/redirects are required: the branch is not merged or
live, so no public URLs change. The Phase 4 slug change
(`local-python-script` → `control-the-robot-from-python`) is therefore safe.

### Part 2 — Per-page content (one authoring commit each, grounded in companion code)

Content requirements are the per-page spec in `pick-n-place-tutorial-plan.md`;
the self-serve rationale is in `tutorial-review-notes.md`. Summary per page:

- **`_index.md` (rewrite, facilitated → self-serve).** Two-milestone framing
  (Phase 4 = milestone one, "drive the robot from your own code," a bankable
  win; Phase 5 = milestone two, perception; Phase 6 optional; **Phases 1–5
  core**). Prerequisites **gate** with verify commands *and* install links
  (Python 3.10+, `viam-sdk`, a working terminal, a Viam account with a Live
  machine). Login/machine-access as a prerequisite. Environment validation
  (`uv` recommended, can `import viam`) before Phase 4. Hardware context via the
  setup-guide link + header image, not a tour. Two entry paths distinguishing
  hardware provisioning (may be pre-provisioned) from resource configuration
  (always hands-on). Link to companion repo. Remove resolved TODOs.
- **P1 `01-platform-mental-model.md`.** Three-layer architecture, SDK
  connection, config-as-source-of-truth, components vs. services, dependency
  graph. Live "open your CONFIGURE tab, find `arm-1`, read its
  `namespace:family:model`" grounding throughout (overrides the old "no live
  interactions yet"). Keep `shape-detector` / `vision-segment` foreshadow in the
  dependency graph. Builtin (RDK) vs. module-provided resources, with the
  module-download moment previewed (it lands in P2). Closing self-check.
- **P2 `02-configure-resources.md`.** Hands-on config of `arm-1`, `gripper-1`,
  `cam-1` (resource table as target state, not "what's pre-configured").
  Configuring `viam:ufactory:xArm6` is the module-download moment. 3D-scene
  active task: "jog joint 1, watch `cam-1` move with the arm" (sets up the
  wrist-camera rule). Gripper `IsHoldingSomething` active task. Per-card
  checkpoints (camera, arm, gripper). Vision pipeline is **not** configured here
  — it moves to P5.
- **P3 `03-static-positions.md` (self-serve rewrite).** Problem-isolation
  rationale kept as proof of value (real production workflow). The five key
  poses. Explicit hands-on arm-position-saver setup (`erh:vmodutils` from
  Registry, one switch per pose, `arm: arm-1`), using the app's "duplicate"
  feature for poses 2–5; remove "already configured / pre-loaded" framing.
  Teach frame-geometry config and have the learner **measure their own
  workspace** (remove "facilitator provides dimensions"). Safety walls framed
  as a production-motion feature. SetPosition `1`=save / `2`=execute callout +
  "does nothing" troubleshooting aside. `machine-fragment.json` /
  `obstacles-template.json` as check-your-work references. Reconcile the
  obstacle JSON against the real `config/obstacles-template.json` and the Viam
  motion-service schema (resolves the existing "illustrative JSON" TODO).
- **P4 `04-control-the-robot-from-python.md`.** Why script before module
  (comparison). Sell programmability + the Control-tab-UI→SDK-method-name
  mapping. Clone the companion `scripts/` project and `uv run starter-script.py`
  (`uv` primary, pip fallback; env already validated in the prerequisites gate).
  Reference the Connect-tab boilerplate rather than authoring the connection
  from scratch. Secrets-handling note. Obstacles live in machine config and
  apply to every `motion.move` automatically — **not** passed in code.
  Checkpoints: `resource_names` prints all resources; static sequence runs
  end-to-end from Python. **Static sequence only — no perception.**
- **P5 `05-perception-guided-picking.md` (new).** Configure the vision pipeline
  here (shape-detector → `vision-segment`, `detections-to-segments`) +
  Control-tab test. Frame system + `transform_pose`. **Home-pose guard clause**
  in the perception loop (assert/return to `home-pose` before every detect;
  structurally enforced; first entry in the debugging guide). Worked
  approach-offset as a fully worked example; learner practices the
  gripper-TCP grasp offset (productive struggle). Explicit
  `motion.move("gripper-1", …)` frame semantics (drives the gripper frame to the
  world pose — contrast with the arm/UI MoveToPosition). Perception API using
  `len(o.point_cloud)`. Symptom → 3D-scene-tab debugging with a back-link to P3
  obstacle/safety-wall config. Granular sub-checkpoints (detector works →
  transform yields sane world coords → approach reachable → grasp succeeds). All
  code verified against `reference-solution.py`, including the gripper-TCP
  offset value and `PoseInFrame` kwargs.
- **P6 `06-inline-module.md` (optional).** Framed as an optional next step (no
  time pressure). Strong "why bother" (survives disconnection, auto-restart, OTA
  deploy, scheduled runs). Honest "mostly packaging + one real change." Tiered
  scope: MVP (repackage + `do_command`, manual trigger) vs. level-2 (scheduled
  job / autonomous). `validate_config` + `reconfigure` (dependency injection).
  **Corrected `transform_pose`-in-module pattern:** a single reused in-module
  `RobotClient` authenticated from `VIAM_API_KEY` / `VIAM_API_KEY_ID` /
  `VIAM_MACHINE_FQDN` env vars — there is **no** `FrameSystemClient` and no
  injected frame-system dependency (this reverses the current stub's incorrect
  note). `from_robot` ↔ `cast + get_resource_name` bridge callout. ~1 min cloud
  build time stated upfront.

### Part 3 — Correctness grounding

- Python snippets are drawn from / verified against
  `../pick-and-place/scripts/{starter-script.py,reference-solution.py}`.
- Machine-config and obstacle JSON are verified against
  `../pick-and-place/config/{machine-fragment.json,obstacles-template.json}` and
  the Viam motion-service obstacle schema.
- Two known correctness items to resolve during authoring: the "illustrative"
  obstacle JSON in P3, and the fabricated `FrameSystemClient` note in P6.
- Remove now-stale TODO comments that say the companion repo "does not exist yet"
  (it is published).

### Part 4 — Verification

Per commit, run the CLAUDE.md pre-PR checks on the changed Markdown, in order:

1. `npx prettier --write docs/tutorials/pick-and-place/**/*.md`
2. `npx markdownlint-cli --config .markdownlint.yaml docs/tutorials/pick-and-place/**/*.md`
3. `vale sync && vale docs/tutorials/pick-and-place/`
4. `make build-prod` (must complete without errors)

Spot-check with `hugo server`: the six phases appear in order in the
`workshop-phases` box and the sidebar with the current phase highlighted;
`workshop-nav` prev/next chains correctly across all six; the landing card and
`/tutorials/all/` archive are unaffected. No unit tests (docs site).

### Part 5 — Sequencing

Commit this design doc first, then:

1. Restructure prep commit (Part 1).
2. `_index.md` rewrite.
3. Phase 1 authoring.
4. Phase 2 authoring.
5. Phase 3 self-serve rewrite.
6. Phase 4 authoring.
7. Phase 5 authoring (new page).
8. Phase 6 authoring (corrected module API).

Each step keeps the build green and passes the four checks before committing.

## Risks / watch-items

- **Nav derivation:** confirm the new Phase 5 page slots correctly in
  `workshop-phases` / `workshop-nav` (weight-ordered) and that `phase_total: 6`
  renders consistently.
- **Slug change:** the Phase 4 slug change must be reflected in every `prev`/`next`
  reference and the `_index` phase list; grep for the old
  `/local-python-script/` and `/inline-module/` (position 5) URLs after the
  restructure.
- **Obstacle JSON schema:** the existing P3 JSON is flagged illustrative;
  reconcile against the real template + Viam schema before publishing.
- **Module API correctness:** ensure the P6 rewrite fully removes the
  `FrameSystemClient` pattern and matches the in-module `RobotClient` reference.
- **Scope creep into landing/sidebar:** this effort touches only
  `docs/tutorials/pick-and-place/*`; the 2026-06-30 layout work is out of scope.

## Out-of-scope follow-ups (noted, not now)

- Companion-repo code changes (e.g. adding the home-pose guard clause to
  `reference-solution.py`).
- The separate hardware-setup how-to guide
  (`docs/guides/hardware-setup/xarm6-pick-and-place.md`).
- The `code-file` shortcode and `data/tutorials.yaml` card-grid data file.
- Header/hardware-overview imagery for `_index` and the landing card.
