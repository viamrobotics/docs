---
title: "Configure your module and modular resource"
linkTitle: "Configure"
weight: 30
type: "docs"
tags: ["server", "rdk", "extending viam", "modular resources", "components", "services"]
description: "Use the Viam module system to implement custom resources that can be included in any Viam-powered robot."
no_list: true
---

Configure a module on your robot to make one or more modular resources available for configuration.

If you want to create your own modular resource, you must first follow [these steps](/extend/modular-resources/create/) to code your own module and generate an executable.
If you are using a pre-built modular resource, make sure you install the module and determine the filename of [the module's executable](/extend/modular-resources/create/#compile-the-module-into-an-executable).

Follow these steps to configure the module and modular resource:

1. [Save the executable](#make-sure-viam-server-can-access-your-executable) in a location your `viam-server` instance can access.
2. [Add a **module**](#configure-your-module) referencing this executable to the configuration of your robot.
3. [Add a new component or service](#configure-your-modular-resource) referencing the custom resource provided by the configured **module** to the configuration of your robot.

{{% alert title="Modules vs. modular resources" color="tip" %}}

A configured *module* can make one or more *modular resources* available for configuration.

{{% /alert %}}

### Make sure `viam-server` can access your executable

Ensure that your module executable is saved where the instance of `viam-server` behind your robot can read and execute it.

For example, if you are running `viam-server` on an Raspberry Pi, you'll need to save the module on the Pi's filesystem.

Obtain the real (absolute) path to the executable file on your computer/[board's](/components/board/) filesystem by running the following command in your terminal:

``` shell
realpath <path-to-your-module-directory>/<your-module>
```

### Configure your module

To configure your new *module* on your robot, navigate to the **Config** tab of your robot's page on [the Viam app](https://app.viam.com) and click on the **Modules** subtab.

The following properties are available for modules:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
`name` | string | **Required**| Name of the module you are registering. |
`executable_path` | string | **Required**| The robot's computer's filesystem path to the module executable. |

Add these properties to your module's configuration:

{{< tabs >}}
{{% tab name="Config Builder" %}}

![Creation of a new module in the Viam app config builder.](/program/img/modular-resources/module-ui-config.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "modules": [
    {
      "name": "<your-module-name>",
      "executable_path": "<path-on-your-filesystem-to/your-module-directory>/<your_executable.sh>"
    }
  ]
}
```

{{% /tab %}}
{{% /tabs %}}

### Configure your modular resource

Once you have configured a module as part of your robot configuration, you can add any number of the resources that module makes available to your robot by adding new components or services configured with your modular resources' new type or [model](/extend/modular-resources/key-concepts/#models).

The following properties are available for modular resources:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `namespace` | string | **Required** | The namespace of the [API](/extend/modular-resources/key-concepts/#apis) (the first part of the {{< glossary_tooltip term_id="api-namespace-triplet" text="API namespace triplet">}}). |
| `type` | string | **Required** | The subtype of the [API](/extend/modular-resources/key-concepts/#apis) (the third part of the {{< glossary_tooltip term_id="api-namespace-triplet" text="API namespace triplet">}}). |
| `name` | string | **Required** | What you want to name this instance of your modular resource. |
| `model` | string | **Required** | The full {{< glossary_tooltip term_id="model-namespace-triplet" text="model namespace triplet">}} of the modular resource's [model](/extend/modular-resources/key-concepts/#models). |
| `depends_on` | array | Optional | The `name` of components you want to confirm are available on your robot alongside your modular resource. Usually a [board](/components/board/). |

All standard properties for configuration, such as `attributes` and `depends_on`, are also supported for modular resources.
The `attributes` available vary depending on your implementation.

{{< tabs >}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "namespace": "<your-module-namespace>",
      "type": "<your-resource-type>",
      "model": "<model-namespace>:<model-family-name>:<model-name>",
      "name": "<your-module-name>",
      "depends_on": [],
    }
  ],
  "modules": [ ... ] // < INSERT YOUR MODULE CONFIGURATION >
}
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

The following is an example configuration for a base modular resource implementation.
The configuration adds `acme:demo:mybase` as a modular resource from the module `my_base`.
The custom model is configured as a component with the name "my-custom-base-1".
You can send commands to the base according to the Viam [base API](/components/base/#api):

```json {class="line-numbers linkable-line-numbers"}
{
    "components": [
        {
            "type": "board",
            "name": "main-board",
            "model": "pi"
        },
        {
        "type": "base",
        "name": "my-custom-base-1",
        "model": "acme:demo:mybase",
        "namespace": "rdk",
        "attributes": {},
        "depends_on": [ "main-board" ]
        }
    ],
    "modules": [
    {
      "name": "my-custom-base",
      "executable_path": "/home/my_username/my_base/run.sh"
    }
  ]
}
```

{{% /tab %}}
{{% /tabs %}}

## Next Steps

Now that you've configured a modular resource, test it with the [Control tab](/manage/fleet/#remote-control) and program it with the [Viam SDKs](/program/apis/).
