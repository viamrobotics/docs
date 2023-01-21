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

## Robots

A *robot* in Viam is a single-board computer, like a [Raspberry Pi](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html), running `viam-server` along with the hardware the computer controls.
The term *component* describes a piece of hardware that a computer controls, like an arm or a motor.

Robots can be small and simple or very complex.
A movement sensor connected to a single-board computer is a robot.
But a robot can also consist of multiple computers with many components, acting as one unit.
Each computer that runs `viam-server` in a robot is called a *part*.

![Robot components](img/robot-components.png)

## viam-server

[`viam-server`](https://github.com/viamrobotics/rdk) is the open-source software which runs on each part of a robot and:

- Creates, configures, and maintains the robot
- Securely communicates with your robot and the [Viam app](https://app.viam.com)
- Runs drivers, custom code, and any other software
- Accepts API requests
- Runs services like computer vision, data synchronization, and motion planning

A robot's configuration lives in the cloud on the [Viam app](https://app.viam.com).
Configuration describes how hardware and software interact.
A basic example that you can configure using the Viam platform is connecting a computer to a camera.
A more advanced example is a computer connected to a camera, actuating components (like motors or arms), and an ML model.

{{% alert title="Info" color="tip" %}}
Everything that runs on your robot is [open-source](http://github.com/viamrobotics).
{{% /alert %}}

## Networking

Your robot does not need to be permanently connected to the internet to work:

- All APIs work locally or in the cloud
- Data is cached locally and synced when possible
- Configuration is cached
- `viam-server` can act as both a client and a server.
  In other words, each instance can request services or resources, as well as provide them.
  This allows for tremendous flexibility.

## Communication

TLS certificates provided by [app.viam.com](https://app.viam.com) ensure that all communication is both authenticated and encrypted.

Viam uses [WebRTC](https://webrtc.org/) to create secure peer-to-peer paths between robots and clients for fast, low latency communication.
The Viam cloud does not receive any command or control information regarding your robots, ensuring low latency, robustness, and privacy.

With WebRTC established, Viam uses [gRPC](https://grpc.io/) so you can program your robot in most common programming languages.

## APIs

There are four categories of APIs:

- [Robot](/services/robot-service/) - high level robot commands
- [Components](/components) like motors, arms, GPS
- [Services](/services) like computer vision, motion planning, SLAM
- Cloud Applications like [fleet management](/services/fleet-management), [data management](/services/data-management)

To see the Viam API specification, check [GitHub](https://github.com/viamrobotics/api).

## SDKs

We provide SDKs in several languages to easily connect to your robot, use components and services, and create custom modular resources.

Viam currently has SDKs for [Go](https://pkg.go.dev/go.viam.com/rdk) and [Python](https://python.viam.dev/).
Additional SDKs are coming soon, including Typescript, Rust, Java, C++, and Flutter.

## Next Steps

Start by borrowing one of our robots.
Use [Try Viam](/try-viam/).

If you already have your own robot, [set up `viam-server`](/getting-started/app-usage/) and learn how Viam helps you prototype and scale.

For more inspiration, check out our [tutorials](/tutorials) or visit our community on [Slack](https://viamrobotics.slack.com/) to get help or workshop ideas with others!
