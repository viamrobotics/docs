---
title: "Client Sessions and Machine Network Connectivity"
linkTitle: "Network Connectivity Issues"
weight: 80
type: "docs"
description: "When a machine loses its connection to a LAN or WAN, all client sessions will timeout and end by default."
tags:
  ["client", "sdk", "viam-server", "networking", "apis", "robot api", "session"]
aliases:
  - /program/connectivity/
  - /sdks/connectivity/
date: "2022-01-01"
# updated: ""  # When the content was last entirely checked
---

When connecting to a machine using the connection code from the [**CONNECT** tab](/dev/reference/sdks/), a [client session](/dev/reference/apis/sessions/) automatically uses the most efficient route to connect to your machine either through local LAN or WAN or the internet.

When a machine loses its connection to the internet but is still connected to a LAN or WAN:

- Client sessions connected through the same LAN or WAN will function normally.
- Client sessions connected through the internet will timeout and end.
  If the client is on the same LAN or WAN but the route it chose to connect is through the internet, the client will automatically disconnect and then reconnect over LAN.
- Cloud sync for the [data management service](/data-ai/capture-data/capture-sync/) will pause until the internet connection is re-established since the machine will be unable to connect to the [Viam app](https://app.viam.com).

When a machine loses its connection to LAN or WAN, all client sessions will timeout and end by default.

## Client session timeout and end

When your client cannot connect to your machine's `viam-server` instance, `viam-server` will end any current client [_sessions_](/dev/reference/apis/sessions/) on this machine and all client operations will [timeout automatically](/dev/reference/apis/sessions/) and halt: any active commands will be cancelled, stopping any moving parts, and no new commands will be able to reach the machine until the connection is restored.

To disable the default behavior and manage resource timeout and reconfiguration over a networking session yourself, you can [disable the default behavior](/dev/reference/apis/sessions/#disable-default-session-management) of session management, then use [Viam's SDKs](/dev/reference/sdks/) in your code to make calls to [the session management API](https://pkg.go.dev/go.viam.com/rdk/session#hdr-API).

## Configure a connection timeout

When connecting to a machine using the [robot API](/dev/reference/apis/robot/) from a supported [Viam SDK](/dev/reference/apis/), you can configure an [optional timeout](/dev/reference/apis/robot/#configure-a-timeout) to account for intermittent or delayed network connectivity.
