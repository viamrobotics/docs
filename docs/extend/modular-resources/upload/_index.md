---
title: "Upload your own modules to the Viam Registry"
linkTitle: "Upload"
weight: 20
type: "docs"
tags: ["server", "rdk", "extending viam", "modular resources", "components", "services"]
description: "Use the Viam CLI to upload a custom module to the Viam Registry."
no_list: true
---

{{% alert title="Beta Notice" color="note" %}}
This feature is in beta, and may not be suitable for production use.
{{% /alert %}}

Once you have [created a custom module](/extend/modular-resources/create/), you can use the [Viam CLI](/manage/cli/) to upload it to the Viam Registry.

With the CLI, you can register your module with the Viam Registry to share it with other Viam users, or upload it as a private module that is shared only within your [organization](/manage/fleet/organizations/).

For more information, see the [`viam module` command](/manage/cli/#module).

## Upload a custom module

To upload your custom module to the Viam Registry, either as a public or private module, use the Viam CLI commands `create`, `upload`, and `update` following the instructions below:

1. First, [install the Viam CLI](/manage/cli/#install) and [authenticate](/manage/cli/#authenticate) to Viam, from the same machine that you intend to upload your module from.

1. Next, run the `viam module create` command to select a new custom module name and generate module metadata.

   1. If you haven't already, [create a new namespace](/manage/fleet/organizations/#create-a-namespace-for-your-organization) for your organization.
      If you have already created a namespace, you can find it on your organization's **Settings** page in [the Viam App](https://app.viam.com/).

   1. To generate metadata for your module using your public namespace, run the following command from the same directory as your custom module:

      ``` sh {id="terminal-prompt" class="command-line" data-prompt="$"}
      viam module create --name <your-module-name> --public-namespace <your-unique-namespace>
      ```

   This command creates a new `meta.json` metadata file in your current working directory, which serves as a template on which to base your custom configurations.
   Editing and then uploading the `meta.json` file sets important configuration information about your module, such as whether it will be publicly available to all Viam users, or only available within your organization.

1. Edit the newly-created `meta.json` file, and provide the required configuration information for your custom module by filling in the following fields.
   The `module_id` field is pre-populated using the `--name` you provided in the `viam module create` command, and `visibility` is set to `private` by default.

   <table class="table table-striped">
     <tr>
       <th>Name</th>
       <th>Type</th>
       <th>Inclusion</th>
       <th>Description</th>
     </tr>
     <tr>
       <td><code>name</code></td>
       <td>string</td>
       <td><strong>Required</strong></td>
       <td>The name of the module, including its <a href="/manage/fleet/organizations/#create-a-namespace-for-your-organization">namespace</a></td>

     </tr>
     <tr>
       <td><code>visibility</code></td>
       <td>string</td>
       <td><strong>Required</strong></td>
       <td>Whether the module is visible to all Viam users (<code>public</code>), or accessible only to members of your <a href="/manage/fleet/organizations/">organization</a> (<code>private</code>). You can change this setting later using the <code>viam module update</code> command.<br><br>Default: <code>private</code></td>
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
     "name": "acme:my-module",
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
   If you are publishing a public module (`visibility: "public"`), the [namespace of your model](/extend/modular-resources/key-concepts/#namespace-1) must match the [namespace of your organization](/manage/fleet/organizations/#create-a-namespace-for-your-organization).
   In the example above, the model namespace is set to `acme` to match the owning organization's namespace.
   If the two namespaces do not match, the command will return an error.
   {{% /alert %}}

   See [The `meta.json` file](/manage/cli/#the-metajson-file) for more information.

1. Run `viam module update` to register the configuration changes you just made to `meta.json` with the Viam Registry.
   Run this command from within the same directory as your `meta.json` file:

      ``` sh {id="terminal-prompt" class="command-line" data-prompt="$"}
      viam module update
      ```

   On a successful update, the command will return a link to the updated module in the Viam Registry.

1. Package your custom module to get it ready to upload to the Viam Registry.
   Currently, the Registry only supports `tar.gz` or `tar.xz` format.
   Use the command below specific for the language of your module:

   - To package a module written in Go, run the following command from the same directory as your `meta.json` file:

     ``` sh {id="terminal-prompt" class="command-line" data-prompt="$"}
     tar -czf module.tar.gz module.go
     ```

     Where `module.go` is your [compiled entrypoint file](/extend/modular-resources/create/#compile-the-module-into-an-executable).

   - To package a module written in Python, run the following command from the same directory as your `meta.json` file:

     ``` sh {id="terminal-prompt" class="command-line" data-prompt="$"}
     tar -czf module.tar.gz run.sh requirements.txt src
     ```

     Where `run.sh` is your [entrypoint file](/extend/modular-resources/create/#compile-the-module-into-an-executable), `requirements.txt` is your Python dependency list, and `src` is the source directory of your module.

1. Run `viam module upload` to upload the updated custom module to the Viam Registry:

   ``` sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   viam module upload --version <version> --platform <platform> module.tar.gz
   ```

   Where:

   - `version` - provide a version for your custom module, using [semantic versioning](https://semver.org/) (example: `1.0.0`).
      You can later increment this value with subsequent `viam module upload` commands.
      See [Using the `--version` argument](/manage/cli/#using-the---version-argument) for more information.
   - `platform` - provide *one* of the following, depending on the platform you have built your custom module for (You can use the `uname -m` command to determine your system architecture):
      - `darwin/arm64` - macOS computers running the `arm64` architecture, such as Apple Silicon.
      - `darwin/amd64` - macOS computers running the Intel `x86_64` architecture.
      - `linux/arm64` - Linux computers or {{< glossary_tooltip term_id="board" text="boards" >}} running the `arm64` (`aarch64`) architecture, such as the Raspberry Pi.
      - `linux/amd64` - Linux computers or {{< glossary_tooltip term_id="board" text="boards" >}} running the Intel `x86_64` architecture.
   - `path` - provide the path to the compressed archive, in `tar.gz` or `tar.xz` format, that contains your custom module code.

   {{% alert title="Important" color="note" %}}
   The `viam module upload` command only supports one `platform` argument at a time.
   If you would like to upload your module with support for multiple platforms, you must run a separate `viam module upload` command for each platform.
   Use the *same version number* when running multiple `upload` commands of the same module code if only the `platform` support differs.
   {{% /alert %}}

   For example, the following command uploads the compressed `module.tar.gz` archive to the Viam Registry when run in the same directory as the corresponding `meta.json` file:

   ``` sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   viam module upload --version 1.0.0 --platform darwin/arm64 module.tar.gz
   ```

For more information, see the [`viam module` command](/manage/cli/#module)

## Update an existing module

You can also use the [Viam CLI](/manage/cli/) to update an existing custom module in the Viam Registry.

1. Edit your custom module with the changes you'd like to make.

1. Update your custom module's `meta.json` file with the changes, if any.
   For example, if you have altered your model's name, or adjusted the endpoint name, you'll need to update `meta.json` with these changes.

1. Run `viam module update` to register the configuration changes to your module (and to `meta.json` if applicable):

   - To register a *public* module, run the following command from within the same directory as your `meta.json` file:

      ``` sh {id="terminal-prompt" class="command-line" data-prompt="$"}
      viam module update
      ```

   - To register a *private* module, run the following command from within the same directory as your `meta.json` file, providing your organization ID:

      ``` sh {id="terminal-prompt" class="command-line" data-prompt="$"}
      viam module update --org-id <org-id>
      ```

   On successful update, the command will return a link to the updated module in the Viam Registry.

1. Package your custom module to get it ready to upload to the Viam Registry.
   Currently, the Registry only supports `tar.gz` or `tar.xz` format.
   Use the command below specific for the language of your module:

   - To package a module written in Go, run the following command from the same directory as your `meta.json` file:

     ``` sh {id="terminal-prompt" class="command-line" data-prompt="$"}
     tar -czf module.tar.gz module.go
     ```

     Where `module.go` is your [compiled entrypoint file](/extend/modular-resources/create/#compile-the-module-into-an-executable).

   - To package a module written in Python, run the following command from the same directory as your `meta.json` file:

     ``` sh {id="terminal-prompt" class="command-line" data-prompt="$"}
     tar -czf module.tar.gz run.sh requirements.txt src
     ```

     Where `run.sh` is your [entrypoint file](/extend/modular-resources/create/#compile-the-module-into-an-executable), `requirements.txt` is your Python dependency list, and `src` is the source directory of your module.

1. Run `viam module upload` to upload the updated custom module to the Viam Registry:

   ``` sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   viam module upload --version <version> --platform <platform> <path-to-tar.gz>
   ```

   For example, the following command uploads the compressed `my-module.tar.gz` archive to the Viam Registry when run in the same directory, and increments the [`version`](/manage/cli/#using-the---version-argument) of the module to version `1.0.1`:

   ``` sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   viam module upload --version 1.0.1 --platform darwin/arm64 my-module.tar.gz
   ```

For more information, see the [`viam module` command](/manage/cli/#module)
