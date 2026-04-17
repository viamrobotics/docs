---
linkTitle: "Deploy a module"
title: "Deploy a module"
weight: 30
layout: "docs"
type: "docs"
description: "Package, upload, and distribute a module through the Viam registry."
date: "2025-01-30"
aliases:
  - /build/development/deploy-a-module/
  - /development/deploy-a-module/
  - /extend/modular-resources/upload/
  - /modular-resources/upload/
  - /registry/upload/
  - /how-tos/upload-module/
---

A module that only runs locally on your development machine is useful for testing
but limits what you can do. Deploying through the Viam module registry lets you:

- **Install on any machine** in your organization (or publicly) through the
  Viam app -- no SSH or manual file copying.
- **Update over the air** -- release a new version and machines pick it up
  automatically within minutes.
- **Target multiple platforms** -- cloud build compiles for every architecture
  you need so you don't have to cross-compile locally.

For background on the module registry, versioning, and cloud builds, see the
[overview](/build-modules/overview/#the-module-registry).

## Steps

### 1. Review meta.json

The generator creates a `meta.json` file in your module directory. Open it and
review each field:

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
| `url`               | No       | Link to the source code repository. Required for cloud builds.                                                                                                                                       |
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

- **`private`** -- only your organization can see and use the module.
- **`public`** -- all Viam users can see and use it. Requires your organization
  to have a public namespace.
- **`public_unlisted`** -- any user can use the module if they know the ID, but
  it does not appear in registry search results.

Common `api` values:

- `rdk:component:sensor` for sensors
- `rdk:component:camera` for cameras
- `rdk:component:motor` for motors
- `rdk:component:generic` for generic components
- `rdk:service:vision` for vision services

### 2. Review the generated build scripts

The generator creates build and setup scripts for your module. Review them
and customize if needed:

{{< tabs >}}
{{% tab name="Python" %}}

| File       | Purpose                                              |
| ---------- | ---------------------------------------------------- |
| `setup.sh` | Installs Python dependencies from `requirements.txt` |
| `build.sh` | Packages the module into a `.tar.gz` archive         |
| `run.sh`   | Entrypoint script that starts the module             |

If your module has additional build steps (for example, compiling native extensions),
add them to `build.sh`.

{{% /tab %}}
{{% tab name="Go" %}}

| File       | Purpose                                                               |
| ---------- | --------------------------------------------------------------------- |
| `setup.sh` | Installs build dependencies (Go modules are typically self-contained) |
| `build.sh` | Cross-compiles the binary and packages it into a `.tar.gz` archive    |
| `Makefile` | Local build targets                                                   |

The generated `build.sh` uses `GOOS` and `GOARCH` environment variables to
cross-compile for the target platform. Cloud build sets these automatically.

{{% /tab %}}
{{< /tabs >}}

Make sure all scripts are executable:

```bash
chmod +x setup.sh build.sh run.sh
```

### 3. Write a README (recommended)

Document your module and its models so users know how to configure and use
them. If you plan to make your module public, a good README is essential.

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

You can point your module's registry page to a README by setting the
`markdown_link` field in `meta.json` to a file path (for example, `README.md`) or a
section anchor (for example, `README.md#my-sensor`).

### 4. Deploy with cloud build (recommended)

Cloud build is the recommended way to deploy modules. It uses GitHub Actions to
compile your module for every target platform automatically, so you don't need
to cross-compile locally.

The generator creates the workflow file at
`.github/workflows/deploy.yml`. To use it:

**Push your code to GitHub:**

```bash
cd my-sensor-module
git init
git add .
git commit -m "Initial module code"
git remote add origin https://github.com/my-org/my-sensor-module.git
git push -u origin main
```

**Add Viam credentials as GitHub secrets:**

1. In the [Viam app](https://app.viam.com), go to your organization's settings.
2. Create an API key with organization-level access (or use an existing one).
3. In your GitHub repository, go to **Settings > Secrets and variables >
   Actions**.
4. Add two secrets:
   - `VIAM_KEY_ID` -- your API key ID
   - `VIAM_KEY_VALUE` -- your API key

**Tag a release to trigger the build:**

```bash
git tag v0.1.0
git push origin v0.1.0
```

The GitHub Action runs automatically. Monitor progress in the **Actions** tab
of your GitHub repository. When it completes, your module is in the registry
and ready to install on any machine.

You can also trigger a cloud build from the CLI:

```bash
viam module build start
```

{{< alert title="Non-main default branches" color="tip" >}}
Cloud build expects your repository's default branch to be `main`. If your
repository uses a different default branch (for example, `master`), use the `--ref`
flag:

```bash
viam module build start --ref master
```

{{< /alert >}}

### 5. Deploy manually (alternative)

If you cannot use cloud build, you can build and upload from the command line.

{{< alert title="You must build for the target platform" color="caution" >}}
When you upload manually, the binary in your archive must already be compiled
for the target machine's OS and architecture. If you build on an x86 laptop
and upload for `linux/arm64` without cross-compiling, the module will fail
with an exec format error on ARM machines (like Raspberry Pi).

Cloud build handles this automatically. If you deploy manually, you must
cross-compile yourself or build on a machine with the target architecture.
{{< /alert >}}

**Build locally:**

{{< tabs >}}
{{% tab name="Python" %}}

```bash
cd my-sensor-module
bash build.sh
```

The generated `build.sh` uses [PyInstaller](https://pypi.org/project/pyinstaller/)
to compile your module into a standalone executable containing the Python
interpreter and all dependencies.

{{< alert title="PyInstaller limitations" color="note" >}}

- PyInstaller does not support relative imports in entrypoints (imports
  starting with `.`). If you get `"ImportError: attempted relative import with
no known parent package"`, see the
  [PyInstaller workaround](https://github.com/pyinstaller/pyinstaller/issues/2560).
- PyInstaller does not support cross-compilation. Use
  [cloud build](#4-deploy-with-cloud-build-recommended) to build for multiple
  architectures automatically.
  {{< /alert >}}

{{% /tab %}}
{{% tab name="Go" %}}

```bash
cd my-sensor-module
# Cross-compile for the target platform
GOOS=linux GOARCH=arm64 go build -o dist/module cmd/module/main.go
tar -czf dist/archive.tar.gz -C dist module
```

Set `GOARCH` to match your target machine: `amd64` for x86_64, `arm64` for
ARM (Raspberry Pi 4, Jetson, etc.).

{{% /tab %}}
{{< /tabs >}}

**Upload to the registry:**

```bash
viam module upload \
    --version=0.1.0 \
    --platform=linux/arm64 \
    dist/archive.tar.gz
```

To support multiple platforms, cross-compile and upload once per platform:

```bash
# Build and upload for amd64
GOOS=linux GOARCH=amd64 go build -o dist/module cmd/module/main.go
tar -czf dist/archive.tar.gz -C dist module
viam module upload --version=0.1.0 --platform=linux/amd64 dist/archive.tar.gz

# Build and upload for arm64
GOOS=linux GOARCH=arm64 go build -o dist/module cmd/module/main.go
tar -czf dist/archive.tar.gz -C dist module
viam module upload --version=0.1.0 --platform=linux/arm64 dist/archive.tar.gz
```

### 6. Configure the module on a machine

Once your module is in the registry, any machine in your organization can use it.

1. In the [Viam app](https://app.viam.com), navigate to your machine's
   **CONFIGURE** tab.
2. Click **+** and select **Configuration block**.
3. Search for your module by name or browse the registry.
4. Add the module and create a component (or service) instance.
5. Name the component and configure the attributes your module expects:

```json
{
  "source_url": "https://api.example.com/sensor/data"
}
```

7. Click **Save**.

`viam-server` downloads the module from the registry, starts it, and makes the
component available. Test it from the **CONTROL** tab.

### 7. Manage versions

**Release a new version:**

```bash
git add .
git commit -m "Add humidity calibration offset"
git tag v0.2.0
git push origin main v0.2.0
```

If using cloud build, the workflow runs automatically. For manual upload:

```bash
viam module upload --version=0.2.0 --platform=linux/amd64 dist/archive.tar.gz
```

**Automatic updates:** By default, machines track the latest version. When you
upload `v0.2.0`, all machines update automatically within a few minutes.

**Pin to a specific version:**

1. In the Viam app, go to the machine's **CONFIGURE** tab.
2. Find the module in the configuration.
3. Set the **Version** field to the specific version (for example, `0.1.0`).
4. Click **Save**.

**View module details:**

You can view version history and details for your module in the
[Viam registry](https://app.viam.com/registry).

### 8. Keep meta.json in sync with your code

As you add models to your module, you can auto-detect them from a built binary
instead of editing `meta.json` by hand:

```bash
viam module update-models --binary ./bin/module
```

This inspects the binary, discovers registered models, and updates the `models`
array in `meta.json`.

Then push the updated metadata to the registry:

```bash
viam module update
```

### 9. Download a module

To download a module from the registry (for testing or inspection):

```bash
viam module download --id my-org:my-sensor-module --version 0.1.0 --platform linux/amd64 --destination ./downloaded-module
```

### Platform constraints

When uploading, you can attach platform constraint tags that restrict which
machines can use a particular upload. For example, to require Debian:

```bash
viam module upload \
    --version=0.1.0 \
    --platform=linux/amd64 \
    --tags=distro:debian \
    dist/archive.tar.gz
```

The machine must report matching platform tags for the constrained upload to be
selected. If no constraints are specified, the upload is available to all
machines on that platform.

### Upload limits

The registry enforces these size limits:

| Limit                          | Value  |
| ------------------------------ | ------ |
| Compressed package (`.tar.gz`) | 50 GB  |
| Decompressed contents          | 250 GB |
| Single file within package     | 25 GB  |

Before uploading, the CLI validates that:

- The entrypoint executable exists in the archive
- The entrypoint has execute permissions
- No symlinks escape the archive boundaries

Use `--force` to skip these checks (not recommended for production uploads).

## Try It

1. Review the generated `meta.json` and build scripts in your module directory.
2. Push your code to GitHub and add the Viam API key secrets.
3. Tag a release (`v0.1.0`) to trigger a cloud build.
4. Navigate to a machine in the Viam app and add your module from the registry.
5. Configure a component and set the required attributes.
6. Open the **CONTROL** tab and verify the component works.
7. Tag a new release (`v0.2.0`) and verify the machine picks it up
   automatically within a few minutes.

## Troubleshooting

{{< expand "Upload fails with \"not authenticated\"" >}}

- Log in to the Viam CLI: `viam login`.
- If using an API key, verify it has organization-level access.
- Check that `VIAM_KEY_ID` and `VIAM_KEY_VALUE` are set correctly in your GitHub
  secrets (for cloud build).

{{< /expand >}}

{{< expand "Upload fails with \"invalid meta.json\"" >}}

- Verify `meta.json` is valid JSON. Run `python -m json.tool meta.json` or
  `jq . meta.json` to check.
- Confirm the `module_id` matches the format `namespace:module-name`.
- Ensure all model entries have both `api` and `model` fields.

{{< /expand >}}

{{< expand "Module not appearing in the registry" >}}

- Check the module's visibility. If it is `private`, it only appears for users
  in your organization.
- Verify the upload completed successfully.
- The module may take a minute to propagate. Refresh the page and try again.

{{< /expand >}}

{{< expand "Machine cannot find the module" >}}

- Verify the module version supports the machine's platform. If your machine
  runs `linux/arm64` but you only uploaded for `linux/amd64`, the machine
  cannot use it.
- Check the module version. If the machine is pinned to a nonexistent version,
  it will fail.
- Confirm the machine is online and connected to the cloud.

{{< /expand >}}

{{< expand "Cloud build fails in GitHub Actions" >}}

- Check the Actions tab in your GitHub repository for the build log.
- If your repository's default branch is not `main` (for example, it uses `master`),
  use `viam module build start --ref master`. The cloud build system expects
  `main` by default.
- Verify your `setup.sh` and `build.sh` scripts work locally.
- Confirm the `build.path` in `meta.json` matches the actual output location.
- Ensure the GitHub secrets are set and not expired.

{{< /expand >}}

{{< expand "Exec format error on target machine" >}}

This means the binary was compiled for the wrong architecture. For example,
you built on an x86 laptop but the target machine is ARM (Raspberry Pi).

- Use [cloud build](#4-deploy-with-cloud-build-recommended) to compile for all
  target platforms automatically.
- If deploying manually, cross-compile with the correct `GOOS` and `GOARCH`
  before uploading. See [Deploy manually](#5-deploy-manually-alternative).
- Verify the platform flag in your `upload` command matches the binary's
  architecture (for example, `--platform=linux/arm64` for Raspberry Pi 4).

{{< /expand >}}

{{< expand "Module works locally but fails after deployment" >}}

- Check for hard-coded paths, missing environment variables, or dependencies
  installed on your machine but not in the build environment.
- For Python, verify all dependencies are in `requirements.txt`.
- For Go, verify the binary is compiled for the correct target architecture.
- Check the module logs in the **LOGS** tab.

{{< /expand >}}
