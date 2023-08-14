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
For information about how you would configure a component yourself if you weren't using the fragment, click the links on each component below.
To see the pin numbers and other values specific to this fragment, [see the components on the configuration page](#see-the-components-on-the-configuration-page).

- A [board component](/components/board/pi/) named `local` representing the Raspberry Pi
  - An I<sup>2</sup>C bus is configured on the board because the accelerometer connects to the board with I<sup>2</sup>C.
- Two [motors](/components/motor/gpio/) (`right` and `left`)
  - The configured pin numbers correspond to where the motor drivers are connected to the board.
- Two [encoders](/components/encoder/single/), one for each motor
- A wheeled [base](/components/base/), an abstraction that coordinates the motors for steering
- A webcam [camera](/components/camera/webcam/)
- An [accelerometer](/components/movement-sensor/adxl345/)

{{% alert title="Info" color="info" %}}

This particular motor driver has pins labeled "ENA" and "ENB."
Typically, this would suggest that they should be configured as enable pins, but on this specific driver these function as PWM pins, so we configure them as such.

{{% /alert %}}

## See the components on the configuration page

Adding a fragment to your robot adds the configuration to your robot.
The components and services included in the fragment appear inside a read-only fragment section in the **Components** and **Services** subtabs.

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
