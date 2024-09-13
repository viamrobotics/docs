---
title: "How to upload a module to the Viam Registry"
linkTitle: "Upload a module"
type: "docs"
weight: 26
images: ["/registry/module-puzzle-piece.svg"]
icon: true
tags: ["modular resources", "components", "services", "registry"]
description: "Make your module available to others by uploading it to the modular resource registry."
aliases:
  - /registry/upload/
  - /extend/modular-resources/upload/
  - /modular-resources/upload/
languages: []
viamresources: []
platformarea: ["registry"]
level: "Beginner"
date: "2024-08-21"
# updated: ""  # When the tutorial was last entirely checked
cost: "0"
---

After [writing a module](/how-tos/create-module/), you can upload your module to the Viam registry to:

- share your module with other Viam users
- deploy your module to a fleet of machines from a central interface

You can choose to upload it to the Viam registry as a _public module_ that is shared with other Viam users, or as a _private module_ that is shared only within your [organization](/cloud/organizations/).

To upload your custom module to the [Viam registry](https://app.viam.com/registry), either as a public or private module, use the Viam CLI commands `create` and `upload` following these instructions.

{{% alert title="In this page" color="info" %}}

- [Package and upload a module to the Viam registry](#upload-a-module)

{{% /alert %}}

## Prerequisites

{{% expand "A local module you've written and tested" %}}

See [Create a Module](/how-tos/create-module/) or [Create a Sensor Module with Python](/how-tos/sensor-module/) for instructions.

{{% /expand%}}

## Upload a module

{{< table >}}
{{% tablestep %}}
**1. Install the CLI**

First, install the Viam CLI and [authenticate](/cli/#authenticate) to Viam, from the same machine that you intend to upload your module from.

{{< readfile "/static/include/how-to/install-cli.md" >}}

{{% /tablestep %}}
{{% tablestep %}}
**2. Generate a metadata file**

Next, run the `viam module create` command to choose a custom module name and generate the required metadata for your module.
By default, a new module is created as _private_, meaning that it is only accessible to members of your [organization](/cloud/organizations/), but you can choose to set the `visibility` of your module to _public_ to make it accessible to all Viam users.

Select the private or public tab for instructions to upload your module with the respective `visibility` setting:

{{< tabs >}}
{{% tab name="Private" %}}

Get the `org-id` for your {{< glossary_tooltip term_id="organization" text="organization" >}} from your organization's **Settings** page in [the Viam App](https://app.viam.com/) and run the following command from the same directory as your custom module to generate metadata for your module:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam module create --name <your-module-name> --org-id <your-org-id>
```

If you later wish to make your module public, you can use the [`viam module update` command](/cli/#module).

{{% /tab %}}
{{% tab name="Public" %}}

1.  If you haven't already, [create a new namespace](/cloud/organizations/#create-a-namespace-for-your-organization) for your organization.
    If you have already created a namespace, you can find it on your organization's **Settings** page in [the Viam app](https://app.viam.com/), or by running the [`viam organizations list`](/cli/#organizations) command.

2.  To generate metadata for your module using your public namespace, run the following command from the same directory as your custom module:

    ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
    viam module create --name <your-module-name> --public-namespace <your-unique-namespace>
    ```

{{% /tab %}}
{{< /tabs >}}

This command creates a new `meta.json` metadata file in your current working directory, which serves as a template.

{{% /tablestep %}}
{{% tablestep %}}
**3. Edit the metadata file**

Edit the newly-created `meta.json` file, and provide the required configuration information for your custom module by filling in the following fields.

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
    <td>The module ID, which includes either the module <a href="/cloud/organizations/#create-a-namespace-for-your-organization">namespace</a> or <a href="/cloud/organizations/">organization-id</a>, followed by its name (pre-populated using the <code>--name</code> you provided in the <code>viam module create</code> command).
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
    <td>Whether the module is accessible only to members of your <a href="/cloud/organizations/">organization</a> (<code>private</code>), or visible to all Viam users (<code>public</code>). You can later make a private module public using the <code>viam module update</code> command. Once you make a module public, you can change it back to private if it is not configured on any machines outside of your organization.<br><br>Default: <code>private</code></td>
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
    <td><p>A list of one or more {{< glossary_tooltip term_id="model" text="models" >}} provided by your custom module. You must provide at least one model, which consists of an <code>api</code> and <code>model</code> key pair. If you are publishing a public module (<code>"visibility": "public"</code>), the namespace of your model must match the <a href="/cloud/organizations/#create-a-namespace-for-your-organization">namespace of your organization</a>.</p><p>For more information, see <a href="/how-tos/create-module/#name-your-new-resource-model">naming your model</a>.</p></td>
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
    <td>Optional</td>
    <td>An object containing the command to run to build your module, as well as optional fields for the path to your dependency setup script, the target architectures to build for, and the path to your built module. Use this with the <a href="/cli/#using-the-build-subcommand">Viam CLI's build subcommand</a>. </td>
  </tr>

</table>

For example, the following represents the configuration of an example `my-module` public module in the `acme` namespace:

{{< expand "Click to view example meta.json with build object" >}}

```json {class="line-numbers linkable-line-numbers"}
{
  "module_id": "acme:my-module",
  "visibility": "public",
  "url": "https://github.com/<my-repo-name>/my-module",
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
  "entrypoint": "dist/main" // path to executable
}
```

{{< /expand >}}

{{< expand "Click to view example meta.json without build object" >}}

```json {class="line-numbers linkable-line-numbers"}
{
  "module_id": "acme:my-module",
  "visibility": "public",
  "url": "https://github.com/<my-repo-name>/my-module",
  "description": "An example custom module.",
  "models": [
    {
      "api": "rdk:component:generic",
      "model": "acme:demo:my-model"
    }
  ],
  "entrypoint": "my-module.sh" // path to executable
}
```

{{< /expand >}}

{{% alert title="Important" color="note" %}}

In the example above, the model namespace is set to `acme` to match the owning organization's namespace.
If the two namespaces do not match, the command will return an error.

For more information, see [Name your new resource model](/how-tos/create-module/#name-your-new-resource-model).

{{% /alert %}}

See [`meta.json` file](/cli/#the-metajson-file) for more information.

{{% /tablestep %}}
{{% tablestep %}}
**4. (For Python) Package module as an archive**

For modules written in Python, you should package your module files as an archive first, before uploading.
Other languages can proceed to the next step to upload their module directly.
To package a module written in Python, run the following command from the same directory as your `meta.json` file:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
tar -czvf dist/archive.tar.gz <PATH-TO-EXECUTABLE>
```

where `<PATH-TO-EXECUTABLE>` is the [packaged executable](/how-tos/create-module/#compile-or-package-your-module) that runs the module at the [entry point](/how-tos/create-module/#write-an-entry-point-main-program-file).
If using PyInstaller, by default this would be `dist/main`.

For a Python module built using the `venv` approach, the command might look like this:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
tar -czf module.tar.gz run.sh requirements.txt src
```

Where `run.sh` is your [entrypoint file](/how-tos/create-module/#compile-or-package-your-module), `requirements.txt` is your [pip dependency list file](/how-tos/create-module/#compile-or-package-your-module), and `src` is the directory that contains the source code of your module.

Supply the path to the resulting archive file in the next step.

{{% /tablestep %}}
{{% tablestep %}}
**5. Upload your module**

Run `viam module upload` to upload your custom module to the Viam registry.
Specify the path to the file, directory, or compressed archive (with `.tar.gz` or `.tgz` extension) that contains your custom module code:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam module upload --version <version> --platform <platform> <module-path>
```

where:

- `version`: provide a version for your custom module, using [semantic versioning](https://semver.org/) (example: `1.0.0`).
  You can later increment this value with subsequent `viam module upload` commands.
  See [Using the `--version` argument](/cli/#using-the---version-argument) for more information.
- `platform`: provide the system architecture your custom module supports.
  You can only provide one `platform` argument at a time to the `viam module upload` command.
  See [Using the `--platform` argument](/cli/#using-the---platform-argument) for the full list of supported architectures.
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

When you `upload` a module, the command performs basic [validation](/cli/#upload-validation) of your module to check for common errors.

For more information, see the [`viam module` command](/cli/#module).

{{% /tablestep %}}
{{< /table >}}

## Next steps

Now that your module is available in the registry, you can configure the components or services it supports just as you would configure other resources: Go to the **CONFIGURE** tab of a machine, add a component or service (as applicable), and search for the name of your model.

To update, delete, or change the privacy settings of a module you deployed, see [Manage Modules](/how-tos/manage-modules/).
