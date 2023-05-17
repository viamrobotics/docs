---
title: "Interact with Resources with Viam's SDKs"
linkTitle: "Add Control Logic"
weight: 50
type: "docs"
description: "Access and control your robot or fleet with the resource and robot APIs."
icon: "/services/img/icons/sdk.svg"
tags: ["client", "sdk"]
---

Every Viam {{< glossary_tooltip term_id="resource" text="resource" >}} exposes an [Application Programming Interface (API)](https://en.wikipedia.org/wiki/API).
This can be understood as a description of how you can interact with that resource.
Each API is described through [protocol buffers](https://developers.google.com/protocol-buffers).
Viam SDKs [expose these APIs](/internals/robot-to-robot-comms/).

Each Viam resource's API is uniquely namespaced as a colon-delimited-triplet in the form of `namespace:type:subtype`.

For example:

- The API of built-in component [camera](/components/camera) is `rdk:component:camera`, which exposes methods such as `GetImage()`.
- The API of built-in service [vision](/services/vision) is `rdk:service:vision`, which exposes methods such as `GetDetectionsFromCamera()`.

{{% alert title="Note" color="note" %}}
You can see built-in Viam resource APIs in the [Viam GitHub](https://github.com/viamrobotics/api).
{{% /alert %}}

A *model* describes a specific implementation of a resource that implements (speaks) its API.
Models allow you to control different versions of resource types with a consistent interface.

For example:

Some DC motors use just [GPIO](/components/board), while other DC motors use serial protocols like [SPI bus](/components/board/#spis).
Regardless, you can power any motor model that implements the *rdk:component:motor* API with the `SetPower()` method.

Models are also uniquely namespaced as colon-delimited-triplets in the form of `namespace:family:name`.

For example:

- The `rdk:builtin:gpio` model of the `rdk:component:motor` API provides RDK support for [GPIO-controlled DC motors](/components/motor/gpio/).
- The `rdk:builtin:DMC4000` model of the same `rdk:component:motor` API provides RDK support for the [DMC4000](/components/motor/dmc4000/) motor.

TODO: Talk about how these methods work --> providing wrapper for gRPC client request to these endpoints, which are how you access/interface with the components you have configured on your robot/`viam-server`.
