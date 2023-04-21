---
title: "Board Component"
linkTitle: "Board"
weight: 20
type: "docs"
no_list: true
description: "The signal wire hub of a robot, with GPIO pins for transmitting signals between the robot's computer and its other components."
tags: ["board", "components"]
icon: "/components/img/components/board.svg"
# SMEs: Gautham, Rand
---

A *board* is the signal wire hub of a robot that provides access to GPIO pins.

If your board has a computer that is capable of running `viam-server`, or is connected to one, it can act not only as the signal wire hub for your robot, but also as the software hub.

Configure a board component on your robot to control and read from the other hardware components of the robot, signaling through the GPIO pins on the board as overseen by a computer running `viam-server`.

{{% figure src="img/board-comp-options.png" alt="Image showing two board options: First, running viam-server locally and second, running via a peripheral plugged into the USB port of a computer that is running the viam-server." title="Two different board options: a single-board computer with GPIO pins running `viam-server` locally, or a GPIO peripheral plugged into a desktop computer's USB port, with the computer running `viam-server`." %}}

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

Most robots with a board need at least the following hardware:

- A power supply with the correct voltage and current to avoid damaging or power cycling the board.
See the data sheet of your board model for requirements.

  - For example, a Raspberry Pi 4 takes a 5V power supply and converts it to 3.3V for its logic circuitry.
  The easiest way to power it is with a 5V USB-C power supply.

## Configuration

Supported board models include:

| Model | Description |
| ----- | ----------- |
| [`pi`](pi) | [Raspberry Pi 4](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/) or [Raspberry Pi Zero 2 W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/) |
| [`ti`](ti) | [Texas Instruments TDA4VM](https://devices.amazonaws.com/detail/a3G8a00000E2QErEAN/TI-TDA4VM-Starter-Kit-for-Edge-AI-vision-systems) |
| [`beaglebone`](beaglebone) | [BeagleBoard's BeagleBone AI 64](https://beagleboard.org/ai-64) |
| [`jetson`](jetson) | [NVIDIA Jetson AGX Orin](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-orin/), [NVIDIA Jetson Xavier NX](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-agx-xavier/), [NVIDIA Jetson  Nano](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-nano/) |
| [`numato`](numato) | [Numato GPIO Peripheral Modules](https://numato.com/product-category/automation/gpio-modules/) |
| [`nanopi`](nanopi) | [FriendlyElec’s NanoPi Mini Board](https://www.friendlyelec.com/index.php?route=product/category&path=69) |
| [`pca9685`](pca9685) | [PCA9685 Arduino I2C Interface](https://www.adafruit.com/product/815) |
| [`fake`](fake) | A model used for testing, with no physical hardware. |

## Control your board with Viam's client SDK libraries

To get started using Viam's SDKs to connect to and control your robot, go to your robot's page on [the Viam app](https://app.viam.com), navigate to the **code sample** tab, select your preferred programming language, and copy the sample code generated.

When executed, this sample code will create a connection to your robot as a client.
Then control your robot programmatically by adding API method calls as shown in the following examples.

These examples assume you have a board called "my_board" configured as a component of your robot.
If your board has a different name, change the `name` in the code.

## API

The board component supports the following methods:

| Method Name | Description |
| ----------- | ----------- |
| [Readings](#readings) | Get the measurements or readings that this sensor provides. |

### Readings

Get the measurements or readings that this sensor provides.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional[Dict[str, Any]])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional[float])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- `readings` [(Mapping[str, Any])](https://docs.python.org/3/library/typing.html#typing.Mapping): The measurements or readings that this sensor provides.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/sensor/index.html#viam.components.sensor.Sensor.get_readings).

```python
my_sensor = Sensor.from_robot(robot=robot, name='my_sensor')

# Get the readings provided by the sensor.
readings = await my_sensor.get_readings()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `Context` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- `readings` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): The measurements or readings that this sensor provides.
- `error` [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/sensor#Sensor).

```go
mySensor, err := sensor.FromRobot(robot, "my_sensor")
if err != nil {
  logger.Fatalf("cannot get sensor: %v", err)
}

readings, err := mySensor.Readings(context.Background(), nil)
```

{{% /tab %}}
{{< /tabs >}}

## Signaling Objects

### GPIO Pins

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

If an analog-to-digital converter (ADC) chip is being used in your
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

## Communication Protocols

Boards can communicate with other hardware components in a few different ways.
Some devices only require basic GPIO pins whereas others require more specialized methods.
For example, the TMC5072 stepper motor microcontroller requires SPI bus communication.
The following are brief descriptions of each protocol Viam supports, as well as the corresponding configuration information.

### SPI Buses

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
|`bus_select`| string|--| A Raspberry Pi has two SPI buses: `0` and `1`. See your board's data sheet for specifics on its SPI wiring.

### I2Cs

I2C stands for inter-integrated circuit and is similar to SPI but requires fewer pins: serial data (SDA) and serial clock (SCL).
Some boards that support I2C have the SDA and SCL pins configured by default, so in your config file you need only specify which I2C bus you are using.
For example, if you use I2C bus 1 on a Raspberry Pi 4, SDA and SCL will be pins 3 and 5, respectively.
You will also need to enable I2C on your board if it is not enabled by default.
Review the [instructions in our documentation](/installation/prepare/rpi-setup/#enable-communication-protocols) to learn how to enable I2C on a Raspberry Pi 4.
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
|`name`| string|--| Choose a name for the I2C bus. Note that a component that uses this bus must then have this same name configured in its attributes.
|`bus`| string|--| Usually a number. Raspberry Pi recommends using bus `1`. See your board's data sheet for specifics on its I2C wiring.

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}

## Next Steps

{{< cards >}}
  {{% card link="/tutorials/get-started/make-an-led-blink-with-the-viam-app" size="small" %}}
{{< /cards >}}
