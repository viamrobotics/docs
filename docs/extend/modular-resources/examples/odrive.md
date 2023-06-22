---
title: "Add an ODrive motor as a Modular Resource"
linkTitle: "ODrive"
weight: 40
type: "docs"
description: "How to add an ODrive motor with serial or canbus as a modular resource of your robot."
tags: ["motor", "odrive", "canbus", "serial", "module", "modular resources"]
# SMEs: Kim, Martha, Rand
---

The [Viam GitHub](https://github.com/viamrobotics/odrive) provides an implementation of ODrive Robotics' [ODrive S1](https://odriverobotics.com/shop/odrive-s1) motor driver as a modular {{< glossary_tooltip term_id="resource" text="resource" >}}.

Before configuring the Viam ODrive module, ensure you have [installed `viam-server`](/installation/), [configured](/manage/configuration/) a robot, and set up your ODrive.
Read through the [ODrive documentation](https://docs.odriverobotics.com/v/latest/getting-started.html) to wire, calibrate, and connect your motor to your [board](/components/board/).
Follow [this guide](https://docs.odriverobotics.com/v/latest/control.html#control-doc) to tune your motor.

<!-- TODO: Should we make the following a note?
The configuration remains on the same ODrive motor controller across reboots, and only changes when you go through the configuration of the ODrive again. 
- grab path to ODRIVEconfig file for configuration later if you want it to be reconfigured
-->

{{% alert title="Note" color="note" %}}

You must also enable SPI on your board if it is not enabled by default.
See your [board model's configuration instructions](/components/board/#configuration) if applicable.

{{% /alert %}}

<!-- 

* Update the sample config as following:
    * Update the `executable_path` (string) to the location of `run.sh` on your machine
    * If using a `"canbus"` connection, update the `canbus_node_id` (int) to the node ID of whichever CAN node you'd like to use
TODO: NEED TO POINT SOMEWHERE TO MODULAR RESOURCES DOCUMENTATION
   -->

After preparing your ODrive, download and configure the module to configure `odrive-serial` or `odrive-canbus` model motors on your robot.

## Requirements

Clone the [Viam ODrive module](https://github.com/viamrobotics/odrive) on your robot's computer:

``` {id="terminal-prompt" class="command-line" data-prompt="$"}
https://github.com/viamrobotics/odrive.git
```

- maybe above needs to be link not command prompt? lol
- find path to run.sh on your local machine
- install odrive, python-can, cantools, and viam-sdk

## Configuration

### Module

{{< tabs name="Add the ODrive module">}}
{{% tab name="Config Builder" %}}

Click on the **Modules** subtab.

Add the ODrive module with a name of your choice and an executable path that points to the location of your ODrive module's run script.

<!-- TODO: add image -->

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
"modules": [
  {
    "name": "odrive",
    "executable_path": "path/to/run.sh"
  }
]
```

{{% /tab %}}
{{< /tabs >}}

 <!-- diff requirements for canbus and odrive can tab?
    - can deffo show requirements for multiple on canbus tab example but should I consider if it should be its own section?
    - connecting section is split in these tabs  -->

### Modular Resource

{{< tabs name="Add an ODrive motor">}}
{{% tab name="odrive-serial" %}}

TODO: CFG BLD and json tabs?
```json {class="line-numbers linkable-line-numbers"}
{
  "modules": [
    {
      "name": "odrive",
      "executable_path": "path/to/run.sh"
    }
  ],
  "components": [
    {
      "model": "viam:motor:odrive-serial",
      "namespace": "rdk",
      "attributes": {
        "serial_number": "NUM000",
        "odrive_config_file": "local/path/to/motor/config.json",
      },
      "depends_on": [],
      "type": "motor",
      "name": "odrive-motor"
    }
  ]
}
```

{{% /tab %}}
{{% tab name="odrive-canbus" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "modules": [
    {
      "name": "odrive",
      "executable_path": "path/to/run.sh"
    }
  ],
  "components": [
    {
      "model": "viam:motor:odrive-canbus",
      "namespace": "rdk",
      "attributes": {
        "canbus_node_id": 0,
      },
      "depends_on": [],
      "type": "motor",
      "name": "odrive-motor"
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

<!-- 
{{< tabs name="Add an Odrive motor component">}}
{{% tab name="Config Builder" %}}

Physically connect the ODrive motor to your machine.
Go to your robot's page on the [Viam app](https://app.viam.com/).

Navigate to the **Config** tab on your robot's page, and click on the **Components** subtab.

Add a component with type `motor`, model `viam:motor:odrive-canbus`, and a name of your choice:

![adding odrive component](../../img/add-odrive/add-odrive-component-ui.png)

Paste the following into the **Attributes** field of your new component according to your machine's architecture (none needed for Linux):

{{% /tab %}}
{{% tab name="JSON Template" %}}

Navigate to the **Config** tab.
Select the **Raw JSON** mode, then copy/paste the following `"components"` and `"modules"` JSON:

```json {class="line-numbers linkable-line-numbers"}

```

{{% /tab %}}
{{< /tabs >}} -->

Check the **Logs** tab of your robot in the Viam app to make sure your ODrive motor has connected and no errors are being raised.

{{< snippet "social.md" >}}

## Next Steps

<!-- {{< cards >}}
  {{% card link="/services/slam/cartographer" size="small" %}}
  {{% card link="/services/slam" size="small" %}}
{{< /cards >}} -->
