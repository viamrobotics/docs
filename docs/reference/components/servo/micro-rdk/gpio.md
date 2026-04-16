---
title: "gpio"
linkTitle: "gpio"
weight: 90
type: "docs"
description: "Reference for the gpio servo model. Gpio hobby servo with a microcontroller."
tags: ["servo", "components"]
icon: true
images: ["/icons/components/servo.svg"]
aliases:
  - /micro-rdk/servo/gpio/
  - /build/micro-rdk/servo/gpio/
  - /components/servo/gpio-micro-rdk/
  - "/operate/reference/components/servo/gpio-micro-rdk/"
micrordk_component: true
# SME: Gautham
---

Configure a `gpio` servo to integrate a hobby servo controlled by general-purpose input/output (GPIO) pins into your machine.

{{< tabs name="Configure a gpio Servo" >}}
{{% tab name="Attributes example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "pin": "16",
  "board": "local"
}
```

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-servo-name>",
      "model": "gpio",
      "api": "rdk:component:servo",
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
      "api": "rdk:component:board",
      "attributes": {
        "pins": [16]
      }
    },
    {
      "name": "my_servo",
      "model": "gpio",
      "api": "rdk:component:servo",
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
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `pin` | string | **Required** | The GPIO number of the pin the servo's control wire is wired to on the board. |
| `board` | string | **Required** | `name` of the [board](/reference/components/board/) the servo is wired to. |
| `frequency_hz` | int | Optional | The frequency of [PWM](https://docs.arduino.cc/learn/microcontrollers/analog-output) pulses sent to the servo, in Hertz (*Hz*). <br> Default = [`300`] <br> Range = [`0`, `450`] |
| `min_angle_deg` | int | Optional | The minimum angle in degrees that the servo can reach. <br> Default = `0` <br> Range = [`0`, `180`] |
| `max_angle_deg` | int | Optional | The maximum angle in degrees that the servo can reach. <br> Default = `180` <br> Range = [`0`, `180`] |
| `min_period_us` | int | Optional | Override the safe minimum [PWM](https://docs.arduino.cc/learn/microcontrollers/analog-output) pulse width in microseconds. <br> Default: `500` |
| `max_period_us` | int | Optional | Override the safe maximum [PWM](https://docs.arduino.cc/learn/microcontrollers/analog-output) pulse width in microseconds. <br> Default: `2500` |
| `pwm_resolution` | int | Optional | The resolution of the [PWM](https://docs.arduino.cc/learn/microcontrollers/analog-output) driver (for example, the number of ticks for a full period). <br> Default: `0` |

### PWM frequency and `esp32` boards

A `gpio` servo using a PWM pin leaves you with three remaining PWM frequencies for use on an `esp32`.
If the frequency of another PWM signal is unimportant, it can also be set to the same frequency as your servo.
See [PWM signals on `esp32` pins](/reference/components/board/micro-rdk/esp32/#pwm-signals-on-esp32-pins) for more information.

{{% alert title="Tip" color="tip" %}}

Refer to your servo's data sheet for [pulse-width modulation (PWM)](https://docs.arduino.cc/learn/microcontrollers/analog-output), rotation, and wiring specifications.

{{% /alert %}}

{{< readfile "/static/include/components/test-control/servo-control.md" >}}
