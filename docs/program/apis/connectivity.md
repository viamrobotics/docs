---
title: "Client Sessions and Robot Network Connectivity"
linkTitle: "Network Connectivity Issues"
weight: 20
type: "docs"
description: "Whan a robot loses its connection to the internet, all client sessions will timeout and end by default."
tags: ["client", "sdk", "viam-server", "networking", "apis", "robot api", "session"]
---

What happens when your robot loses its connection to the internet over a LAN or WAN and can no longer communicate with clients through [the Viam app](https://app.viam.com).

## How does `viam-server` work if your robot loses its network connection?

When a robot loses its connection over LAN or WAN, it can no longer communicate with clients through [the Viam app](https://app.viam.com).
`viam-server` will timeout and the `SessionsClient` will end any current client [*sessions*](/program/apis/sessions/) on this robot.

## What happens to clients connected to the robot when your robot loses its network connection?

When your client cannot connect to your robot's `viam-server` instance, all client operations will timeout automatically and halt.
Any active commands will be cancelled, stopping any moving parts, and no new commands will be able to reach the robot until the connection is restored.

### How do Viam's client SDKs work if your robot loses its network connection?

As a client of your robot, Viam's SDKs will by default have their session ended when the robot loses its connection to the internet.

To disable the default behavior here and manage resource timeout and reconfiguration over a networking session yourself, follow [these instructions](/program/apis/sessions/).
[Disable the default behavior](/program/apis/sessions/#disable-default-session-management) of session management, then utilize [Viam's SDKs](/program/) in your code to make calls to [the session management API](https://pkg.go.dev/go.viam.com/rdk/session#hdr-API).
