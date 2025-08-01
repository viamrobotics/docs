---
title: "Base Remote Control Service"
linkTitle: "Base Remote Control"
weight: 70
type: "docs"
description: "The base remote control service allows you to remotely control a base with an input controller like a gamepad."
tags: ["base", "services", "rover", "input controller", "remote control"]
icon: true
images: ["/services/icons/base-rc.svg"]
aliases:
  - "/services/base-rc/"
  - "/mobility/base-rc/"
no_service: true
date: "2022-01-01"
# updated: ""  # When the content was last entirely checked
# SME: Eric
---

The base remote control service implements an [input controller](/operate/reference/components/input-controller/) as a remote control for a [base](/operate/reference/components/base/).
This uses the [`input` API](/operate/reference/components/input-controller/#api) to make it easy to add remote drive controls for your rover or other mobile robot with a controller like a gamepad.

Add the base remote control service after configuring your machine with a base and input controller to control the linear and angular velocity of the base with the controller's button or joystick controls.

Control mode is determined by the configuration attribute `"control_mode"`, for which there are five options:

1. `"arrowControl"`: Arrow buttons control speed and angle
2. `"triggerSpeedControl"`: Trigger button controls speed and joystick controls angle
3. `"buttonControl"`: Four buttons (usually X, Y, A, B) control speed and angle
4. `"joystickControl"`: One joystick controls speed and angle
5. `"droneControl"`: Two joysticks control speed and angle

You can monitor the input from these controls in the **CONTROL** tab.

## Used with

{{< cards >}}
{{< relatedcard link="/operate/reference/components/base/" required="yes" >}}
{{< relatedcard link="/operate/reference/components/input-controller/" required="yes" >}}
{{< relatedcard link="/operate/reference/components/movement-sensor/" >}}
{{< /cards >}}

{{% snippet "required-legend.md" %}}

## Configuration

You must configure a [base](/operate/reference/components/base/) with a [movement sensor](/operate/reference/components/movement-sensor/) as part of your machine to be able to use a base remote control service.

First, make sure your base is physically assembled and powered on.
Then, configure the service:

{{< tabs >}}
{{% tab name="Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page.
Click the **+** icon next to your machine part in the left-hand menu and select **Component or service**.
Select the `base remote control` type.
Enter a name or use the suggested name for your service and click **Create**.

In your base remote control service's configuration panel, copy and paste the following JSON object into the attributes field:

```json {class="line-numbers linkable-line-numbers"}
{
  "base": "<your-base-name>",
  "input_controller": "<your-controller-name>"
}
```

Edit the attributes as applicable to your machine, according to the table below.

For example:

![An example configuration for a base remote control service.](/services/base-rc/base-rc-ui-config.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-base-remote-control-service>",
  "api": "rdk:service:base_remote_control",
  "model": "rdk:builtin:builtin",
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
  "name": "gamepad_service",
  "api": "rdk:service:base_remote_control",
  "model": "rdk:builtin:builtin",
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
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `base` | string | **Required** | The `name` of the [base](/operate/reference/components/base/) you have configured for the base you are operating with this service. |
| `input_controller` | string | **Required** | The `name` of the [input controller](/operate/reference/components/input-controller/) you have configured for the base you are operating with this service. |
| `control_mode` | string | Optional | The mode of remote control you want to use. <br> Options: <ul><li>`"arrowControl"`</li><li>`"triggerSpeedControl"`</li><li>`"buttonControl"`</li><li>`"joystickControl"`</li> <li>`"droneControl"`</li></ul> <br> Default: `"arrowControl"` |
| `max_angular_degs_per_sec` | float | Optional | The max angular velocity for the [base](/operate/reference/components/base/) in degrees per second. |
| `max_linear_mm_per_sec` | float | Optional | The max linear velocity for the [base](/operate/reference/components/base/) in meters per second. |

## API

The base remote control service supports the following methods:

{{< readfile "/static/include/services/apis/generated/base_remote_control-table.md" >}}

{{% alert title="Tip" color="tip" %}}

The following code examples assume that you have a machine configured with a [base](/operate/reference/components/base/) named `"my_base"`, [input controller](/operate/reference/components/input-controller/) named `"my_controller"`, and base remote control service named `"my_base_rc_service"`.
Make sure to add the required code to connect to your machine and import any required packages at the top of your code file.
Go to your machine's **CONNECT** tab and select the **Code sample** page for sample code to connect to your machine.

{{% /alert %}}

{{< readfile "/static/include/services/apis/generated/base_remote_control.md" >}}
