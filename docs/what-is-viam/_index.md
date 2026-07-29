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
date: "2025-01-30"
---

Viam is a software platform for building, deploying, and managing robotics applications.

With Viam, you declare the hardware and services you need in a JSON config. Viam installs the drivers and any additional software modules required to support your configuration.
Vision, motion planning, and most other capabilities you need are built in or available in the Viam module Registry, all with well-defined APIs to support your use case.
Application code versioning, deployment, and rollback are native to the Viam platform.
It's the development workflow you're used to, applied to physical devices.

Viam brings software engineering practices to robotics: version control, remote monitoring and diagnostics, staged rollouts, and a registry of modules and models you can build on.

<img src="/what-is-viam-technical.svg" alt="Architecture diagram showing how a Viam machine works: app.viam.com at top, connected to your machine running viam-agent and viam-server with hardware drivers, software integrations, built-in services, and your code, connected to physical peripherals at bottom." style="width:100%;max-width:720px;height:auto;display:block" >

## Viam fundamentals

Every Viam machine starts with `viam-agent`.
Install it with a single command.
`viam-agent` installs `viam-server`, supervises it, and keeps it up to date.

`viam-server` is the core runtime.
It pulls your machine's configuration from app.viam.com, fetches the necessary modules from the Viam Registry, launches required processes, and keeps them running to support all the hardware and services your application requires.

The [Viam Registry](https://app.viam.com/registry) is a central repository of modules, ML models, and training scripts maintained by Viam and the robotics community.
All registry assets support semantic versioning, enabling controlled deployment to individual robots and across your fleet.

Registry modules provide drivers for cameras, motors, sensors, arms, and other hardware, plus services like object detection.
`viam-server` also includes built-in services such as motion planning and data management.
For machine learning, the Registry includes pretrained models for common tasks. You can also train and use your own models.

Viam supports reusable configuration through [fragments](/fleet/reuse-configuration/).
Define a combination of components, services, and modules once, then apply that configuration across any number of machines.
Use fragments to configure a camera-arm combination, a camera-to-object-detection pipeline, or an entire work cell.
Fragments support variable substitution and per-machine overwrites, so you can deploy the same base configuration to hundreds of machines while accommodating site-specific settings.

For a closer look at how machines, parts, components, services, and modules relate, and the difference between using the APIs and authoring a module, see [How Viam fits together](platform-model/).

## Viam capabilities

- **[Get hardware running in minutes](/hardware/):** Add a camera, motor, arm, or sensor to your configuration with a few parameters. `viam-server` pulls the driver and exposes the device through a consistent API. No writing drivers, no managing dependencies.
- **[Operate from anywhere](/monitor/):** Connect to a machine over the network with no VPN or port forwarding. Stream logs, view live camera and sensor data, teleoperate, and see a 3D view of the machine, all from the browser.
- **[Capture data from edge to cloud](/data/):** Configure which components to record and how often. Data syncs when bandwidth allows, queues locally when a machine goes offline, and can be filtered at the edge to control cost.
- **[Train and deploy models](/train/):** Train machine learning models on captured data, or bring models from TensorFlow, PyTorch, or ONNX. Deploy them to your fleet and run inference on the device.
- **[Develop code remotely](/reference/sdks/):** Write code on your laptop and run it against machine hardware over the network. When you are ready, package it as a module for production.
- **[Manage software deployments](/build-modules/):** Package your control logic as a module and deploy it through the Registry. Pin machines to exact versions or allow automatic updates, and push new versions over the air.
- **[Scale easily](/fleet/):** Apply one fragment to dozens or hundreds of machines, update them fleet-wide from a single change, override per-machine differences, and roll changes out or back incrementally.
- **[Productize with Viam apps](/build-apps/overview/):** Build customer-facing web and mobile apps with the TypeScript and Flutter SDKs, add white-label authentication, and bill customers through Viam.

## Next steps

We recommend putting these concepts into practice by following the [Try Viam tutorial](/try/) to build your first machine.

For more information on cloud capabilities like fleet management and provisioning, see [Monitor Air Quality with a Fleet of Sensors](/tutorials/control/air-quality-fleet/).
