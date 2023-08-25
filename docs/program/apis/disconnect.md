---
title: "Session Connectivity Resource Disonnection during a Session"
linkTitle: "Session Connectivity"
weight: 20
type: "docs"
description: "How to troubleshoot a resource losing connection during a robot session."
tags: ["client", "sdk", "viam-server", "networking", "apis", "robot api", "session"]
---

A session:

- allows a client to express that it is actively connected or authenticated to `viam-server` on your robot
- supports stopping moving components when the connection is no longer active.

### how does viam-server work if you lose connectivity during a session?

If you lose connectivity, `viam-server` should stop this robot's session, therefore stopping the flow of power to all actuating resources.

### how does the sdk work if you lose connectivity during a session?

As a client of your robot, the Python or TypeScript SDKs will have their connection to the robot stopped when the robot loses connectivity, if the session is ended properly.
Client implementation is necessary to make this work.

### how the primary parts and sub parts work if you lose connectivity during a session?

Resources on the robot will no longer be connected and signaling to each other if you lose connectivity and the session is ended.
If opting to manage sessions yourself with the session management API, you must make sure the topographical hierachy of resources is respected when shutting down resources at session end.
This means that sub-parts signal their shutdown to the primary part, which then closes the connection to accessing clients like SDKs.
