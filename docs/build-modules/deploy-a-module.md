---
linkTitle: "Deploy a module"
title: "Deploy a module"
weight: 30
layout: "docs"
type: "docs"
description: "Pick a deployment path for your module: hot-reload onto one machine, release a versioned package through the registry, or rely on Viam's automatic deploy for inline modules."
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

You have several ways to get a module you wrote onto a machine. Which one to use depends on what you want to do next.

## Pick a path

| You want to...                                         | Path                                                                        | When to use it                                                                                                                                                                                              |
| ------------------------------------------------------ | --------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Test on one machine right now                          | [Hot-reload](#hot-reload-onto-one-machine)                                  | You wrote a module on your laptop and want to try it on a Pi or another machine. Fastest dev loop. Module is uploaded as a private version on your org and configured on the target machine in one command. |
| Release a versioned module for others (or for a fleet) | [Versioned release](#release-a-versioned-module)                            | You want a stable version that any machine in your org (or any Viam user, if public) can install. This is what you do once your module is ready to share.                                                   |
| Deploy a module you wrote in the browser               | [`Save & Deploy`](/build-modules/write-an-inline-module/#6-save-and-deploy) | You used the inline editor in the Viam app. Deployment is one click: Viam builds and deploys for you. You don't need this page.                                                                             |

Hot-reload and versioned release both go through the Viam registry. Hot-reload uploads as a private development version on your org and immediately configures it on the machine you specify. A versioned release is a tagged, semver-numbered upload that any authorized machine can pull.

## Hot-reload onto one machine

`viam module reload` builds your module, uploads it as a private development version, and adds it to the machine you specify, all in one command. Use this for the inner dev loop.

**Pick a variant:**

| Command                    | What it does                                          | Use when                                                                                         |
| -------------------------- | ----------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| `viam module reload`       | Builds in the cloud, then deploys.                    | Your laptop and target machine have different architectures (for example, macOS → Raspberry Pi). |
| `viam module reload-local` | Builds locally, transfers the artifact, then deploys. | Architectures match. Faster, no cloud round-trip.                                                |

**Run it:**

Find your machine's part ID first. At the top of the machine's page, click the **Live** / **Offline** status dropdown, then click **Part ID** to copy it.

Run the command from your module's root directory (where `meta.json` lives):

```sh {class="command-line wrap" data-prompt="$"}
viam module reload --part-id <machine-part-id> --model-name my-org:my-sensor-module:my-sensor --name my-sensor-1
```

`--model-name` adds an instance of your model to the machine config (so you don't have to add it by hand), and `--name` names that instance.

**What to expect:**

- The CLI prints build progress, then upload progress, then a success line.
- The machine's **CONFIGURE** tab shows the new component (named `my-sensor-1` in the example above). Open it and set the attributes your module expects.
- The module starts within a few seconds. The **LOGS** tab shows `module my-sensor-module-private started`.
- Each subsequent code change: rerun `viam module reload` (or `reload-local`) to push a new build. Use `--no-build` to skip the build step if you already built manually, or `viam module restart` to restart the running module without rebuilding (useful for Python source edits).

For the full hot-reload walkthrough including how it fits into the dev loop, see [Test locally](/build-modules/write-a-driver-module/#3-test-locally) on the driver-module page.

When you're ready to share the module beyond the one machine you tested on, do a [versioned release](#release-a-versioned-module).

## Release a versioned module

A versioned release uploads a numbered package to the registry. Any authorized machine (across your org, or across all Viam users if the module is public) can install it. New uploads with a higher version number deploy automatically to machines tracking the latest, usually within a minute or two.

Two ways to build and upload:

- **Cloud build (recommended).** Viam compiles your module for every target platform from your GitHub repo. Triggered by tagging a release (or a manual CLI command). No local cross-compilation. Set up once, run on every release.
- **Manual upload.** You build locally and run `viam module upload`. You're responsible for cross-compiling for each target platform yourself.

Both paths share the same prep work first.

### Before you start

The page from here on assumes you ran `viam module generate` to scaffold your module. The generator creates `meta.json`, build scripts, an entrypoint, and (for cloud build) a GitHub Actions workflow. If you wrote your module from scratch and don't have these, see [Module reference](/build-modules/module-reference/) for the file formats you need to create by hand.

For cloud build you also need:

- Your module code in a GitHub repo with a `main` default branch (or pass `--ref <branch>`).
- A Viam organization API key. Create one in the Viam app at your org's **Settings** page if you don't have one already.

For manual upload you need:

- A way to build a binary for each platform you want to support. Cross-compiling from x86 to ARM (Raspberry Pi) requires `GOOS`/`GOARCH` for Go or building on the target architecture for Python (PyInstaller does not cross-compile).

### Step 1: Review meta.json

The generator creates a `meta.json` file in your module directory. Open it and review each field:

```json
{
  "module_id": "my-org:my-sensor-module",
  "visibility": "private",
  "url": "https://github.com/my-org/my-sensor-module",
  "description": "A custom sensor module that reads temperature and humidity from an HTTP endpoint.",
  "models": [
    {
      "api": "rdk:component:sensor",
      "model": "my-org:my-sensor-module:my-sensor"
    }
  ],
  "entrypoint": "run.sh",
  "build": {
    "setup": "./setup.sh",
    "build": "./build.sh",
    "path": "dist/archive.tar.gz",
    "arch": ["linux/amd64", "linux/arm64"]
  }
}
```

| Field               | Required | Purpose                                                                                                                                                                                              |
| ------------------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `$schema`           | No       | JSON Schema URL for editor validation. Set to `https://dl.viam.dev/module.schema.json`.                                                                                                              |
| `module_id`         | Yes      | Unique ID in the registry. Format: `namespace:name`.                                                                                                                                                 |
| `visibility`        | Yes      | Who can see and install the module: `private`, `public`, or `public_unlisted`.                                                                                                                       |
| `url`               | No       | Link to the source code repository. **Required for cloud build.**                                                                                                                                    |
| `description`       | Yes      | Shown in the registry UI and search results.                                                                                                                                                         |
| `models`            | No       | List of resource models the module provides. Each has `api`, `model`, and optionally `short_description` and `markdown_link`. Models can be auto-detected with `viam module update-models --binary`. |
| `entrypoint`        | Yes      | The path to the command that starts the module inside the archive.                                                                                                                                   |
| `first_run`         | No       | Path to a setup script that runs once after first install (default timeout: 1 hour).                                                                                                                 |
| `markdown_link`     | No       | Path to a README file (or `README.md#section` anchor) used as the registry description.                                                                                                              |
| `build.setup`       | No       | Script that installs build dependencies (runs once).                                                                                                                                                 |
| `build.build`       | No       | Script that compiles and packages the module.                                                                                                                                                        |
| `build.path`        | No       | Path to the packaged output archive (default: `module.tar.gz`).                                                                                                                                      |
| `build.arch`        | No       | Target platforms to build for (default: `["linux/amd64", "linux/arm64"]`).                                                                                                                           |
| `build.darwin_deps` | No       | Homebrew dependencies for macOS builds (for example, `["go", "pkg-config"]`).                                                                                                                        |

Visibility options:

- **`private`**: only your organization can see and use the module.
- **`public`**: all Viam users can see and use it. Requires your organization to have a public namespace.
- **`public_unlisted`**: any user can use the module if they know the ID, but it does not appear in registry search results.

### Step 2: Review the build scripts

The generator creates build and setup scripts. Review them and customize if your module has additional build steps (for example, compiling native extensions).

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

Make sure all scripts are executable:

```sh {class="command-line" data-prompt="$"}
chmod +x setup.sh build.sh run.sh
```

### Step 3: Document your module (recommended)

Add a README so users (or future-you) know how to configure each model. If your module is going public, a README is essential. Set `markdown_link` in `meta.json` to point the registry page at it.

For starter templates, see [README templates](#readme-templates) at the bottom of this page.

### Step 4: Build and upload

Pick one path:

#### Option A: Release with cloud build (recommended) {#release-with-cloud-build}

Cloud build is a Viam-side build service that compiles your module from your GitHub repo for every target platform listed in `meta.json`'s `build.arch`. You can trigger it two ways:

- Tag a release in GitHub. The generator's `.github/workflows/deploy.yml` workflow runs `viam module build start` for you.
- Run `viam module build start` directly from your laptop. This runs the same backend build without going through GitHub Actions.

Set up GitHub Actions once, then every tagged release deploys automatically.

**1. Push your code to GitHub.**

```sh {class="command-line" data-prompt="$"}
cd my-sensor-module
git init
git add .
git commit -m "Initial module code"
git remote add origin https://github.com/my-org/my-sensor-module.git
git push -u origin main
```

**2. Add Viam credentials as GitHub secrets.**

1. In the [Viam app](https://app.viam.com), open your organization's **Settings** page and either create or copy an existing API key with org-level access.
1. In your GitHub repository: **Settings → Secrets and variables → Actions**.
1. Add two repository secrets:
   - `VIAM_KEY_ID`: your API key ID
   - `VIAM_KEY_VALUE`: your API key value

**3. Tag a release.**

```sh {class="command-line" data-prompt="$"}
git tag v0.1.0
git push origin v0.1.0
```

**What to expect:**

- The GitHub Action starts immediately. Watch progress in the **Actions** tab of your GitHub repo. A typical first build takes 5-15 minutes (longer for the first run because dependencies aren't cached).
- When the workflow turns green, your module appears at `https://app.viam.com/registry` with the tagged version.
- If the workflow fails, click into the run for the build log. See [Cloud build fails in GitHub Actions](#cloud-build-fails-in-github-actions) below for the common causes.

To trigger a build without tagging a GitHub release (useful for testing the build pipeline before your first tagged release):

```sh {class="command-line" data-prompt="$"}
viam module build start --version 0.1.0
```

{{< alert title="Non-main default branches" color="tip" >}}
Cloud build expects your repository's default branch to be `main`. If your repository uses `master` (or another branch), pass the `--ref` flag:

```sh {class="command-line" data-prompt="$"}
viam module build start --ref master
```

{{< /alert >}}

Once cloud build is set up, jump to [Step 5](#step-5-configure-on-a-machine).

#### Option B: Release with a manual upload {#release-manually}

Use this when you can't use cloud build (no GitHub repo, restricted CI, etc.). You build locally and upload one archive per target platform.

{{< alert title="You must build for the target platform" color="caution" >}}
The binary in your archive must already be compiled for the target machine's OS and architecture. If you build on an x86 laptop and upload as `linux/arm64` without cross-compiling, the module will fail with `exec format error` on ARM machines.
{{< /alert >}}

**1. Build for each target platform:**

{{< tabs >}}
{{% tab name="Python" %}}

```sh {class="command-line" data-prompt="$"}
cd my-sensor-module
bash build.sh
```

The generated `build.sh` uses [PyInstaller](https://pypi.org/project/pyinstaller/) to compile your module into a standalone executable containing the Python interpreter and all dependencies.

{{< alert title="PyInstaller limitations" color="note" >}}

- PyInstaller does not support relative imports in entrypoints (imports starting with `.`). If you get `ImportError: attempted relative import with no known parent package`, see the [PyInstaller workaround](https://github.com/pyinstaller/pyinstaller/issues/2560).
- PyInstaller does not cross-compile. To support multiple architectures, build on each architecture or use [cloud build](#release-with-cloud-build) instead.

{{< /alert >}}

{{% /tab %}}
{{% tab name="Go" %}}

```sh {class="command-line" data-prompt="$"}
cd my-sensor-module
GOOS=linux GOARCH=arm64 go build -o dist/module cmd/module/main.go
tar -czf dist/archive.tar.gz -C dist module
```

Set `GOARCH` to match your target machine: `amd64` for x86_64, `arm64` for ARM (Raspberry Pi 4, Jetson, etc.).

{{% /tab %}}
{{< /tabs >}}

**2. Upload the archive:**

```sh {class="command-line" data-prompt="$"}
viam module upload --version=0.1.0 --platform=linux/arm64 dist/archive.tar.gz
```

**3. Repeat for each platform you want to support:**

```sh {class="command-line" data-prompt="$"}
GOOS=linux GOARCH=amd64 go build -o dist/module cmd/module/main.go
tar -czf dist/archive.tar.gz -C dist module
viam module upload --version=0.1.0 --platform=linux/amd64 dist/archive.tar.gz
```

**What to expect:**

- Each `viam module upload` prints `successfully uploaded <module-id> version <version> for <platform>` on success.
- Your module appears at `https://app.viam.com/registry` with the uploaded version. Each platform you uploaded is listed under that version.
- Before uploading, the CLI checks that the entrypoint exists in the archive, has execute permissions, and that no symlinks escape the archive. To skip these checks (not recommended for production), pass `--force`.

### Step 5: Configure on a machine {#step-5-configure-on-a-machine}

With your module in the registry, any authorized machine can use it.

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
- The **LOGS** tab shows `module <module-name> started`.
- Open the **CONTROL** tab and verify the component responds.
- If the module fails to start, the **LOGS** tab shows the error. See [Module works locally but fails after deployment](#module-works-locally-but-fails-after-deployment) below.

You're done with first deploy. From here, you can release new versions, manage who can use the module, or set platform constraints. See [After your first release](#after-your-first-release) below.

## After your first release

### Release new versions {#manage-versions}

Edit your module, commit, and tag a new version. With cloud build, pushing the tag is all that's needed:

```sh {class="command-line" data-prompt="$"}
git add .
git commit -m "Add humidity calibration offset"
git tag v0.2.0
git push origin main v0.2.0
```

For manual upload, rebuild and run `viam module upload --version=0.2.0` for each platform.

**Automatic updates:** Machines tracking the latest version pick up the new release within a few minutes. Machines pinned to a specific version stay on that version until you change the pin.

**Pin to a specific version:**

1. In the Viam app, go to the machine's **CONFIGURE** tab.
1. Find the module in the configuration.
1. Set the **Version** field to a specific version (for example, `0.1.0`).
1. Click **Save**.

For more on version management (including managing visibility, deleting modules, and choosing release branches), see [Update and manage modules](/build-modules/manage-modules/).

### Auto-detect models with `update-models`

As your module grows, you can keep `meta.json`'s `models` array in sync with your code automatically:

```sh {class="command-line" data-prompt="$"}
viam module update-models --binary ./bin/module
viam module update
```

`update-models` inspects the binary, discovers registered models, and rewrites the `models` array. `viam module update` pushes the updated metadata to the registry.

### Download a module from the registry

For inspection, debugging, or local testing of someone else's module:

```sh {class="command-line wrap" data-prompt="$"}
viam module download --id my-org:my-sensor-module --version 0.1.0 --platform linux/amd64 --destination ./downloaded-module
```

### Platform constraints

You can restrict an upload to machines that report specific platform tags. For example, to require Debian:

```sh {class="command-line" data-prompt="$"}
viam module upload --version=0.1.0 --platform=linux/amd64 --tags=distro:debian dist/archive.tar.gz
```

The machine must report a matching tag for the constrained upload to be selected. Uploads with no constraints are available to all machines on that platform.

### Upload limits

| Limit                          | Value  |
| ------------------------------ | ------ |
| Compressed package (`.tar.gz`) | 50 GB  |
| Decompressed contents          | 250 GB |
| Single file within package     | 25 GB  |

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

This means the binary was compiled for the wrong architecture. For example, you built on an x86 laptop but the target machine is ARM (Raspberry Pi).

- Use [cloud build](#release-with-cloud-build) to compile for all target platforms automatically.
- If deploying manually, cross-compile with the correct `GOOS` and `GOARCH` before uploading.
- Verify the platform flag in your `upload` command matches the binary's architecture (for example, `--platform=linux/arm64` for Raspberry Pi 4).

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
