---
title: "Session Connectivity: Network Disconnection during a Session"
linkTitle: "Network Disconnection"
weight: 20
type: "docs"
description: "How Viam handles losing connection to the internet during a robot session."
tags: ["client", "sdk", "viam-server", "networking", "apis", "robot api", "session"]
---

A guide to what happens when your robot loses its network connection during a session.

### How does `viam-server` work if you lose connectivity during a session?

If you lose connectivity, `viam-server` should stop this robot's session, therefore stopping the flow of power to all actuating resources.

To disable the default behavior here and manage resource timeout and reconfiguration over a networking session yourself, follow [these instructions](/program/apis/sessions/) to [disable the default behavior](/program/apis/sessions/#disable-default-session-management) of session management, then utilize [Viam's SDKs](/program/) to make calls to [the session management API](https://pkg.go.dev/go.viam.com/rdk/session#hdr-API).

### How do Viam's SDKs work if you lose connectivity during a session?

As a client of your robot, the Python or TypeScript SDKs will have their connection to the robot stopped when the robot loses connectivity, if the session is ended properly.
If you wish to implement your own client SDK, note that client implementation of session management is necessary to make this work.
The Go Client SDK is a little bit different: as the session management API is implemented through the Go Client, the session can be managed from within this client, allowing for more flexibility in timing disconnection.

### How will your robot's primary parts and sub parts work if you lose connectivity during a session?

Resources on the robot will no longer be connected and signaling to each other if you lose connectivity and the session is ended.
If opting to manage sessions yourself with the session management API, you must make sure the topographical hierachy of resources is respected when shutting down resources at session end.
This means that sub-parts signal their shutdown to the primary part, which then closes the connection to accessing clients like SDKs.
