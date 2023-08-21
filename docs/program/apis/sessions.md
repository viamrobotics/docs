---
title: "Session Management with Viam's Client SDKs"
linkTitle: "Session Management API"
weight: 20
type: "docs"
description: "How to use the session management API with Viam's Client SDKs."
tags: ["client", "sdk", "viam-server", "networking", "apis", "robot api", "session", "sessions", "session management"]
---

The session management API provides support for robot session management.

A session:
- allows a client to express that it is actively connected or authenticated to `viam-server` on your robot
- supports stopping moving components when the connection is no longer active.

{{< alert title="Info" color="info" >}}

### Purpose of session management

When controlling a robot or fleet with Viam, you want a way to understand the presence of the clients that are communicating with and authenticated to each robot's `viam-server` through Viam's various [resource APIs](/program/apis/).

The presence of these clients at one point in time is called a *session*.
A session technically is any presence mechanism at the RDK application layer maintained by any client with `viam-server`.

Session management allows for safer operation of robots that physically move.
Specifically, without session management, controls that would be "sticky" (for example [`SetPower()` of a base](/components/base/#setpower)) based on the last input of a **client**, meaning the API request from the client sets the flow of electricity on a part of the robot and then does not time out, could lead to **having a robot trying to continue doing what it was told to do forever.**

You do not want that to happen.

#### Clients and Viam's client SDKs

*Client* has multiple meanings for a Viam robot.
Essentially, it's anything that is receiving the information served by `viam-server` running on the robot.

A **client** can be an SDK script controlling the robot, an input controller, or just the different resources on the robot talking amongst themselves.
For example, if you use Viam's module registry to [add modular resources to your robot](/extend/modular-resources/), the clients of your robot in its lifetime will include the "model servers" you instantiate on your robot for individual resources.

Viam's session management API is your built-in solution to this.
Your client maintains the session, telling the `viam-server` instance that it is still present every so often, or staying within the heartbeat window.

Your client must send at least one session heartbeat within this window.
As soon as the window lapses/expires, the server will safely stop all resources that are marked for safety monitoring that have been last used by that session, and no others; a lapsed client will attempt to establish a new session immediately prior to the next operation it performs.

{{< /alert >}}

## Usage

Usage of the session management API differs across [Viam's SDKS](/program/).

{{< tabs >}}
{{% tab name="Go" %}}

### On-Robot Session Management

To use the [Session Management API](https://pkg.go.dev/go.viam.com/rdk/session) the Go Client SDK provides, use your [`RobotClient`](/program/apis/#robot-api) instance (client of the Robot API) to instantiate a `SessionsManager` with `SessionManager()`.

### Sessions for RobotClients

First, use your [`RobotClient()`](/program/apis/#robot-api) instance to access the [`SessionsClient`](https://pkg.go.dev/go.viam.com/rdk/session) within your Go Client SDK program.
This is a [gRPC](https://grpc.io/) client that `viam-server` instantiates at robot runtime.
Find `SessionsClient` defined on [Github](https://github.com/viamrobotics/rdk/blob/main/robot/client/client.go).

{{% /tab %}}
{{% tab name="Python" %}}

### On-Robot Session Management

The `Session Management API` is not currently provided in the Python SDK.
Use the Go Client SDK instead.

### Sessions for RobotClients

First, use your [`RobotClient()`](/program/apis/#robot-api) instance to access the [`SessionsClient`](https://python.viam.dev/autoapi/viam/sessions_client/index.html#viam.sessions_client.SessionsClient) within your Python Client SDK program.
This is a [gRPC](https://grpc.io/) client that `viam-server` instantiates at robot runtime.
Find `SessionsClient` defined on [GitHub](https://github.com/viamrobotics/rdk/blob/main/robot/client/client.go).

{{% /tab %}}
{{% /tabs %}}

### Disable the sessions client

The `SessionsClient` is automatically enabled on your robot.
If you want to disable it to keep any additional clients from authenticating to your robot's session while running a control program with Viam's client SDKs, access your `SessionsClient` instance with the `disabled` parameter set to `True`, as shown in the following Python code snippet:

```python {class="line-numbers linkable-line-numbers"}
async def main():
    robot = await connect()
    sessions = SessionsClient.(channel: Channel, disabled: bool = True)
```
