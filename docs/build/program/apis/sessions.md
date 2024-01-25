---
title: "Session Management with Viam's Client SDKs"
linkTitle: "Session Management"
weight: 20
type: "docs"
description: "Manage sessions between your machine and clients connected through Viam's SDKs."
tags:
  [
    "client",
    "sdk",
    "viam-server",
    "networking",
    "apis",
    "robot api",
    "session",
    "sessions",
    "session management",
  ]
aliases:
  - /program/apis/sessions/
---

When you connect to a machine using an SDK, the SDK connects to the machine's `viam-server` instance as a _client_.
The period of time during which a client is connected to a machine is called a _session_.

_Session management_ is a safety precaution that allows you to manage the clients that are authenticated and communicating with a machine's `viam-server` instance.
The default session management configuration checks for presence to ensures that a machine only moves when a client is actively connected and stops any components that remain running when a client disconnects.
This is especially important for machines that physically move.
For example, imagine a wheeled rover gets a [`SetPower()`](/components/base/#setpower) command as the last input from a client before the connection to the machine is interrupted.
Without session management, the API request from the client would cause the rover's motors to move, causing the machine to continue driving forever and potentially colliding with objects and people.

For more information, see [Client Sessions and Machine Network Connectivity](/build/program/connectivity/).

If you want to manage operations differently, you can manage your machine's client sessions yourself.
The Session Management API provides functionality for:

- clients to notify to the machine that the client is actively authenticated and connected
- the machine to stop moving components when a session ends

### The `SessionsClient`

A _client_ of a Viam machine can be a program using an SDK to control the machine, or all the different resources on the machine, including all {{< glossary_tooltip term_id="part" text="parts" >}} and sub-parts, like an input controller and a base, communicating.

For example, if you use Viam's module registry to add {{< glossary_tooltip term_id="modular-resource" text="modular resources" >}} to your machine, the clients of your machine will include the model servers you instantiate on your machine for individual resources, as well as the SDKs you are using to program the modular resources.

Viam's session management API's `SessionsClient` is a built-in solution that manages the connection between your machine's clients and your machine.
If you connect to your machine using one of Viam's SDKs, the resulting client will automatically maintain the session by sending a _heartbeat_ notifying the machine's `viam-server` instance of its continued presence.
The `SessionsClient` on the machine maintains an overview of all sessions based on the clients' heartbeat messages.

If the machine does not receive a signal from the client in the expected interval, the machine ends the session and stop all resources that are marked for safety monitoring and have been last used by that session.
That means if a client sends a command to a machine to move the motors and then loses the connection, the machine will stop moving.

{{< alert title="Caution" color="caution" >}}
If a resource was used by client A and then by client B, and client A disconnects, the resource will not be stopped, regardless of possibly ongoing commands initiated by client A.
{{< /alert >}}

A disconnected client will attempt to establish a new session immediately prior to the next operation it performs.

#### Heartbeats

A _heartbeat_ is a signal that indicates machine connectivity.
Essentially, heartbeats are a client's way of letting a machine know that they are still connected.

Heartbeats are sent automatically from Viam's SDKs unless you disable them with the session management API or session management is not implemented by the server in question.
Heartbeats are automatically sent at an interval that is one fifth of the heartbeat window.
For example, if the heartbeat window is 5 seconds, clients will each send a heartbeat every 1 second.

You can adjust the heartbeat window in the configuration of your machine:

{{< tabs >}}
{{% tab name="Builder UI" %}}

On your **Auth/Network** tab, set the **Heartbeat Window**:

![Heartbeat window configuration screen](/build/program/sessions/heartbeatwindow.png)

{{% /tab %}}
{{% tab name="JSON" %}}

Add the following `heartbeat_window` configuration to your `network.sessions` object:

```json
  ... // components {...}, services {...},
  "network": {
    "sessions": {
      "heartbeat_window": "30s" // Changes heartbeat window to 30 seconds
    }
  },
  ...
```

{{% /tab %}}
{{< /tabs >}}

{{< alert title="Note" color="note" >}}
You must restart your machine for the new `heartbeat_window` to take effect.
{{< /alert >}}

The default heartbeat window is 2 seconds if this configuration is omitted.

If you manually manage sessions, each client must send at least one heartbeat within the window you set.

## Manage sessions with the session management API

The [Session Management API](https://pkg.go.dev/go.viam.com/rdk/session) is not currently provided in the Python or TypeScript SDKs.
Use the Go Client SDK instead.

{{< alert title="Tip" color="tip" >}}
If you are looking to implement session management yourself only to increase the session window, you can increase the session window instead, by [increasing the `heartbeat_window`](#heartbeats).
{{< /alert >}}

To manage your session with the session management API:

1. [Disable the default session management](#disable-default-session-management)
1. [Use the session management API to manually manage sessions](#use-the-session-management-api-to-manually-manage-sessions)

### Disable default session management

The `SessionsClient` that serves the session management API is automatically enabled on your machine.
It is instantiated as part of your [`RobotClient`](/build/program/apis/#robot-api) instance (client of the Robot API).
If you want to disable it, you can pass the option to your machine, as demonstrated in the following code snippets:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
async def main():
    opts = RobotClient.Options(disable_sessions=True)
    await RobotClient.at_address("my-machine-address", opts)
    robot = await connect()
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
robot, err := client.New(ctx, "my-machine-address", logger, client.WithDisableSessions(), ...)
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

```ts {class="line-numbers linkable-line-numbers"}
const robot = await VIAM.createRobotClient({
  // ...
  disableSessions: true,
  // ...
});
```

{{% /tab %}}
{{% /tabs %}}

This option allows you to have full control over sessions management.
After disabling the client, you must now manage each of your sessions manually with the session management API.
You can do this with Viam's [client SDKs](https://pkg.go.dev/go.viam.com/rdk/session).

### Use the session management API to manually manage sessions

Use your [`RobotClient()`](/build/program/apis/#robot-api) instance to access the [`SessionsClient`](https://pkg.go.dev/go.viam.com/rdk/session) within your client SDK program.
This is a [gRPC](https://grpc.io/) client that `viam-server` instantiates at robot runtime.
Then, define your own [`SessionsClient`](https://github.com/viamrobotics/rdk/blob/main/robot/client/client.go).
