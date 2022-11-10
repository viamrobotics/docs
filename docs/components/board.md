---
title: "Board Component"
linkTitle: "Board"
weight: 20
type: "docs"
description: "Explanation of board types, configuration, and usage in Viam."
# SMEs: Gautham, Rand
---
In the Viam framework, a **board** is the signal wire hub of a robot.
It sends signals to the other hardware components, and may or may not also act as the software hub, running an instance of the Viam server on its CPU.
Boards have general purpose input/output (GPIO) pins through
which they can transmit <a href="https://en.wikipedia.org/wiki/Pulse-width_modulation" target="_blank">PWM</a>[^pwm] and other signals.

[^pwm]:PWM (Pulse Width Modulation): <a href="https://en.wikipedia.org/wiki/Pulse-width_modulation" target="_blank">ht<span></span>tps://en.wikipedia.org/wiki/Pulse-width_modulation</a>

Some examples of boards include Raspberry Pi, BeagleBone, and Jetson.
These are all single-board computers (SBCs) capable of advanced computation, including running the Viam server.
These all come with built-in GPIO pins.

Another type of board is a GPIO peripheral such as a Numato GPIO Module, which cannot run the Viam server itself, but can take input from another computer running Viam and communicate with other hardware components.
Note that a desktop computer does not typically have GPIO pins, so it cannot act as a board without a GPIO peripheral.

<img src="../img/board/board-comp-options.png" alt="Image showing two board options: First, running the Viam Server locally and second, running via a peripheral plugged into the USB port of a computer that is running the Viam Server.">

*Figure 1. Two different board options: SBC with GPIO pins running Viam server locally; or GPIO peripheral plugged into a computer's USB port, with the computer running Viam server.*

{{% alert title="Note" color="note" %}}  
The GPIO pins of various boards (including Raspberry Pi) are not accessible to external computers.
In these cases, the board itself must run an instance of Viam server.
{{% /alert %}}

## General Hardware Requirements

A common board setup comprises the following:

- A computing device with general purpose input/output (GPIO) pins such as a Raspberry Pi or other single-board computer, or a desktop computer outfitted with a GPIO peripheral.

- Power supply

  - A power supply must supply the correct voltage and sufficient current to avoid damaging or power cycling the board.
    See the board's data sheet for requirements.
    For example, a Raspberry Pi 4 takes a 5V power supply and converts it to 3.3V for its logic circuitry.
    The easiest way to power it is with a 5V USB-C power supply.

- Some component(s) for the board to talk to!
The board can't do much on its own so you'll probably want some actuators and/or sensors to make your robot a robot!

## General Configuration

If your application only involves GPIO and no other board attributes or communication methods are required, your board can be configured quite
simply as in this example:

![board-gen-config](../img/board/board-gen-config.png)

All boards will be of type **board**. Specify the correct **model** for your board.
The following board models are currently supported (not exhaustive):

- **pi**: Raspberry Pi 4 or Pi Zero W

- **ti**: BeagleBone AI 64

- **jetson**: Nvidia Jetson Xavier NX

- **numato**: Numato GPIO model

Give your board a **name**. Choose any name you like, and note that this name is how you will refert to this particular board in your code and when configuring other components.

## Using GPIO

Essentially all electrical signals sent from and received by your board go through GPIO pins so it is important to understand some of what they can do and how to use them.
Here are a few use cases:

- Can be set high (to 3.3V for example) or low (zero volts) to do things like:
  - Switch an enable or mode pin on a motor driver or other chip.
  - Light up an LED or similar.
  - Switch a relay.
- Send a PWM signal to control the speed of a motor or servo.
- Read the state of the pin (i.e., the voltage), which can be used to monitor the status of whatever is connected to it.
- Receive digital signals from sensors, as detailed in the Analog section below.
- Receive input as a digital interrupt, detailed below.
- Communicate using different protocols such as I2C and SPI bus.

Some things GPIO pins *cannot* do:

- Power a motor or other high power draw device directly.
GPIO pins are built for logic levels of power, i.e., 3.3V and 16mA per pin.
Power amplification (a motor driver or relay) would be necessary.
- Receive signals over 3.3V (or whatever the logic voltage is on a given board).

If you are using GPIO pin methods like `gpio_pin_by_name` ([documented in our Python SDK](https://python.viam.dev/autoapi/viam/components/board/index.html#viam.components.board.Board.gpio_pin_by_name)) you do not need to configure anything about the pins in your config file. The pins are automatically configured based on the board model you put in your config, and you can access them using the board pin number (*not* the GPIO number). You can find these pin numbers from an online service such as <a href="https://pinout.xyz" Target="_blank">pinout.xyz</a> or by running `pinout` in your Pi terminal.

### Getting started with GPIO and the Viam SDK

In the snippet below, we are using the `gpio_pin_by_name` method to get a GPIO pin by name. We are then using the `set` method to set the pin high. This will turn on the LED connected to the pin 8.

{{% alert title="Note" color="note" %}}  
These code snippets expect you to have a board named "local" configured as a component of your robot, and an LED connected to pin 8.
{{% /alert %}}

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.board import Board

local = Board.from_robot(robot, 'local')
led = await local.gpio_pin_by_name('8')

# When True, sets the LED pin to high or on.
await led.set(True)
await asyncio.sleep(1)

# When False, sets the pin to low or off.
await led.set(False)
```

{{% /tab %}}
{{% tab name="Golang" %}}

```go
import (
  "time"
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

//When true, sets the LED pin to high or on.
led.Set(context.Background(), true, nil)
time.Sleep(1 * time.Second)

//When false, sets the LED pin to low or off.
led.Set(context.Background(), false, nil)
```

{{% /tab %}}
{{< /tabs >}}


## Analogs

If an analog to digital converter (ADC) chip is being used in your
robot, analog readers (analogs) will have to be configured. An ADC takes
a voltage as input and converts it to an integer output (for example, a
number between 0 and 1023 in the case of the 10 bit MCP3008 chip).

### Configuration

Some boards like Numato have built-in ADCs which makes configuration more straightforward.

Some boards (such as Raspberry Pi) communicate with the ADC over SPI so both analog and SPI must be configured. An example:

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

#### Required Fields

Name | Type | Default Value | Description
-------------- | ---- | ------------- | ---------------
|`name` | string | -- | Choose a name for the analog reader
|`spi_bus` | string | -- |This value should match the name given to the relevant SPI bus in its section of the config file.
|`pin`| string | -- | Specify which pin of the ADC chip to use.
|`chip_select`| string| --| Specify the pin number of the board GPIO pin connected to the ADC chip. Use the pin number, not the GPIO number.

#### Optional Fields

**average_over_ms** (int) and **samples_per_sec** (int): Together these
allow for the use of AnalogSmoother. Specify the duration in
milliseconds over which the rolling average of the input should be
taken, and the sampling rate in samples per second, respectively.

## Digital Interrupts

Digital interrupts are useful when your code needs to be notified
immediately anytime there is a change in GPIO value. Contrast this with
running the Get method on a GPIO pin only at specific times when you
want to know its value, which you can do without configuring interrupts;
you only need to getGPIOpin by name.

### Configuration

An example:

```json-viam
{
  "components": [
    {
      "attributes": {
        "digital_interrupts": [
          {
            "name": "encoder",
            "pin": "15"
          },
          {
            "name": "encoder-b",
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

#### Required Fields

Name | Type | Default Value | Description
-------------- | ---- | ------------- | ---------------
|`name`| string|--| Choose a name for the digital interrupt.
|`pin`| string|--| Specify which GPIO pin of the board to use. Use the pin number, not the GPIO number.

#### Optional Fields

Name | Type | Default Value | Description
-------------- | ---- | ------------- | ---------------
|`type`| string|--| Set type to "basic" to count the number of interrupts that occur. Set type to "servo" to count the average time between the interrupts (akin to pulse width).
|`formula`| string|--| Apply a mathematical function to the input.

## Other Communication Methods

Boards can communicate with other hardware components in a few different ways.
Some devices only require basic GPIO pins whereas others require more specialized methods.
For example, the TMC5072 stepper motor microcontroller requires SPI bus communication.
The following are brief descriptions of each protocol Viam supports, as well as the corresponding configuration information.

### SPI Bus

<a href="https://en.wikipedia.org/wiki/Serial_Peripheral_Interface" target="_blank">Serial Peripheral Interface (SPI)</a>[^spi] uses several pins for serial communication: main out/serial in (MOSI); main in/serial out (MISO); SCLK which is a clock for serial communication; and chip enable (also called chip select) pins.
If you are using a Raspberry Pi, the “built-in” chip select pins are labeled CE0 and CE1 on the pinout sheet.
The required connections between corresponding board pins and peripheral device pins must be wired, but each of these pins does not need to be specified in the config as most boards have them configured by default.
Only the index of the entire bus must be specified.

[^spi]:Serial Peripheral Interface (SPI):  <a href="https://en.wikipedia.org/wiki/Serial_Peripheral_Interface" target="_blank">ht<span></span>tps://en.wikipedia.org/wiki/Serial_Peripheral_Interface</a>

#### Configuration

The attributes section of a board using SPI will contain the following:

```json-viam
{
  "spis": [
    {
      "name": "main",
      "bus_select": "0"
    }
  ]
}
```

#### Required Fields

Name | Type | Default Value | Description
-------------- | ---- | ------------- | ---------------
|`name`| string|--| Choose a name for the SPI bus. Note that a component that uses this bus must then have this same name configured in its attributes.
|`bus_select`| string|--| A Raspberry Pi has two SPI buses: 0 and 1. See data sheet for specifics on other boards.

### I2C

I2C stands for inter-integrated circuit and is similar to SPI but requires fewer pins: serial data (SDA) and serial clock (SCL).
Some boards that support I2C have the SDA and SCL pins configured by default, so in your config file you need only specify which I2C bus you are using.
For example, if you use I2C bus 1 on a Raspberry Pi 4, SDA and SCL will be pins 3 and 5, respectively.
You will also need to enable I2C on your board if it is not enabled by default.
Review the [instructions in our documentation](/getting-started/rpi-setup/#enabling-the-i2c-protocol-on-the-raspberry-pi) to learn how to enable I2C on a Raspberry Pi 4.
<a href="https://pinout.xyz/pinout/i2c" target="_blank">Pinout.xyz</a>[^pocom] has additional information about I2C on Raspberry Pi.
[^pocom]:I2C - Inter Integrated Circuit on Pinout.xyz:  <a href="https://pinout.xyz/pinout/i2c" target="_blank">ht<span></span>tps://pinout.xyz/pinout/i2c</a>

#### Configuration

```json-viam
{
  "i2cs": [
    {
      "name": "bus1",
      "bus": "1"
    }
  ]
}
```

#### Required Fields

Name | Type | Default Value | Description
-------------- | ---- | ------------- | ---------------
|`name`| string|--| Choose a name for the SPI bus. Note that a component that uses this bus must then have this same name configured in its attributes.
|`bus`| string|--| Usually a number such as 1. See board data sheet for specifics on its I2C wiring. Raspberry Pi recommends using bus 1.

## Implementation

[Python SDK
Documentation](https://python.viam.dev/autoapi/viam/components/board/board/index.html)
