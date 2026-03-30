---
linkTitle: "Build and deploy modules"
title: "Build and deploy modules with the CLI"
weight: 50
layout: "docs"
type: "docs"
description: "Scaffold, build, upload, and version modules from the command line."
---

Scaffold a new module, iterate on it locally with hot-reload, upload it to the registry, and manage versions and cloud builds.

{{< expand "Prerequisites" >}}
You need the Viam CLI installed and authenticated.
See [Viam CLI](/cli/) for installation and authentication instructions.
{{< /expand >}}

## Find your IDs

To find the part ID for a running machine (needed for reload and restart):

```sh {class="command-line" data-prompt="$"}
viam machines list --organization=<org-id> --location=<location-id>
```

```sh {class="command-line" data-prompt="$"}
viam machines part list --machine=<machine-id>
```

To find your organization and location IDs:

```sh {class="command-line" data-prompt="$"}
viam organizations list
```

```sh {class="command-line" data-prompt="$"}
viam locations list
```

## Scaffold a new module

Generate a module project with boilerplate code, a `meta.json` manifest, and a build script.
This command does not require authentication, so you can scaffold a module before logging in.

```sh {class="command-line" data-prompt="$"}
viam module generate
```

The generator walks you through an interactive prompt to choose:

- Module name
- Programming language (Python or Go)
- Namespace and visibility
- Resource type (component or service) and API

You can also pass flags to skip the interactive prompts:

```sh {class="command-line" data-prompt="$"}
viam module generate \
  --name=my-sensor-module \
  --language=python \
  --visibility=public
```

## Iterate during development

After making code changes, reload your module on a running machine without restarting the entire machine:

```sh {class="command-line" data-prompt="$"}
viam module reload-local --part-id=<part-id>
```

To reload a module from the registry (after uploading a new version):

```sh {class="command-line" data-prompt="$"}
viam module reload --part-id=<part-id>
```

If a reload is not sufficient, restart the module process:

```sh {class="command-line" data-prompt="$"}
viam module restart --part-id=<part-id>
```

## Update model definitions

After adding or changing models in your module, update the model definitions in `meta.json`.
This command runs the module binary in a sandbox, queries it for the API-model pairs it advertises, and updates the manifest.
It also auto-detects markdown documentation files named `namespace_module_model.md`.

```sh {class="command-line" data-prompt="$"}
viam module update-models --binary=./bin/module
```

Then push the updated `meta.json` to the registry:

```sh {class="command-line" data-prompt="$"}
viam module update
```

## Upload to the registry

Upload a module version for a specific platform.
The CLI validates the tarball before uploading: it checks for an executable at the declared entrypoint, verifies file permissions, and warns about platform mismatches or symlinks escaping the archive.
Pass `--force` to skip validation.

```sh {class="command-line" data-prompt="$"}
viam module upload \
  --version=1.0.0 \
  --platform=linux/amd64 \
  dist/archive.tar.gz
```

On success, the CLI prints a link to your module in the registry:

```sh {class="command-line" data-prompt="$" data-output="1"}
Version successfully uploaded! you can view your changes online here: https://app.viam.com/module/my-org/my-module
```

Upload for multiple platforms by running the command once per platform:

```sh {class="command-line" data-prompt="$"}
viam module upload --version=1.0.0 --platform=linux/amd64 dist/archive-amd64.tar.gz
```

```sh {class="command-line" data-prompt="$"}
viam module upload --version=1.0.0 --platform=linux/arm64 dist/archive-arm64.tar.gz
```

## Cloud builds

For CI/CD workflows, use cloud builds to compile your module on Viam's build infrastructure.

Start a cloud build:

```sh {class="command-line" data-prompt="$"}
viam module build start --version=1.0.0
```

Build for multiple platforms in one command:

```sh {class="command-line" data-prompt="$"}
viam module build start --version=1.0.0 --platforms=linux/amd64,linux/arm64
```

Build from a specific git ref:

```sh {class="command-line" data-prompt="$"}
viam module build start --version=1.0.0 --ref=main
```

Build locally to test before pushing:

```sh {class="command-line" data-prompt="$"}
viam module build local
```

List recent builds (the output includes build IDs you need for `build logs`):

```sh {class="command-line" data-prompt="$"}
viam module build list
```

View build logs:

```sh {class="command-line" data-prompt="$"}
viam module build logs --build-id=<build-id>
```

Wait for a build to complete and stream logs:

```sh {class="command-line" data-prompt="$"}
viam module build logs --build-id=<build-id> --wait
```

## Download a module

Download a module from the registry for local testing or inspection.
The `--id` flag takes the format `org-namespace:module-name`:

```sh {class="command-line" data-prompt="$"}
viam module download \
  --id=my-org:my-sensor-module \
  --version=1.0.0 \
  --platform=linux/amd64 \
  --destination=./downloaded-module
```

## Create a module

If you need to register a module in the registry before uploading (for example, to reserve a name), use `create`:

```sh {class="command-line" data-prompt="$"}
viam module create --name=my-new-module
```

Most users should use `viam module generate` instead, which handles both creation and scaffolding.

## Related pages

- [Write a driver module](/build-modules/write-a-driver-module/) for a complete guide to writing a hardware driver
- [Write a logic module](/build-modules/write-a-logic-module/) for writing automation and monitoring logic
- [Deploy a module](/build-modules/deploy-a-module/) for deployment with GitHub Actions
- [CLI reference](/dev/tools/cli/#module) for the complete `module` command reference
