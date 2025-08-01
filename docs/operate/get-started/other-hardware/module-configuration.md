---
title: "Modular resource and module configuration"
linkTitle: "Module configuration"
weight: 40
type: docs
icon: true
description: "Configure module versions and module environment variables."
aliases:
  - /operate/reference/module-configuration/
# date: "2022-01-01"
# updated: ""  # When the content was last entirely checked
prev: /operate/get-started/other-hardware/manage-modules/
next: /operate/get-started/other-hardware/lifecycle-module/
---

This page contains reference material.
For quick instructions on configuring a module on your machine, see [Configure hardware on your machine](/operate/get-started/supported-hardware/#configure-hardware-on-your-machine).

## Modular resource configuration details

The modular resource card allows you to configure attributes for the resource.

{{< tabs >}}
{{% tab name="Config Builder" %}}

The following image shows an example of a configured modular resource, specifically an ultrasonic sensor component.
This modular component is made available by the `ultrasonic` module.
See [module configuration](#module-configuration-details).

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
| `attributes` | object | Sometimes **Required** | Any configuration attributes for your model Check the module's GitHub Readme for information about available configuration attributes for a resource. |
| `name` | string | **Required** | What you want to name this instance of your modular resource. |
| `api` | string | **Required** | The {{< glossary_tooltip term_id="api-namespace-triplet" text="API namespace triplet">}}. |
| `model` | string | **Required** | The full {{< glossary_tooltip term_id="model-namespace-triplet" text="model namespace triplet">}} of the modular resource's {{< glossary_tooltip term_id="model" text="model" >}}. |
| `depends_on` | array | Optional | The `name` of resources you want to confirm are available on your machine alongside your modular resource. Unnecessary if you coded [implicit dependencies](/operate/get-started/other-hardware/create-module/dependencies/). |
| `notes` | string | Optional | Descriptive text to document the purpose, configuration details, or other important information about this modular resource. |

## Module configuration details

{{< tabs >}}
{{% tab name="Config Builder" %}}

The following image shows an example of a configured module in a machine's config.
This ultrasonic sensor in the previous section is provided by the [`ultrasonic` module](https://app.viam.com/module/viam/ultrasonic) shown here.

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
You can add and edit `env` by switching from **Builder** to **JSON** mode in the **CONFIGURE** tab.

<!--prettier-ignore-->
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `type` | string | **Required** | `registry` or `local`, depending on whether the module is in the [registry](https://app.viam.com/registry) or is only available [locally](/operate/get-started/other-hardware/create-module/#test-your-module-locally) on your computer. |
| `name` | string | **Required** | A name for this instance of the module. |
| `module_id` | string | **Required** | The module author's organization namespace or UUID, then a colon, then the name of the module. Identical to the first two pieces of the {{< glossary_tooltip term_id="model-namespace-triplet" text="model namespace triplet" >}}. `<module namespace>:<module name>`. Not applicable to local modules. |
| `version` | string | **Required** | <p>You can specify: <ul><li>a specific version (X.Y.Z) of the module to use</li><li>to pin the module version to the newest release, so your machine automatically updates to the latest version of the module that is available or to the latest patch release of a configured minor (X.Y.\_) or major (X.\_) version.</li></ul>For more information, see [Module versioning](/operate/get-started/other-hardware/module-configuration/#module-versioning).</p> |
| `env` | object | Optional | Environment variables available to the module. For example `{ "API_KEY": "${environment.API_KEY}" }`. Some modules require that you set environment variables as part of configuration. Check the module's readme for more information. See [environment variables](#environment-variables). |
| `executable_path` | string | Local modules only | The path to the module's executable file. Only applicable to, and required for, local modules. Registry modules use the `entrypoint` in the [<file>meta.json</file> file](/operate/get-started/other-hardware/create-module/metajson/) instead. |
| `disabled` | boolean | Optional | Whether to disable the module.<br>Default: `false`. |
| `notes` | string | Optional | Descriptive text to document the purpose, configuration details, or other important information about this module. |
| `log_level` | object | Optional | Set the log level for the module. See [Logging](/operate/reference/viam-server/#logging). |
| `tcp_mode` | boolean | Optional | Whether to start the module with a TCP connection. Regardless of the value set here, if the environment variable `VIAM_TCP_SOCKETS` is set to true, `viam-server` will start the module with a TCP connection.<br>TCP mode is currently only supported for Python and C++ modules.<br>Default: `false`.  |

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
- **Major (X.\*)**: Only update to newer minor releases of the same major release branch.
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

If a module appears in both a {{< glossary_tooltip term_id="fragment" text="fragment" >}} and the part configuration, or in multiple fragments, Viam will import the newest of the configured versions.

### Module meta.json configuration

When creating a module, you'll need to create a `meta.json` file that defines the module's properties. This file includes information about the module's ID, visibility, models, and other features.

Here's an example of a `meta.json` file:

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
  "first_run": "setup.sh"
}
```

For modules that include [Viam applications](/operate/control/viam-applications/), you can add the `applications` field:

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
  "applications": [
    {
      "name": "your-app-name",
      "type": "web",
      "entrypoint": "dist/index.html"
    }
  ]
}
```

The `applications` field is an array of application objects with the following properties:

| Property     | Type   | Description                                                                                       |
| ------------ | ------ | ------------------------------------------------------------------------------------------------- |
| `name`       | string | The name of your application, which will be used in the URL (`name.publicnamespace.viamapps.com`) |
| `type`       | string | The type of application (currently only `"web"` is supported)                                     |
| `entrypoint` | string | The path to the HTML entry point for your application                                             |

For more information about Viam applications, see the [Viam applications documentation](/operate/control/viam-applications/).

### Environment variables

Each module has access to the following default environment variables.
Not all of these variables are automatically available on [local modules](/operate/get-started/other-hardware/create-module/#test-your-module-locally); you can manually set variables your module requires if necessary.

<!-- prettier-ignore -->
| Name | Description | Automatically set on local modules? |
| ---- | ----------- | ----------------------------------- |
| `VIAM_HOME` | The root of the `viam-server` configuration.<br>Default for Linux, macOS, and WSL: <file>$HOME/.viam</file><br>Default for Windows: <file>C:\WINDOWS\system32\config\systemprofile\\.viam</file> | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| `VIAM_MODULE_ROOT` | The root of the module install directory. The module process uses this directory as its current working directory (`cwd`). This variable is useful for file navigation that is relative to the root of the module.<br>Example: <file>/opt/my-module/verxxxx-my-module/</file> | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| `VIAM_RESOURCE_CONFIGURATION_TIMEOUT` | Duration that resources are allowed to configure or reconfigure.<br>Example: `4m0s`<br>Default: 1 minute. | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| `VIAM_MODULE_STARTUP_TIMEOUT` | Duration that modules are allowed to start up.<br>Example: `7m15s`<br>Default: 5 minutes. | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| `VIAM_MODULE_DATA` | A persistent folder location a module can use to store data across reboots and versions. This location is a good place to store [python virtual environments](/dev/reference/sdks/python/python-venv/).<br>Example: <file>$VIAM_HOME/module-data/cloud-machine-id/my-module-name/</file> | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
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

To configure a module that is uploaded to the Viam Registry but has [visibility](/operate/get-started/other-hardware/manage-modules/#change-module-visibility) set to **Unlisted**, you need to manually add the module to your configuration:

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
    "name": "jessamyhello-world",
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
    "name": "<module-namespace><module-name>",
    "module_id": "<module-namespace>:<module-name>",
    "version": "latest"
  }
]
```

{{% /tab %}}
{{< /tabs >}}
