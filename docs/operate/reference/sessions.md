---
title: "Session Management with Viam's Client SDKs"
linkTitle: "Session Management"
weight: 70
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
  - /build/program/apis/sessions/
date: "2022-01-01"
no_list: true
# updated: ""  # When the content was last entirely checked
---

When you connect to a machine using an SDK, the SDK connects to the machine's `viam-server` instance as a _client_.
The period of time during which a client is connected to a machine is called a _session_.

_Session management_ is a safety precaution that allows you to manage the clients that are authenticated and communicating with a machine's `viam-server` instance.
The default session management configuration checks for presence to ensures that a machine only moves when a client is actively connected and stops any components that remain running when a client disconnects.
This is especially important for machines that physically move.
For example, imagine a wheeled rover gets a [`SetPower()`](/dev/reference/apis/components/base/#setpower) command as the last input from a client before the connection to the machine is interrupted.
Without session management, the API request from the client would cause the rover's motors to move, causing the machine to continue driving forever and potentially colliding with objects and people.

For more information, see [Client Sessions and Machine Network Connectivity](/dev/reference/sdks/connectivity/).

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

## Manage sessions with the session management API

The [Session Management API](https://pkg.go.dev/go.viam.com/rdk/session) is not currently provided in the Python or TypeScript SDKs.
Use the Go Client SDK instead.

{{< alert title="Tip" color="tip" >}}
If you are looking to implement session management yourself only to increase the session window, you can increase the session window instead, by [increasing the `heartbeat_window`](/configure/#network).
{{< /alert >}}

To manage your session with the session management API:

1. [Disable default session management](#disable-default-session-management)
1. [Use the session management API to manually manage sessions](#use-the-session-management-api-to-manually-manage-sessions)

### Disable default session management

The `SessionsClient` that serves the session management API is automatically enabled on your machine.
It is instantiated as part of your [`RobotClient`](/dev/reference/apis/robot/) instance (client of the Machine API).
If you want to disable it, you can pass the option to your machine, as demonstrated in the following code snippets:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
async def main():
    opts = RobotClient.Options(disable_sessions=True)
    await RobotClient.at_address("my-machine-address", opts)
    robot = await connect()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.Options.disable_sessions).

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
robot, err := client.New(
  ctx, "my-machine-address",
  logger,
  client.WithDisableSessions(),
  ...)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot/client#WithDisableSessions)

{{% /tab %}}
{{% tab name="TypeScript" %}}

```ts {class="line-numbers linkable-line-numbers"}
const robot = await VIAM.createRobotClient({
  // ...
  disableSessions: true,
  // ...
});
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/interfaces/DialWebRTCConf.html).

{{% /tab %}}
{{% /tabs %}}

This option allows you to have full control over sessions management.
After disabling the client, you must now manage each of your sessions manually with the session management API.
You can do this with Viam's client SDKs.

### Use the session management API to manually manage sessions

Use your [`RobotClient()`](/dev/reference/apis/robot/) instance to access the [`SessionsClient`](https://pkg.go.dev/go.viam.com/rdk/session) within your client SDK program.
This is a [gRPC](https://grpc.io/) client that `viam-server` instantiates at robot runtime.
Then, define your own [`SessionsClient`](https://github.com/viamrobotics/rdk/blob/main/robot/client/client.go).
