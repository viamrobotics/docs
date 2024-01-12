---
title: "Client Sessions and Machine Network Connectivity"
linkTitle: "Network Connectivity Issues"
weight: 20
type: "docs"
description: "When a machine loses its connection to a LAN or WAN, all client sessions will timeout and end by default."
tags:
  ["client", "sdk", "viam-server", "networking", "apis", "robot api", "session"]
aliases:
  - /program/connectivity/
---

When connecting to a machine using the connection code from the [code sample tab](/build/program/#hello-world-the-code-sample-tab), a [client session](/build/program/apis/sessions/) automatically uses the most efficient route to connect to your machine either through local LAN or WAN or the internet.

When a machine loses its connection to the internet but is still connected to a LAN or WAN:

- Client sessions connected through the same LAN or WAN will function normally.
- Client sessions connected through the internet will timeout and end.
  If the client is on the same LAN or WAN but the route it chose to connect is through the internet, the client will automatically disconnect and then reconnect over LAN.
- [Cloud Sync](/data/cloud-sync/) for Data Management will pause until the internet connection is re-established since the machine will be unable to connect to the [Viam app](https://app.viam.com).

When a machine loses its connection to LAN or WAN, all client sessions will timeout and end by default.

## Client session timeout and end

When your client cannot connect to your machine's `viam-server` instance, `viam-server` will end any current client [_sessions_](/build/program/apis/sessions/) on this machine and all client operations will [timeout automatically](/build/program/apis/sessions/#heartbeats) and halt: any active commands will be cancelled, stopping any moving parts, and no new commands will be able to reach the machine until the connection is restored.

To disable the default behavior and manage resource timeout and reconfiguration over a networking session yourself, you can [disable the default behavior](/build/program/apis/sessions/#disable-default-session-management) of session management, then use [Viam's SDKs](/build/program/) in your code to make calls to [the session management API](https://pkg.go.dev/go.viam.com/rdk/session#hdr-API).

## Configure a connection timeout

When connecting to a machine using the [robot API](/build/program/apis/robot/) from a supported [Viam SDK](/build/program/apis/), you can configure an [optional timeout](/build/program/apis/robot/#configure-a-timeout) to account for intermittent or delayed network connectivity.
