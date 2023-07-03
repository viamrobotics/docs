---
title: "Add an ODrive motor as a Modular Resource"
linkTitle: "ODrive"
weight: 40
type: "docs"
description: "How to add an ODrive motor with serial or canbus as a modular resource of your robot."
tags: ["motor", "odrive", "canbus", "serial", "module", "modular resources"]
# SMEs: Kim, Martha, Rand
---

The [Viam GitHub](https://github.com/viamrobotics/odrive) provides an implementation of ODrive Robotics' [ODrive S1](https://odriverobotics.com/shop/odrive-s1) motor driver as a modular resource [extending the motor API](/extend/modular-resources/).

[Prepare](#prepare-your-odrive) your ODrive and [download](#requirements) and [configure](#configuration) the module to add an `odrive-serial` or `odrive-canbus` [motor](/components/motor/) {{< glossary_tooltip term_id="resource" text="resource" >}} to your robot.

### Prepare your ODrive

Read through the [ODrive documentation](https://docs.odriverobotics.com/v/latest/getting-started.html) to wire, calibrate, and connect your motor to your [board](/components/board/).

Follow [this guide](https://docs.odriverobotics.com/v/latest/control.html#control-doc) to tune your motor.

{{< tabs name="Prepare your ODrive">}}
{{% tab name="odrive-serial" %}}

- Plug the USB Isolator for Odrive into a USB port on your board, and then plug a USB-C to USB-A cable from the isolator to the Odrive.

{{% /tab %}}
{{% tab name="odrive-canbus" %}}

- wire the CANH and CANL (see Odrive pinout) pins from your board to your Odrive
- To prepare the Odrive (see the first item in the Getting Started secion), you have already needed to plug the ODrive into your board through a USB port with the USB Isolator for ODrive.
Once you have prepared the ODrive, you can either leave the serial connection plugged in, or remove it and just leave the CANH and CANL pins wired.

{{% /tab %}}
{{< /tabs >}}

<!-- 

* Update the sample config as following:
    * Update the `executable_path` (string) to the location of `run.sh` on your machine
    * If using a `"canbus"` connection, update the `canbus_node_id` (int) to the node ID of whichever CAN node you'd like to use AND ALSO NEED TO DO SOMETHING ELSE FROM THE ODRIVE DOCS FOR CANBUS
TODO: NEED TO POINT SOMEWHERE TO MODULAR RESOURCES DOCUMENTATION

{{% alert title="Note" color="note" %}}

You must also enable SPI on your board if it is not enabled by default.
See your [board model's configuration instructions](/components/board/#configuration) if applicable.

{{% /alert %}}

The configuration remains on the same ODrive motor controller across reboots, and only changes when you go through the configuration of the ODrive again. 
- grab path to ODRIVEconfig file for configuration later if you want it to be reconfigured
   -->

After preparing your ODrive, download and configure the module to configure `odrive-serial` or `odrive-canbus` model motors on your robot.
<!-- TODO: does this sentence really need to be here 

TODO: should we also connect to more detailed module instructions at this point? like github readme?
-->

## Requirements

<!-- [make sure `viam-sdk` is installed and a robot is configured] maybe put this right before this section starts? -->

Clone the [Viam ODrive module](https://github.com/viamrobotics/odrive) on your robot's computer:

``` {id="terminal-prompt" class="command-line" data-prompt="$"}
git clone https://github.com/viamrobotics/odrive.git
```

TODO: make into tabs
Install `odrivetool`, `python-can`, and `cantools`:

``` {id="terminal-prompt" class="command-line" data-prompt="$"}
pip3 install python-can
pip3 install cantools
```

Follow [these instructions](https://docs.odriverobotics.com/v/latest/odrivetool.html) to install `odrivetool`.

Find and copy the path to `run.sh` on your machine to provide in configuration.

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
