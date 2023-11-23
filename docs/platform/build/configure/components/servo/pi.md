---
title: "Configure a pi Servo"
linkTitle: "pi"
weight: 90
type: "docs"
description: "Configure a pi servo to integrate a hobby servo controlled by GPIO pins on a Raspberry Pi board."
tags: ["servo", "components"]
icon: "/icons/components/servo.svg"
aliases:
  - "/components/servo/pi/"
# SME: Rand
---

{{% alert title="Info" color="info" %}}

Unlike other servo models, `pi` servos are implemented as part of the [`pi` board component](https://github.com/viamrobotics/rdk/blob/main/components/board/pi/impl/servo.go).

{{% /alert %}}

Configure a `pi` servo to integrate a hobby servo controlled by general-purpose input/output (GPIO) pins on a [Raspberry Pi board](/platform/build/configure/components/board/pi/) into your robot:

{{< tabs name="Configure a pi Servo" >}}
{{% tab name="Config Builder" %}}

Navigate to the **config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `servo` type, then select the `pi` model.
Enter a name for your servo and click **Create**.

{{< imgproc src="/platform/build/configure/components/servo/pi-servo-ui-config.png" alt="An example configuration for a pi servo in the Viam app Config Builder." resize="600x" >}}

Copy and paste the following attribute template into your servo's **Attributes** box.
Then remove and fill in the attributes as applicable to your servo, according to the table below.

{{< tabs >}}
{{% tab name="Attributes template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "pin": "<your-pin-number>",
  "board": "<your-board-name>",
  "min": <float>,
  "max": <float>,
  "starting_position_deg": <float>,
  "hold_position": <int>,
  "max_rotation_deg": <int>
}
```

{{% /tab %}}
{{% tab name="Attributes example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "pin": "16",
  "board": "local"
}
```

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-servo-name>",
      "model": "pi",
      "type": "servo",
      "namespace": "rdk",
      "attributes": {
        "pin": "<your-pin-number>",
        "board": "<your-board-name>",
        "min": <float>,
        "max": <float>,
        "starting_position_deg": <float>,
        "hold_position": <int>,
        "max_rotation_deg": <int>
      }
    }
  }
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "local",
      "model": "pi",
      "type": "board",
      "namespace": "rdk"
    },
    {
      "name": "my_servo",
      "model": "pi",
      "type": "servo",
      "namespace": "rdk",
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

![A servo JSON config with explanatory annotations for each attribute.](/platform/build/configure/components/servo/servo-json.png)

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `pi` servos:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `pin` | string | **Required** | The {{< glossary_tooltip term_id="pin-number" text="pin number" >}} of the pin the servo's control wire is wired to on the [board](/platform/build/configure/components/board/). |
| `board` | string | **Required** | `name` of the [board](/platform/build/configure/components/board/) the servo is wired to. |
| `min` | float | Optional | Sets a software limit on the minimum angle in degrees your servo can rotate to. <br> Default = `0.0` <br> Range = [`0.0`, `180.0`] |
| `max` | float | Optional | Sets a software limit on the maximum angle in degrees your servo can rotate to. <br> Default = `180.0` <br> Range = [`0.0`, `180.0`] |
| `starting_position_degs` | float | Optional | Starting position of the servo in degrees. <br> Default = `0.0` <br> Range = [`0.0`, `180.0`] |
| `hold_position` | boolean | Optional | If `false`, power down a servo if it has tried and failed to go to a position for a duration of 500 milliseconds. <br> Default = `true` |
| `max_rotation_deg` | int | Optional | The maximum angle that you know your servo can possibly rotate to, according to its hardware. Refer to your servo's data sheet for clarification. Must be greater than or equal to the value you set for `max`. <br> Default = `180` |

{{% alert title="Tip" color="tip" %}}

Refer to your servo's data sheet for [pulse-width modulation (PWM)](https://docs.arduino.cc/learn/microcontrollers/analog-output), rotation, and wiring specifications.

{{% /alert %}}

{{< readfile "/static/include/components/test-control/servo-control.md" >}}
