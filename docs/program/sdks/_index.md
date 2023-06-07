---
title: "Interact with Resources with Viam's SDKs"
linkTitle: "SDK API Libraries"
weight: 20
type: "docs"
description: "Access and control your robot or fleet with the resource and robot APIs."
icon: "/services/img/icons/sdk.svg"
tags: ["client", "sdk", "viam-server", "networking"]
---

Every Viam {{< glossary_tooltip term_id="resource" text="resource" >}} exposes an [Application Programming Interface (API)](https://en.wikipedia.org/wiki/API) described through [protocol buffers](https://developers.google.com/protocol-buffers).
This can be understood as a description of how you can interact with that resource.
Different models of resources implement the same API, which [Viam SDKs expose](/internals/robot-to-robot-comms/), allowing you to control different models of resource types with a consistent interface.

The API methods provided by the SDKs for each of these resource APIs wrap gRPC client requests to the robot when you execute your program, interacting with the resources you configured on your robot.
