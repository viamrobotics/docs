---
title: "Base Remote Control Service"
linkTitle: "Base Remote Control"
weight: 60
type: "docs"
description: "The base remote control service allows you to remotely control a base with an input controller like a gamepad."
tags: ["base", "services", "rover", "input controller", "remote control"]
icon: "/services/icons/base-rc.svg"
images: ["/services/icons/base-rc.svg"]
aliases:
  - "/services/base-rc/"
# SME: Eric
---

The base remote control service implements an [input controller](/components/input-controller/) as a remote control for a [base](/components/base/).
This uses the [`input` api](/components/input-controller/#api) to make it easy to add remote drive controls for your rover or other mobile robot with a controller like a gamepad.

Add the base remote control service after configuring your machine with a base and input controller to control the linear and angular velocity of the base with the controller's button or joystick controls.

Control mode is determined by the configuration attribute `"mode"`, for which there are five options:

1. `"arrowControl"`: Arrow buttons control speed and angle
2. `"triggerSpeedControl"`: Trigger button controls speed and joystick controls angle
3. `"buttonControl"`: Four buttons (usually X, Y, A, B) control speed and angle
4. `"joyStickControl"`: One joystick controls speed and angle
5. `"droneControl"`: Two joysticks control speed and angle

You can monitor the input from these controls in the **Control** tab of the [Viam app](https://app.viam.com).

## Used with

{{< cards >}}
{{< relatedcard link="/components/base/" required="yes" >}}
{{< relatedcard link="/components/input-controller/" required="yes" >}}
{{< relatedcard link="/components/movement-sensor/" >}}
{{< /cards >}}

{{% snippet "required-legend.md" %}}

## Configuration

You must configure a [base](/components/base/) with a [movement sensor](/components/movement-sensor/) as part of your machine to be able to use a base remote control service.

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **Services** subtab, then click **Create service** in the lower-left corner.
Select the type `Base Remote Control`.
Enter a name for your service, then click **Create**.

![An example configuration for a base remote control service in the Viam app Config Builder.](/mobility/base-rc/base-rc-ui-config.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-base-remote-control-service>",
  "type": "base_remote_control",
  "attributes": {
    "base": "<your-base-name>",
    "input_controller": "<your-controller-name>"
  }
}
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "my-base-remote-control-service",
  "type": "base_remote_control",
  "attributes": {
    "base": "my-base",
    "input_controller": "my-input-controller",
    "control_mode": "arrowControl"
  }
}
```

{{% /tab %}}
{{< /tabs >}}

Edit and fill in the attributes as applicable.
The following attributes are available for base remote control services:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `base` | string | **Required** | The `name` of the [base](/components/base/) you have configured for the base you are operating with this service. |
| `input_controller` | string | **Required** | The `name` of the [input controller](/components/input-controller/) you have configured for the base you are operating with this service. |
| `control_mode` | string | Optional | The mode of remote control you want to use. <br> Options: <ul><li>`"arrowControl"`</li><li>`"triggerSpeedControl"`</li><li>`"buttonControl"`</li><li>`"joyStickControl"`</li> <li>`"droneControl"`</li></ul> <br> Default: `"arrowControl"` |
| `max_angular_degs_per_sec` | float | Optional | The max angular velocity for the [base](/components/base/) in degrees per second. |
| `max_linear_mm_per_sec` | float | Optional | The max linear velocity for the [base](/components/base/) in meters per second. |

## API

The base remote control service supports the following methods:

{{< readfile "/static/include/services/apis/base-rc.md" >}}

{{% alert title="Tip" color="tip" %}}

The following code examples assume that you have a machine configured with a [base](/components/base/) named `"my_base"`, [input controller](/components/input-controller/) named `"my_controller"`, and base remote control service named `"my_base_rc_service"`.
Make sure to add the required code to connect to your machine and import any required packages at the top of your code file.
Go to your machine's **Code sample** tab on the [Viam app](https://app.viam.com) for boilerplate code to connect to your machine.

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
baseRCService, err := baseremotecontrol.FromRobot(robot, "my_base_rc_service")

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

- [([]Control)](https://python.viam.dev/autoapi/viam/components/input/index.html#viam.components.input.Control): A list of inputs from the controller that are being monitored for that control mode..

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/baseremotecontrol).

```go {class="line-numbers linkable-line-numbers"}
baseRCService, err := baseremotecontrol.FromRobot(robot, "my_base_rc_service")

// Get the list of inputs from the controller that are being monitored for that control mode.
inputs := baseRCService.ControllerInputs()
```

{{% /tab %}}
{{< /tabs >}}
