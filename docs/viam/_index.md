---
title: "Viam in 3 minutes"
linkTitle: "Viam in 3 minutes"
description: "Viam is a complete software platform for robots which provides modular robot components and services for vision, motion, SLAM, ML, and data management."
weight: 10
no_list: true
type: docs
aliases:
    - "/getting-started/"
    - "/getting-started/high-level-overview"
    - "/product-overviews/"
images: ["/img/understand.png"]
---

Viam is a complete software platform that supports every step of your robot development lifecycle.

## Plan your robot

When using Viam, this is what you'll need to know to plan your robot:

<img src="https://assets-global.website-files.com/62fba5686b6d47fe2a1ed2a6/633d91b848050946efcf0690_viam-overview-illustrations-build.svg" alt="A diagram of robotic parts and software" class="alignright" style="width:250px;"></img>

- **Hardware**:
Many {{< glossary_tooltip term_id="component" text="robotic components">}} are natively supported by the Viam platform.
You will not need to write a single line of code to integrate them, and swapping out component models will not require code changes.
- **Functionality**:
You can make use of computer vision, motion planning, SLAM, data management, machine learning, and more by configuring Viam's built-in {{< glossary_tooltip term_id="service" text="services">}}.
- **Architecture**:
You can build simple robots or multi-part robots that use secure communication channels across local networks and the cloud, all of which can be managed with a uniform API.
- **Extensibility**: If you need additional functionality, you can leverage community contributed and custom resources to [extend](/extend) Viam.

Join the [**Viam community**](https://discord.gg/viam) to collaborate during planning and beyond.

## Get started

A *robot* in Viam consists of at least one computer, typically a [single-board computer](/installation/), running `viam-server` and communicating with any hardware connected to it by signaling through digital data pins.
Viam supports devices running **any** 64-bit Linux OS or macOS.

<img src="img/board-viam-server.png" alt="A diagram of a single-board computer running viam-server." class="alignleft" style="max-width:270px"></img>

The Viam platform provides a user interface for connecting to and managing robots, the [Viam app](https://app.viam.com/).

To use the Viam platform with your robot, log in to [the app](https://app.viam.com/), create a new robot, and [install](/installation/) the [`viam-server`](https://github.com/viamrobotics/rdk) binary which:

- Creates, configures, and maintains the robot.
- Securely handles all communications.
- Runs drivers, custom code, and any other software.
- Accepts API requests.
- Runs services like computer vision, data synchronization, and motion planning.

{{% alert title="Info" color="info" %}}
Everything Viam runs on your robot is [open-source](https://github.com/viamrobotics).
{{% /alert %}}

## Configure your robot

Robots can be small and simple or very complex.
A robot can be a single-board computer with a single sensor or LED wired to it, or a robot can consist of multiple computers with many physical components connected, acting as one unit.

The term {{% glossary_tooltip term_id="component" text="*component*" %}} describes a piece of hardware that a computer controls, like an arm or a motor.

For each component that makes up your robot:

<img src="img/test_components.png" alt="Multiple components being tested in the Viam app." class="alignright" style="max-width:320px"></img>

1. Add it to your robot by [choosing the component type](/manage/configuration/#components) (example: `camera`) and model (example: `webcam`).
2. Test it with the visual [control tab](/manage/fleet/robots/#control).
3. See any problems with in-app [logs](/manage/fleet/robots/#logs), review or roll back configuration [history](/manage/fleet/robots/#history).

After configuring your robot's hardware, you can configure [high level functionality](/services/) the same way:

- **Data Management** enables you to capture and sync data from one or more robots, and use that data for machine learning and beyond.
- **Fleet management** enables you to configure, control, debug, and manage entire fleets of robots.
- **Motion planning** enables your robot to plan and move itself.
- **Vision** enables your robot to intelligently see and interpret the world around it.
- **Simultaneous Localization And Mapping (SLAM)** enables your robot to map its surroundings and find its position on a map.

![Robot components](img/robot-components.png)

## Control your robot

<img src="https://assets-global.website-files.com/62fba5686b6d47fe2a1ed2a6/63334e5e19a68d329b1c5b0e_viam-overview-illustrations-manage.svg" alt="A diagram illustrating secure robot control." class="alignleft" style="max-width:270px;"></img>

The Viam platform provides a consistent programming interface for all robots, allowing you to [control your robots](/program/sdks/) with code in the **language of your choice**.
Viam currently has SDKs for [Go](https://pkg.go.dev/go.viam.com/rdk), [Python](https://python.viam.dev/), and [TypeScript](https://ts.viam.dev/).
Additional SDKs are coming soon, including Rust, Java, C++, and Flutter.

TLS certificates provided by [app.viam.com](https://app.viam.com) ensure that all communication is authenticated and encrypted.
Viam uses {{< glossary_tooltip term_id="webrtc" >}} to create secure peer-to-peer paths between robots and clients for fast, low-latency communication.
The Viam cloud does not receive any command or control information regarding your robots, ensuring low latency, robustness, and privacy.
With WebRTC established, Viam uses {{< glossary_tooltip term_id="grpc" text="gRPC" >}} so you can program your robot in many common programming languages.

This provides flexibility and security whether you are building tight control loops for autonomous mobile robots, event-based triggers for IoT devices, or custom web-based robot management interfaces.

There are four categories of APIs:

- [Robot](https://github.com/viamrobotics/api/blob/main/proto/viam/robot/v1/robot.proto) provides high level robot commands
- [Components](/components/) like motors, arms, GPS
- [Services](/services/) like computer vision, motion planning, SLAM
- Cloud applications like [Fleet Management](/manage/fleet/), [Data Management](/manage/data/)

You can see the Viam API specification on [GitHub](https://github.com/viamrobotics/api).

### Network flexibility

Your robot does not need to be connected to the cloud.

The `viam-server` software resides on your robot alongside your configurations, your code, and appropriate services.
In scenarios without cloud connectivity, you can still connect your robot to a local area network (LAN), or to any relevant devices (such as a gamepad).
It all depends on your use case and configuration.

- All APIs work locally or in the cloud
- Data is cached locally and synced when possible
- Configuration is cached

When your robot is connected (to either LAN or WAN), `viam-server` can act as both a client and a server.
In other words, each instance can request resources, as well as provide them.
This allows for tremendous flexibility in terms of your architecture design.

## Scale

With robots in production, Viam provides [fleet management capabilities](/manage/fleet/) to help you scale.
With it you can:

- Manage permissions within your organization and locations.
- Manage software across your fleet, including deployment of code and machine learning models.
- Keep your robot configuration and capabilities up-to-date.

## Next steps

Start by borrowing one of our robots.
Use [Try Viam](/try-viam/).

If you already have your own robot, [set up `viam-server`](/installation/) and learn how Viam helps you prototype and scale.

For more inspiration, check out our [tutorials](/tutorials/) or visit our community on [Discord](https://discord.gg/viam) to get help or workshop ideas with others!
