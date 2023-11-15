---
title: "Configure a gpio Servo"
linkTitle: "gpio"
weight: 90
type: "docs"
description: "Configure a gpio servo."
tags: ["servo", "components"]
icon: "/icons/components/servo.svg"
# SME: Gautham
---

Configure a `gpio` servo to integrate a hobby servo controlled by general-purpose input/output (GPIO) pins into your robot:

{{< tabs name="Configure a gpio Servo" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `servo` type, then select the `gpio` model.
Enter a name for your servo and click **Create**.

![An example configuration for a gpio servo in the Viam app Config Builder.](/components/servo/gpio-servo-ui-config.png)

Copy and paste the following attribute template into your servo's **Attributes** box.
Then remove and fill in the attributes as applicable to your servo, according to the table below.

{{< tabs >}}
{{% tab name="Attributes template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "pin": "<your-pin-number>",
  "board": "<your-board-name>",
  "frequency_hz": <int>,
  "min_angle_deg": <int>,
  "max_angle_deg": <int>,
  "min_period_us": <int>,
  "max_period_us": <int>,
  "pwm_resolution": <int>
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
      "model": "gpio",
      "type": "servo",
      "namespace": "rdk",
      "attributes": {
        "pin": "<your-pin-number>",
        "board": "<your-board-name>",
        "frequency_hz": <int>,
        "min_angle_deg": <int>,
        "max_angle_deg": <int>,
        "min_period_us": <int>,
        "max_period_us": <int>,
        "pwm_resolution": <int>
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
      "model": "esp32",
      "type": "board",
      "namespace": "rdk",
      "attributes": {
        "pins": [16]
      }
    },
    {
      "name": "my_servo",
      "model": "gpio",
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
{{< /tabs >}}

The following attributes are available for `gpio` servos:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `pin` | string | **Required** | The GPIO number of the pin the servo's control wire is wired to on the board. |
| `board` | string | **Required** | `name` of the [board](/micro-rdk/board/) the servo is wired to. |
| `frequency_hz` | int | Optional | The frequency of [PWM](https://docs.arduino.cc/learn/microcontrollers/analog-output) pulses sent to the servo, in Hertz (*Hz*). <br> Default = [`300`] <br> Range = [`0`, `450`] |
| `min_angle_deg` | int | Optional | The minimum angle in degrees that the servo can reach. <br> Default = `0` <br> Range = [`0`, `180`] |
| `max_angle_deg` | int | Optional | The maximum angle in degrees that the servo can reach. <br> Default = `180` <br> Range = [`0`, `180`] |
| `min_period_us` | int | Optional | Override the safe minimum [PWM](https://docs.arduino.cc/learn/microcontrollers/analog-output) pulse width in microseconds. <br> Default: `500` |
| `max_period_us` | int | Optional | Override the safe maximum [PWM](https://docs.arduino.cc/learn/microcontrollers/analog-output) pulse width in microseconds. <br> Default: `2500` |
| `pwm_resolution` | int | Optional | The resolution of the [PWM](https://docs.arduino.cc/learn/microcontrollers/analog-output) driver (for example, the number of ticks for a full period). <br> Default: `0` |

### PWM frequency and `esp32` boards

A `gpio` servo using a PWM pin leaves you with three remaining PWM frequencies for use on an `esp32`.
If the frequency of another PWM signal is unimportant, it can also be set to the same frequency as your servo.
See [PWM signals on `esp32` pins](/micro-rdk/board/esp32/#pwm-signals-on-esp32-pins) for more information.

{{% alert title="Tip" color="tip" %}}

Refer to your servo's data sheet for [pulse-width modulation (PWM)](https://docs.arduino.cc/learn/microcontrollers/analog-output), rotation, and wiring specifications.

{{% /alert %}}

{{< readfile "/static/include/components/test-control/servo-control.md" >}}
