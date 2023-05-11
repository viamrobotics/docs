---
title: "Add the Viam Fragment to your Robot"
linkTitle: "Add the Viam Fragment to your Robot"
weight: 20
type: "docs"
tags: ["rover", "tutorial"]
description: "Configure your rover by adding the Viam-provided configuration fragment to your rover."
---

To be able to drive your rover, you need to configure it.
Viam provides a reusable *fragment* for [Viam rovers](https://www.viam.com/resources/rover).

{{< alert title="Tip" color="tip" >}}
A fragment is a reusable configuration block representing a common hardware pattern.
Using a fragment makes managing a fleet of multiple robots configured in the same way easy.
{{< /alert >}}

## Prerequisites

* An assembled Viam Rover with a Raspberry Pi.
  For assembly instructions, see [Unbox and Set Up your Viam Rover](../rover-tutorial)
* The Pi is able to connect to [the Viam app](https://app.viam.com).
  To add your Pi to the Viam app, refer to [the rover setup guide](/try-viam/rover-resources/rover-tutorial/#connect-to-the-viam-app).

## Add the Fragment

Navigate to your robot in [the Viam app](https://app.viam.com/robots).
On the  **Config** tab, click on the **Fragments** subtab.

![Fragments tab inside the Viam app](../img/fragments/fragments_tab.png)

On the **Fragments** tab, you can see the available fragments to add.
Find `ViamRover202210b` and click `ADD` to add the fragment to your robot configuration.

![List of available fragments](../img/fragments/fragments_list.png)

After you add the fragment, the config on the right side shows the robot's configuration with the new fragment.
Click **Save Config** to save the new configuration.

![Fragment configuration](../img/fragments/fragment_configuration.png)

The fragment adds the following components to your robot's JSON configuration:

* [Board component](/components/board/), which is the Raspberry Pi.
  * Within the board component attributes, digital interrupts: "re" to pin "37" and "le" to pin "35" and I2Cs: name "default_i2c_bus" and bus "1".
* Right gpio [motor](/components/motor/).
  * Within the motor attributes, board: "local", encoder: "Renc", ticks per rotation: "996".
  * Within the component pin assignment, type: In1/In2, A/In1: "16 GPIO 23", B/In2: "18 GPIO 24", PWM: "22 GPIO 25".
  * Depends on local and Renc.
* Left gpio [motor](/components/motor/).
  * Within the motor attributes, board: "local", encoder: "Lenc", ticks per rotation: "996".
  * Within the component pin assignment, type: In1/In2, A/In1: "11 GPIO 17", B/In2: "13 GPIO 27", PWM: "15 GPIO 22".
  * Depends on local and Lenc.
* A wheeled Viam [base](/components/base/) with attributes:
  * Right Motors: right
  * Left Motors: left
  * Wheel circumference (mm): 217
  * Width (mm): 260
  * Spin slip factor: 1.76
  * Depends on: left, right, local.
* A webcam [camera](/components/camera) with video_path: video0 and depends on: local.
* Renc [encoder](/components/encoder/) with board: local, pins "i": "re" and depends on: local.
* Lenc [encoder](/components/encoder/) with board: local, pins "i": "le" and depends on: local.
* An [accelerometer](/components/movement-sensor/) with the following configuration:
  * Model: "accel-adxl345"
  * Name: "accelerometer"
  * Type: "movement_sensor"
  * and attributes of "i2c_bus": "default_i2c_bus", "use_alternate_i2c_address": false, and "board": "local".
  * Depends on: local.
* A microphone, type: audio_input, with attributes "audio_path_pattern": "3a" and "debug": false.

## See the components on the configuration page

Adding a fragment to your robot adds the configuration to your robot but it does not automatically fill your robot configuration page in the app with these components.
It is normal for your **Components** subtab on the builder view to be empty:

![Builder Tab](../img/fragments/builder_tab.png)

Instead, your Raw JSON will reference the fragment in it.

![Raw JSON](../img/fragments/raw_json.png)

If you want each component to show up in your **Components** subtab so you can view or edit them, copy the entire configuration from the **Fragments** subtab, paste it into your Raw JSON section, and save your configuration.

## Next Steps

{{< cards >}}
  {{% card link="/tutorials/get-started/try-viam-sdk" size="small" %}}
  {{% card link="/tutorials/services/try-viam-color-detection" size="small" %}}
{{< /cards >}}
