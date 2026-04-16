---
linkTitle: "Automate with scripts"
title: "Automate with scripts"
weight: 80
layout: "docs"
type: "docs"
description: "Use the Viam CLI in shell scripts, CI/CD pipelines, and provisioning workflows."
---

Combine CLI commands into shell scripts, CI/CD pipelines, and provisioning workflows to automate common Viam operations.

## Authenticate in scripts

Interactive `viam login` opens a browser, which does not work in headless environments.
Use API key authentication instead:

```sh {class="command-line" data-prompt="$"}
viam login api-key --key-id=$VIAM_API_KEY_ID --key=$VIAM_API_KEY
```

Store credentials in environment variables or your CI/CD system's secret manager, not in the script itself.
To create an API key, see [Manage API keys](/cli/administer-your-organization/#manage-api-keys).

### Use profiles for non-interactive auth

If a script needs to operate across multiple organizations, set up profiles in advance:

```sh {class="command-line" data-prompt="$"}
viam profiles add --profile-name=production --key-id=$PROD_KEY_ID --key=$PROD_KEY
viam profiles add --profile-name=staging --key-id=$STAGING_KEY_ID --key=$STAGING_KEY
```

Then use `--profile` on each command, or set `VIAM_CLI_PROFILE_NAME` to activate a profile for the entire script:

```sh {class="command-line" data-prompt="$"}
export VIAM_CLI_PROFILE_NAME=production
viam machines list --all
```

## CI/CD: upload a module on release

Viam publishes two official GitHub Actions for building and uploading modules. Prefer these over invoking the CLI by hand in a workflow:

- [`viamrobotics/build-action`](https://github.com/viamrobotics/build-action) triggers a cloud build for every platform declared in your module's `meta.json` and uploads each artifact to the registry.
- [`viamrobotics/upload-module`](https://github.com/viamrobotics/upload-module) uploads a tarball you built yourself. Use this when you need custom runners or only target one platform.

A minimal workflow that runs a cloud build and uploads to the registry on every release:

```yaml
# .github/workflows/publish.yml
on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: viamrobotics/build-action@v1
        with:
          version: ${{ github.ref_name }}
          ref: ${{ github.sha }}
          key-id: ${{ secrets.VIAM_KEY_ID }}
          key-value: ${{ secrets.VIAM_KEY }}
```

`build-action` reads the `build` block in `meta.json` to determine target platforms and build commands. For the full setup, including `meta.json` configuration and an example that uses `upload-module` instead, see [Deploy a module](/build-modules/deploy-a-module/).

## CI/CD: retrain a model on new data

A script that creates a fresh dataset from recent data and submits a training job.

Set these environment variables before running:

- `VIAM_KEY_ID` and `VIAM_KEY`: your API key credentials (see [Manage API keys](/cli/administer-your-organization/#manage-api-keys))
- `ORG_ID`: your organization ID (run `viam organizations list`)

```sh
#!/bin/bash
set -euo pipefail

viam login api-key --key-id=$VIAM_KEY_ID --key=$VIAM_KEY

# Create a dataset from the last 7 days of labeled images.
# The create command prints: "Created dataset <name> with dataset ID: <uuid>"
DATASET_ID=$(viam dataset create --org-id=$ORG_ID --name="weekly-$(date +%F)" \
  | grep -oE '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}')

# date -v is macOS; date -d is Linux. Adjust for your platform.
START=$(date -u -v-7d +%FT%TZ 2>/dev/null || date -u -d '7 days ago' +%FT%TZ)
END=$(date -u +%FT%TZ)

viam dataset data add filter \
  --dataset-id=$DATASET_ID \
  --org-ids=$ORG_ID \
  --tags=labeled \
  --start=$START \
  --end=$END

# Submit a managed training job
viam train submit managed \
  --dataset-id=$DATASET_ID \
  --model-org-id=$ORG_ID \
  --model-name=defect-detector-$(date +%F) \
  --model-type=object_detection \
  --model-framework=tflite \
  --model-labels=defective,good
```

Schedule this as a cron job or a weekly CI/CD trigger.

## Batch fleet operations

### List all machines

Set `ORG_ID` to your organization ID (run `viam organizations list`).

```sh
#!/bin/bash
set -euo pipefail

viam login api-key --key-id=$VIAM_KEY_ID --key=$VIAM_KEY

# List all machines across all locations
viam machines list --organization=$ORG_ID --all
```

## Provisioning: create and configure a machine

Script that creates a machine and applies a standard configuration fragment.

Set these environment variables before running:

- `VIAM_KEY_ID` and `VIAM_KEY`: your API key credentials
- `ORG_ID`: your organization ID
- `LOCATION_ID`: your location ID (run `viam locations list`)

The script takes two arguments: the machine name and the fragment ID.

```sh
#!/bin/bash
set -euo pipefail

MACHINE_NAME=$1
FRAGMENT_ID=$2

viam login api-key --key-id=$VIAM_KEY_ID --key=$VIAM_KEY

# Create the machine.
# Output format: "created new machine with id <uuid>"
CREATE_OUTPUT=$(viam machines create --name=$MACHINE_NAME --location=$LOCATION_ID)
MACHINE_ID=$(echo "$CREATE_OUTPUT" | grep -oE '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}')

# Get the part ID from the part list.
# Output includes lines like "  ID: <uuid>"
PART_ID=$(viam machines part list --machine=$MACHINE_ID | grep 'ID:' | head -1 | awk '{print $2}')

# Apply the configuration fragment
viam machines part fragments add --part=$PART_ID --fragment=$FRAGMENT_ID

echo "Machine $MACHINE_NAME ($MACHINE_ID) created with fragment $FRAGMENT_ID applied."
```

## Bulk data export

Export all images from a fleet for offline analysis.
Set `ORG_ID` to your organization ID.

```sh
#!/bin/bash
set -euo pipefail

viam login api-key --key-id=$VIAM_KEY_ID --key=$VIAM_KEY

# date -v is macOS; date -d is Linux. Adjust for your platform.
START=$(date -u -v-30d +%FT%TZ 2>/dev/null || date -u -d '30 days ago' +%FT%TZ)
END=$(date -u +%FT%TZ)

viam data export binary filter \
  --destination=./fleet-data \
  --org-ids=$ORG_ID \
  --mime-types=image/jpeg,image/png \
  --start=$START \
  --end=$END \
  --parallel=20
```

The `--parallel` flag controls how many concurrent downloads run (default: 100).
Increase it for faster exports on high-bandwidth connections, or decrease it to reduce load.

## Tips for scripting

- Use `--quiet` (`-q`) to suppress non-essential output when parsing command results
- Use `--debug` (`-vvv`) when troubleshooting a script
- Set defaults with `viam defaults set-org` to avoid passing `--org-id` on every command
- All timestamps use ISO-8601 format: `2026-01-15T00:00:00Z`
- Exit codes are non-zero on failure, so `set -e` works as expected

## Related pages

- [Viam CLI overview](/cli/overview/) for installation and authentication
- [Provision devices](/fleet/provision-devices/) for provisioning with viam-agent
- [Deploy a module](/build-modules/deploy-a-module/) for GitHub Actions integration
- [CLI reference](/cli/) for the complete command reference
