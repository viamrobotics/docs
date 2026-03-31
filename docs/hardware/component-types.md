---
linkTitle: "Component types"
title: "Component types"
weight: 5
layout: "docs"
type: "docs"
description: "All the component types Viam supports and when to use each one."
date: "2025-03-07"
aliases:
  - /hardware-components/component-types/
---

Every component on your machine has a **type** that determines its API,
which defines what methods your code can call on it.
Choosing the right type means platform features like data capture, test panels,
and the SDKs work with your hardware automatically.

## Sensing

These components read information from the physical world.

| Type                                                      | What it does                                                 | Examples                                             |
| --------------------------------------------------------- | ------------------------------------------------------------ | ---------------------------------------------------- |
| [Camera](/reference/components/camera/)                   | Captures 2D images or 3D point clouds                        | USB webcams, IP cameras, depth cameras, lidar        |
| [Encoder](/reference/components/encoder/)                 | Tracks rotational or linear position                         | Incremental encoders, absolute encoders              |
| [Movement sensor](/reference/components/movement-sensor/) | Reports position, orientation, velocity, or angular velocity | GPS, IMU, accelerometer, gyroscope, odometry         |
| [Power sensor](/reference/components/power-sensor/)       | Reports voltage, current, and power consumption              | INA219, INA226, current clamps                       |
| [Sensor](/reference/components/sensor/)                   | Returns key-value readings                                   | Temperature, humidity, air quality, distance sensors |

## Actuation

These components make things move.

| Type                                      | What it does                                                          | Examples                                              |
| ----------------------------------------- | --------------------------------------------------------------------- | ----------------------------------------------------- |
| [Arm](/reference/components/arm/)         | Controls a multi-jointed robotic arm                                  | xArm, UR5, custom serial arms                         |
| [Base](/reference/components/base/)       | Moves a mobile robot as a unit (no need to command individual motors) | Wheeled rovers, tracked vehicles, holonomic platforms |
| [Gantry](/reference/components/gantry/)   | Moves along linear rails with precise positioning                     | Single-axis stages, multi-axis CNC gantries           |
| [Gripper](/reference/components/gripper/) | Opens and closes a grasping device                                    | Parallel-jaw grippers, vacuum grippers                |
| [Motor](/reference/components/motor/)     | Drives rotational or linear motion with speed and position control    | DC motors, stepper motors, brushless motors           |
| [Servo](/reference/components/servo/)     | Moves to precise angular positions                                    | Hobby servos, PWM-controlled actuators                |

## Interface

These components provide low-level hardware access or human input.

| Type                                                        | What it does                                              | Examples                                      |
| ----------------------------------------------------------- | --------------------------------------------------------- | --------------------------------------------- |
| [Board](/reference/components/board/)                       | Exposes GPIO pins, analog readers, and digital interrupts | Raspberry Pi GPIO, Arduino, custom I/O boards |
| [Button](/reference/components/button/)                     | Reads presses from a physical button                      | Momentary switches, push buttons              |
| [Generic](/reference/components/generic/)                   | Catch-all for hardware that doesn't fit another type      | Custom devices with non-standard interfaces   |
| [Input controller](/reference/components/input-controller/) | Reads human input from control devices                    | Gamepads, joysticks, custom button panels     |
| [Switch](/reference/components/switch/)                     | Reads position from a multi-position switch               | Toggle switches, selector switches            |

## Choosing a type

Match your hardware to the type whose API best describes what it does:

- If it **produces images**, use [camera](/reference/components/camera/).
- If it **produces readings** (temperature, distance, pressure), use [sensor](/reference/components/sensor/).
- If it **reports position or motion** (GPS, IMU), use [movement sensor](/reference/components/movement-sensor/).
- If it **spins or drives linear motion**, use [motor](/reference/components/motor/).
- If it **moves to an angle**, use [servo](/reference/components/servo/).
- If you need **direct GPIO access**, use [board](/reference/components/board/).
- If **nothing fits**, use [generic](/reference/components/generic/). It provides `DoCommand` for arbitrary interactions.

Every type also has a `DoCommand` method for functionality beyond the standard
API. For example, a sensor that also has a calibration routine can expose
calibration through `DoCommand` while still using `GetReadings` for its primary
data.

## Models

Each component type has one or more **models**: drivers that know how to communicate with specific hardware. Some models ship with `viam-server` (like `webcam` for USB cameras or `gpio` for motors). Most hardware-specific models come from the [Viam registry](https://app.viam.com/registry). All models work the same way regardless of where they come from.

If no model exists for your hardware, you can [write a driver module](/build-modules/write-a-driver-module/) that implements the standard API for your device.

## Switching hardware without changing code

Because every model of a given type exposes the same API, your application
code doesn't change when you swap hardware. For example, this Python code
reads a motor's position:

```python
motor = Motor.from_robot(robot, "drive-motor")
position = await motor.get_position()
```

This works whether `drive-motor` is configured as a `gpio` motor on a
Raspberry Pi, a Trinamic stepper over CAN bus, or an ODrive brushless
controller. To switch hardware, you change the model and attributes in your
machine's configuration. Your code stays the same.

## What's next

- [How components work](/hardware/configure-hardware/): understand components
  and walk through adding any component to your machine.
- [Add a component](/hardware/common-components/): step-by-step guides for each
  component type.
