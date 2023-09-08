---
title: "Configure a module on your robot"
linkTitle: "Configure"
weight: 30
type: "docs"
tags: ["server", "rdk", "extending viam", "modular resources", "components", "services"]
description: "Add and configure a module from the Viam Registry on your robot."
no_list: true
---

You can extend Viam by adding a module on your robot to make one or more modular resources available for configuration.
You can [add a module from the Viam Registry](#add-a-module-from-the-viam-registry), or you can [code your own module and add it to your robot locally](#add-a-local-module-to-your-robot).

A *module* makes one or more *modular resources* available for configuration.
See [Key Concepts of Modular Resource APIs](/extend/modular-resources/key-concepts/) for more information.

## Add a module from the Viam Registry

The Viam Registry is a central repository of modules from both Viam and the robotics community that allows you to easily extend Viam's capabilities on your robot.

To add a module from the Viam Registry to your robot:

1. Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
1. Click on the **Components** subtab and click the **Create component** button.
1. Enter the name of the module you would like to add to your robot.
   To find the name of a module you're interested in, you can:

   - Start typing to search for modules by name.
     Modules available from the Viam Registry will be listed under the `From Registry` section of the search results.
   - [Browse the Viam Registry](https://app.viam.com/modules) directly to search available modules.

   {{<imgproc src="extend/modular-resources/configure/add-module-from-registry.png" resize="400x" declaredimensions=true alt="The add a component modal showing results for the intel realsense module ">}}

1. After entering the name of the module that you would like to add to your robot, select the matching module in the search results and click the **Add module** button.

When you add a module from the Viam Registry, the custom modular component it provides appears under the **Components** subtab like any other component.
You can also find [the module itself](#configure-a-module-from-the-viam-registry) listed as **Deployed** under the **Modules** subtab.

{{<imgproc src="extend/modular-resources/configure/conf-component-from-module.png" resize="400x" declaredimensions=true alt="The components subtab of the config tab showing the camera component configuration pane for the realsense module">}}

If the module requires you to configure specific **Atrributes**, click the **URL** link in the module's configuration pane to view the specific documentation on the module's GitHub page.

To delete a module added from the Viam Registry, click the trash can icon in the upper-right corner of the module configuration pane in the **Components** tab.

### Configure a module from the Viam Registry

Once you have added a module from the Viam Registry, you can view and configure the module from the **Modules** subtab:

1. Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
1. Click on the **Modules** subtab.
   All modules you have added to your robot appear under the **Deployed** section.

This pane lists the models provided by the module, any [components](/components/) on your robot that are currently using those models, and allows you to configure [how the module updates](#configure-version-update-management-for-a-registry-module) when a new version is available from the Viam Registry.

{{<imgproc src="extend/modular-resources/configure/conf-module-from-registry.png" resize="1000x" declaredimensions=true alt="The module subtab of the config tab showing the realsense custom module configuration pane includes the update management section showing version update management options version type, set to Patch (X.Y.Z) and version set to 0.0.3">}}

#### Configure version update management for a Registry module

When you add a module to your robot, you can also configure how that module updates itself when a newer version becomes available from the Viam Registry.
By default, a newly-added module is set to pin to the specific patch release (**Patch (X.Y.Z)**) of the version you added, meaning that the module will *never automatically update itself*.

If you wish to allow automatic module updates when a new version of the module becomes available in the Viam Registry, you can set the **Version type** for your module in the **Modules** subtab.
Updating to a newer version of a module brings new functionality and bug fixes, but requires restarting the module to apply the update.
The following update options are available:

- **Patch (X.Y.Z)**: Do not update to any other version.
  This is the default.
- **Minor (X.Y.*)**: Only update to newer patch releases of the same minor release branch.
  The module will automatically restart and update itself whenever new updates within the same minor release are available in the Viam Registry.
  For example, use this option to permit a module with version `1.2.3` to update to version `1.2.4` or `1.2.5` but not `1.3.0` or `2.0.0`.
- **Major (X.*)**: Only update to newer minor releases of the same major release branch.
  The module will automatically restart and update itself whenever new updates within the same major release are available in the Viam Registry.
  For example, use this option to permit a module with version `1.2.3` to update to version `1.2.4` or `1.3.0` but not `2.0.0` or `3.0.0`.
- **Latest**: Always update to the latest version of this module available from the Viam Registry as soon as a new version becomes available.

When using the **Patch (X.Y.Z)** version type, you may select any patch version of the module from the **Version** drop down menu, including past versions if desired.

The current deployed version of your module and the latest version of that module available from the Viam Registry are shown on this pane for your reference.

{{% alert title="Caution" color="caution" %}}
For any version type other than **Patch (X.Y.Z)**, the module will upgrade as soon as an update that matches that specified version type is available, which will **restart the module**.
If, for example, the module provides a motor component, and the motor is running, it will stop while the module upgrades.
{{% /alert %}}

### Configure a modular resource from a Registry module

Once you have configured a module from the Viam Registry, you can add any number of the resources that the module makes available to your robot by adding new components or services configured with your modular resources' [model](/extend/modular-resources/key-concepts/#models).

The following properties are available for modular resources:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `namespace` | string | **Required** | The namespace of the API (the first part of the {{< glossary_tooltip term_id="api-namespace-triplet" text="API namespace triplet">}}). See [Valid APIs to implement in your model](/extend/modular-resources/key-concepts/#valid-apis-to-implement-in-your-model) |
| `type` | string | **Required** | The {{< glossary_tooltip term_id="subtype" text="subtype">}} of the API (the third part of the {{< glossary_tooltip term_id="api-namespace-triplet" text="API namespace triplet">}}). See [Valid APIs to implement in your model](/extend/modular-resources/key-concepts/#valid-apis-to-implement-in-your-model). |
| `name` | string | **Required** | What you want to name this instance of your modular resource. |
| `model` | string | **Required** | The full {{< glossary_tooltip term_id="model-namespace-triplet" text="model namespace triplet">}} of the modular resource's [model](/extend/modular-resources/key-concepts/#models). |
| `depends_on` | array | Optional | The `name` of components you want to confirm are available on your robot alongside your modular resource. Often a [board](/components/board/). Unnecessary if you coded [implicit dependencies](/extend/modular-resources/key-concepts/#dependency-management). |

All standard properties for configuration, such as `attributes` and `depends_on`, are also supported for modular resources.
The `attributes` available vary depending on your implementation.

{{< tabs >}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "namespace": "<your-module-namespace>",
      "type": "<your-resource-subtype>",
      "model": "<model-namespace>:<model-family>:<model-name>",
      "name": "<your-model-instance-name>",
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

## Add a local module to your robot

If you are developing your own modular resource, and intend to deploy it to your robot locally, first follow [these steps](/extend/modular-resources/create/) to code your own module and generate an executable.
If you are using a pre-built modular resource, make sure you install the module and determine the filename of [the module's executable](/extend/modular-resources/create/#compile-the-module-into-an-executable).

Follow these steps to configure a module and its modular resources locally:

1. [Save the executable](#make-sure-viam-server-can-access-your-executable) in a location your `viam-server` instance can access.
2. [Add a **module**](#configure-your-module) referencing this executable to the configuration of your robot.
3. [Add a new component or service](#configure-your-modular-resource) referencing the modular resource provided by the configured **module** to the configuration of your robot.

### Make sure `viam-server` can access your executable

Ensure that your module executable is saved where the instance of `viam-server` behind your robot can read and execute it.

For example, if you are running `viam-server` on an Raspberry Pi, you'll need to save the module on the Pi's filesystem.

Obtain the real (absolute) path to the executable file on your computer's filesystem by running the following command in your terminal:

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

{{< imgproc src="/program/modular-resources/module-ui-config.png" alt="Creation of a new module in the Viam app config builder." resize="1000x" >}}

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

Once you have configured a module as part of your robot configuration, you can add any number of the resources that the module makes available to your robot by adding new components or services configured with your modular resources' [model](/extend/modular-resources/key-concepts/#models).

The following properties are available for modular resources:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `namespace` | string | **Required** | The namespace of the API (the first part of the {{< glossary_tooltip term_id="api-namespace-triplet" text="API namespace triplet">}}). See [Valid APIs to implement in your model](/extend/modular-resources/key-concepts/#valid-apis-to-implement-in-your-model). |
| `type` | string | **Required** | The {{< glossary_tooltip term_id="subtype" text="subtype">}} of the API (the third part of the {{< glossary_tooltip term_id="api-namespace-triplet" text="API namespace triplet">}}). See [Valid APIs to implement in your model](/extend/modular-resources/key-concepts/#valid-apis-to-implement-in-your-model). |
| `name` | string | **Required** | A custom name for this instance of your modular resource. |
| `model` | string | **Required** | The full {{< glossary_tooltip term_id="model-namespace-triplet" text="model namespace triplet">}} of the modular resource's [model](/extend/modular-resources/key-concepts/#models). |
| `depends_on` | array | Optional | The `name` of components you want to confirm are available on your robot alongside your modular resource. Often a [board](/components/board/). Unnecessary if you coded [implicit dependencies](/extend/modular-resources/key-concepts/#dependency-management). |

All standard properties for configuration, such as `attributes` and `depends_on`, are also supported for modular resources.
The `attributes` available vary depending on your implementation.

{{< tabs >}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "namespace": "<your-module-namespace>",
      "type": "<your-resource-subtype>",
      "model": "<model-namespace>:<model-family>:<model-name>",
      "name": "<your-model-instance-name>",
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
