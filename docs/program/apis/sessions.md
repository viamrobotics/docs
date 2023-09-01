---
title: "Session Management"
linkTitle: "Session Management"
weight: 20
type: "docs"
description: "Manage sessions between your robot and clients connected through Viam's SDKs."
tags: ["client", "sdk", "viam-server", "networking", "apis", "robot api", "session", "sessions", "session management"]
---

When you connect to a robot using an SDK, the SDK connects to the robot's `viam-server` instance as a _client_.
The period of time during which a client is connected to a robot is called a *session*.

*Session management* is a presence mechanism that allows you to manage the clients that are authenticated and communicating with a robot's `viam-server` instance.

As a safety precaution, the default Session management configuration ensures that a robot only moves when a client is actively connected.
This is especially important for robots that physically move.
For example, imagine a wheeled rover gets a [`SetPower()`](/components/base/#setpower) command as the last input from a client before the connection to the robot is interrupted.
Without session management, the API request from the client would cause the rover's motors to move, causing the robot to continue driving forever and potentially colliding with objects and people.

If you need to different functionality, you can manage sessions yourself.
The Session Management API provides functionality for

- clients to notify to the robot that the client is actively authenticated and connected
- the robot to stop moving components when a session ends

### The `SessionsClient`

A *client* of a Viam robot can be an SDK script controlling the robot, an input controller, or just the different resources on the robot talking amongst themselves.
A Viam robot generally has many clients because a client is anything that is receiving the information served by `viam-server`, which includes the primary {{< glossary_tooltip term_id="part" text="part" >}}, sub-parts, client SDKs, and more.

For example, if you use Viam's module registry to [add modular resources to your robot](/extend/modular-resources/), the clients of your robot will include the "model servers" you instantiate on your robot for individual resources.

Viam's session management API's `SessionsClient` is a built-in solution that manages the connection between your robot's clients and your robot.
With the `SessionsClient`, if the robot does not receive a signal from the client at regular intervals, it safely stops until the connection is reestablished.
Your client of the session management API maintains the session, telling the `viam-server` instance that it is still present every so often; in other words, staying within the *heartbeat* window.

#### Heartbeats

A *heartbeat* is a signal that indicates robot connectivity.
Essentially, "heartbeats" are a Viam robot's way of letting a user reading data from it know the different parts of it are "alive."

Heartbeats are sent automatically from Viam's Go, Python, and TypeScript client SDKs unless you disable this with the session management API, or session management is not implemented by the server in question.
Heartbeats are automatically sent at an interval that is one fifth of the heartbeat window.
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

### Access the session management API

To manage sessions on-robot manually, you can use the following client SDKs:

{{< tabs >}}
{{% tab name="Go" %}}

To enable the [Session Management API](https://pkg.go.dev/go.viam.com/rdk/session) the Go Client SDK provides, [disable the default behavior of sessions](#disable-default-session-management).

{{% /tab %}}
{{% tab name="Other SDKs" %}}

The session management API is not currently provided in the Python or TypeScript SDKs.
Use the Go Client SDK instead.

{{% /tab %}}
{{% /tabs %}}

### Use the session management API to manually manage sessions

First, use your [`RobotClient()`](/program/apis/#robot-api) instance to access the [`SessionsClient`](https://pkg.go.dev/go.viam.com/rdk/session) within your client SDK program.
This is a [gRPC](https://grpc.io/) client that `viam-server` instantiates at robot runtime.
Find `SessionsClient` defined on [GitHub](https://github.com/viamrobotics/rdk/blob/main/robot/client/client.go).

### Disable default session management

The `SessionsClient` that serves the session management API is automatically enabled on your robot.
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
After disabling the client, you must now manage each of your sessions manually with the session management API.
You can do this with Viam's [client SDKs](https://pkg.go.dev/go.viam.com/rdk/session).
