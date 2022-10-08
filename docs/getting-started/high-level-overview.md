---
title: "What is Viam?"
linkTitle: "What is Viam?"
weight: 1
type: "docs"
description: "A high-level overview of Viam."
---
## Basics
Viam runs on your robot and the cloud.

Everything that runs on your robot is open source and is availble at http://github.com/viamrobotics 

We reccomend using our cloud app to configure, manage, and control your robots at http://app.viam.com/

A robot's configuration lives in the cloud. The configuration is a description of the hardware and higher level software services. For example how a motor is connected to a Raspberry PI, or what maching learning models you want to use for classification.

On the robot, a single viam process, called _viam-server_ runs, and is responsible for: 
- keeping the configuration up to date
- logging to the cloud
- connecting to hardware
- running and other code that is needed, such as drivers for hardware, or user code.
- accepting API requests either for data or for hardware actuation

Your robot code can run directly on the robot, or anywhere else with internet connectivity you want and access all the same functionality.

### API

All communication across Viam is done with GRPC, directly if wanted, or via webrtc, which provides authentication and encryption.

You can see all Viam APIs at https://github.com/viamrobotics/api

All APIs specifications are open source.

### Concepts

#### Robot
A _Robot_ in Viam is 1 or more computers, combined into 1 logical robot. A mobile robot that has 1 Jetson and 1 raspberry pi is 1 robot.  The bounds of a robot are usually pretty clear, but can be subjective. 

#### Part
Each of those computers are a _Part_. In that example, you have 1 robot, and 2 parts (the jetson and pi).

Most simple robots will likely only have 1 part.

The parts are organized in a tree, with one of them being the _main_ part, and the others being _sub parts_.
You can access any sub part either directly, or via any part above it in the tree.
Therefore if you only talk to the main part, you can access the entire robot, so that the layout of the tree below can change without any code changes.

Each part runs a single _viam-server_ instance.

####  Component

A component is a piece of hwardware or software that exposes a specific API, such as arm, motor, or gps.
These components are configured, and then the drivers are loaded by _viam server_.
Every part will likely have at least 1 component, but some will have a lot.
For example, a raspberry pi part on a mobile robot might have: 4 motors, gps, imu, and a camera.

#### Remote

Parts can talk to arbitrary processes to add more components by adding them as a remote.
A remote is a server that implementats the same GRPC interfaces, including the robot service which describs what it provides.
If a remote is added to a part, that part will that proxy all requests.

For example, If you have an arm on a mobile robot, and it has it's own server that implementats the GRPC api, you can add it as a remote, and then control the arm via the part.

#### Process
Processes are scripts or programs run by the [Robot Development Kit (RDK)](../../appendix/glossary#rdk_anchor) whose life cycle is managed by the Viam server.
One example is running a [Software Development Kit (SDK)](/product-overviews/sdk-as-server) server like the Python SDK where the implementation of a component is easier to create than in the RDK.

### Pictures

![two-part-architecture](../img/overview-two-part-architecture.png)  
_Figure 1.
An example of a two-part robot.
Each part has its own compute unit which runs an instance of `viam-server` and communicates with its respective components.
Part 1 is the main part and could exist without Part 2.
Part 2 is a remote._

Parts communicate with one another using a consistent and unified API, regardless of the hardware they are running on.
This is done via <a href="https://en.wikipedia.org/wiki/WebRTC)" target="_blank">WebRTC</a>[^webrtc]  using the [gRPC and protobuf APIs](../../deeper-dive/architecture-and-protobuf).
This SDK API is available in any language, and provides direct and secure connections to and between parts.

[^webrtc]: <a href="https://en.wikipedia.org/wiki/WebRTC)" target="_blank">WebRTC: ht<span></span>tps://en.wikipedia.org/wiki/WebRTC</a> 

## Getting Started

After installing the Viam server on a computer (like a Raspberry Pi), you can connect your newly minted part to the Viam App ([https://app.viam.com](https://app.viam.com)).
The web app provides a page for each robot to do the following:

- Logs: Displays `viam-server` logs including status changes and error messages.
- Config: Provides a UI for building out your robot configuration.
- Control: Provides a basic UI for testing your robot components and services without needing to write any script–for example, driving the motors and viewing camera feeds.
- Connect: Contains boilerplate connection code to copy and paste into any script you write using SDKs.

SDK-based applications can be run locally on one part of the robot or on an entirely separate computer (like your laptop).
They use the same APIs as the web UI.

![laptop-architecture](../img/overview-laptop-architecture.png)  
_Figure 2.
Example architecture showing how SDK-based applications communicate with your robot’s main instance of `viam-server` over gRPC._

If your hardware isn't supported by Viam’s [RDK](../../appendix/glossary#rdk_anchor), you can write your own implementation of a component model.
If a library already exists, then you just need to write a few lines of code.
To read more on how to do this, check out our documentation on [Using Our SDKs for a Server Component Implementation](/product-overviews/sdk-as-server).
Your part will manage this process and expose the API as it does with all of your other components.

If and when you start collaborating with other users, then you may wish to manage their access to different robots.
You can organize robots, users, and organizations using [Viam’s Organizational Management System](/product-overviews/organization-management).

More detailed information can be found in the product overview and deep dive documents.
To start making robots with Viam, [Get a Viam-Server Running on a Raspberry Pi](/getting-started/installation) or explore our other [Tutorials](/tutorials/tutorials).

