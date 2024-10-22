---
title: "Machine Configuration"
linkTitle: "Machine Configuration"
weight: 429
type: "docs"
description: "Before you can program a machine, you must configure its components and services as well as any modules, remotes, processes and frames."
imageAlt: "Configure a Machine"
images: ["/viam.svg"]
tags: ["manage", "components"]
aliases:
  - /manage/configuration/
  - /build/configure/
  - /build/
no_list: true
menuindent: true
---

Before you can program a smart machine, you must configure it.

A machine's configuration defines the _{{< glossary_tooltip term_id="resource" text="resources" >}}_ (hardware and software services) it has access to, as well as any relevant parameters for those resources.
You can configure the following resources:

- [Components](/configure/#components): _{{< glossary_tooltip term_id="component" text="Components" >}}_ are the hardware of your machine.
- [Services](/configure/#services): _{{< glossary_tooltip term_id="service" text="Services" >}}_ are the software that runs on your machine.
- [Processes](/configure/#processes): Processes automatically run specified scripts when the machine boots.
- [Modules](/configure/#modules): {{< glossary_tooltip term_id="module" text="Modules" >}} provide {{< glossary_tooltip term_id="modular-resource" text="modular resources" >}}, which are a way to add resource types or models that are not built into Viam.
- [Remote parts](/configure/#remote-parts): Remotes are a way to connect two separate machines so one can access the resources of the other.
- [Sub-parts](/configure/#sub-parts): Sub-parts are a way to connect two computers inside the same machine.
- [Fragments](/configure/#fragments): Fragments are a way of sharing and managing identical configuration files (or parts of config files) across multiple machines.
- [Frames](#frames): Frames hold reference frame information for the relative position of components in space.
- [Triggers](/configure/#triggers): Triggers allow you to trigger actions when certain types of data are sent from your machine to the cloud, or when the internet connectivity of your machine changes.
- [Network](/configure/#network): Networking options allow you to configure the bind address for accepting connections.

To start configuring, go to the [Viam app](https://app.viam.com) and create a new machine.
Open the part status dropdown menu in the top left corner of the page, next to the machine's name.
Click **View setup instructions** to open the setup instructions.
Follow the appropriate instructions for your machine's architecture.

The setup steps copy your machine's credentials to your machine.
When you turn on your machine, `viam-server` starts up and uses the provided credentials to fetch its full config from the [Viam app](https://app.viam.com).
Once the machine has a configuration, it caches it locally and can use the configuration for up to 60 days.
Since the configuration is cached locally, your machine does not need to stay connected to the Viam app after it has obtained its configuration file.

If it is online, the machine checks for new configurations every 15 seconds and changes its configuration automatically when a new configuration is available.
All communication happens securely over HTTPS using secret tokens that are in a machine's configuration.

If your machine will never connect to the internet, you can also create a [local configuration file](/internals/local-configuration-file/) on the machine itself.

{{< alert title="Tip" color="tip" >}}
On Linux, the configuration is stored at <FILE>/etc/viam.json</FILE> by default and `viam-server` uses this configuration if no configuration is specified on startup.

You can store your config file in a custom location if desired.
See [Run `viam-server`](/installation/manage-viam-server/#run-viam-server) for more information.
{{< /alert >}}

After you have completed the setup steps and successfully connected to your machine, go to the **CONFIGURE** tab to start adding to the configuration.

## The CONFIGURE tab

The **CONFIGURE** tab on the [Viam app](https://app.viam.com) is the place to configure everything about your machine.

You can switch between **Builder**, **JSON**, and **Frame** mode by clicking on the icon in the upper left-hand corner:

![Mode selector on CONFIGURE tab.](/build/configure/mode-selector.png)

- **Builder** mode provides a graphical interface for configuring your machine resources.
- **JSON** mode provides a text editing field where you can write and edit the config manually.
- **Frame** mode provides a graphical interface for configuring and visualizing the relative position of components in space.
  For more information, see the [Frame System documentation](/services/frame-system/).

Regardless of the editing mode you choose, Viam stores the configuration file in [JSON (JavaScript Object Notation)](https://en.wikipedia.org/wiki/JSON).

{{< alert title="Caution: Simultaneous config edits" color="caution" >}}
If you edit a config while someone else edits the same config, the person who saves last will overwrite any prior changes that aren't reflected in the new config.

Before editing a config, we recommend you refresh the page to ensure you have all the latest changes.
{{< /alert >}}

If you add components in **Builder** mode and click **Save** in the top right corner of the screen, you can switch to **JSON** and see the JSON that has been generated by the builder.

{{% expand "An example JSON config file for a machine with a board component, motor component, camera component, and vision service configured" %}}

```json
{
  "components": [
    {
      "name": "local",
      "model": "pi",
      "type": "board",
      "namespace": "rdk",
      "attributes": {},
      "depends_on": []
    },
    {
      "name": "my-motor",
      "model": "gpio",
      "type": "motor",
      "namespace": "rdk",
      "attributes": {
        "pins": {
          "a": "13",
          "b": "15"
        },
        "board": "local",
        "max_rpm": 120
      },
      "depends_on": []
    },
    {
      "name": "my_camera",
      "model": "webcam",
      "type": "camera",
      "namespace": "rdk",
      "attributes": {
        "video_path": "video0"
      }
    }
  ],
  "services": [
    {
      "name": "detector",
      "type": "vision",
      "attributes": {
        "register_models": [
          {
            "parameters": {
              "segment_size_px": 200,
              "hue_tolerance_pct": 0.05,
              "detect_color": "#19FFD9"
            },
            "type": "color_detector",
            "name": "green_detector"
          }
        ]
      }
    }
  ],
  "modules": []
}
```

See [Example JSON configuration file](/internals/local-configuration-file/#example-json-configuration-file) for an additional example.

{{% /expand %}}

<!-- While in **Builder** mode, if you select the **+** (Create) icon next to your {{ < glossary_tooltip term_id="part" text="machine part" >}} in the left-hand menu, the following options are displayed:

TODO R2D2 add image once "insert fragment" option is removed -->

### Components

Components represent the pieces of hardware on your machine that you want to control with Viam.
To add a new component, click the **+** icon next to your {{< glossary_tooltip term_id="part" text="machine part" >}} in the left-hand menu of the **CONFIGURE** tab and select **Component** or hit **C**.
Search for and select your desired {{< glossary_tooltip term_id="model" text="model" >}}.

You must configure each component with a type, a model, a name, attributes, and dependencies:

- `type`: The broad component category, such as `motor`, `arm` or `camera`.
  Components of a given type have a common API.

- `model`: Indicates the more specific category of hardware.
  Components of the same model are supported using the same low-level code.

- `name`: Serves as an identifier when accessing the resource from your code, as well as when configuring other resources that are dependent on that resource.
  You can either accept the suggested default name when creating a component or choose a unique name for a component.
  The name must start with a letter or number and only contain letters, numbers, dashes, and underscores with a max length of 60.

- `attributes`: Configure component details such as how the component is wired to the machine, its dimensions, and other specifications; attributes vary widely between models.
  See a {{< glossary_tooltip term_id="component" text="component" >}}'s documentation for more details.

- `depends_on`: Any components that a given component relies upon, and that must be initialized on boot before this component is initialized.
  Many built-in components have convenient implicit dependencies, in which case `depends_on` can be left blank.
  For example, a [`gpio` motor](/components/motor/gpio/) depends on the `board` to which it is wired, but it has a dedicated `board` attribute and `viam-server` will automatically initialize that board before it looks for the motor.

For specific information on how to configure each supported component type, see the {{< glossary_tooltip term_id="component" text="component" >}}'s documentation:

{{< cards >}}
{{% relatedcard link="/components/arm" %}}
{{% relatedcard link="/components/base" %}}
{{% relatedcard link="/components/board" %}}
{{% relatedcard link="/components/camera" %}}
{{% relatedcard link="/components/encoder" %}}
{{% relatedcard link="/components/gantry" %}}
{{% relatedcard link="/components/generic" %}}
{{% relatedcard link="/components/gripper" %}}
{{% relatedcard link="/components/input-controller" %}}
{{% relatedcard link="/components/motor" %}}
{{% relatedcard link="/components/movement-sensor" %}}
{{% relatedcard link="/components/power-sensor" %}}
{{% relatedcard link="/components/sensor" %}}
{{% relatedcard link="/components/servo" %}}
{{< /cards >}}

Some resources have a **TEST** section on the bottom half of their configuration pane which you can expand and interact with to test out controlling the component.
You must be running `viam-server` and connected to your machine to use this feature.

{{<gif webm_src="/test.webm" mp4_src="/test.mp4" alt="Test a camera stream" max-width="600px" class="aligncenter">}}

On the **...** menu in the upper right corner of each resource you can **Duplicate**, **Delete**, and **Disable** or **Enable** it.

{{<imgproc src="/configure/component-menu.png" resize="600x" declaredimensions=true alt="menu on a component card" class="aligncenter imgzoom">}}

{{% alert title="Tip" color="tip" %}}

When you configure a component on the **CONFIGURE** tab, it will also appear on the **CONTROL** tab which gives you an interface to interact with it.
The **Code sample** page on the **CONNECT** tab will also update to include code for some basic interaction with that component using the Viam [SDKs](/appendix/apis/).

{{% /alert %}}

### Services

Services are software packages that make it easier to add complex capabilities such as motion planning or object detection to your machine.
To add a new service, click the **+** icon next to your {{< glossary_tooltip term_id="part" text="machine part" >}} in the left-hand menu of the **CONFIGURE** tab and select **Service** or hit **S**.
Search for and select your desired {{< glossary_tooltip term_id="model" text="model" >}}.

You must configure a service with a `name` and a `type`:

- `type`: specifies which of the Viam services you want to use on your machine, such as the vision service or the motion service.
- `name`: serves as an identifier when accessing the resource from your code, as well as when configuring other resources that are dependent on that resource.
  You can accept the suggested default name when creating a service or choose a choose any unique name for a service.
  The name must start with a letter or number and can only contain letters, numbers, dashes, and underscores with a max length of 60.

The other aspects of configuring a service are highly specific to the type of service, review the docs for the service you are interested in:

{{< cards >}}
{{% relatedcard link="/services/data/" %}}
{{% relatedcard link="/services/ml/" alt_title="Machine Learning" %}}
{{% relatedcard link="/services/motion" %}}
{{% relatedcard link="/services/navigation" %}}
{{% relatedcard link="/services/slam" %}}
{{% relatedcard link="/services/vision" %}}
{{% relatedcard link="/services/generic" %}}
{{% relatedcard link="/services/frame-system" %}}
{{< /cards >}}

Some resources have a **TEST** section on the bottom half of their configuration pane which you can expand and interact with to test out controlling the service.
You must be running `viam-server` and connected to your machine to use this feature.

You can disable a service without removing it from the configuration by selecting the **...** menu in the upper right corner and selecting **Disable**.

{{% alert title="Tip" color="tip" %}}

When you configure a service on the **CONFIGURE** tab, it will also appear on the **CONTROL** tab which gives you an interface to test and interact with it.
The **Code sample** page on the **CONNECT** tab will also update to include code for some basic interaction with that service using the Viam [SDKs](/appendix/apis/).

{{% /alert %}}

### Processes

To automatically run a specified command when the machine boots, configure a _{{< glossary_tooltip term_id="process" text="process" >}}_.
You can configure any command, for example one that executes a binary or a script, to run as a process.

To add a new process, click the **+** icon next to your {{< glossary_tooltip term_id="part" text="machine part" >}} in the left-hand menu of the **CONFIGURE** tab and select **Process**.
Find more information in the [processes documentation](/configure/processes/).

### Modules

Modules allow you to add [modular resources](/registry/) to your machines which add resource types or models that are not built into Viam.
Many models are available in the [registry](https://app.viam.com/registry) and you are able to add them as components or services.

#### Local Modules

To add a module that is not in the registry and is local to your machine, click the **+** icon next to your {{< glossary_tooltip term_id="part" text="machine part" >}} in the left-hand menu of the **CONFIGURE** tab and select **Local module**.
Follow the instructions in our [registry documentation](/registry/modular-resources/#configuration) to configure the module.

### Remote parts

Configuring a remote part is a way to connect two separate machines so one can access the resources of the other.

To configure a remote part, click the **+** icon next to your {{< glossary_tooltip term_id="part" text="machine part" >}} in the left-hand menu of the **CONFIGURE** tab and select **Remote part**.
Find more information in our [machine parts documentation](/architecture/parts/).

### Sub-parts

Configure a sub-part to connect two computers inside the same machine.

To configure a sub-part, click the **+** icon next to your {{< glossary_tooltip term_id="part" text="machine part" >}} in the left-hand menu of the **CONFIGURE** tab and select **Sub-part**.
Find more information in our [machine parts documentation](/architecture/parts/).

### Fragments

You can use fragments to share similar {{< glossary_tooltip term_id="resource" text="resource" >}} configuration files across multiple machines in your fleet.
For example, if you have multiple machines with the same motor hardware, wired the same way, you can create a fragment to configure that motor and share it easily across all of your machines, without needing to individually configure the motor component for each machine.

To use a fragment, click the **+** icon next to your {{< glossary_tooltip term_id="part" text="machine part" >}} in the left-hand menu of the **CONFIGURE** tab and select **Insert fragment**.
See [Use Fragments to Configure a Fleet](/fleet/fragments/) for more information on creating and deploying fragments.

### Frames

The frame system holds reference frame information for the relative position of components in space.

Click on the **Frame** mode to visualize and configure the relative positions of components.
Find more information in the [frame system documentation](/services/frame-system/).

### Triggers

Triggers allow you to trigger actions when certain types of data are sent from your machine to the cloud, or when the internet connectivity of your machine changes.
For example, you can configure a trigger to send you a notification when your robot's sensor collects a new reading.

See [Configure a Trigger](/configure/triggers/) for more information on triggers.

### Network

Expand a part's configuration card to open its network configuration interface:

{{<imgproc src="/build/configure/network.png" resize="x400" style="width: 300px" declaredimensions=true alt="The network configuration interface on a part card of a machine.">}}

You can configure the address `viam-server` binds to for accepting connections.
By default, `viam-server` binds to `0.0.0.0:8080` when managed by the Viam app or when authentication and TLS are enabled.
You can also set the [heartbeat](/appendix/apis/sessions/#heartbeats) window.

## Configuration History

The Viam app keeps a record of each machine's configuration changes, allowing you to revert to earlier configurations if needed and see who made specific changes.

To see the configuration history for a machine part, click on the **History** link at the top right corner of the machine part's card in the Viam app.

{{<imgproc src="build/configure/history.png" resize="1000x" declaredimensions=true alt="Configuration history for a machine part">}}

To restore to an earlier version of your configuration, click the **Restore version** button next to the desired configuration.

## Troubleshooting

If you run into issues, here are some things to try:

- Check the [**LOGS** tab](/cloud/machines/#logs) to view log messages and errors from `viam-server`.
  You can also [access the local log file](/installation/manage-viam-server/#view-viam-server-logs) on your machine if needed.
- Make sure all configured components are saved to your config.
  If they aren't, you will see an **Unsaved changes** note next to the **Save** button in the top right corner of the page.
- Try restarting `viam-server` by navigating to the app's **CONFIGURE** tab in **Builder** mode, clicking the **...** menu on the right side of the machine part's card, and selecting **Restart part**.
  It takes a few minutes for the server to shut down and restart.
- If you need to revert to an earlier configuration, use the [Configuration History](#configuration-history) to restore to an earlier version.
- Make sure the issue is not hardware related.
  Some things to check are that the machine has adequate power, all wires are properly connected, and no chips or other hardware components are shorted or overheated.
- See [Troubleshooting](/appendix/troubleshooting/) for additional troubleshooting steps.
- {{< snippet "social.md" >}}

## Local setup

Configuring `viam-server` with the Viam app allows you to use Viam's cloud features:

- [Fleet Management](/fleet/)
- [Data Management](/services/data/)
- [Machine Learning](/services/ml/)

However, if you are configuring a machine that can never connect to the internet, you can create a [local configuration file](/internals/local-configuration-file/) on your machine.
A locally-configured machine will not be able to access Viam's cloud features.

## Next steps

After configuring your machine, you can use the [Viam SDKs](/appendix/apis/) to program and control your machine.

If you want to try configuring a machine but don't have any hardware on hand, try the [Build a Mock Robot](/tutorials/configure/build-a-mock-robot/) tutorial.
