---
linkTitle: "Use input to act"
title: "Use input to determine actions"
weight: 70
layout: "docs"
type: "docs"
no_list: true
description: "Actuate your machine based on sensor readings or other inputs."
---

You can program your machine to move based on sensor readings or other inputs.

{{% alert title="Disambiguation" color="tip" %}}
If you want to act or send alerts based on computer vision, see [Act based on inferences](/data-ai/ai/act/) or [Alert on inferences](/data-ai/ai/alert/).
To alert based on data, see [Alert on data](/data-ai/data/advanced/alert-data/).
{{% /alert %}}

## Prerequisites

{{% expand "A running machine connected to the Viam app. Click to see instructions." %}}

{{% snippet "setup.md" %}}

{{% /expand%}}

{{% expand "Components configured on your machine." %}}

[Configure your sensing and actuation hardware](/operate/get-started/supported-hardware/) as components of your machine.

This may include sensors, cameras, motors, bases, arms, gantries, servos, grippers, or other components.

{{% /expand%}}

## Program your machine

{{< table >}}
{{% tablestep %}}
**1. Start building your app**

Depending on your use case, see [Create a web app](/operate/control/web-app/), [Create a mobile app](/operate/control/mobile-app/), or [Create a headless app](/operate/control/headless-app/) for information on installing an SDK and connecting your code to your machine.

{{% /tablestep %}}
{{% tablestep %}}
**2. Get an input**

Use one of the input APIs, such as:

- [Sensor](/dev/reference/apis/components/sensor/)

  - Input methods include `GetReadings`.
    Python example:

    ```python {class="line-numbers linkable-line-numbers"}
    my_sensor = Sensor.from_robot(robot=machine, name='my_sensor')

    # Get the readings provided by the sensor.
    readings = await my_sensor.get_readings()
    ```

- [Power sensor](/dev/reference/apis/components/power-sensor/)

  - Input methods include `GetVoltage`, `GetCurrent`, `GetPower`, and `GetReadings`.

- [Board](/dev/reference/apis/components/board/)
  - Input methods include `GetGPIO`, `GetPWM`, `PWMFrequency`, `GetDigitalInterruptValue`, and `ReadAnalogReader`.

If you are using camera input with computer vision, see [Act based on inferences](/data-ai/ai/act/) for relevant examples.

{{% /tablestep %}}
{{% tablestep %}}
**3. Actuate based on the input**

To move your actuator, use your actuator component's API, with logic based on your input:

- [Motor](/dev/reference/apis/components/motor/)

  - Actuation methods include `SetPower`, `SetRPM`, `GoFor`, `GoTo`, `Stop`.
    Python example:

    ```python {class="line-numbers linkable-line-numbers"}
    my_motor = Motor.from_robot(robot=machine, name="my_motor")

    # Assume your sensor returns a reading with a key called "level"
    # If the sensor reads less than 50, spin the motor at 95 RPM.
    current_level = readings.get('level')
    if (current_level < 50):
        await my_motor.set_rpm(rpm=95)
    else:
        await my_motor.stop()
    ```

- [Servo](/dev/reference/apis/components/servo/)
  - Actuation methods include `Move`.
- [Gripper](/dev/reference/apis/components/gripper/)
  - Actuation methods include `Open`, `Grab`, `Stop`.
- [Board](/dev/reference/apis/components/board/)
  - Input methods include `SetGPIO`, `SetPWM`, `SetPWMFrequency`, and `WriteAnalog`.

If your use case involves planning coordinated motion of multiple motors, see [Move a base](/operate/mobility/move-base/), [Move an arm](/operate/mobility/move-arm/), or [Move a gantry](/operate/mobility/move-gantry/) for more information on how to automate intelligent motion planning.
Instead of actuating using the component API, you can use the [motion service API](/dev/reference/apis/services/motion/)'s `Move`, `MoveOnMap`, or `MoveOnGlobe` commands.

{{% /tablestep %}}
{{% /table %}}

## Usage examples

To water a plant based on moisture sensor readings using the board API, see [Plant watering robot with a Raspberry Pi](/tutorials/projects/make-a-plant-watering-robot/).

To turn a fan on or off based on air quality sensor data, see [Automate air filtration with air quality sensors](https://codelabs.viam.com/guide/air-quality/index.html?index=..%2F..index#0).
