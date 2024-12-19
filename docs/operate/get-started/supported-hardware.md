---
linkTitle: "Integrate supported hardware"
title: "Integrate supported hardware"
weight: 20
layout: "docs"
type: "docs"
no_list: true
description: "Use supported hardware with your machine."
modulescript: true
---

Viam supports a wide variety of sensors, cameras, motors, robotic arms, and other physical hardware.
Viam also supports various software services such as [data capture](/data-ai/get-started/capture-sync/), [computer vision](/data-ai/ai/create-dataset/), and [motion planning](/operate/mobility/move-arm/), designed to integrate seamlessly with the hardware driver modules.

Any hardware that is not already supported by a Viam {{< glossary_tooltip term_id="module" text="module" >}} can be added into Viam's system of modular resources by [creating a new module](../other-hardware/) that provides a driver for the hardware.
You can also create a module to support new software-only functionality.

In addition to physical hardware, there are "virtual" hardware modules that do not directly drive any physical hardware, but rather augment physical hardware with another layer of abstraction, or add functionality that has little to do with hardware, for example:

- [A "camera" that takes a camera feed from a physical camera, and crops it, overlays it, or otherwise transforms the output](/components/camera/transform/)
- [A "sensor" that allows you to designate a primary sensor and backup sensors in case of failure](https://github.com/viam-modules/failover)
- [A ChatGPT integration module](https://github.com/jeremyrhyde/chat-gpt-module)
- [A "sensor" that returns all active I2C addresses as sensor readings](https://github.com/michaellee1019/i2cdetect)

These software-only "hardware" modules implement the same [component APIs](/dev/reference/apis/#component-apis) as physical hardware modules.

{{% alert title="In this page" color="tip" %}}

- [What hardware is already supported?](#supported-hardware)
- [Add supported hardware to my machine's configuration](#configure-hardware-on-your-machine)

{{% /alert %}}

{{% alert title="See also" color="tip" %}}

- [Support other hardware by creating a new module](../other-hardware/)

{{% /alert %}}

## Supported hardware

Many modules are designed to run alongside the full version of [`viam-server`](/operate/get-started/setup/), which runs on 64-bit architectures such as single-board computers and laptop/desktop computers running 64-bit Linux, as well as macOS.

Other modules are designed to run on microcontrollers alongside `viam-micro-server`.

### For use with 64-bit architecture

The following modular components are available for computers and SBCs running `viam-server`.

Search for the name, model number, or manufacturer name of your hardware to see if there is already a hardware driver (_component {{< glossary_tooltip term_id="model" text="model" >}}_) for it.
Also try searching by broader category name, for example "webcam" or "motor," since some components do not require drivers that are specific to their exact make and model.

{{<resources api="rdk:component" no-intro="true">}}

{{% alert title="Info" color="tip" %}}
Some components are supported by drivers built into `viam-server`.
The list above contains both modular components and built-in components.
You can also browse these same built-in and modular registry components on your machine's configuration page in the Viam app.

The Viam Registry is the storage and distribution system for not just hardware modules but also software modules (called services), ML models, and ML model training scripts.
You can browse the [Viam Registry in the Viam app](https://app.viam.com/registry?type=Module).
{{% /alert %}}

### For use with microcontrollers

The following is a selection of components (some built-ins and some modules) written for use with `viam-micro-server`.
To use any of the built-in components, configure them according to their readmes.
To use a module with `viam-micro-server`, you need to [build firmware that combines `viam-micro-server` with one or more modules](/operate/get-started/other-hardware/micro-module).

<!--prettier-ignore-->
| Model | Description | Built-in |
| ----- | ----------- | -------- |
| `gpio` | A servo controlled by GPIO pins. [Configuration info](/components/servo/gpio-micro-rdk/). | Yes |
| `two_wheeled_base` | A robotic base with differential steering. [Configuration info](/components/base/two_wheeled_base/). | Yes |
| `free_heap_sensor` | Ships with `viam-micro-server`. [GitHub repo](https://github.com/viamrobotics/micro-rdk/tree/main/examples/modular-drivers/src). | No |
| `wifi_rssi_sensor` | Ships with `viam-micro-server`. [GitHub repo](https://github.com/viamrobotics/micro-rdk/tree/main/examples/modular-drivers/src). | No |
| `moisture_sensor` | [GitHub repo](https://github.com/viamrobotics/micro-rdk/tree/main/examples/modular-drivers/src). | No |
| `water_pump` | [GitHub repo](https://github.com/viamrobotics/micro-rdk/tree/main/examples/modular-drivers/src). | No |

## Configure hardware on your machine

After installing `viam-server` or `viam-micro-server` on your computer or microcontroller, you can configure hardware components on your machine's page in the [Viam app](https://app.viam.com):

1. Click the **+** button on your machine's **CONFIGURE** tab.
1. Click **Component**, then select from available components from the Viam Registry (as well as built-in resources).
1. Use the link to the module README to find information on configuring that specific component.

   {{<gif webm_src="/integrate/configure.webm" mp4_src="/integrate/configure.mp4" alt="Configuring a board and ultrasonic sensor." max-width="600px">}}

   When you add a modular resource _from the registry_, the module that provides it is automatically added at the same time, generating a configuration card for the modular resource and a separate one for the module.
   If you add a built-in component, there will only be a configuration card for the component.

### Modular resource configuration details

The modular resource card allows you to configure attributes for the resource.

{{< tabs >}}
{{% tab name="Config Builder" %}}

The following image shows an example of a configured modular resource, specifically an ultrasonic sensor component.
This modular component is made available by the `ultrasonic` module.
See [module configuration](#module-configuration).

{{<imgproc src="registry/modular-resources/ultrasonic-resource.png" resize="900x" style="width: 600px" declaredimensions=true alt="A configured modular resource example in the Viam app builder UI.">}}

{{% /tab %}}
{{% tab name="JSON" %}}

{{< tabs >}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "sensor-1",
  "model": "viam:ultrasonic:sensor",
  "type": "sensor",
  "namespace": "rdk",
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
  "model": "<namespace>:<repo-name>:<name>",
  "type": "<your-resource-subtype>",
  "namespace": "<your-module-namespace>",
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
| `namespace` | string | **Required** | The namespace of the API (the first part of the {{< glossary_tooltip term_id="api-namespace-triplet" text="API namespace triplet">}}). This will be `rdk` unless the module implements a [custom, non-standard API](/registry/advanced/). See [Valid API identifiers](/how-tos/create-module/#valid-api-identifiers). |
| `type` | string | **Required** | The {{< glossary_tooltip term_id="subtype" text="subtype">}} of the API (the third part of the {{< glossary_tooltip term_id="api-namespace-triplet" text="API namespace triplet">}}). See [Valid API identifiers](/how-tos/create-module/#valid-api-identifiers). |
| `model` | string | **Required** | The full {{< glossary_tooltip term_id="model-namespace-triplet" text="model namespace triplet">}} of the modular resource's {{< glossary_tooltip term_id="model" text="model" >}}. |
| `depends_on` | array | Optional | The `name` of components you want to confirm are available on your machine alongside your modular resource. Often a [board](/components/board/). Unnecessary if you coded [implicit dependencies](/architecture/viam-server/#dependency-management). |

### Module configuration details

{{< tabs >}}
{{% tab name="Config Builder" %}}

The following image shows an example of a configured module in a machine's config.
This ultrasonic sensor in the previous section is provided by the [`ultrasonic` module](https://app.viam.com/module/viam/ultrasonic) shown here.

{{<imgproc src="registry/modular-resources/ultrasonic-module.png" resize="900x" style="width: 600px" declaredimensions=true alt="A configured module example in the Viam app builder UI.">}}

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
      "version": "latest"
    },
    {
      "type": "registry",
      "name": "viam_raspberry-pi",
      "module_id": "viam:raspberry-pi",
      "version": "1.1.0"
    },
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
      "model": "<module-namespace>:<repo-name>:<name>",
      "type": "<your-resource-subtype>",
      "namespace": "<model-API-namespace>",
      "attributes": {},
      "depends_on": []
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
      "type": "camera",
      "namespace": "rdk",
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
      "version": "0.0.3"
    }
  ]
}
```

{{% /tab %}}
{{% /tabs %}}

{{% /tab %}}
{{< /tabs >}}

The following properties are configurable for each module:

<!--prettier-ignore-->
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `version` | string | **Required** | <p>You can specify: <ul><li>a specific version (X.Y.Z) of the module to use</li><li>to pin the module version to the newest release, so your machine automatically updates to the latest version of the module that is available or to the latest patch release of a configured minor (X.Y.\_) or major (X.\_) version.</li></ul>For more information, see [Module versioning](/registry/modular-resources/#module-versioning).</p> |
| `type` | string | **Required** | `registry` or `local`, depending on whether the module is in the [Viam Registry](https://app.viam.com/registry) or is only available [locally](/how-tos/create-module/#test-your-module-locally) on your computer. |
| `module_id` | string | **Required** | The module author's organization namespace or UUID, then a colon, then the name of the module. Identical to the first two pieces of the {{< glossary_tooltip term_id="model-namespace-triplet" text="model namespace triplet" >}}. `<module namespace>:<module name>`. |
| `name` | string | **Required** | A name for this instance of the module. |
| `env` | object | Optional | Environment variables available to the module. For example `{ "API_KEY": "${environment.API_KEY}" }`. Some modules require that you set environment variables as part of configuration. Check the module's readme for more information. See [environments variables](#environment-variables). |

#### Module versioning

You can configure how each module on your machine updates itself when a newer version becomes available from the Viam Registry.
By default, a newly-added module is set to pin to the specific patch release (**Patch (X.Y.Z)**) of the version you added, meaning that the module will _never automatically update itself_.

To allow automatic module updates when a new version of the module becomes available in the Viam Registry, set the **Pinned version type** for your module in its module card on the **CONFIGURE** tab.

{{<imgproc src="registry/modular-resources/deployed-module-with-component.png" style="width: 400px" resize="500x" declaredimensions=true alt="The module card">}}

The following update options are available:

- **Patch (X.Y.Z)**: Do not update to any other version.
  This is the default.
- **Minor (X.Y.\*)**: Only update to newer patch releases of the same minor release branch.
  The module will automatically restart and update itself whenever new updates within the same minor release are available in the Viam Registry.
  For example, use this option to permit a module with version `1.2.3` to update to version `1.2.4` or `1.2.5` but not `1.3.0` or `2.0.0`.
- **Major (X.\*)**: Only update to newer minor releases of the same major release branch.
  The module will automatically restart and update itself whenever new updates within the same major release are available in the Viam Registry.
  For example, use this option to permit a module with version `1.2.3` to update to version `1.2.4` or `1.3.0` but not `2.0.0` or `3.0.0`.
- **Latest (`latest`)**: Always update to the latest version of this module available from the Viam Registry as soon as a new version becomes available.
- **Latest with prerelease (`latest-with-prerelease`)**: Always update to the latest release or prerelease version of this module available from the Viam Registry as soon as the new version becomes available.

When using the **Patch (X.Y.Z)** version type, you may select any patch version of the module from the **Version** dropdown menu, including past versions if desired.

The current deployed version of your module and the latest version of that module available from the Viam Registry are shown on this module card for your reference.

{{% alert title="Caution" color="caution" %}}
For any version type other than **Patch (X.Y.Z)**, the module will upgrade as soon as an update that matches that specified version type is available, which will **restart the module**.
If, for example, the module provides a motor component, and the motor is running, it will stop while the module upgrades.
{{% /alert %}}

#### Environment variables

Each module has access to the following default environment variables:

<!-- prettier-ignore -->
| Name | Description |
| ---- | ----------- |
| `VIAM_HOME` | The root of the `viam-server` configuration.<br>Default: `$HOME/.viam` |
| `VIAM_MODULE_ROOT` | The root of the module install directory. The module process uses this directory as its current working directory (`cwd`). This variable is useful for file navigation that is relative to the root of the module. If you are using a [local module](/how-tos/create-module/#test-your-module-locally), you must set this value manually if your module requires it.<br>Example: `/opt/my-module/verxxxx-my-module/` |
| `VIAM_MODULE_DATA` | A persistent folder location a module can use to store data across reboots and versions. This location is a good place to store [python virtual environments](/sdks/python/python-venv/).<br>Example: `$VIAM_HOME/module-data/cloud-machine-id/my-module-name/` |
| `VIAM_MODULE_ID` | The module ID of the module. <br>Example: `viam:realsense` |

You can also set additional environment variables.

{{% expand "Example: string value" %}}

Set the environment variable `MODULE_USER`:

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

{{% /expand%}}

Use the notation `${environment.<ENV-VAR-NAME>}` to access any system environment variable that `viam-server` has access to, where `<ENV-VAR-NAME>` represents a system environment variable, like `PATH`, `USER`, or `PWD`.
For example, you can use `${environment.HOME}` to access the `HOME` environment variable for the user running `viam-server`.

{{% expand "Example: system variable" %}}

To set the path to a program or library on a machine, you can set a system variable:

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

{{% /expand%}}

## How modules run

Modules run alongside [`viam-server`](/architecture/viam-server/) as separate processes, communicating with `viam-server` over UNIX sockets.
When a module initializes, it registers its {{< glossary_tooltip term_id="model" text="model or models" >}} and associated [APIs](/appendix/apis/) with `viam-server`, making the new model available for use.
`viam-server` manages the [dependencies](/architecture/viam-server/#dependency-management), [start-up](/architecture/viam-server/#start-up), [reconfiguration](/architecture/viam-server/#reconfiguration), [data management](/services/data/#configuration), and [shutdown](/architecture/viam-server/#shutdown) behavior of your modular resource.
