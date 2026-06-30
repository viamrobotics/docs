# Plan 00: Provision a new org, machine, and secrets

**Status:** NOT STARTED
**Fixes:** the live-API foundation for `test-code-snippets.yml` and the
`docs.yml` search-index jobs.
**Depended on by:** [Plan 02](02-fix-test-code-snippets.md).

## Problem

The code-sample tests and the search-index sync run against a shared Viam test
organization whose identity lives in repository secrets and whose resource IDs
are hardcoded into both the workflow and the sample files. The current org has
drifted (no roleless member, possible stale machine/keys), and the secret
values are not recoverable. The cleanest reset is a fresh org, location,
machine, and key set, with every secret and hardcoded ID re-pointed in one
coordinated change.

## What the jobs actually need from the org

Collected from `test-code-snippets.yml` and the sample files:

1. An **organization** whose ID becomes `TEST_ORG_ID`.
2. An **org owner API key** (key + key ID) for `VIAM_API_KEY` /
   `VIAM_API_KEY_ID`. The samples authenticate with this and expect owner-level
   access (create/delete locations, keys, datasets, data pipelines, roles).
3. A **location** that replaces the hardcoded `pg5q3j3h95`. Samples reference it
   directly and through the machine address `auto-machine-main.<loc>.viam.cloud`.
4. A **machine** with a **main part**, used two ways:
   - The workflow fetches its config to run a local `viam-server`
     (`config?id=<machine-part-id>`), authenticated with a **machine part API
     key** (`key_id` + `TEST_MACHINE_KEY`).
   - Samples connect to it at the machine address above.
5. A **roleless member** in the org so the roles lifecycle sample can grant a
   fresh role (see [Plan 02](02-fix-test-code-snippets.md)).
6. A **user to invite** whose email becomes `TEST_EMAIL` (must not already be a
   member; the sample invites then deletes the invite).
7. A **second organization** (`ORG_ID_2`) used only by the share/unshare
   location sample.
8. A **second org + key for data regions** (`VIAM_API_KEY_DATA_REGIONS` /
   `VIAM_API_KEY_ID_DATA_REGIONS`) used by the data-regions sample.

## Hardcoded IDs to replace

These are baked into the workflow and sample files and must be updated to the
new resources. Counts are approximate occurrence counts across the repo.

| Current value | Meaning | Where | New value |
| --- | --- | --- | --- |
| `pg5q3j3h95` | Location ID | `test-code-snippets.yml`-adjacent samples; ~11 direct + 25 in machine address | new location ID |
| `deb8782c-7b48-4d35-812d-2caa94b61f77` | Machine **part** ID | workflow config fetch (`id=`); `MACHINE_PART_ID`/`PART_ID` in samples (~12) | new part ID |
| `824b6570-7b1d-4622-a19d-37c472dba467` | `VIAM_PART_ID` / `PART_ID` | workflow env line 49; samples (~8) | new part ID (confirm which part) |
| `1030f25a-f4f2-4872-9762-e33fa1e0444d` | Machine part **key ID** | workflow config-fetch header | new machine key ID |
| `5ec7266e-f762-4ea8-9c29-4dd592718b48` | Machine ID | samples (~3) | new machine ID |
| `b5e9f350-cbcf-4d2a-bbb1-a2e2fd6851e1` | `ORG_ID_2` (share target) | samples (~18) | new second org ID |
| `16b8a3e5-7944-4e1c-8ccd-935c1ba3be59` | resource ID (confirm: dataset/fragment) | samples (~6) | new ID |

> [!NOTE]
> There appear to be **two distinct part IDs** (`deb8782c...` and `824b6570...`).
> Confirm whether the machine has two parts, or whether one of these is stale,
> before re-pointing. The config fetch uses `deb8782c...`; the workflow env var
> `VIAM_PART_ID` uses `824b6570...`.

## Tooling

A future session can use the available skills:

- `local-viam-server`: create a machine and run a local `viam-server` (handles
  the machine part secret the CLI does not expose).
- `viam-modules-fleet`: `viam` CLI for orgs, locations, machines, API keys.
- `viam-machine-config`: push a machine config if the machine needs components.

The machine only needs to start and stay connected; the samples do not require
specific components on it unless a sample connects and calls a component API.
Audit the samples that use `MACHINE_ADDRESS` to confirm what the machine must
expose, and configure those components (see [Plan 02](02-fix-test-code-snippets.md)).

## Plan

1. **Create the primary test org.** Record its ID for `TEST_ORG_ID`. Give it a
   recognizable name; note that the orgs sample resets the name to
   `docs-scheduled-tests` on each run, so expect that name to reappear.
2. **Create a location** in that org. Record its ID (replaces `pg5q3j3h95`).
3. **Create a machine** in that location with a main part. Record the machine
   ID, the part ID, and confirm the machine address
   (`auto-machine-main.<location-id>.viam.cloud` or the actual address shown in
   the app).
4. **Create a machine part API key.** Record the key ID and key value for the
   workflow config fetch (`key_id` header and `TEST_MACHINE_KEY`).
5. **Create an org owner API key.** Record the key and key ID for `VIAM_API_KEY`
   / `VIAM_API_KEY_ID`.
6. **Add a roleless member** to the org (invite a service/test user and remove
   any default role, or confirm a member with no authorizations). This unblocks
   the roles lifecycle sample.
7. **Choose a `TEST_EMAIL`** for a user who is not a member of the org (the
   sample invites and then revokes this address).
8. **Create the second org** (`ORG_ID_2`) for the share/unshare sample. A bare
   org with no resources is enough.
9. **Create the data-regions org and key** for `VIAM_API_KEY_DATA_REGIONS` /
   `VIAM_API_KEY_ID_DATA_REGIONS`. Confirm what the data-regions sample requires
   (it changes an org region and tolerates the "region cannot be changed" error).
10. **Configure the machine** so every sample that connects to `MACHINE_ADDRESS`
    finds the components it calls (audit list in Plan 02). Start a
    `viam-server` once to confirm the config is valid and the machine reports
    online.
11. **Update the workflow** `test-code-snippets.yml`: replace the hardcoded
    `key_id` and config-fetch `id` (lines around 29) and `VIAM_PART_ID`
    (line ~49) with the new machine values. Prefer moving these into secrets or
    workflow `env` referencing secrets rather than re-hardcoding.
12. **Update the sample files** with the new location/machine/org IDs (see the
    table above). Use a scripted find-and-replace, then grep to confirm no old
    IDs remain.
13. **Update the GitHub repository secrets** (Settings -> Secrets and variables
    -> Actions): `TEST_ORG_ID`, `VIAM_API_KEY`, `VIAM_API_KEY_ID`,
    `TEST_MACHINE_KEY`, `TEST_EMAIL`, `VIAM_API_KEY_DATA_REGIONS`,
    `VIAM_API_KEY_ID_DATA_REGIONS`.

## Verification

- Run the workflow through `workflow_dispatch` on the branch and confirm the
  "Start viam-server in background" step fetches the config and the server
  reports running.
- Confirm `grep -rE 'pg5q3j3h95|deb8782c|824b6570|1030f25a|5ec7266e|b5e9f350|16b8a3e5' static/include/examples .github/workflows/test-code-snippets.yml`
  returns nothing.
- Proceed to [Plan 02](02-fix-test-code-snippets.md) to make the samples pass.

## Rollback

Keep the old secret values recorded until the new org is confirmed working. If
the new org misbehaves, restore the previous secret values and revert the ID
changes in one commit. The old org can stay untouched until the new one is
green.

## Risks and open questions

- **Two part IDs**: confirm the machine's part topology before re-pointing.
- **Component requirements**: some samples may call specific component APIs on
  the machine; the machine config must provide them or those samples fail at
  connect/call time even with a healthy server.
- **Data-regions org**: regions can only be set once per org, so the
  data-regions org may be a single-use resource; confirm the sample tolerates a
  pre-set region (it currently logs and continues on that error).
- **`ORG_ID_2` permissions**: the owner key for the primary org must be allowed
  to share a location into `ORG_ID_2`; confirm cross-org sharing is permitted.
