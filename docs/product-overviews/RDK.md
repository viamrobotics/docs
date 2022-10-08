---
title: "Robot Development Kit"
linkTitle: "Robot Development Kit"
weight: 99
type: "docs"
description: "An overview of Viam's Robot Development Kit (RDK)."
---
## Coming soon!

This page will describe:

- What RDK consists of:
  - viam-server:
    - What it does
    - How it does
    - Where it lives and how to manage it
  - Golang SDK:
    - How to install it as a golang library
    - Explanation of SDK as client application vs SDK as server side implementation of hardware



Robot Development Kit (RDK) is the official Viam-developed codebase that provides all functionality of an SDK and more. It is written in Golang.

* The RDK contains: 
    * Go SDK
    * Various packages and libraries (Motion Planning, Controls, Frame System, SLAM)
    * gRPC Server Implementations (hardware drivers)

* It can be used to build viam-server:
    * Can parse and respond to changes in a remote robot configuration file.
    * With updates possibly provided by the Viam App ([https://app.viam.com](https://app.viam.com)).
    * Initializes resources from a config.
    * Hosts a gRPC server implementing the Viam Robot API.
    * That serves functionality for all registered resources.

* It can be used as a client to connect to another robot implementing the Viam Robot API.

* Contains different libraries:
    * Motion Planning, Frame System, SLAM, Controls
    * These are used to help implement components/services.
    * Note: Libraries are called “services” ONLY if we expose their functionality in our proto APIs.
