---
title: "Configure a GPIO Servo (Micro-RDK)"
linkTitle: "gpio (Micro-RDK)"
weight: 90
type: "docs"
description: "Configure a gpio hobby servo with a microcontroller."
tags: ["servo", "components"]
icon: true
images: ["/icons/components/servo.svg"]
aliases:
  - /micro-rdk/servo/gpio/
  - /build/micro-rdk/servo/gpio/
  - /components/servo/gpio-micro-rdk/
micrordk_component: true
toc_hide: true
# SME: Gautham
---

Configure a `gpio` servo to integrate a hobby servo controlled by general-purpose input/output (GPIO) pins into your machine.
Physically connect your servo to your microcontroller and power both on.
Then, configure the servo:

{{< tabs name="Configure a gpio Servo" >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page.
Click the **+** icon next to your machine part in the left-hand menu and select **Component or service**.
Select the `servo` type, then select the `gpio` model.
Enter a name or use the suggested name for your servo and click **Create**.

![An example configuration for a gpio servo.](/components/servo/gpio-servo-ui-config.png)

Copy and paste the following attribute template into your servo's attributes field.
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
| `board` | string | **Required** | `name` of the [board](/operate/reference/components/board/) the servo is wired to. |
| `frequency_hz` | int | Optional | The frequency of [PWM](https://docs.arduino.cc/learn/microcontrollers/analog-output) pulses sent to the servo, in Hertz (*Hz*). <br> Default = [`300`] <br> Range = [`0`, `450`] |
| `min_angle_deg` | int | Optional | The minimum angle in degrees that the servo can reach. <br> Default = `0` <br> Range = [`0`, `180`] |
| `max_angle_deg` | int | Optional | The maximum angle in degrees that the servo can reach. <br> Default = `180` <br> Range = [`0`, `180`] |
| `min_period_us` | int | Optional | Override the safe minimum [PWM](https://docs.arduino.cc/learn/microcontrollers/analog-output) pulse width in microseconds. <br> Default: `500` |
| `max_period_us` | int | Optional | Override the safe maximum [PWM](https://docs.arduino.cc/learn/microcontrollers/analog-output) pulse width in microseconds. <br> Default: `2500` |
| `pwm_resolution` | int | Optional | The resolution of the [PWM](https://docs.arduino.cc/learn/microcontrollers/analog-output) driver (for example, the number of ticks for a full period). <br> Default: `0` |

### PWM frequency and `esp32` boards

A `gpio` servo using a PWM pin leaves you with three remaining PWM frequencies for use on an `esp32`.
If the frequency of another PWM signal is unimportant, it can also be set to the same frequency as your servo.
See [PWM signals on `esp32` pins](/operate/reference/components/board/esp32/#pwm-signals-on-esp32-pins) for more information.

{{% alert title="Tip" color="tip" %}}

Refer to your servo's data sheet for [pulse-width modulation (PWM)](https://docs.arduino.cc/learn/microcontrollers/analog-output), rotation, and wiring specifications.

{{% /alert %}}

{{< readfile "/static/include/components/test-control/servo-control.md" >}}

## Troubleshooting

{{< readfile "/static/include/components/troubleshoot/servo.md" >}}

## Next steps

For general configuration and development info, see:

{{< cards >}}
{{% card link="/dev/reference/apis/components/servo/" customTitle="Servo API" noimage="true" %}}
{{% card link="/operate/get-started/supported-hardware/" noimage="true" %}}
{{% card link="/operate/control/web-app/" noimage="true" %}}
{{< /cards >}}
