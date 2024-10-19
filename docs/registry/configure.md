---
title: "Modular Resources"
linkTitle: "Modular Resources"
weight: 10
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
description: "Integrate additional hardware or software functionality into your machine with modular resources."
no_list: true
icon: true
images: ["/registry/create-module.svg"]
aliases:
  - "program/extend/modular-resources/configure/"
  - "/extend/modular-resources/configure/"
  - "/modular-resources/configure/"
modulescript: true
---

Viam provides built-in support for a variety of {{< glossary_tooltip term_id="resource" text="resources" >}}:

- Various types of hardware {{< glossary_tooltip term_id="component" text="components" >}}.
- High-level functionality exposed as {{< glossary_tooltip term_id="service" text="services" >}}.

You can extend Viam beyond the built-in component and service models by adding a _{{< glossary_tooltip term_id="module" text="module" >}}_ on your machine.
A module provides one or more _{{< glossary_tooltip term_id="modular-resource" text="modular resources" >}}_, and is packaged to streamline deployment to a Viam machine.

{{< expand "How modules and modular resources work" >}}

To use a modular resource from the registry, add it from your machine's **CONFIGURE** tab in the Viam app, using the **+** button.

When you add a modular resource _from the registry_, the underlying module that provides it is automatically added at the same time.
To add a modular resource from a _local_ module, you must add the module first.

After adding a module to your machine, you can choose to [configure](/registry/configure/) it for automatic version updates from the Viam registry, or update your module manually.
By default, newly added modules will remain at the version they were when you installed them, and will not update automatically.

Once you have added and configured the module and corresponding modular resource you would like to use in the Viam app, you can test the modular resource using the [**CONTROL** tab](/fleet/control/) and program it using [standardized APIs](/appendix/apis/).

Modules run alongside [`viam-server`](/architecture/rdk/) as separate processes, communicating with `viam-server` over UNIX sockets.
When a module initializes, it registers its {{< glossary_tooltip term_id="model" text="model or models" >}} and associated [APIs](/appendix/apis/) with `viam-server`, making the new model available for use.
`viam-server` manages the [dependencies](/architecture/rdk/#dependency-management), [start-up](/architecture/rdk/#start-up), [reconfiguration](/architecture/rdk/#reconfiguration), [data management](/services/data/capture-sync/#configure-data-capture-and-sync), and [shutdown](/architecture/rdk/#shutdown) behavior of your modular resource.

{{< /expand >}}

## Browse existing modular resources

You can search the available modular resources from the Viam Registry here:

{{<all-modular-resources>}}

You can see details about each module in the [Viam registry](https://app.viam.com/registry) on its dedicated module page.
You can integrate modules into any Viam-powered machine.

## Create your own modular resources

If none of the existing modular resources in the Viam registry support your use case, you can create your own modules to provide your own modular resources.

You can write modules in a variety of programming languages, such as, Go, Python, C++, Rust, while implementing the same [APIs](/appendix/apis/) as the built-in components and services.

{{< cards >}}
{{% card link="/how-tos/create-module/" class="fit-contain" %}}
{{% card link="/how-tos/sensor-module/" class="fit-contain" %}}
{{< /cards >}}

## Add a modular resource to your machine

### Modular resource configuration

When you add components and services to your machine with the builder UI, you can select available modular resources from the Viam registry.
As you add them, Viam automatically also adds the module that provides the modular resource to your configuration.
The modular resource card allows you to configure attributes for the resource.
Check the module's GitHub Readme for information about available configuration attributes for a resource.
You can configure modules and their modular resources in the config builder or with JSON.

{{< tabs >}}
{{% tab name="Config Builder" %}}

The following image shows an example of a configured modular resource, specifically an ultrasonic sensor component.
This modular component is made available by the `ultrasonic` module, shown in the [next section](#module-configuration).

{{<imgproc src="registry/configure/ultrasonic-resource.png" resize="900x" style="width: 600px" declaredimensions=true alt="A configured modular resource example in the Viam app builder UI.">}}

{{% /tab %}}
{{% tab name="JSON" %}}

{{< tabs >}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
  "components": [
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
  ]
```

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
  "components": [
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
  ]
```

{{% /tab %}}
{{< /tabs >}}

The following properties are available for modular resources:

<!-- prettier-ignore -->
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `name` | string | **Required** | What you want to name this instance of your modular resource. |
| `namespace` | string | **Required** | The namespace of the API (the first part of the {{< glossary_tooltip term_id="api-namespace-triplet" text="API namespace triplet">}}). This will be `rdk` unless the module implements a [custom, non-standard API](/registry/advanced/). See [Valid API identifiers](/how-tos/create-module/#valid-api-identifiers). |
| `type` | string | **Required** | The {{< glossary_tooltip term_id="subtype" text="subtype">}} of the API (the third part of the {{< glossary_tooltip term_id="api-namespace-triplet" text="API namespace triplet">}}). See [Valid API identifiers](/how-tos/create-module/#valid-api-identifiers). |
| `model` | string | **Required** | The full {{< glossary_tooltip term_id="model-namespace-triplet" text="model namespace triplet">}} of the modular resource's {{< glossary_tooltip term_id="model" text="model" >}}. |
| `depends_on` | array | Optional | The `name` of components you want to confirm are available on your machine alongside your modular resource. Often a [board](/components/board/). Unnecessary if you coded [implicit dependencies](/architecture/rdk/#dependency-management). |

{{% /tab %}}
{{< /tabs >}}

All standard properties for configuration, such as `attributes` and `depends_on`, are also supported for modular resources.
The attributes available vary depending on your implementation.
If the module requires you to configure specific attributes, click the **Readme** link in the module's configuration card to view the specific attribute requirements on the module's GitHub page.

### Module configuration

{{< tabs >}}
{{% tab name="Config Builder" %}}

The following image shows an example of a configured module in a machine's config.
This ultrasonic sensor modular component in the previous section is provided by the [module](https://app.viam.com/module/viam/ultrasonic) shown here.

{{<imgproc src="registry/configure/ultrasonic-module.png" resize="900x" style="width: 600px" declaredimensions=true alt="A configured module example in the Viam app builder UI.">}}

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
      "version": "<module-version>"
    }
  ]
}
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

The following is an example configuration for the [Intel Realsense module](https://app.viam.com/module/viam/realsense).
The configuration adds `viam:camera:realsense` as a modular resource from the module `viam:realsense`.
The custom model is configured as a component with the name `myRealsenseCamera1`.

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
| `version` | string | **Required** | <p>You can specify: <ul><li>a specific version (X.Y.Z) of the module to use</li><li>to pin the module version to the newest release, so your machine automatically updates to the latest version of the module that is available or to the latest patch release of a configured minor (X.Y.\_) or major (X.\_) version.</li></ul></p> |
| `type` | string | **Required** | `registry` or `local`, depending on whether the module is in the [Viam registry](https://app.viam.com/registry) or is only available [locally](/how-tos/create-module/#test-your-module-locally) on your computer. |
| `name` | string | **Required** | The module author's organization namespace, followed by an underscore, followed by the name of the module. `<module namespace>_<module name>` |
| `module_id` | string | **Required** | The module namespace, then a colon, then the name of the module. Identical to the first two pieces of the {{< glossary_tooltip term_id="model-namespace-triplet" text="model namespace triplet" >}} |

### Further configuration options

{{< expand "Configure version update management" >}}

You can configure how each module on your machine updates itself when a newer version becomes available from the Viam registry.
By default, a newly-added module is set to pin to the specific patch release (**Patch (X.Y.Z)**) of the version you added, meaning that the module will _never automatically update itself_.

To allow automatic module updates when a new version of the module becomes available in the Viam registry, set the **Pinned version type** for your module in its module card on the **CONFIGURE** tab.

{{<imgproc src="registry/configure/deployed-module-with-component.png" style="width: 400px" resize="500x" declaredimensions=true alt="The module card">}}

The following update options are available:

- **Patch (X.Y.Z)**: Do not update to any other version.
  This is the default.
- **Minor (X.Y.\*)**: Only update to newer patch releases of the same minor release branch.
  The module will automatically restart and update itself whenever new updates within the same minor release are available in the Viam registry.
  For example, use this option to permit a module with version `1.2.3` to update to version `1.2.4` or `1.2.5` but not `1.3.0` or `2.0.0`.
- **Major (X.\*)**: Only update to newer minor releases of the same major release branch.
  The module will automatically restart and update itself whenever new updates within the same major release are available in the Viam registry.
  For example, use this option to permit a module with version `1.2.3` to update to version `1.2.4` or `1.3.0` but not `2.0.0` or `3.0.0`.
- **Latest**: Always update to the latest version of this module available from the Viam registry as soon as a new version becomes available.

When using the **Patch (X.Y.Z)** version type, you may select any patch version of the module from the **Version** dropdown menu, including past versions if desired.

The current deployed version of your module and the latest version of that module available from the Viam registry are shown on this module card for your reference.

{{% alert title="Caution" color="caution" %}}
For any version type other than **Patch (X.Y.Z)**, the module will upgrade as soon as an update that matches that specified version type is available, which will **restart the module**.
If, for example, the module provides a motor component, and the motor is running, it will stop while the module upgrades.
{{% /alert %}}

{{< /expand >}}
{{< expand "Use environment variables with a registry module" >}}

Some modules require that you set specific environment variables as part of configuration.
You can click the **Readme** link in the upper-right corner of the module configuration card to view any specific requirements on the module's GitHub page.

Module environment variables can be either:

- Static string values, or
- References to a system environment variable.

For example, if your module requires a `MODULE_USER` environment variable, you can add it with the following configuration:

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

Or if you are using a module that requires access to an additional program or library on your machine, you can create a `PATH` environment variable for that module:

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

This configures a module environment variable `PATH` that uses your system's `PATH` (which you can view by running `echo $PATH`) as a base, and adds one additional filesystem path: <file>/home/username/bin</file>.

The notation `${environment.<ENV-VAR-NAME>}` can be used to access any system environment variable that `viam-server` has access to, where `<ENV-VAR-NAME>` represents a system environment variable, like `PATH`, `USER`, or `PWD`.
For example, you can use `${environment.HOME}` to access the `HOME` environment variable for the user running `viam-server`.

To configure a modular resource with an environment variable, navigate to the **CONFIGURE** tab on your machine's page in the Viam app, select **JSON** mode, and add the following `env` configuration to the `modules` section:

{{< tabs >}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "modules": [
    {
      "type": "registry",
      "name": "<module-name>",
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

```json {class="line-numbers linkable-line-numbers"}
{
  "modules": [
    {
      "type": "registry",
      "name": "my-module",
      "module_id": "my-namespace:my-module",
      "version": "1.0.0",
      "env": {
        "PATH": "/home/username/bin:${environment.PATH}",
        "MY_USER": "username"
      }
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

To delete an environment variable configuration, delete the `env` section from your smart machine's configuration.

### Default environment variables

When a module is instantiated, it has access to the following default environment variables:

<!-- prettier-ignore -->
| Name | Description |
| ---- | ----------- |
| `VIAM_HOME` | The root of the `viam-server` configuration.<br>Default: `$HOME/.viam` |
| `VIAM_MODULE_ROOT` | The root of the module install directory. The module process uses this directory as its current working directory (`cwd`). This variable is useful for file navigation that is relative to the root of the module. If you are using a [local module](/how-tos/create-module/#test-your-module-locally), you must set this value manually if your module requires it.<br>Example: `/opt/my-module/verxxxx-my-module/` |
| `VIAM_MODULE_DATA` | A persistent folder location a module can use to store data across reboots and versions. This location is a good place to store [python virtual environments](/sdks/python/python-venv/).<br>Example: `$VIAM_HOME/module-data/cloud-machine-id/my-module-name/` |
| `VIAM_MODULE_ID` | The module ID of the module. <br>Example: `viam:realsense` |

{{< /expand >}}

## Next steps

Now that you've configured a modular resource, test it with the [**CONTROL** tab](/fleet/control/) and program it with the [Viam SDKs](/appendix/apis/).

You can also check out these tutorials that configure and use modular resources:

{{< cards >}}
{{% card link="/tutorials/projects/make-a-plant-watering-robot/" %}}
{{% card link="/tutorials/projects/integrating-viam-with-openai/" %}}
{{< /cards >}}
