---
title: "Viam in 3 minutes"
linkTitle: "Viam in 3 minutes"
weight: 10
no_list: true
type: docs
aliases:
    - /getting-started
---

Viam is a complete software platform for robots.

#### Platform Quickstart: Using the App

The most simple way to create your first robot on the Viam platform is through our user interface for connecting with and managing robots, the [Viam app](app.viam.com).

Create an account, and create a new robot on there, even if you don't know what you want your robot to look like yet.
You'll be redirected to a control center for this new robot.

The Viam platform natively handles the following for you:

- **Data management** enabling you to capture and sync data from one or more robots.
- **Fleet management** enabling you to configure, control, debug, and manage entire fleets of robots.
- **Motion** enabling your robot to plan and move itself.
- **Vision** enabling your robot to intelligently see and interpret the world around it.
- **Simultaneous Localization And Mapping (SLAM)** enabling your robot to map its surroundings and find its position on a map.

On top of these services, the Viam platform provides a consistent programming interface for all robots, allowing you to program your robots in the language of your choice.

To make use of these features, all you need to do is:

1) Follow one of our [installation guides](/installation) to connect a development machine or a single-board computer to the in-app control center.
2) Configure the robot's [components](/components) and [services](/services).

## What's a robot?

A *robot* in Viam consists of at least one computer, like a [Raspberry Pi](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html), running `viam-server` along with the hardware the computer controls.
The term *component* describes a piece of hardware that a computer controls, like an arm or a motor.

Robots can be small and simple or very complex.
A robot can be a single-board computer with a single [sensor](/components/sensor/) or LED wired to it, or a robot can consist of multiple computers with many physical components connected, acting as one unit.

![Robot components](img/robot-components.png)

## `viam-server`: The software on your robot

[`viam-server`](https://github.com/viamrobotics/rdk) is the open-source software which runs on each computer in a robot and:

- Creates, configures, and maintains the robot
- Securely handles all communications
- Runs drivers, custom code, and any other software
- Accepts API requests
- Runs services like computer vision, data synchronization, and motion planning

The Viam platform uses the cloud for configuration.
Configuration describes how hardware and software interact.
A basic example that you can configure using the Viam platform is connecting a computer to a camera.
A more advanced example is a computer connected to a camera, actuating components (like motors or arms), and an ML model.

Skip ahead to our [installation guide](/installation/) to get started with installing and running `viam-server` on your robot.

{{% alert title="Info" color="info" %}}
Everything Viam runs on your robot is [open-source](http://github.com/viamrobotics).
{{% /alert %}}

## Networking: Connecting to your robot

Your robot does not need to be permanently connected to the internet to work:

- All APIs work locally or in the cloud
- Data is cached locally and synced when possible
- Configuration is cached

When your robot is connected (either LAN or WAN), `viam-server` can act as both a client and a server.
In other words, each instance can request resources, as well as provide them.
This allows for tremendous flexibility.

## Communication: Talking to your robot

TLS certificates provided by [app.viam.com](https://app.viam.com) ensure that all communication is both authenticated and encrypted.

Viam uses [WebRTC](https://webrtc.org/) to create secure peer-to-peer paths between robots and clients for fast, low latency communication.
The Viam cloud does not receive any command or control information regarding your robots, ensuring low latency, robustness, and privacy.

With WebRTC established, Viam uses [gRPC](https://grpc.io/) so you can program your robot in most common programming languages.

## APIs: Services for your robot

There are four categories of APIs:

- [Robot](/services/robot-service/) - high level robot commands
- [Components](/components) like motors, arms, GPS
- [Services](/services) like computer vision, motion planning, SLAM
- Cloud Applications like [fleet management](/manage/fleet-management), [data management](/manage/data-management)

To see the Viam API specification, check [GitHub](https://github.com/viamrobotics/api).

## SDKs: Programming your robot

We provide SDKs in several languages to easily connect to your robot, use components and services, and create custom modular resources.

Viam currently has SDKs for [Go](https://pkg.go.dev/go.viam.com/rdk) and [Python](https://python.viam.dev/).
Additional SDKs are coming soon, including Typescript, Rust, Java, C++, and Flutter.

## Next Steps

Start by borrowing one of our robots.
Use [Try Viam](/try-viam/).

If you already have your own robot, [set up `viam-server`](/installation/) and learn how Viam helps you prototype and scale.

For more inspiration, check out our [tutorials](/tutorials) or visit our community on [Slack](https://join.slack.com/t/viamrobotics/shared_invite/zt-1f5xf1qk5-TECJc1MIY1MW0d6ZCg~Wnw/) to get help or workshop ideas with others!
