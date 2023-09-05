---
title: "Client Sessions and Robot Network Connectivity"
linkTitle: "Network Disconnection"
weight: 20
type: "docs"
description: "How a Viam robot handles losing its connection to the internet."
tags: ["client", "sdk", "viam-server", "networking", "apis", "robot api", "session"]
---

What happens when your robot loses its connection to the internet over a LAN or WAN and can no longer communicate with clients through [the Viam app](https://app.viam.com).

## How does `viam-server` work if your robot loses its network connection?

If the robot loses its connection to the internet, `viam-server` will timeout and end any current client [*sessions*](/program/apis/sessions/) on this robot.

## How do `viam-server`'s clients work if your robot loses its network connection?

If your robot running `viam-server` is no longer connected to the internet and each client session is ended, all operations will timeout automatically and operations will be halted.
When its session times out, each client is asked to cancel any ongoing operations by the automatically-configured `SessionsClient` of your robot.
Any active commands will be cancelled, stopping any moving parts, and no new commands will be able to reach the robot until the connection is restored.

### How do Viam's client SDKs work if your robot loses its network connection?

As a client of your robot, Viam's SDKs will by default have their session ended when the robot loses its connection to the internet.

To disable the default behavior here and manage resource timeout and reconfiguration over a networking session yourself, follow [these instructions](/program/apis/sessions/).
[Disable the default behavior](/program/apis/sessions/#disable-default-session-management) of session management, then utilize [Viam's SDKs](/program/) in your code to make calls to [the session management API](https://pkg.go.dev/go.viam.com/rdk/session#hdr-API).
