---
title: "Configure a GPIO Motor (Micro-RDK)"
linkTitle: "gpio (Micro-RDK)"
weight: 10
type: "docs"
description: "Configure brushed or brushless DC motors with a microcontroller."
images: ["/icons/components/motor.svg"]
aliases:
  - /micro-rdk/motor/gpio/
  - /components/motor/gpio-micro-rdk/
micrordk_component: true
toc_hide: true
# SMEs: Rand, James
---

The `gpio` model supports [DC motors](https://en.wikipedia.org/wiki/DC_motor) (both brushed and brushless).

You can configure [encoders](/operate/reference/components/encoder/) to work with `gpio` motors.
Find more information in the [encoded motor documentation](/operate/reference/components/motor/encoded-motor/).

To configure a DC motor as a component of your machine, first make sure the motor is wired to a suitable motor driver, which is in turn wired to the microcontroller.
Connect the system to power if you want to test it while configuring.
Configure the [board](/operate/reference/components/board/esp32/) to which the motor driver is wired.
Then configure the motor:
Then add your motor:

{{< tabs name="gpio-config">}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page.
Click the **+** icon next to your machine part in the left-hand menu and select **Component or service**.
Select the `motor` type, then select the `gpio` model.
Enter a name or use the suggested name for your motor and click **Create**.

![G P I O motor config in the builder UI with the In1 and In2 pins configured and the PWM pin field left blank.](/components/motor/gpio-config-ui.png)

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json
{
  "components": [
    {
      "name": "<your-board-name>",
      "model": "<your-board-model>",
      "api": "rdk:component:board",
      "attributes": {},
      "depends_on": [],
    },
    {
      "name": "<your-motor-name>",
      "model": "gpio",
      "api": "rdk:component:motor",
      "attributes": {
        "pins": {
          "dir": "<int>",
          "pwm": "<int>"
        },
        "board": "<your-board-name>",
        "min_power_pct": <float>,
        "max_power_pct": <float>,
        "pwm_freq": <float>,
        "dir_flip": <float>
      },
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

An example configuration for a `gpio` motor:

```json
{
  "components": [
    {
      "name": "local",
      "model": "pi",
      "api": "rdk:component:board",
      "attributes": {},
      "depends_on": []
    },
    {
      "name": "example-gpio",
      "model": "gpio",
      "api": "rdk:component:motor",
      "attributes": {
        "pins": {
          "dir": "36",
          "pwm": "32"
        },
        "board": "local"
      },
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `gpio` motors:

<!-- prettier-ignore -->
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `board` | string | **Required** | `name` of the [board](/operate/reference/components/board/) to which the motor driver is wired. |
| `pins` | object | **Required** | A structure that holds pin configuration information; [see below](#pins). |
| `min_power_pct` | float | Optional | Sets a limit on minimum power percentage sent to the motor. <br> Default: `0.0` |
| `max_power_pct` | float | Optional | Range is 0.06 to 1.0; sets a limit on maximum power percentage sent to the motor. <br> Default: `1.0` |
| `pwm_freq` | int | Optional | Sets the PWM pulse frequency in Hz. Many motors operate optimally in the kHz range. <br> Default: `800` |
| `dir_flip` | bool | Optional | Flips the direction of "forward" versus "backward" rotation. Default: `false` |
| `encoder` | string | Optional | The name of an encoder attached to this motor. See [encoded motor](/operate/reference/components/motor/encoded-motor/). |

Refer to your motor and motor driver data sheets for specifics.

## `pins`

There are three common ways for your computer to communicate with a brushed DC motor driver chip.
**Your motor driver data sheet will specify which one to use.**

- PWM/DIR: Use this if one of your motor driver's pins (labeled "PWM") takes a [pulse width modulation (PWM)](https://en.wikipedia.org/wiki/Pulse-width_modulation) signal to the driver to control speed while another pin labeled "DIR" takes a high or low signal to control the direction.
  - Configure `pwm` and `dir`.
- In1/In2: Use this if your motor driver has pins labeled "IN1" and "IN2" or "A" and "B," or similar.
  One digital signal set to a high voltage and another set to a low voltage turns the motor in one direction and vice versa.
  Speed is controlled with PWM through one or both pins.
  - Configure `a` and `b`.
- In1/In2 and PWM: Use this if your motor driver uses three pins: In1 (A) and In2 (B) to control direction and a separate PWM pin to control speed.
  - Configure `a`, `b`, and `pwm`.

Inside the `pins` struct you need to configure **two or three** of the following depending on your motor driver:

<!-- prettier-ignore -->
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `a` | string | **Required** for some drivers | Board {{< glossary_tooltip term_id="pin-number" text="pin number" >}} this motor driver's "IN1" or "A" pin is wired to. |
| `b` | string | **Required** for some drivers | Board {{< glossary_tooltip term_id="pin-number" text="pin number" >}} this motor driver's "IN2" or "B" pin is wired to. |
| `dir` | string | **Required** for some drivers | Board {{< glossary_tooltip term_id="pin-number" text="pin number" >}} this motor driver's direction ("DIR") pin is wired to. |
| `pwm` | string | **Required** | Board {{< glossary_tooltip term_id="pin-number" text="pin number" >}} this motor driver's "PWM" pin is wired to. |

### PWM frequency and `esp32` boards

Each `gpio` motor uses a PWM pin at 10000 Hz PWM frequency.

This leaves you with three remaining PWM frequencies for use on an `esp32`.
If the frequency of another PWM signal is unimportant, it can also be set to 10000 Hz.
See [PWM signals on `esp32` pins](/operate/reference/components/board/esp32/#pwm-signals-on-esp32-pins) for more information.

## Test the motor

{{< readfile "/static/include/components/test-control/motor-control.md" >}}

## Troubleshooting

{{< readfile "/static/include/components/troubleshoot/motor.md" >}}

## Next steps

For more configuration and usage info, see:

{{< cards >}}
{{% card link="/dev/reference/apis/components/motor/" customTitle="Motor API" noimage="true" %}}
{{% card link="/operate/modules/configure-modules/" noimage="true" %}}
{{< /cards >}}
