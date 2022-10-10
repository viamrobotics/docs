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

We recommend using our cloud app to configure, manage, and control your robots at http://app.viam.com/

A robot's configuration lives in the cloud.
The configuration is a description of the hardware and higher level software services.
For example how a motor is connected to a Raspberry PI, or what matching learning models you want to use for classification.

On the robot, a single viam process, called _viam-server_ runs, and is responsible for: 
- keeping the configuration up to date
- logging to the cloud
- connecting to hardware
- running and other code that is needed, such as drivers for hardware, or user code.
- accepting API requests either for data or for hardware actuation
- running higher level services like computer vision, data synchronization, or motion planning

Your robot code can run directly on the robot, or anywhere else with internet connectivity you want and access all the same functionality.

## API

All communication across Viam is done with gRPC[^grpc], directly if wanted, or via webrtc[^webrtc], which provides authentication and encryption.

[^grpc]: <a href="https://grpc.io/" target="_blank">gRPC</a>
[^webrtc]: <a href="https://en.wikipedia.org/wiki/WebRTC)" target="_blank">WebRTC: ht<span></span>tps://en.wikipedia.org/wiki/WebRTC</a> 

There are three buckets of APIs
- [Components](/components)
- [Services](/services)
- Cloud Application

You can see all Viam API specifications at https://github.com/viamrobotics/api

## Concepts

### Robot
A _Robot_ in Viam is 1 or more computers, combined into 1 logical robot.
A mobile robot that has 1 Jetson and 1 raspberry pi is 1 robot.
The bounds of a robot are usually pretty clear, but can be subjective. 

### Part
Each of those computers are a _Part_. In that example, you have 1 robot, and 2 parts (the jetson and pi).

Most simple robots will likely only have 1 part, but can have as many as you need.

Parts are organized in a tree, with one of them being the _main_ part, and the others being _sub parts_.
You can access any sub part either directly, or via any part above it in the tree.

Each part runs a single _viam-server_ instance.

### Component

A component is a piece of hardware or software that exposes a specific API, such as arm, motor, or gps.
These components are configured, and then the drivers are loaded by _viam server_.
Every part will likely have at least 1 component, but some will have a lot.
For example, a raspberry pi part on a mobile robot might have: 4 motors, gps, imu, and a camera.

### Service

[Services](/services) offer higher level software abstractions.

For example: motion planning and computer vision.

### Remote

A remote is a server that implementats the same GRPC interfaces, including the robot service which describs what it provides.
Parts can talk to arbitrary processes to add more components by adding them as a remote.
If a remote is added to a part, that part will that proxy all requests.

Remotes are typically implemented with SDKs.

Examples: 
- a robot arm manufacturer has a network attached arm that implementats the Viam API, you can add it directly to a part as a remote.
- a POE camera implementats the camera grpc interface, so can be added directly as a remote.

### Process
Processes are scripts or programs run by the [Robot Development Kit (RDK)](../../appendix/glossary#rdk_anchor) whose life cycle is managed by the Viam server.
One example is running a [Software Development Kit (SDK)](/product-overviews/sdk-as-server) server like the Python SDK where the implementation of a component is easier to create than in the RDK.

## SDKs

While you can connect to a robot with gRPC directly, we provide SDKs to make this easier, and handle authentication and webrtc.

SDKs are used for:
- writing your application code for building your robot to interact with the components and services
- implementing drivers for hardware not yet supported

We currently have SDKs for go, Python, Typescript, and Rust. With many more coming soon including c++ and flutter

## Pictures

![two-part-architecture](../img/overview-two-part-architecture.png)  
_Figure 1.
An example of a two-part robot.
Each part has its own compute unit which runs an instance of `viam-server` and communicates with its respective components.
Part 1 is the main part and could exist without Part 2.
Part 2 is a remote._

## Next steps

If you have hardware lying around, the best thing to do is try to get it setup.

If there are issues, please work with us on [slack](https://viamrobotics.slack.com/) as we're still working on rough edges.

We also have a number of [tutorials](/tutorials) to get you started.

If you have no hardware, you can use our mock tutorial FIX ME.


