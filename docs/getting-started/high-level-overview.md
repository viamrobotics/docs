---
title: "What is Viam?"
linkTitle: "What is Viam?"
weight: 1
type: "docs"
description: "A high-level overview of Viam."
---

Viam's goal is to make it easy to take a robotics idea from paper, to prototype, to production, to scale. 

That includes making it easy to configure hardware, test hardware prototypes, write production code, deploy, and add features.

## Basics
Viam runs on your robot and the cloud.

Everything that runs on your robot is open source and is available at http://github.com/viamrobotics 

To get the most out of the Viam platform, we recommend using  http://app.viam.com/ to configure, manage, and control your robots

A robot's configuration lives in the cloud.
The configuration is a description of the hardware and higher level software services.
For example, how a motor is connected to a Raspberry Pi, or what matching learning models you want to use for classification.

On the robot, a single Viam process, called _viam-server_ runs, and is responsible for: 
- keeping the configuration up-to-date
- logging to the cloud
- connecting to hardware
- running and other code that is needed, such as drivers for hardware, or user code
- accepting API requests either for data or for hardware actuation
- running higher level services like computer vision, data synchronization, or motion planning

Your robot code can run directly on the robot itself or anywhere else with internet connectivity and access all the same functionality.

## API

All communication across Viam is done with gRPC[^grpc], directly if wanted, or via webrtc[^webrtc], which provides authentication and encryption.

[^grpc]: <a href="https://grpc.io/" target="_blank">gRPC</a>
[^webrtc]: <a href="https://en.wikipedia.org/wiki/WebRTC)" target="_blank">WebRTC: ht<span></span>tps://en.wikipedia.org/wiki/WebRTC</a> 

There are three buckets of APIs
- [Components](/components) - e.g. motors, arms, gps 
- [Services](/services) - computer vision, motion planning, slam
- Cloud Application - fleet management, data management

You can see all Viam API specifications at https://github.com/viamrobotics/api

## Concepts

### Robot
A _Robot_ in Viam is 1 or more computers combined into 1 logical robot.
A mobile robot that has one Jetson and one Raspberry Pi is one robot.
The bounds of a robot are usually pretty clear, but can be subjective. 

### Part
Each of those computers are a _Part_. In the above example, you have one robot, and two parts (the Jetson and the Pi).

Most simple robots will have only one part, but can have as many parts as needed.

Parts are organized in a tree, with one of them being the _main_ part, and the others being _sub-parts_.
You can access any sub-part either directly, or via any part above it in the tree.

Each part runs a single _viam-server_ instance.

### Component

A component is a piece of hardware or software that exposes a specific API, such as arm, motor, or gps.
These components are configured, and then the drivers are loaded by _viam-server_.
Every part will likely have at least 1 component, but some will have a lot.
For example, a Raspberry Pi part on a mobile robot might have: 4 motors, gps, imu, and a camera.

### Service

[Services](/services) offer higher level software abstractions.

For example: motion planning and computer vision.

### Remote

A remote is a server that implements the same gRPC interfaces, including the robot service which describes what it provides.
Parts can talk to arbitrary processes to add more components by adding them as a remote.
If a remote is added to a part, then that part will proxy all requests.

Remotes are typically implemented with SDKs.

Examples: 
- A robot arm manufacturer has a network attached arm that implements the Viam API, so you you can add it directly to a part as a remote.
- A POE camera implements the camera gRPC interface, so it can be added directly as a remote.

### Process
Processes are scripts or programs run by the [Robot Development Kit (RDK)](../../appendix/glossary#rdk_anchor) whose lifecycle is managed by the viam-server.
One example is running a [Software Development Kit (SDK)](/product-overviews/sdk-as-server) server like the Python SDK where the implementation of a component is easier to create than in the RDK.

## SDKs

While you can connect to a robot with gRPC directly, we provide SDKs to make this easier, and handle authentication and webrtc.

SDKs are used for:
- writing your application code for building your robot to interact with the components and services
- implementing drivers for hardware not yet supported

We currently have SDKs for go, Python, Typescript, and Rust. With many more coming soon including C++ and Flutter.

## Pictures

![two-part-architecture](../img/overview-two-part-architecture.png)  
_Figure 1.
An example of a two-part robot.
Each part has its own compute unit which runs an instance of `viam-server` and communicates with its respective components.
Part 1 is the main part and could exist without Part 2.
Part 2 is a remote._

## Next steps

If you have hardware lying around, the best thing to do is try to get it setup.

If you encounter issues, please work with us on [Slack](https://viamrobotics.slack.com/) as we're still working on rough edges.

Also, we have a number of [tutorials](/tutorials) to get you started.

If you have no hardware, you can use our mock tutorial FIX ME.


