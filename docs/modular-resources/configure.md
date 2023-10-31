---
title: "Configure a module on your robot"
linkTitle: "Configure"
weight: 30
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
description: "Add and configure a module from the Viam registry on your robot."
no_list: true
aliases:
  - "/program/extend/modular-resources/configure/"
---

You can extend Viam by adding a module on your robot that provides one or more {{< glossary_tooltip term_id="resource" text="modular resources" >}} ([components](/components/) or [services](/services/)).

You can [add a module from the Viam registry](#add-a-module-from-the-viam-registry), or you can [add a local module](#local-modules).

See [Key Concepts of Modular Resource APIs](/modular-resources/key-concepts/) for more information.

## Add a module from the Viam registry

The [Viam registry](https://app.viam.com/registry) is a central repository of modules from both Viam and the robotics community that allows you to easily extend Viam's capabilities on your robot.

A module provides one or more {{< glossary_tooltip term_id="resource" text="modular resources" >}} (either a [component](/components/) or [service](/services/)).

Follow the instructions below depending on the type of modular resource you would like to add to your robot:

- [Add a modular component](#add-a-modular-component-from-the-viam-registry)
- [Add a modular service](#add-a-modular-service-from-the-viam-registry)

### Add a modular component from the Viam registry

To add a modular [component](/components/) from the Viam registry to your robot:

1. Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
1. Click on the **Components** subtab and click the **Create component** button.
1. Browse the list of available component types, and select the specific modular component you'd like to add.

   {{<imgproc src="modular-resources/configure/add-component-by-category.png" resize="400x" declaredimensions=true alt="The add a component modal showing results for the intel realsense module when searching by the category 'camera'">}}

   You can also start typing to search for a module by name or to narrow down your search results.

   {{<imgproc src="modular-resources/configure/add-component-by-name.png" resize="400x" declaredimensions=true alt="The add a component modal showing results for the intel realsense module when searching by the name 'realsense'">}}

1. After selecting the modular component, click the **Add module** button, enter a name for your modular component, and click **Create** to add it to your robot.

   {{<imgproc src="modular-resources/configure/add-component-screen.png" resize="400x" declaredimensions=true alt="The add a component modal showing the intel realsense module pane, with the 'Add module' button shown">}}

   Be sure the modular component you select supports the [platform](/manage/cli/#using-the---platform-argument) you intend to use it with, such as `linux arm64`.
   You can see which platforms the module supports at bottom of the module information screen before you add it.

When you add a module from the Viam registry, the custom modular component it provides appears under the **Components** subtab like any other component.
You can also find [the module itself](#configure-a-module-from-the-viam-registry) listed as **Deployed** under the **Modules** subtab.

If the module requires you to configure specific **Attributes**, click the **URL** link in the [module's configuration pane](#configure-a-module-from-the-viam-registry) to view the specific attribute requirements on the module's GitHub page.

To delete a module added from the Viam registry, click the trash can icon in the upper-right corner of the module configuration pane in the **Modules** subtab of the robot's **Config** tab.
Deleting a module _does not_ delete any configured modular resources it provides.

### Add a modular service from the Viam registry

To add a modular [service](/services/) from the Viam registry to your robot:

1. Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
1. Click on the **Services** subtab and click the **Create service** button.
1. Browse the list of available service types and select the specific modular service you'd like to add.

   {{<imgproc src="modular-resources/configure/add-service-by-category.png" resize="400x" declaredimensions=true alt="The add a component modal showing results for the mlmodelservice triton module when searching by the category 'ML Model'">}}

   You can also start typing to search for a module by name or to narrow down your search results.

   {{<imgproc src="modular-resources/configure/add-service-by-name.png" resize="400x" declaredimensions=true alt="The add a component modal showing results for the mlmodelservice triton module when searching by the name 'triton'">}}

1. After selecting the modular service, click the **Add module** button, enter a name for your modular service, and click **Create** to add it to your robot.

   {{<imgproc src="modular-resources/configure/add-service-screen.png" resize="400x" declaredimensions=true alt="The add a component modal showing the mlmodelservice triton module pane, with the 'Add module' button shown">}}

   Be sure the modular service you select supports the [platform](/manage/cli/#using-the---platform-argument) you intend to use it with, such as `linux arm64`.
   You can see which platforms the module supports at bottom of the module information screen before you add it.

When you add a module from the Viam registry, the custom modular service it provides appears under the **Services** subtab like any other service.
You can also find [the module itself](#configure-a-module-from-the-viam-registry) listed as **Deployed** under the **Modules** subtab.

If the module requires you to configure specific **Attributes**, click the **URL** link in the [module's configuration pane](#configure-a-module-from-the-viam-registry) to view the specific attribute requirements on the module's GitHub page.

To delete a module added from the Viam registry, click the trash can icon in the upper-right corner of the module configuration pane in the **Services** tab.
Deleting a module _does not_ delete any configured modular resources it provides.

## Configure a module from the Viam registry

Once you have added a modular resource to your robot, you can view and configure the module itself from the **Modules** subtab:

1. Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
1. Click on the **Modules** subtab.
   All modules you have added to your robot appear under the **Deployed** section.

This pane lists the models provided by the module, any [components](/components/) or [services](/services/) on your robot that are currently using the module, and allows you to configure [how the module updates](#configure-version-update-management-for-a-registry-module) when a new version is available from the Viam registry.

{{<imgproc src="modular-resources/configure/deployed-module-with-component.png" resize="1000x" declaredimensions=true alt="The module subtab of the config tab showing the realsense custom module configuration pane includes the update management section showing version update management options version type, set to Patch (X.Y.Z) and version set to 0.0.3">}}

### Configure version update management for a registry module

When you add a module to your robot, you can also configure how that module updates itself when a newer version becomes available from the Viam registry.
By default, a newly-added module is set to pin to the specific patch release (**Patch (X.Y.Z)**) of the version you added, meaning that the module will _never automatically update itself_.

If you wish to allow automatic module updates when a new version of the module becomes available in the Viam registry, you can set the **Version type** for your module in the **Modules** subtab.
Updating to a newer version of a module brings new functionality and bug fixes, but requires restarting the module to apply the update.
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

When using the **Patch (X.Y.Z)** version type, you may select any patch version of the module from the **Version** drop down menu, including past versions if desired.

The current deployed version of your module and the latest version of that module available from the Viam registry are shown on this pane for your reference.

{{% alert title="Caution" color="caution" %}}
For any version type other than **Patch (X.Y.Z)**, the module will upgrade as soon as an update that matches that specified version type is available, which will **restart the module**.
If, for example, the module provides a motor component, and the motor is running, it will stop while the module upgrades.
{{% /alert %}}

### Create a new modular resource from a registry module

Once you have [added a module](#add-a-module-from-the-viam-registry) from the Viam registry, you can add any number of the modular resources it provides to your robot by adding new components or services configured with your modular resources' [model](/modular-resources/key-concepts/#models).

The following properties are available for modular resources:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `namespace` | string | **Required** | The namespace of the API (the first part of the {{< glossary_tooltip term_id="api-namespace-triplet" text="API namespace triplet">}}). See [Valid APIs to implement in your model](/modular-resources/key-concepts/#valid-apis-to-implement-in-your-model) |
| `type` | string | **Required** | The {{< glossary_tooltip term_id="subtype" text="subtype">}} of the API (the third part of the {{< glossary_tooltip term_id="api-namespace-triplet" text="API namespace triplet">}}). See [Valid APIs to implement in your model](/modular-resources/key-concepts/#valid-apis-to-implement-in-your-model). |
| `name` | string | **Required** | What you want to name this instance of your modular resource. |
| `model` | string | **Required** | The full {{< glossary_tooltip term_id="model-namespace-triplet" text="model namespace triplet">}} of the modular resource's [model](/modular-resources/key-concepts/#models). |
| `depends_on` | array | Optional | The `name` of components you want to confirm are available on your robot alongside your modular resource. Often a [board](/components/board/). Unnecessary if you coded [implicit dependencies](/modular-resources/key-concepts/#dependency-management). |

All standard properties for configuration, such as `attributes` and `depends_on`, are also supported for modular resources.
The `attributes` available vary depending on your implementation.
If the module requires you to configure specific **Attributes**, click the **URL** link in the module's configuration pane to view the specific attribute requirements on the module's GitHub page.

{{< tabs >}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-model-instance-name>",
      "model": "<namespace>:<repo-name>:<name>",
      "type": "<your-resource-subtype>",
      "namespace": "<your-module-namespace>",
      "attributes": {},
      "depends_on": []
    }
  ],
  "modules": [
    {
      "type": "registry",
      "name": "<module-name>",
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
The custom model is configured as a component with the name "my-realsense".

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "my-realsense",
      "model": "viam:camera:realsense",
      "type": "camera",
      "namespace": "rdk",
      "attributes": {},
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

## Local modules

If you wish to add a module to your robot without uploading it to the Viam registry, you can add your module as a _local module_.

You can add your own custom modules as local modules, or you can add pre-built modules written by other Viam users.

### Prepare a local module

First determine the module you wish to add as a local module:

- If you are adding your own custom module, be sure that you have followed the steps to [create your own module](/modular-resources/create/) to code and compile your module and generate an executable.
- If you are using a pre-built module, make sure you have installed the module and determined the filename of [the module's executable](/modular-resources/create/#compile-the-module-into-an-executable).

Then, ensure that `viam-server` is able to find and run the executable:

- Ensure that the module executable is saved to a location on the filesystem of your robot that `viam-server` can access.
  For example, if you are running `viam-server` on an Raspberry Pi, you must save the module executable on the Pi's filesystem.
- Ensure that this file is executable (runnable) with the following command:

  ```shell
  sudo chmod a+rx <path-to-your-module-executable>
  ```

See the instructions to [compile your module into an executable](/modular-resources/create/#compile-the-module-into-an-executable) for more information.

### Add a local module

To add a local module on your robot:

1. Navigate to the **Config** tab of your robot's page on [the Viam app](https://app.viam.com).

   - If you are adding a modular [component](/components/), click the **Components** subtab and click **Create component**.
   - If you are adding a modular [service](/services/), click the **Services** subtab and click **Create service**.

1. Then, select the `local modular resource` type from the list.

   {{<imgproc src="modular-resources/configure/add-local-module-list.png" resize="300x" declaredimensions=true alt="The add a component modal showing the list of components to add with 'local modular resource' shown at the bottom">}}

1. On the next screen:

   - Select the type of modular resource provided by your module, such as a [camera](/components/camera/), from the drop down menu.
   - Enter the {{< glossary_tooltip term_id="model-namespace-triplet" text="model namespace triplet">}} of your modular resource's [model](/modular-resources/key-concepts/#models).
     If you are adding a pre-built modular resource, the model triplet should be provided for you in the module's documentation.
   - Enter a name for this instance of your modular resource.
     This name must be different from the module name.

   {{<imgproc src="modular-resources/configure/add-local-module-create.png" resize="400x" declaredimensions=true alt="The add a component modal showing the create a module step for an intel realsense module">}}

1. Click **Create** to create the modular resource provided by the local module.

You can also add the module directly, without first adding its modular component or service:

1. Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
1. Click on the **Modules** subtab.
1. Scroll to the **Add local module** section.
1. Enter a **Name** for this instance of your modular resource.
1. Enter the [module's executable path](/modular-resources/create/#compile-the-module-into-an-executable).
   This path must be the absolute path to the executable on your robot's filesystem.
1. Then, click the **Add module** button, and click **Save config**.

   {{<imgproc src="modular-resources/configure/add-local-module-csi-cam.png" resize="600x" declaredimensions=true alt="The add a local module pane with name 'my-csi-ca' and executable path '/usr/local/bin/viam-csi'">}}

   This example shows the configuration for adding a [CSI camera](/modular-resources/examples/csi/) as a local module.

## Configure a local module

Once you have added a modular resource to your robot, you can view and configure the module itself from the **Modules** subtab:

1. Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
1. Click on the **Modules** subtab.
   Local modules you have added to your robot appear under the **Local** section.

The following properties are available for modules:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
`name` | string | **Required**| Name of the module you are registering. |
`executable_path` | string | **Required**| The absolute path to the executable on your robot's filesystem. |
`type` | string | **Required**| Either `registry` or `local`. |

Add these properties to your module's configuration:

{{< tabs >}}
{{% tab name="Config Builder" %}}

{{<imgproc src="modular-resources/configure/add-local-module-config-builder.png" resize="600x" declaredimensions=true alt="The add a local module pane with an example name and executable path">}}

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "modules": [
    {
      "name": "<your-module-name>",
      "executable_path": "<path-on-your-filesystem-to/your-module-directory>/<your_executable.sh>",
      "type": "local"
    }
  ]
}
```

{{% /tab %}}
{{% /tabs %}}

### Configure a modular resource

Once you have added a local module to your robot, you can add any number of the {{< glossary_tooltip term_id="resource" text="resources" >}} provided by that module to your robot by adding new components or services that use your modular resources' [model](/modular-resources/key-concepts/#models).

The following properties are available for modular resources:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `namespace` | string | **Required** | The namespace of the API (the first part of the {{< glossary_tooltip term_id="api-namespace-triplet" text="API namespace triplet">}}). See [Valid APIs to implement in your model](/modular-resources/key-concepts/#valid-apis-to-implement-in-your-model). |
| `type` | string | **Required** | The {{< glossary_tooltip term_id="subtype" text="subtype">}} of the API (the third part of the {{< glossary_tooltip term_id="api-namespace-triplet" text="API namespace triplet">}}). See [Valid APIs to implement in your model](/modular-resources/key-concepts/#valid-apis-to-implement-in-your-model). |
| `name` | string | **Required** | A custom name for this instance of your modular resource. |
| `model` | string | **Required** | The full {{< glossary_tooltip term_id="model-namespace-triplet" text="model namespace triplet">}} of the modular resource's [model](/modular-resources/key-concepts/#models). |
| `depends_on` | array | Optional | The `name` of components you want to confirm are available on your robot alongside your modular resource. Often a [board](/components/board/). Unnecessary if you coded [implicit dependencies](/modular-resources/key-concepts/#dependency-management). |

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
      "model": "<namespace>:<repo-name>:<name>",
      "name": "<your-model-instance-name>",
      "attributes": {},
      "depends_on": []
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
      "depends_on": ["main-board"]
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
