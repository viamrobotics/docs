---
linkTitle: "Add a component"
title: "Add a component"
weight: 20
layout: "docs"
type: "docs"
no_list: true
description: "Step-by-step guides for adding and configuring each component type."
aliases:
  - /hardware-components/components/
  - /hardware/components/
  - /hardware/common-components/
---

Each guide walks you through adding a specific component type to your machine:
choosing a model, configuring attributes, and verifying it works.
The general process is the same for every component -- [How components work](/hardware/configure-hardware/) covers the universal steps.
The guides below add component-specific details: tested attribute examples, working code, and troubleshooting.

If you're not sure which component type you need, start with
[Component types](/hardware/component-types/).

## Control an arm, gripper, or gantry

| Component                                             | Description                                                                                                |
| ----------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| [Arm](/hardware/common-components/add-an-arm/)        | Control a multi-joint robotic arm: move joints, position the end effector, integrate with motion planning. |
| [Gripper](/hardware/common-components/add-a-gripper/) | Open, close, and grasp objects with a gripper mounted on an arm or gantry.                                 |
| [Gantry](/hardware/common-components/add-a-gantry/)   | Move a tool head, camera, or sensor to precise coordinates along one or more linear axes.                  |

## Sensing

Components that read data from the physical world.

| Component                                                             | Description                                                                                  |
| --------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| [Camera](/hardware/common-components/add-a-camera/)                   | Capture images or video from a USB webcam, IP camera, or depth sensor.                       |
| [Sensor](/hardware/common-components/add-a-sensor/)                   | Read environmental data: temperature, humidity, distance, air quality, and more.             |
| [Movement sensor](/hardware/common-components/add-a-movement-sensor/) | Get position, velocity, orientation, or compass heading from a GPS, IMU, or odometry source. |
| [Power sensor](/hardware/common-components/add-a-power-sensor/)       | Monitor voltage, current, and power consumption.                                             |
| [Encoder](/hardware/common-components/add-an-encoder/)                | Track how far a motor has turned and how fast it's spinning.                                 |

## Drive a mobile robot

| Component                                       | Description                                                                                                                                         |
| ----------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Base](/hardware/common-components/add-a-base/) | Drive a mobile robot with movement commands like "move forward 300mm" or "spin 90 degrees." A base wraps your drive system into a single interface. |

## Control motors and servos

| Component                                         | Description                                                         |
| ------------------------------------------------- | ------------------------------------------------------------------- |
| [Motor](/hardware/common-components/add-a-motor/) | Control a DC or stepper motor through a motor driver and GPIO pins. |
| [Servo](/hardware/common-components/add-a-servo/) | Set the angular position of a hobby servo with a PWM pin.           |

## Control

Components for physical I/O and user interaction.

| Component                                                                | Description                                                                                                                     |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------- |
| [Board](/hardware/common-components/add-a-board/)                        | Expose GPIO pins, analog readers, and digital interrupts from a single-board computer. Many other components depend on a board. |
| [Button](/hardware/common-components/add-a-button/)                      | Detect presses from a physical button to trigger actions.                                                                       |
| [Switch](/hardware/common-components/add-a-switch/)                      | Read or set the position of a toggle or selector switch.                                                                        |
| [Input controller](/hardware/common-components/add-an-input-controller/) | Use a gamepad, joystick, or other input device for manual machine control.                                                      |

## Other

| Component                                             | Description                                                           |
| ----------------------------------------------------- | --------------------------------------------------------------------- |
| [Generic](/hardware/common-components/add-a-generic/) | Interface with hardware that doesn't fit any standard component type. |
