---
title: "Base Remote Control Service"
linkTitle: "Base Remote Control"
weight: 80
type: "docs"
description: "The Base Remote Control Service implements remote control for a base."
tags: ["base", "services", "rover", "input controller", "remote control"]
# icon: "/services/img/icons/base-remote-control.svg"
# images: ["/services/img/icons/base-remote-control.svg"]
# SME: Eric
---

The Base Remote Control service implements an [input controller](/components/input-controller/) as a remote control for a [base](/components/base/).
This makes the process of coding remote drive controls for your rover or other mobile robot with a controller like a gamepad more simple.

Add the Base Remote Control service after configuring your robot with a base and input controller to monitor input from the controller in the **Control** tab of the [Viam app](https://app.viam.com).
Depending on how you configure the service, use either the button or joystick controls to control the linear and angular velocity of the base.

## API

The Base Remote Control service supports the following methods:

Method Name | Description
----------- | -----------
[`Close`](#close) | Close out of all remote control related systems.
[`ControllerInputs`](#controllerinputs) | Get a list of inputs from the controller that are being monitored for that control mode.

{{% alert title="Note" color="note" %}}

The following code examples assume that you have a robot configured with a [base](/components/base/) named `"my_base"` and an [input controller](/components/input-controller/) called `"my_controller"`, and that you add the required code to connect to your robot and import any required packages at the top of your code file.
Go to your robot's **Code sample** tab on the [Viam app](https://app.viam.com) for boilerplate code to connect to your robot.

{{% /alert %}}

### Close

Close out of all remote control related systems.

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/baseremotecontrol).

```go {class="line-numbers linkable-line-numbers"}
baseRCService, err := sensors.FromRobot(robot, "my_base_rc_service")

// Close out of all remote control related systems.
err := baseRCService.Close(context.Background())
```

{{% /tab %}}
{{< /tabs >}}

### ControllerInputs

Get a list of inputs from the controller that are being monitored for that control mode.

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- None

**Returns:**

- [([]Control)](https://python.viam.dev/autoapi/viam/components/input/index.html#viam.components.input.Control): Alist of inputs from the controller that are being monitored for that control mode..

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/baseremotecontrol).

```go {class="line-numbers linkable-line-numbers"}
baseRCService, err := sensors.FromRobot(robot, "my_base_rc_service")

// Get the list of inputs from the controller that are being monitored for that control mode.
inputs := baseRCService.ControllerInputs()
```

{{% /tab %}}
{{< /tabs >}}
