<!-- vale off -->
<!-- This is internal tooling documentation for the daily docs change agent,
     copied from the agent's working repo. It is not user-facing docs content,
     so Viam prose style rules do not apply. -->

# Playbook: Processing Daily Code Changes

Detect code changes across all source repos, classify their docs impact, update affected docs pages, and file PRs grouped by semantic coherence.

This playbook is designed for a scheduled cloud agent running daily. It reads its own prior output on each run and records what it learns for future runs.

---

## Repos

The agent clones and diffs these repos on every run:

| Repo                            | Branch | What it covers                                                                                                                                                                                                                                                                                                                                                                                                                      |
| ------------------------------- | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `viamrobotics/rdk`              | `main` | Go SDK, CLI, config structs, behavioral flows, component/service models                                                                                                                                                                                                                                                                                                                                                             |
| `viamrobotics/api`              | `main` | Proto definitions (source of truth for API surface)                                                                                                                                                                                                                                                                                                                                                                                 |
| `viamrobotics/app`              | `main` | App backend, `app/ui/src/`, `app/test-cards/src/`, feature flags                                                                                                                                                                                                                                                                                                                                                                    |
| `viamrobotics/viam-python-sdk`  | `main` | Python SDK                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `viamrobotics/viam-cpp-sdk`     | `main` | C++ SDK                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `viam-labs/motion-tools`        | `main` | 3D scene tab UI (`src/`), `draw` library, `client/api` push API, snapshot format. Once docs PR #5099 merges, the Visualization section documents all four surfaces — treat `draw/` and `client/api/` signature changes as docs-affecting (see the 2026-07-02 snapshot-API drift, caught only by manual review). Note: this repo had no baseline row in `maintenance.md` until 2026-07-21, so earlier runs never actually diffed it. |
| `shannonbradshaw/viam-code-map` | `main` | Xref mappings, playbooks, flows, inventory, agent state files                                                                                                                                                                                                                                                                                                                                                                       |
| `viamrobotics/docs`             | `main` | Docs site (target for PRs)                                                                                                                                                                                                                                                                                                                                                                                                          |

All docs PRs target the `main` branch on `viamrobotics/docs`.

---

## Agent state files

The agent reads these files from the code-map repo at the start of every run and writes updates at the end.

| File                   | Purpose                                               | Agent reads        | Agent writes                                 |
| ---------------------- | ----------------------------------------------------- | ------------------ | -------------------------------------------- |
| `maintenance.md`       | Last-checked commit SHAs per repo, verification dates | Every run          | Updates after each run                       |
| `backlog.yaml`         | Findings awaiting PR creation (exceeded per-run cap)  | Every run          | Merges new findings, removes processed items |
| `search-patterns.yaml` | Non-obvious symbol-to-docs-text mappings              | Every run          | Adds new patterns discovered                 |
| `missed-findings.md`   | Human-reported false negatives                        | Every run          | Marks entries as processed                   |
| `false-positives.md`   | Human-reported false positives                        | Every run          | Marks entries as processed                   |
| `exclusions.yaml`      | Paths and patterns to skip                            | Every run          | Proposes additions                           |
| `run-history.yaml`     | Per-run metrics                                       | For trend analysis | Appends each run                             |
| `coverage-gaps.md`     | Known docs gaps                                       | Every run          | Updates                                      |
| `playbook-feedback.md` | Proposed playbook refinements                         | Every run          | Adds new proposals                           |
| Xref files             | Code-to-docs mappings                                 | Every run          | Adds new mappings discovered                 |

---

## Phase 1: Initialize

### Step 1: Read agent state

Read all agent state files from the code-map repo:

1. Read `maintenance.md` to get the last-checked commit SHA for each repo.
2. Read `search-patterns.yaml` to load non-obvious search term mappings.
3. Read `missed-findings.md` for unprocessed human-reported false negatives. Extract any new search patterns or classification rules. Mark processed entries.
4. Read `false-positives.md` for unprocessed human-reported false positives. Extract any new exclusion rules or classification refinements. Mark processed entries.
5. Read `exclusions.yaml` to load paths and patterns to skip.
6. Read `playbook-feedback.md` for accepted playbook refinements (entries marked `status: accepted`). Apply them to classification logic for this run.

### Step 2: Collect diffs

For each repo, diff from the last-checked commit SHA to HEAD:

```
git -C <repo> log --oneline <last_sha>..HEAD
git -C <repo> diff --name-only <last_sha>..HEAD
```

Record the list of changed files per repo. Record the list of commits per repo (these will be used for PR grouping in Phase 5).

If a repo has no changes since the last-checked SHA, skip it entirely.

### Step 2b: Fetch PR metadata

For each commit in the change set, fetch the associated pull request description and comments from GitHub. These contain critical context that the code diff alone does not: the author's intent, known limitations, follow-up work planned, and behavioral explanations.

For each repo with changes:

```
gh pr list -R <owner>/<repo> --state merged --search "<commit_sha>" --json number,title,body,comments
```

Or for each commit, find its merged PR:

```
gh log --oneline <last_sha>..HEAD  # get commit SHAs
gh pr list -R <owner>/<repo> --search "<sha>" --state merged --json number,title,body,comments,reviews
```

If `gh` is available, use it. If not, use `git log --format="%H %s"` and the GitHub API via curl.

**What to extract from PR metadata:**

- **PR description:** What the author says the change does and why. This often names specific flags, behaviors, or config fields that changed — use these as search terms in Phase 3.
- **PR comments and review comments:** May contain corrections to the description, caveats, or discussion of docs impact. Look for phrases like "docs", "documentation", "breaking", "deprecate", "follow-up", "not yet", "will come in a separate PR".
- **Linked issues:** Jira tickets or GitHub issues referenced in the PR. These may describe the user-facing motivation.
- **Scope limitations:** Authors often note what is NOT included in a PR ("full support will come in a follow-up"). Do not document incomplete features as complete.

Record the PR metadata alongside the diffs. Use it in Phase 2 classification to:

1. Confirm or supplement what you learn from the diff
2. Identify changes the diff makes hard to see (behavioral intent, scope limitations)
3. Pick up search terms the author uses that might differ from symbol names

### Step 3: Filter irrelevant files

Remove files that cannot affect docs. Apply the exclusions from `exclusions.yaml` plus these baseline rules:

**Always exclude:**

- `**/*_test.go`
- `**/*.test.ts`, `**/*.test.js`, `**/*.spec.ts`, `**/*.spec.js`
- `**/*_test.py`, `**/test_*.py`, `**/tests/**`
- `**/testutils/**`, `**/testdata/**`, `**/fixtures/**`
- `**/.github/**`, `**/.circleci/**`, `**/.gitlab-ci*`
- `**/vendor/**`, `**/node_modules/**`
- `**/*.sum`, `**/package-lock.json`, `**/yarn.lock`
- `**/*.md` in source repos (internal docs, READMEs, changelogs within the source repo)
- `**/*.pb.go`, `**/*.pb.gw.go` (generated from protos — check the `.proto` source instead)

**Never exclude** (even if matched by a broader pattern):

- `**/proto/**/*.proto`
- `**/config/*.go`, `**/config.go`
- `**/cli/*.go`
- `**/app/ui/src/**`
- `**/app/test-cards/src/**`
- Any path explicitly listed in the xref files, `flows.md`, or `maintenance.md`

After filtering, the remaining files are the **change set** for this run.

---

## Phase 2: Read and classify every diff

For every file in the change set, read the full diff AND the associated PR metadata (description, comments, reviews) collected in Step 2b. Classify every change using the 14 cases below. A single diff can produce findings in multiple cases.

**Use PR metadata to:**

- Understand the author's intent when the diff is ambiguous
- Identify scope limitations ("this PR does X but not Y, follow-up coming")
- Find search terms the author uses that differ from code symbol names
- Detect caveats or known issues noted in review comments
- Determine whether a feature is complete or partial (do not document partial features as complete)

### Case 1: API surface change

**Trigger:** Changed files in `api/proto/viam/`. Also triggered by proto-generated types appearing in SDK diffs.

**What to look for in the diff:**

- New RPC methods added to an existing service
- Removed or renamed RPC methods
- Changed request or response message fields (added, removed, renamed, type changed)
- Changed field numbers (wire-breaking)
- New or changed enum values
- New proto service definitions
- Changes to `common.proto` shared types (`Pose`, `Vector3`, `GeoPoint`, `GeoGeometry`, `ResourceName`, `Geometry`, etc.) — these ripple across every RPC that uses them

**Shared type ripple effect:** When a type defined in `common.proto` or any shared message changes, identify every RPC that uses that type in its request or response. Every one of those RPCs' docs pages is potentially affected.

**Classification output:** For each changed RPC or message, record:

- The proto file and service name
- The specific method or message that changed
- Whether the change is additive (new field/method), breaking (removed/renamed), or modification (changed type/default)
- The deprecation status if applicable

### Case 2: Config field change

**Trigger:** Changed files matching `rdk/config/*.go`, `rdk/resource/config.go`, or any file containing a config struct for a component or service (`rdk/components/*/`, `rdk/services/*/`).

**What to look for in the diff:**

- New struct fields or removed struct fields
- Changed JSON struct tags (field rename from docs perspective)
- Changed field types
- Changed default values — check ALL of these locations:
  - Struct field tags
  - `Validate()` method
  - Constructor functions (often `New*()` or `init()`)
  - `ProcessConfig()` in `rdk/config/config.go`
  - Package-level `var` or `const` declarations
- Changed required/optional status (field added to `Validate()` error checks, or removed from them)
- Changed validation rules (new constraints, relaxed constraints, changed allowed values)

**Classification output:** For each changed config field, record:

- The Go file and struct name
- The JSON field name
- What changed (new field, removed field, changed default, changed type, changed validation)
- The old and new values where applicable

### Case 3: CLI change

**Trigger:** Changed files in `rdk/cli/`.

**What to look for in the diff:**

- New commands or subcommands registered
- Removed commands
- New flags added to existing commands
- Removed or renamed flags
- Changed flag defaults
- Changed flag types
- New or changed aliases
- Changed usage text or help descriptions
- Changed output format (what the command prints)

**Classification output:** For each changed command or flag, record:

- The command path (e.g., `viam data export tabular`)
- The specific flag or attribute that changed
- The old and new values where applicable

### Case 4: New capability without docs

**Trigger:** Any of these appearing in the diff:

- New directory under `rdk/components/` or `rdk/services/`
- New `.proto` file under `api/proto/viam/`
- New model registration (grep for `resource.Register` or model registration patterns in new files)
- New route directory under `app/ui/src/routes/`
- New domain directory under `app/domains/`
- New public class or module in Python SDK or C++ SDK
- New CLI top-level command

**What to look for in the diff:**

- Is this a real user-facing capability or internal infrastructure?
- Does it have only a `fake` model (API exists but no real implementation)?
- What user access paths exist (UI, CLI, SDK, API)?

**Classification output:** For each new capability, record:

- What it is and where it lives
- Whether it has real implementations or only fake/test
- What user access paths exist
- What documentation it would need (API reference, config reference, how-to, conceptual)

For this case, the agent writes a new docs page following **Playbook 2** (Writing a New Docs Page) and **Playbook Diataxis** for page type classification. The agent gathers code references, reads the actual code, determines page type and location, checks vocabulary, and writes the page. The result is a PR with the agent's best attempt at a complete, accurate docs page.

### Case 5: Changed system behavior

**Trigger:** Changed files in paths listed in `maintenance.md`'s staleness detection table, or in any path referenced by `flows.md`.

Key paths:

- `rdk/data/`, `rdk/services/datamanager/` — data capture and sync behavior
- `rdk/module/modmanager/` — module lifecycle behavior
- `rdk/motionplan/`, `rdk/services/motion/` — motion planning behavior
- `rdk/robot/impl/`, `rdk/robot/client/` — machine config lifecycle, connection behavior
- `rdk/session/` — session management behavior
- `rdk/robot/web/` — auth and server behavior
- `app/domains/` — app backend business logic
- `agent/` — viam-agent behavior: subsystem management, update checks, provisioning flow, network management, restart logic. Affects docs: foundation setup, fleet provisioning, fleet system-settings, viam-agent reference pages.
- `viam-mobile/` — mobile app behavior: provisioning flow, Bluetooth/WiFi setup, machine control, teleop. Affects docs: fleet end-user setup, teleop, provisioning guides.

**What to look for in the diff — high confidence signals:**

- Changed default values for any user-facing parameter
- Changed timeout or retry constants
- Changed error messages or error codes
- Changed HTTP/gRPC status codes
- Changed validation rules (stricter or relaxed input constraints)

**What to look for — medium confidence signals:**

- Changed sort order or pagination behavior
- Modified retry/backoff logic (algorithm, intervals, max attempts)
- Altered rate limiting behavior
- Changed data format or serialization (wire format)
- Changed threading/concurrency model
- Changed file formats or file naming conventions

**What to look for — low confidence signals (require careful reading):**

- Performance characteristic changes (synchronous becoming async, fast operation gaining expensive I/O)
- Implicit contract violations (results no longer sorted, idempotency changed)
- Side effect changes (new global state, changed resource usage, race condition fixes that alter timing)
- Downgradability changes (irreversible migrations, state changes)

**Classification output:** For each behavioral change, record:

- The file and function where the change occurred
- What behavior changed, stated as a before/after
- Which flow in `flows.md` is affected (if any)
- The confidence tier (high/medium/low)

### Case 6: UI change

**Trigger:** Changed files in `app/ui/src/`, `app/test-cards/src/`, or `viam-mobile/`.

**What to look for in the diff:**

_Navigation and structure:_

- Changed tab names, sidebar labels, sub-tab names
- Changed menu item text, submenu structure
- New or removed routes under `app/ui/src/routes/`
- Changed page section headings in components (especially `section-group.svelte` which applies CSS uppercase)

_Interactive elements:_

- Changed button labels, toggle labels, dropdown option text
- Changed form field labels and placeholder text
- Changed modal titles and dialog text
- Changed toast/notification messages
- Changed tooltip text
- Changed banner messages

_Visual state:_

- Changed status indicator text
- Changed widget type names or labels
- Changed settings panel labels

_Feature flags:_

- Feature flag added, removed, or default changed in `app/data/feature_models.go` or `app/ui/src/lib/api/feature.ts`
- A feature flag change determines whether a UI element is visible — any docs describing that element's availability may need updating

_CSS rendering:_

- Changed `text-transform` rules that affect how labels render (source says "test" but user sees "TEST")
- These affect what docs should tell users to look for

_URLs and routes:_

- Changed route paths (docs link to app URLs)
- Changed URL patterns

**Classification output:** For each UI change, record:

- The component file and the specific label/element that changed
- The old and new text (accounting for CSS transforms)
- Whether this is a rename (old text → new text), removal, or addition

### Case 7: Deprecation or removal

**Trigger:** Any of these patterns in the diff across any repo:

- Proto `deprecated = true` option added to a field, method, or message
- Go `// Deprecated:` comment added to a function, type, or method
- Python `@deprecated` decorator or `DeprecationWarning`
- A previously-existing public symbol (function, struct, proto message, CLI command) deleted entirely
- Feature flag removed (feature may have gone GA or been dropped)
- Feature flag default changed (experimental → enabled by default, or vice versa)

**Lifecycle stages to distinguish:**

| Stage                        | Signal                                             | Docs action                                    |
| ---------------------------- | -------------------------------------------------- | ---------------------------------------------- |
| Newly deprecated             | `deprecated` marker added, symbol still exists     | Add deprecation notice, document replacement   |
| Removed                      | Symbol deleted from codebase                       | Remove from docs or add migration guide        |
| Promoted to GA               | Feature flag removed, experimental warning removed | Remove "experimental"/"beta" caveats from docs |
| Feature flag default changed | Flag now enabled/disabled by default               | Update availability descriptions               |

**Classification output:** For each deprecation or removal, record:

- The symbol and its location
- The lifecycle stage
- The replacement (if any) — look for the replacement in the same commit or PR
- Every language-specific form of the symbol name (for grepping docs)

### Case 8: SDK code example breakage

**Trigger:** Changed files in public API surfaces of SDK repos:

- `rdk/components/*/`, `rdk/services/*/` (Go SDK — interfaces and client code)
- `viam-python-sdk/src/viam/` (Python SDK)
- `viam-cpp-sdk/src/viam/` (C++ SDK)
- `viam-typescript-sdk/src/` (TypeScript SDK)
- `viam-flutter-sdk/lib/src/` (Flutter/Dart SDK)

**What to look for in the diff:**

- Renamed public functions or methods
- Changed function signatures (new parameters, removed parameters, changed types, changed return types)
- Changed class names or class hierarchies
- Changed import paths (module reorganization)
- Renamed helper functions that appear in docs examples (`sensor.FromDependencies` → `sensor.FromProvider`)
- Changed constructor signatures or initialization patterns
- Changed type aliases (`Mapping[str, Any]` → `Mapping[str, SensorReading]`)
- New required parameters on existing functions
- Changed exception/error types raised

**What distinguishes this from Case 1:** Case 1 covers proto-level changes. This case covers SDK-layer changes that don't originate from proto changes — helper functions, convenience methods, class hierarchies, framework features, import paths.

**Classification output:** For each SDK change, record:

- The SDK language
- The file and symbol that changed
- The old and new signature/name/path
- All language forms the old name might appear as in docs

### Case 9: Prerequisite/dependency change

**Trigger:** Changed files: `go.mod`, `go.sum` (for minimum Go version), `pyproject.toml`, `setup.py`, `setup.cfg`, `requirements.txt`, `CMakeLists.txt`, `package.json` (TypeScript/Flutter), `pubspec.yaml` (Flutter), Dockerfiles, install scripts.

**What to look for in the diff:**

- Minimum language version bumped (Go 1.24 → 1.25, Python 3.8 → 3.9, Dart SDK constraint changed)
- New system dependency required
- Removed platform support
- Added platform support
- Changed Docker base image
- New build dependency
- Changed installation instructions or scripts
- `agent/`: changed supported platforms, changed subsystem versions, changed provisioning requirements
- `viam-mobile/`: changed minimum iOS/Android version, changed app store requirements, changed Bluetooth/WiFi capabilities

**Classification output:** For each change, record:

- What prerequisite changed
- The old and new values
- Which docs sections state the old value (setup guides, quickstarts, SDK pages, tutorials)

### Case 10: Error message/condition change

**Trigger:** Diffs containing changed string literals in error-producing code (`fmt.Errorf`, `errors.New`, `raise`, `throw`, status codes), or changed error-handling control flow.

**What to look for in the diff:**

- Changed error message text
- New error conditions (new `if` blocks that return errors)
- Removed error conditions
- Changed error types or codes
- Changed circumstances under which an error occurs (validation now rejects input it previously accepted, or accepts input it previously rejected)

**Classification output:** For each error change, record:

- The old and new error text (or the new error condition if newly added)
- The circumstance that triggers it
- Whether any troubleshooting guide references this specific error text

### Case 11: Constraint/limit change

**Trigger:** Diffs containing changed `const` declarations, changed numeric literals in well-known locations, changed limit/threshold variables.

**What to look for in the diff:**

- Changed constants: timeout values, buffer sizes, max retries, max concurrent operations, file size limits, rate limits
- Changed threshold values: disk usage thresholds, confidence thresholds, connection limits
- Changed range constraints: valid value ranges for config fields, min/max values
- Changed formulas for computed limits (e.g., `CPU/2` → `CPU/4`)

**Classification output:** For each constraint change, record:

- The constant or variable name
- The file and line
- The old and new values
- The human-readable interpretation (e.g., `0.1` minutes = "6 seconds")

### Case 12: Implicit contract change

**Trigger:** This case cannot be detected from file paths alone. It is detected by reading diffs of functions in key behavioral paths and noticing that user-observable behavior changed without any explicit API, config, or interface change.

**What to look for in the diff:**

- Changed sort order of returned results
- Changed pagination behavior or page sizes
- Changed timing guarantees or ordering of operations
- Changed idempotency behavior
- Changed caching behavior (results that were cached are no longer, or vice versa)
- Changed concurrency model (serial → parallel or vice versa)
- Changed data precision or rounding
- Changed encoding or serialization details (float-as-number → float-as-string)

**This is the hardest case to detect.** The agent must read the diff carefully and reason: "Does this change alter anything a user would observe, even though no interface changed?" If uncertain, err on the side of flagging it.

**Classification output:** For each implicit contract change, record:

- What the implicit contract was (e.g., "results were sorted by date")
- What changed (e.g., "results are now sorted by ID")
- Why this matters to users
- Which docs pages describe the old behavior (even implicitly)

### Case 13: Security/compliance change

**Trigger:** Diffs touching auth, TLS, credential, permission, session, or telemetry code. Keyword scan all diffs for: `auth`, `tls`, `credential`, `secret`, `token`, `permission`, `rbac`, `session`, `encrypt`, `decrypt`, `certificate`, `telemetry`, `analytics`, `tracking`, `privacy`, `compliance`.

Key paths:

- `rdk/robot/web/` — auth handlers, TLS configuration
- `rdk/config/config.go` — `AuthConfig`, `NetworkConfig`
- `rdk/session/` — session management
- `app/auth/`, `app/selfservice/` — RBAC, OAuth
- `agent/` — credential management, provisioning security, TLS certificate handling
- `viam-mobile/` — authentication flow, credential storage, Bluetooth security
- Any file containing credential handling

**What to look for in the diff:**

- New permissions required for an operation
- Changed auth behavior (new credential types, changed validation)
- Changed TLS defaults (required → optional, or vice versa)
- New data collection or telemetry
- Changed credential storage or handling
- Changed session behavior (timeout changes, heartbeat changes)
- Changed encryption defaults

**Security changes have outsized impact.** Users may be making security decisions based on docs claims. Even small changes warrant immediate docs attention.

**Classification output:** For each security change, record:

- What changed and where
- The security implication
- Which docs pages make claims about the old behavior (auth docs, access control docs, architecture docs)

### Case 14: Installation/platform support change

**Trigger:** Changed files: CI configuration (platform matrices), Dockerfiles, installation scripts, build configuration, minimum version checks.

Key paths:

- `rdk/.github/` or equivalent CI config — supported platform matrices
- Dockerfiles — base images, dependencies
- Installation scripts — `install.sh`, setup commands
- Build configuration — `Makefile`, `CMakeLists.txt`, `build.gradle`
- `rdk/web/cmd/server/` — startup requirements
- `agent/` — supported platforms, installation methods, subsystem management, update mechanisms. Affects foundation setup and fleet system-settings docs.
- `viam-mobile/` — supported iOS/Android versions, app store deployment, device compatibility. Affects end-user setup and provisioning docs.
- Micro-RDK: ESP32 support files, toolchain requirements

**What to look for in the diff:**

- Platforms added or dropped from CI matrices
- Minimum OS version changes
- New system package dependencies
- Changed Docker base images
- Changed build requirements
- Changed supported architectures

**Classification output:** For each change, record:

- What platform or prerequisite changed
- The old and new state
- Which docs pages state the old information (setup guides, device prep guides, SDK installation pages)

---

## Phase 3: Find all affected docs pages

For every finding from Phase 2, identify every docs page that needs updating. Use both xref lookup and exhaustive grep. Never rely on xref alone — xrefs map to primary pages but miss secondary references across tutorials, how-tos, and quickstarts.

### Step 1: Xref lookup

For each finding, check the relevant xref file for a direct mapping:

| Finding type              | Xref file                            |
| ------------------------- | ------------------------------------ |
| Component API change      | `component-api-xref.md`              |
| Service API change        | `service-api-xref.md`                |
| App/fleet/data API change | `app-api-xref.md`                    |
| Config field change       | `config-xref.md`                     |
| CLI change                | `cli-xref.md`                        |
| Behavioral change         | `flows.md` ("Docs to check" headers) |

Record the primary docs page(s) from the xref. This is the starting point, not the complete answer.

### Step 2: Construct the full search set

For every changed symbol, construct the complete set of search terms. This is mandatory — the agent must not skip any form.

**Name variants — search for ALL of these:**

| Source form                                     | Generate and search for                                                                                       |
| ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| `ProtoCase` (e.g., `GetEndPosition`)            | `GetEndPosition`, `get_end_position`, `getEndPosition`, `get end position`, `end position`                    |
| `snake_case` (e.g., `sync_interval_mins`)       | `sync_interval_mins`, `SyncIntervalMins`, `syncIntervalMins`, `sync interval`, `sync_interval`                |
| CLI flag (e.g., `--org-id`)                     | `--org-id`, `org-id`, `org_id`, `orgId`, `OrgID`, `org id`                                                    |
| `kebab-case` (e.g., `base-remote-control`)      | `base-remote-control`, `base_remote_control`, `BaseRemoteControl`, `baseRemoteControl`, `base remote control` |
| Model triplet (e.g., `rdk:component:arm`)       | `rdk:component:arm`, the model name alone (`arm`), the full triplet                                           |
| Environment variable (e.g., `VIAM_MODULE_DATA`) | `VIAM_MODULE_DATA`, `viam_module_data`                                                                        |
| Import path (e.g., `viam.components.sensor`)    | `viam.components.sensor`, `from viam.components.sensor`, `viam/components/sensor`                             |

**Value variants — search for ALL of these:**

For every changed default value, timeout, constant, or limit:

- The numeric value itself (e.g., `0.1`)
- The value with units (e.g., `0.1 minutes`, `6 seconds`, `6s`)
- The human-readable form (e.g., "every 6 seconds", "every six seconds", "6-second interval")
- The old value AND the new value (the new value may already appear on some pages, revealing inconsistency)

**String variants:**

For every changed error message, UI label, or status string:

- The exact string
- Substrings that are likely to appear in docs (e.g., for error "exceeded request limit 100 on resource", also search "request limit 100", "exceeded request limit")
- The string in bold formatting (e.g., `**CONFIGURE**`, `**Save**`)
- The string in backticks (e.g., `` `CONFIGURE` ``)

**Also load search terms from `search-patterns.yaml`.** This file contains previously-discovered non-obvious mappings (e.g., `sync_interval_mins` default 0.1 → also search "6 seconds").

### Step 3: Execute the grep

Search the **entire docs repo**, not just `docs/**/*.md`. Include:

- `docs/**/*.md` — all markdown content
- `data/**` — Hugo data files (YAML, JSON, TOML) that populate generated tables
- `layouts/partials/**` — shared content blocks included across pages
- `layouts/shortcodes/**` — reusable content invoked from markdown
- `static/**` — may contain generated content or schema references
- `i18n/**` — internationalization strings if present
- `assets/**` — may contain embedded strings
- `config.toml` or `hugo.toml` — site configuration with strings

For each search term in the full search set, grep the docs repo. Use case-insensitive search for prose forms. Use case-sensitive search for code forms (function names, config fields).

**Process every match.** Do not truncate results. Do not sample. Do not skip matches because "the first few were enough." Every matching file is a candidate for updating.

For each match, record:

- The file path and line number
- The matching text in context (surrounding lines)
- Whether the match is in a code block, prose, frontmatter, data file, partial, or shortcode

### Step 4: Follow generated content

For each matched markdown file, check whether it uses Hugo shortcodes or includes that pull content from other files:

- `{{< readfile "..." >}}` — read the referenced file and search it too
- `{{< tabs >}}` — content may come from data files
- Custom shortcodes — check `layouts/shortcodes/` for the template
- Partials referenced in templates — check `layouts/partials/`

If a partial or include file contains a match, every page that uses that partial is affected. Find all pages that include it.

### Step 5: Check frontmatter

Search page frontmatter (title, linkTitle, description, aliases) for matches. These fields contain claims that can go stale:

- `description: "Sync data every 6 seconds to the cloud"` references a default
- `title: "Configure a wheeled base"` references a model name
- `aliases` contain old URL paths that may reference changed features

### Step 6: Deduplicate and compile

Union the results from xref lookup (Step 1) and grep (Steps 3-5). Remove duplicates. The result is the **complete list of affected docs pages** for this finding.

For each affected page, record:

- The file path
- Every specific line or section that references the changed symbol
- Whether the reference is in code, prose, frontmatter, or generated content

---

## Phase 4: Assess docs impact and produce changes

For each finding with its list of affected docs pages, assess whether the docs are actually wrong and produce the fix.

### Step 1: Read the current docs

For each affected page, read the specific section that references the changed symbol. Understand what claim the docs make.

### Step 2: Compare docs claim to current code

State explicitly:

- What the docs say (quote the specific text)
- What the code now says (quote or describe the current state)
- Whether there is a discrepancy

If there is no discrepancy (the docs are already correct — perhaps updated by a prior PR), mark the finding as "already correct" and move on.

### Step 3: Categorize the discrepancy

| Category       | Meaning                                             | Action                           |
| -------------- | --------------------------------------------------- | -------------------------------- |
| **Incorrect**  | Docs say X, code says Y                             | Fix the docs to say Y            |
| **Missing**    | Code has X, docs don't mention it                   | Add X to the docs                |
| **Stale**      | Docs describe deprecated/removed feature as current | Add deprecation notice or remove |
| **Incomplete** | Docs cover the topic but skip important new details | Add the missing details          |

### Step 4: Produce the fix

Edit the affected docs page(s) to correct the discrepancy. When editing:

- Fix the specific incorrect claim. Do not rewrite surrounding content.
- If fixing a code example, fix it in every language tab it appears in.
- If fixing a default value, fix it everywhere it appears (reference pages, how-to guides, tutorials, overview pages, frontmatter descriptions).
- Follow the style rules in the docs repo: sentence case for headings, no em dashes, no "e.g." or "via", no "(s)" plurals.
- If the fix requires substantial new content (new docs page, major rewrite), file an issue instead of making the change.

### Step 5: Validate each fix

For every edited file:

1. Run `npx prettier --write <file>`
2. Run `npx markdownlint-cli --config .markdownlint.yaml <file>`
3. Run `vale sync && vale <file>`
4. Verify the fix is consistent with the current code (re-read the code to confirm)

If `make build-prod` is available in the cloud environment, run it to catch Hugo build errors.

---

## Phase 5: Group and create PRs

### PR grouping rules

Do not create one PR for all findings. Group changes by **what caused them in the source code**, not by when they were detected or which docs file is affected.

**Rule 1: One source code change → one docs PR.**

If a single commit or merged PR in a source repo caused multiple docs pages to need updating, those updates belong in one PR. Example: a commit that changed `sync_interval_mins` default produces one PR that updates every page referencing that default.

**Rule 2: Multiple independent source changes → multiple docs PRs.**

If today's run finds three unrelated changes (a new CLI flag, a renamed Python SDK helper, a changed timeout constant), those become three separate PRs. A reviewer of the CLI flag PR should not need to understand the SDK rename.

**Rule 3: Multiple source commits to the same feature → one docs PR.**

If three commits over two days all modified motion planning constraints (added a field, changed a default, deprecated an old field), those changes are semantically related. One docs PR covers all of them.

**Rule 4: Two unrelated changes that happen to affect the same docs page → two PRs.**

Each PR touches different sections of the page. This is preferable to one PR with unrelated changes, even if it means the same file appears in two PRs.

**Rule 5: New capabilities get full docs PRs.**

Case 4 findings (new capability without docs) produce a PR with the agent's best attempt at a complete docs page. The agent follows **Playbook 2** (Writing a New Docs Page) to gather code references, read the code, determine page type and location, check vocabulary, and write the page. It follows **Playbook Diataxis** to classify the page type and avoid type mixing. The PR description notes that this is a new page and may need additional human review.

### How to determine grouping

1. For each finding, record which source commit(s) caused it.
2. Group findings that share the same source commit or source PR.
3. If source commits are in the same repo, by the same author, touching the same component/service area, within the same day — they can be grouped even if they're separate commits.
4. Findings from different repos or different feature areas are always separate groups.

### Priority ranking

After grouping, rank each group by the severity of its highest-severity finding:

| Priority    | Severity       | Description                                                                                              | Examples                                                                                                  |
| ----------- | -------------- | -------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| 1 (highest) | **Breaking**   | Docs describe something that no longer exists or works differently in a way that will cause user failure | Removed method still documented, renamed CLI flag, deleted config field, changed required/optional status |
| 2           | **Incorrect**  | Docs state a specific fact that is now wrong                                                             | Wrong default value, wrong parameter type, wrong error message, wrong UI label                            |
| 3           | **Security**   | Docs make a security-relevant claim that is now wrong                                                    | Changed auth behavior, changed TLS defaults, new permissions required                                     |
| 4           | **Stale**      | Docs describe a deprecated or removed feature as current                                                 | Deprecated method not marked, removed model still listed                                                  |
| 5           | **Missing**    | Code has something new that docs don't cover                                                             | New API method, new config field, new CLI flag, new component model                                       |
| 6           | **Incomplete** | Docs cover the topic but are missing new details                                                         | New optional field not listed, new enum value not shown                                                   |
| 7 (lowest)  | **Implicit**   | Behavioral or contractual change that docs may describe indirectly                                       | Changed sort order, changed retry timing, changed pagination                                              |

A group's priority is the highest (lowest number) severity among its findings. A group with one breaking finding and three incomplete findings is priority 1.

### PR cap and backlog

**The agent creates at most 5 PRs per run.**

Process groups in priority order (priority 1 first). After 5 PRs have been created, stop creating PRs. Write all remaining groups to the **backlog file** (`backlog.yaml` in the code-map repo) with their full finding details, grouping, and priority.

On the next run, the agent:

1. Reads the backlog file before processing new changes.
2. Merges backlog items with new findings from today's diffs.
3. Re-ranks all items (backlog + new) by priority.
4. Processes the top 5.
5. Writes the rest back to the backlog.

This ensures:

- On quiet days (1-2 changes), everything ships same day.
- On busy days, the most critical items always get through.
- Lower-priority items queue up and get processed over subsequent quiet days.
- Nothing is lost — every finding either becomes a PR or sits in the backlog until it does.

**Backlog file format** (`backlog.yaml`):

```yaml
# Backlog of findings awaiting PR creation.
# The daily agent reads this at the start of each run,
# merges with new findings, and writes back unprocessed items.

items:
  - id: "rdk-abc123-sync-default"
    priority: 2
    severity: incorrect
    source_commits:
      - repo: rdk
        sha: "abc123"
        description: "changed sync_interval_mins default from 0.1 to 0.5"
    affected_pages:
      - docs/data/reference.md
      - docs/data/capture-sync/capture-and-sync-data.md
      - docs/data/overview.md
    description: "Sync interval default changed from 0.1 (6 seconds) to 0.5 (30 seconds). Three pages reference the old value."
    added_date: "2026-04-07"
    case: 11
```

**Backlog hygiene:** If a backlog item has been waiting for more than 14 days, the agent promotes its priority by one level (e.g., priority 6 becomes priority 5) to prevent indefinite deferral. Items at priority 1 cannot be promoted further.

### Creating the PR

For each group:

1. Create a branch from `main`, named after the ticket when one is known:
   - DOCS ticket known: `claude/DOCS-<n>-<brief-description>`
   - Otherwise, upstream ticket key: `claude/<APP|RSDK>-<n>-<brief-description>`
   - Neither available: `claude/update-<brief-description>`
2. Apply all edits for this group.
3. Run all validators (prettier, markdownlint, vale).
4. Commit with a message describing the source change that motivated the update.
5. Push and create a PR against `viamrobotics/docs` base `main`.

**PR format:**

```
Title: Update <area> docs for <what changed>

## Source changes

- <TICKET-KEY> — <repo>#<PR-number-or-commit>: <one-line description of what changed in code>

## Docs changes

- <file>: <what was fixed and why>
- <file>: <what was fixed and why>

## How I found these

- Xref lookup: <which xref entries pointed here>
- Grep matches: <how many additional pages were found via grep>

---
Generated by daily docs change agent
```

### Recording the ticket key

Every docs PR must carry the ticket key of the change that motivated it, in the
branch name and in the `Source changes` line. GitHub for Jira reads the key from
the branch, commit message, PR title or body **at creation time**. Editing any of
them afterwards does nothing until a later push makes Jira rescan, so the key has
to be present when the PR is opened.

The branch name is the carrier that matters: it is set at creation, it is not
reworded during review, and it is what produces a pull-request link rather than
only a commit link.

**Getting the key.** You already read linked issues as motivation context in
Phase 2. Take the key from the same place:

- Usually it leads the upstream commit message or PR title:
  `APP-17295: embed MotionPlanReplayer…`, `RSDK-14259 CLI: Module reload…`
- If the commit carries only a PR number — `… (#13098)` — fetch that PR and take
  the key from its title.
- If no key exists, write `Documents: no ticket key found` in the body and use
  `claude/update-<brief-description>`. Never guess or construct a key.

**Preferring the DOCS key.** DOCS tickets are auto-filed from upstream tickets and
linked to them, so the DOCS key can be resolved from the upstream key:

```
project = DOCS AND issue in linkedIssues("APP-17295") AND statusCategory != Done
```

- One result → use that DOCS key in the branch, and add `Documents: DOCS-<n>` to
  the body.
- Several → use the closest summary match; list the others in the body.
- No result, or Jira is not reachable from the run environment → use the upstream
  key instead, and note which case applied.

Write the bare key either way. `viamrobotics/app#12896` alone is not matchable;
`APP-17295` is.

### Moving the ticket to Review in progress

When a docs PR is opened against a DOCS ticket, that ticket moves to
`Review in progress`, so the board shows the work as written and awaiting review
rather than untouched.

This is implemented as a Jira Automation rule in the DOCS project, not by the
agent:

- **When:** Pull request created
- **If:** repository is `viamrobotics/docs`
- **Then:** Transition issue to `Review in progress`

The agent does not transition tickets itself — its run environment has no Jira
write access. The rule is what performs the change, and it can only fire if
GitHub for Jira has already linked the PR to the ticket. That link requires the
DOCS key to be present in the branch name when the PR is opened, which is what
the previous section establishes. A key added later does not retroactively
trigger the rule.

The counterpart rule — transition to `Closed` when the PR merges — is a separate
decision and is not assumed here.

### Creating PRs for new docs pages

For Case 4 findings (new capabilities without docs), the agent writes a complete new docs page following **Playbook 2**:

1. Gather all code references (feature-inventory, coverage-gaps, xref files)
2. Read the actual code to understand behavior, params, defaults, errors
3. Determine page type using **Playbook Diataxis** and location in the docs site
4. Check `vocabulary.md` and landscape files for practitioner terms
5. Check whether the Viam app UI supports the feature
6. Write the page structured by type (API reference, config reference, how-to)
7. Track user state through sequential steps (for how-to/tutorial pages)
8. Validate SDK code examples against SDK source
9. Run all linters and vale

The PR description notes this is a new page:

```
Title: Add docs page for <new capability>

## Source changes

- <repo>#<PR-number-or-commit>: <one-line description of what was added>

## New page

- <file path>: <page type> covering <what the page documents>
- Written following Playbook 2; may need additional human review

## Code references

- <list of code files consulted>

---
Generated by daily docs change agent
```

---

## Phase 5b: Request and process Copilot review

After each PR is created, request a GitHub Copilot review, wait for it to complete, and action the feedback. Do this for every PR before moving on to the next one or to Phase 6.

### Step 1: Request Copilot review

The `viamrobotics/docs` repo may have a branch ruleset that auto-requests Copilot review on every PR. Even so, explicitly request it from the agent as a fallback:

```
gh api --method POST \
  /repos/viamrobotics/docs/pulls/<PR_NUMBER>/requested_reviewers \
  -f 'reviewers[]=copilot-pull-request-reviewer[bot]'
```

The `[bot]` suffix on the login name is required. If the request returns 422 because Copilot is already assigned by the ruleset, treat that as success and continue.

### Step 2: Wait for Copilot to complete its review

Copilot typically posts a review within 30 seconds to 2 minutes of the request. Poll for the review using:

```
gh api repos/viamrobotics/docs/pulls/<PR_NUMBER>/reviews \
  --jq '.[] | select(.user.login == "copilot-pull-request-reviewer[bot]") | {state, submitted_at, id}'
```

Poll every 15 seconds with a **5 minute timeout**. If Copilot has not reviewed after 5 minutes, record the skip in `run-history.yaml` under that PR and move on. Do not block the run indefinitely.

### Step 3: Fetch Copilot's review comments

Once Copilot's review exists, fetch its line-level comments:

```
gh api repos/viamrobotics/docs/pulls/<PR_NUMBER>/comments \
  --jq '.[] | select(.user.login == "Copilot") | {path, line, body, id}'
```

And the top-level review body:

```
gh api repos/viamrobotics/docs/pulls/<PR_NUMBER>/reviews \
  --jq '.[] | select(.user.login == "copilot-pull-request-reviewer[bot]") | .body'
```

### Step 4: Classify each Copilot comment

For every comment, decide one of three actions:

1. **Accept** — the comment identifies a real issue you should fix. Examples: wrong CLI flag, outdated example, misleading wording, missing reference, broken link, style inconsistency with surrounding content.

2. **Reject** — the comment is wrong or not applicable. Examples: suggests a change that contradicts the source code, flags a pattern that is intentional per the style guide, or comments on pre-existing content that is out of scope for this PR.

3. **Defer** — the comment identifies a real issue but fixing it is out of scope for this PR (e.g., a pre-existing bug unrelated to the source change being documented). Record these as entries in `missed-findings.md` for future processing rather than expanding this PR's scope.

**When in doubt, accept.** Copilot catches real mistakes. False positives are easy to revert; missed fixes mean user-facing errors ship.

**One important exception — pattern propagation:** If Copilot flags a wrong pattern (for example, a CLI command path) and the same pattern appears elsewhere in the docs repo that this PR didn't touch, grep the entire docs repo for every instance of the wrong pattern and fix them all in this PR. Do not leave pre-existing instances of the same bug unfixed. This is the lesson from 2026-04-10 missed-findings entry.

### Step 5: Apply accepted fixes

For each accepted comment:

1. Make the edit on the PR branch.
2. If Copilot's comment is a `suggestion` block (`.pull_request_review_comment` with a suggestion field), you can apply it directly or use the suggested wording as a starting point.
3. Re-run `prettier@3.2.5 --check`, `markdownlint-cli`, and `vale` on every file you touched.
4. Commit with a message like: "Address Copilot review: <brief description>".
5. Push to the same branch (no new PR needed).

### Step 6: Reply to Copilot comments

For accepted comments, leave a brief reply on each comment thread acknowledging the fix and referencing the commit SHA:

```
gh api --method POST \
  /repos/viamrobotics/docs/pulls/<PR_NUMBER>/comments/<COMMENT_ID>/replies \
  -f body="Fixed in <commit-sha-short>."
```

For rejected comments, leave a short explanation:

```
gh api --method POST \
  /repos/viamrobotics/docs/pulls/<PR_NUMBER>/comments/<COMMENT_ID>/replies \
  -f body="Not applicable here because <reason>."
```

For deferred comments, note the deferral and the `missed-findings.md` entry:

```
gh api --method POST \
  /repos/viamrobotics/docs/pulls/<PR_NUMBER>/comments/<COMMENT_ID>/replies \
  -f body="Valid finding but out of scope for this PR. Recorded in missed-findings.md for follow-up."
```

### Step 7: Record in run history

In `run-history.yaml`, record for each PR:

- Whether Copilot reviewed (yes / no / timeout)
- Number of Copilot comments received
- Number accepted, rejected, deferred
- The commit SHA of any follow-up fix commits

This builds a dataset for tuning the agent's first-pass quality over time.

### Failure modes

- **Copilot never reviews (timeout):** Record the timeout, continue to the next PR or Phase 6. Do not block.
- **Copilot reviews after the timeout:** The review will be visible on the PR for human review; treat it as a human task.
- **Copilot review conflicts with the source PR's intent:** Reject with explanation. Do not let Copilot override engineering decisions recorded in the source PR description.
- **Copilot flags pre-existing content the agent didn't touch:** Defer and record in `missed-findings.md`. Do not expand PR scope uncontrollably.

---

## Phase 6: Update agent state

After all PRs and issues are created, update the agent's state files in the code-map repo.

### Step 1: Update commit SHAs

In `maintenance.md`, update the last-checked commit SHA for every repo to the HEAD that was checked in this run. Update the verification date.

### Step 2: Add new xref mappings

For every code-to-docs mapping discovered via grep that was not already in an xref file, add it to the appropriate xref file. Format it consistently with existing entries.

### Step 3: Add new search patterns

For every non-obvious symbol-to-docs-text mapping discovered during grep (a search term that found a match the obvious terms would have missed), add it to `search-patterns.yaml`.

Example entry:

```yaml
- symbol: sync_interval_mins
  source: rdk/services/datamanager/builtin/config.go
  additional_terms:
    - "6 seconds"
    - "every 6 seconds"
    - "sync frequency"
  reason: "default of 0.1 minutes = 6 seconds, used in prose throughout data section"
  discovered: "2026-04-06"
```

### Step 4: Update coverage-gaps.md

- Add new entries for Case 4 findings (new capabilities without docs).
- Remove or mark entries for gaps that have been filled (a docs page now exists for a previously-flagged gap).
- Update deprecation entries for Case 7 findings.

### Step 5: Update feature-inventory.md

- Add new entries for new models, components, or services discovered in Case 4.
- Update existing entries if models changed.

### Step 6: Propose exclusions

If the agent encountered files that passed the relevance filter but turned out to be consistently irrelevant (internal test helpers with public-looking names, generated files not in the exclude list), add proposed entries to `exclusions.yaml` with a `proposed: true` flag and a reason. These require human approval before taking effect.

### Step 7: Record run metrics

Append to `run-history.yaml`:

```yaml
- run_date: "2026-04-06"
  repos:
    rdk:
      {
        old_commit: "abc123",
        new_commit: "def456",
        files_changed: 47,
        files_relevant: 12,
      }
    api:
      {
        old_commit: "ghi789",
        new_commit: "jkl012",
        files_changed: 3,
        files_relevant: 3,
      }
    app:
      {
        old_commit: "mno345",
        new_commit: "pqr678",
        files_changed: 28,
        files_relevant: 5,
      }
    viam-python-sdk:
      {
        old_commit: "stu901",
        new_commit: "vwx234",
        files_changed: 8,
        files_relevant: 2,
      }
    viam-cpp-sdk:
      {
        old_commit: "yza567",
        new_commit: "bcd890",
        files_changed: 0,
        files_relevant: 0,
      }
    motion-tools:
      {
        old_commit: "efg123",
        new_commit: "hij456",
        files_changed: 4,
        files_relevant: 1,
      }
  changes_processed: 23
  changes_by_case:
    case_1_api: 3
    case_2_config: 1
    case_3_cli: 0
    case_4_new_capability: 1
    case_5_behavior: 2
    case_6_ui: 4
    case_7_deprecation: 1
    case_8_sdk_examples: 2
    case_9_prerequisites: 0
    case_10_errors: 1
    case_11_constraints: 4
    case_12_implicit: 0
    case_13_security: 1
    case_14_platform: 0
  docs_pages_affected: 34
  prs_created: 5
  issues_filed: 1
  xref_entries_added: 7
  search_patterns_added: 2
  exclusions_proposed: 0
```

### Step 8: Validate prior findings

Check the status of PRs and issues created in the last 5 runs:

- **Merged PRs:** Confirm the fix is on `main`. No action needed.
- **Rejected PRs / closed issues:** Read the rejection reason. If the agent was wrong (false positive), add an entry to `false-positives.md` with the reason. If the finding was valid but deprioritized, note that in run history.
- **Open PRs with reviewer comments:** Note the feedback. If it reveals a pattern (e.g., "agent always over-fixes tutorial prose"), record in `playbook-feedback.md`.
- **Stale open PRs (open > 7 days, no review):** Note in run history. Do not nag.

### Step 9: Record playbook feedback

If the agent encountered any of these during this run, add an entry to `playbook-feedback.md`:

- A change that didn't fit any of the 14 cases
- A case definition that was ambiguous for a specific change
- A search pattern that seems like it should be a standard rule
- A docs area that is consistently hard to assess (suggest improving the xref or flow coverage)

Format:

```markdown
## <Date>: <Brief description>

- Situation: <what happened>
- Problem: <what was unclear or missing in the playbook>
- Suggestion: <proposed refinement>
- Status: proposed
```

Entries marked `status: accepted` by a human are applied in Phase 1 Step 1 on subsequent runs.

### Step 10: Commit and push code-map

Commit all changes to the code-map repo:

- Updated `maintenance.md`
- Updated `backlog.yaml` (new items added, processed items removed)
- Updated xref files
- Updated `search-patterns.yaml`
- Updated `coverage-gaps.md`
- Updated `feature-inventory.md`
- Updated `exclusions.yaml` (if proposed additions)
- Updated `run-history.yaml`
- Updated `playbook-feedback.md` (if new entries)
- Processed entries in `missed-findings.md` and `false-positives.md`

Push to `shannonbradshaw/viam-code-map`.

---

## Definition of "symbol"

Throughout this playbook, "symbol" means any identifiable thing in a code diff that could appear in docs. The complete list:

**Names:**

- Function/method names (`MoveToJointPositions`, `get_readings`, `TabularDataByMQL`)
- Class/struct/interface names (`Sensor`, `MLModelConfig`, `PackageConfig`)
- Proto message names (`MoveToJointPositionsRequest`, `DataCaptureMetadata`)
- Proto RPC names (`GetEndPosition`, `StreamingDataCaptureUpload`)
- Proto enum names and values (`PlanState`, `IN_PROGRESS`, `FAILED`)
- Proto field names (`capture_frequency_hz`, `sync_interval_mins`)
- Config JSON field names (`"mlmodel_name"`, `"wheel_circumference_mm"`)
- CLI command names (`viam data export`, `viam module generate`)
- CLI flag names (`--org-id`, `--key-id`, `--disable-browser-open`)
- CLI alias names (`-q`, `-vvv`, `auth` for `login`)
- Module model triplets (`rdk:component:arm`, `viam:camera:webcam`)
- Environment variable names (`VIAM_MODULE_DATA`, `VIAM_MODULE_ROOT`, `VIAM_HOME_DIR`)
- Package/import paths (`go.viam.com/rdk/components/arm`, `viam.components.sensor`)
- Registry identifiers (`namespace:module-name`, `viam:mlmodel:tflite_cpu`)
- Feature flag names (`ENABLE_INLINE_MODULES`, `RENDER_3D_ARM_MODELS_VIZ`)

**Values:**

- Default values (`0.1` for sync_interval_mins, `"localhost:8080"` for bind_address)
- Timeout values (`5s` restart backoff, `20s` session timeout, `10s` config refresh)
- Buffer/limit sizes (`256 KB` max capture file, `250` capture queue size, `10` concurrent resource construction)
- Threshold values (`0.90` disk usage deletion, `0.50` capture dir deletion)
- Retry parameters (`200ms` initial backoff, `2x` factor, `1hr` max)
- Port numbers (`8080`, `8443`)
- File paths (`~/.viam/capture`, `~/.viam/packages/`, `/tmp/viam-parent.sock`)
- File extensions (`.prog`, `.capture`)
- URL patterns (`appname_publicnamespace.viamapplications.com`)
- Version constraints (`Go 1.25.1+`, ESP32-WROVER minimum specs)
- Numeric limits (`5000` max planning iterations, `100` concurrent request limit, `10000` pipeline document limit, `5` minute pipeline timeout)

**Strings:**

- Error messages ("exceeded request limit 100 on resource", "failed to connect")
- Log messages that docs tell users to look for
- Status strings (`INITIALIZING`, `RUNNING`)
- MIME types (`application/x-gzip`)
- Protocol identifiers (`rpc.CredentialsTypeAPIKey`)

**UI elements:**

- Tab names, sidebar labels, sub-tab names (CONFIGURE, CONTROL, 3D SCENE, DATA)
- Button labels, toggle labels, dropdown option text
- Form field labels and placeholder text
- Modal titles, dialog text, tooltip text
- Toast/notification messages, banner messages
- Status indicator text, widget type names
- Settings panel labels
- Menu item text, submenu structure
- URL routes (`/machine/{id}/3d-scene`, `/data/query`)

**Signatures and shapes:**

- Function parameter lists (names, types, required/optional)
- Function return types
- Proto field types (`int64`, `double`, `bool`, `repeated string`)
- Proto field numbers (wire compatibility)
- Config field types (`string`, `float64`, `[]string`, `map[string]string`)
- Required vs optional status
- HTTP/gRPC status codes

**Structural patterns:**

- File/directory layouts documented in docs (`~/.viam/packages/data/module/...`)
- Config JSON structure (nesting, which fields go where)
- Command/subcommand hierarchy (`viam organizations auth-service oauth-app create`)
- Route/URL structures (`/machine/{id}/configure`, `/data/query`)
- Data schemas (the `readings` table structure with `organization_id`, `component_name`, etc.)

**Behavioral descriptions expressed as code references:**

- Algorithm names referenced in docs ("cBiRRT", "exponential backoff")
- Sequence descriptions ("sends SIGTERM, waits, then SIGKILL")
- Conditional logic ("if disk >= 90% AND capture dir >= 50%")
- Lifecycle phases ("startup -> validation -> creation -> reconfiguration -> shutdown")

When a diff contains a change to any of these, the agent must construct the full search set for that symbol and grep the entire docs repo.

---

## Thoroughness rules

These rules are non-negotiable. The agent must follow them on every run.

1. **Read every diff in the change set.** Do not skip files because they "probably don't matter." Every file that passed the relevance filter gets read.

2. **For every changed symbol, construct the full search set.** All language-specific forms (proto, Python, Go, TypeScript, C++, CLI), prose forms, partial matches, and associated values (old and new). See Phase 3 Step 2 for the complete variant table. See "Definition of symbol" above for what counts as a symbol.

3. **For every changed value, search for the value and its human-readable forms.** "0.1" and "6 seconds" and "every 6 seconds."

4. **Search the entire docs repo.** Not just `docs/**/*.md`. Include data files, partials, shortcodes, layouts, static includes.

5. **Process every grep match.** No truncation, no sampling, no "and several other pages." Every matching page gets assessed.

6. **Search in both directions.** The old form (to find what needs fixing) and the new form (to find what's already correct or inconsistent).

7. **Follow generated content.** When a page uses a shortcode or include, check the source file too. If the source file matches, every page that includes it is affected.

8. **Check frontmatter.** Titles, descriptions, and aliases contain claims that can go stale.

9. **Never declare "no docs impact" without running the full search set.** The agent cannot shortcut this for any change that passed the relevance filter.

10. **When uncertain whether a change affects docs, flag it.** False positives are correctable. False negatives are silent staleness. Err on the side of flagging.

---

## Case-to-playbook cross-reference

When a finding requires deeper analysis than this playbook covers, use the referenced playbook from the code-map:

| Case                                     | When to reference another playbook                                                                                                  |
| ---------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| Case 1, 2 (API/config)                   | Use **Playbook 1 Steps 2-3** for bidirectional comparison (code vs docs, docs vs code)                                              |
| Case 4 (new capability)                  | Follow **Playbook 2** end-to-end to write the new docs page; use **Playbook Diataxis** for page type                                |
| Case 5, 12 (behavioral/implicit)         | Use **flows.md** for the current flow trace; use **Playbook 1 Step 3** for verifying behavioral claims                              |
| Case 6 (UI)                              | Use **Playbook 5** for the full UI verification procedure (CSS transforms, superseded components, feature flags, permission gating) |
| Case 7 (deprecation)                     | Use **coverage-gaps.md** deprecated items table for context on known deprecations                                                   |
| Any case producing a new docs page       | Use **Playbook 2** for writing, **Playbook Diataxis** for page type classification                                                  |
| Any case touching a section landing page | Use **Playbook 7** to check if the section IA is still coherent                                                                     |

---

## Failure modes and recovery

**Agent cannot reach a repo:** Skip that repo for this run. Do not update its commit SHA in `maintenance.md`. Log the failure in run history. The next run will pick up the accumulated changes.

**Diff is extremely large (> 500 changed files in one repo):** This likely indicates a major release, rebase, or merge. Do not attempt to process all changes. Instead:

1. Log the situation in run history.
2. File a single issue: "Large change detected in <repo> (<N> files). Manual triage needed."
3. Update the commit SHA to HEAD so the next run starts fresh.

**Hugo build fails after edits:** Do not create the PR. Log the build failure. Review the edits for Hugo syntax errors (broken shortcodes, invalid frontmatter). Fix if possible; otherwise file an issue describing the intended change and the build error.

**Rate limiting or quota errors on GitHub:** Stop creating PRs. Log how many were created successfully. The remaining findings carry over implicitly — the commit SHAs are only updated if all processing completed, so the next run will re-discover them.
