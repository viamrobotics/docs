---
title: "Configure a GPIO-Controlled Servo"
linkTitle: "gpio"
weight: 90
type: "docs"
description: "Configure a gpio servo."
tags: ["servo", "components"]
icon: true
images: ["/icons/components/servo.svg"]
aliases:
  - "/components/servo/gpio/"
component_description: "Supports a hobby servo wired to a board that supports PWM, for example Raspberry Pi 5, Orange Pi, Jetson, or PCAXXXX."
toc_hide: true
# SME: Rand
---

Configure a `gpio` servo to integrate a hobby servo controlled by general-purpose input/output (GPIO) pins on a non-`viam:raspberry-pi:rpi` model [board](/operate/reference/components/board/) into your machine.
Physically connect your servo to your board and power both on.
Then, configure the servo:

{{< tabs name="Configure a gpio Servo" >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page.
Click the **+** icon next to your machine part in the left-hand menu and select **Component or service**.
Select the `servo` type, then select the `gpio` model.
Enter a name or use the suggested name for your servo and click **Create**.

{{< imgproc src="/components/servo/gpio-servo-ui-config.png" alt="An example configuration for a gpio servo." resize="1200x" style="width:650px" class="shadow"  >}}

Fill in the attributes as applicable to your servo, according to the table below.

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
      "api": "rdk:component:board"
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
| `pin` | string | **Required** | The {{< glossary_tooltip term_id="pin-number" text="pin number" >}} of the pin the servo's control wire is wired to on the [board](/operate/reference/components/board/). |
| `board` | string | **Required** | `name` of the [board](/operate/reference/components/board/) the servo is wired to. |
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

## Troubleshooting

{{< readfile "/static/include/components/troubleshoot/servo.md" >}}

## Next steps

For general configuration and development info, see:

{{< cards >}}
{{% card link="/dev/reference/apis/components/servo/" customTitle="Servo API" noimage="true" %}}
{{% card link="/operate/get-started/supported-hardware/" noimage="true" %}}
{{% card link="/operate/control/web-app/" noimage="true" %}}
{{< /cards >}}
