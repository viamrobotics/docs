# GitHub Actions workflows

This directory holds the CI/CD workflows for the Viam documentation site, plus
the Python helper scripts that some of them call. This document describes what
each workflow does, when it runs, whether it blocks a pull request, what
external services or secrets it depends on, and any known maintenance concerns.

For a one-line summary table, see the [Continuous integration section of the
top-level README](../../README.md#continuous-integration).

## How to read this

- **Trigger:** what causes the workflow to run.
- **Blocking:** whether a failure blocks a pull request from merging.
  "Informational" workflows set `continue-on-error: true` and never block.
  Scheduled workflows have no PR to block; they open a Jira ticket on failure
  instead.
- **Secrets:** repository secrets the workflow needs. Several scheduled jobs
  authenticate to a shared Viam test organization and to Jira.

> [!NOTE]
> Some scheduled jobs run code samples and SDK checks against a **live Viam
> organization** using the `TEST_ORG_ID`, `VIAM_API_KEY`, and related secrets.
> That org's data state (members, roles, locations, machines) directly affects
> whether those jobs pass. See [Test-org dependency](#test-org-dependency).

## Workflows by category

### Build and publish

#### `docs.yml`—_docs-publish_

- **Purpose:** Builds the production Hugo site and pushes search-index
  artifacts (tutorials and modular-resource models) into Typesense.
- **Trigger:** Push to `main`; manual (`workflow_dispatch`).
- **Blocking:** N/A (runs after merge to `main`).
- **What it does:** `build` job runs `make build-prod` with Hugo 0.152.2
  extended and uploads two Typesense JSON artifacts; `upsert-tutorials` and
  `upsert-modular-resources` jobs run `upload_tutorials.py` and
  `get_modular_resources.py` to sync those artifacts into the search cluster.
- **Tests:** None—build plus search-index sync only.
- **Secrets:** `TYPESENSE_TUTORIALS_API_KEY`, `TYPESENSE_API_KEY_R`,
  `VIAM_API_KEY`, `VIAM_API_KEY_ID`, `TEST_ORG_ID`.
- **Notes:** The `deploy` job is commented out, so this workflow does **not**
  deploy to GitHub Pages—production hosting is handled by Netlify (see the
  Netlify badge in the README). Action versions are old
  (`actions/checkout@v3`, `actions/configure-pages@v2`).

### Link checking

#### `run-htmltest-local.yml`—_run-htmltest_

- **Purpose:** Builds the site and checks **internal** links on every pull
  request.
- **Trigger:** `pull_request` (all PRs).
- **Blocking:** Yes (`continue-on-error: false`).
- **What it does:** `make build-dist-pr`, then `wjdp/htmltest-action` with
  `.htmltest-local.yml` (local links only).
- **Secrets:** None.
- **Notes:** The header comment is copy-pasted from `run-htmltest.yml` and is
  misleading. `wjdp/htmltest-action@master` is pinned to a moving branch.

#### `run-htmltest.yml`—_run-htmltest-external_

- **Purpose:** Weekly broken-link check that **includes external** links.
- **Trigger:** Schedule—`0 10 * * 2` (Tuesdays 10:00 UTC).
- **Blocking:** N/A (scheduled); opens a Jira `DOCS` bug on failure.
- **What it does:** Builds the site and runs `wjdp/htmltest-action` with
  `.htmltest.yml` (the external-links-inclusive config); uploads `htmltest.log`.
- **Secrets:** `JIRA_BASE_URL`, `JIRA_USER_EMAIL`, `JIRA_API_TOKEN`.
- **Notes:** Same moving-branch pin on `wjdp/htmltest-action@master`. External
  link failures are expected to be noisy (third-party sites change/expire).

### Linting and prose style (pull requests)

#### `vale-lint.yml`—_vale-lint_

- **Purpose:** Runs the Vale prose style linter and reports violations as
  GitHub checks through reviewdog.
- **Trigger:** `pull_request` (`opened`, `synchronize`).
- **Blocking:** **Yes**—`fail_on_error: true`, `level: error`. This is the
  prose-style gate referenced in `CLAUDE.md`.
- **Secrets:** `GITHUB_TOKEN` (automatic).
- **Notes:** The Python 3.8 / venv setup steps are dead weight—Vale is a Go
  binary and the venv is never used. Python 3.8 is end-of-life. The action is
  pinned to the `reviewdog` branch rather than a version.

#### `codespell.yml`—_codespell_

- **Purpose:** Spell-checks `docs/` for common misspellings.
- **Trigger:** `pull_request` (`opened`, `synchronize`).
- **Blocking:** Yes (action fails on misspellings).
- **Secrets:** None. Relies on `.codespellignore` in the repo root.

#### `markdown-lint.yml`—_Lint Markdown files_

- **Purpose:** Lints Markdown structure in `docs/` against `.markdownlint.yaml`.
- **Trigger:** `pull_request`; manual.
- **Blocking:** Informational (`continue-on-error: true`).
- **Secrets:** None.
- **Notes:** Uses the unmaintained `ruzickap/action-my-markdown-linter@v1` and
  `actions/checkout@v2` (deprecated).

#### `prettier-lint.yml`—_Lint JS files with Prettier_

- **Purpose:** Runs Prettier in check mode over changed `docs/**/*.md` files.
- **Trigger:** `pull_request`; push to `main`.
- **Blocking:** Informational (`continue-on-error: true`).
- **Secrets:** None.
- **Notes:** The workflow name says "JS files" but it checks Markdown. Prettier
  is pinned to `3.2.5`, which can drift from the repo devDependency and cause
  CI/local mismatches.

#### `python-lint.yml`—_Lint Python Code Snippets_

- **Purpose:** Lints Python code blocks embedded in `docs/**/*.md` with
  `flake8-markdown`.
- **Trigger:** `pull_request`; manual.
- **Blocking:** Informational (`continue-on-error: true`).
- **Secrets:** None.
- **Notes:** Same dead Python-3.8/venv boilerplate as `vale-lint.yml`
  (`source env/bin/activate` runs in its own shell and has no effect).

### Scheduled validation against the SDKs and live services

#### `test-code-snippets.yml`—_Test Code Samples_

- **Purpose:** Runs every Python, Go, and TypeScript example under
  `static/include/examples/` against a live `viam-server` and a live Viam org
  to verify the documented SDK samples still execute without error.
- **Trigger:** Schedule—`0 9 * * 1` (Mondays 09:00 UTC); push to `main`
  touching `static/include/examples/**` or this workflow; manual.
- **Blocking:** N/A (scheduled/push); opens a Jira `DOCS` bug on failure.
- **What it does:** Fetches a machine config from `app.viam.com`, starts the
  stable `viam-server` AppImage in the background, then runs each `*.py`,
  `*.go`, and `*.ts` sample in turn, tallying pass/fail.
- **Tests:** Yes—end-to-end execution of the real samples against live APIs.
- **Secrets:** `TEST_MACHINE_KEY`, `VIAM_API_KEY`, `VIAM_API_KEY_ID`,
  `TEST_ORG_ID`, `VIAM_API_KEY_DATA_REGIONS`, `VIAM_API_KEY_ID_DATA_REGIONS`,
  `TEST_EMAIL`, plus the Jira secrets.
- **Notes / current status:** Language steps run sequentially in one job, so a
  failure in the Python step aborts the Go and TypeScript steps. This job has
  been failing on every run since 2025-11-10, driven by
  `fleet-api/fleet-management-api-orgs.py` depending on the test org having a
  member with no existing roles. See [Test-org dependency](#test-org-dependency).
  The `viam-server` AppImage is re-pulled as "stable" each run, so a server
  release can change the test surface with no repo change. A literal machine
  `id`/`key_id` is hardcoded in the server-start step; if that machine or key
  is deleted the whole job fails at startup.

#### `check-methods.yml`—_SDK method coverage_

- **Purpose:** Detects when the Viam SDKs gain or remove API methods that the
  docs' generated API reference has not accounted for.
- **Trigger:** Schedule—`0 10 * * 3` (Wednesdays 10:00 UTC); manual.
- **Blocking:** N/A—job-level `continue-on-error: true`; opens a Jira `DOCS`
  task on failure (its only real signal).
- **What it does:** `make coveragetest` runs `update_sdk_methods.py --coverage`,
  which scrapes the four SDK doc sites and the upstream gRPC protos and diffs
  them against `sdk_protos_map.csv`; unmapped or missing methods fail the check.
- **Tests:** Documentation-coverage validation (no live robot calls).
- **Secrets:** Jira only.
- **Notes:** The cron comment says "weekdays" but the schedule is Wednesday
  only. Because it scrapes external doc-site HTML, upstream layout changes can
  break parsing and open spurious tickets. The `concurrency.group` references a
  PR number that is null for scheduled runs, so unrelated runs share one group.

### Pull-request automation

#### `pr-labeler.yml`—_PR Test Label Manager_

- **Purpose:** When a PR opens, adds the `safe to build` label if the author is
  a `viamrobotics` org member; otherwise posts a welcome comment.
- **Trigger:** `pull_request_target` (`opened`).
- **Blocking:** No.
- **Secrets:** `PR_TOKEN`.
- **Notes:** The job condition checks for `synchronize`/`reopened`, but the
  trigger only subscribes to `opened`, so those branches never fire. Any
  membership-check API error (not just non-membership) falls through to the
  contributor-comment path. Uses `actions/github-script@v6`.

#### `alias-reminder.yml`—_Alias reminder_

- **Purpose:** On PRs, detects renamed/moved `.md` files and posts a sticky
  comment reminding the author to add redirect aliases.
- **Trigger:** `pull_request_target` (`labeled`, `synchronize`).
- **Blocking:** No.
- **Secrets:** `PR_TOKEN`.
- **Notes:** The detection step uses the deprecated `::set-output` workflow
  command, which GitHub has disabled, so the output is not populated and the
  comment step's gate never fires—the reminder is effectively dead and should
  be migrated to `$GITHUB_OUTPUT`.

#### `inkeep.yml`—_Inkeep Source Sync_

- **Purpose:** On pushes to `main` that touch `docs/`, triggers Inkeep to
  re-sync the docs source for AI search/chat.
- **Trigger:** Push to `main`, paths `docs/**`.
- **Blocking:** N/A.
- **Secrets:** `INKEEP_API_KEY` (plus `GITHUB_TOKEN`).
- **Notes:** Has both a top-level `paths` filter and a redundant in-job
  `dorny/paths-filter` check. Hardcoded Inkeep `sourceId`.

## Helper scripts

These Python files are invoked by the workflows above, not run on their own:

- **`update_sdk_methods.py`** (+ `parse_python.py`, `parse_go.py`,
  `parse_typescript.py`, `parse_flutter.py`, `parser_utils.py`)—the engine for
  the docs' autogenerated SDK API reference. It maps every Viam component,
  service, app, and robot API to its upstream `*_grpc.pb.go` definition and
  scrapes each SDK's doc site to generate the `static/include/.../generated/`
  include files. In `--coverage` mode it instead reports method gaps
  (used by `check-methods.yml`). `sdk_protos_map.csv` is the hand-maintained
  proto-to-method mapping it reads.
- **`get_modular_resources.py`**—reads the modular-resources Typesense
  artifact and the Viam app registry and upserts models into the search
  cluster (used by `docs.yml`).
- **`upload_tutorials.py`**—upserts the tutorials Typesense artifact into the
  search cluster (used by `docs.yml`).
- **`requirements.txt`**—Python dependencies for the `docs.yml` index-sync
  jobs (`viam-sdk`, `asyncio`, `typesense`).

## Test-org dependency

`test-code-snippets.yml` (and the index-sync jobs in `docs.yml`) authenticate
to a shared Viam test organization identified by the `TEST_ORG_ID` secret. The
samples create, modify, and delete real resources (locations, API keys, roles,
datasets, data pipelines) in that org, and some assert on its existing state.

Practical consequences:

- The org's display name is reset to `docs-scheduled-tests` on each run of the
  orgs sample, and the samples reference a hardcoded location ID
  (`pg5q3j3h95`). The org that owns that location is the test org.
- `fleet-api/fleet-management-api-orgs.py` requires the org to have at least one
  member with **no existing authorizations**, so a fresh location-owner role can
  be added to them. If every member is already an owner, the sample fails.
- Several samples make live API calls that can return transient `INTERNAL`
  errors; these can cause intermittent (flaky) failures unrelated to docs
  changes.

Because the secret values are not readable, identify the live org through these
fingerprints (location `pg5q3j3h95`, org name `docs-scheduled-tests`) rather
than from the secret itself.

## Recurring maintenance themes

- **Action versions are old across the board**—`actions/checkout@v2`/`v3`,
  `setup-python@v4`, `github-script@v6`, and two `wjdp/htmltest-action@master`
  (moving-branch) pins. Bumping these is a safe, batchable cleanup.
- **Two PR-automation workflows have dead logic**—`alias-reminder.yml`
  (`::set-output`) and `pr-labeler.yml` (event/condition mismatch).
- **Reliance on external HTML scraping and live services** makes the scheduled
  jobs fragile; failures there are often environmental, not docs regressions.
- **End-of-life Python 3.8** appears in `vale-lint.yml` and `python-lint.yml`
  (in unused venv steps).

## TODO: repairs

Work items to get the broken and degraded jobs back to a healthy, monitored
state. Roughly ordered by impact.

### Restore failure visibility (highest impact)

Three scheduled jobs (`test-code-snippets.yml`, `check-methods.yml`,
`run-htmltest.yml`) report failures only by opening a Jira ticket, and the Jira
steps are themselves failing—so these jobs currently run unmonitored.

- [ ] Fix the `atlassian/gajira-login` / `gajira-create` steps (refresh
      `JIRA_BASE_URL` / `JIRA_USER_EMAIL` / `JIRA_API_TOKEN`, confirm the `DOCS`
      project still accepts the issue types used).
- [ ] Confirm the `DOCS` Jira project is actively watched; if not, add a second
      notification path (for example a Slack or email alert on failure).

### `test-code-snippets.yml` (Test Code Samples)

- [ ] Add a member with no roles to the `docs-scheduled-tests` test org so
      `fleet-api/fleet-management-api-orgs.py` can grant a fresh location-owner
      role. (Sample-side change tracked in #5106.)
- [ ] Re-run the job and confirm it goes green end to end (the Python failure
      currently blocks the Go and TypeScript steps).
- [ ] Split the Python, Go, and TypeScript runs into separate jobs (or add
      `continue-on-error` per language with a final gate) so one language
      failing no longer hides the others.
- [ ] Replace the hardcoded machine `id` / `key_id` in the server-start step
      with secrets so a rotated machine or key does not break startup.
- [ ] Add resilience to samples that make live calls returning transient
      `INTERNAL` errors (the `data-pipelines` teardown deletes), so flaky
      backend responses do not fail the run.

### `alias-reminder.yml` (Alias reminder)

- [ ] Migrate the moved-files detection from the disabled `::set-output`
      command to `$GITHUB_OUTPUT` so the reminder comment posts again.
- [ ] Verify the reminder fires on a test PR that renames a `.md` file.

### `pr-labeler.yml` (PR Test Label Manager)

- [ ] Confirm what consumes the `safe to build` label (likely Netlify
      deploy-preview gating); document the consumer or remove the workflow if
      nothing uses it.
- [ ] Resolve the trigger/condition mismatch: either subscribe to
      `synchronize` and `reopened`, or drop them from the job `if`.
- [ ] Stop the membership-check error path from posting the contributor comment
      on API errors (rate limits), and remove the leftover `console.log` debug.

### `check-methods.yml` (SDK method coverage)

- [ ] Decide whether coverage gaps should fail the run; if so, remove the
      job-level `continue-on-error: true` once the Jira signal is reliable.
- [ ] Fix the `concurrency.group` so scheduled and manual runs do not cancel
      each other (it currently keys on a null PR number).
- [ ] Correct the cron comment ("weekdays" → Wednesday only).

### Cleanup (batchable, low risk)

- [ ] Bump stale action versions: `actions/checkout@v2`/`v3`,
      `actions/setup-python@v4`, `actions/github-script@v6`,
      `actions/configure-pages@v2`.
- [ ] Pin `wjdp/htmltest-action@master` to a released version or commit SHA in
      both htmltest workflows.
- [ ] Remove the unused Python 3.8 venv steps from `vale-lint.yml` and
      `python-lint.yml`; move `python-lint` off end-of-life Python.
- [ ] Delete the commented-out `deploy` job from `docs.yml` (Netlify handles
      deployment).
- [ ] Decide whether `markdown-lint.yml`, `prettier-lint.yml`, and
      `python-lint.yml` should block PRs or be removed; as informational-only
      jobs they duplicate the local pre-commit checks and never gate a merge.
- [ ] Fix the misleading `name`/header comments (`prettier-lint.yml` says "JS
      files"; the htmltest headers are copy-pasted).
