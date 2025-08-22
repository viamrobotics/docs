---
linkTitle: "Use input to act"
title: "Use input to determine actions"
weight: 70
layout: "docs"
type: "docs"
no_list: true
description: "Actuate your machine based on sensor readings or other inputs."
toc_hide: true
---

You can program your machine to move based on sensor readings or other inputs.

## Prerequisites

{{% expand "A running machine connected to Viam. Click to see instructions." %}}

{{% snippet "setup.md" %}}

{{% /expand%}}

{{% expand "Components configured on your machine." %}}

[Configure your sensing and actuation hardware](/operate/get-started/supported-hardware/) as components of your machine.

This may include sensors, cameras, motors, bases, arms, gantries, servos, grippers, or other components.

{{% /expand%}}

## Program your machine

{{< table >}}
{{% tablestep start=1 %}}
**Start building your app**

Depending on your use case, see [Create a web app](/operate/control/web-app/), [Create a mobile app](/operate/control/mobile-app/), or [Create a headless app](/operate/control/headless-app/) for information on installing an SDK and connecting your code to your machine.

{{% /tablestep %}}
{{% tablestep %}}
**Get an input**

Use one of the input APIs, such as a [sensor's](/dev/reference/apis/components/sensor/) `GetReadings` method:

```python {class="line-numbers linkable-line-numbers"}
my_sensor = Sensor.from_robot(robot=machine, name='my_sensor')

# Get the readings provided by the sensor.
readings = await my_sensor.get_readings()
```

Other common inputs include the methods of a [board](/dev/reference/apis/components/board/) (`GetGPIO`, `GetPWM`, `PWMFrequency`, `GetDigitalInterruptValue`, and `ReadAnalogReader`), or a [power sensor](/dev/reference/apis/components/power-sensor/) (`GetVoltage`, `GetCurrent`, `GetPower`, and `GetReadings`).

You can also use camera input, for example to detect objects and pick them up with an arm.
See [Act based on inferences](/data-ai/ai/act/) for relevant examples.

If you want to send alerts based on computer vision or captured data, see [Alert on inferences](/data-ai/ai/alert/) or [Alert on data](/data-ai/data/advanced/alert-data/).

{{% /tablestep %}}
{{% tablestep %}}
**Actuate based on the input**

To move your actuator, use your actuator component's API, with logic based on your input.

For example, use the [motor API's](/dev/reference/apis/components/motor/) which includes methods like `SetPower`, `SetRPM`, `GoFor`, `GoTo`, and `Stop`.
A Python example:

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

Other actuation methods include the [servo API's](/dev/reference/apis/components/servo/) `Move` method, the [gripper API's](/dev/reference/apis/components/gripper/) `Open`, `Grab`, and `Stop` methods, and the [board API's](/dev/reference/apis/components/board/) `SetGPIO`, `SetPWM`, `SetPWMFrequency`, and `WriteAnalog` methods.

If your use case involves planning coordinated motion of multiple motors, see [Move a base](/operate/mobility/move-base/), [Move an arm](/operate/mobility/move-arm/), or [Move a gantry](/operate/mobility/move-gantry/) for more information on how to automate intelligent motion planning.
Instead of actuating using the component API, you can use the [motion service API](/dev/reference/apis/services/motion/)'s `Move`, `MoveOnMap`, or `MoveOnGlobe` commands.

{{% /tablestep %}}
{{% /table %}}

## Usage examples

To water a plant based on moisture sensor readings using the board API, see [Plant watering robot with a Raspberry Pi](/tutorials/projects/make-a-plant-watering-robot/).

To turn a fan on or off based on air quality sensor data, see [Automate air filtration with air quality sensors](https://codelabs.viam.com/guide/air-quality/index.html?index=..%2F..index#0).
