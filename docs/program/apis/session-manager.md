---
title: "Session Management with Viam's Client SDKs"
linkTitle: "Session Management API"
weight: 20
type: "docs"
description: "How to use the session management API with Viam's Client SDKs."
tags: ["client", "sdk", "viam-server", "networking", "apis", "robot api", "session", "sessions", "session management"]
---

When controlling a robot or fleet with Viam, you want a way to understand the presence of the clients that are communicating with and authenticated to each robot's `viam-server`.
The period of time during which these clients are present is called a *session.*
Sessions each have [their own API](/program/apis/session/), which is a client of both `viam-server` and the [session management API](/program/apis/sessions).

Session management:

- allows a client to express that it is actively connected or authenticated to `viam-server` on your robot
- supports stopping moving components when the connection is no longer active.

*Session management* is a presence mechanism between a client and `viam-server`.
Session management allows for safer operation of robots that physically move.
For example, imagine a wheeled rover gets a [`SetPower()`](/components/base/#setpower) command as the last input from a client before the connection to the robot is interrupted.
Without session management, the API request from the client sets the flow of electricity to the motors of the robot and then does not time out, causing the robot to continue driving forever, colliding with objects and people.

With default configuration, sessions are automatically managed for you with Viam's session management API's default `SessionsClient`.
If you want to manage sessions yourself, use Viam's session management API.

### What is a `SessionsClient`

A Viam robot has many clients because a client is anything that is receiving the information served by `viam-server` running on the robot, which includes the primary part, sub-parts, client SDKs, and more.
A *client* of a Viam robot could be an SDK script controlling the robot, an input controller, or just the different resources on the robot talking amongst themselves.
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

This option allows you to have full control over session management.
After disabling the client, you must now manage each of your sessions manually with the session management API.
You can do this with Viam's [client SDKs](https://pkg.go.dev/go.viam.com/rdk/session).

## API

The `SessionManager` API supports the following methods:

{{< readfile "/static/include/program/apis/session-management.md" >}}

### Start

Create a new session that expects at least one heartbeat within the configured window.

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `heartbeatWindow` [(string)](https://pkg.go.dev/time#Duration): The heartbeat window you want this `SessionManager` to follow for this session. The window is the elapsed time between two instants as an [int64](https://pkg.go.dev/builtin#int64) nanosecond count. The representation limits the largest representable duration to approximately 290 years

**Returns:**

- [(*Session)](https://pkg.go.dev/go.viam.com/rdk/robot#SessionManager): A new session.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#SessionManager.Start).

``` go
newSession, err := mySessionManager.Start(context.Background(), nil)
```

### All

Get all sessions that are actively being held by this `SessionManager`.

**Parameters:**

- None

**Returns:**

- [([]*Session)](https://pkg.go.dev/go.viam.com/rdk@v0.8.0/session#Session): All active sessions associated with this `SessionManager`.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#SessionManager.All).

``` go
sessions := mySessionManager.All(context.Background(), nil)
```

### FindByID

Find a session by the given ID.
If found, trigger a heartbeat, extending the lifetime of the session.

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `id` [(uuid.UUID)](https://pkg.go.dev/github.com/google/uuid#UUID): The client's UUID associated with this session.
- `ownerID` [(string)](https://pkg.go.dev/builtin#string): The client's ownerID associated with this session.
If ownerID is in use but the session in question has a different owner, this is a security violation and Viam reports back that no session is found.

**Returns:**

- [(*Session)](https://pkg.go.dev/go.viam.com/rdk@v0.8.0/session#Session): A new manager for holding sessions.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#SessionManager.Start).

``` go
newSession, err := mySessionManager.Start(context.Background(), uuid, ownerID)
```

### AssociateResource

Associate a session ID to a monitored resource so that when a session expires:

- If a resource is currently associated with that ID based on the order of AssociateResource calls, then it will have its resource stopped.
- If id is `uuid.Nil`, this has no effect other than disassociation with a session. Be sure to include any remote information in the name.

**Parameters:**

- `id` [(uuid.UUID)](https://pkg.go.dev/github.com/google/uuid#UUID): The client's UUID associated with this session.
- `resourceName` [(resource.Name)](https://pkg.go.dev/go.viam.com/rdk/resource#Name): The `name` you have configured for this resource on your robot.

**Returns:**

- None

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#SessionManager.AssociateResource).

``` go
newSession, err := mySessionManager.AssociateResource(uuid.Nil, "my_base")
```

### Close

Stop the session manager without directing any sessions to expire.

**Parameters:**

- None

**Returns:**

- None

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk@v0.8.0/robot#SessionManager.Start).

``` go
mySessionManager.Close()
```
