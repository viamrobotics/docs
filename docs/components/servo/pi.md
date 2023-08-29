---
title: "Configure a pi Servo"
linkTitle: "pi"
weight: 90
type: "docs"
description: "Configure a pi servo to integrate a hobby servo controlled by GPIO pins on a Raspberry Pi board."
tags: ["servo", "components"]
icon: "/icons/components/servo.svg"
# SME: Rand
---

{{% alert title="Info" color="info" %}}

Unlike other servo models, `pi` servos are implemented as part of the [`pi` board component](https://github.com/viamrobotics/rdk/blob/main/components/board/pi/impl/servo.go).

{{% /alert %}}

Configure a `pi` servo to integrate a hobby servo controlled by general-purpose input/output (GPIO) pins on a [Raspberry Pi board](/components/board/pi/) into your robot:

{{< tabs name="Configure a pi Servo" >}}
{{% tab name="Config Builder" %}}

Navigate to the **config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your servo, select the type `servo`, and select the `pi` model.

Click **Create component**:

{{< imgproc src="/components/servo/pi-servo-ui-config.png" alt="An example configuration for a pi servo in the Viam app Config Builder." resize="600x" >}}

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
    "components": [
        {
            "name": "<your-servo-name>",
            "type": "servo",
            "model": "pi",
            "attributes": {
                "pin": "<your-pin-number>",
                "board": "<your-board-name>"
            }
        },
        ... // insert your board component config
    }
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
        "name": "local",
        "type": "board",
        "model": "pi"
    },
    {
        "name": "my_servo",
        "type": "servo",
        "model": "pi",
        "attributes": {
            "pin": "16",
            "board": "local"
        }
    }
  ]
}
```

{{% /tab %}}
{{% tab name="Annotated JSON" %}}

![A servo JSON config with explanatory annotations for each attribute.](/components/servo/servo-json.png)

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `pi` servos:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `pin` | string | **Required** | The {{< glossary_tooltip term_id="pin-number" text="pin number" >}} of the pin the servo's control wire is wired to on the [board](/components/board/). |
| `board` | string | **Required** | `name` of the [board](/components/board/) the servo is wired to. |
| `min` | float | Optional | The minimum angle in degrees that the servo can reach. <br> Default = `0.0` <br> Range = [`0.0`, `180.0`] |
| `max` | float | Optional | The maximum angle in degrees that the servo can reach. <br> Default = `180.0` <br> Range = [`0.0`, `180.0`] |
| `starting_position_degs` | float | Optional | Starting position of the servo in degrees. <br> Default = `0.0` <br> Range = [`0.0`, `180.0`] |
| `hold_position` | boolean | Optional | If `false`, power down a servo if it has tried and failed to go to a position for a duration of 500 milliseconds. <br> Default = `true` |
| `max_rotation_deg` | int | Optional | The maximum angle the servo can rotate. Must be in between `min` and `max`. <br> Default = `180` |

{{% alert title="Tip" color="tip" %}}

Refer to your servo's data sheet for [pulse-width modulation (PWM)](https://docs.arduino.cc/learn/microcontrollers/analog-output), rotation, and wiring specifications.

{{% /alert %}}

{{< readfile "/static/include/components/servo-control.md" >}}


