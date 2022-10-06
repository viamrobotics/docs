---
title: "What is Viam?"
linkTitle: "What is Viam?"
weight: 1
type: "docs"
description: "A high-level overview of Viam."
---
A robot is a computer that interacts with its environment.
What does this mean? A robot can collect information about its environment and make behavioral decisions on based on that information.

Robots don't all look the same. They can range in complexity from a simple wheeled rover to a base with various [_components_](/docs/#components) such as grippers, arms, cameras and other sensors.
A simple system might be controlled by a single computer (such as a Raspberry Pi, Jetson or Arduino), whereas a more complex system might involve multiple computers controlling different parts of the robot.
Whether their physical hardware is simple or complex, robots built on Viam can use our [_services_](/docs/#services) - on-device software with complex capabilities such as SLAM, Computer Vision, Motion Planning, and Data Collection. 

At Viam, each computer (and the components it controls) is called a _part_.
Robots are organized into one or more parts, depending on the number of computers they're comprised of.
A robot with multiple parts will have one main part and any number of _sub-parts_.
A robot with multiple parts will have one main part and any number of _sub-parts_.
Each part runs a session of the viam-server, which handles receiving API requests and translating them into hardware actuation.
The viam-server reads in a configuration file that defines the components, services, and other processes.

Processes are scripts or programs run by the [Robot Development Kit (RDK)](/docs/product-overviews/rdk) whose life cycle is managed by the Viam server.
One example is running a [Software Development Kit (SDK)](/docs/product-overviews/sdk-as-server) server like the Python SDK where the implementation of a component is easier to create than in the RDK.

Each `viam-server` instance is defined by a configuration file that describes its components, the services it employs, and connections to other viam-server instances that it wants to communicate with, which we call _remotes_.
A remote represents a connection to another robot.

![two-part-architecture](../img/overview-two-part-architecture.png)  
_Figure 1.
An example of a two-part robot.
Each part has its own compute unit which runs an instance of `viam-server` and communicates with its respective components.
Part 1 is the main part and could exist without Part 2.
Part 2 is a remote._

Parts communicate with one another using a consistent and unified API, regardless of the hardware they are running on.
This is done via [WebRTC](https://en.wikipedia.org/wiki/WebRTC) using the [gRPC and protobuf APIs](../../deeper-dive/architecture-and-protobuf).
This SDK API is available in any language, and provides direct and secure connections to and between parts.

After installing the Viam server on a computer, you can connect your newly minted part to Viam ([https://app.viam.com](https://app.viam.com)).
The website provides a page for each of the following:

- Logs: Displays `viam-server` logs including status changes and error messages.
- Config: Provides a UI for building out your robot configuration.
- Control: Provides a basic UI for testing your robot components and services without needing to write any script–for example, driving the motors and viewing camera feeds.
- Connect: Contains boilerplate connection code to copy and paste into any script you write using SDKs.

SDK-based applications can be run locally on one part of the robot or on an entirely separate computer (like your laptop).
They use the same APIs as the web UI.

![laptop-architecture](../img/overview-laptop-architecture.png)  
_Figure 2.
Example architecture showing how SDK-based applications communicate with your robot’s main instance of `viam-server` over gRPC._

If your hardware isn't supported by Viam’s RDK, you can write your own implementation of a component model.
If a library already exists, then you just need to write a few lines of code.
To read more on how to do this, check out our documentation on [Using Our SDKs for a Server Component Implementation](/docs/product-overviews/sdk-as-server).
Your part will manage this process and expose the API as it does with all of your other components.

<<<<<<< HEAD
If and when you start collaborating with other users, you may wish to manage their access to different robots.
You can organize robots, users, and organizations using [Viam’s Organizational Management System](/docs/product-overviews/organization-management).

More detailed information can be found in the product overview and deep dive documents.
To start making robots with Viam, [get a viam-server running on a Raspberry Pi](/docs/getting-started/installation) or explore our other [tutorials](/docs/tutorials/tutorials).
=======
If and when you start collaborating with other users, then you may wish to manage their access to different robots.
You can organize robots, users, and organizations using [Viam’s Organizational Management System](/docs/product-overviews/organization-management).

More detailed information can be found in the product overview and deep dive documents.
To start making robots with Viam, [Get a Viam-Server Running on a Raspberry Pi](/docs/getting-started/installation) or explore our other [Tutorials](/docs/tutorials/tutorials).
>>>>>>> 0dbe555c (additional copy edits)
