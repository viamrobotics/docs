---
title: "The Session API"
linkTitle: "Session API"
weight: 20
type: "docs"
description: "The session API offers resource safety monitoring and context attachment."
tags: ["client", "sdk", "viam-server", "networking", "apis", "robot api", "session", "sessions", "session management"]
---

When controlling a robot or fleet with Viam, you want a way to understand the presence of the clients that are communicating with and authenticated to each robot's `viam-server`.
The period of time during which these clients are present is called a *session*.

## API

The `Session` API supports the following methods:

{{< readfile "/static/include/program/apis/session.md" >}}

{{% alert title="Tip" color="tip" %}}

The following code examples assume that you have a robot configured with a [base component](/components/base/), and that you add the required code to connect to your robot and import any required packages, including the `sessions` package, at the top of your client file.
Go to your robot's **Code Sample** tab on the [Viam app](https://app.viam.com) for boilerplate code to connect to your robot.

{{% /alert %}}

### SafetyMonitor

Safety monitor this target {{< glossary_tooltip term_id="resource" text="resource" >}} so that, if it exists, if this session ends as the last session to monitor it, the `SessionManager` attempts to stop the resource by calling the `Stop()` method of the resource API.

Do not call this method from the resource being monitored itself, but instead from another client, like another resource, that controls the monitored resource on behalf of some request or routine.
For example, it would be appropriate for a remote [input controller](/components/input-controller/) resource to call a `SafetyMonitor()` on a base that it is remotely controlling the motion of.

In the context of a gRPC handled request, this function can only be called before the first response is sent back.
In the case of unary, it can only be called before the handler returns.

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `target` [(resource.Resource)](https://pkg.go.dev/go.viam.com/rdk/resource#Resource): The target resource.

**Returns:**

- None

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/session#SafetyMonitor).

```go
myBase, err := base.FromRobot(robot, "my_base")

// Signal to the session that the given target resource should be safety monitered.
session = session.SafetyMonitor(ctx, myBase)
```

### SafetyMonitorResourceName

Safety monitor this target {{< glossary_tooltip term_id="resource" text="resource" >}} so that, if it exists, if this session ends as the last session to monitor it, the `SessionManager` attempts to stop the resource by calling the `Stop()` method of the resource API.

Do not call this method from the resource being monitored itself, but instead from another client, like another resource, that controls the monitored resource on behalf of some request or routine.
For example, it would be appropriate for a remote [input controller](/components/input-controller/) resource to call a `SafetyMonitor()` on a base that it is remotely controlling the motion of.

In the context of a gRPC handled request, this function can only be called before the first response is sent back.
In the case of unary, it can only be called before the handler returns.

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `targetName` [(resource.Name)](https://pkg.go.dev/go.viam.com/rdk/resource#Name): The `name` you have set for the resource in configuration.

**Returns:**

- None

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/session#SafetyMonitorResourceName).

```go
myBase, err := base.FromRobot(robot, "my_base")

// Signal to the session that the given target resource should be safety monitered.
session = session.SafetyMonitor(ctx, "my_base")
```

### ToContext

Attach a session to the given context.

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `sess` [(*Session)](https://pkg.go.dev/go.viam.com/rdk/session#Session): The session object that you wish to attach to this context.

**Returns:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/session#ToContext).

```go
// Attach session "my session" to the given Context 
session = session.ToContext(context.Background(), my_session)
```
