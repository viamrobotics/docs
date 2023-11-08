---
title: "Client Sessions and Robot Network Connectivity"
linkTitle: "Network Connectivity Issues"
weight: 20
type: "docs"
description: "When a robot loses its connection to a LAN or WAN, all client sessions will timeout and end by default."
tags:
  ["client", "sdk", "viam-server", "networking", "apis", "robot api", "session"]
---

When connecting to a robot using the connection code from the [code sample tab](/program/#hello-world-the-code-sample-tab), a [client session](/program/apis/sessions/) automatically uses the most efficient route to connect to your robot either through local LAN or WAN or the internet.

When a robot loses its connection to the internet but is still connected to a LAN or WAN:

- Client sessions connected through the same LAN or WAN will function normally.
- Client sessions connected through the internet will timeout and end.
  If the client is on the same LAN or WAN but the route it chose to connect is through the internet, the client will automatically disconnect and then reconnect over LAN.
- [Cloud Sync](/services/data/#cloud-sync) for Data Management will pause until the internet connection is re-established since the robot will be unable to connect to the [Viam app](https://app.viam.com).

When a robot loses its connection to LAN or WAN, all client sessions will timeout and end by default.

## Client session timeout and end

When your client cannot connect to your robot's `viam-server` instance, `viam-server` will end any current client [_sessions_](/program/apis/sessions/) on this robot and all client operations will [timeout automatically](/program/apis/sessions/#heartbeats) and halt: any active commands will be cancelled, stopping any moving parts, and no new commands will be able to reach the robot until the connection is restored.

To disable the default behavior and manage resource timeout and reconfiguration over a networking session yourself, you can [disable the default behavior](/program/apis/sessions/#disable-default-session-management) of session management, then use [Viam's SDKs](/program/) in your code to make calls to [the session management API](https://pkg.go.dev/go.viam.com/rdk/session#hdr-API).

## Configure a connection timeout

When connecting to a smart machine using the [robot API](/program/apis/robot/) from a supported [Viam SDK](/program/apis/), you can configure an [optional timeout](docs/program/apis/robot/#configure-a-timeout) to account for intermittent or delayed network connectivity.
