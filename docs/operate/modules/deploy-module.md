---
title: "Package and deploy a module"
linkTitle: "Package and deploy"
weight: 39
layout: "docs"
type: "docs"
icon: true
images: ["/registry/create-module.svg"]
description: "Add support for more physical or virtual hardware to the Viam ecosystem by creating a custom module."
aliases:
  - /extend/modular-resources/upload/
  - /modular-resources/upload/
  - /registry/upload/
  - /how-tos/upload-module/
---

At this point you should have a working module, deployed locally on a machine for testing.
To make it available to deploy on more machines, the following steps will show you how to package it and upload it to the [registry](https://app.viam.com/registry).

## Prepare the module for upload

{{< table >}}
{{% tablestep start=1 %}}
**Create a README (strongly recommended)**

It's quite helpful to create a README to document what your module does and how to configure and use it, especially if you plan to share your module with others.

{{< expand "Example sensor module README" >}}

````md
# `meteo_PM` modular component

This module implements the [Viam sensor API](https://docs.viam.com/dev/reference/apis/components/sensor/) in a `jessamy:weather:meteo_PM` model.
With this model, you can gather [Open-Meteo](https://open-meteo.com/en/docs/air-quality-api) PM2.5 and PM10 air quality data from anywhere in the world, at the coordinates you specify.

Navigate to the **CONFIGURE** tab of your machine's page.
Click the **+** button, select **Component or service**, then select the `sensor / weather:meteo_PM` model provided by the [`weather` module](https://app.viam.com/module/jessamy/weather).
Click **Add module**, enter a name for your sensor, and click **Create**.

## Configure your `meteo_PM` sensor

On the new component panel, copy and paste the following attribute template into your sensor's **Attributes** box:

```json
{
  "latitude": <float>,
  "longitude": <float>
}
```

### Attributes

The following attributes are available for `rdk:sensor:jessamy:weather:meteo_PM` sensors:

| Name        | Type  | Inclusion | Description                            |
| ----------- | ----- | --------- | -------------------------------------- |
| `latitude`  | float | Optional  | Latitude at which to get the readings  |
| `longitude` | float | Optional  | Longitude at which to get the readings |

### Example Configuration

```json
{
  "latitude": -40.6,
  "longitude": 93.125
}
```
````

{{< /expand >}}

{{% /tablestep %}}
{{% tablestep %}}
**Create a GitHub repo and link to it from your `meta.json`**

Create a GitHub repository with all the source code and the README for your module.
This is required for cloud build to work.
{{% /tablestep %}}
{{% tablestep %}}
**Add the link to the repo to the meta.json file**

Add the link to that repo as the `url` in the <file>meta.json</file> file.

{{% /tablestep %}}
{{% tablestep %}}
**Edit the meta.json file**

Make any necessary edits to the `meta.json` file.
For example, if you've changed the module's functionality, update the description in the `meta.json` file.
Click below for information about the available fields.

If you want to share the module outside of your organization, set `"visibility": "public"`.

{{< expand "meta.json reference" >}}

{{< readfile "/static/include/metajson.md" >}}

{{< /expand >}}

{{% /tablestep %}}
{{< /table >}}

## Package and upload the module

{{< table >}}
{{% tablestep start=1 %}}
**Package and upload**

To package (for Python) and upload your module and make it available to configure on machines in your organization (or in any organization, depending on how you set `visibility` in the <file>meta.json</file> file):

{{< tabs >}}
{{% tab name="Python: PyInstaller (recommended)" %}}

The recommended approach for Python is to use [PyInstaller](https://pypi.org/project/pyinstaller/) to compile your module into a packaged executable: a standalone file containing your program, the Python interpreter, and all of its dependencies.
When packaged in this fashion, you can run the resulting executable on your desired target platform or platforms without needing to install additional software or manage dependencies manually.

{{% alert title="Note" color="note" %}}
To follow these PyInstaller packaging steps, you must have enabled cloud build when moving through the module generator prompts.
If you did not, you will need to manually create a <file>build.sh</file> entrypoint script.
{{% /alert %}}

Edit your <file>meta.json</file> file back to its original state, reverting the edits you made for local testing purposes.
It should resemble the following:

```json {class="line-numbers linkable-line-numbers" data-start="13" data-line="1, 4, 6" }
 "entrypoint": "dist/main",
 "first_run": "",
 "build": {
   "build": "./build.sh",
   "setup": "./setup.sh",
   "path": "dist/archive.tar.gz",
   "arch": [
     "linux/amd64",
     "linux/arm64"
   ]
 }
```

Delete the <file>reload.sh</file> script since it was only meant for testing purposes.

Now you are ready to build and upload your module, either using Viam's cloud build tooling which is recommended for continuous integration, or a more manual process:

{{< tabs >}}
{{% tab name="PyInstaller cloud build (recommended)" %}}

We recommend you use PyInstaller with the [`build-action` GitHub action](https://github.com/viamrobotics/build-action) which provides a simple cross-platform build setup for multiple platforms: x86 and Arm Linux distributions, and MacOS.

The `viam module generate` command already generated the `build-action` file in your <file>.github/workflows</file> folder, so you just need to set up authentication in GitHub, and then create a new release to trigger the action:

1. In your terminal, run `viam organizations list` to view your organization ID.
1. Create an organization API key by running the following command:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   viam organization api-key create --org-id YOUR_ORG_UUID --name descriptive-key-name
   ```

1. In the GitHub repo for your project, go to **Settings** &rarr; **Secrets and variables** &rarr; **Actions**.
   Create two new secrets using the **New repository secret** button:

   - `VIAM_KEY_ID` with the UUID from `Key ID:` in your terminal
   - `VIAM_KEY_VALUE` with the string from `Key Value:` in your terminal

1. From the main code page of your GitHub repo, find **Releases** in the right side menu and click **Create a new release**.
1. In the **Choose a tag** dropdown, create a new tag with a name consisting of three numbers separated by periods, following the regular expression `[0-9]+.[0-9]+.[0-9]+` (for example, `1.0.0`).
   You must follow this format to trigger the build action.
   For details about versioning, see [Module versioning](/operate/modules/advanced/module-configuration/#module-versioning).

1. Click **Publish release**.
   The cloud build action will begin building the new module version for each architecture listed in your <file>meta.json</file>, and any machines configured to use the latest release of the module will receive the update once it has finished building.

See [Update an existing module using a GitHub action](/operate/modules/advanced/manage-modules/#update-automatically-from-a-github-repo-with-cloud-build) for more information.

{{% /tab %}}
{{% tab name="Manual PyInstaller build" %}}

From within the module directory, create a virtual Python environment with the necessary packages and then build an executable by running the setup and build scripts:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
sh setup.sh
sh build.sh
```

Run the `viam module upload` CLI command to upload the module to the registry.
If your module can only be run on Linux or macOS, for example due to platform-specific dependencies, replace `any` with `linux/any` or `darwin/any`, respectively.
If your module runs on all platforms, keep `any`:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam module upload --version 1.0.0 --platform any dist/archive.tar.gz
```

For details on platform support, see [Using the `--platform` argument](/dev/tools/cli/#using-the---platform-argument).

For details about versioning, see [Module versioning](/operate/modules/advanced/module-configuration/#module-versioning).

{{% alert title="Important" color="note" %}}
The `viam module upload` command only supports one `platform` argument at a time.
If you would like to upload your module with support for multiple platforms, you must run a separate `viam module upload` command for each platform.
Use the _same version number_ when running multiple `upload` commands of the same module code if only the `platform` support differs.
The Viam Registry page for your module displays the platforms your module supports for each version you have uploaded.
{{% /alert %}}

{{% /tab %}}
{{< /tabs >}}

{{% alert title="Note" color="note" %}}

PyInstaller does not support relative imports in entrypoints (imports starting with `.`).
If you get `"ImportError: attempted relative import with no known parent package"`, set up a stub entrypoint as described on [GitHub](https://github.com/pyinstaller/pyinstaller/issues/2560).

In addition, PyInstaller does not support cross-compiling: you must compile your module on the target architecture you wish to support.
For example, you cannot run a module on a Linux `arm64` system if you compiled it using PyInstaller on a Linux `amd64` system.
Viam makes this easy to manage by providing a build system for modules.
Follow [these instructions](/dev/tools/cli/#using-the-build-subcommand) to automatically build for each system your module can support using Viam's [CLI](/dev/tools/cli/).

{{% /alert %}}

{{% /tab %}}
{{% tab name="Python: venv" %}}

You can use the following package and upload method if you opted not to enable cloud build when you ran `viam module generate`.

1. Package the module as an archive by running the following command from inside the module directory:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   tar -czf module.tar.gz run.sh setup.sh requirements.txt src meta.json
   ```

   where `run.sh` is your entrypoint file, `requirements.txt` is your pip dependency list file, and `src` is the directory that contains the source code of your module.

   This creates a tarball called <file>module.tar.gz</file>.

1. Run the `viam module upload` CLI command to upload the module to the registry.
   If your module can only be run on Linux or macOS, for example due to platform-specific dependencies, replace `any` with `linux/any` or `darwin/any`, respectively.
   If your module runs on all platforms, keep `any`:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   viam module upload --version 1.0.0 --platform any module.tar.gz
   ```

   For details on platform support, see [Using the `--platform` argument](/dev/tools/cli/#using-the---platform-argument).

   For details about versioning, see [Module versioning](/operate/modules/advanced/module-configuration/#module-versioning).

{{% alert title="Important" color="note" %}}
The `viam module upload` command only supports one `platform` argument at a time.
If you would like to upload your module with support for multiple platforms, you must run a separate `viam module upload` command for each platform.
Use the _same version number_ when running multiple `upload` commands of the same module code if only the `platform` support differs.
The Viam Registry page for your module displays the platforms your module supports for each version you have uploaded.
{{% /alert %}}

{{% /tab %}}
{{% tab name="Go" %}}

From within your module's directory, run the `viam module upload` CLI command to upload the module to the registry.
If your module can only be run on Linux or macOS, for example due to platform-specific dependencies, replace `<platform>` with `linux/amd64`, `linux/arm64`, or another [platform](/dev/tools/cli/#using-the---platform-argument).

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam module upload --version 1.0.0 --platform <platform> .
```

For details about versioning, see [Module versioning](/operate/modules/advanced/module-configuration/#module-versioning).

{{% alert title="Important" color="note" %}}
The `viam module upload` command only supports one `platform` argument at a time.
If you would like to upload your module with support for multiple platforms, you must run a separate `viam module upload` command for each platform.
Use the _same version number_ when running multiple `upload` commands of the same module code if only the `platform` support differs.
The Viam Registry page for your module displays the platforms your module supports for each version you have uploaded.
{{% /alert %}}

{{% /tab %}}
{{< /tabs >}}
{{% /tablestep %}}
{{% tablestep %}}

If you look at the [Viam Registry page](https://app.viam.com/registry) while logged into your account, you'll be able to find your module listed.

{{% /tablestep %}}
{{% tablestep %}}

If your module supports hardware, add the hardware name in the **Components & services** section on the module registry page under the heading **Supported hardware**.

{{% /tablestep %}}
{{< /table >}}

For information about updating modules, see [Update and manage modules you created](/operate/modules/advanced/manage-modules/).

## Use your uploaded module

Once your module is in the registry, you can use the registry version of your module on machines.
Configure it just as you would [configure any other component or service in the registry](/operate/modules/configure-modules/#configure-hardware-or-software-on-your-machine):

1. Go to your machine's **CONFIGURE** tab.

1. Click the **+** button.
1. Select **Component or service**, and search for and select your model.
   If you cannot find your new module, it may be private and not accessible to the {{< glossary_tooltip term_id="organization" text="organization" >}} you are in.
   Check that you are in an organization that can [access the module](/operate/modules/advanced/manage-modules/#change-module-visibility).

1. Click **Add module**.
1. Enter a name for your resource and click **Create**.
1. If the module has requires attributes, configure them.
1. Click **Save**.

Your module will now be added to your machine.

If you used a local module for testing, you can safely delete it.
