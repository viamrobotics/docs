---
linkTitle: "Deploy a module"
title: "Deploy a module"
weight: 30
layout: "docs"
type: "docs"
description: "Pick a deployment path for your module: hot-reload onto one machine, or release a versioned package through the registry."
date: "2025-01-30"
aliases:
  - /operate/modules/deploy-a-module/
  - /build/development/deploy-a-module/
  - /development/deploy-a-module/
  - /extend/modular-resources/upload/
  - /modular-resources/upload/
  - /registry/upload/
  - /how-tos/upload-module/
---

There are several ways to deploy a module you wrote onto a machine. Which one to use depends on where you are in your software development cycle.

## Pick a path

| You want to...                                         | Path                                             | When to use it                                                                                                                                                                                                                                                      |
| ------------------------------------------------------ | ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Test on one machine right now                          | [Hot-reload](#hot-reload-onto-one-machine)       | You wrote a module on your laptop and want to deploy it for testing on the compute machine for your robot. This is the fastest develop-deploy loop. The CLI builds the module, gets it onto the target machine, and adds it to the machine's config in one command. |
| Release a versioned module for others (or for a fleet) | [Versioned release](#release-a-versioned-module) | You want a stable version that any machine in your org (or any Viam user, if public) can install. This is what you do once your module is ready to share.                                                                                                           |

Hot-reload gets your module onto a target machine and adds it to the machine's config in one command. A versioned release is a tagged upload to the Viam registry, numbered with a semantic version like `0.1.0`. Any machine in your org (or any Viam user's machine, if public) can install it.

## Hot-reload onto one machine

Hot-reload deploys your in-progress module to a single machine in one command: build, copy, add to the machine's config. It's faster than a versioned release because it builds only for the target's platform, skips GitHub Actions runner setup, and tells the machine to restart the module right away with the new code instead of waiting for the next cloud sync.

The CLI provides two commands: `viam module reload` (build in the cloud) and `viam module reload-local` (build on your laptop). The procedure below uses `viam module reload`, which works regardless of your laptop's architecture. To skip the cloud round-trip when your laptop matches the target, see [Build on your laptop with `reload-local`](#reload-local) at the end of this section.

**Run it:**

Find your machine's part ID first. At the top of the machine's page, click the **Live** / **Offline** status dropdown, then click **Part ID** to copy it.

In the command below:

- `--model-name` is the full model identifier from your `meta.json`, in the form `namespace:module-name:model-name`. Copy it from the `model` field of the entry in `meta.json`'s `models` array. If your module declares more than one model, pick the one you want to add to the machine.
- `--resource-name` names the component or service that the model adds to the machine — a component (sensor, motor, camera, and so on) or a service (ML model, vision, motion, and so on), depending on which API the model implements. Pick any unique string. It appears on the **CONFIGURE** tab and is how you reference the component or service from client code.

From your module's root directory (where `meta.json` lives), run:

```sh {class="command-line wrap" data-prompt="$"}
viam module reload --part-id <machine-part-id> --model-name <namespace:module-name:model> --resource-name <resource-name>
```

**What to expect:**

- The CLI prints build progress, then upload progress, then a success line.
- The machine's **CONFIGURE** tab shows the new component or service with the name you passed to `--resource-name`. Open it and set the attributes your module expects.
- The module starts within a few seconds. The **LOGS** tab shows a `Module successfully added` entry with your module name.

**On each code change:** rerun the same command to deploy the new code.

### Build on your laptop with `reload-local` {#reload-local}

If your laptop and the target have the same architecture (for example, both `linux/arm64`), `reload-local` builds on your laptop and copies the archive directly to the target over the network. No cloud round-trip.

For cross-architecture deploys, use cloud `reload` rather than `reload-local`. Python in particular has no alternative because PyInstaller can't cross-compile.

The flags are the same as `reload`. From your module's root directory:

```sh {class="command-line wrap" data-prompt="$"}
viam module reload-local --part-id <machine-part-id> --model-name <namespace:module-name:model> --resource-name <resource-name>
```

The target machine must be online (visible in the Viam app). The CLI connects over WebRTC, authenticates with your `viam login` session, and uses the machine's shell service to copy the archive. You don't need LAN access, a VPN, SSH keys, or port forwarding.

**Useful flags:**

- `--no-build` skips the build step if you already built the archive manually with `bash build.sh`.
- `--local` runs the module from source files on your laptop instead of shipping a tarball. Use this only when the target machine is your laptop. In `--local` mode, `viam module restart` picks up Python source edits without a rebuild.

For the full hot-reload walkthrough including how it fits into the development loop, see [Test locally](/build-modules/write-a-driver-module/#3-test-locally) on the driver-module page.

When you're ready to share the module beyond the one machine you tested on, do a [versioned release](#release-a-versioned-module).

## Release a versioned module

If you've been testing with `viam module reload`, your code is already running on a single target machine. A versioned release publishes the same code as a numbered package in the Viam registry. Any machine in your org can install it (or any Viam user's machine, if the module is public). Machines that aren't pinned to a specific version pick up new releases automatically, within a minute or two.

Two ways to build and upload:

- **Cloud build (recommended).** Viam compiles your module for every target platform from your GitHub repo. Trigger it manually with one CLI command, or set up GitHub Actions to auto-build on every release tag. No local cross-compilation.
- **Manual upload.** You build locally and run `viam module upload`. You're responsible for cross-compiling for each target platform yourself.

Both paths share the same prep work first.

### Before you start

**For cloud build (recommended):** create a Viam organization API key in the Viam app at your org's **Settings** page. The key value is shown once and can't be retrieved later, so save it before navigating away. You'll also need your module's code in a GitHub repo with the `url` set in `meta.json`; if you don't have one yet, you'll set it up in [Publish with cloud build](#release-with-cloud-build) below.

**For manual upload:** you need a way to build a binary for each platform you want to support. Cross-compiling from `linux/amd64` to `linux/arm64` requires `GOOS`/`GOARCH` for Go or building on the target architecture for Python (PyInstaller does not cross-compile).

### Update meta.json for publishing

The Viam module generator created a working `meta.json` in your module directory. Before publishing, update these fields if needed:

- **`visibility`**: defaults to `private` (only your organization can install). Change to `public` if you want any Viam user to install your module, or `public_unlisted` to make it reachable by ID but not listed in registry search results. Public visibility requires your organization to have a public namespace, set up at your org's **Settings** page in the Viam app.
- **`url`**: link to the source repository. **Required for cloud build** — set this to your GitHub repo's URL.
- **`description`**: shown in the registry UI and search results. Replace the generator default with what your module actually does.
- **`markdown_link`** (optional): path to a README. If your module is going public, a README is essential. For starter templates, see [README templates](#readme-templates) at the bottom of this page.

For the full `meta.json` field reference, see [Module reference](/build-modules/module-reference/).

### Review the build scripts

The generator creates build and setup scripts. The defaults work for typical Python and Go modules. Review and customize them if you need additional build steps (for example, compiling native extensions or installing system packages).

{{< tabs >}}
{{% tab name="Python" %}}

| File       | Purpose                                              |
| ---------- | ---------------------------------------------------- |
| `setup.sh` | Installs Python dependencies from `requirements.txt` |
| `build.sh` | Packages the module into a `.tar.gz` archive         |
| `run.sh`   | Entrypoint script that starts the module             |

{{% /tab %}}
{{% tab name="Go" %}}

| File       | Purpose                                                               |
| ---------- | --------------------------------------------------------------------- |
| `setup.sh` | Installs build dependencies (Go modules are typically self-contained) |
| `build.sh` | Cross-compiles the binary and packages it into a `.tar.gz` archive    |
| `Makefile` | Local build targets                                                   |

The generated `build.sh` uses `GOOS` and `GOARCH` environment variables to cross-compile for the target platform. Cloud build sets these automatically.

{{% /tab %}}
{{< /tabs >}}

With prep complete, follow one of the two sections below to publish your module. [Cloud build](#release-with-cloud-build) is recommended for most cases; use a [manual upload](#release-manually) only when cloud build isn't an option.

### Publish with cloud build (recommended) {#release-with-cloud-build}

Cloud build is a Viam-side build service that compiles your module from your GitHub repo for every target platform listed in `meta.json`'s `build.arch`. Both paths below require your module to be in a GitHub repo with the URL set in `meta.json`.

If you don't have a GitHub repo yet, push your module's code to one. From your module's root directory:

```sh {class="command-line" data-prompt="$"}
git init
git add .
git commit -m "Initial module code"
git remote add origin <your-repo-url>
git push -u origin main
```

There are two ways to start a build: a [one-shot build from the CLI](#one-shot-build-from-the-cli) for a single release, or [auto-build on every GitHub release](#auto-build-on-every-github-release) for ongoing releases.

#### One-shot build from the CLI

Use this for a single release without setting up GitHub Actions. From your module's root directory:

```sh {class="command-line" data-prompt="$"}
viam module build start --version 0.1.0
```

The `--version` value is what the package will be tagged as in the registry. Increment it for each release.

{{< alert title="Non-main default branches" color="tip" >}}
Cloud build expects your repository's default branch to be `main`. If your repository uses `master` (or another branch), pass the `--ref` flag:

```sh {class="command-line" data-prompt="$"}
viam module build start --ref master --version 0.1.0
```

{{< /alert >}}

**What to expect:**

- The CLI prints a build ID and exits. The build runs in Viam's cloud.
- Follow the logs with `viam module build logs --id <build-id>`.
- On success, your module appears at `https://app.viam.com/module/<namespace>/<module-name>` with the version you passed to `--version`.

#### Auto-build on every GitHub release

Use this for ongoing releases. Set up once, then every new release tag triggers a build automatically. The generator's `.github/workflows/deploy.yml` workflow uses the [`viamrobotics/build-action`](https://github.com/viamrobotics/build-action) GitHub action to start the build.

**1. Add Viam credentials as GitHub secrets.**

1. In your GitHub repository: **Settings → Secrets and variables → Actions**.
1. Add two repository secrets:
   - `VIAM_KEY_ID`: your API key ID
   - `VIAM_KEY_VALUE`: your API key value

**2. Tag a release.**

```sh {class="command-line" data-prompt="$"}
git tag v0.1.0
git push origin v0.1.0
```

**What to expect:**

- The GitHub Action starts immediately. Watch progress in the **Actions** tab of your GitHub repo. A typical first build takes 5-15 minutes (longer for the first run because dependencies aren't cached).
- When the workflow turns green, your module appears at the registry with the tagged version.
- If the workflow fails, click into the run for the build log. See the **Cloud build fails in GitHub Actions** entry under [Troubleshooting](#troubleshooting) for the common causes.

### Publish with a manual upload {#release-manually}

Use this when you can't use cloud build (no GitHub repo, restricted CI, etc.). You build locally and upload one archive per target platform.

{{< alert title="You must build for the target platform" color="caution" >}}
The binary in your archive must already be compiled for the target machine's OS and architecture. If you build on an x86 laptop and upload as `linux/arm64` without cross-compiling, the module will fail with `exec format error` on ARM machines.
{{< /alert >}}

**1. Build for each target platform:**

{{< tabs >}}
{{% tab name="Python" %}}

PyInstaller doesn't cross-compile, so each platform you want to support needs its own build run on a machine of that architecture. (Or use [cloud build](#release-with-cloud-build), which handles this for you.)

```sh {class="command-line" data-prompt="$"}
cd my-sensor-module
bash build.sh
```

The generated `build.sh` uses [PyInstaller](https://pypi.org/project/pyinstaller/) to compile your module into a standalone executable containing the Python interpreter and all dependencies.

{{< alert title="PyInstaller limitation: relative imports" color="note" >}}
PyInstaller does not support relative imports in entrypoints (imports starting with `.`). If you get `ImportError: attempted relative import with no known parent package`, see the [PyInstaller workaround](https://github.com/pyinstaller/pyinstaller/issues/2560).
{{< /alert >}}

{{% /tab %}}
{{% tab name="Go" %}}

```sh {class="command-line" data-prompt="$"}
cd my-sensor-module
GOOS=linux GOARCH=arm64 go build -o dist/module cmd/module/main.go
tar -czf dist/archive.tar.gz -C dist module
```

Set `GOARCH` to match your target machine: `amd64` for x86_64, `arm64` for ARM.

{{% /tab %}}
{{< /tabs >}}

**2. Upload the archive:**

```sh {class="command-line" data-prompt="$"}
viam module upload --version=0.1.0 --platform=linux/arm64 dist/archive.tar.gz
```

**3. Repeat for each platform you want to support:**

{{< tabs >}}
{{% tab name="Python" %}}

On each target architecture, build and upload separately:

```sh {class="command-line" data-prompt="$"}
bash build.sh
viam module upload --version=0.1.0 --platform=<linux/amd64-or-linux/arm64> dist/archive.tar.gz
```

{{% /tab %}}
{{% tab name="Go" %}}

```sh {class="command-line" data-prompt="$"}
GOOS=linux GOARCH=amd64 go build -o dist/module cmd/module/main.go
tar -czf dist/archive.tar.gz -C dist module
viam module upload --version=0.1.0 --platform=linux/amd64 dist/archive.tar.gz
```

{{% /tab %}}
{{< /tabs >}}

**What to expect:**

- Each `viam module upload` prints `Version successfully uploaded! you can view your changes online here: <url>` on success.
- Your module appears at the registry with the uploaded version. Each platform you uploaded is listed under that version.
- Before uploading, the CLI checks that the entrypoint exists in the archive and has execute permissions. If either check fails, the CLI stops the upload. The CLI also warns (but does not block) if the archive contains symlinks that point outside the archive. To skip the entrypoint checks (not recommended for production), pass `--force`.

## Configure on a machine {#step-5-configure-on-a-machine}

With your module in the registry, any machine in your org can use it (and any Viam user's machine, if the module is public).

1. In the [Viam app](https://app.viam.com), open your machine's **CONFIGURE** tab.
1. Click **+** and select **Configuration block**.
1. Search for your module by name or browse the registry, then add it.
1. Pick a model from your module and create an instance. Name the instance and configure its attributes:

   ```json
   {
     "source_url": "https://api.example.com/sensor/data"
   }
   ```

1. Click **Save**.

**What to expect:**

- `viam-server` downloads the module from the registry within a few seconds.
- The **LOGS** tab shows a `Module successfully added` entry with your module name.
- Open the **CONTROL** tab and verify the component responds.
- If the module fails to start, the **LOGS** tab shows the error. See the **Module works locally but fails after deployment** entry under [Troubleshooting](#troubleshooting) below.

That's the first deploy. To release new versions, pin a machine to a specific version, change visibility, restrict uploads to specific platforms, or perform other lifecycle operations, see [Update and manage modules](/build-modules/manage-modules/).

## Troubleshooting

{{< expand "Upload fails with \"not authenticated\"" >}}

- Log in to the Viam CLI: `viam login`.
- If using an API key, verify it has organization-level access.
- Check that `VIAM_KEY_ID` and `VIAM_KEY_VALUE` are set correctly in your GitHub secrets (for cloud build).

{{< /expand >}}

{{< expand "Upload fails with \"invalid meta.json\"" >}}

- Verify `meta.json` is valid JSON. Run `python -m json.tool meta.json` or `jq . meta.json` to check.
- Confirm the `module_id` matches the format `namespace:module-name`.
- Ensure all model entries have both `api` and `model` fields.

{{< /expand >}}

{{< expand "Module not appearing in the registry" >}}

- Check the module's visibility. If it is `private`, it only appears for users in your organization.
- Verify the upload completed successfully.
- The module may take a minute to propagate. Refresh the page and try again.

{{< /expand >}}

{{< expand "Machine cannot find the module" >}}

- Verify the module version supports the machine's platform. If your machine runs `linux/arm64` but you only uploaded for `linux/amd64`, the machine cannot use it.
- Check the module version. If the machine is pinned to a nonexistent version, it will fail.
- Confirm the machine is online and connected to the cloud.

{{< /expand >}}

{{< expand "Cloud build fails in GitHub Actions" >}}

- Check the **Actions** tab in your GitHub repository for the build log.
- If your repository's default branch is not `main` (for example, it uses `master`), pass `--ref master` to `viam module build start`.
- Verify your `setup.sh` and `build.sh` scripts work locally.
- Confirm the `build.path` in `meta.json` matches the actual output location.
- Ensure the GitHub secrets are set and not expired.

{{< /expand >}}

{{< expand "Exec format error on target machine" >}}

This means the binary was compiled for the wrong architecture. For example, you built a `linux/amd64` binary but the target machine is `linux/arm64`.

- Use [cloud build](#release-with-cloud-build) to compile for all target platforms automatically.
- If deploying manually, cross-compile with the correct `GOOS` and `GOARCH` before uploading.
- Verify the platform flag in your `upload` command matches the binary's architecture (for example, `--platform=linux/arm64` for an `arm64` target).

{{< /expand >}}

{{< expand "Module works locally but fails after deployment" >}}

- Check for hard-coded paths, missing environment variables, or dependencies installed on your machine but not in the build environment.
- For Python, verify all dependencies are in `requirements.txt`.
- For Go, verify the binary is compiled for the correct target architecture.
- Check the module logs in the **LOGS** tab.

{{< /expand >}}

## Reference

### README templates {#readme-templates}

{{< expand "Module README template" >}}

```md
# `my-sensor-module`

This module implements the [Viam sensor API](https://docs.viam.com/reference/apis/components/sensor/) in a `my-org:my-sensor-module:my-sensor` model.
With this model, you can gather temperature and humidity data from a custom HTTP endpoint.

Navigate to the **CONFIGURE** tab of your machine's page.
Click the **+** button, select **Configuration block**, then select the `sensor / my-sensor-module:my-sensor` model provided by the [`my-sensor-module` module](https://app.viam.com/module/my-org/my-sensor-module).
Click **Add module**, enter a name for your sensor, and click **Create**.

## Models

This module provides the following model(s):

- [`my-org:my-sensor-module:my-sensor`](#my-sensor) - A custom sensor that reads temperature and humidity from an HTTP endpoint
```

{{< /expand >}}

{{< expand "Model README template" >}}

````md
# Model `my-org:my-sensor-module:my-sensor`

A description of what this model does and what hardware or services it supports.

## Configuration

The following attribute template can be used to configure this model:

```json
{
  "source_url": "<string>",
  "poll_interval": <float>
}
```

### Attributes

| Name            | Type   | Required | Description                                 |
| --------------- | ------ | -------- | ------------------------------------------- |
| `source_url`    | string | Yes      | The HTTP endpoint to read sensor data from  |
| `poll_interval` | float  | No       | Polling interval in seconds (default: 10.0) |

### Example Configuration

```json
{
  "source_url": "https://api.example.com/sensor/data",
  "poll_interval": 5.0
}
```

## DoCommand

If your model implements DoCommand, document each supported command.

### Example DoCommand

```json
{
  "command": "calibrate",
  "offset": 1.5
}
```
````

{{< /expand >}}

You can point your module's registry page to a README by setting the `markdown_link` field in `meta.json` to a file path (for example, `README.md`) or a section anchor (for example, `README.md#my-sensor`).
