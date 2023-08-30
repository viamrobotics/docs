---
title: "Session Connectivity: Network Disconnection during a Session"
linkTitle: "Network Disconnection"
weight: 20
type: "docs"
description: "How Viam handles losing connection to the internet during a robot session."
tags: ["client", "sdk", "viam-server", "networking", "apis", "robot api", "session"]
---

What happens when your robot loses its connection to the internet and can no longer talk to the Viam cloud through [the Viam app](https://app.viam.com).

### How does `viam-server` work if you lose connectivity during a session?

If you lose connectivity, `viam-server` will by default timeout all resource and end this robot's [*session*](/program/apis/sessions/). 
This does not immediately stop the flow of power to all actuating resources, but it signals that the robot can no longer receive operations over the internet, so any further operations will not be performed.

This is because the robot cannot access Viam's APIs, including the robot API, without a connection to the cloud.

To disable the default behavior here and manage resource timeout and reconfiguration over a networking session yourself, follow [these instructions](/program/apis/sessions/) to [disable the default behavior](/program/apis/sessions/#disable-default-session-management) of session management, then utilize [Viam's SDKs](/program/) in your code to make calls to [the session management API](https://pkg.go.dev/go.viam.com/rdk/session#hdr-API).
If you do this, and configure the primary and sub-parts of your robot to cache all tokens so that authentication to Viam's cloud is not required for operation-related communication over the local network or directly through `viam-server`, you can operate your robot consistently without the need for a network connection.
However, the low-network approach is not recommended if you want to utilize any of Viam's [services](/services/), like the vision service, motion planning, or the frame system.

### How do Viam's SDKs work if you lose connectivity during a session?

As a client of your robot, the Python or TypeScript SDKs will have their connection to the Viam cloud and Viam app stopped when the robot loses its internet connection, if the session is ended properly.
The Go Client SDK is a little bit different: as the session management API is implemented through the Go Client, the session can be managed from within this client, allowing for more flexibility in timing disconnection.
Follow [these instructions](/program/apis/sessions/#use-the-session-management-api-to-manually-manage-sessions) to enable this manual session management.

### How will your robot's primary parts and sub parts work if you lose connectivity during a session?

Resources on the robot will still be connected and signaling to each other if your robot running `viam-server` is no longer connected to the internet and the session is ended, but they will not be connected to the Viam cloud and Viam app.
If opting to manage sessions yourself with the session management API, you must make sure the topographical hierachy of resources is respected when shutting down resources at session end.
This means that sub-parts signal their shutdown to the primary part, which then closes the connection to accessing clients like SDKs.
