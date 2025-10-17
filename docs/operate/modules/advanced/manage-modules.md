---
title: "Update and manage modules you created"
linkTitle: "Update and manage modules"
type: "docs"
weight: 27
images: ["/registry/create-module.svg"]
icon: true
tags: ["modular resources", "components", "services", "registry"]
description: "Update or delete your existing modules, or change their privacy settings."
aliases:
  - /use-cases/deploy-code/
  - /use-cases/manage-modules/
  - /how-tos/manage-modules/
  - /operate/modules/other-hardware/manage-modules/
languages: []
viamresources: []
platformarea: ["registry"]
level: "Beginner"
date: "2024-06-30"
# updated: ""  # When the tutorial was last entirely checked
cost: "0"
---

After you [create and upload a module](/operate/modules/create-module/), you can update, delete, or change its visibility settings.

For information on pinning module deployments to versions, see [Module versioning](/operate/modules/advanced/module-configuration/#module-versioning).

## Update a module

Once your module is in the [registry](https://app.viam.com/registry), there are two ways to update it:

- [Update automatically](#update-automatically-from-a-github-repo-with-cloud-build) using GitHub Actions: Recommended for ongoing projects with continuous integration (CI) workflows, or if you want to build for multiple platforms.

  - If you enabled cloud build when you generated your module, the GitHub Actions are already set up for you.

- [Update manually](#update-manually) using the [Viam CLI](/dev/tools/cli/): Fine for small projects with one contributor.

### Update automatically from a GitHub repo with cloud build

Use [GitHub Actions](https://docs.github.com/actions) to automatically build and deploy your new module version when you create a tag or release in GitHub:

1. Edit your module code and update the [`meta.json`](/operate/modules/advanced/metajson/) file if needed.
   For example, if you've changed the module's functionality, update the description in the `meta.json` file.

   {{% alert title="Important" color="note" %}}
   Make sure the `url` field contains the URL of the GitHub repo that contains your module code.
   This field is required for cloud build to work.
   {{% /alert %}}

1. Push your changes to your module GitHub repository.

   {{% alert title="Tip" color="tip" %}}

   If you used `viam module generate` to create your module and enabled cloud build, and you followed all the [steps to publish your module with PyInstaller](/operate/modules/create-module/#upload-your-module) including adding API keys for the build action, all you need to do to trigger a new build is create a tag and publish a release in GitHub as you did when you first published the module.

   {{% /alert %}}

1. If you did not use the Viam CLI generator and enable cloud build, you can set up one of the following GitHub Actions up manually:

   {{< tabs >}}
   {{% tab name="build-action (Recommended)" %}}

   The `build-action` GitHub action provides a cross-platform build setup for multiple platforms: x86, ARM Linux, and macOS.

   In your repository, create a workflow file called <FILE>build.yml</FILE> in the <FILE>.github/workflows<FILE> directory:

   ```yaml
   on:
     push:
       tags:
         - "[0-9]+.[0-9]+.[0-9]+"

   jobs:
     publish:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         - uses: viamrobotics/build-action@v1
           with:
             version: ${{ github.ref_name }}
             ref: ${{ github.sha }}
             key-id: ${{ secrets.viam_key_id }}
             key-value: ${{ secrets.viam_key_value }}
             token: ${{ github.token }} # only required for private git repos
   ```

The `build-action` GitHub action relies on a build command that you need to specify in the <file>meta.json</file> file.
At the end of your <file>meta.json</file>, add the build configuration:

<!-- { {< tabs >}}
{ {% tab name="Single Build File" %}} -->

```json {class="line-numbers linkable-line-numbers" data-line="5-9"}
{
  "module_id": "example-module",
  ...
  "build": {
    "setup": "./setup.sh", // optional - command for one-time setup
    "build": "./build.sh", // command that will build your module's tarball
    "path" : "dist/archive.tar.gz", // optional - path to your built module tarball
    "arch" : ["linux/amd64", "linux/arm64", "darwin/arm64"], // architecture(s) to build for
    "darwin_deps" : ["go", "x264", "nlopt-static"] // optional - Homebrew dependencies for Darwin builds. Explicitly pass `[]` for empty.
  }
}
```

{{% expand "Cloud build configuration attributes" %}}

<!-- prettier-ignore -->
| Attribute | Inclusion | Description |
| --------- | --------- | ----------- |
| `"setup"` | Optional | Command to run for setting up the build environment. |
| `"build"` | **Required** | Command to run to build the module tarball. |
| `"path"` | Optional | Path to the build module tarball. |
| `"arch"` | **Required** | Array of architectures to build for. For more information see [Supported platforms for automatic updates](#supported-platforms-for-automatic-updates). |
| `"darwin_deps"` | **Required** | Array of homebrew dependencies for Darwin builds. Explicitly pass `[]` for empty. Default: `["go", "pkg-config", "nlopt-static", "x264", "jpeg-turbo", "ffmpeg"]` |

{{% /expand %}}

{{< expand "Python module script examples" >}}

The following code snippet demonstrates an example `setup.sh` for a Python module:

```bash {class="line-numbers linkable-line-numbers"}
#!/bin/sh
cd `dirname $0`

# Create a virtual environment to run our code
VENV_NAME="venv"
PYTHON="$VENV_NAME/bin/python"
ENV_ERROR="This module requires Python >=3.8, pip, and virtualenv to be installed."

if ! python3 -m venv $VENV_NAME >/dev/null 2>&1; then
  echo "Failed to create virtualenv."
  if command -v apt-get >/dev/null; then
    echo "Detected Debian/Ubuntu, attempting to install python3-venv automatically."
    SUDO="sudo"
    if ! command -v $SUDO >/dev/null; then
      SUDO=""
    fi
  if ! apt info python3-venv >/dev/null 2>&1; then
    echo "Package info not found, trying apt update"
    $SUDO apt -qq update >/dev/null
  fi
  $SUDO apt install -qqy python3-venv >/dev/null 2>&1
  if ! python3 -m venv $VENV_NAME >/dev/null 2>&1; then
    echo $ENV_ERROR >&2
    exit 1
  fi
  else
    echo $ENV_ERROR >&2
    exit 1
  fi
fi

# remove -U if viam-sdk should not be upgraded whenever possible
# -qq suppresses extraneous output from pip
echo "Virtualenv found/created. Installing/upgrading Python packages..."
if ! [ -f .installed ]; then
  if ! $PYTHON -m pip install -r requirements.txt -Uqq; then
    exit 1
  else
    touch .installed
  fi
fi
```

The following code snippet demonstrates an example `build.sh` for a Python module:

```bash {class="line-numbers linkable-line-numbers"}
#!/bin/sh
cd `dirname $0`

# Create a virtual environment to run our code
VENV_NAME="venv"
PYTHON="$VENV_NAME/bin/python"

if ! $PYTHON -m pip install pyinstaller -Uqq; then
    exit 1
fi

$PYTHON -m PyInstaller --onefile --hidden-import="googleapiclient" src/main.py
tar -czvf dist/archive.tar.gz ./dist/main
```

{{< /expand >}}

You can test this build configuration by running the Viam CLI's [`build local` command](/dev/tools/cli/#using-the-build-subcommand) on your development machine:

```sh {class="command-line" data-prompt="$"}
viam module build local
```

The command will run your build instructions locally without running a cloud build job.

For more details, see the [`build-action` GitHub Action documentation](https://github.com/viamrobotics/build-action), or take a look through one of the following example repositories that show how to package and deploy modules using the Viam SDKs:

- [Golang CI yaml](https://github.com/viam-labs/wifi-sensor/blob/main/.github/workflows/build.yml)
- [Golang Example CI meta.json](https://github.com/viam-labs/wifi-sensor/blob/main/meta.json)
<!-- - [C++ Example CI yaml](https://github.com/viamrobotics/module-example-cpp/blob/main/.github/workflows/build2.yml)
- [C++ Example CI meta.json](https://github.com/viamrobotics/module-example-cpp/blob/main/meta.json) -->

  {{% /tab %}}
  {{% tab name="upload-module" %}}

  If you already have your own CI with access to arm runners or only intend to build on `x86` or `mac`, you can use the `upload-module` GitHub action instead which allows you to define the exact build steps.

  Add this to your GitHub workflow:

  ```yaml {class="line-numbers linkable-line-numbers"}
  on:
    push:
    release:
      types: [released]

  jobs:
    publish:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v3
        - name: build
          run: echo "your build command goes here" && false # <-- replace this with the command that builds your module's tar.gz
        - uses: viamrobotics/upload-module@v1
          # if: github.event_name == 'release' # <-- once the action is working, uncomment this so you only upload on release
          with:
            module-path: module.tar.gz
            platform: linux/amd64 # <-- replace with your target architecture, or your module will not deploy
            version: ${{ github.event_name == 'release' && github.ref_name || format('0.0.0-{0}.{1}', github.ref_name, github.run_number) }} # <-- see 'Versioning' section below for explanation
            key-id: ${{ secrets.viam_key_id }}
            key-value: ${{ secrets.viam_key_value }}
  ```

Set `run` to the command you use to build and package your module, such as invoking a makefile or running a shell script.
When you are ready to test the action, uncomment `if: github.event_name == 'release'` to enable the action to trigger a run when you [issue a release](https://docs.github.com/en/repositories/releasing-projects-on-github).

For guidance on configuring the other parameters, see the documentation for each:

- [`org-id`](/dev/tools/cli/#using-the---org-id-and---public-namespace-arguments): Not required if your module is public.
- [`platform`](/dev/tools/cli/#using-the---platform-argument): You can only upload one platform at a time.
- [`version`](https://github.com/viamrobotics/upload-module/blob/main/README.md#versioning): See [Using the --version argument](/dev/tools/cli/#using-the---version-argument) for more details on the types of versioning supported.

For more details, see the [`upload-module` GitHub Action documentation](https://github.com/viamrobotics/upload-module), or take a look through one of the following example repositories that show how to package and deploy modules using the Viam SDKs:

- [Python with virtualenv](https://github.com/viam-labs/python-example-module)
- [Python with docker](https://github.com/viamrobotics/python-container-module)
- [Golang](https://github.com/viam-labs/wifi-sensor)
- [C++](https://github.com/viamrobotics/module-example-cpp)

  {{% /tab %}}
  {{< /tabs >}}

3. [Create an organization API key](/dev/tools/cli/#create-an-organization-api-key) with owner role:

   ```sh {class="command-line" data-prompt="$"}
   viam organizations api-key create --org-id <org-id> --name <key-name>
   ```

1. Add the key ID and value as GitHub repository secrets named `viam_key_id` and `viam_key_value`.

1. Push a tag or create a [release](https://docs.github.com/en/repositories/releasing-projects-on-github) in GitHub to trigger the build.
   The build can be quick or take over 15 minutes to complete, depending on factors including the size of the module.

   Once the build is complete, the module will automatically update in the [registry](https://app.viam.com/registry), and the machines set to use the latest [version](/operate/modules/advanced/module-configuration/#module-versioning) of the module will automatically update to the new version.

#### Supported platforms for automatic updates

When using cloud build, you can specify which platforms you want to build your module for in the `arch` field of your `meta.json` file.
The following table lists all available platforms:

<!-- prettier-ignore -->
| Platform | Supported in cloud build | Container used by cloud build | Notes |
|----------|--------------------------|------------------------------|-------|
| `linux/amd64` | ✅ | Ubuntu | Standard x86_64 Linux platform. |
| `linux/arm64` | ✅ | Ubuntu | For ARM64 Linux devices like Raspberry Pi 4. |
| `darwin/arm64` | ✅ | macOS | For Apple Silicon Macs (M1/M2/M3). |
| `linux/arm32v6` | ❌ | N/A | For older ARM devices; must be built manually. |
| `linux/arm32v7` | ❌ | N/A | For 32-bit ARM devices; must be built manually. |
| `windows/amd64` | ⚠️ | N/A | <ul><li>Cloud builds work for Go modules but have issues linking to C libraries.</li><li>Windows support is still in development.</li></ul> |
| `darwin/amd64` | ❌ | N/A | Intel Macs; must be built manually. You can choose to support it, though many modules do not since Apple is phasing out this platform. |

{{% alert title="Note" color="note" %}}
While the registry supports additional platforms like `windows/amd64`, `linux/arm32v6`, and `linux/arm32v7`, these are not currently supported by cloud build and must be [built and uploaded manually](#update-manually).
{{% /alert %}}

### Update manually

Use the [Viam CLI](/dev/tools/cli/) to manually update your module:

1. Edit your module code and update the [`meta.json`](/operate/modules/advanced/metajson/) file if needed.
   For example, if you've changed the module's functionality, update the description in the `meta.json` file.

2. For Python modules only, package your files as an archive, for example:

   ```sh {class="command-line" data-prompt="$"}
   tar -czf module.tar.gz run.sh requirements.txt src meta.json
   ```

   Supply the path to the resulting archive file in the next step.

3. Upload to the Viam Registry:

   ```sh {class="command-line" data-prompt="$"}
   viam module upload --version <version> --platform <platform> <module-path>
   ```

   For example, `viam module upload --version 1.0.1 --platform darwin/arm64 my-module.tar.gz`.

When you `upload` a module, the command performs basic [validation](/dev/tools/cli/#upload-validation) of your module to check for common errors.

For more information, see the [`viam module` command](/dev/tools/cli/#module).

## Change module visibility

You can change the visibility of a module from public to private if:

- you are an [owner](/manage/manage/rbac/) of the {{< glossary_tooltip term_id="organization" text="organization" >}} that owns the module, AND
- no machines outside of the organization that owns the module have the module configured (no other orgs are using it).

To change the visibility:

1. Navigate to your module's page in the [registry](https://app.viam.com/registry).
2. Hover to the right of the visibility indicator near the right side of the page until an **Edit** button appears, and click it to make changes.

   {{<imgproc src="/registry/upload/edit-module-visibility.png" resize="x150" declaredimensions=true alt="A module page with a Visibility heading on the right side. Under it, an Edit button has appeared." class="shadow" >}}

   The options are:

   - **Private**: Only users inside your organization can view, use, and edit the module.
   - **Public**: Any user inside or outside of your organization can view, use, and edit the module.
   - **Unlisted**: Any user inside or outside of your organization, with a direct link, can view and use the module.
     Only organization members can edit the module.
     Not listed in the registry for users outside of your organization.

You can also edit the visibility by editing the [meta.json](/operate/modules/advanced/metajson/) file and then running the following [CLI](/dev/tools/cli/#module) command:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam module update
```

{{% hiddencontent %}}
If you don't see a private module of yours in the registry, make sure that you have the correct organization selected in the upper right corner of the page.
{{% /hiddencontent %}}

## Delete a module

You can delete a module if:

- you are an [owner](/manage/manage/rbac/) in the {{< glossary_tooltip term_id="organization" text="organization" >}} that owns the module, AND
- no machines have the module configured.

To delete a module:

1. Navigate to its page in the [registry](https://app.viam.com/registry).
2. Click the **...** menu in the upper-right corner of the page, and click **Delete**.

   {{<imgproc src="/registry/upload/delete-module.png" resize="x200" declaredimensions=true alt="A module page with the ... menu open. Delete is the only option in the menu." class="shadow" >}}

{{% alert title="Note" color="note" %}}

If you need to delete a module and the delete option is unavailable to you, please [contact our support team](mailto:contact@viam.com) for assistance.

{{% /alert %}}

{{% hiddencontent %}}
Other registry items such as training scripts and ML models can be deleted in the same way as modules.
{{% /hiddencontent %}}

### Delete just one version of a module

Deleting a version of a module requires the same org owner permissions as deleting the entire module, and similarly, you cannot delete a version if any machines are using it.
To delete just one version of a module:

1. Navigate to its page in the [registry](https://app.viam.com/registry).

1. Click **Show previous versions** under the **Latest version** heading.

1. Hover on the architecture pill next to the version you'd like to delete and click the trash icon.

You cannot upload a new file with the same version number as the deleted one.
To upload another version, you must increment the version number to a later version number.

## Transfer ownership of a module

To transfer ownership of a module from one organization to another:

1. You must be an [owner](/manage/manage/rbac/) in both the current and new organizations.

1. Navigate to the module's page in the [registry](https://app.viam.com/registry).

1. Make sure the visibility of the module is set to **Public**.

1. Click the **...** menu in the upper-right corner of the page, and click **Transfer ownership**.

1. Select the new organization from the dropdown menu, then click **Transfer module**.

1. (Recommended) Transfer the GitHub repository containing the module code to the new owner.
   Be sure to remove the existing secrets from the repository's settings before transferring.
   If the repository is using Viam's cloud build, the secrets contain an organization API key that will be exposed to the new owner after the repository transfer.

1. Update the `meta.json` file to reflect the new organization:

   - Change the first part of the `module_id` field to the new organization's [namespace](/operate/modules/advanced/naming-modules/#create-a-namespace-for-your-organization).
   - For each model, change the first part of the `model` field to the new organization's namespace.
   - Update the `url` field to point to the new code repository if it has moved.

1. Update the module code:

   - Throughout your module implementation code, change the model names in your component or service classes to match the changes you made to the `meta.json` file.

1. Publish a new version of the module to the registry by following either set of update steps on this page.
   This ensures that the model names in the module code match the registered model names in the registry.

1. (Recommended) Update the `model` field in the configuration of any machines that use the module to use the new organization's namespace.
   Viam maintains backwards compatibility with the old namespace, but you should update the configuration to use the new namespace to avoid confusion.

## Rename a module

You can rename a module that your organization owns through the Viam web interface.
To rename a module:

1. Navigate to your module page at `app.viam.com/module/<namespace>/<module-name>`.
1. Click the **...** menu in the top right corner of the module page.
1. Select **Rename** from the dropdown menu.
1. Enter the new module name in the modal that appears.
1. Click **Rename** to confirm the change.

When you rename a module, Viam reserves the old module name for backwards compatibility and you cannot reuse it.

Existing machine configurations containing the old module name will continue to work.

{{% hiddencontent %}}

## Rename a model

If you need to change the name of a model that a module implements, do the following:

1. Update the `model` field in the `meta.json` file to the new model name.

1. Update the model name in the module code to match the new model name.

1. Publish a new version of the module to the registry by following either set of update steps on this page.

1. (Recommended) Update the configuration of any machines that use the module to use the new model name.
   Viam maintains backwards compatibility with the old model name, but updating the configuration is recommended to avoid confusion.

{{% /hiddencontent %}}
