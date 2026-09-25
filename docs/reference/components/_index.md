---
title: "Built-in components"
linkTitle: "Built-in components"
weight: 20
type: "docs"
layout: "docs"
no_list: true
description: "Configuration reference for Viam's built-in components: per-component models, attributes, and JSON templates."
capabilities: ["section-index"]
date: "2026-09-24"
aliases:
  - /operate/reference/components/
---

Built-in components are resource types that ship with [`viam-server`](/reference/viam-server/) for controlling common hardware.
Each component type has one standard API, so your application code works the same way regardless of the exact device attached—a USB webcam and an IP camera are both cameras as far as your code is concerned.

Because they are built in, you can add built-in components to any machine's configuration without installing a separate module.
If a built-in component doesn't fit your use case, you can also find community and Viam-maintained component models in the [Viam registry](https://app.viam.com/registry) or [build your own](/build-modules/overview/).

Each page below covers available models, configuration attributes, and JSON templates.
For API method reference, see [Component APIs](/reference/apis/components/).

| Component                                                   | Description                                                                                |
| ----------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| [Arm](/reference/components/arm/)                           | A multi-joint robotic arm that moves its end effector through 3D space                     |
| [Base](/reference/components/base/)                         | A mobile platform that other parts of a mobile robot attach to                             |
| [Board](/reference/components/board/)                       | A signal wire hub that provides access to GPIO pins and hardware interfaces                |
| [Button](/reference/components/button/)                     | A pushbutton or binary switch input                                                        |
| [Camera](/reference/components/camera/)                     | A device that captures images or point clouds                                              |
| [Encoder](/reference/components/encoder/)                   | A device that measures rotation or linear position of a motor or joint                     |
| [Gantry](/reference/components/gantry/)                     | A mechanical system that uses linear motion to position a tool or payload                  |
| [Generic](/reference/components/generic/)                   | A catch-all API for devices that don't fit other component types                           |
| [Gripper](/reference/components/gripper/)                   | A device that grabs and releases objects                                                   |
| [Input controller](/reference/components/input-controller/) | A human-interface device like a gamepad, joystick, or keyboard                             |
| [Motor](/reference/components/motor/)                       | A device that converts electrical energy into rotary or linear motion                      |
| [Movement sensor](/reference/components/movement-sensor/)   | A device that reports position, velocity, or orientation (GPS, IMU, accelerometer)         |
| [Power sensor](/reference/components/power-sensor/)         | A device that measures voltage, current, or power consumption                              |
| [Sensor](/reference/components/sensor/)                     | A general-purpose device that returns readings (temperature, humidity, pressure, and more) |
| [Servo](/reference/components/servo/)                       | A motor that moves to and holds a specific angular position                                |
| [Switch](/reference/components/switch/)                     | A device that toggles between discrete states (on/off, multi-position)                     |
