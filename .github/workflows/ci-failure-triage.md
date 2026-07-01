# CI failure triage

This document describes how failures in the scheduled CI jobs are reported and
triaged, so anyone can understand, run, or change the process.

## Overview

The scheduled jobs have no pull request to block, so they can't fail loudly the
way PR checks do. Instead there are two halves:

1. **Report** — when a scheduled job fails, it opens (or updates) a GitHub issue
   labeled `ci-failure`.
2. **Triage** — once a day, an automated Claude Code session reads the open
   `ci-failure` issues, verifies each failure against the actual run, and either
   opens a fix PR or comments with the root cause.

```text
scheduled job fails
   └─ report-ci-failure composite action  →  GitHub issue (label: ci-failure)
                                                 └─ daily triage session  →  fix PR  (fixable)
                                                                          └─ comment (transient / owner decision)
```

This replaced the previous `atlassian/gajira-*` Jira integration, which had
stopped authenticating and left the jobs silently unmonitored.

## 1. Reporting (in-repo)

Each of `test-code-snippets.yml`, `check-methods.yml`, and `run-htmltest.yml`
ends with a `Report failure` step (gated `if: failure()`) that calls the local
composite action [`.github/actions/report-ci-failure`](../actions/report-ci-failure/action.yml):

- Opens an issue titled `CI failure: <job name>` with the `ci-failure` label and
  a link to the failing run.
- If an open `ci-failure` issue for that job already exists, it comments the new
  run link instead of opening a duplicate, so repeat failures collapse into one
  tracking issue.
- Authenticates with the automatic `GITHUB_TOKEN` (the workflows grant
  `issues: write`). No external service or extra secret.

To wire the reporter into another scheduled workflow, add `issues: write` to its
permissions and a final step:

```yaml
- name: Report failure
  if: failure()
  uses: ./.github/actions/report-ci-failure
  with:
    job-name: <human-readable job name>
```

## 2. Triage (Claude Code scheduled session)

A scheduled **Claude Code** session runs daily (~6 AM US Eastern) and triages the
open `ci-failure` issues. It runs under a maintainer's Claude account (no API key
or extra secret) and produces PRs on `claude/ci-fix-<slug>` branches, mirroring
how the repo's other `claude/*` PRs are made.

**At a glance:**

- **Frequency:** daily, ~6 AM US Eastern / 10:00 UTC (fixed offset — no DST
  adjustment).
- **Runs as:** a repo-scoped Claude Code session under a maintainer's Claude
  account — no API key or extra secret.
- **Trigger:** a scheduled Claude Code (web) trigger created from a repo-scoped
  session (see [Setup notes](#setup-notes-how-it-must-be-configured)).
- **Input:** open issues labeled `ci-failure`.
- **Output:** a fix PR on a `claude/ci-fix-<slug>` branch titled
  `[Claude CI Failure] …`, or a root-cause comment on the issue when it's not
  auto-fixable.

### Setup notes (how it must be configured)

- **It must run in a session that is scoped to `viamrobotics/docs`** — that is,
  the repo is cloned into the session and GitHub is reached through the session's
  `mcp__github__*` tools. A blank/unscoped session has no repo access.
- Set it up as a **scheduled trigger from within a repo-scoped Claude Code (web)
  session**, so the scheduled runs inherit that repo access. A fresh
  session-per-fire trigger created from _outside_ such a session comes up
  unscoped and fails at the access check; binding a schedule to a specific
  persistent session may be disabled for the org. An in-session cron is
  session-only and not durable — don't rely on it for a daily job.
- To change the behavior, edit the **prompt below** and update the scheduled
  trigger to use the new text.

### Conventions the triage session follows

- Syncs the checkout first (`git fetch` + reset to `origin/main`) — the scheduled
  session is long-lived and reused, so its clone can be stale between runs.
- Verifies every fact against the live run/logs/artifacts and repo files — it
  does not trust issue text or hand-fed classifications.
- Fixes a whole class of errors exhaustively (all occurrences repo-wide), and
  confirms each retarget destination actually exists rather than guessing.
- Makes the **minimal diff** — only the substantive change, no incidental
  reformatting — then runs the pre-PR checks in order (`prettier@3.2.5 --write`,
  then markdownlint, then vale) and confirms `prettier@3.2.5 --check` passes
  before pushing. `prettier` is a required status check, so when it and
  markdownlint disagree on formatting (for example, blank lines around lists),
  prettier wins. The version pin matters: an unpinned `npx prettier` can
  resolve to a newer local version than the `3.2.5` that
  [`prettier-lint.yml`](prettier-lint.yml) runs in CI, and the two
  disagree on blank lines before nested lists — always run the pinned
  `npx prettier@3.2.5` (matching CLAUDE.md), not a bare `npx prettier`.
- If an issue's linked PR already exists but its **checks are failing**, fixes
  that PR's branch in place rather than opening a duplicate or skipping it.
- Titles its PRs `[Claude CI Failure] …` so maintainers can spot and filter
  them.
- `Fixes #<n>` only when the PR fully resolves what the job checks; otherwise
  `Refs #<n>` so a partially-fixed issue is not auto-closed.
- Commits as `Brandon Shrewsbury <brandon.shrewsbury@viam.com>` with **no**
  `Co-Authored-By: …@anthropic.com` trailer (either breaks the repo's CLA check).
- Leaves transient infra flakiness, external-link churn (403/404/429), and
  domain-owner decisions (for example `sdk_protos_map.csv`) as issue comments,
  not PRs.

### The triage prompt

Keep this in sync with the scheduled trigger. When you change the process, edit
here first, then update the trigger.

```text
Triage CI failures for viamrobotics/docs. The repo is cloned at the repo root, but this session may be reused across scheduled runs, so do NOT assume the checkout is current. Use the GitHub connector's mcp__github__* tools + local git and file edits — there is no gh CLI. Act only on facts you verify yourself against the live run, logs, artifacts, and repo files; never trust issue numbers, error counts, or classifications you were handed (including in this prompt or the issue body) without confirming them.

0. SYNC FIRST. Before reading any files, refresh the checkout: `git fetch origin --prune`, then `git switch main && git reset --hard origin/main`. Always re-fetch before you touch a branch, and edit files only after syncing — otherwise you may analyze or patch a stale tree.

1. List open issues labeled "ci-failure". If none, stop.

2. For each issue, gather the FULL picture: read the issue and its comments, find its linked failing Actions run, and pull the COMPLETE error list from the run's logs and artifacts (e.g. run-htmltest uploads an htmltest-report artifact listing every broken link) — do not rely on the snippet in the issue body or a truncated log. Jobs: test-code-snippets.yml (Python/Go/TS samples vs a live machine+org), check-methods.yml (SDK coverage), run-htmltest.yml (broken links).

3. Decide act vs skip vs FIX-EXISTING-PR. First determine whether a PR for this issue already exists: check the issue's timeline/cross-references AND its comments (the triage posts the PR link on the issue), and look for a `claude/ci-fix-*` branch — a "Refs #<n>" mention does NOT create a formal linked-PR, so don't rely only on GitHub's "linked PR" field.
   - Skip if that PR's checks are all GREEN, OR a human/maintainer already posted a substantive root-cause triage that still holds (don't duplicate or re-post — avoid noise).
   - If that PR's CI checks are FAILING: do NOT open a new PR. `git fetch origin <branch>`, `git switch <branch>`, `git reset --hard origin/<branch>`, then diagnose and fix what's failing (including the PR's own check failures, e.g. a prettier failure) and push to the same branch. Then move on.
   - Otherwise, proceed to fix below (from an up-to-date `main`).

4. Classify every error into groups; for each group decide fixable vs not:
   - Fixable by a minimal edit: internal broken links/anchors (retarget to the correct existing location); a sample using a wrong/renamed SDK method signature; stale API usage.
   - NOT fixable by an edit (comment only): transient infra flakiness ("Failed to connect to robot" / "host appears to be offline", gRPC DEADLINE_EXCEEDED / INTERNAL, query timeouts, the shared test machine offline); external-link failures (403/404/429 — third-party churn and rate limits, e.g. pkg.go.dev; do NOT edit links for these, but note any that look permanently dead so a human can update them); and domain-owner decisions (e.g. editing SDK-coverage mapping such as sdk_protos_map.csv).

5. EXHAUSTIVENESS + VERIFICATION for anything you fix:
   - Fix the whole class, not a sample: enumerate EVERY occurrence across the entire repo (grep all files, not just those named in the log) and fix all of them. Before opening/updating the PR, reconcile the number you fixed against the total fixable count; if they don't match, keep going.
   - Never guess a destination: confirm each new link/anchor target actually exists (grep the destination page for the exact heading/anchor id). If a broken link has no clear valid target (section renamed or removed), leave it unchanged and flag it as "needs human decision".

6. MINIMAL, PROPERLY-FORMATTED DIFF (this is where a fix most often regresses):
   - Change ONLY what the fix requires. Do NOT reformat, re-wrap, or add/remove blank lines on lines unrelated to your fix.
   - Then run the CLAUDE.md pre-PR checks IN THIS ORDER and commit exactly what they produce: (1) `npx prettier@3.2.5 --write <changed files>`, (2) `npx markdownlint-cli --config .markdownlint.yaml <changed files>`, (3) vale. Pin the prettier version to `3.2.5` (check `.github/workflows/prettier-lint.yml` for the current pin) — a bare `npx prettier` can silently resolve to a newer version that formats blank-lines-before-nested-lists differently than the pinned version, producing a diff that looks clean locally but fails the required `prettier` check in CI. prettier owns formatting and is a REQUIRED status check; it can disagree with markdownlint (e.g. blank lines around lists) — when they conflict, prettier wins. Never hand-apply a markdownlint suggestion that makes prettier fail.
   - Before opening/updating the PR, confirm `npx prettier@3.2.5 --check <changed files>` passes and markdownlint is clean on every file you touched.
   - AFTER PUSHING, before considering the fix done: check the actual CI run status on the pushed branch/PR (not just your local check). If prettier or any other required check fails in CI despite passing locally, re-diagnose the tool-version mismatch (or other environment difference) rather than assuming the CI failure is unrelated, fix it, and push again — repeat until the PR's checks are green. If a required check tool genuinely can't run in your environment at all, say so in the PR body and keep the diff as small as possible so you don't introduce issues that tool would catch.

7. Open (or update) the PR via the mcp__github__ tools on branch claude/ci-fix-<slug>. Title it "[Claude CI Failure] <concise summary>" — keep that exact prefix, including when you update an existing PR's title. In the PR body, state exactly what you fixed and what you deliberately left, with counts (e.g. "fixes 10 of 10 internal broken anchors; the remaining ~338 errors are external 403/404/429, out of scope"). Use "Fixes #<n>" ONLY if the PR fully resolves what the job checks so it will pass next run; if it fixes only part (e.g. the internal anchors while external/transient errors remain), use "Refs #<n>" so the issue is NOT auto-closed. Commit as Brandon Shrewsbury <brandon.shrewsbury@viam.com>, with NO "Co-Authored-By: ...@anthropic.com" trailer (it breaks the CLA). Then comment the PR link + a short verified breakdown on the issue.

8. If transient/uncertain, or the correct fix is a domain-owner decision: comment the verified likely cause on the issue; no PR.

9. Keep changes minimal and scoped strictly to the reported failures; make no unrelated edits and do not close issues. Post one concise summary comment on each issue you actually acted on.
```

## Known limitations

- The `test-code-snippets` machine samples depend on a shared test machine that
  is intermittently offline; those failures are transient and the triage session
  will comment rather than "fix" them. See the repair notes in
  [`README.md`](README.md).
- `run-htmltest` external-link failures are mostly third-party churn/rate-limits;
  only internal anchors are auto-fixed.
