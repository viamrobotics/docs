---
title: "Base Remote Control Service"
linkTitle: "Remote Control"
weight: 60
type: "docs"
description: "The Base Remote Control Service allows you to remotely control a base with an input controller like a gamepad."
tags: ["base", "services", "rover", "input controller", "remote control"]
icon: "/services/icons/base-rc.svg"
images: ["/services/icons/base-rc.svg"]
# SME: Eric
---

The Base Remote Control service implements an [input controller](/components/input-controller/) as a remote control for a [base](/components/base/).
This uses the [`input` api](/components/input-controller/#api) to make it easy to add remote drive controls for your rover or other mobile robot with a controller like a gamepad.

Add the Base Remote Control service after configuring your robot with a base and input controller to control the linear and angular velocity of the base with the controller's button or joystick controls.

Control mode is determined by the configuration attribute `"mode"`, for which there are five options:

1. `"arrowControl"`: Arrow buttons control speed and angle
2. `"triggerSpeedControl"`: Trigger button controls speed and joystick controls angle
3. `"buttonControl"`: Four buttons (usually X, Y, A, B) control speed and angle
4. `"joyStickControl"`: One joystick controls speed and angle
5. `"droneControl"`: Two joysticks control speed and angle

You can monitor the input from these controls in the **Control** tab of the [Viam app](https://app.viam.com).

## Configuration

You must configure a [base](/components/base/) with a [movement sensor](/components/movement-sensor/) as part of your robot to be able to use a Base Remote Control service.

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Services** subtab and navigate to the **Create service** menu.
Select the type `Navigation` and enter a name for your service.

Click **Create service**:

{{< imgproc src="/services/base-rc/base-rc-ui-config.png" alt="An example configuration for a Base Remote Control service in the Viam app Config Builder." resize="1000x" >}}

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

Next, add the JSON `"attributes"` you want the service to have.
The following attributes are available for Base Remote Control services:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `base` | string | **Required** | The `name` of the [base](/components/base/) you have configured for the base you are operating with this service. |
| `input_controller` | string | **Required** | The `name` of the [input controller](/components/input-controller/) you have configured for the base you are operating with this service. |
| `control_mode` | string | Optional | The mode of remote control you want to use. <br> Options: <ul><li>`"arrowControl"`</li><li>`"triggerSpeedControl"`</li><li>`"buttonControl"`</li><li>`"joyStickControl"`</li> <li>`"droneControl"`</li></ul> <br> Default: `"arrowControl"` |
| `max_angular_degs_per_sec` | float | Optional | The max angular velocity for the [base](/components/base/) in degrees per second. |
| `max_linear_mm_per_sec` | float | Optional | The max linear velocity for the [base](/components/base/) in meters per second. |

## API

The Base Remote Control Service supports the following methods:

Method Name | Description
----------- | -----------
[`Close`](#close) | Close out of all remote control related systems.
[`ControllerInputs`](#controllerinputs) | Get a list of inputs from the controller that is being monitored for that control mode.

{{% alert title="Tip" color="tip" %}}

The following code examples assume that you have a robot configured with a [base](/components/base/) named `"my_base"`, [input controller](/components/input-controller/) named `"my_controller"`, and Base Remote Control service named `"my_base_rc_service"`.
Make sure to add the required code to connect to your robot and import any required packages at the top of your code file.
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
