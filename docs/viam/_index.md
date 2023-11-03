---
title: "Viam in 3 minutes"
linkTitle: "Viam in 3 minutes"
description: "Viam is a complete software platform for smart machines which provides modular components and services for vision, motion, SLAM, ML, and data management."
weight: 10
no_list: true
type: docs
aliases:
  - "/getting-started/"
  - "/getting-started/high-level-overview"
  - "/product-overviews/"
image: "/general/understand.png"
imageAlt: "/general/understand.png"
images: ["/general/understand.png"]
---

Viam is a complete software platform that supports every step of your {{< glossary_tooltip term_id="smart-machine" text="smart machine">}} development lifecycle.

## Plan your smart machine

When using Viam, this is what you'll need to know to plan your smart machine:

<img src="https://assets-global.website-files.com/62fba5686b6d47fe2a1ed2a6/633d91b848050946efcf0690_viam-overview-illustrations-build.svg" alt="A diagram of smart machine parts and software" class="alignright" style="width:250px;"></img>

- **Hardware**:
  Many {{< glossary_tooltip term_id="component" text="components">}} are natively supported by the Viam platform.
  You will not need to write a single line of code to integrate them, and swapping out component models will not require code changes.
- **Functionality**:
  You can make use of computer vision, motion planning, SLAM, data management, machine learning, and more by configuring Viam's built-in {{< glossary_tooltip term_id="service" text="services">}}.
- **Architecture**:
  You can build simple smart machines or multi-part smart machines that use secure communication channels across local networks and the cloud, all of which can be managed with a uniform API.
- **Extensibility**: If you need additional functionality, you can leverage {{< glossary_tooltip term_id="modular-resource" text="modular resources" >}} from the Viam registry to extend support in Viam to new hardware components and software services.

Join the [**Viam community**](https://discord.gg/viam) to collaborate during planning and beyond.

## Get started

A _smart machine_ in Viam consists of at least one computer, typically a [single-board computer](/installation/), running `viam-server` and communicating with any hardware connected to it by signaling through digital data pins.
Viam supports devices running **any** 64-bit Linux OS or macOS.

{{< imgproc src="/viam/board-viam-server.png" alt="A diagram of a single-board computer running viam-server." resize="270x" class="alignleft" style="max-width:270px" >}}

The Viam platform provides a user interface for connecting to and managing smart machines, the [Viam app](https://app.viam.com/).

To use the Viam platform with your smart machine, log in to [the app](https://app.viam.com/), create a new robot, and [install](/installation/) the [`viam-server`](https://github.com/viamrobotics/rdk) binary which:

- Creates, configures, and maintains the smart machine.
- Securely handles all communications.
- Runs drivers, custom code, and any other software.
- Accepts API requests.
- Runs services like computer vision, data synchronization, and motion planning.

{{% alert title="Info" color="info" %}}
Everything Viam runs on your smart machine is [open-source](https://github.com/viamrobotics).
{{% /alert %}}

## Configure your smart machine

Robots can be small and simple or very complex.
A smart machine can be a single-board computer with a single sensor or LED wired to it, or a smart machine can consist of multiple computers with many physical components connected, acting as one unit.

The term {{% glossary_tooltip term_id="component" text="_component_" %}} describes a piece of hardware that a computer controls, like an arm or a motor.

For each component that makes up your smart machine:

<p>
{{< imgproc src="/viam/test_components.png" alt="Multiple components being tested in the Viam app." resize="320x" style="max-width:320px" class="alignright" >}}
</p>

1. Add it to your robot by [choosing the component type](/manage/configuration/#components) (example: `camera`) and model (example: `webcam`).
2. Test it with the visual [control tab](/manage/fleet/robots/#control).
3. See any problems with in-app [logs](/manage/fleet/robots/#logs), review or roll back configuration [history](/manage/fleet/robots/#history).

After configuring your smart machine's hardware, you can configure [high level functionality](/services/) the same way:

- **Data Management** enables you to capture and sync data from one or more smart machine, and use that data for machine learning and beyond.
- **Fleet management** enables you to configure, control, debug, and manage entire fleets of smart machines.
- **Motion planning** enables your smart machine to plan and move itself.
- **Vision** enables your smart machine to intelligently see and interpret the world around it.
- **Simultaneous Localization And Mapping (SLAM)** enables your smart machine to map its surroundings and find its position on a map.

<div>
{{< imgproc src="/viam/robot-components.png" alt="Robot components" resize="600x" class="aligncenter" >}}
</div>

## Control your smart machine

<img src="https://assets-global.website-files.com/62fba5686b6d47fe2a1ed2a6/63334e5e19a68d329b1c5b0e_viam-overview-illustrations-manage.svg" alt="A diagram illustrating secure smart machine control." class="alignleft" style="max-width:270px;"></img>

The Viam platform provides a consistent programming interface for all smart machines, allowing you to [control your smart machines](/program/apis/) with code in the **language of your choice**.
Viam currently has SDKs for [Go](https://pkg.go.dev/go.viam.com/rdk), [Python](https://python.viam.dev/), and [TypeScript](https://ts.viam.dev/).
Additional SDKs are coming soon, including Rust, Java, C++, and Flutter.

TLS certificates provided by [app.viam.com](https://app.viam.com) ensure that all communication is authenticated and encrypted.
Viam uses {{< glossary_tooltip term_id="webrtc" >}} to create secure peer-to-peer paths between smart machines and clients for fast, low-latency communication.
The Viam cloud does not receive any command or control information regarding your smart machines, ensuring low latency, robustness, and privacy.
With WebRTC established, Viam uses {{< glossary_tooltip term_id="grpc" text="gRPC" >}} so you can program your smart machines in many common programming languages.

This provides flexibility and security whether you are building tight control loops for autonomous mobile smart machines, event-based triggers for IoT devices, or custom web-based smart machine management interfaces.

There are four categories of APIs:

- [Robot](https://github.com/viamrobotics/api/blob/main/proto/viam/robot/v1/robot.proto) provides high level robot commands
- [Components](/components/) like motors, arms, GPS
- [Services](/services/) like computer vision, motion planning, SLAM
- Cloud applications like [Fleet Management](/manage/fleet/), [Data Management](/manage/data/)

You can see the Viam API specification on [GitHub](https://github.com/viamrobotics/api).

### Network flexibility

Your smart machine does not need to be connected to the cloud.

The `viam-server` software resides on your smart machine alongside your configurations, your code, and appropriate services.
In scenarios without cloud connectivity, you can still connect your smart machine to a local area network (LAN), or to any relevant devices (such as a gamepad).
It all depends on your use case and configuration.

- All APIs work locally or in the cloud
- Data is cached locally and synced when possible
- Configuration is cached

When your smart machine is connected (to either LAN or WAN), `viam-server` can act as both a client and a server.
In other words, each instance can request resources, as well as provide them.
This allows for tremendous flexibility in terms of your architecture design.

## Scale

With smart machines in production, Viam provides [fleet management capabilities](/manage/fleet/) to help you scale.
With it you can:

- Manage permissions within your organization and locations.
- Manage software across your fleet, including deployment of code and machine learning models.
- Keep your smart machine configuration and capabilities up-to-date.

## Extensibility

You can also extend Viam to support additional hardware components or software services by deploying a module from the [Viam registry](https://app.viam.com/registry) to your smart machine.

The Viam registry allows hardware and software engineers to collaborate on their smart machine projects by writing and sharing custom modules with each other.
You can add a module from the Viam registry directly from your smart machine's **Configuration** tab in [the Viam app](https://app.viam.com/), using the **+ Create component** button.
You can also [upload your own module to the Viam registry](/modular-resources/upload/).

See [Modular resources](/modular-resources/) for more information.

## Next steps

Start by borrowing one of our rovers.
Use [Try Viam](/try-viam/).

If you already have your own smart machine, [set up `viam-server`](/installation/) and learn how Viam helps you prototype and scale.

For more inspiration, check out our [tutorials](/tutorials/) or visit our community on [Discord](https://discord.gg/viam) to get help or workshop ideas with others!
