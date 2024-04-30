---
title: "Upload your Own Modules to the Viam Registry"
linkTitle: "Upload your module"
weight: 20
type: "docs"
tags:
  [
    "server",
    "rdk",
    "extending viam",
    "modular resources",
    "components",
    "services",
  ]
description: "Use the Viam CLI to upload a custom module to the Viam registry as a public module or as a private module that is shared only within your organization."
no_list: true
icon: true
images: ["/registry/upload-module.svg"]
aliases:
  - "/extend/modular-resources/upload/"
  - "/modular-resources/upload/"
---

Once you have [created a custom module](/registry/create/), use the instructions on this page to upload it to the Viam registry as a public module that is shared with other Viam users, or as a private module that is shared only within your [organization](/fleet/organizations/).

You can upload your module in one of two ways:

- You can [upload your module using the Viam CLI](#upload-a-custom-module-using-the-cli), ideal for testing or on-demand releases.
  You can also [update your module using the CLI](#update-an-existing-module) to push code changes as needed.
- You can [use a GitHub Action to automatically upload your module when you make a new GitHub release](#update-an-existing-module-using-a-github-action), ideal for continuous integration (CI) pipelines.

## Upload a custom module using the CLI

To upload your custom module to the [Viam registry](https://app.viam.com/registry), either as a public or private module, use the Viam CLI commands `create` and `upload` following these instructions:

1. First, [install the Viam CLI](/fleet/cli/#install) and [authenticate](/fleet/cli/#authenticate) to Viam, from the same machine that you intend to upload your module from.

2. Next, run the `viam module create` command to choose a custom module name and generate the required metadata for your module.
   By default, a new module is created as _private_, meaning that it is only accessible to members of your [organization](/fleet/organizations/), but you can choose to set the `visibility` of your module to _public_ to make it accessible to all Viam users.

   Select the private or public tab for instructions to upload your module with the respective `visibility` setting:

   {{< tabs >}}
   {{% tab name="Private" %}}

Get the `org-id` for your {{< glossary_tooltip term_id="organization" text="organization" >}} from your organization's **Settings** page in [the Viam App](https://app.viam.com/) and run the following command from the same directory as your custom module to generate metadata for your module:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam module create --name <your-module-name> --org-id <your-org-id>
```

If you later wish to make your module public, you can use the [`viam module update` command](/fleet/cli/#module).

{{% /tab %}}
{{% tab name="Public" %}}

{{% alert title="Important" color="note" %}}
If you mark your module as public, you cannot change it back to private.
{{% /alert %}}

1.  If you haven't already, [create a new namespace](/fleet/organizations/#create-a-namespace-for-your-organization) for your organization.
    If you have already created a namespace, you can find it on your organization's **Settings** page in [the Viam App](https://app.viam.com/), or by running the [`viam organizations list`](/fleet/cli/#organizations) command.

2.  To generate metadata for your module using your public namespace, run the following command from the same directory as your custom module:

    ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
    viam module create --name <your-module-name> --public-namespace <your-unique-namespace>
    ```

    {{% /tab %}}
    {{< /tabs >}}

    This command creates a new `meta.json` metadata file in your current working directory, which serves as a template.

3.  Edit the newly-created `meta.json` file, and provide the required configuration information for your custom module by filling in the following fields.

    <table class="table table-striped">
      <tr>
        <th>Name</th>
        <th>Type</th>
        <th>Inclusion</th>
        <th>Description</th>
      </tr>
      <tr>
        <td><code>module_id</code></td>
        <td>string</td>
        <td><strong>Required</strong></td>
        <td>The module ID, which includes either the module <a href="/fleet/organizations/#create-a-namespace-for-your-organization">namespace</a> or <a href="/fleet/organizations/">organization-id</a>, followed by its name (pre-populated using the <code>--name</code> you provided in the <code>viam module create</code> command).
        <div class="alert alert-caution" role="alert">
      <h4 class="alert-heading">Caution</h4>

      <p>The <code>module_id</code> uniquely identifies your module.
      Do not change the <code>module_id</code>.</p>

      </div>
        </td>

      </tr>
      <tr>
        <td><code>visibility</code></td>
        <td>string</td>
        <td><strong>Required</strong></td>
        <td>Whether the module is accessible only to members of your <a href="/fleet/organizations/">organization</a> (<code>private</code>), or visible to all Viam users (<code>public</code>). You can later make a private module public using the <code>viam module update</code> command, but once you make a module public, you cannot change it back to private.<br><br>Default: <code>private</code></td>
      </tr>
      <tr>
        <td><code>url</code></td>
        <td>string</td>
        <td>Optional</td>
        <td>The URL of the GitHub repository containing the source code of the module.</td>
      </tr>
      <tr>
        <td><code>description</code></td>
        <td>string</td>
        <td><strong>Required</strong></td>
        <td>A description of your module and what it provides.</td>
      </tr>
      <tr>
        <td><code>models</code></td>
        <td>object</td>
        <td><strong>Required</strong></td>
        <td><p>A list of one or more {{< glossary_tooltip term_id="model" text="models" >}} provided by your custom module. You must provide at least one model, which consists of an <code>api</code> and <code>model</code> key pair. If you are publishing a public module (<code>"visibility": "public"</code>), the namespace of your model must match the <a href="/fleet/organizations/#create-a-namespace-for-your-organization">namespace of your organization</a>.</p><p>For more information, see <a href="/registry/#naming-your-model-namespacerepo-namename">naming your model</a>.</p></td>
      </tr>
      <tr>
        <td><code>entrypoint</code></td>
        <td>string</td>
        <td><strong>Required</strong></td>
        <td>The name of the file that starts your module program. This can be a compiled executable, a script, or an invocation of another program. If you are providing your module as a single file to the <code>upload</code> command, provide the path to that single file. If you are providing a directory containing your module to the <code>upload</code> command, provide the path to the entry point file contained within that directory.</td>
      </tr>
      <tr>
        <td><code>build</code></td>
        <td>object</td>
        <td><strong>Optional</strong></td>
        <td>An object containing the command to run to build your module, as well as optional fields for the path to your dependency setup script, the target architectures to build for, and the path to your built module. Use this with the <a href="/fleet/cli/#using-the-build-subcommand">Viam CLI's build subcommand</a>. </td>
      </tr>

    </table>

    For example, the following represents the configuration of an example `my-module` public module in the `acme` namespace:

    ```json {class="line-numbers linkable-line-numbers"}
    {
      "module_id": "acme:my-module",
      "visibility": "public",
      "url": "https://github.com/acme-co-example/my-module",
      "description": "An example custom module.",
      "models": [
        {
          "api": "rdk:component:generic",
          "model": "acme:demo:my-model"
        }
      ],
      "build": {
        "path": "dist/archive.tar.gz", // optional - path to your built module
        "build": "./build.sh", // command that will build your module
        "arch": ["linux/amd64", "linux/arm64"] // architecture(s) to build for
      },
      "entrypoint": "dist/main"
    }
    ```

    {{% alert title="Important" color="note" %}}

In the example above, the model namespace is set to `acme` to match the owning organization's namespace.
If the two namespaces do not match, the command will return an error.

For more information, see [Naming your model](/registry/#naming-your-model-namespacerepo-namename).

    {{% /alert %}}

    See [`meta.json` file](/fleet/cli/#the-metajson-file) for more information.

1. For modules written in Python, you should package your module files as an archive first, before uploading.
   Other languages can proceed to the next step to upload their module directly.
   To package a module written in Python, run the following command from the same directory as your `meta.json` file:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   tar -czvf dist/archive.tar.gz dist/main
   ```

Where `dist/main` is the [packaged executable](/registry/create/#compile-or-package-your-module) that runs the module at the [entry point](/registry/create/#write-an-entry-point-main-program-file).

Supply the path to the resulting archive file in the next step.

1. Run `viam module upload` to upload your custom module to the Viam registry.
   Specify the path to the file, directory, or compressed archive (with `.tar.gz` or `.tgz` extension) that contains your custom module code:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   viam module upload --version <version> --platform <platform> <module-path>
   ```

   Where:

   - `version`: provide a version for your custom module, using [semantic versioning](https://semver.org/) (example: `1.0.0`).
     You can later increment this value with subsequent `viam module upload` commands.
     See [Using the `--version` argument](/fleet/cli/#using-the---version-argument) for more information.
   - `platform`: provide the system architecture your custom module supports.
     You can only provide one `platform` argument at a time to the `viam module upload` command.
     See [Using the `--platform` argument](/fleet/cli/#using-the---platform-argument) for the full list of supported architectures.
   - `module-path`: provide the path to the file, directory, or compressed archive (with `.tar.gz` or `.tgz` extension) that contains your custom module code.

   {{% alert title="Important" color="note" %}}
   The `viam module upload` command only supports one `platform` argument at a time.
   If you would like to upload your module with support for multiple platforms, you must run a separate `viam module upload` command for each platform.
   Use the _same version number_ when running multiple `upload` commands of the same module code if only the `platform` support differs.
   The Viam registry page for your module displays the platforms your module supports for each version you have uploaded.
   {{% /alert %}}

   For example:

   - To upload a custom module that is defined in a single file named `my-module-file` in a local `bin` directory:

     ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
     viam module upload --version 1.0.0 --platform linux/amd64 ./bin/my-module-file
     ```

   - To upload a custom module that includes multiple files, as well as a separate entry point file, all contained with a local `bin` directory:

     ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
     viam module upload --version 1.0.0 --platform linux/amd64 ./bin
     ```

   - To upload a custom module that has been compressed as an archive named `packaged-module.tar.gz`:

     ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
     viam module upload --version 1.0.0 --platform linux/amd64 packaged-module.tar.gz
     ```

When you `upload` a module, the command performs basic [validation](/fleet/cli/#upload-validation) of your module to check for common errors.

For more information, see the [`viam module` command](/fleet/cli/#module)

## Update an existing module

You can update an existing module in the [Viam registry](https://app.viam.com/registry) in one of two ways:

- [Upload new versions of your module manually](#update-an-existing-module-using-the-viam-cli) using the [Viam CLI](/fleet/cli/).
- [Automatically upload new versions of your module on release](#update-an-existing-module-using-a-github-action) as part of a continuous integration (CI) workflow, using a GitHub Action.

Updating your module manually is appropriate for smaller projects, especially those with only one contributor.
Updating your module automatically using CI is better suited for larger, ongoing projects, especially those with multiple contributors.

{{% alert title="Tip" color="tip" %}}
If you would like to test your module locally against its intended target platform before uploading it, you can follow the steps for [Iterative module development](/registry/advanced/iterative-development/) to verify that any code changes you have made work as expected on your target platform.
{{% /alert %}}

### Update an existing module using the Viam CLI

To update an existing module in the [Viam registry](https://app.viam.com/registry) manually, you can use the [Viam CLI](/fleet/cli/).

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
   tar -czf module.tar.gz dist/main
   ```

   Where `dist/main` is your [packaged executable](/registry/create/#compile-or-package-your-module).

   Supply the path to the resulting archive file in the next step.

1. Run `viam module upload` to upload your custom module to the Viam registry:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   viam module upload --version <version> --platform <platform> <module-path>
   ```

   For example, the following command uploads a module compressed as an archive named `my-module.tar.gz` to the Viam registry, and increments the [`version`](/fleet/cli/#using-the---version-argument) of the module to version `1.0.1`:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   viam module upload --version 1.0.1 --platform darwin/arm64 my-module.tar.gz
   ```

   When you `upload` a module, the command performs basic [validation](/fleet/cli/#upload-validation) of your module to check for common errors.

For more information, see the [`viam module` command](/fleet/cli/#module)

### Update an existing module using a GitHub action

To update an existing module in the [Viam registry](https://app.viam.com/registry) using continuous integration (CI), you can use one of two Github actions.
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

The `build-action` GitHub action relies on a build command that you need to specify in the <file>meta.json</file> file that you created for your module when you first [uploaded it](/registry/upload/#upload-a-custom-module-using-the-cli).
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
tar -czvf dist/archive.tar.gz dist/main
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
tar -czvf dist/archive.tar.gz dist/main
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
tar -czvf dist/archive.tar.gz dist/main
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
tar -czvf dist/archive.tar.gz dist/main
```

{ {% /expand%}}

{ {% /tab %}}
{ {< /tabs >}} -->

You can test this build configuration by running the Viam CLI's [`build local` command](/fleet/cli/#using-the-build-subcommand) on your development machine:

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

- [`org-id`](/fleet/cli/#using-the---org-id-and---public-namespace-arguments): Not required if your module is public.
- [`platform`](/fleet/cli/#using-the---platform-argument): You can only upload one platform at a time.
- [`version`](https://github.com/viamrobotics/upload-module/blob/main/README.md#versioning): Also see [Using the --version argument](/fleet/cli/#using-the---version-argument) for more details on the types of versioning supported.

For more details, see the [`upload-module` GitHub Action documentation](https://github.com/viamrobotics/upload-module), or take a look through one of the following example repositories that show how to package and deploy modules using the Viam SDKs:

- [Python with virtualenv](https://github.com/viam-labs/python-example-module/blob/main/.github/workflows/main.yml)
- [Python with docker](https://github.com/viamrobotics/python-container-module/blob/main/.github/workflows/deploy.yml)
- [Golang](https://github.com/viam-labs/wifi-sensor/blob/main/.github/workflows/deploy.yml)

{{% /tab %}}
{{< /tabs >}}

1. Create an [organization API key](/fleet/cli/#create-an-organization-api-key) with the [owner](/fleet/rbac/#permissions) role, which the GitHub action will use to authenticate to the Viam platform, using one of the following methods:

   - Use the Viam CLI to create an organization API key, which includes the owner role by default:

     ```sh {class="command-line" data-prompt="$"}
     viam organizations api-key create --org-id <org-id> --name <key-name>
     ```

   - Use the organizations page on the [Viam app](https://app.viam.com/) to generate a new organization API key.
     Make sure your organization API key is set to **Role: Owner**, or the GitHub action will not be able to successfully authenticate during runs.
     If you are using an existing organization API key which is not set to **Role: Owner**, you can change an API key's permissions from the Viam app on the organizations page by clicking the **Show details** link next to your API key.
     The operator role cannot be used to authenticate GitHub action runs.
     For more information see [Manage organizations](/fleet/organizations/).

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

## Next steps

{{< cards >}}
{{% card link="/registry/configure/" %}}
{{% card link="/registry/examples/" %}}
{{< /cards >}}
