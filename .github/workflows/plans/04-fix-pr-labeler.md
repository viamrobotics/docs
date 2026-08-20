# Plan 04: Fix PR Test Label Manager

**Status:** NOT STARTED
**Fixes:** `pr-labeler.yml` (the _PR Test Label Manager_ job).
**Depends on:** nothing (but step 1 is a discovery task).

## Problem

When a PR opens, the workflow adds a `safe to build` label if the author is a
`viamrobotics` org member, otherwise it posts a welcome comment. Two issues:

1. **No in-repo consumer of `safe to build`.** Nothing in `.github/` reads the
   label. It is almost certainly consumed by Netlify (deploy-preview gating for
   untrusted PRs), but that is unconfirmed. If nothing consumes it, the whole
   workflow is dead weight.
2. **Trigger/condition mismatch.** The workflow subscribes only to
   `types: [opened]`, but the job `if:` checks for
   `opened`/`synchronize`/`reopened`. The `synchronize` and `reopened` branches
   can never fire.
3. **Fragile error handling.** Any `checkMembershipForUser` error (rate limit,
   transient API failure), not just non-membership, falls into the `catch` and
   posts the contributor comment. A leftover `console.log("here")` remains.

## Plan

1. **Confirm the consumer first.** Check the Netlify site settings for this repo
   for a build condition or "deploy only when label present" rule referencing
   `safe to build`. Also check branch protection and any external automation.
   - If a consumer exists: document it in the [workflows reference](../README.md)
     and proceed to fix the workflow.
   - If no consumer exists: propose removing the workflow (record the decision
     in the reference) and stop here.
2. **Resolve the trigger/condition mismatch.** Decide the intended behavior:
   - If labeling should happen only on open: simplify the job `if:` to
     `github.event.action == 'opened'`.
   - If it should also re-check on updates: add `synchronize` and `reopened` to
     the `on: pull_request_target` types.
3. **Tighten error handling.** Distinguish "not a member" (the expected 404 path)
   from other API errors. Only post the contributor comment on a genuine
   non-membership result; let unexpected errors fail the step (or log and skip)
   rather than mislabeling a member as an outside contributor.
4. **Remove the leftover `console.log("here")` debug line.**

## Verification

1. Open a test PR as an org member and confirm the `safe to build` label is
   added and no welcome comment is posted.
2. Open or simulate a PR from a non-member and confirm the welcome comment is
   posted and the label is not added.
3. If a consumer was confirmed (step 1), verify the downstream build behaves as
   expected with and without the label.

## Rollback

Single-workflow change; revert the commit. The label itself is idempotent, so
reverting does not strand PRs.

## Risks and open questions

- `pull_request_target` runs with elevated permissions and `PR_TOKEN`; the
  script must not check out or execute PR code (it currently does not).
- The membership check requires the token to have org read scope; confirm
  `PR_TOKEN` still has it.
