---
title: "Upload your own modules to the Viam registry"
linkTitle: "Upload"
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
description: "Use the Viam CLI to upload a custom module to the Viam registry."
no_list: true
---

Once you have [created a custom module](/extend/modular-resources/create/), you can use the [Viam CLI](/manage/cli/) to upload it to the Viam registry.

With the CLI, you can register your module with the [Viam registry](https://app.viam.com/registry) to share it with other Viam users, or upload it as a private module that is shared only within your [organization](/manage/fleet/organizations/).

For more information, see the [`viam module` command](/manage/cli/#module).

## Upload a custom module

To upload your custom module to the [Viam registry](https://app.viam.com/registry), either as a public or private module, use the Viam CLI commands `create`, `upload`, and `update` following the instructions below:

1. First, [install the Viam CLI](/manage/cli/#install) and [authenticate](/manage/cli/#authenticate) to Viam, from the same machine that you intend to upload your module from.

1. Next, run the `viam module create` command to select a new custom module name and generate module metadata.

   1. If you haven't already, [create a new namespace](/manage/fleet/organizations/#create-a-namespace-for-your-organization) for your organization.
      If you have already created a namespace, you can find it on your organization's **Settings** page in [the Viam App](https://app.viam.com/).

   1. To generate metadata for your module using your public namespace, run the following command from the same directory as your custom module:

      ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
      viam module create --name <your-module-name> --public-namespace <your-unique-namespace>
      ```

   This command creates a new `meta.json` metadata file in your current working directory, which serves as a template on which to base your custom configurations.
   Editing and then uploading the `meta.json` file sets important configuration information about your module, such as whether it will be publicly available to all Viam users, or only available within your organization.

1. Edit the newly-created `meta.json` file, and provide the required configuration information for your custom module by filling in the following fields.
   The `name` field is pre-populated using the `--name` you provided in the `viam module create` command, and `visibility` is set to `private` by default.

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
       <td>The name of the module, including its <a href="/manage/fleet/organizations/#create-a-namespace-for-your-organization">namespace</a></td>

     </tr>
     <tr>
       <td><code>visibility</code></td>
       <td>string</td>
       <td><strong>Required</strong></td>
       <td>Whether the module is accessible only to members of your <a href="/manage/fleet/organizations/">organization</a> (<code>private</code>), or visible to all Viam users (<code>public</code>). You can change this setting later using the <code>viam module update</code> command.<br><br>Default: <code>private</code></td>
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
       <td>A list of one or more <a href="/extend/modular-resources/key-concepts/#models">models</a> provided by your custom module. You must provide at least one model, which consists of an <code>api</code> and <code>model</code> key pair.</td>
     </tr>
     <tr>
       <td><code>entrypoint</code></td>
       <td>string</td>
       <td><strong>Required</strong></td>
       <td>The name of the file that starts your module program. This can be a compiled executable, a script, or an invocation of another program.</td>
     </tr>
   </table>

   For example, the following represents the configuration of an example `my-module` module in the `acme` namespace:

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
     "entrypoint": "my-module.sh"
   }
   ```

   {{% alert title="Important" color="note" %}}
   If you are publishing a public module (`"visibility": "public"`), the [namespace of your model](/extend/modular-resources/key-concepts/#naming-your-model) must match the [namespace of your organization](/manage/fleet/organizations/#create-a-namespace-for-your-organization).
   In the example above, the model namespace is set to `acme` to match the owning organization's namespace.
   If the two namespaces do not match, the command will return an error.
   {{% /alert %}}

   See [The `meta.json` file](/manage/cli/#the-metajson-file) for more information.

1. Run `viam module update` to register the configuration changes you just made to `meta.json` with the Viam registry.
   Run this command from within the same directory as your `meta.json` file:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   viam module update
   ```

   On a successful update, the command will return a link to the updated module in the Viam registry.

1. Package your custom module to get it ready to upload to the Viam registry.
   Currently, the Registry only supports `tar.gz` or `tar.xz` format.
   Use the command below specific for the language of your module:

   - To package a module written in Go, run the following commands from the same directory as your `meta.json` file:

     ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
     go build -o bin/module ./module/main.go
     tar -cxf module.tar.gz bin/module
     ```

     For more information, see [Compile a module into an executable](/extend/modular-resources/create/#compile-the-module-into-an-executable).

   - To package a module written in Python, run the following command from the same directory as your `meta.json` file:

     ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
     tar -czf module.tar.gz run.sh requirements.txt src
     ```

     Where `run.sh` is your [entrypoint file](/extend/modular-resources/create/#compile-the-module-into-an-executable), `requirements.txt` is your [pip dependency list file](/extend/modular-resources/create/#compile-the-module-into-an-executable), and `src` is the source directory of your module.

1. Run `viam module upload` to upload the updated custom module to the Viam registry:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   viam module upload --version <version> --platform <platform> module.tar.gz
   ```

   Where:

   - `version` - provide a version for your custom module, using [semantic versioning](https://semver.org/) (example: `1.0.0`).
     You can later increment this value with subsequent `viam module upload` commands.
     See [Using the `--version` argument](/manage/cli/#using-the---version-argument) for more information.
   - `platform` - provide _one_ of the following, depending on the platform you have built your custom module for (You can use the `uname -m` command to determine your system architecture):
     - `darwin/arm64` - macOS computers running the `arm64` architecture, such as Apple Silicon.
     - `darwin/amd64` - macOS computers running the Intel `x86_64` architecture.
     - `linux/arm64` - Linux computers or {{< glossary_tooltip term_id="board" text="boards" >}} running the `arm64` (`aarch64`) architecture, such as the Raspberry Pi.
     - `linux/amd64` - Linux computers or {{< glossary_tooltip term_id="board" text="boards" >}} running the Intel `x86_64` architecture.
   - `path` - provide the path to the compressed archive, in `tar.gz` or `tar.xz` format, that contains your custom module code.

   {{% alert title="Important" color="note" %}}
   The `viam module upload` command only supports one `platform` argument at a time.
   If you would like to upload your module with support for multiple platforms, you must run a separate `viam module upload` command for each platform.
   Use the _same version number_ when running multiple `upload` commands of the same module code if only the `platform` support differs.
   The Viam registry page for your module displays the platforms your module supports for each version you have uploaded.
   {{% /alert %}}

   For example, the following command uploads the compressed `module.tar.gz` archive to the Viam registry when run in the same directory as the corresponding `meta.json` file:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   viam module upload --version 1.0.0 --platform darwin/arm64 module.tar.gz
   ```

   When you `upload` a module, the command performs basic [validation](/manage/cli/#upload-validation) of your packaged module to ensure it is compatible with the Viam registry.

For more information, see the [`viam module` command](/manage/cli/#module)

## Update an existing module

You can update an existing module in the [Viam registry](https://app.viam.com/registry) in one of two ways:

- [Upload new versions of your module manually](#update-an-existing-module-using-the-viam-cli) using the [Viam CLI](/manage/cli/).
- [Automatically upload new versions of your module on release](#update-an-existing-module-using-a-github-action) as part of a continuous integration (CI) workflow, using a GitHub Action.

Updating your module manually is appropriate for smaller projects, especially those with only one contributor.
Updating your module automatically using CI is better suited for larger, ongoing projects, especially those with multiple contributors.

### Update an existing module using the Viam CLI

To update an existing module in the [Viam registry](https://app.viam.com/registry) manually, use the [Viam CLI](/manage/cli/):

1. Edit your custom module with the changes you'd like to make.

1. Update your custom module's `meta.json` file with the changes, if any.
   For example, if you have altered your model's name, or adjusted the endpoint name, you'll need to update `meta.json` with these changes.

1. Run `viam module update` to register the configuration changes you just made to `meta.json` with the Viam registry.
   Run this command from within the same directory as your `meta.json` file:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   viam module update
   ```

   On a successful update, the command will return a link to the updated module in the Viam registry.

1. Package your custom module to get it ready to upload to the Viam registry.
   Currently, the Registry only supports `tar.gz` or `tar.xz` format.
   Use the command below specific for the language of your module:

   - To package a module written in Go, run the following commands from the same directory as your `meta.json` file:

     ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
     go build -o bin/module ./module/main.go
     tar -cxf module.tar.gz bin/module
     ```

     For more information, see [Compile a module into an executable](/extend/modular-resources/create/#compile-the-module-into-an-executable).

   - To package a module written in Python, run the following command from the same directory as your `meta.json` file:

     ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
     tar -czf module.tar.gz run.sh requirements.txt src
     ```

     Where `run.sh` is your [entrypoint file](/extend/modular-resources/create/#compile-the-module-into-an-executable), `requirements.txt` is your [pip dependency list file](/extend/modular-resources/create/#compile-the-module-into-an-executable), and `src` is the source directory of your module.

1. Run `viam module upload` to upload the updated custom module to the Viam registry:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   viam module upload --version <version> --platform <platform> <path-to-tar.gz>
   ```

   For example, the following command uploads the compressed `my-module.tar.gz` archive to the Viam registry when run in the same directory, and increments the [`version`](/manage/cli/#using-the---version-argument) of the module to version `1.0.1`:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   viam module upload --version 1.0.1 --platform darwin/arm64 my-module.tar.gz
   ```

   When you `upload` a module, the command performs basic [validation](/manage/cli/#upload-validation) of your packaged module to ensure it is compatible with the Viam registry.

For more information, see the [`viam module` command](/manage/cli/#module)

### Update an existing module using a GitHub action

To update an existing module in the [Viam registry](https://app.viam.com/registry) using CI, use the [`upload-module` GitHub action](https://github.com/viamrobotics/upload-module).

1. Edit your custom module with the changes you'd like to make.

1. Navigate to the **Actions** tab of the GitHub repository you are using for your module code.
   If you have already created GitHub actions for this repository, click the **New workflow** button to create a new one.
   If you have not yet created any GitHub actions, click the **Set up a workflow yourself** link.
   See the [GitHub actions documentation](https://docs.github.com/en/actions/creating-actions) for more information.

1. Paste the following action template YAML into the edit window.

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
             org-id: your-org-id-uuid # <-- replace with your org ID. not required for public modules
             platform: linux/amd64 # <-- replace with your target architecture, or your module will not deploy
             version: ${{ github.event_name == 'release' && github.ref_name || format('0.0.0-{0}.{1}', github.ref_name, github.run_number) }} # <-- see 'Versioning' section below for explanation
             key-id: ${{ secrets.viam_key_id }}
             key-value: ${{ secrets.viam_key_value }}
   ```

1. Edit the copied code to include the configuration specific to your module.
   Each item marked with a `<--` comment requires that you edit the configuration values accordingly.

   Set `run` to the command you use to build and package your module.
   When ready to test the action, uncomment `if: github.event_name == 'release'` to enable the action to trigger a run when you [issue a release](https://docs.github.com/en/repositories/releasing-projects-on-github).

   For guidance on configuring the other parameters, see the documentation for each:

   - [`org-id`](/manage/cli/#using-the---org-id-and---public-namespace-arguments) - Not required if your module is public.
   - [`platform`](/manage/cli/#using-the---platform-argument) - You can only upload one platform at a time.
   - [`version`](https://github.com/viamrobotics/upload-module/blob/main/README.md#versioning) - Also see [Using the --version argument](/manage/cli/#using-the---version-argument) for more details on the types of versioning supported.

1. Create an organization API key and configure your GitHub repository to use it to authenticate during GitHub action runs, following the steps below:

   1. Follow the instructions to [Create an organization API key](/manage/cli/#create-an-organization-api-key).
      These steps will return a `key id` and a `key value` which together comprise your organization API key.
      If you have already created an organization API key, you can skip this step.

   1. In the GitHub repository for your project, select **Settings**, then **Secrets and variables**, then **Actions**.

   1. Click the green **New repository secret** button, enter `viam_key_id` as the **NAME**, paste the value for `key id` from above into the **Secret** text field, then click **Add secret**.

   1. Then, click the green **New repository secret** button, enter `viam_key_value` as the **NAME**, paste the value for `key value` from above into the **Secret** text field, then click **Add secret**.

   For more information on GitHub secrets, see the GitHub documentation for [Creating secrets for a repository](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions#creating-secrets-for-a-repository).

1. Push a commit to your module or [create a new release](https://docs.github.com/en/repositories/releasing-projects-on-github).
   The specific step to take to release your software depends on your CI workflow, your GitHub configuration, and the `run` step you defined earlier.
   Once complete, your module should upload to the [Viam registry](https://app.viam.com/registry) with the appropriate version automatically.

For more details, see the [`upload-module` GitHub action documentation](https://github.com/viamrobotics/upload-module), or take a look through one of the following example repositories that show how to package and deploy modules using the Viam SDKs:

- [Python with virtualenv](https://github.com/viam-labs/python-example-module)
- [Python with docker](https://github.com/viamrobotics/python-container-module)
- [Golang](https://github.com/viam-labs/wifi-sensor)
- [C++](https://github.com/viamrobotics/module-example-cpp)
