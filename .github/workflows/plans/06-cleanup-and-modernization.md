# Plan 06: Cleanup and modernization

**Status:** NOT STARTED
**Fixes:** stale and dead configuration across all workflows.
**Depends on:** nothing; safe to batch independently.

## Problem

Several non-functional issues accumulate maintenance debt and confuse readers:
old action versions, moving-branch pins, dead setup steps, a commented-out job,
and misleading names. None blocks today, but they make the workflows fragile and
hard to trust.

## Plan

Each item is independent; land them as small, reviewable commits.

### Action version bumps

- [ ] `actions/checkout`: bump `v2` (`markdown-lint.yml`, `python-lint.yml`) and
      `v3` (most others) to the current major.
- [ ] `actions/setup-python@v4` to current.
- [ ] `actions/github-script@v6` (`pr-labeler.yml`) to current.
- [ ] `actions/configure-pages@v2` (`docs.yml`) to current.

### Pin moving references

- [ ] `wjdp/htmltest-action@master` in `run-htmltest.yml` and
      `run-htmltest-local.yml`: pin to a released tag or commit SHA for
      reproducibility and supply-chain safety.
- [ ] `errata-ai/vale-action@reviewdog` (`vale-lint.yml`): pin to a version or
      SHA instead of a branch.

### Remove dead steps and jobs

- [ ] Delete the unused Python 3.8 venv steps in `vale-lint.yml` (Vale is a Go
      binary; the venv is never used) and in `python-lint.yml` (the
      `source env/bin/activate` runs in its own shell and has no effect).
- [ ] Move `python-lint.yml` off end-of-life Python 3.8.
- [ ] Delete the commented-out `deploy` job in `docs.yml` (Netlify handles
      deployment; the Pages permissions and Setup Pages step are then unused).
- [ ] Remove `pip install asyncio` from `test-code-snippets.yml` (stdlib).

### Fix misleading names and comments

- [ ] `prettier-lint.yml` `name:` says "Lint JS files" but it checks Markdown.
- [ ] Copy-pasted header comments in `run-htmltest-local.yml` (says
      `run-htmltest.yml` and `dist/`).
- [ ] The "Don't fail the build on broken links" comments contradict
      `continue-on-error: false` in both htmltest workflows.

### Decide on the informational linters

- [ ] `markdown-lint.yml`, `prettier-lint.yml`, `python-lint.yml` all set
      `continue-on-error: true`, so they never block and duplicate the local
      pre-commit checks. Decide per workflow: make it blocking (give it teeth)
      or remove it (reduce noise). Record the decision in the
      [workflows reference](../README.md).

### Redundant gating

- [ ] `inkeep.yml` has both a top-level `paths` filter and an in-job
      `dorny/paths-filter` check; remove the redundant inner check.

## Verification

- Open a PR with the batched changes and confirm all PR-triggered checks still
  run and pass.
- For scheduled-only workflows, trigger each through `workflow_dispatch` and
  confirm the bumped actions and new pins resolve and run.

## Rollback

Each item is a small isolated commit; revert individually. Action-version bumps
are the only ones with behavior risk; if a bumped action changes inputs, pin to
the last working version and note it.

## Risks and open questions

- Bumped actions occasionally change input names or defaults; read each action's
  changelog for the major bump.
- Making the informational linters blocking may surface a backlog of existing
  violations; fix or baseline them before flipping.
