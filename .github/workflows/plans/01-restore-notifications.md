# Plan 01: Restore failure notifications

**Status:** NOT STARTED
**Fixes:** the Jira notification steps in `test-code-snippets.yml`,
`check-methods.yml`, and `run-htmltest.yml`.
**Depended on by:** [Plan 05](05-fix-check-methods.md) (its only signal is Jira).

## Problem

Three scheduled jobs report failures only by opening a Jira ticket, and the
Jira steps are themselves failing (the `Login to Jira` / `Create Jira ticket`
steps show as failed in recent runs). The result: these jobs run unmonitored,
so even a real regression is silent. This is the highest-impact repair because
it is the prerequisite for trusting every other scheduled job.

## Root cause (to confirm)

The `atlassian/gajira-login@v3` step authenticates with `JIRA_BASE_URL`,
`JIRA_USER_EMAIL`, and `JIRA_API_TOKEN`. The most likely causes, in order:

1. An expired or rotated `JIRA_API_TOKEN`.
2. A changed `JIRA_BASE_URL` or account email.
3. The `DOCS` project no longer accepting the issue types used
   (`Bug` for the htmltest and code-sample jobs, `Task` for check-methods), or
   a required field now being enforced on create.

## Plan

1. **Reproduce** by triggering one scheduled workflow through
   `workflow_dispatch` and reading the `Login to Jira` step log for the exact
   error (auth failure, project not found, required field, and so on).
2. **Refresh credentials**: regenerate the Jira API token, confirm the account
   email and base URL, and update the three secrets.
3. **Confirm the create payload**: verify the `DOCS` project key, the issue
   types (`Bug` / `Task`), and any newly required fields. Update the
   `gajira-create` step inputs if the project schema changed.
4. **Add a backup notification path** so a single broken integration cannot
   silence the jobs again. Options, cheapest first:
   - A Slack incoming-webhook step on `failure()` posting the run URL.
   - A GitHub issue created on failure with a dedup label.
   - Email through an action on `failure()`.
5. **Make notification failures visible**: ensure the Jira/Slack steps run with
   `if: failure()` (they do today) and that a failure of the notification step
   itself surfaces in the run status rather than passing silently.

## Verification

- Trigger each of the three scheduled jobs through `workflow_dispatch` while
  forcing a failure (or run against a known-failing state) and confirm a ticket
  is created and the backup alert fires.
- Confirm the created ticket lands in the expected `DOCS` project with the
  correct issue type and a useful title and body (include the run URL).

## Rollback

The notification steps are isolated from the test logic, so reverting the
`gajira-*` step changes or removing the backup step does not affect what the
jobs test. Keep the previous step config in the PR description for quick revert.

## Risks and open questions

- Is the `DOCS` Jira project still the right destination, and who owns the
  service account behind `JIRA_USER_EMAIL`?
- If Jira is being retired for this purpose, replace it with the backup path as
  the primary, rather than fixing the login.
