---
linkTitle: "What is Viam?"
title: "What is Viam?"
weight: 10
layout: "docs"
type: "docs"
no_list: true
images: ["/general/understand.png"]
imageAlt: "Viam platform overview"
description: "Viam is a software platform for building, deploying, and managing robotics applications."
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
date: "2026-05-27"
---

Viam is a software platform for building, deploying, and managing robotics applications.

A Viam machine is hardware plus the software that runs it: cameras, motors, arms, and sensors, together with the services and code that control them. You build a machine by declaring the parts you need in a JSON configuration, and `viam-server` installs the drivers and modules to support them.

Every component of the same type exposes the same API. All cameras work through one camera interface, all motors through one motor interface, and the same holds for sensors, arms, and other component types. Your code does not change when the hardware does: swap an Intel RealSense camera for an Orbbec Astra, update the configuration, and your application keeps working.

Vision, motion planning, data management, and most other capabilities are either built into `viam-server` or available in the [Viam Registry](https://app.viam.com/registry), a shared catalog of modules, machine learning models, and training scripts maintained by Viam and the robotics community. You build on these instead of writing them from scratch.

You manage a machine the way you manage software. Configuration, code, and models are versioned, so you can deploy updates, roll them back, and pin a machine to an exact version. You monitor machines remotely and stage changes across a fleet before rolling them out everywhere. It is the development workflow you already use, applied to physical devices.

## How it works

Every Viam machine runs two programs.
`viam-agent` installs with a single command, then installs `viam-server`, supervises it, and keeps it up to date.
`viam-server` is the runtime: it pulls your machine's configuration from [app.viam.com](https://app.viam.com), fetches the modules it needs from the Registry, and runs the hardware drivers, services, and code your application requires.

<img src="/what-is-viam-technical.svg" alt="Architecture diagram showing how a Viam machine works: app.viam.com at top, connected to your machine running viam-agent and viam-server with hardware drivers, software integrations, built-in services, and your code, connected to physical peripherals at bottom." style="width:100%;max-width:720px;height:auto;display:block" >

To run the same setup on more than one machine, turn a working configuration into a [fragment](/fleet/reuse-configuration/) and apply it across your fleet.
Fragments support variable substitution and per-machine overrides, so one base configuration can serve hundreds of machines with site-specific settings.

## What you can do with Viam

- **[Get hardware running in minutes](/hardware/):** Add a camera, motor, arm, or sensor to your configuration with a few parameters. `viam-server` pulls the driver and exposes the device through a consistent API. No writing drivers, no managing dependencies.
- **[Operate from anywhere](/monitor/):** Connect to a machine over the network with no VPN or port forwarding. Stream logs, view live camera and sensor data, teleoperate, and see a 3D view of the machine, all from the browser.
- **[Capture data from edge to cloud](/data/):** Configure which components to record and how often. Data syncs when bandwidth allows, queues locally when a machine goes offline, and can be filtered at the edge to control cost.
- **[Train and deploy models](/train/):** Train machine learning models on captured data, or bring models from TensorFlow, PyTorch, or ONNX. Deploy them to your fleet and run inference on the device.
- **[Develop code remotely](/reference/sdks/):** Write code on your laptop and run it against machine hardware over the network. When you are ready, package it as a module for production.
- **[Manage software deployments](/build-modules/):** Package your control logic as a module and deploy it through the Registry. Pin machines to exact versions or allow automatic updates, and push new versions over the air.
- **[Scale easily](/fleet/):** Apply one fragment to dozens or hundreds of machines, update them fleet-wide from a single change, override per-machine differences, and roll changes out or back incrementally.
- **[Productize with Viam apps](/build-apps/overview/):** Build customer-facing web and mobile apps with the TypeScript and Flutter SDKs, add white-label authentication, and bill customers through Viam.

## Next steps

Put these concepts into practice by following the [Try Viam tutorial](/try/) to build your first machine.

For more on fleet management and provisioning, see [Monitor air quality with a fleet of sensors](/tutorials/control/air-quality-fleet/).
