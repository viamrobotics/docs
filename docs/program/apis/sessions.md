---
title: "Sessions Management with Viam's Client SDKs"
linkTitle: "Session Management API"
weight: 20
type: "docs"
description: "How to use the Sessions Management API with Viam's Client SDKs."
tags: ["client", "sdk", "viam-server", "networking", "apis", "robot api", "session", "sessions", "session management"]
---

The Session Management API provides support for robot session management.

A Session allows a client to express that it is actively connected and
supports stopping actuating components when it's not.

{{< alert title="Info" color="info" >}}

### Purpose

When working with robots, we want a protocol and system-wide means to be able to understand the presence of a client connected to a robot.

This provides for safer operation scenarios when dealing with actuating controls. S

pecifically, without this, controls that would be "sticky" (e.g. SetPower of a base) based on the last input of a client, can have a robot try to continue what it was told to do forever.

These clients range from SDK scripts, input controllers, and robots talking amongst themselves.

Part of the solution to this is session management.
A session, as defined here, is a presence mechanism at the application layer (i.e. RDK, not TCP) maintained by a client (e.g. SDK) with a server (e.g. RDK).

The client maintains the session, telling the server it is still present every so often, or staying within the heartbeat window.

The client must send at least one session heartbeat within this window.
As soon as the window lapses/expires, the server will safely stop all resources that are marked for safety monitoring that have been last used by that session, and no others; a lapsed client will attempt to establish a new session immediately prior to the next operation it performs.

{{< /alert >}}

Python SDK: [Sessions Client](https://python.viam.dev/autoapi/viam/sessions_client/index.html#viam.sessions_client.SessionsClient)

- To interact with the Robot API with the Python SDK, instantiate a `SessionsClient` ([gRPC](https://grpc.io/) client) and use that class for all interactions.

Go Client SDK: [Session Management API](https://pkg.go.dev/go.viam.com/rdk@v0.5.0/session)

First, use your [`RobotClient()`](/program/apis/#robot-api) instance to initialize a `SessionsClient()`.

SessionsClient provides a client for the [Sessions Management API](https://github.com/viamrobotics/rdk/blob/main/robot/client/client.go), which is the `viam-server` built-in solution for controlling session management on your robot.

Next: what are sessions?

- some updates to RobotClient methods.
- maybe just put them here?

### Initialize the Sessions Client

(initialized along with a robot client automaticially anyways, the option to disable is there https://github.com/viamrobotics/viam-python-sdk/blob/79c7c85b11a73b753f5cd9cbbf787dd07fd9eb50/src/viam/robot/client.py#L46)

```python {class="line-numbers linkable-line-numbers"}
async def main():
    robot = await connect()
    sessions = SessionsClient.(channel: Channel, disabled: bool = False)
```
