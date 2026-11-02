# Plan 02: Fix Test Code Samples

**Status:** NOT STARTED
**Fixes:** `test-code-snippets.yml` (the _Test Code Samples_ job).
**Depends on:** [Plan 00](00-provision-org-machine-secrets.md) (org, machine,
secrets) and benefits from [Plan 01](01-restore-notifications.md).

## Problem

The job runs every Python, Go, and TypeScript sample under
`static/include/examples/` against a live `viam-server` and a live Viam org. It
has failed on every run since 2025-11-10. The Python step exits non-zero on the
first failing file, which aborts the Go and TypeScript steps, so a single bad
sample hides the rest of the suite.

## Root causes

1. **Org data dependency**: `fleet-api/fleet-management-api-orgs.py` granted a
   location-owner role to `member_list[-1]`, who is now an org owner and already
   inherits that role, so the grant is rejected. PR #5106 changes the sample to
   pick a member with no existing authorizations, but the org must actually
   contain such a member (Plan 00, step 6).
2. **No step isolation**: the three language steps run sequentially in one job;
   the Python step's non-zero exit skips Go and TypeScript.
3. **Stale hardcoded IDs**: the server-start step and many samples hardcode the
   machine, location, and org IDs (Plan 00).
4. **Flaky live calls**: some samples fail intermittently on transient
   `INTERNAL` backend errors (observed in the `data-pipelines` teardown
   `delete_data_pipeline` calls), unrelated to docs changes.

## Plan

### A. Land the org-data prerequisites

1. Confirm [Plan 00](00-provision-org-machine-secrets.md) is complete: new org,
   machine, secrets, and a **roleless member**.
2. Merge or rebase PR #5106 so the orgs sample selects a roleless member and
   asserts clearly if none exists.

### B. Isolate the language steps

Today a Python failure blocks Go and TypeScript. Pick one:

- **Preferred**: split into three jobs (`test-python`, `test-go`, `test-ts`),
  each setting up its own runtime and running its own samples. Share the
  viam-server startup through a reusable setup (composite action or a setup
  job + artifact), or start the server in each job. This gives independent
  pass/fail per language and parallel execution.
- **Lighter**: keep one job but make each language loop record failures and
  continue, then fail the job once at the end with a combined summary, so all
  three languages always run.

### C. Re-point hardcoded IDs

Apply the ID replacements from [Plan 00](00-provision-org-machine-secrets.md).
Prefer reading machine identifiers from secrets in the workflow rather than
hardcoding. Confirm with:

```bash
grep -rE 'pg5q3j3h95|deb8782c|824b6570|1030f25a|5ec7266e|b5e9f350|16b8a3e5' \
  static/include/examples .github/workflows/test-code-snippets.yml
```

### D. Make teardown resilient to flaky backends

For samples whose **teardown** (not the demonstrated behavior) makes a live call
that can return a transient `INTERNAL` error, wrap the teardown so a flaky
response does not fail the run. Confirmed cases:

- `data-pipelines/pipeline-create.py` (`delete_data_pipeline` teardown).
- `data-pipelines/pipeline-list.py` (`delete_data_pipeline` teardown).

Pattern (teardown only, never the asserted behavior):

```python
try:
    await data_client.delete_data_pipeline(pipeline_id)
except GRPCError as e:
    print(f"teardown delete failed (ignored): {e}")
```

Do not blanket-wrap asserted calls; only teardown/cleanup that is incidental to
what the sample demonstrates.

### E. Audit machine-dependent samples

List the samples that connect to the machine and confirm the new machine
exposes the components they call, so they do not fail at connect or call time:

```bash
grep -rln 'MACHINE_ADDRESS\|auto-machine-main' static/include/examples
```

For each, note the component or service APIs it calls and ensure the Plan 00
machine config provides them.

### F. Quieten known anti-patterns (optional, low risk)

- Remove `pip install asyncio` (line ~61): `asyncio` is stdlib.
- Move Python off 3.9 (end of life approaching) and Node off the non-LTS 23.

## Verification

1. Trigger the workflow through `workflow_dispatch` on the branch.
2. Confirm all three language steps run (not just Python) and report a per-file
   pass/fail summary.
3. Confirm a fully green run end to end.
4. Re-run once to confirm previously flaky samples are now stable.

## Rollback

Each change is independent: the step-split, the ID re-point, and the teardown
guards can be reverted individually. Keep the single-job version in git history
so it can be restored if the split causes runner or secret-scoping issues.

## Risks and open questions

- Splitting jobs multiplies viam-server startups (and secret usage); confirm the
  machine tolerates concurrent connections, or gate the language jobs to run
  sequentially with `needs`.
- The "stable" viam-server AppImage is re-pulled each run, so a server release
  can change behavior with no repo change; consider pinning a known-good server
  version for reproducibility.
- Some failures may be genuine sample bugs surfaced once the suite runs fully;
  budget time to triage newly visible Go and TypeScript failures.
