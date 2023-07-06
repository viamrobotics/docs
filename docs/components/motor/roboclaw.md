---
title: "Configure a DC brushed motor driven by a roboclaw motor controller"
linkTitle: "28byj48"
weight: 22
type: "docs"
description: "Configure a DC brushed motor driven by a roboclaw motor controller."
images: ["/components/img/components/motor.svg"]
# SMEs: Olivia, Rand
---

The `roboclaw` model of the motor component supports small unipolar [stepper motors](https://en.wikipedia.org/wiki/Stepper_motor) controlled by stepper motor drivers like [ULN2003](https://www.ti.com/product/ULN2003A). The `28byj48` is often used for low-current and low-precision applications and supports full, half, and quarter stepping with 2048 steps in a rotation in full-step mode.

To configure a `28byj48` motor as a component of your robot, first configure the [board](/components/board/) to which the motor driver is wired.
Then, add the motor:

{{< tabs name="gpiostepper-config">}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your motor, select the type `motor`, and select the `28byj48` model.

Click **Create component**.

![A 28byj48 motor config.](../../img/motor/28byj48-config-ui.png)

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json
{
  "components": [
    {
      "name": "<your-board-name>",
      "type": "board",
      "model": "<your-board-model>",
      "attributes": {},
      "depends_on": [],
    },
    {
      "name": "<your-motor-name>",
      "type": "motor",
      "model": "28byj48",
      "attributes": {
        "board": "<your-board-name>",
        "pins": {
          "in1": "<pin-number>",
          "in2": "<pin-number>",
          "in3": "<pin-number>",
          "in4": "<pin-number>"
        },
        "ticks_per_rotation": <int>
      },
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

Example configuration for a `28byj48` stepper motor:

```json
{
  "components": [
    {
      "name": "example-board",
      "type": "board",
      "model": "pi"
    },
    {
      "name": "example-motor",
      "type": "motor",
      "model": "28byj48",
      "attributes": {
        "board": "example-board",
        "pins": {
          "in1": "16",
          "in2": "18",
          "in3": "29",
          "in4": "22"
        },
        "ticks_per_rotation": 200
      }
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `roboclaw` motors:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `serial` | string | **Required** |  |
| `serial_baud_rate` | int | **Required** |  |
| `motor_channel` | int | **Required** |  |
| `address` | int | Optional |  |
| `ticks_per_rotation` | int | Optional |  |

Refer to your motor and motor driver data sheets for specifics.
