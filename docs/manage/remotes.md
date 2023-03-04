---
title: "Remotes and Sub-Parts"
linkTitle: "Remotes and Sub-Parts"
weight: 40
type: "docs"
description: "Connect robots to each other."
tags: ["server", "components", "services"]
---

Sometimes you want robots to communicate with each other.
You can do this by establishing a secure connection called a *remote*.
Example use cases include:

- Two rovers mapping a room with SLAM.
  If they can communicate, they can coordinate to divide the work efficiently and avoid crashing into one another.
- A swarm of drones with limited onboard computing power.
  They send images to a computer with significant computing power that runs machine learning code, and sends requests back to the drones based on the data.

Remotes are established using direct [gRPC](https://grpc.io/), or gRPC through [WebRTC](https://webrtc.org/).

Once you configure a remote, the main robot can access all the components and services configured on the remote robot as though they are part of the main robot.

## Parts and Sub-Parts

Robots are organized into *parts*, where each part represents a computer (a single-board computer like a Rapsberry Pi or a desktop, laptop, or other computer), the hardware [components](/components/) attached to it, and any [services](/services/) or other resources running on it.

You can make a multi-part robot by first configuring one part (which we'll call the "main" part), and then configuring one or more sub-parts.

![The Viam app interface with the part drop-down open. A new part called "my-sub-part" is being created.](../img/remotes/sub-part-config.png)
