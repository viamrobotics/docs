---
title: "Configure your Viam Rover with a Fragment"
linkTitle: "Configure your Viam Rover"
weight: 20
type: "docs"
tags: ["rover", "tutorial"]
description: "Configure your rover by adding the Viam-provided configuration fragment to your rover."
aliases:
  - "/try-viam/rover-resources/rover-tutorial-fragments/"
---

To be able to drive your rover, you need to configure it.
Viam provides reusable {{% glossary_tooltip term_id="fragment" text="*fragments*" %}} for [Viam rovers](https://www.viam.com/resources/rover).

## Prerequisites

- An assembled Viam Rover.
  For assembly instructions, see [Unbox and Set Up your Viam Rover](../rover-tutorial/)
- The board is connected to [the Viam app](https://app.viam.com).
  To add your Pi to the Viam app, refer to [the rover setup guide](/get-started/try-viam/rover-resources/rover-tutorial/#control-your-rover-on-the-viam-app).

## Add the fragment

Follow the appropriate instructions for the model of rover and board you have:

{{< tabs >}}
{{% tab name="Viam Rover 2 (Pi)" %}}

Navigate to your machine in [the Viam app](https://app.viam.com/robots).
In the left-hand menu of the **CONFIGURE** tab, click the **+** (Create) icon next to the machine {{< glossary_tooltip term_id="part" text="part" >}} you want to add the fragment to.

Select **Insert fragment**.
Now, you can see the available fragments to add.
Select `ViamRover2-2024-rpi4-a` and click **Insert fragment** again to add the fragment to your machine configuration:

{{<imgproc src="get-started/try-viam/rover-resources/fragments/fragments_list.png" resize="400x" style="max-width: 500px" alt="List of available fragments">}}

Click **Save** in the upper right corner of the page to save your new configuration.

The fragment adds the following components to your machine's JSON configuration:

- A [board component](/components/board/pi/) named `local` representing the Raspberry Pi.
- Two [motors](/components/motor/gpio/) (`right` and `left`)
  - The configured pin numbers correspond to where the motor drivers are connected to the board.
- Two [encoders](/components/encoder/single/), one for each motor
- A wheeled [base](/components/base/), an abstraction that coordinates the movement of the right and left motors
- A webcam [camera](/components/camera/webcam/)
- An [accelerometer](/components/movement-sensor/mpu6050/)
- A [power sensor](/components/power-sensor/ina219/)

For information about how to configure components yourself when you are not using the fragment, click the links on each component above.
To see the configured pin numbers and other values specific to this fragment, [view it in the app](https://app.viam.com/fragment?id=7c413f24-691d-4ae6-a759-df3654cfe4c8).

{{% /tab %}}
{{% tab name="Viam Rover 1 (Pi)" %}}

Navigate to your machine in [the Viam app](https://app.viam.com/robots).
In the left-hand menu of the **CONFIGURE** tab, click the **+** (Create) icon next to the machine {{< glossary_tooltip term_id="part" text="part" >}} you want to add the fragment to.

Select **Insert fragment**.
Now, you can see the available fragments to add.
Select `ViamRover202210b` and click **Insert fragment** again to add the fragment to your machine configuration:

{{<imgproc src="get-started/try-viam/rover-resources/fragments/fragments_list.png" resize="400x" style="max-width: 500px" alt="List of available fragments">}}

Click **Save** in the upper right corner of the page to save your configuration.

{{<imgproc src="get-started/try-viam/rover-resources/fragments/fragment_configuration.png" resize="400x" style="max-width: 500px" alt="Fragment configuration">}}

The fragment adds the following components to your machine's JSON configuration:

- A [board component](/components/board/pi/) named `local` representing the Raspberry Pi
  - An I<sup>2</sup>C bus for connection to the accelerometer.
- Two [motors](/components/motor/gpio/) (`right` and `left`)
  - The configured pin numbers correspond to where the motor drivers are connected to the board.
- Two [encoders](/components/encoder/single/), one for each motor
- A wheeled [base](/components/base/), an abstraction that coordinates the movement of the right and left motors
  - Width between the wheel centers: 260 mm
  - Wheel circumference: 217 mm
  - Spin slip factor: 1
- A webcam [camera](/components/camera/webcam/)
- An [accelerometer](/components/movement-sensor/adxl345/)

{{% alert title="Info" color="info" %}}

This particular motor driver has pins labeled "ENA" and "ENB."
Typically, this would suggest that they should be configured as enable pins, but on this specific driver these function as PWM pins, so we configure them as such.

{{% /alert %}}

For information about how you would configure a component yourself if you weren't using the fragment, click the links on each component above.
To see the configured pin numbers and other values specific to this fragment, [view it in the app](https://app.viam.com/fragment?id=3e8e0e1c-f515-4eac-8307-b6c9de7cfb84).

{{% /tab %}}
{{% tab name="Viam Rover 2 (Jetson Nano)" %}}

Navigate to your machine in [the Viam app](https://app.viam.com/robots).
In the left-hand menu of the **CONFIGURE** tab, click the **+** (Create) icon next to the machine {{< glossary_tooltip term_id="part" text="part" >}} you want to add the fragment to.

Select **Insert fragment**.
Now, you can see the available fragments to add.
Select `ViamRover2-2024-jetson-nano-a` and click **Insert fragment** again to add the fragment to your machine configuration.

{{<imgproc src="get-started/try-viam/rover-resources/fragments/fragments_list.png" resize="400x" style="max-width: 500px" alt="List of available fragments">}}

Click **Save** in the upper right corner of the page to save your new configuration.

The fragment adds the following components to your machine's JSON configuration:

- A [board component](/components/board/pi/) named `local` representing the Jetson.
- Two [motors](/components/motor/gpio/) (`right` and `left`)
  - The configured pin numbers correspond to where the motor drivers are connected to the board.
- Two [encoders](/components/encoder/single/), one for each motor
- A wheeled [base](/components/base/), an abstraction that coordinates the movement of the right and left motors
- A webcam [camera](/components/camera/webcam/)
- An [accelerometer](/components/movement-sensor/mpu6050/)
- A [power sensor](/components/power-sensor/ina219/)

For information about how to configure components yourself when you are not using the fragment, click the links on each component above.
To see the configured pin numbers and other values specific to this fragment, [view it in the app](https://app.viam.com/fragment?id=747e1f43-309b-4311-b1d9-1dfca45bd097).

{{% /tab %}}
{{% tab name="Viam Rover 2 (Jetson Orin Nano)" %}}

Navigate to your machine in [the Viam app](https://app.viam.com/robots).
In the left-hand menu of the **CONFIGURE** tab, click the **+** (Create) icon next to the machine {{< glossary_tooltip term_id="part" text="part" >}} you want to add the fragment to.

Select **Insert fragment**.
Now, you can see the available fragments to add.
Find `ViamRover2-2024-nano-orin-a` and select **Insert fragment** again to add the fragment to your machine configuration.

Click **Save** in the upper right corner of the page to save your new configuration.

{{<imgproc src="get-started/try-viam/rover-resources/fragments/fragments_list.png" resize="400x" style="max-width: 500px" alt="List of available fragments">}}

The fragment adds the following components to your machine's JSON configuration:

- A [board component](/components/board/pi/) named `local` representing the Jetson.
- Two [motors](/components/motor/gpio/) (`right` and `left`)
  - The configured pin numbers correspond to where the motor drivers are connected to the board.
- Two [encoders](/components/encoder/single/), one for each motor
- A wheeled [base](/components/base/), an abstraction that coordinates the movement of the right and left motors
- A webcam [camera](/components/camera/webcam/)
- An [accelerometer](/components/movement-sensor/mpu6050/)
- A [power sensor](/components/power-sensor/ina219/)

For information about how to configure components yourself when you are not using the fragment, click the links on each component above.
To see the configured pin numbers and other values specific to this fragment, [view it in the app](https://app.viam.com/fragment?id=6208e890-8400-4197-bf0f-e8ddeca4e157).

{{% /tab %}}
{{< /tabs >}}

## See the components on the configuration page

Adding a fragment to your machine adds the configuration to your machine.
The components and services included in the fragment will now appear as cards on the **CONFIGURE** tab, along with a card for your fragment:

{{<imgproc src="get-started/try-viam/rover-resources/fragments/fragments_cards.png" resize="400x" style="max-width: 500px" alt="List of available fragments">}}

## Modify the config

The fragment you added is read-only, but if you need to modify your rover's config you can do the following:

1. Navigate to the card belonging to your fragment on the **CONFIGURE** tab.
2. Click the **View JSON** button in the upper right corner of the card.
   Copy all the JSON.
3. Return to the fragment card.
   Click the **...** (Actions) button in the upper right corner of the card. Click **Delete** and confirm your choice.
4. In the left-hand menu of the **CONFIGURE** tab, click **JSON** to switch to JSON mode.
5. Paste the raw fragment contents into the editor and click **Save** in the upper-right corner of the screen to save your config.
6. Now, you can edit the config in either **JSON** or **Builder** mode.

## Next steps

Before you can use your Viam rover with the Viam platform you need to configure your rover:

{{< cards >}}
{{% card link="/get-started/try-viam/rover-resources/rover-tutorial-fragments/" %}}
{{< /cards >}}

After you have configured your rover, follow one of these tutorials:

{{< cards >}}
{{% card link="/tutorials/get-started/try-viam-sdk/" %}}
{{% card link="/tutorials/services/try-viam-color-detection/" %}}
{{% card link="/tutorials/services/navigate-with-rover-base/" %}}
{{< /cards >}}
