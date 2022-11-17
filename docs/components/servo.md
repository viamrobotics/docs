---
title: "Servo Component"
linkTitle: "Servo"
weight: 80
type: "docs"
description: "Explanation of servo wiring and configuration in Viam."
# SME: #team-bucket
---
Hobby servos are a type of actuator comprising a small motor with built-in closed-loop control.

The Viam `servo` component is not designed to support industrial servomotors.
Configure an industrial servomotor as a [motor](/components/motor/) with an [encoder](/components/encoder/).

## Hardware Requirements

A typical servo control setup comprises the following:

- A Raspberry Pi (or other [board](/components/board/))
- A servo
- An appropriate power supply

## Wiring Example

{{% alert title="Caution" color="caution" %}}  
Always disconnect devices from power before plugging, unplugging or moving wires or otherwise modifying electrical circuits.
{{% /alert %}}

Here's an example of how a servo might be wired to a Raspberry Pi:  

![A diagram showing the signal wire of a servo connected to pin 16 on a Raspberry Pi. The servo's power wires are connected to a 4.8V power supply.](../img/servo/servo-wiring.png)

## Viam Configuration

The following fields are required when configuring a servo:

- **Name**: A name of the user's choosing by which to identify the component

- **Type**: `servo` for all servos

- **Model**: Either `gpio`, `pi`, or `fake`:

  - `gpio` is the **recommended general-purpose model**, compatible with all Viam-supported boards including Raspberry Pi.

  - `pi` is only compatible with Raspberry Pi.
  It has a timeout parameter to help prevent burning out cheap servos, but this is not necessary in most cases.

  - `fake` is for testing code without any actual hardware.

- **Attributes**: Other details the component requires to function.
All models require the following:

  - `pin` (string): The board pin (with PWM capabilities) to which the servo's control wire is attached.
  Use pin number, not GPIO number.

  - `board` (string): The name of the board to which the servo is wired.

  - Some models have additional attributes which are [described below](#optional-attributes-gpio-model).

### Example Config

An example configuration file containing the necessary attributes is as follows:

{{< tabs name="Example Servo Config" >}}
{{% tab name="Raw JSON" %}}

```json
{
  "components": [
    {
      "name": "example-pi",
      "type": "board",
      "model": "pi"
      
    },
    {
      "name": "example-name",
      "type": "servo",
      "model": "gpio",
      "attributes": {
        "pin": "16",
        "board": "example-pi"
      }
    }
  ]
}
```

{{% /tab %}}
{{< tab name="Annotated JSON" >}}

<img src="../img/servo/servo-json.png" alt="An example servo config file with explanatory annotations."></img>

{{< /tab >}}
{{< /tabs >}}

### Optional Attributes: GPIO Model

Attribute Name | Type | Description
-------------- | ---- | ---------------
`min_angle_deg` | float64 | Specifies the minimum angle in degrees to which the servo can move. Does not affect PWM calculation.
`max_angle_deg` | float64 | Specifies the maximum angle in degrees to which the servo can move. Does not affect PWM calculation.
`starting_position_deg` | float64 | Starting position of the servo in degrees.
`frequency_hz` | uint | The servo driver will attempt to change the GPIO pin's frequency. Default for a Pi is 19.2MHz.
`pwm_resolution` | uint | Resolution of the PWM driver (e.g. number of ticks for a full period). Must be in range (0, 450). If not specified, the driver will attempt to estimate the resolution.
`min_width_us` | uint | Override the safe minimum pulse width in microseconds. This affects PWM calculation.
`max_width_us` | uint | Override the safe maximum pulse width in microseconds. This affects PWM calculation.

## Implementation

The servo component supports the following methods:

Method Name (Go) | Method Name (Python) | Description
---------------- | -------------------- | -----------
Move | move | Move the servo to the provided angle.
Position | get_position | Returns an int representing the current angle of the servo in degrees.
Stop | stop | Stops the servo.
IsMoving | is_moving | Returns true if the servo is currently moving. Not all servos are able to report this.

[Python SDK Documentation](https://python.viam.dev/autoapi/viam/components/servo/index.html)

{{% alert title="Note" color="note" %}}
If you are using a continuous rotation servo, you will still use the Move command but instead of moving to a given position, the servo will start moving at a set speed.
The speed will be approximately linearly related to the "angle" you pass in, but you will need to determine based on your own hardware which "angle" represents your desired speed.
{{% /alert %}}