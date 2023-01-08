---
title: "Robot Development Kit"
linkTitle: "Robot Development Kit"
weight: 99
type: "docs"
description: "An overview of Viam's Robot Development Kit (RDK)."
tags: ["server", "rdk"]
---

Make sure to understand the [Viam high-level overview first](../../getting-started/high-level-overview/).

Viam's RDK is the open-source, on-robot portion of the Viam platform, that provides _viam-server_ and the Go SDK.

## viam-server

_viam-server_ is responsible for:

- All gRPC and WebRTC communication
- Connecting robots to the cloud
- Loading and managing connections to hardware [components](../../components/)
- Running built-in [services](../../services/)
- Managing configured processes
- Connecting to other parts of your robot

## Go SDK

The RDK provides the Go SDK.

[Examples](https://github.com/viamrobotics/rdk/tree/main/examples)

## Open-source

<https://github.com/viamrobotics/rdk>
