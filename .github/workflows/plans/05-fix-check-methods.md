# Plan 05: Fix SDK method coverage

**Status:** NOT STARTED
**Fixes:** `check-methods.yml` (the _SDK method coverage_ job).
**Depends on:** [Plan 01](01-restore-notifications.md) (Jira is its only signal).

## Problem

The job detects when the Viam SDKs gain or remove API methods that the docs'
generated reference has not accounted for. Three issues blunt its value:

1. **Job-level `continue-on-error: true`** means the coverage check never fails
   the run; its only signal is a Jira ticket, and Jira is currently broken
   (see Plan 01). Regressions are effectively silent.
2. **`concurrency.group` keys on `github.event.number`**, which is null for
   `schedule` and `workflow_dispatch`, so unrelated runs share one group with
   `cancel-in-progress: true` and can cancel each other.
3. **Fragile external scraping.** The check parses the HTML of four SDK doc
   sites (`python.viam.dev`, `pkg.go.dev`, `ts.viam.dev`, `flutter.viam.dev`)
   and the upstream gRPC protos; an upstream layout change breaks parsing and
   opens spurious tickets.
4. **Stale cron comment.** The comment says "weekdays" but the schedule
   `0 10 * * 3` is Wednesday only.

## Plan

1. **Restore the signal first** (Plan 01). Coverage results are worthless if no
   one is told.
2. **Decide on blocking.** Once Jira (or a backup alert) is reliable, decide
   whether a coverage gap should fail the run. If yes, remove
   `continue-on-error: true` so the run status reflects reality. If the check is
   too noisy to block, keep it non-blocking but ensure the alert is dependable.
3. **Fix the concurrency group.** Use a static group for scheduled runs, for
   example `group: check-methods-${{ github.ref }}` or drop
   `cancel-in-progress`, so a manual run and a scheduled run do not cancel each
   other.
4. **Correct the cron comment** to "Wednesdays 10:00 UTC".
5. **Harden the scrapers (optional, larger).** The parsers
   (`update_sdk_methods.py` plus `parse_*.py`) depend on exact external HTML.
   Options: add a clear "parsing failed" error distinct from "coverage gap" so
   an upstream layout change does not masquerade as a docs regression; or move
   toward an API/introspection-based source where available instead of HTML
   scraping.
6. **Trim inline deps.** The workflow installs `beautifulsoup4 markdownify
   argparse`; `argparse` is stdlib and can be dropped.

## Verification

1. Trigger through `workflow_dispatch` and confirm the coverage check runs and,
   on a seeded gap, both fails appropriately (if made blocking) and notifies.
2. Trigger a manual run while a scheduled run is in flight (or simulate) and
   confirm they no longer cancel each other.
3. Confirm the run distinguishes a scraping/parse failure from a real coverage
   gap.

## Rollback

The `continue-on-error` and concurrency changes are one-line reverts. The
scraper hardening, if attempted, should be a separate commit so it can be
reverted without losing the smaller fixes.

## Risks and open questions

- Making the check blocking will surface real, possibly large, coverage gaps
  that have accumulated while it was silent; budget triage time before flipping
  `continue-on-error`.
- The scrapers carry hand-maintained ignore-lists and resource-name remaps that
  drift as SDKs evolve; expect maintenance regardless of hardening.
