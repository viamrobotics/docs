---
title: "Configure a gpio Servo"
linkTitle: "gpio"
weight: 90
type: "docs"
description: "Configure a gpio servo."
tags: ["servo", "components"]
icon: "/icons/components/servo.svg"
aliases:
  - "/components/servo/gpio/"
# SME: Rand
---

Configure a `gpio` servo to integrate a hobby servo controlled by general-purpose input/output (GPIO) pins on a non-`pi` model [board](/components/board/) into your robot:

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
  "min_angle_deg": <float>,
  "max_angle_deg": <float>,
  "starting_position_deg": <float>,
  "frequency_hz": <int>,
  "pwm_resolution": <int>,
  "min_width_us": <int>,
  "max_width_us": <int>
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
        "min_angle_deg": <float>,
        "max_angle_deg": <float>,
        "starting_position_deg": <float>,
        "frequency_hz": <int>,
        "pwm_resolution": <int>,
        "min_width_us": <int>,
        "max_width_us": <int>
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
      "model": "jetson",
      "type": "board",
      "namespace": "rdk"
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
| `pin` | string | **Required** | The {{< glossary_tooltip term_id="pin-number" text="pin number" >}} of the pin the servo's control wire is wired to on the [board](/components/board/). |
| `board` | string | **Required** | `name` of the [board](/components/board/) the servo is wired to. |
| `min_angle_deg` | float | Optional | The minimum angle in degrees that the servo can reach. <br> Default = `0.0` <br> Range = [`0.0`, `180.0`] |
| `max_angle_deg` | float | Optional | The maximum angle in degrees that the servo can reach. <br> Default = `180.0` <br> Range = [`0.0`, `180.0`] |
| `starting_position_deg` | float | Optional | Starting position of the servo in degrees. <br> Default = `0.0` <br> Range = [`0.0`, `180.0`] |
| `frequency_hz` | int | Optional | The frequency of [PWM](https://docs.arduino.cc/learn/microcontrollers/analog-output) pulses sent to the servo, in Hertz (*Hz*). <br> Default = [`300`] <br> Range = [`0`, `450`] |
| `pwm_resolution` | int | Optional | The resolution of the [PWM](https://docs.arduino.cc/learn/microcontrollers/analog-output) driver (for example, the number of ticks for a full period). If not specified or given as `0`, the driver will attempt to estimate the resolution. |
| `min_width_us` | int | Optional | Override the safe minimum [PWM](https://docs.arduino.cc/learn/microcontrollers/analog-output) pulse width in microseconds. <br> Range > `450` |
| `max_width_us` | int | Optional | Override the safe maximum [PWM](https://docs.arduino.cc/learn/microcontrollers/analog-output) pulse width in microseconds. <br> Range < `2500` |

{{% alert title="Tip" color="tip" %}}

Refer to your servo's data sheet for [pulse-width modulation (PWM)](https://docs.arduino.cc/learn/microcontrollers/analog-output), rotation, and wiring specifications.

{{% /alert %}}

{{< readfile "/static/include/components/test-control/servo-control.md" >}}
