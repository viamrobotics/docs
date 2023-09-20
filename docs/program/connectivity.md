---
title: "Client Sessions and Robot Network Connectivity"
linkTitle: "Network Connectivity Issues"
weight: 20
type: "docs"
description: "When a robot loses its connection to a LAN or WAN, all client sessions will timeout and end by default."
tags:
  ["client", "sdk", "viam-server", "networking", "apis", "robot api", "session"]
---

A [client session](/program/apis/sessions/) uses the most efficient route to connect to your robot either through local LAN or WAN or the internet.

When a robot loses its connection to the internet but is still connected to a LAN or WAN:

- Client sessions connected through the internet will timeout and end.
- Client sessions connected through the same LAN or WAN will function normally.
- [Cloud Sync](/services/data/#cloud-sync) for Data Management will pause until the internet connection is re-established since the robot will be unable to connect to the [Viam app](https://app.viam.com).

When a robot loses its connection to LAN or WAN, all client sessions will timeout and end by default.

## Client session timeout and end

When your client cannot connect to your robot's `viam-server` instance, `viam-server` will end any current client [_sessions_](/program/apis/sessions/) on this robot and all client operations will [timeout automatically](/program/apis/sessions/#heartbeats) and halt: any active commands will be cancelled, stopping any moving parts, and no new commands will be able to reach the robot until the connection is restored.

To disable the default behavior and manage resource timeout and reconfiguration over a networking session yourself, you can [disable the default behavior](/program/apis/sessions/#disable-default-session-management) of session management, then use [Viam's SDKs](/program/) in your code to make calls to [the session management API](https://pkg.go.dev/go.viam.com/rdk/session#hdr-API).
