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

### Purpose of session management

When controlling a robot or fleet with Viam, you want a way to understand the presence of the clients that are communicating with and authenticated to each robot's `viam-server`.

The period of time during which these clients are present is called a *session*.
*Session management* is a presence mechanism between a client and `viam-server`.

Session management allows for safer operation of robots that physically move.
For example, imagine a wheeled rover gets a [`SetPower()`](/components/base/#setpower) command as the last input from a client before the connection to the robot is interrupted.
Without session management, the API request from the client sets the flow of electricity to the motors of the robot and then does not time out, causing the robot to continue driving forever, colliding with objects and people.

With session management, if the robot does not receive a signal from the client at regular intervals, it safely stops until the connection is reestablished.

#### Clients and Viam's client SDKs

*Client* has multiple meanings for a Viam robot.
Essentially, it's anything that is receiving the information served by `viam-server` running on the robot.

A **client** can be an SDK script controlling the robot, an input controller, or just the different resources on the robot talking amongst themselves.
For example, if you use Viam's module registry to [add modular resources to your robot](/extend/modular-resources/), the clients of your robot in its lifetime will include the "model servers" you instantiate on your robot for individual resources.

Viam's session management API is your built-in solution to manage this.
Your client maintains the session, telling the `viam-server` instance that it is still present every so often, or staying within the **heartbeat** window.

#### Heartbeats

A **heartbeat** is a signal that indicates robot connectivity.
Essentially, "heartbeats" are a Viam robot's way of letting a user reading data from it know the different parts of it are "alive."

Heartbeats are sent automatically from Viam's Go, Python, and TypeScript client SDKs unless you disable this with the session management API, or session management is not implemented by the server in question.

As of now, heartbeats are sent at an interval that is one fifth of the heartbeat window.
For example, if the heartbeat window is 5 seconds, clients will each send a heartbeat every 1 second.

You can adjust the heartbeat window through the configuration of your robot.
To do so, add Raw JSON to the configuration of your robot in this format:

``` json
  ... // components {...}, services {...}, 
  "network": {
    "sessions": {
      "heartbeat_window": "30s" // Changes heartbeat window to 30 seconds 
    }
  },
  ...
```

The default heartbeat window is 2 seconds if this configuration is omitted.

If you choose to use the session management API to manage sessions, your client must send at least one session heartbeat within the window you set.
As soon as your window lapses or expires, the server will safely stop all resources that are marked for safety monitoring that have been last used by that session, and no others.
A lapsed client will attempt to establish a new session immediately prior to the next operation it performs.

## Usage

Usage of the session management API differs across [Viam's SDKS](/program/).

### Manage on-robot sessions

{{< tabs >}}
{{% tab name="Go" %}}

To enable the [Session Management API](https://pkg.go.dev/go.viam.com/rdk/session) the Go Client SDK provides, disable the default behavior of sessions.

### Sessions for RobotClients

Use your [`RobotClient()`](/program/apis/#robot-api) instance to access the [`SessionsClient`](https://pkg.go.dev/go.viam.com/rdk/session) within your Go Client SDK program.
This is a [gRPC](https://grpc.io/) client that `viam-server` instantiates at robot runtime.
Find `SessionsClient` defined on [Github](https://github.com/viamrobotics/rdk/blob/main/robot/client/client.go).

{{% /tab %}}
{{% tab name="Python" %}}

### On-Robot Session Management

The session management API is not currently provided in the Python SDK.
Use the Go Client SDK instead.

### Manage sessions for robot clients

First, use your [`RobotClient()`](/program/apis/#robot-api) instance to access the [`SessionsClient`](https://python.viam.dev/autoapi/viam/sessions_client/index.html#viam.sessions_client.SessionsClient) within your Python Client SDK program.
This is a [gRPC](https://grpc.io/) client that `viam-server` instantiates at robot runtime.
Find `SessionsClient` defined on [GitHub](https://github.com/viamrobotics/rdk/blob/main/robot/client/client.go).

{{% /tab %}}
{{% /tabs %}}

### Disable the sessions client

The `SessionsClient` is automatically enabled on your robot.
It is instantiated as part of your [`RobotClient`](/program/apis/#robot-api) instance (client of the Robot API).
If you want to disable it to keep any additional clients from authenticating to your robot's session while running a control program with Viam's client SDKs, you can pass the option to your robot, as demonstrated in the following code snippets:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
async def main():
    opts = RobotClient.Options(disable_sessions=True, ...)
    await RobotClient.at_address("my-robot-address", opts)
    robot = await connect()
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
robot, err := client.New(ctx, "my-robot-address", logger, client.WithDisableSessions(), ...)
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

```ts {class="line-numbers linkable-line-numbers"}
const robot = await VIAM.createRobotClient({
// ...
disableSessions: true
// ...
});
```

{{% /tab %}}

{{% /tabs %}}

This option allows you to have full control over sessions management.
After disabling the client, you must now manage each of your sessions manually with the session management API through the Go client SDK.
