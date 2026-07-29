# CI repair plans

These documents are a working plan for repairing the broken and degraded
GitHub Actions jobs described in the [workflows reference](../README.md). They
are written so a future session (human or agent) can pick up any one plan and
execute it without re-deriving the context.

Each plan is self-contained and follows the same structure: problem, root
cause, prerequisites, step-by-step changes (with exact file and line
references), verification, rollback, and risks.

## Status legend

- `NOT STARTED`: no work done yet.
- `IN PROGRESS`: partially done; see the notes in the plan.
- `BLOCKED`: waiting on a prerequisite (named in the plan).
- `DONE`: merged and verified; the plan can be deleted.

## Plans and execution order

Run them in roughly this order. Plan 00 is a hard prerequisite for plan 02.

| # | Plan | Fixes | Status | Depends on |
| --- | --- | --- | --- | --- |
| 00 | [Provision a new org, machine, and secrets](00-provision-org-machine-secrets.md) | Foundation for the live-API jobs | NOT STARTED | — |
| 01 | [Restore failure notifications](01-restore-notifications.md) | Jira steps in the 3 scheduled jobs | NOT STARTED | — |
| 02 | [Fix Test Code Samples](02-fix-test-code-snippets.md) | `test-code-snippets.yml` | NOT STARTED | 00 |
| 03 | [Fix Alias reminder](03-fix-alias-reminder.md) | `alias-reminder.yml` | NOT STARTED | — |
| 04 | [Fix PR Test Label Manager](04-fix-pr-labeler.md) | `pr-labeler.yml` | NOT STARTED | — |
| 05 | [Fix SDK method coverage](05-fix-check-methods.md) | `check-methods.yml` | NOT STARTED | 01 |
| 06 | [Cleanup and modernization](06-cleanup-and-modernization.md) | All workflows (stale actions, dead steps) | NOT STARTED | — |

## Shared context

- The scheduled jobs `test-code-snippets.yml`, `check-methods.yml`, and
  `run-htmltest.yml` report failures only by opening a Jira ticket, and those
  Jira steps are themselves failing. Plan 01 restores that signal; do it early
  so the other jobs' results are actually seen.
- `test-code-snippets.yml` and the search-index jobs in `docs.yml` authenticate
  to a shared Viam test organization through repository secrets. Plan 00
  provisions a fresh org, machine, and API keys and re-points every secret and
  hardcoded ID. Plan 02 then makes the samples pass against it.
- Related work already in flight: PR #5106 makes the orgs sample select a
  roleless member; PR #5107 adds the workflows reference and the repair TODO.

## Repository secrets inventory

Names referenced by the workflows (values are not readable; this is the list to
re-point in plan 00):

| Secret | Used by | Tied to the test org? |
| --- | --- | --- |
| `TEST_ORG_ID` | test-code-snippets, docs (index sync) | Yes |
| `VIAM_API_KEY` / `VIAM_API_KEY_ID` | test-code-snippets, docs | Yes (org owner key) |
| `TEST_MACHINE_KEY` | test-code-snippets (config fetch) | Yes (machine part key) |
| `TEST_EMAIL` | test-code-snippets (invite target) | Yes (a user, not a member) |
| `VIAM_API_KEY_DATA_REGIONS` / `VIAM_API_KEY_ID_DATA_REGIONS` | test-code-snippets (data-regions sample) | Yes (a second org) |
| `JIRA_BASE_URL` / `JIRA_USER_EMAIL` / `JIRA_API_TOKEN` | test-code-snippets, check-methods, run-htmltest | No (Jira) |
| `TYPESENSE_TUTORIALS_API_KEY` / `TYPESENSE_API_KEY_R` | docs (index sync) | No (Typesense) |
| `INKEEP_API_KEY` | inkeep | No (Inkeep) |
| `PR_TOKEN` | pr-labeler, alias-reminder | No (GitHub PAT) |
