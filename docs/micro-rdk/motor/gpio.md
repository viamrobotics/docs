---
title: "Configure a gpio motor"
linkTitle: "gpio"
weight: 10
type: "docs"
description: "Configure brushed or brushless DC motors."
images: ["/icons/components/motor.svg"]
# SMEs: Rand, James
---

The `gpio` model supports [DC motors](https://en.wikipedia.org/wiki/DC_motor) (both brushed and brushless).

You can configure [encoders](/micro-rdk/encoder/) to work with `gpio` motors.
Find more information in the [encoded motor documentation](/components/motor/gpio/encoded-motor/).

To configure a DC motor as a component of your robot, first configure the [board](/micro-rdk/board/) to which the motor driver is wired.
Then add your motor:

{{< tabs name="gpio-config">}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `motor` type, then select the `gpio` model.
Enter a name for your motor and click **Create**.

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
      "type": "board",
      "namespace": "rdk",
      "attributes": {},
      "depends_on": [],
    },
    {
      "name": "<your-motor-name>",
      "model": "gpio",
      "type": "motor",
      "namespace": "rdk",
      "attributes": {
        "pins": {
          <...>
        },
        "board": "<your-board-name>",
        "min_power_pct": <float>,
        "max_power_pct": <float>,
        "pwm_freq": <float>,
        "dir_flip": <float>,
        "en_low": <float>
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
      "type": "board",
      "namespace": "rdk",
      "attributes": {},
      "depends_on": []
    },
    {
      "name": "example-gpio",
      "model": "gpio",
      "type": "motor",
      "namespace": "rdk",
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
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `board` | string | **Required** | `name` of the [board](/micro-rdk/board/) to which the motor driver is wired. |
| `pins` | object | **Required** | A structure that holds pin configuration information; [see below](#pins). |
| `min_power_pct` | number | Optional | Sets a limit on minimum power percentage sent to the motor. <br> Default: `0.0` |
| `max_power_pct` | number | Optional | Range is 0.06 to 1.0; sets a limit on maximum power percentage sent to the motor. <br> Default: `1.0` |
| `pwm_freq` | int | Optional | Sets the PWM pulse frequency in Hz. Many motors operate optimally in the kHz range. <br> Default: `800` |
| `dir_flip` | bool | Optional | Flips the direction of "forward" versus "backward" rotation. Default: `false` |
| `en_high` / `en_low` | string | Optional | Some drivers have optional enable pins that enable or disable the driver chip. If your chip requires a high signal to be enabled, add `en_high` with the pin number to the pins section. If you need a low signal use `en_low`. |
| `encoder` | string | Optional | The name of an encoder attached to this motor. See [encoded motor](/components/motor/gpio/encoded-motor/). |

Refer to your motor and motor driver data sheets for specifics.

## `pins`

There are two common ways for your computer to communicate with a brushed DC motor driver chip that are supported in the micro-RDK.
**Your motor driver data sheet will specify which one to use.**

- PWM/DIR: Use this if one of your motor driver's pins (labeled "PWM") takes a [pulse width modulation (PWM)](https://en.wikipedia.org/wiki/Pulse-width_modulation) signal to the driver to control speed while another pin labeled "DIR" takes a high or low signal to control the direction.
  - Configure `pwm` and `dir`.
- In1/In2 and PWM: Use this if your motor driver uses three pins: In1 (A) and In2 (B) to control direction and a separate PWM pin to control speed.
  - Configure `a`, `b`, and `pwm`.

Inside the `pins` struct you need to configure **two or three** of the following, depending on your motor driver:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `a` | string | **Required** for some drivers | Board {{< glossary_tooltip term_id="pin-number" text="pin number" >}} this motor driver's "IN1" or "A" pin is wired to. |
| `b` | string | **Required** for some drivers | Board {{< glossary_tooltip term_id="pin-number" text="pin number" >}} this motor driver's "IN2" or "B" pin is wired to. |
| `dir` | string | **Required** for some drivers | Board {{< glossary_tooltip term_id="pin-number" text="pin number" >}} this motor driver's direction ("DIR") pin is wired to. |
| `pwm` | string | **Required** | Board {{< glossary_tooltip term_id="pin-number" text="pin number" >}} this motor driver's "PWM" pin is wired to. |

### PWM frequency and `esp32` boards

Each `gpio` motor uses a PWM pin at 10000 Hz PWM frequency.

This leaves you with three remaining PWM frequencies for use on an `esp32`.
If the frequency of another PWM signal is unimportant, it can also be set to 10000 Hz.
See [PWM signals on `esp32` pins](/micro-rdk/board/esp32/#pwm-signals-on-esp32-pins) for more information.

{{< readfile "/static/include/components/test-control/motor-control.md" >}}
