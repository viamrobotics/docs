---
title: "Session Connectivity: Network Disconnection during a Session"
linkTitle: "Network Disconnection"
weight: 20
type: "docs"
description: "How Viam handles losing connection to the internet during a robot session."
tags: ["client", "sdk", "viam-server", "networking", "apis", "robot api", "session"]
---

What happens when your robot loses its connection to the internet over a LAN or WAN and can no longer communicate through [the Viam app](https://app.viam.com).

### How does `viam-server` work if your robot loses connectivity during a session?

If the robot loses connectivity, `viam-server` will timeout and end any current client [*sessions*](/program/apis/sessions/) on this robot.
When its session times out, each client is asked to cancel any ongoing operations by the automatically-configured `SessionsClient` of your robot. 
Any active commands will be cancelled, stopping any moving parts, and no new commands will be able to reach the robot until the connection is restored.


### How will your robot's primary parts and sub parts work if you lose connectivity during a session?

Resources on the robot will still be able to send operations requests to each other if your robot running `viam-server` is no longer connected to the internet and the session is ended, but if your session has been ended, all operations will timeout automatically under the management of the `SessionsClient`.

### How do Viam's client SDKs work if your robot loses connectivity during a session?

As a client of your robot, Viam's SDKs will by default have their session ended when the robot loses its connection to the internet.

To disable the default behavior here and manage resource timeout and reconfiguration over a networking session yourself, follow [these instructions](/program/apis/sessions/).
[Disable the default behavior](/program/apis/sessions/#disable-default-session-management) of session management, then utilize [Viam's SDKs](/program/) in your code to make calls to [the session management API](https://pkg.go.dev/go.viam.com/rdk/session#hdr-API).

