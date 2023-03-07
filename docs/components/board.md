---
title: "Board Component"
linkTitle: "Board"
weight: 20
type: "docs"
description: "The signal wire hub of a robot, with GPIO pins for transmitting signals between the robot's computer and its other components."
tags: ["board", "components"]
icon: "img/components/board.png"
# SMEs: Gautham, Rand
---

A *board* is the signal wire hub of a robot that provides access to GPIO pins.

If your board has a computer that is capable of running `viam-server`, or is connected to one, it can act not only as the signal wire hub for your robot, but also as the software hub.

Configure a board component on your robot to control and read from the other hardware components of the robot, signaling through the GPIO pins on the board as overseen by a computer running `viam-server`.

{{% figure src="../img/board/board-comp-options.png" alt="Image showing two board options: First, running viam-server locally and second, running via a peripheral plugged into the USB port of a computer that is running the viam-server." title="Two different board options: a single-board computer with GPIO pins running `viam-server` locally, or a GPIO peripheral plugged into a desktop computer's USB port, with the computer running `viam-server`." %}}

#### What does "signal wire hub" mean?

A robot's board component has general purpose input/output (GPIO) pins.
As the name suggests, these pins can be inputs or outputs, and can be set high or low--that is, turned on or off--and thus used to signal (or read signals from) other hardware.
Many GPIO implementations also support [PWM (Pulse Width Modulation)](https://en.wikipedia.org/wiki/Pulse-width_modulation), or can be used as more advanced signaling systems such as [I2C](#i2c), [SPI](#spi-bus), or UART/Serial.

#### What can I use as my board?

Generally, you should use a single-board computer with GPIO pins or a computer outfitted with a GPIO peripheral.

This way, overseen by a computer running `viam-server`, the GPIO pins on your board can receive signals from and send signals to the hardware components of your robot.

**Single-Board Computer with GPIO Pins:**

This refers to boards like the [Raspberry Pi](/installation/prepare/rpi-setup/), [BeagleBone](/installation/prepare/beaglebone-setup/), and [Jetson](/installation/prepare/jetson-nano-setup/).

These are all small computing devices outfitted with GPIO pins that are capable of advanced computation, including running `viam-server`.

{{% alert title="Note" color="note" %}}
If you want to use the GPIO pins on your single-board computer to control your robot, the board itself must run `viam-server`.
The GPIO pins of various boards (including Raspberry Pi) are not accessible to external computers.
{{% /alert %}}

**Computer outfitted with a GPIO Peripheral**:

A GPIO peripheral can act as the signal wire hub of your robot.
However, a board like this does not contain a computer to run `viam-server` on the robot, so it can only act as the *board* if you have physically connected it to another computer.

In this case, the computer running `viam-server` signals through the GPIO peripheral's GPIO pins to communicate with the other hardware components of the robot.

You can use any computer capable of running `viam-server`, whether it's your personal computer or another machine, as long as it is connected to the GPIO peripheral.

<!-- ESP-32 - mini RDK -->
<br>

Most robots with a board need at least the following hardware:

- A power supply with the correct voltage and current to avoid damaging or power cycling the board.
See the data sheet of your board model for requirements.

  - For example, a Raspberry Pi 4 takes a 5V power supply and converts it to 3.3V for its logic circuitry.
  The easiest way to power it is with a 5V USB-C power supply.

## Configuration

Refer to the following example configuration file for a single-board computer like Raspberry Pi:

{{< tabs name="Example Board Config" >}}
{{% tab name="Config Builder" %}}

![An example of configuration for a single-board computer in the Viam app config builder.](../img/board/board-config-ui.png)

{{% /tab %}}
{{% tab name="Template JSON" %}}

```json
{
  "components": [
    {
      "type": "board",
      "model": <your_model>
      "name": <your_name>
    }
  ]
}
```

{{% /tab %}}
{{% tab name="Full JSON Example" %}}

```json
{
  "components": [
    {
      "type": "board",
      "model": "pi"
      "name": "viam-board-example"
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

| Attribute | Inclusion | Description |
| ----------- | -------------- | --------------  |
| `type`  |  *Required* | All boards are of type `board`. |
| `model` | *Required* | Specify the correct `model` for your board. |
| `name`  | *Required* | Choose a name for your board. Note that the `name` you choose is the name you need to refer to this particular board in your code. |

For the `model`, supported board models include:

- **pi**: Raspberry Pi 4 or Pi Zero W2

- **beaglebone**: BeagleBone AI 64

- **ti**: TDA4VM devkit

- **jetson**: Nvidia Jetson Xavier NX, Nvidia Jetson Nano

- **numato**: Numato GPIO model (GPIO peripheral)

For more advanced configuration options, read on.

## Deeper Dives: Advanced Configuration

### Using GPIO

Essentially all electrical signals sent from and received by your board go through GPIO pins.
It is important to understand some of what they can do and how to use them.

Here are a few use cases:

- Can be set high (to 3.3V for example) or low (zero volts) to do things like:
  - Switch an enable or mode pin on a motor driver or other chip.
  - Light up an LED or similar.
  - Switch a relay.
- Send a PWM signal to control the speed of a motor or servo.
- Read the state of the pin (High/Low), which can be used to monitor the status of whatever is connected to it.
- Receive digital signals from sensors [see I2C & SPI protocols](#i2c) and [Analogs](#analogs) sections below.
- Receive input as a digital interrupt, [detailed below](#digital-interrupts).

Some things GPIO pins *cannot* do:

- Power a motor or other high power draw device directly.
GPIO pins are built for logic levels of power, that is 3.3V and 16mA per pin.
Power amplification (a motor driver or relay) would be necessary.
- Receive signals over 3.3V (or whatever the logic voltage is on a given board).

If you are using GPIO pin methods like `gpio_pin_by_name` ([documented in our Python SDK](https://python.viam.dev/autoapi/viam/components/board/index.html#viam.components.board.Board.gpio_pin_by_name)) you do not need to configure anything about the pins in your config file.
The pins are automatically configured based on the board model you put in your config, and you can access them using the board pin number (*not* the GPIO number).
You can find these pin numbers from an online service such as <a href="https://pinout.xyz" Target="_blank">pinout.xyz</a> or by running `pinout` in your Pi terminal.

#### Getting started with GPIO and the Viam SDK

The following snippet uses the `gpio_pin_by_name` method to get a GPIO pin by name.
It then uses the `set` method to set the pin to high.
This turns the LED connected to pin 8 on.

{{% alert title="Note" color="note" %}}
These code snippets expect you to have a board named "local" configured as a component of your robot, and an LED connected to pin 8.
{{% /alert %}}

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
from viam.components.board import Board

local = Board.from_robot(robot, 'local')
led = await local.gpio_pin_by_name('8')

# When True, sets the LED pin to high/on.
await led.set(True)
await asyncio.sleep(1)

# When False, sets the pin to low/off.
await led.set(False)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
import (
  "context"
  "time"

  "github.com/edaniels/golog"

  "go.viam.com/rdk/components/board"
)

local, err := board.FromRobot(robot, "local")
if err != nil {
  logger.Fatalf("could not get board: %v", err)
}

led, err := local.GPIOPinByName("8")
if err != nil {
  logger.Fatalf("could not get led: %v", err)
}

// When true, sets the LED pin to high/on.
led.Set(context.Background(), true, nil)
time.Sleep(1 * time.Second)

// When false, sets the LED pin to low/off.
led.Set(context.Background(), false, nil)
```

{{% /tab %}}
{{< /tabs >}}

### Analogs

If an analog to digital converter (ADC) chip is being used in your
robot, analog readers (analogs) will have to be configured.
An ADC takes a voltage as input and converts it to an integer output (for example, a
number between 0 and 1023 in the case of the 10 bit MCP3008 chip).

#### Configuration

Some boards like Numato have built-in ADCs which makes configuration more straightforward.

Some boards (such as Raspberry Pi) communicate with the ADC over SPI so both analog and SPI must be configured.
An example:

``` json
{
  "components": [
    {
      "attributes": {
        "analogs": [
          {
            "chip_select": "24",
            "name": "current",
            "pin": "1",
            "spi_bus": "main"
          },
          {
            "chip_select": "24",
            "name": "pressure",
            "pin": "0",
            "spi_bus": "main"
          }
        ],
        "spis": [
          {
            "bus_select": "0",
            "name": "main"
          }
        ]
      },
      "model": "pi",
      "name": "local",
      "type": "board"
    }
  ]
}
```

Note that the name of the SPI bus ("main") matches between the analog
configuration and SPI configuration.

##### Required Fields

Name | Type | Default Value | Description
-------------- | ---- | ------------- | ---------------
|`name` | string | -- | Choose a name for the analog reader
|`spi_bus` | string | -- |This value should match the name given to the relevant SPI bus in its section of the config file.
|`pin`| string | -- | Specify which pin of the ADC chip to use.
|`chip_select`| string| --| Specify the pin number of the board GPIO pin connected to the ADC chip. Use the pin number, not the GPIO number.

##### Optional Fields

**average_over_ms** (int) and **samples_per_sec** (int): Together these
allow for the use of AnalogSmoother.
Specify the duration in milliseconds over which the rolling average of the input should be taken, and the sampling rate in samples per second, respectively.

### Digital Interrupts

Digital interrupts are useful when your code needs to be notified
immediately anytime there is a change in GPIO value.
Contrast this with running the `Get` method on a GPIO pin only at specific times when you want to know its value, which you can do without configuring interrupts; you only need to call `Get` on the name yielded by `GPIOPinByName`.

#### Configuration

An example:

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "attributes": {
        "digital_interrupts": [
          {
            "name": "example-interrupt-1",
            "pin": "15"
          },
          {
            "name": "example-interrupt-2",
            "pin": "16"
          }
        ]
      },
      "model": "pi",
      "name": "local",
      "type": "board"
    }
  ]
}
```

##### Required Fields

Name | Type | Default Value | Description
-------------- | ---- | ------------- | ---------------
|`name`| string|--| Choose a name for the digital interrupt.
|`pin`| string|--| Specify which GPIO pin of the board to use. Use the pin number, not the GPIO number.

##### Optional Fields

Name | Type | Default Value | Description
-------------- | ---- | ------------- | ---------------
|`type`| string|--| Set type to "basic" to count the number of interrupts that occur. Set type to "servo" to count the average time between the interrupts (akin to pulse width).
|`formula`| string|--| Apply a mathematical function to the input.

### Other Communication Methods

Boards can communicate with other hardware components in a few different ways.
Some devices only require basic GPIO pins whereas others require more specialized methods.
For example, the TMC5072 stepper motor microcontroller requires SPI bus communication.
The following are brief descriptions of each protocol Viam supports, as well as the corresponding configuration information.

#### SPI Bus

[Serial Peripheral Interface (SPI)](https://en.wikipedia.org/wiki/Serial_Peripheral_Interface) uses several pins for serial communication: main out/secondary in (MOSI); main in/secondary out (MISO); SCLK, a clock for serial communication; and chip enable (also called chip select) pins.
If you are using a Raspberry Pi, the "built-in" chip select pins are labeled CE0 and CE1 on the pinout sheet.
The required connections between corresponding board pins and peripheral device pins must be wired, but each of these pins does not need to be specified in the config as most boards have them configured by default.
Only the index of the entire bus must be specified.

##### Configuration

The attributes section of a board using SPI will contain the following:

```json {class="line-numbers linkable-line-numbers"}
{
  "spis": [
    {
      "name": "main",
      "bus_select": "0"
    }
  ]
}
```

##### Required Fields

Name | Type | Default Value | Description
-------------- | ---- | ------------- | ---------------
|`name`| string|--| Choose a name for the SPI bus. Note that a component that uses this bus must then have this same name configured in its attributes.
|`bus_select`| string|--| A Raspberry Pi has two SPI buses: 0 and 1. See data sheet for specifics on other boards.

#### I2C

I2C stands for inter-integrated circuit and is similar to SPI but requires fewer pins: serial data (SDA) and serial clock (SCL).
Some boards that support I2C have the SDA and SCL pins configured by default, so in your config file you need only specify which I2C bus you are using.
For example, if you use I2C bus 1 on a Raspberry Pi 4, SDA and SCL will be pins 3 and 5, respectively.
You will also need to enable I2C on your board if it is not enabled by default.
Review the [instructions in our documentation](/installation/prepare/rpi-setup/#enabling-specific-communication-protocols-on-the-raspberry-pi) to learn how to enable I2C on a Raspberry Pi 4.
[Pinout.xyz](https://pinout.xyz/pinout/i2c) has additional information about I2C on Raspberry Pi.

##### Configuration

```json {class="line-numbers linkable-line-numbers"}
{
  "i2cs": [
    {
      "name": "bus1",
      "bus": "1"
    }
  ]
}
```

##### Required Fields

Name | Type | Default Value | Description
-------------- | ---- | ------------- | ---------------
|`name`| string|--| Choose a name for the SPI bus. Note that a component that uses this bus must then have this same name configured in its attributes.
|`bus`| string|--| Usually a number such as 1. See board data sheet for specifics on its I2C wiring. Raspberry Pi recommends using bus 1.

## Implementation

See the [example code above](#getting-started-with-gpio-and-the-viam-sdk) to get started, and check out our [Python SDK Documentation](https://python.viam.dev/autoapi/viam/components/board/board/index.html).

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

You can also ask questions on the [Viam Community Slack](https://join.slack.com/t/viamrobotics/shared_invite/zt-1f5xf1qk5-TECJc1MIY1MW0d6ZCg~Wnw) and we will be happy to help.

## Next Steps

<div class="container text-center">
  <div class="row">
    <div class="col hover-card">
        <a href="/tutorials/pi/make-an-led-blink-with-the-viam-app/">
            <br>
            <h4 style="text-align: left; margin-left: 0px;">Blink an LED with a Pi and the Viam App</h4>
            <p style="text-align: left;">How to make an LED blink with a Raspberry Pi and the Viam app.</p>
        </a>
    </div>
  </div>
</div>
