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

## Built-in models vs. module models

Each component type page lists the **models** available for that type.
Models come from two sources:

- **Built-in models** ship with `viam-server` and work out of the box.
  For example, the `webcam` model for cameras or the `gpio` model for motors.
- **Module models** come from the [Viam registry](https://app.viam.com/registry)
  or from modules you write yourself.
  If your hardware isn't supported by a built-in model, you can
  [write a driver module](/build-modules/write-a-driver-module/) that implements
  the same standard API.

Both kinds of models are configured and used identically. The distinction
matters only when you're setting up a machine for the first time and need to
know whether you can use a built-in model or need to find or write a module.

## What's next

- [How components work](/hardware/configure-hardware/): understand components
  and walk through adding any component to your machine.
- [Add a component](/hardware/common-components/): step-by-step guides for each
  component type.
