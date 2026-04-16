---
linkTitle: "Add a component"
title: "Add a component"
weight: 20
layout: "docs"
type: "docs"
no_list: true
description: "Every component type Viam supports, with step-by-step guides for adding each one to your machine."
aliases:
  - /hardware-components/components/
  - /hardware/components/
  - /hardware/common-components/
  - /hardware/component-types/
  - /hardware-components/component-types/
---

Every component on your machine has a **type** that determines its API, which defines what methods your code can call on it.
Pick the type whose API best describes what your hardware does, then use the per-type guide to add a model and configure it.
The general add-a-component process is the same for every type.
For the universal steps, see [Configure hardware components](/hardware/configure-hardware/).

## Control an arm, gripper, or gantry

| Component                                             | What it does                                                                                               | Examples                                    |
| ----------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- | ------------------------------------------- |
| [Arm](/hardware/common-components/add-an-arm/)        | Control a multi-joint robotic arm: move joints, position the end effector, integrate with motion planning. | xArm, UR5, custom serial arms               |
| [Gripper](/hardware/common-components/add-a-gripper/) | Open, close, and grasp objects with a gripper mounted on an arm or gantry.                                 | Parallel-jaw grippers, vacuum grippers      |
| [Gantry](/hardware/common-components/add-a-gantry/)   | Move a tool head, camera, or sensor to precise coordinates along one or more linear axes.                  | Single-axis stages, multi-axis CNC gantries |

## Sensing

Components that read data from the physical world.

| Component                                                             | What it does                                                                                 | Examples                                             |
| --------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| [Camera](/hardware/common-components/add-a-camera/)                   | Capture images or video from a USB webcam, IP camera, or depth sensor.                       | USB webcams, IP cameras, depth cameras, lidar        |
| [Sensor](/hardware/common-components/add-a-sensor/)                   | Read environmental data: temperature, humidity, distance, air quality, and more.             | Temperature, humidity, air quality, distance sensors |
| [Movement sensor](/hardware/common-components/add-a-movement-sensor/) | Get position, velocity, orientation, or compass heading from a GPS, IMU, or odometry source. | GPS, IMU, accelerometer, gyroscope, odometry         |
| [Power sensor](/hardware/common-components/add-a-power-sensor/)       | Monitor voltage, current, and power consumption.                                             | INA219, INA226, current clamps                       |
| [Encoder](/hardware/common-components/add-an-encoder/)                | Track how far a motor has turned and how fast it's spinning.                                 | Incremental encoders, absolute encoders              |

## Drive a mobile robot

| Component                                       | What it does                                                                                                                                        | Examples                                              |
| ----------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| [Base](/hardware/common-components/add-a-base/) | Drive a mobile robot with movement commands like "move forward 300mm" or "spin 90 degrees." A base wraps your drive system into a single interface. | Wheeled rovers, tracked vehicles, holonomic platforms |

## Control motors and servos

| Component                                         | What it does                                                        | Examples                                    |
| ------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------- |
| [Motor](/hardware/common-components/add-a-motor/) | Control a DC or stepper motor through a motor driver and GPIO pins. | DC motors, stepper motors, brushless motors |
| [Servo](/hardware/common-components/add-a-servo/) | Set the angular position of a hobby servo with a PWM pin.           | Hobby servos, PWM-controlled actuators      |

## Control

Components for physical I/O and user interaction.

| Component                                                                | What it does                                                                                                                    | Examples                                      |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------- |
| [Board](/hardware/common-components/add-a-board/)                        | Expose GPIO pins, analog readers, and digital interrupts from a single-board computer. Many other components depend on a board. | Raspberry Pi GPIO, Arduino, custom I/O boards |
| [Button](/hardware/common-components/add-a-button/)                      | Detect presses from a physical button to trigger actions.                                                                       | Momentary switches, push buttons              |
| [Switch](/hardware/common-components/add-a-switch/)                      | Read or set the position of a toggle or selector switch.                                                                        | Toggle switches, selector switches            |
| [Input controller](/hardware/common-components/add-an-input-controller/) | Use a gamepad, joystick, or other input device for manual machine control.                                                      | Gamepads, joysticks, custom button panels     |

## Other

| Component                                             | What it does                                                          | Examples                                    |
| ----------------------------------------------------- | --------------------------------------------------------------------- | ------------------------------------------- |
| [Generic](/hardware/common-components/add-a-generic/) | Interface with hardware that doesn't fit any standard component type. | Custom devices with non-standard interfaces |

## Choosing a type

Match your hardware to the type whose API best describes what it does:

- If it **produces images**, use [camera](/hardware/common-components/add-a-camera/).
- If it **produces readings** (temperature, distance, pressure), use [sensor](/hardware/common-components/add-a-sensor/).
- If it **reports position or motion** (GPS, IMU), use [movement sensor](/hardware/common-components/add-a-movement-sensor/).
- If it **spins or drives linear motion**, use [motor](/hardware/common-components/add-a-motor/).
- If it **moves to an angle**, use [servo](/hardware/common-components/add-a-servo/).
- If you need **direct GPIO access**, use [board](/hardware/common-components/add-a-board/).
- If **nothing fits**, use [generic](/hardware/common-components/add-a-generic/). It provides `DoCommand` for arbitrary interactions.

Every type also has a `DoCommand` method for functionality beyond the standard API.
For example, a sensor that also has a calibration routine can expose calibration through `DoCommand` while still using `GetReadings` for its primary data.
