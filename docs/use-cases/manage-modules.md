---
title: "How to manage modules you created"
linkTitle: "Manage modules"
type: "docs"
weight: 26
images: ["/registry/create-module.svg"]
tags: ["modular resources", "components", "services", "registry"]
description: "Update or delete your existing modules."
aliases:
  - /use-cases/deploy-code/
---

After you [create and deploy a module](/use-cases/create-module/), you may need to update or delete it.

{{% alert title="In this page" color="tip" %}}

- [Update an existing module](#update-an-existing-module)
- [Change the privacy settings of a module](#change-a-module-from-public-to-private)
- [Delete a module](#delete-a-module)

{{% /alert %}}

For information on pinning module deployments to versions, see [Configuring version update management for a registry module](/registry/configure/#configure-version-update-management-for-a-registry-module).

## Update an existing module

You can update an existing module in the [Viam registry](https://app.viam.com/registry) in one of two ways:

- [Upload new versions of your module manually](#update-an-existing-module-using-the-viam-cli) using the [Viam CLI](/cli/).
- [Automatically upload new versions of your module on release](#update-an-existing-module-using-a-github-action) as part of a continuous integration (CI) workflow, using a GitHub action.

Updating your module manually is appropriate for smaller projects, especially those with only one contributor.
Updating your module automatically using CI is better suited for larger, ongoing projects, especially those with multiple contributors.

### Update an existing module using the Viam CLI

To update an existing module in the [Viam registry](https://app.viam.com/registry) manually, you can use the [Viam CLI](/cli/).

{{% alert title="Tip" color="tip" %}}
If you intend to make frequent code changes to your module, want to support a variety of platforms, or otherwise want to streamline your module development workflow, consider [using a GitHub action to update your module](#update-an-existing-module-using-a-github-action) instead.
{{% /alert %}}

1. Edit your custom module code with the changes you'd like to make.

1. Update your custom module's `meta.json` file with any needed changes.
   For example, if you have altered your model's description, or adjusted the endpoint name, you'll need to update `meta.json` with these changes.

1. For modules written in Python, you should package your module files as an archive first, before uploading.
   Other languages can proceed to the next step to upload their module directly.
   To package a module written in Python, run the following command from the same directory as your `meta.json` file:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   tar -czf module.tar.gz <PATH-TO-EXECUTABLE>
   ```

   Where `<PATH-TO-EXECUTABLE>` is your [packaged executable](/use-cases/create-module/#compile-or-package-your-module).

   Supply the path to the resulting archive file in the next step.

1. Run `viam module upload` to upload your custom module to the Viam registry:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   viam module upload --version <version> --platform <platform> <module-path>
   ```

   For example, the following command uploads a module compressed as an archive named `my-module.tar.gz` to the Viam registry, and increments the [`version`](/cli/#using-the---version-argument) of the module to version `1.0.1`:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   viam module upload --version 1.0.1 --platform darwin/arm64 my-module.tar.gz
   ```

   When you `upload` a module, the command performs basic [validation](/cli/#upload-validation) of your module to check for common errors.

For more information, see the [`viam module` command](/cli/#module).

### Update an existing module using a GitHub action

To update an existing module in the [Viam registry](https://app.viam.com/registry) using continuous integration (CI), you can use one of two GitHub actions.
You can only use these GitHub actions if you have already created the module by running `viam module create` and `viam module update`.
For most use cases, we recommend the [`build-action` GitHub action](https://github.com/viamrobotics/build-action) which provides a simple cross-platform build setup for multiple platforms: x86, ARM Linux, and MacOS.
However, if you already have your own CI with access to arm runners or only intend to build on `x86` or `mac`, you may also use the [`upload-module` GitHub action](https://github.com/viamrobotics/upload-module) instead which allows you to define the exact build steps.

1. Edit your custom module with the changes you'd like to make.

1. Navigate to the **Actions** tab of the GitHub repository you are using for your module code.
   If you have already created GitHub actions for this repository, click the **New workflow** button to create a new one.
   If you have not yet created any GitHub actions, click the **Set up a workflow yourself** link.
   See the [GitHub actions documentation](https://docs.github.com/en/actions/creating-actions) for more information.

1. Paste one of the following action templates into the edit window, depending on whether you are using the `build-action` or `upload-module` action:

{{< tabs >}}
{{% tab name="CI with build-action" %}}

```yaml {class="line-numbers linkable-line-numbers"}
# see https://github.com/viamrobotics/build-action for help
on:
  push:
    tags:
      - "[0-9]+.[0-9]+.[0-9]+" # the build-action will trigger on tags with the format 1.0.0

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: viamrobotics/build-action@v1
        with:
          # note: you can replace this line with 'version: ""' if
          # you want to test the build process without deploying
          version: ${{ github.ref_name }}
          ref: ${{ github.sha }}
          key-id: ${{ secrets.viam_key_id }}
          key-value: ${{ secrets.viam_key_value }}
```

The `build-action` GitHub action relies on a build command that you need to specify in the <file>meta.json</file> file that you created for your module when you first [uploaded it](/use-cases/create-module/#upload-your-module-to-the-modular-resource-registry).
At the end of your <file>meta.json</file>, add the build configuration:

<!-- { {< tabs >}}
{ {% tab name="Single Build File" %}} -->

```json {class="line-numbers linkable-line-numbers" data-line="4-7"}
{
  "module_id": "example-module",
  ...
  "build": {
    "setup": "./setup.sh", // optional - command to install your build dependencies
    "build": "./build.sh", // command that will build your module
    "path" : "dist/archive.tar.gz", // optional - path to your built module
    "arch" : ["linux/amd64", "linux/arm64"] // architecture(s) to build for
  }
}
```

{{%expand "Click to view example setup.sh" %}}

```sh { class="command-line"}
#!/bin/bash
set -e
UNAME=$(uname -s)

if [ "$UNAME" = "Linux" ]
then
    echo "Installing venv on Linux"
    sudo apt-get install -y python3-venv
fi
if [ "$UNAME" = "Darwin" ]
then
    echo "Installing venv on Darwin"
    brew install python3-venv
fi

python3 -m venv .venv
. .venv/bin/activate
pip3 install -r requirements.txt
```

{{% /expand%}}

{{%expand "Click to view example build.sh (with setup.sh)" %}}

```sh { class="command-line"}
#!/bin/bash
pip3 install -r requirements.txt
python3 -m PyInstaller --onefile --hidden-import="googleapiclient" src/main.py
tar -czvf dist/archive.tar.gz <PATH-TO-EXECUTABLE>
```

{{% /expand%}}

{{%expand "Click to view example build.sh (without setup.sh)" %}}

```sh { class="command-line"}
#!/bin/bash
set -e
UNAME=$(uname -s)

if [ "$UNAME" = "Linux" ]
then
    echo "Installing venv on Linux"
    sudo apt-get install -y python3-venv
fi
if [ "$UNAME" = "Darwin" ]
then
    echo "Installing venv on Darwin"
    brew install python3-venv
fi

python3 -m venv .venv
. .venv/bin/activate
pip3 install -r requirements.txt
python3 -m PyInstaller --onefile --hidden-import="googleapiclient" src/main.py
tar -czvf dist/archive.tar.gz <PATH-TO-EXECUTABLE>
```

{{% /expand%}}

<!-- { {% /tab %}}
{ {% tab name="Platform Specific" %}}

```json {class="line-numbers linkable-line-numbers" data-line="4-13"}
{
  "module_id": "example-module",
  ...
  "build": {
    "arch": {
          "linux/arm64": {
            "path" : "dist/archive.tar.gz",               // optional - path to your built module
            "build": "./build-linux-arm64.sh" // command that will build your module
          },
          "darwin/arm64": {
            "build": "./build-darwin-arm64.sh" // command that will build your module
          }
        } // architecture(s) to build for
  }
}
```

{ {%expand "Click to view example build-linux-arm64.sh" %}}

```sh { class="command-line"}
#!/bin/bash
set -e

sudo apt-get install -y python3-venv
python3 -m venv .venv
. .venv/bin/activate
pip3 install -r requirements.txt
python3 -m PyInstaller --onefile --hidden-import="googleapiclient" src/main.py
tar -czvf dist/archive.tar.gz <PATH-TO-EXECUTABLE>
```

{ {% /expand%}}

{{ %expand "Click to view example build-darwin-arm64.sh" %}}

```sh { class="command-line"}
#!/bin/bash
set -e

brew install python3-venv
python3 -m venv .venv
. .venv/bin/activate
pip3 install -r requirements.txt
python3 -m PyInstaller --onefile --hidden-import="googleapiclient" src/main.py
tar -czvf dist/archive.tar.gz <PATH-TO-EXECUTABLE>
```

{ {% /expand%}}

{ {% /tab %}}
{ {< /tabs >}} -->

You can test this build configuration by running the Viam CLI's [`build local` command](/cli/#using-the-build-subcommand) on your development machine:

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
{{% tab name="CI with upload-action" %}}

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

Edit the copied code to include the configuration specific to your module.
Each item marked with a `<--` comment requires that you edit the configuration values accordingly.

Set `run` to the command you use to build and package your module, such as invoking a makefile or running a shell script.
When you are ready to test the action, uncomment `if: github.event_name == 'release'` to enable the action to trigger a run when you [issue a release](https://docs.github.com/en/repositories/releasing-projects-on-github).

For guidance on configuring the other parameters, see the documentation for each:

- [`org-id`](/cli/#using-the---org-id-and---public-namespace-arguments): Not required if your module is public.
- [`platform`](/cli/#using-the---platform-argument): You can only upload one platform at a time.
- [`version`](https://github.com/viamrobotics/upload-module/blob/main/README.md#versioning): Also see [Using the --version argument](/cli/#using-the---version-argument) for more details on the types of versioning supported.

For more details, see the [`upload-module` GitHub Action documentation](https://github.com/viamrobotics/upload-module), or take a look through one of the following example repositories that show how to package and deploy modules using the Viam SDKs:

- [Python with virtualenv](https://github.com/viam-labs/python-example-module/blob/main/.github/workflows/main.yml)
- [Python with docker](https://github.com/viamrobotics/python-container-module/blob/main/.github/workflows/deploy.yml)
- [Golang](https://github.com/viam-labs/wifi-sensor/blob/main/.github/workflows/deploy.yml)

{{% /tab %}}
{{< /tabs >}}

4. Create an [organization API key](/cli/#create-an-organization-api-key) with the [owner](/cloud/rbac/#permissions) role, which the GitHub action will use to authenticate to the Viam platform, using one of the following methods:

   - Use the Viam CLI to create an organization API key, which includes the owner role by default:

     ```sh {class="command-line" data-prompt="$"}
     viam organizations api-key create --org-id <org-id> --name <key-name>
     ```

   - Use the organizations page on the [Viam app](https://app.viam.com/) to generate a new organization API key.
     Make sure your organization API key is set to **Role: Owner**, or the GitHub action will not be able to successfully authenticate during runs.
     If you are using an existing organization API key which is not set to **Role: Owner**, you can change an API key's permissions from the Viam app on the organizations page by clicking the **Show details** link next to your API key.
     The operator role cannot be used to authenticate GitHub action runs.
     For more information see [Manage organizations](/cloud/organizations/).

   Both methods return a `key id` and a `key value` which together comprise your organization API key.

1. Then, configure your GitHub repository to use your organization API key to authenticate during GitHub action runs, following the steps below:

   1. In the GitHub repository for your project, select **Settings**, then **Secrets and variables**, then **Actions**.

   1. Click the green **New repository secret** button, enter `viam_key_id` as the **NAME**, paste the value for `key id` from above into the **Secret** text field, then click **Add secret**.

   1. Then, click the green **New repository secret** button, enter `viam_key_value` as the **NAME**, paste the value for `key value` from above into the **Secret** text field, then click **Add secret**.

   For more information on GitHub secrets, see the GitHub documentation for [creating secrets for a repository](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions#creating-secrets-for-a-repository).

1. Push a tag to your repo or [create a new release](https://docs.github.com/en/repositories/releasing-projects-on-github).
   The specific step to take to release your software depends on your CI workflow, your GitHub configuration, and the `run` step you defined earlier.
   Once complete, your module will upload to the [Viam registry](https://app.viam.com/registry) with the appropriate version automatically.

For more details, see the [`upload-module` GitHub Action documentation](https://github.com/viamrobotics/upload-module), or take a look through one of the following example repositories that show how to package and deploy modules using the Viam SDKs:

- [Python with virtualenv](https://github.com/viam-labs/python-example-module)
- [Python with docker](https://github.com/viamrobotics/python-container-module)
- [Golang](https://github.com/viam-labs/wifi-sensor)
- [C++](https://github.com/viamrobotics/module-example-cpp)

## Change a module from public to private

You can change the visibility of a module from public to private if:

- you are an [owner](/cloud/rbac/) in the {{< glossary_tooltip term_id="organization" text="organization" >}} that owns the module, AND
- no machines outside of the organization that owns the module have the module configured (no other orgs are using it).

To change the visibility, navigate to its page in the [**REGISTRY** section of the Viam app](https://app.viam.com/registry), hover to the right of the visibility indicator near the right side of the page until an **Edit** button appears, and click it to make changes.

{{<imgproc src="/registry/upload/edit-module-visibility.png" resize="x1000" declaredimensions=true alt="A module page with a Visibility heading on the right side. Under it, an Edit button has appeared." max-width="700px" >}}

You can also edit the visibility by editing the <file>meta.json</file> file and then running the following [CLI](/cli/#module) command:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam module update
```

## Delete a module

You can delete a module if:

- you are an [owner](/cloud/rbac/) in the {{< glossary_tooltip term_id="organization" text="organization" >}} that owns the module, AND
- no machines have the module configured.

To delete a module, navigate to its page in the [**REGISTRY** section of the Viam app](https://app.viam.com/registry), click the **...** menu in the upper-right corner of the page, and click **Delete**.

{{<imgproc src="/registry/upload/delete-module.png" resize="x1000" declaredimensions=true alt="A module page with the ... menu open. Delete is the only option in the menu." max-width="700px" >}}

{{% alert title="Note" color="note" %}}

If you need to delete a module and the delete option is unavailable to you, please [contact our support team](https://support.viam.com/hc/en-us) for assistance.

{{% /alert %}}

### Delete just one version of a module

Deleting a version of a module requires the same org owner permissions as deleting the entire module, and similarly, you cannot delete a version if any machines are using it.
To delete just one version of a module:

1. Navigate to its page in the [**REGISTRY** section of the Viam app](https://app.viam.com/registry)
2. Click **Show previous versions** under the **Latest version** heading.
3. Click the trash can icon next to the version you'd like to delete.

Versions are immutable, meaning that you cannot upload a new file with the same version number as the deleted one.
To upload another version, you must increment the version number to a later version number.
