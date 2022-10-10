---
title: "Glossary"
linkTitle: "Glossary"
weight: 30
type: "docs"
description: "A glossary of robotics and Viam-specific jargon."
---

## Viam-specific definitions

**Attribute**: A configuration parameter of a resource specific to a model.

**Base**: A physical, mobile component to which other components are typically mounted.
For example, a wheeled chassis and its drivetrain.

**Board**: An IO board connected to a robot part used to express low-level electronics functionality such as GPIO, SPI, or I2C.
Examples of boards include Jetson, Raspberry Pi, Numato, or Arduino.
Boards like Jetson and Pi run the Viam server and can expose the board component itself.

**Client Application**: Client applications are what applies the business logic to operate your robot. 
You can run a client application on the same part that runs the viam-server, or on a separate device.

**Component**: A resource that represents a physical component in a robot (RDK definition); for example, a servo, camera, or an arm.

**Fragment**: A reusable config block typically representing a common resource; for example, viam_gripper.
Available across an organization and when used in a config, gets merged (key/value wise) with a specific robot part.

**Frame**: A single element of a Frame System.
A frame represents a coordinate system that is used to describe position and orientation.
The location of a frame is described in relation to its parent frame using rigid transformations rather than in absolute terms.

**Frame System**: A hierarchy of frames that are related to one another via coordinate transformations.

<a href="https://en.wikipedia.org/wiki/GRPC" target="_blank">**gRPC**: gRPC Remote Procedure Calls</a>[^grpc] is a cross-platform open source high performance Remote Procedure Call (RPC) framework.

[^grpc]:GRPC, webpage, 2022, Wikipedia authors:  <a href="https://en.wikipedia.org/wiki/GRPC" target="_blank">ht<span><span>tps://en.wikipedia.org/wiki/GRPC</a> 

**Model**: A particular implementation of a component type.
For example, UR5e is a model of the arm component type.

**Packages**: Internal generalizable libraries that are not exposed to the user via proto and can be used by components and services to better implement functionality.

**Process**: Processes are binaries or scripts that run on a part. 
Processes are often used to create a new local instance of viam-server to implement drivers for custom components.
They provide a bespoke, OS-specific process managed by the viam-server to either run once or indefinitely; for example, to run one of Viam's camera servers.

<a id="rdk_anchor" />**RDK (Robot Development Kit)**: The official Viam-developed codebase that provides all functionality of an SDK and more. (golang)

* The RDK contains: 
    * Go SDK
    * Various packages and libraries (Motion Planning, Controls, Frame System, SLAM)
    * gRPC Server Implementations (hardware drivers)

* It can be used to build a server.
    * Can parse and respond to changes in a remote robot configuration file.
    * With updates possibly provided by the Viam App ([https://app.viam.com](https://app.viam.com)).
    * Initializes resources from a config.
    * Hosts a gRPC server implementing the Viam Robot API.
    * That serves functionality for all registered resources.

* It can be used as a client.
    * To connect to another robot implementing the Viam Robot API.

* Contains different libraries:
    * Motion Planning, Frame System, SLAM, Controls
    * These are used to help implement components/services.
{{% alert title="Note" color="note" %}}  
Libraries are called “services” ONLY if we expose their functionality in our proto APIs.
{{% /alert %}}

**Resource**: Resources are individual, addressable elements of a robot (RDK definition) operated by parts. 
Parts operate two types of Resources: physical components and software services.
Each part has local resources, and also surfaces remote resources when a remote is established to another part. 
The capabilities of each resource are exposed through the part’s API.

**Resource Config**: The configuration element of either a component or a service.
Typically expressed in JSON.

**Remote**: A robot part which is controlled by another robot part. 
The connection from one part to another part. 
Remotes are established using direct gRPC or gRPC via WebRTC. 
Within a robot, a main part always establishes a remote to each of the other parts associated with the robot. 
When a remote is established, the part establishing the remote will surface all of the other part’s resources as its own. 
A client application connecting to the part will see all of the part’s local resources and remote resources. 

You can establish remotes to parts in different robots. However, Viam recommends using a client application to control interaction between robots. 

**Remote UI**: Uses the Web JS SDK and provides UI elements to control a robot via WebRTC.

**Robot**: The configuration and entry point for a computer and components coupled into one logical grouping of parts that work together to complete tasks. 
A robot usually reflects a physical device, from a camera collecting images, to a wheeled rover, or an articulated arm on a factory floor. 
A robot always has a main part that receives client requests, and any number of other parts. 

A simple robot often contains a single part. 
For example, a rover has one main part with motors and a camera all attached to a board. 
However, a more sophisticated robot, like an autonomous arm, could consist of multiple parts. 
One main part receiving client application requests and relaying them to the other parts, one part with cameras for image processing, and one part for movement and actuating the arm.

**Robot Config**: The complete configuration of a single robot part.
Typically expressed in JSON.

**Robot Part**: A part runs an instance of viam-server to operate underlying resources – hardware components, software services, and any additional processes. Parts expose a uniform API for their resources. 

Every robot has a main part that receives client requests and any number of other parts. 
Parts connect to other parts by establishing a remote.  
For example, one robot may be composed of two parts, a Jetson and a Pi.
There is generally one robot part per CPU.

**SDK (Software Development Kit)**: Viam provides an SDK to help you write client applications,and create custom implementations of viam-server to support custom components.

* One per language.
* Can be used as a server for a custom component implementation.
    * Hosts a gRPC server implementing the Viam Robot API.
    * That serves functionality for all registered resources.
* Can be used as a client.
    * To connect to a robot implementing the Viam Robot API.
* Effectively, non-golang versions of RDK’s resource authoring and activation functionality.

**Service**: Services are on-device software for complex capabilities such as SLAM, Computer Vision, Motion Planning, and Data Collection. Services are resources that represent elements of software that typically work with components; for example, navigation, base remote control, or metadata service.

**Viam Robot API**:

* The de facto description of how all resources can be communicated with.
* The RDKs/SDKs implement this server side.
* The RDKs/SDKs use this to act as clients.
* Currently expressed as a collection of Protocol Buffer files.
* Does not mandate gRPC as the transport mechanism.
    * However, all RDKs/SDKs written by Viam use gRPC.

## Other important non-Viam terminology

**Gantry**: A robot that only uses linear motion to carry out a task; for example, the scaffolding of a 3D printer, which moves the print head around on motorized linear rails.

**gRPC**: Google Remote Procedure Call.
An open source universal RPC system initially developed at Google in 2015.
This framework can run in any environment and efficiently connect services across data centers.

**Protocol Buffers (Protobuf)**: A free and open-source, language-neutral, cross-platform data format for serializing structured data.
It is useful in developing programs to communicate with each other over a network or for storing data.

**SLAM**: Simultaneous localization and mapping.
An algorithm that allows a robot to navigate around a space creating or updating a map of the layout as it goes.

**Web Sockets**: A computer communications protocol that provides full-duplex communication channels over a single Transmission Control Protocol (TCP) connection.

**WebRTC**: An open source project which provides applications with real-time communication (RTC) via application programming interfaces (API) allowing powerful voice and video integration.