---
title: "Add an ODrive motor as a Modular Resource"
linkTitle: "Add an ODrive motor as a Modular Resource"
weight: 40
type: "docs"
description: "How to add an ODrive motor with serial or canbus as a modular resource of your robot with the Viam ODrive module."
tags: ["motor", "odrive", "canbus", "serial", "module", "modular resources"]
# SMEs: Kim, Martha, Rand
---

The [Viam GitHub](https://github.com/viamrobotics/odrive) provides an implementation of ODrive Robotics' [ODrive S1](https://odriverobotics.com/shop/odrive-s1) motor driver as a modular {{< glossary_tooltip term_id="resource" text="resource" >}}.

Before getting started, make sure you have read through the [ODrive documentation](https://docs.odriverobotics.com/v/latest/getting-started.html) to wire, calibrate, and connect your motor to your [board](/components/board/).

Use [this guide](https://docs.odriverobotics.com/v/latest/control.html#control-doc) to tune your motor.

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
   -->
TODO: NEED TO POINT SOMEWHERE TO MODULAR RESOURCES DOCUMENTATION
After completing the re 

Download and configure this module to configure `odrive-serial` or `odrive-canbus` model motors on your robot.

## Requirements

Clone the [Viam ODrive module](https://github.com/viamrobotics/odrive) on your robot's computer:

``` {id="terminal-prompt" class="command-line" data-prompt="$"}
https://github.com/viamrobotics/odrive.git
```

- find path to run.sh on your local machine

## Configuration

### Module

Click on the **Modules** subtab.

Add the odrive module with a name of your choice and an executable path that points to the location of your ODrive module's run script.



- diff requirements for canbus and odrive --> can tab?
    - can deffo show requirements for multiple on canbus tab example but should I consider if it should be its own section?
    - https://github.com/viamrobotics/odrive/tree/main#connecting-to-an-odrive connecting section is split in these tabs

{{< tabs name="Add an Odrive motor component">}}
{{% tab name="odrive-serial" %}}



{{% /tab %}}

{{% tab name="odrive-canbus" %}}

{{% /tab %}}
{{< /tabs >}}

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

  {{< tabs name="Add the Odrive component - configs" >}}
  {{% tab name="Linux" %}}

  ```json

  ```

  {{% /tab %}}
  {{% tab name="macOS x86_64" %}}

  ```json

  ```

  {{% /tab %}}
  {{% tab name="macOS ARM64 (M1 & M2)" %}}

  ```json

  ```

  {{% /tab %}}
  {{< /tabs >}}

{{% /tab %}}
{{< /tabs >}}

Check the **Logs** tab of your robot in the Viam app to make sure your ODrive motor has connected and no errors are being raised.

{{< snippet "social.md" >}}

## Next Steps

{{< cards >}}
  {{% card link="/services/slam/cartographer" size="small" %}}
  {{% card link="/services/slam" size="small" %}}
{{< /cards >}}
