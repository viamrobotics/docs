---
title: Viam Glossary
summary: Glossary of Viam terminology
authors:
    - Matt Dannenberg
date: 2022-04-08
---
# Glossary
Robot: The configuration and entry point for a components and computer coupled into one logical unit

Robot Part: A single viam-server process belonging to a robot. e.g. one robot composed of two parts,  a jetson and a pi. Usually 1-to-1 with a CPU.

RDK (Robot Development Kit):

* The official Viam developed codebase that provides all functionality of an SDK and more. (golang)

* The RDK contains: 

* * Go SDK

* * Various Packages (Motion Planning, Controls, Frame System, SLAM)

* * gRPC Interfaces (protobuf files)

* * gRPC Server Implementations (hardware drivers)

* Can be used as a Server

* * Can parse and respond to changes in a remote robot configuration file
 
* * With updates possibly provided by app.viam.com

* * Initializes resources from a config

* * Hosts a gRPC server implementing the Viam Robot API

* * That serves functionality for all registered resources.

* Can be used as a Client

* * To connect to another robot implementing the Viam Robot API

* Contains different libraries

* * Motion Planning, SLAM, Controls

* * Note: Libraries are called “services” ONLY if we expose their functionality in our proto APIs. 

* * Used to help implement components/services.

SDK (Software Development Kit):

* Will be one per language

* Can be used as a server for a custom component implementation

* * Hosts a gRPC server implementing the Viam Robot API

* * That serves functionality for all registered resources.

* Can be used as a Client

* * To connect to a robot implementing the Viam Robot API

* Effectively, non-golang versions of RDK’s resource authoring and activation functionality.

Viam Robot API:

* The de facto description of how all resources can be communicated with.

* The RDKs/SDKs implement this server side.

* The RDKs/SDKs use this to act as clients.

* Currently expressed as a collection of Protocol Buffer files

* Does not mandate gRPC as the transport mechanism

* * However, all RDKs/SDKs written by Viam use gRPC

Resource: an individual, addressable element of a robot (RDK definition).

* Currently split into two types of resources: components and services

Component: a resource that represents an element of hardware in a robot (RDK definition). e.g. servo, camera, arm, etc.

Service: a resource that represents an element of software that typically works with components. e.g. navigation, base remote control, metadata service.

Process: A bespoke, OS specific process managed by the RDK to either run once or indefinitely. e.g. run one of Viam's camera servers.

Resource Config: The configuration element of either a component or a service. Typically expressed in JSON.

Robot Config: The complete configuration of a single robot part. Typically expressed in JSON.

Model: A particular implementation of a component type. e.g. ur5e is a model of an arm.

Attribute: a configuration parameter of a resource specific to a model.

Remote: a robot part which is controlled by another robot part.

Base: a physical, moving component to which other components are typically mounted.

Board: an IO board connected to a robot park used to express low-level electronics functionality like GPIO, SPI, I2C, etc.. e.g. Jetson, Pi, Numato, Arduino, 

Boards like Jetson and Pi run the RDK and can expose the board component itself.

Frame System: A hierarchy of frames that are related to one another via coordinate transformations.

Frame: A single element of a Frame System, it is a coordinate system that is used to describe position and orientation. The location of a frame is described in relation to its parent frame using rigid transformations rather than in absolute terms.

Fragment: a reusable config block typically representing a common resource. Ex, viam_gripper

Available across an organization and when used in a config, gets merged (key/value wise) with a specific robot part.

Remote UI: Uses the Web JS SDK and provides UI elements to control a robot via WebRTC.

## Other important non-VIAM terminology
gRPC: 

WebRTC: 

Protocol Buffers: 

SLAM: Simultaneous Location And Mapping. An algorithm that allows a robot to navigate around a space creating a map of the layout as it goes.

Gantry: a robot that only uses linear motion to carry out a task. (eg, the scaffolding of a 3D printer, which moves the print head around) see also: motorized linear rail.
