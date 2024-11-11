---
title: "Configure your Viam Rover with a Fragment"
linkTitle: "Configure your Viam Rover"
weight: 20
type: "docs"
tags: ["rover", "tutorial"]
description: "Configure your rover by adding the Viam-provided configuration fragment to your rover."
aliases:
  - "/try-viam/rover-resources/rover-tutorial-fragments/"
  - "/get-started/try-viam/rover-resources/rover-tutorial-fragments/"
date: "2022-01-01"
# updated: ""  # When the content was last entirely checked
---

To be able to drive your rover, you need to configure it.
Viam provides reusable {{% glossary_tooltip term_id="fragment" text="*fragments*" %}} for [Viam rovers](https://www.viam.com/resources/rover).

## Prerequisites

- An assembled Viam Rover.
  For assembly instructions, see [Unbox and Set Up your Viam Rover](../rover-tutorial/)
- The board is connected to the [Viam app](https://app.viam.com).
  To add your Pi to the Viam app, refer to [the rover setup guide](/appendix/try-viam/rover-resources/rover-tutorial/#control-your-rover-on-the-viam-app).

## Add the fragment

Follow the appropriate instructions for the model of rover and board you have:

{{< tabs >}}
{{% tab name="Viam Rover 2 (RPi 5)" %}}

Navigate to your machine in the [Viam app](https://app.viam.com/robots).
In the left-hand menu of the **CONFIGURE** tab, click the **+** (Create) icon next to the machine {{< glossary_tooltip term_id="part" text="part" >}} you want to add the fragment to.

Select **Insert fragment**.
Now, you can see the available fragments to add.
Select [`ViamRover2-2024-rpi5`](https://app.viam.com/fragment/11d1059b-eaed-4ad8-9fd8-d60ad7386aa2/json) and click **Insert fragment** again to add the fragment to your machine configuration:

{{<imgproc src="appendix/try-viam/rover-resources/fragments/fragments_list.png" resize="400x" style="width: 500px" alt="List of available fragments">}}

Click **Save** in the upper right corner of the page to save your new configuration.

The fragment adds the following components to your machine's JSON configuration:

- A [board component](/components/board/) named `local` representing the Raspberry Pi.
- Two [motors](/components/motor/gpio/) (`right` and `left`)
  - The configured pin numbers correspond to where the motor drivers are connected to the board.
- Two [encoders](/components/encoder/single/), one for each motor
- A wheeled [base](/components/base/), an abstraction that coordinates the movement of the right and left motors
  - Width between the wheel centers: 356 mm
  - Wheel circumference: 381 mm
  - Spin slip factor: 1
- A webcam [camera](/components/camera/webcam/)
- An [accelerometer](https://github.com/viam-modules/tdk-invensense/tree/main/mpu6050)
- A [power sensor](https://github.com/viam-modules/texas-instruments/tree/main/ina)

For information about how to configure components yourself when you are not using the fragment, click the links on each component above.
To see the configured pin numbers and other values specific to this fragment, [view it in the app](https://app.viam.com/fragment?id=7c413f24-691d-4ae6-a759-df3654cfe4c8).

{{% /tab %}}
{{% tab name="Viam Rover 2 (RPi 4)" %}}

Navigate to your machine in the [Viam app](https://app.viam.com/robots).
In the left-hand menu of the **CONFIGURE** tab, click the **+** (Create) icon next to the machine {{< glossary_tooltip term_id="part" text="part" >}} you want to add the fragment to.

Select **Insert fragment**.
Now, you can see the available fragments to add.
Select [`ViamRover2-2024-rpi4-a`](https://app.viam.com/fragment/7c413f24-691d-4ae6-a759-df3654cfe4c8/json) and click **Insert fragment** again to add the fragment to your machine configuration:

{{<imgproc src="appendix/try-viam/rover-resources/fragments/fragments_list.png" resize="400x" style="width: 500px" alt="List of available fragments">}}

Click **Save** in the upper right corner of the page to save your new configuration.

The fragment adds the following components to your machine's JSON configuration:

- A [board component](/components/board/) named `local` representing the Raspberry Pi.
- Two [motors](/components/motor/gpio/) (`right` and `left`)
  - The configured pin numbers correspond to where the motor drivers are connected to the board.
- Two [encoders](/components/encoder/single/), one for each motor
- A wheeled [base](/components/base/), an abstraction that coordinates the movement of the right and left motors
  - Width between the wheel centers: 356 mm
  - Wheel circumference: 381 mm
  - Spin slip factor: 1
- A webcam [camera](/components/camera/webcam/)
- An [accelerometer](https://github.com/viam-modules/tdk-invensense/tree/main/mpu6050)
- A [power sensor](https://github.com/viam-modules/texas-instruments/tree/main/ina)

For information about how to configure components yourself when you are not using the fragment, click the links on each component above.
To see the configured pin numbers and other values specific to this fragment, [view it in the app](https://app.viam.com/fragment?id=7c413f24-691d-4ae6-a759-df3654cfe4c8).

{{% /tab %}}
{{% tab name="Viam Rover 1 (RPi 4)" %}}

Navigate to your machine in the [Viam app](https://app.viam.com/robots).
In the left-hand menu of the **CONFIGURE** tab, click the **+** (Create) icon next to the machine {{< glossary_tooltip term_id="part" text="part" >}} you want to add the fragment to.

Select **Insert fragment**.
Now, you can see the available fragments to add.
Select [`ViamRover202210b`](https://app.viam.com/fragment/3e8e0e1c-f515-4eac-8307-b6c9de7cfb84/json) and click **Insert fragment** again to add the fragment to your machine configuration:

{{<imgproc src="appendix/try-viam/rover-resources/fragments/fragments_list.png" resize="400x" style="width: 500px" alt="List of available fragments">}}

Click **Save** in the upper right corner of the page to save your configuration.

The fragment adds the following components to your machine's JSON configuration:

- A [board component](/components/board/) named `local` representing the Raspberry Pi
  - An I<sup>2</sup>C bus for connection to the accelerometer.
- Two [motors](/components/motor/gpio/) (`right` and `left`)
  - The configured pin numbers correspond to where the motor drivers are connected to the board.
- Two [encoders](/components/encoder/single/), one for each motor
- A wheeled [base](/components/base/), an abstraction that coordinates the movement of the right and left motors
  - Width between the wheel centers: 260 mm
  - Wheel circumference: 217 mm
  - Spin slip factor: 1
- A webcam [camera](/components/camera/webcam/)
- An [accelerometer](https://github.com/viam-modules/analog-devices/tree/main/adxl345)

{{% alert title="Info" color="info" %}}

This particular motor driver has pins labeled "ENA" and "ENB."
Typically, this would suggest that they should be configured as enable pins, but on this specific driver these function as PWM pins, so we configure them as such.

{{% /alert %}}

For information about how you would configure a component yourself if you weren't using the fragment, click the links on each component above.
To see the configured pin numbers and other values specific to this fragment, [view it in the app](https://app.viam.com/fragment?id=3e8e0e1c-f515-4eac-8307-b6c9de7cfb84).

{{% /tab %}}
{{% tab name="Viam Rover 2 (Jetson Nano)" %}}

Navigate to your machine in the [Viam app](https://app.viam.com/robots).
In the left-hand menu of the **CONFIGURE** tab, click the **+** (Create) icon next to the machine {{< glossary_tooltip term_id="part" text="part" >}} you want to add the fragment to.

Select **Insert fragment**.
Now, you can see the available fragments to add.
Select [`ViamRover2-2024-jetson-nano-a`](https://app.viam.com/fragment/747e1f43-309b-4311-b1d9-1dfca45bd097/json) and click **Insert fragment** again to add the fragment to your machine configuration.

{{<imgproc src="appendix/try-viam/rover-resources/fragments/fragments_list.png" resize="400x" style="width: 500px" alt="List of available fragments">}}

Click **Save** in the upper right corner of the page to save your new configuration.

The fragment adds the following components to your machine's JSON configuration:

- A [board component](/components/board/) named `local` representing the Jetson.
- Two [motors](/components/motor/gpio/) (`right` and `left`)
  - The configured pin numbers correspond to where the motor drivers are connected to the board.
- Two [encoders](/components/encoder/single/), one for each motor
- A wheeled [base](/components/base/), an abstraction that coordinates the movement of the right and left motors
  - Width between the wheel centers: 356 mm
  - Wheel circumference: 381 mm
  - Spin slip factor: 1
- A webcam [camera](/components/camera/webcam/)
- An [accelerometer](https://github.com/viam-modules/tdk-invensense/tree/main/mpu6050)
- A [power sensor](https://github.com/viam-modules/texas-instruments/tree/main/ina)

For information about how to configure components yourself when you are not using the fragment, click the links on each component above.
To see the configured pin numbers and other values specific to this fragment, [view it in the app](https://app.viam.com/fragment?id=747e1f43-309b-4311-b1d9-1dfca45bd097).

{{% /tab %}}
{{% tab name="Viam Rover 2 (Jetson Orin Nano)" %}}

Navigate to your machine in the [Viam app](https://app.viam.com/robots).
In the left-hand menu of the **CONFIGURE** tab, click the **+** (Create) icon next to the machine {{< glossary_tooltip term_id="part" text="part" >}} you want to add the fragment to.

Select **Insert fragment**.
Now, you can see the available fragments to add.
Select [`ViamRover2-2024-nano-orin-a`](https://app.viam.com/fragment/6208e890-8400-4197-bf0f-e8ddeca4e157/json) and click **Insert fragment** again to add the fragment to your machine configuration:

{{<imgproc src="appendix/try-viam/rover-resources/fragments/fragments_list.png" resize="400x" style="width: 500px" alt="List of available fragments">}}

Click **Save** in the upper right corner of the page to save your new configuration.

The fragment adds the following components to your machine's JSON configuration:

- A [board component](/components/board/) named `local` representing the Jetson.
- Two [motors](/components/motor/gpio/) (`right` and `left`)
  - The configured pin numbers correspond to where the motor drivers are connected to the board.
- Two [encoders](/components/encoder/single/), one for each motor
- A wheeled [base](/components/base/), an abstraction that coordinates the movement of the right and left motors
  - Width between the wheel centers: 356 mm
  - Wheel circumference: 381 mm
  - Spin slip factor: 1
- A webcam [camera](/components/camera/webcam/)
- An [accelerometer](https://github.com/viam-modules/tdk-invensense/tree/main/mpu6050)
- A [power sensor](https://github.com/viam-modules/texas-instruments/tree/main/ina)

For information about how to configure components yourself when you are not using the fragment, click the links on each component above.
To see the configured pin numbers and other values specific to this fragment, [view it in the app](https://app.viam.com/fragment?id=6208e890-8400-4197-bf0f-e8ddeca4e157).

{{% /tab %}}
{{< /tabs >}}

## See the components on the configuration page

Adding a fragment to your machine adds the configuration to your machine.
The components and services included in the fragment will now appear as cards on the **CONFIGURE** tab, along with a card for your fragment:

{{<imgproc src="appendix/try-viam/rover-resources/fragments/fragments_cards.png" resize="400x" style="width: 500px" alt="List of available fragments">}}

## Modify the config

The fragment you added is read-only, but if you need to modify your rover's config you can [overwrite sections of the fragment](/how-tos/one-to-many/#modify-a-fragment).

## Next steps

After you have configured your rover, follow one of these tutorials:

{{< cards >}}
{{% card link="/how-tos/drive-rover/" %}}
{{% card link="/how-tos/detect-color/" %}}
{{% card link="/tutorials/services/navigate-with-rover-base/" %}}
{{< /cards >}}
