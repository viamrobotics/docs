---
title: "Session Connectivity: Network Disconnection during a Session"
linkTitle: "Network Disconnection"
weight: 20
type: "docs"
description: "How Viam handles losing connection to the internet during a robot session."
tags: ["client", "sdk", "viam-server", "networking", "apis", "robot api", "session"]
---

What happens when your robot loses its connection to the internet over a LAN or WAN and can no longer talk to the Viam cloud through [the Viam app](https://app.viam.com).

### How does `viam-server` work if your robot loses connectivity during a session?

If the robot loses connectivity, `viam-server` will timeout and end any client [*sessions*](/program/apis/sessions/) on this robot.
When a session times out, any active commands will be cancelled, stopping any moving parts, and no new commands will be able to reach the robot until the connection is restored.

To disable the default behavior here and manage resource timeout and reconfiguration over a networking session yourself, follow [these instructions](/program/apis/sessions/).
[Disable the default behavior](/program/apis/sessions/#disable-default-session-management) of session management, then utilize [Viam's SDKs](/program/) in your code to make calls to [the session management API](https://pkg.go.dev/go.viam.com/rdk/session#hdr-API).

### How do Viam's client SDKs work if your robot loses connectivity during a session?

As a client of your robot, the Python or TypeScript SDKs will have their connection to the Viam cloud and Viam app stopped when the robot loses its internet connection, if the session is ended properly.
The Go Client SDK is a little bit different: as the session management API is implemented through the Go Client, the session can be managed from within this client, allowing for more flexibility in timing disconnection.

Follow [these instructions](/program/apis/sessions/#use-the-session-management-api-to-manually-manage-sessions) to enable the manual session management.

### How will your robot's primary parts and sub parts work if you lose connectivity during a session?

Resources on the robot will still be connected and signaling to each other if your robot running `viam-server` is no longer connected to the internet and the session is ended, but they will not be connected to the Viam cloud and Viam app.

If opting to manage sessions yourself with the session management API, you must make sure the topographical hierachy of resources is respected when your robot signals to its clients that the session is over.
This means that the sub-parts of your robot should signal their shutdown to the primary part, which should then close the connection to any accessing clients like Viam's SDKs or modular resources.
