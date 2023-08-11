---
title: "Add the Viam Fragment to your Robot"
linkTitle: "Add the Viam Fragment to your Robot"
weight: 20
type: "docs"
tags: ["rover", "tutorial"]
description: "Configure your rover by adding the Viam-provided configuration fragment to your rover."
---

To be able to drive your rover, you need to configure it.
Viam provides a reusable {{% glossary_tooltip term_id="fragment" text="*fragment*" %}} for [Viam rovers](https://www.viam.com/resources/rover).

## Prerequisites

- An assembled Viam Rover with a Raspberry Pi.
  For assembly instructions, see [Unbox and Set Up your Viam Rover](../rover-tutorial/)
- The Pi is connected to [the Viam app](https://app.viam.com).
  To add your Pi to the Viam app, refer to [the rover setup guide](/try-viam/rover-resources/rover-tutorial/#connect-to-the-viam-app).

## Add the fragment

Navigate to your robot in [the Viam app](https://app.viam.com/robots).
On the  **Config** tab, click on the **Fragments** subtab.

{{<imgproc src="try-viam/rover-resources/fragments/fragments_tab.png" resize="1200x" alt="Fragments tab inside the Viam app">}}

On the **Fragments** tab, you can see the available fragments to add.
Find `ViamRover202210b` and click `Add` to add the fragment to your robot configuration.

{{<imgproc src="try-viam/rover-resources/fragments/fragments_list.png" resize="1200x" alt="List of available fragments">}}

Click **Save Config** to save the new configuration.

{{<imgproc src="try-viam/rover-resources/fragments/fragment_configuration.png" resize="1200x" alt="Fragment configuration">}}

The fragment adds the following components to your robot's JSON configuration.
For details about how a given type of component is configured, see the [component documentation](/components/) for that type.

* [Board component](/components/board/), which is the Raspberry Pi.
  * Within the board component attributes, digital interrupts: "re" to pin "37" and "le" to pin "35" and I2Cs: name "default_i2c_bus" and bus "1".
* Right gpio [motor](/components/motor/).
  * Within the motor attributes, board: "local", encoder: "Renc", ticks per rotation: "1992".
  * Within the component pin assignment, type: In1/In2, A/In1: "16 GPIO 23", B/In2: "18 GPIO 24", PWM: "22 GPIO 25".
  * Depends on local and Renc.
* Left gpio [motor](/components/motor/).
  * Within the motor attributes, board: "local", encoder: "Lenc", ticks per rotation: "1992".
  * Within the component pin assignment, type: In1/In2, A/In1: "11 GPIO 17", B/In2: "13 GPIO 27", PWM: "15 GPIO 22".
  * Depends on local and Lenc.

{{% alert title="Info" color="info" %}}

This particular motor driver has pins labeled "ENA" and "ENB."
Typically, this would suggest that they should be configured as enable pins, but on this specific driver these function as PWM pins, so we configure them as such.

{{% /alert %}}

* A wheeled Viam [base](/components/base/) with attributes:
  * Right Motors: right
  * Left Motors: left
  * Wheel circumference (mm): 217
  * Width (mm): 260
  * Spin slip factor: 1
  * Depends on: left, right, local.
* A webcam [camera](/components/camera/) with video_path: video0 and depends on: local.
* Renc [encoder](/components/encoder/) with board: local, pins "i": "re" and depends on: local.
* Lenc [encoder](/components/encoder/) with board: local, pins "i": "le" and depends on: local.
* An [accelerometer](/components/movement-sensor/) with the following configuration:
  * Model: "accel-adxl345"
  * Name: "accelerometer"
  * Type: "movement_sensor"
  * and attributes of "i2c_bus": "default_i2c_bus", "use_alternate_i2c_address": false, and "board": "local".
  * Depends on: local.
* A microphone, type: audio_input, with attributes "audio_path_pattern": "3a" and "debug": false.

- A [board component](/components/board/pi/) named `local` representing the Raspberry Pi
- Two [motors](/components/motor/gpio/) (`right` and `left`)

## See the components on the configuration page

Adding a fragment to your robot adds the configuration to your robot.
The components and services included in the fragment will appear inside a read-only fragment section in the **Components** and **Services** subtabs.

## Modify the config

The fragment you added is read-only, but if you need to modify your rover's config you can do the following:

1. Go to the **Fragments** subtab of the **Config** tab.
2. Click **Remove** next to the fragment.
3. Select and copy the contents of the fragment in the box on the right side of the **Fragments** subtab.
5. Toggle to [**Raw JSON** mode](/try-viam/try-viam-tutorial/#raw-json).
6. Paste the raw fragment contents into the **Raw JSON** config field.
7. Click **Save config**.
8. Now, you can edit the config either in **Raw JSON** mode or in **Builder** mode.

## Next Steps

{{< cards >}}
  {{% card link="/tutorials/get-started/try-viam-sdk" %}}
  {{% card link="/tutorials/services/try-viam-color-detection" %}}
{{< /cards >}}
