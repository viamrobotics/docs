---
linkTitle: "What is Viam?"
title: "What is Viam?"
weight: 10
layout: "docs"
type: "docs"
no_list: true
images: ["/general/understand.png"]
imageAlt: "Viam platform overview"
description: "Understand the core concepts behind Viam: machines, parts, resources, models, and modules, and where to go next."
capabilities: ["docs", "viam-server", "viam-agent"]
diataxis: explanation
aliases:
  - /architecture/
  - /architecture/machine-to-machine-comms/
  - /reference/architecture/
  - /reference/architecture/machine-to-machine-comms/
  - /operate/reference/architecture/
  - /operate/reference/architecture/machine-to-machine-comms/
  - /dev/reference/architecture/
  - /internals/robot-to-robot-comms/
  - /internals/machine-to-machine-comms/
  - /dev/
  - /understand/
  - /understand/what-is-viam/
  - /what-is-viam/problems-viam-solves/
  - /what-is-viam/what-is-viam/
date: "2026-09-23"
---

Viam is a platform for building software that runs on physical devices.
You tell Viam what hardware and software capabilities your machine needs, and Viam handles the drivers, networking, and infrastructure so you can focus on what your machine actually does.

It is the development workflow you already know, applied to physical devices: version control, remote monitoring and diagnostics, staged rollouts, and a registry of modules and models you can build on.

<img src="/what-is-viam-technical.svg" alt="How a Viam machine fits together: your code runs on any computer and reaches the machine over WebRTC and gRPC. app.viam.com holds the module registry, data and ML, and fleet management, and sends configuration, modules, and ML models down to the machine, which sends data, logs, and status back up. On the machine's compute (the part), viam-agent supervises viam-server, which exposes resources: components for physical hardware and services for software capabilities. Components connect to cameras, motors, arms, sensors, boards, grippers, and other hardware over USB, GPIO, Ethernet, serial, or CAN." style="width:100%;max-width:720px;height:auto;display:block" >

## Platform mental model

Every device you connect to Viam is a machine made of parts, where each part runs a configuration of resources (components for hardware, services for software), and modules extend the platform with new resource types.

### Machines and parts

On the Viam platform, a **machine** is the combination of your compute resources and hardware that you want to control using Viam. A machine might be a robot arm with a gripper and a camera, a Raspberry Pi wired to some sensors, or a laptop collecting data through a webcam.

Every machine has at least one **part**: the computer that runs Viam's software and is connected to one or more physical devices.

A part can be almost any computer, including your own Mac or PC.
Two programs run there, `viam-agent` and `viam-server`, and [installing Viam](/set-up-a-machine/viam-agent-and-server/) sets up both.

### Configuration, resources, and models

Every part has a JSON [configuration](/hardware/machine-configuration/) describing what hardware is connected to the part and what that hardware can do.
You edit it on app.viam.com or the CLI, and the machine picks up your changes automatically.

Everything in the configuration is a **resource**. Resources come in two kinds:

- **Components** represent physical hardware: a camera, a motor, a sensor, an arm, a gripper, or a board. Each one wraps a piece of hardware and exposes a standard API for it (for example, an arm API with move commands or a camera API that returns images).
- **Services** are software capabilities running on the machine, such as computer vision, motion planning, data management, and any other code that controls the machine.

Every resource has an API, and a **model** is a specific implementation of that API.
For example, an SO-101 arm and a uFactory xArm6 arm are both models of the arm component API: they expose the same methods (`MoveToPosition`, `GetEndPosition`, and so on) even though the underlying hardware and protocols differ.
The same applies to services: the ML model service API has models for TFLite, ONNX, and other inference runtimes, each implementing the same `Infer` method.

When you configure a resource, you choose both the API (what kind of resource it is) and the model (which implementation to use).

### Built-in resources and modules

Some resources are **built-in**, meaning viam-server ships with them by default. These include services like [motion planning](/motion-planning/) and [computer vision](/vision/), as well as basic hardware drivers like [arms](/reference/components/arm/) and [cameras](/reference/components/camera/).

See [built-in components](/reference/components/) and [services](/reference/services/) for the full list.

Beyond builtins, the [Viam registry](https://app.viam.com/registry) has modules for hundreds of hardware drivers and software capabilities, maintained by Viam and the community.
Before building something yourself, check the registry and the built-in services to see if your use case already exists.

If nothing in the registry fits, you can [write and publish your own module](/build-modules/overview/).

## What you can do with Viam

| To do this                                           | Go here                                                          |
| ---------------------------------------------------- | ---------------------------------------------------------------- |
| Get a camera, motor, arm, or sensor running          | [Configure hardware](/hardware/)                                 |
| Capture data on the machine and sync it to the cloud | [Manage data](/data/)                                            |
| Train machine learning models on what you captured   | [Train ML models](/train/)                                       |
| Detect and classify objects in a camera feed         | [Computer vision](/vision/)                                      |
| Plan and execute motion for arms and mobile robots   | [Motion planning](/motion-planning/)                             |
| Write code that controls a machine over the network  | [Viam SDKs](/reference/sdks/)                                    |
| Control a machine from an AI agent or LLM            | [Use Viam from an AI agent](/build-apps/use-viam-from-an-agent/) |
| Package your own logic and deploy it to machines     | [Build and deploy modules](/build-modules/)                      |
| Build a web or mobile app for your customers         | [Build apps](/build-apps/overview/)                              |
| Watch machine status, stream data, and teleoperate   | [Monitor and operate](/monitor/)                                 |
| Configure and update many machines at once           | [Fleet deployment](/fleet/)                                      |
| Organize machines and control who can reach them     | [Admin and access](/organization/overview/)                      |

## Next steps

{{% alert title="Viam 101" color="tip" %}}
Our [**Viam 101 course**](https://www.viam.com/viam-101) is the fastest way to learn to build a robot, with no hardware and no prior robotics experience required.
{{% /alert %}}

- [Try Viam](/try/overview/) to work through a complete project without buying any hardware.
- [Set up your first machine](/set-up-a-machine/first-machine/) when you have a device ready to connect.
