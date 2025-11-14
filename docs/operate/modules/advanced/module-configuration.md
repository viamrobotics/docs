---
title: "Modular resource and module configuration"
linkTitle: "Module configuration"
weight: 40
type: docs
icon: true
description: "Configure module versions and module environment variables."
aliases:
  - /operate/reference/module-configuration/
  - /operate/modules/other-hardware/module-configuration/
date: "2025-11-11"
---

This page contains detailed information on configuring modules and modular resources.
For an introduction to configuring a module on your machine, see [Configure registry modules](/operate/modules/configure-modules/#configure-hardware-or-software-on-your-machine) instead.

## Modular resource configuration details

In the Viam web UI, when you add a modular resource, it adds two cards to the UI: a module card and a resource card.
The modular resource card allows you to configure attributes for the resource.

If you switch to **{} JSON** mode, you can also configure the attributes in JSON.

{{< tabs >}}
{{% tab name="Config Builder" %}}

The resource card shows all configuration attributes for the resource.
For example:

{{<imgproc src="registry/modular-resources/ultrasonic-resource.png" resize="900x" style="width: 600px" declaredimensions=true alt="A configured modular resource example." class="shadow imgzoom" >}}

{{% /tab %}}
{{% tab name="JSON" %}}

{{< tabs >}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "sensor-1",
  "model": "viam:ultrasonic:sensor",
  "api": "rdk:component:sensor",
  "attributes": {
    "trigger_pin": "13",
    "echo_interrupt_pin": "15",
    "board": "board-1",
    "timeout_ms": 500
  },
  "depends_on": []
}
```

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-model-instance-name>",
  "model": "<namespace>:<module-name>:<model-name>",
  "api": "<model-API-namespace>:<component|service>:<model-name>",
  "attributes": {
    "<relevant attributes--see module Readme>"
  },
  "depends_on": []
}
```

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{< /tabs >}}

The following properties are available for modular resources:

<!-- prettier-ignore -->
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `attributes` | object | Sometimes **Required** | The configuration attributes for the resource model. Check the module's Readme for information about available configuration attributes for a resource. |
| `name` | string | **Required** | The name of the configured instance of the modular resource. The name can only contain letters, numbers, dashes, and underscores. Resource names must be unique across all {{< glossary_tooltip term_id="part" text="parts" >}} of a machine. In case of name collisions with resources from a remote, you can add a [`prefix` to the remote](/operate/reference/architecture/parts/#configure-a-remote-part). |
| `api` | string | **Required** | The colon-delimited triplet `namespace:type:subtype` identifying the component or service API. Example: `rdk:component:motor`. See [valid API identifiers](/operate/modules/advanced/metajson/#valid-api-identifiers) for more information. |
| `model`| string | **Required** | A unique colon-delimited triplet `namespace:module-name:model-name` identifying the resource model. See [valid model identifiers](/operate/modules/advanced/metajson/#valid-model-identifiers) for more information. |
| `depends_on`| array | Optional | Deprecated. Use [dependencies](/operate/modules/advanced/dependencies/) instead. The names of resources that must be available before this resource starts. |
| `notes` | string | Optional | Descriptive text to document the purpose, configuration details, or other important information about this modular resource. |

## Module configuration details

In the Viam web UI, when you add a modular resource, it adds two cards to the UI: a module card and a resource card.
The module card allows you to configure attributes for the module.

If you switch to **{} JSON** mode, you can also configure the attributes in JSON.

{{< tabs >}}
{{% tab name="Config Builder" %}}

The module card shows all configuration attributes for the module.
For example:

{{<imgproc src="registry/modular-resources/ultrasonic-module.png" resize="900x" style="width: 600px" declaredimensions=true alt="A configured module example." class="shadow imgzoom" >}}

{{% /tab %}}
{{% tab name="JSON" %}}

Examples:

```json {class="line-numbers linkable-line-numbers"}
  "modules": [
    {
      "type": "registry",
      "name": "viam_ultrasonic",
      "module_id": "viam:ultrasonic",
      "version": "0.0.2"
    },
    {
      "type": "registry",
      "name": "viam_tflite_cpu",
      "module_id": "viam:tflite_cpu",
      "version": "latest",
      "disabled": true
    },
    {
      "type": "registry",
      "name": "viam_raspberry-pi",
      "module_id": "viam:raspberry-pi",
      "version": "1.1.0"
    },
    {
      "type": "local",
      "name": "local-module-1",
      "executable_path": "/Users/jessamy/myFolderOfCode/my-control-logic/run.sh"
    }
  ]
```

The config of both a module and a corresponding modular resource resembles the following:

{{< tabs >}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-model-instance-name>",
      "model": "<module-namespace>:<module-name>:<model-name>",
      "api": "<model-API-namespace>:<component|service>:<model-name>",
      "attributes": {}
    }
  ],
  "modules": [
    {
      "type": "registry",
      "name": "<module-namespace>_<module-name>",
      "module_id": "<module-namespace>:<module-name>",
      "version": "<module-version>",
      "env": {
        "MY_VAR": "<some-value>",
        "PATH": "<example-folder>:${environment.PATH}"
      }
    }
  ]
}
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

The following is an example configuration for the [Intel Realsense module](https://app.viam.com/module/viam/realsense).
The configuration adds `viam:camera:realsense` as a modular resource from the module `viam:realsense`.
The model is configured as a component with the name `myRealsenseCamera1`.

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "myRealsenseCamera1",
      "model": "viam:camera:realsense",
      "api": "rdk:component:camera",
      "attributes": {
        "sensors": ["color", "depth"]
      },
      "depends_on": []
    }
  ],
  "modules": [
    {
      "type": "registry",
      "name": "viam_realsense",
      "module_id": "viam:realsense",
      "version": "0.0.11"
    }
  ]
}
```

{{% /tab %}}
{{% /tabs %}}

{{% /tab %}}
{{< /tabs >}}

The following properties are configurable for each module.

<!--prettier-ignore-->
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `type` | string | **Required** | `registry` or `local`, depending on whether the module is in the [registry](https://app.viam.com/registry) or is started [locally](/operate/modules/support-hardware/#test-your-module-locally) on the device. |
| `name` | string | **Required** | The name of the module. |
| `module_id` | string | **Required** | The module ID, which includes either the module namespace or organization ID, followed by its name: `<namespace>:<module-name>` or `<org-id>:<module-name>`. The `module_id` uniquely identifies your module. Identical to the first two pieces of the {{< glossary_tooltip term_id="model-namespace-triplet" text="model namespace triplet" >}}. |
| `version` | string | **Required** | <p>You can specify: <ul><li>to use a specific version (X.Y.Z) of the module</li><li>to pin the module version to the latest version, so your machine automatically updates to the latest version of the module that is available, or to the latest patch release of a configured minor (X.Y.\_) or major (X.\_) version.</li></ul>For more information, see [Module versioning](/operate/modules/advanced/module-configuration/#module-versioning).</p> |
| `env` | object | Optional | Environment variables available to the module. For example `{ "API_KEY": "${environment.API_KEY}" }`. Some modules require that you set environment variables as part of configuration. For more information, see [environment variables](#environment-variables). You can add and edit `env` by switching from **Builder** to **{} JSON** mode in the **CONFIGURE** tab. |
| `executable_path` | string | Local modules only | The path to the module's executable file. Only applicable to, and required for, local modules. Registry modules use the `entrypoint` in the [<file>meta.json</file> file](/operate/modules/advanced/metajson/) instead. |
| `disabled` | boolean | Optional | Whether to disable the module.<br>Default: `false`. |
| `notes` | string | Optional | Descriptive text to document the purpose, configuration details, or other important information about this module. |
| `log_level` | object | Optional | Set the log level for the module. See [Logging](/operate/reference/viam-server/#logging). |
| `first_run_timeout` | number | Optional | The timeout duration for the first run script.<br>Default: `60m`. |
| `tcp_mode` | boolean | Optional | Whether to start the module with a TCP connection. Regardless of the value set here, if the environment variable `VIAM_TCP_SOCKETS` is set to true, `viam-server` will start the module with a TCP connection.<br>TCP mode is currently only supported for Python and C++ modules.<br>Default: `false`. |

### Module versioning

You can configure how each module on your machine updates itself when a newer version becomes available from the Viam Registry.
By default, a newly-added module is set to pin to the latest release (**Latest**) of the version you added.

To change the update strategy for your module, set the **Pinned version type** for your module in its module card on the **CONFIGURE** tab.

{{<imgproc src="registry/modular-resources/ultrasonic-module.png" resize="900x" style="width: 600px" declaredimensions=true alt="A configured module example." class="shadow imgzoom" >}}

The following update options are available:

- **Patch (X.Y.Z)**: Do not update to any other version.
- **Minor (X.Y.\*)**: Only update to newer patch releases of the same minor release branch.
  The module will automatically restart and update itself whenever new updates within the same minor release are available in the Viam Registry.
  For example, use this option to permit a module with version `1.2.3` to update to version `1.2.4` or `1.2.5` but not `1.3.0` or `2.0.0`.
- **Major (X.\*)**: Only update to newer patch and minor releases of the same major release branch.
  The module will automatically restart and update itself whenever new updates within the same major release are available in the Viam Registry.
  For example, use this option to permit a module with version `1.2.3` to update to version `1.2.4` or `1.3.0` but not `2.0.0` or `3.0.0`.
- **Latest (`latest`)**: Always update to the latest version of this module available from the Viam Registry as soon as a new version becomes available.
  This is the default.
- **Latest with prerelease (`latest-with-prerelease`)**: Always update to the latest release or prerelease version of this module available from the Viam Registry as soon as the new version becomes available.

When using the **Patch (X.Y.Z)** version type, you may select any patch version of the module from the **Version** dropdown menu, including past versions if desired.

The current deployed version of your module and the latest version of that module available from the Viam Registry are shown on this module card for your reference.

{{% alert title="Caution" color="caution" %}}
For any version type other than **Patch (X.Y.Z)**, the module will upgrade as soon as an update that matches that specified version type is available, which will **restart the module**.
If, for example, the module provides a motor component, and the motor is running, it will stop while the module upgrades.
{{% /alert %}}

If a module appears in both a {{< glossary_tooltip term_id="fragment" text="fragment" >}} and the part configuration, or in multiple fragments, Viam imports the newest of the configured versions.

### Environment variables

Each module has access to the following default environment variables.
Not all of these variables are automatically available on [local modules](/operate/modules/support-hardware/#test-your-module-locally); you can manually set variables your module requires if necessary.

<!-- prettier-ignore -->
| Name | Description | Automatically set on local modules? |
| ---- | ----------- | ----------------------------------- |
| `VIAM_HOME` | The root of the `viam-server` configuration.<br>Default for Linux, macOS, and WSL: <file>$HOME/.viam</file><br>Default for Windows: <file>C:\WINDOWS\system32\config\systemprofile\\.viam</file> | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| `VIAM_MODULE_ROOT` | The root of the module install directory. The module process uses this directory as its current working directory (`cwd`). This variable is useful for file navigation that is relative to the root of the module.<br>Example: <file>/opt/my-module/verxxxx-my-module/</file> | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| `VIAM_RESOURCE_CONFIGURATION_TIMEOUT` | Duration that resources are allowed to configure or reconfigure.<br>Example: `4m0s`<br>Default: `2m0s`. | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| `VIAM_MODULE_STARTUP_TIMEOUT` | Duration that modules are allowed to start up.<br>Example: `7m15s`<br>Default: 5 minutes. | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| `VIAM_MODULE_DATA` | A persistent folder location a module can use to store data across reboots and version updates. The folder will be removed when the module is removed from the machine, including when disabled in the machine configuration. This location is a good place to store [python virtual environments](/dev/reference/sdks/python/python-venv/).<br>Example: <file>$VIAM_HOME/module-data/cloud-machine-id/my-module-name/</file> | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| `VIAM_MODULE_ID` | The module ID of the module.<br>Example: `viam:realsense` | |
| `VIAM_API_KEY` | An API key with access to the machine where this instance of the module is running. | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| `VIAM_API_KEY_ID` | The ID of the API key with access to the machine where this instance of the module is running. | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| `VIAM_MACHINE_PART_ID` | The ID of the part where this instance of the module is running. | |
| `VIAM_MACHINE_ID` | The ID of the machine where this instance of the module is running. | |
| `VIAM_MACHINE_FQDN` | The {{< glossary_tooltip term_id="machine-fqdn" text="fully qualified domain name" >}} of the machine where this instance of the module is running. | |
| `VIAM_LOCATION_ID` | The ID of the {{< glossary_tooltip term_id="location" text="location" >}} that owns the machine where this instance of the module is running. | |
| `VIAM_PRIMARY_ORG_ID` | The ID of the {{< glossary_tooltip term_id="organization" text="organization" >}} that owns the machine where this instance of the module is running. | |

#### Set additional environment variables

You can configure additional environment variables for your module, using your choice of variable name and value.
For example, you could create a variable `MODULE_USER` with a string value:

```json {class="line-numbers linkable-line-numbers"}
{
  "modules": [
    {
      ...
      "env": {
        "MODULE_USER": "my-username"
      }
    }
  ]
}
```

To access any system environment variable that `viam-server` has access to, use the notation `${environment.<ENV-VAR-NAME>}` where `<ENV-VAR-NAME>` represents a system environment variable, like `PATH`, `USER`, or `PWD`.
For example, you can use `${environment.HOME}` to access the `HOME` environment variable for the user running `viam-server`:

```json {class="line-numbers linkable-line-numbers"}
{
  "modules": [
    {
      ...
      "env": {
        "PATH": "/home/username/bin:${environment.PATH}"
      }
    }
  ]
}
```

#### Access environment variables from your module

You can access module environment variables from within your module code in the same way you would access any other environment variables.
For example, you could use the following Python code to access the `VIAM_HOME` variable:

```python
import os

viam_home = os.environ.get("VIAM_HOME")
```

## Configure an unlisted module

To configure a module that is uploaded to the Viam Registry but has [visibility](/operate/modules/advanced/manage-modules/#change-module-visibility) set to **Unlisted** (`public_unlisted`), you need to manually add the module to your configuration:

{{% hiddencontent %}}
A public unlisted module is the same as an unlisted module.
{{% /hiddencontent %}}

1. Navigate to the module's page in the Viam Registry, using the link to the module.

1. Find the **Unlisted module usage** section.

1. Copy the module configuration JSON snippet.

1. Navigate to the **CONFIGURE** tab of the machine you want to configure.

1. Switch to **JSON** mode.

1. Paste the copied module configuration into your `modules` array.

1. Copy the model configuration snippet for the model you want to use, and add it to your `components` or `services` array (as appropriate).
   For example:

   {{< tabs >}}
   {{% tab name="Example" %}}

```json {class="line-numbers linkable-line-numbers"}
"components": [
  {
    "name": "sensor-1",
    "api": "rdk:component:sensor",
    "model": "jessamy:hello-world:hello-camera",
    "attributes": {}
  },
  ...
],
"modules": [
  {
    "type": "registry",
    "name": "hello-world",
    "module_id": "jessamy:hello-world",
    "version": "latest"
  }
]
```

{{% /tab %}}
{{% tab name="Template" %}}

```json {class="line-numbers linkable-line-numbers"}
"<components|services>": [
  {
    "name": "<resource-name>",
    "api": "<model-API-namespace>:<component|service>:<model-name>",
    "model": "<module-namespace>:<module-name>:<model-name>",
    "attributes": {}
  }
],
"modules": [
  {
    "type": "registry",
    "name": "<module-name>",
    "module_id": "<module-namespace>:<module-name>",
    "version": "latest"
  }
]
```

{{% /tab %}}
{{< /tabs >}}

### Module meta.json configuration

Each module must have a `meta.json` file that defines the module's properties. This file includes information about the module's ID, visibility, models, and other features.

Example `meta.json` file:

```json
{
  "module_id": "your-namespace:your-module",
  "visibility": "public",
  "url": "https://github.com/your-org/your-repo",
  "description": "Your module description",
  "models": [
    {
      "api": "rdk:component:base",
      "model": "your-namespace:your-module:your-model"
    }
  ],
  "entrypoint": "run.sh",
  "first_run": "setup.sh",
  "applications": [
    {
      "name": "your-app-name",
      "type": "single_machine",
      "entrypoint": "dist/index.html",
      "fragmentIds": [],
      "logoPath": "static/logo.png",
      "customizations": {
        "machinePicker": {
          "heading": "Air monitoring dashboard",
          "subheading": "Sign in and select your devices to view your air quality metrics in a dashboard."
        }
      }
    }
  ]
}
```

<!-- prettier-ignore -->
| Property     | Type   | Description |
| ------------ | ------ | ----------- |
| `module_id` | string | The module ID, which includes either the module namespace or organization ID, followed by its name: `<namespace>:<module-name>` or `<org-id>:<module-name>`. The `module_id` uniquely identifies your module. |
| `visibility` | string | Whether the module is accessible only to members of your organization (`private`), visible to all Viam users (`public`), or unlisted (`public_unlisted`). |
| `url` | string | The URL of the GitHub repository containing the source code of the module. Required for cloud build. Optional for local modules. |
| `description` | string | The description of your module and what it provides. |
| `models` | array | An array of objects describing the models provided by your module. You must provide at least one model in the models array or one application in the applications array. |
| `entrypoint` | string | The name of the file that starts your module. This can be a compiled executable or a script. Required if you are shipping a model. |
| `first_run` | string | The path to a script or binary that `viam-server` executes during the setup phase. It executes once when `viam-server` receives a new configuration, and only once per module or per version of the module. |

For modules that include [Viam applications](/operate/control/viam-applications/), you can add the `applications` field.
The `applications` field is an array of application objects with the following properties:

<!-- prettier-ignore -->
| Property     | Type   | Description |
| ------------ | ------ | ----------- |
| `name`       | string | The name of your application, which will be used in the URL (`name.publicnamespace.viamapps.com`) |
| `type`       | string | The type of application: `"single_machine"` or `"multi_machine"`. Whether the application can access and operate one machine or multiple machines. |
| `entrypoint` | string | The path to the HTML entry point for your application                                             |
| `fragmentIds` | []string | Specify the fragment or fragments that a machine must contain to be selectable from the machine picker screen. Only for single machine applications. |
| `logoPath` | string | The URL or the relative path to the logo to display on the machine picker screen for a single machine application. |
| `customizations` | object | Override the branding heading and subheading to display on the authentication screen for single machine applications: <ul><li>`heading`: Override the heading. May not be longer than 60 characters. </li><li>`subheading`: Override the subheading. May not be longer than 256 characters.</li></ul> Example: `{ "heading": "Air monitoring dashboard", "subheading": "Sign in and select your devices to view your air quality metrics in a dashboard" }`. |

For more information about Viam applications, see the [Viam applications documentation](/operate/control/viam-applications/).
