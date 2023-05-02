---
title: "Configure a gpio Servo"
linkTitle: "gpio"
weight: 90
type: "docs"
description: "Configure a gpio servo."
tags: ["servo", "components"]
icon: "img/components/servo.png"
# SME: Rand
---

Configure a `gpio` servo to integrate a hobby servo controlled by general-purpose input/output (GPIO) pins on a non-`pi` model [board](components/board) into your robot:

{{< tabs name="Configure a Gpio Servo" >}}
{{% tab name="Config Builder" %}}

Navigate to the **config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your servo, select the type `servo`, and select the `gpio` model.

Click **Create component**:

![An example configuration for a gpio servo in the Viam app Config Builder.](../img/gpio-servo-ui-config.png)

Edit and fill in the `"attributes"` JSON to align with your `board` `name` and GPIO wiring.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
    "components": [
        {
            "name": "<your-servo-name>",
            "type": "servo",
            "model": "gpio",
            "attributes": {
                "pin": "<your-pin-number>",
                "board": "<your-board-nam>"
            }
        }, ... <insert your board component config>
    }
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
        "name": "your-servo-name",
        "type": "servo",
        "model": "gpio",
        "attributes": {
            "pin": "16",
            "board": "your-board-name"
        }
    }, 
    {
        "name": "your-board-name",
        "type": "board",
        "model": "jetson"
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `gpio` servos:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `pin` | string | **Required** | The {{< glossary_tooltip term_id="pin-number" text="pin number" >}} of the pin the servo's control wire is wired to on the [board](/components/board). |
| `board` | string | **Required** | `name` of the [board](/components/board) the servo is wired to. |
| `min_angle_deg` | float | Optional | The minimum angle in degrees that the servo can move from its starting position. Refer to your servo's data sheet for specifications. |
| `max_angle_deg` | float | Optional | The maximum angle in degrees that the servo can move from its starting position. Refer to your servo's data sheet for specifications. |
| `starting_position_deg` | float | Optional | Starting position of the servo in degrees. |
| `frequency_hz` | int | Optional | The rate of pulses sent to the servo. The servo driver will attempt to change the GPIO pin's frequency, in Hertz (*Hz*). The recommended [pulse-width modulation (PMW)](/components/board/#pwm) frequency for servos is typically in the range of 40-200 Hz, with most servos using 50 Hz. Refer to your servo's data sheet for specifications. <br> Maximum = `450` |
| `pwm_resolution` | int | Optional | Resolution of the PWM driver (for example, the number of ticks for a full period). If not specified, the driver will attempt to estimate the resolution. Refer to your servo's data sheet for specifications. <br> Range = (`0`, `450`) |
| `min_width_us` | int | Optional | Override the safe minimum pulse width in microseconds. Affects PWM calculation. |
| `max_width_us` | int | Optional | Override the safe maximum pulse width in microseconds. Affects PWM calculation. |
