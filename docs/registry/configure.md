---
title: "Find a Module for your Machine"
linkTitle: "Find modules"
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
description: "Add a modular resource to your machine by configuring it."
no_list: true
image: "/registry/create-module.svg"
imageAlt: "Find a module for your machine"
images: ["/registry/create-module.svg"]
aliases:
  - "program/extend/modular-resources/configure/"
  - "/extend/modular-resources/configure/"
  - "/modular-resources/configure/"
modulescript: true
---

You can extend Viam by adding a module on your machine that provides one or more {{< glossary_tooltip term_id="modular-resource" text="modular resources" >}} ([components](/components/) or [services](/services/)):

1. Add a {{< glossary_tooltip term_id="module" text="module" >}}, either one [from the registry](#add-a-modular-resource-from-the-viam-registry) or a [local module](#local-modules).
   This makes the modular resource available to the machine.
1. Then add the modular resource itself.

When you add a modular resource from the registry, the underlying module that provides it is automatically added at the same time.
To add a modular resource from a local module, you must add the module first.

You can search the available modular resources from the Viam Registry here:

<div id="searchbox"></div>
<p>
<div id="searchstats"></div></p>
<div class="mr-component" id="">
  <div class="modellistheader">
    <div class="type">API</div>
    <div class="name">Model</div>
    <div>Description</div>
  </div>
<div id="hits" class="modellist">
</div>
<div id="pagination"></div>
</div>

You can see details about each module in the [Viam registry](https://app.viam.com/registry) on its dedicated module page.
You can integrate modules into any Viam-powered machine.

## Add a modular resource from the Viam registry

The [Viam registry](https://app.viam.com/registry) is a central repository of modules from both Viam and the robotics community that allows you to easily extend Viam's capabilities on your machine.

A module provides one or more {{< glossary_tooltip term_id="resource" text="modular resources" >}} (either a [component](/components/) or [service](/services/)).

Follow the instructions below depending on the type of modular resource you would like to add to your machine:

- [Add a modular component](#add-a-modular-component-from-the-viam-registry)
- [Add a modular service](#add-a-modular-service-from-the-viam-registry)

{{< alert title="Note" color="note" >}}
If you are using a [rented Viam rover](/get-started/try-viam/), adding modules is disabled for security purposes.
{{< /alert >}}

### Add a modular component from the Viam registry

To add a modular [component](/components/) from the Viam registry to your machine:

1. Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
2. Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
3. Browse the list of available component types, and select the specific modular component you'd like to add.

   {{<imgproc src="registry/configure/add-component-by-category.png" resize="400x" declaredimensions=true alt="The add a component modal showing results for the intel realsense module when searching by the category 'camera'">}}

   You can also start typing to search for a module by name or to narrow down your search results.

   {{<imgproc src="registry/configure/add-component-by-name.png" resize="400x" declaredimensions=true alt="The add a component modal showing results for the intel realsense module when searching by the name 'realsense'">}}

4. After selecting the modular component, enter a name for your modular component and click **Create** to add it to your machine's component configuration.

   {{<imgproc src="registry/configure/add-component-screen.png" resize="400x" declaredimensions=true alt="The add a component modal showing the intel realsense module pane, with the 'Add module' button shown">}}

   Be sure the modular component you select supports the [platform](/fleet/cli/#using-the---platform-argument) you intend to use it with, such as `linux arm64`.
   You can see which platforms the module supports at bottom of the module information screen before you add it.

When you add a modular component from the registry, it appears on the **CONFIGURE** tab like any other component.

If the component requires you to configure specific **Attributes**, navigate to the **CONFIGURE** tab and hover over the component in the machine {{< glossary_tooltip term_id="part" text="part" >}} tree in the upper left-hand corner.
Click on the **...** menu and select **Go to homepage** to view the specific attribute requirements on the module's GitHub page.

To delete a modular component, navigate to the component's card on the **CONFIGURE** tab.
Click on the **...** and click **Delete**.
Confirm your selection.

### Add a modular service from the Viam registry

To add a modular [service](/services/) from the Viam registry to your machine:

1. Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
2. Click the **+** icon next to your machine part in the left-hand menu and select **Service**.
3. Browse the list of available service types and select the specific modular service you'd like to add.

   {{<imgproc src="registry/configure/add-service-by-category.png" resize="400x" declaredimensions=true alt="The add a component modal showing results for the mlmodelservice triton module when searching by the category 'ML Model'">}}

   You can also start typing to search for a module by name or to narrow down your search results.

   {{<imgproc src="registry/configure/add-service-by-name.png" resize="400x" declaredimensions=true alt="The add a component modal showing results for the mlmodelservice triton module when searching by the name 'triton'">}}

4. After selecting the modular service, enter a name for your modular service and click **Create** to add it to your machine's service configuration.

   {{<imgproc src="registry/configure/add-service-screen.png" resize="400x" declaredimensions=true alt="The add a component modal showing the mlmodelservice triton module pane, with the 'Add module' button shown">}}

   Be sure the modular service you select supports the [platform](/fleet/cli/#using-the---platform-argument) you intend to use it with, such as `linux arm64`.
   You can see which platforms the module supports at bottom of the module information screen before you add it.

When you add a modular service from the registry, it appears on the **CONFIGURE** tab like any other service.

If the component requires you to configure specific **Attributes**, navigate to the **CONFIGURE** tab and hover over the service in the machine {{< glossary_tooltip term_id="part" text="part" >}} tree in the upper left-hand corner.
Click on the **...** menu and select **Go to homepage** to view the specific attribute requirements on the module's GitHub page.

To delete a modular service, navigate to the service's card on the **CONFIGURE** tab.
Click on the **...** and click **Delete**.
Confirm your selection.

### Add additional modular resources from a registry module

Once you have [added a module](#add-a-modular-resource-from-the-viam-registry) from the Viam registry, you can add any number of the modular resources it provides to your machine by adding new components or services configured with your modular resource's {{< glossary_tooltip term_id="model" text="model" >}}.

Follow the same steps as when you added the first modular resource, clicking **Create** and **Component** or **Service** as applicable.
You will be prompted to click **Add module** again while configuring the resource, though no duplicate module will be added to the `modules` section of the configuration.

If you prefer to use JSON, the following properties are available for modular resources:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `namespace` | string | **Required** | The namespace of the API (the first part of the {{< glossary_tooltip term_id="api-namespace-triplet" text="API namespace triplet">}}). See [Valid APIs to implement in your model](/registry/#valid-apis-to-implement-in-your-model) |
| `type` | string | **Required** | The {{< glossary_tooltip term_id="subtype" text="subtype">}} of the API (the third part of the {{< glossary_tooltip term_id="api-namespace-triplet" text="API namespace triplet">}}). See [Valid APIs to implement in your model](/registry/#valid-apis-to-implement-in-your-model). |
| `name` | string | **Required** | What you want to name this instance of your modular resource. |
| `model` | string | **Required** | The full {{< glossary_tooltip term_id="model-namespace-triplet" text="model namespace triplet">}} of the modular resource's {{< glossary_tooltip term_id="model" text="model" >}}. |
| `depends_on` | array | Optional | The `name` of components you want to confirm are available on your machine alongside your modular resource. Often a [board](/components/board/). Unnecessary if you coded [implicit dependencies](/internals/rdk/#dependency-management). |

All standard properties for configuration, such as `attributes` and `depends_on`, are also supported for modular resources.
The `attributes` available vary depending on your implementation.
If the module requires you to configure specific **Attributes**, click the **Registry** link in the module's configuration card to view the specific attribute requirements on the module's GitHub page.

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

## Edit the configuration of a module from the Viam registry

Once you have added a modular resource to your machine, you can view and edit the configuration of the underlying module from the **CONFIGURE** tab:

1. Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
2. Scroll to the card with the `namespace` of the organization that published the module and the `:name` of the module, as indicated by its page in the [registry](https://app.viam.com/registry).

This is the **Registry module** card.
This pane lists the deployed version of the module and the latest version available.
Here, [configure how a module updates](#configure-version-update-management-for-a-registry-module).

{{<imgproc src="registry/configure/deployed-module-with-component.png" resize="400x" declaredimensions=true alt="The module card">}}

You can also use JSON mode to [configure environment variables](#use-environment-variables-with-a-registry-module) for your module.

### Configure version update management for a registry module

When you add a module to your machine, you can also configure how that module updates itself when a newer version becomes available from the Viam registry.
By default, a newly-added module is set to pin to the specific patch release (**Patch (X.Y.Z)**) of the version you added, meaning that the module will _never automatically update itself_.

To allow automatic module updates when a new version of the module becomes available in the Viam registry, set the **Pinned version type** for your module in its module card on the **CONFIGURE** tab.
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

### Use environment variables with a registry module

Some modules require that you set specific environment variables as part of configuration.
You can click the **Homepage** link in the upper-right corner of the module configuration card to view any specific requirements on the module's GitHub page.

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

The notation `${environment.<ENV-VAR-NAME>}"` can be used to access any system environment variable that `viam-server` has access to, where `<ENV-VAR-NAME>` represents a system environment variable, like `PATH`, `USER`, or `PWD`.
For example, you can use `${environment.HOME}"` to access the `HOME` environment variable for the user running `viam-server`.

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

#### Default environment variables

When a module is instantiated, it has access to the following default environment variables:

<!-- prettier-ignore -->
| Name | Description |
| ---- | ----------- |
| `VIAM_HOME` | The root of the `viam-server` configuration.<br>Default: `$HOME/.viam` |
| `VIAM_MODULE_ROOT` | The root of the module install directory. The module process uses this directory as its current working directory (`cwd`). This variable is useful for file navigation that is relative to the root of the module. If you are using a [local module](#local-modules), you must set this value manually if your module requires it.<br>Example: `/opt/my-module/verxxxx-my-module/` |
| `VIAM_MODULE_DATA` | A persistent folder location a module can use to store data across reboots and versions. This location is a good place to store [python virtual environments](/build/program/python-venv/).<br>Example: `$VIAM_HOME/module-data/cloud-machine-id/my-module-name/` |
| `VIAM_MODULE_ID` | The module ID of the module. <br>Example: `viam:realsense` |

## Local modules

If you wish to add a module to your machine without uploading it to the Viam registry, you can add your module as a _local module_.

You can add your own custom modules as local modules, or you can add pre-built modules written by other Viam users.

### Prepare a local module

First determine the module you wish to add as a local module:

- If you are adding your own custom module, be sure that you have followed the steps to [create your own module](/registry/create/) to code and compile your module and generate an executable.
- If you are using a pre-built module, make sure you have installed the module and determined the filename of [the module's executable](/registry/create/#compile-or-package-your-module).

Then, ensure that `viam-server` is able to find and run the executable:

- Ensure that the module executable is saved to a location on the filesystem of your machine that `viam-server` can access.
  For example, if you are running `viam-server` on an Raspberry Pi, you must save the module executable on the Pi's filesystem.
- Ensure that this file is executable (runnable) with the following command:

  ```shell
  sudo chmod a+rx <path-to-your-module-executable>
  ```

See the instructions to [compile your module into an executable](/registry/create/#compile-or-package-your-module) for more information.

### Add a local module

To add a local module on your machine, first add its module, then the component or service it implements:

1. Navigate to the **Config** tab of your machine's page in [the Viam app](https://app.viam.com).
1. Click on the **Modules** subtab.
1. Scroll to the **Add local module** section.
1. Enter a **Name** for this instance of your modular resource.
1. Enter the [module's executable path](/registry/create/#compile-or-package-your-module).
   This path must be the absolute path to the executable on your machine's filesystem.
1. Then, click the **Add module** button, and press **Command+S** to save your config..

   {{<imgproc src="registry/configure/add-local-module-csi-cam.png" resize="600x" declaredimensions=true alt="The add a local module pane with name 'my-csi-ca' and executable path '/usr/local/bin/viam-csi'">}}

   This example shows the configuration for adding a [CSI camera](https://github.com/viamrobotics/csi-camera/) as a local module.

1. Navigate to the **Config** tab of your machine's page on [the Viam app](https://app.viam.com).

   - If you are adding a modular [component](/components/), click the **Components** subtab and click **Create component**.
   - If you are adding a modular [service](/services/), click the **Services** subtab and click **Create service**.

1. Then, select the `local component` or `local service` type from the list.

   {{<imgproc src="registry/configure/add-local-module-list.png" resize="300x" declaredimensions=true alt="The add a component modal showing the list of components to add with 'local component' shown at the bottom">}}

1. On the next screen:

   - Select the type of modular resource provided by your module, such as a [camera](/components/camera/), from the dropdown menu.
   - Enter the {{< glossary_tooltip term_id="model-namespace-triplet" text="model namespace triplet">}} of your modular resource's {{< glossary_tooltip term_id="model" text="model" >}}.
     If you are adding a pre-built modular resource, the model triplet should be provided for you in the module's documentation.
   - Enter a name for this instance of your modular resource.
     This name must be different from the module name.

   {{<imgproc src="registry/configure/add-local-module-create.png" resize="400x" declaredimensions=true alt="The add a component modal showing the create a module step for an intel realsense module">}}

1. Click **Create** to create the modular resource provided by the local module.

Once you've added your local module using steps 1-6, you can repeat steps 7-10 to add as many additional instances of your modular resource as you need.

### Edit the configuration of a local module

Once you have added a modular resource to your machine, you can view and edit the underlying module from the **Modules** subtab:

1. Navigate to the **Config** tab of your machine's page in [the Viam app](https://app.viam.com).
1. Click on the **Modules** subtab.
   Local modules you have added to your machine appear under the **Local** section.

The following properties are available for modules:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
`name` | string | **Required**| Name of the module you are registering. |
`executable_path` | string | **Required**| The absolute path to the executable on your machine's filesystem. |
`type` | string | **Required**| Either `registry` or `local`. |

Add these properties to your module's configuration:

{{< tabs >}}
{{% tab name="Config Builder" %}}

{{<imgproc src="registry/configure/add-local-module-config-builder.png" resize="600x" declaredimensions=true alt="The add a local module pane with an example name and executable path">}}

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

### Add a local modular resource

Once you have added a local module to your machine, you can add any number of the {{< glossary_tooltip term_id="resource" text="resources" >}} provided by that module to your machine by adding new components or services that use your modular resource's {{< glossary_tooltip term_id="model" text="model" >}}.

The following properties are available for modular resources:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `namespace` | string | **Required** | The namespace of the API (the first part of the {{< glossary_tooltip term_id="api-namespace-triplet" text="API namespace triplet">}}). See [Valid APIs to implement in your model](/registry/#valid-apis-to-implement-in-your-model). |
| `type` | string | **Required** | The {{< glossary_tooltip term_id="subtype" text="subtype">}} of the API (the third part of the {{< glossary_tooltip term_id="api-namespace-triplet" text="API namespace triplet">}}). See [Valid APIs to implement in your model](/registry/#valid-apis-to-implement-in-your-model). |
| `name` | string | **Required** | A custom name for this instance of your modular resource. |
| `model` | string | **Required** | The full {{< glossary_tooltip term_id="model-namespace-triplet" text="model namespace triplet">}} of the modular resource's {{< glossary_tooltip term_id="model" text="model" >}}. |
| `depends_on` | array | Optional | The `name` of components you want to confirm are available on your machine alongside your modular resource. Often a [board](/components/board/). Unnecessary if you coded [implicit dependencies](/internals/rdk/#dependency-management). |

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

## Next steps

Now that you've configured a modular resource, test it with the [**CONTROL** tab](/fleet/#remote-control) and program it with the [Viam SDKs](/build/program/apis/).

You can also check out these tutorials that configure and use modular resources:

{{< cards >}}
{{% card link="/tutorials/projects/make-a-plant-watering-robot/" %}}
{{% card link="/tutorials/projects/integrating-viam-with-openai/" %}}
{{< /cards >}}
