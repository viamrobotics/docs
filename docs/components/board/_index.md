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
| [`nanopi`](nanopi) | [FriendlyElec’s NanoPi Mini Board](https://www.friendlyelec.com/index.php?route=product/category&path=69) |
| [`numato`](numato) | [Numato GPIO Modules](https://numato.com/product-category/automation/gpio-modules/), peripherals for adding [GPIO pins](#gpio-pins) |
| [`pca9685`](pca9685) | [PCA9685 Arduino I2C Interface](https://www.adafruit.com/product/815), a 16-channel [I2C](#i2cs) [servo](/components/servo) driver peripheral |
| [`fake`](fake) | A model used for testing, with no physical hardware. |
<!-- Could consider adding another column for Pi, Jetsons, TI -> PINOUT diagram section? 

- https://pinout.xyz/pinout/spi 
- https://jetsonhacks.com/nvidia-jetson-nano-j41-header-pinout/

 TODO: needs a better intro here 
 -->

### `analogs`

An [analog-to-digital converter](https://www.electronics-tutorials.ws/combination/analogue-to-digital-converter.html) (ADC) takes a voltage input (analog signal) and converts it to an integer output (digital signal).
ADCs are quite useful when building a robot, as they allow your board to be able to read the analog signals output by most types of [sensor](/components/sensor/) and other hardware components.

- To integrate an ADC into your robot, you must physically connect the pins on your ADC and on your board.
- A [breadboard](https://learn.sparkfun.com/tutorials/how-to-use-a-breadboard/all) is useful and wiring with [SPI](#spis) is often necessary for the two devices to be able to communicate.

Then, configure this connection in the `"attributes"` of your board as follows:

{{< tabs name="Configure an Analog Reader" >}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
// "attributes": { ... ,
"analogs": [
  {
    "chip_select": <"chip-select-pin-number-on-board">,
    "name": <"your-analog-reader-name">,
    "pin": <"pin-number-on-adc">,
    "spi_bus": <"your-spi-bus-name">
  }
]
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "model": "pi",
      "name": "your-board",
      "type": "board",
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
      }
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

The following properties are available for `analogs`:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
|`name` | string | **Required** | Your name for the analog reader. |
|`pin`| string | **Required** | The pin number of the ADC's connection pin, wired to the board.
|`chip_select`| string | **Required** | The pin number of the board's connection pin, wired to the ADC. |
|`spi_bus` | string | Optional | `name` of the [SPI bus](#spi) connecting the ADC and board. Required if your board must communicate with the ADC with the SPI protocol. |
| `average_over_ms` | int | Optional | Duration in milliseconds over which the rolling average of the analog input should be taken. |
|`samples_per_sec` | int | Optional | Sampling rate of the analog input in samples per second. |

### `digital_interrupts`

Digital interrupts are useful when your application needs to know precisely when there is a change in GPIO value between high and low.

- When an interrupt configured on your board processes a change in the state of the GPIO pin it is configured to monitor, it "knocks on the door" with [`Tick()`](#tick).
- Calling [`Get()`](#get) on a GPIO pin, which you can do without configuring interrupts, is great when you want to know a pin's value at specific points, but is less precise and convenient than using an interrupt.

Integrate `digital_interrupts` into your robot in the `attributes` of your board as follows:

{{< tabs name="Configure a Digital Interrupt" >}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
// "attributes": { ... ,
"digital_interrupts": [
  {
    "name": <"your-digital-interrupt-name">,
    "pin": <pin-number>
  }
]
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "model": "pi",
      "name": "your-board",
      "type": "board",
      "attributes": {
        "digital_interrupts": [
          {
            "name": "your-interrupt-1",
            "pin": "15"
          },
          {
            "name": "your-interrupt-2",
            "pin": "16"
          }
        ]
      }
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

The following properties are available for `digital_interrupts`:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
|`name` | string | **Required** | Your name for the digital interrupt. |
|`pin`| string | **Required** | The pin number of the board's GPIO pin that you wish to configure the digital interrupt for. |
|`type`| string | Optional | <ul><li>`basic`: Recommended. Tracks interrupt count. </li> <li>`servo`: For interrupts configured for a pin controlling a [servo](/components/servo). Tracks pulse width value. </li></ul> |

### `spis`

[Serial Peripheral Interface (SPI)](https://en.wikipedia.org/wiki/Serial_Peripheral_Interface) is a serial communication protocol that uses four [signal wires](https://learn.sparkfun.com/tutorials/serial-peripheral-interface-spi) to exchange information between a controller and peripheral devices:

- Main Out/Secondary In: MOSI
- Main In/Secondary Out: MISO
- Clock, an oscillating signal line: SCLK
- Chip Select, with 1 line for each peripheral connected to controller: CS*

To connect your board (controller) and a [component](/components) that requires SPI communication (peripheral device), wire a connection between CS and MOSI/MISO/SLCK pins on the board and component.

{{% alert title="Caution" color="caution" %}}

You must also enable SPI on your board if it is not enabled by default.
See your [board model's configuration instructions](#configuration) if applicable.

{{% /alert %}}

As supported boards have CS pins internally configured to correspond with SPI bus indices, you can enable this connection in your board's configuration by specifying the index of the bus at your CS pin's location and giving it a name.

Integrate `spis` into your robot in the `attributes` of your board as follows:

{{< tabs name="Configure a SPI Bus" >}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
// "attributes": { ... ,
"spis": [
  {
    "name": <"your-bus-name">,
    "bus_select": <"index">
  }
]
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
"spis": [
  {
    "name": "main",
    "bus_select": "0"
  }
]
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `spis`:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
|`name`| string| Required | `name` of the SPI bus. |
|`bus_select`| string | Required | The index of the SPI bus. Refer to your board's pinout diagram for SPI bus indexes and chip select pin numbers. |

{{% alert title="WIRING WITH SPI" color="tip" %}}

Refer to your board's pinout diagram or data sheet for SPI bus indexes and corresponding CS/MOSI/MISO/SCLK pin numbers.

Refer to your peripheral device's data sheet for CS/MOSI/MISO/SLCK pin layouts.

{{% /alert %}}

### `i2cs`

The [Inter-Integrated circuit (I2C)](https://learn.sparkfun.com/tutorials/i2c/all) serial communication protocol is similar to SPI, but requires only two signal wires to exchange information between a controller and a peripheral device:

- Serial Data: SDA
- Serial Clock: SCL

To connect your board (controller) and a [component](/components) that requires I2C communication (peripheral device), wire a connection between SDA and SCL pins on the board and component.

{{% alert title="Caution" color="caution" %}}

You must also enable I2C on your board if it is not enabled by default.
See your [board model's configuration instructions](#configuration) if applicable.

{{% /alert %}}

As supported boards have SDA and SCL pins internally configured to correspond with I2C bus indices, you can enable this connection in your board's configuration by specifying the index of the bus and giving it a name.

Integrate `i2cs` into your robot in the `attributes` of your board as follows:

```json {class="line-numbers linkable-line-numbers"}
// "attributes": { ... ,
{
  "i2cs": [
    {
      "name": "bus1",
      "bus": "1"
    }
  ]
}
```

The following properties are available for `i2cs`:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
|`name`| string| Required | `name` of the I2C bus. |
|`bus_select`| int | Required | The index of the I2C bus. |

{{% alert title="WIRING WITH I2C" color="tip" %}}

Refer to your board's pinout diagram or data sheet for I2C bus indexes and corresponding SDA/SCL pin numbers.

Refer to your peripheral device's data sheet for SDA/SCL pin layouts.

{{% /alert %}}

## Control your board with Viam's client SDK libraries

To get started using Viam's SDKs to connect to and control your robot, go to your robot's page on [the Viam app](https://app.viam.com), navigate to the **code sample** tab, select your preferred programming language, and copy the sample code generated.

When executed, this sample code will create a connection to your robot as a client.
Then control your robot programmatically by getting your `board` component from the robot with `FromRobot` and adding API method calls, as shown in the following examples.

These examples assume you have a board called "my_board" configured as a component of your robot.
If your board has a different name, change the `name` in the code.

## API

The board component supports the following methods:

| Method Name | Description |
| ----------- | ----------- |
| [AnalogReaderByName](#analogreaderbyname) | Get an [`AnalogReader`](#analogs) by `name`. |
| [DigitalInterruptByName](#digitalinterruptbyname) | Get a [`DigitalInterrupt`](#digital_interrupts) by `name`. |
| [GPIOPinByName](#gpiopinbyname) | Get a `GPIOPin` by `name`. |
| [AnalogReaderNames](#analogreadernames) | Get the `name` of every [`AnalogReader`](#analogs). |
| [DigitalInterruptNames](#digitalinterruptnames) | Get the `name` of every [`DigitalInterrupt`](#digital_interrupts). |
| [Status](#status) | Get the current status of this board. |
| [ModelAttributes](#modelattributes) | Get the attributes related to the model of this board. |
| [SetPowerMode](#setpowermode) | Set the board to the indicated power mode. |

Additionally, the nested `GPIOPin`, `AnalogReader`, and `DigitalInterrupt` interfaces support the following methods:

| [`GPIOPin` API](#gpiopin-api) | [`AnalogReader` API](#analogreader-api) | [`DigitalInterrupt` API](#digitalinterrupt-api) |
|--|--|--|
|<table> <tr><th>Method Name</th><th>Description</th></tr><tr><td>[Set](#set)</td><td>...</td></tr><tr><td>[Get](#get)</td><td>....</td></tr><tr><td>[PWM](#getpwm)</td><td>...</td></tr><tr><td>[SetPWM](#setpwm)</td><td>...</td></tr><tr><td>[PWMFreq](#pwmfreq)</td><td>...</td></tr><tr><td>[SetPWMFreq](#setpwmfreq)</td><td>...</td></tr> </table>| <table> <tr><th>Method Name</th><th>Description</th></tr><tr><td>[Read](#read)</td><td>...</td></tr> </table>| <table> <tr><th>Method Name</th><th>Description</th></tr><tr><td>[Value](#value)</td><td>...</td></tr><tr><td>[Tick](#tick)</td><td>...</td></tr><tr><td>[AddCallback](#addcallback)</td><td>...</td></tr><tr><td>[AddPostProcessor](#addpostprocessor)</td><td>...</td></tr> </table>|

### AnalogReaderByName

Get an [`AnalogReader`](#analogs) by `name.`

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `name` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Name of the analog reader you want to retrieve.

**Returns:**

- `reader` [(AnalogReader)](https://python.viam.dev/autoapi/viam/components/board/index.html#viam.components.board.Board.AnalogReader): An interface representing an analog reader configured and residing on the board.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/index.html#viam.components.board.Board.analog_reader_by_name).

```python
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the AnalogReader "my_example_analog_reader".
reader = await my_board.analog_reader_by_name(name="my_example_analog_reader")
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `name` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Name of the analog reader you want to retrieve. Set as the `"name"` property [in configuration](/components/board/#digital_interrupts).

**Returns:**

- `reader` [(AnalogReader)](https://pkg.go.dev/go.viam.com/rdk/components/board#AnalogReader): An interface representing an analog reader configured and residing on the board.
- `ok` [(bool)](https://pkg.go.dev/builtin#bool): True if there was an analog reader of this `name` found on your board.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#Board).

```go
myBoard, err := board.FromRobot(robot, "my_board")

reader, err := myBoard.AnalogReaderByName("my_example_analog_reader")
```

{{% /tab %}}
{{< /tabs >}}

### DigitalInterruptByName

Get an [`DigitalInterrupt`](#digital_interrupts) by `name.`

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `name` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Name of the digital interrupt you want to retrieve. Set as the `"name"` property [in configuration](/components/board/#digital_interrupts).

**Returns:**

- `interrupt` [(DigitalInterrupt)](https://python.viam.dev/_modules/viam/components/board/board.html#Board.DigitalInterrupt): An interface representing a configured interrupt on the board.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/index.html#viam.components.board.Board.digital_interrupt_by_name).

```python
my_board = Board.from_robot(robot=robot, name=

)

# Get the DigitalInterrupt "my_example_digital_interrupt".
interrupt = await my_board.digital_interrupt_by_name(name="my_example_digital_interrupt")
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `name` [(string)](https://pkg.go.dev/builtin#string): Name of the digital interrupt you want to retrieve. Set as the `"name"` property [in configuration](/components/board/#digital_interrupts).

**Returns:**

- `interrupt` [(DigitalInterrupt)](https://pkg.go.dev/go.viam.com/rdk/components/board#DigitalInterrupt): An interface representing a configured interrupt on the board.
- `ok` [(bool)](https://pkg.go.dev/builtin#bool): True if there was a digital interrupt of this `name` found on your board.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#Board).

```go
myBoard, err := board.FromRobot(robot, "my_board")

interrupt, ok := myBoard.DigitalInterruptByName("my_example_digital_interrupt")
```

{{% /tab %}}
{{< /tabs >}}

### GPIOPinByName

Get a `GPIOPin` by its pin number.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `name` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Pin number (NOT GPIO number) of the GPIOPin you want to retrieve. Refer to [the pinout diagram](#configuration) and data sheet of your board model for pin numbers and orientation.

**Returns:**

- `pin` [(GPIOPin)](https://python.viam.dev/_modules/viam/components/board/board.html#Board.GPIOPin): An interface representing an individual GPIO pin on the board.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/index.html#viam.components.board.Board.gpio_pin_by_name).

```python
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the GPIOPin with Pin Number 15 (GPIO 22 on Raspberry Pi 4).
pin = await my_board.GPIO_pin_by_name(name="15")
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `name` [(string)](https://pkg.go.dev/builtin#string): Pin number (NOT GPIO number) of the GPIOPin you want to retrieve. Refer to [the pinout diagram](#configuration) and data sheet of your board model for pin numbers and orientation.

**Returns:**

- `pin` [(GPIOPin)](https://pkg.go.dev/go.viam.com/rdk/components/board#GPIOPin): An interface representing an individual GPIO pin on the board.
- `error` [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#Board).

```go
myBoard, err := board.FromRobot(robot, "my_board")

// Get the GPIOPin with Pin Number 15 (GPIO 22 on Raspberry Pi 4).
pin, err := myBoard.GPIOPinByName("15")
```

{{% /tab %}}
{{< /tabs >}}

### AnalogReaderNames

Get the name of every [`AnalogReader`](#analogs) configured and residing on the board.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- `names` [(List[str])](https://docs.python.org/3/library/stdtypes.html#typesseq-list): An list containing the `"name"` of every analog reader [configured](#configuration) on the board.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/index.html#viam.components.board.Board.analog_reader_names).

```python
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the name of every AnalogReader configured on the board.
names = await my_board.analog_reader_by_name()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- None

**Returns:**

- `names` [([]string)](https://go.dev/tour/moretypes/7): An slice containing the `"name"` of every analog reader [configured](#configuration) on the board.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#Board).

```go
myBoard, err := board.FromRobot(robot, "my_board")

// Get the name of every AnalogReader configured on the board.
names := myBoard.AnalogReaderNames()
```

{{% /tab %}}
{{< /tabs >}}

### DigitalInterruptNames

Get the name of every [`DigitalInterrupt`](#digital_interrupts) configured on the board.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- `names` [(List[str])](https://docs.python.org/3/library/stdtypes.html#typesseq-list): An list containing the `"name"` of every interrupt [configured](#configuration) on the board.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/index.html#viam.components.board.Board.digital_interrupt_names).

```python
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the name of every DigitalInterrupt configured on the board.
names = await my_board.digital_interrupt_names()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- None

**Returns:**

- `names` [([]string)](https://go.dev/tour/moretypes/7): An slice containing the `"name"` of every interrupt [configured](#configuration) on the board.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#Board).

```go
myBoard, err := board.FromRobot(robot, "my_board")

// Get the name of every DigitalInterrupt configured on the board.
names := myBoard.DigitalInterruptNames()
```

{{% /tab %}}
{{< /tabs >}}

### Status

Get the current status of the board as a `BoardStatus`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional[Dict[str, Any]])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional[float])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- `status` [(BoardStatus)](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.BoardStatus): Mappings of the current status of the fields and values of any [AnalogReaders](#analogs) and [DigitalInterrupts](#digital_interrupts) configured on the board.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/index.html#viam.components.board.Board.status).

```python
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the current status of the board.
status = await my_board.status()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `Context` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- `status` [(BoardStatus)](https://pkg.go.dev/go.viam.com/api/common/v1#BoardStatus): Mappings of the current status of the fields and values of any [AnalogReaders](#analogs) and [DigitalInterrupts](#digital_interrupts) configured on the board.
- `error` [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#Board).

```go
myBoard, err := board.FromRobot(robot, "my_board")

// Get the current status of the board.
status, err := myBoard.Status(context.Background(), nil)
```

{{% /tab %}}
{{< /tabs >}}

### ModelAttributes

Get a struct with the board's innate `Remote` attribute indicating whether or not this model of board is accessed over a remote connection, e.g gRPC.

### SetPowerMode

Set the board to the indicated `PowerMode`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `mode` [(PowerMode)](https://python.viam.dev/autoapi/viam/proto/component/board/index.html#viam.proto.component.board.PowerMode): Options to specify power usage of the board: `PowerMode.POWER_MODE_UNSPECIFIED`, `PowerMode.POWER_MODE_NORMAL`, and `PowerMode.POWER_MODE_OFFLINE_DEEP`.
- `extra` [(Optional[Dict[str, Any]])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `duration` [(Optional[datetime.timedelta])](https://docs.python.org/3/library/typing.html#typing.Optional): If provided, the board will exit the given power mode after the specified duration.
- `timeout` [(Optional[float])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/index.html#viam.components.board.Board.set_power_mode).

```python
my_board = Board.from_robot(robot=robot, name="my_board")

# Set the power mode of the board to OFFLINE_DEEP.
status = await my_board.set_power_mode(mode=PowerMode.POWER_MODE_OFFLINE_DEEP)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `Context` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `mode` [(PowerMode)](https://pkg.go.dev/go.viam.com/api/component/board/v1#PowerMode): Options to specify power usage of the board: `boardpb.PowerMode_POWER_MODE_UNSPECIFIED`, `boardpb.PowerMode_POWER_MODE_NORMAL`, and `boardpb.PowerMode_POWER_MODE_OFFLINE_DEEP`.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.
- `duration` [(*time.Duration)](https://pkg.go.dev/time#Duration): If provided, the board will exit the given power mode after the specified duration.

**Returns:**

- `error` [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#Board).

```go
myBoard, err := board.FromRobot(robot, "my_board")

// Set the power mode of the board to OFFLINE_DEEP.
err := myBoard.Status(context.Background(), nil)
myBoard.SetPowerMode(context.Background(), boardpb.PowerMode_POWER_MODE_OFFLINE_DEEP, nil)
```

{{% /tab %}}
{{< /tabs >}}

## `GPIOPin` API

### Set

Set the digital signal output of this pin to either low (0V) or high (active, >0V).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `high` [(bool)](https://docs.python.org/3/library/stdtypes.html#bltin-boolean-values): If `true`, set the state of the pin to high.
If `false`, set the state of the pin to low.
- `extra` [(Optional[Dict[str, Any]])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional[float])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/index.html#viam.components.board.Board.GPIOPin.set).

```python
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the GPIOPin with Pin Number 15 (GPIO 22 on Raspberry Pi 4).
pin = await my_board.GPIO_pin_by_name(name="15")

# Set the pin to high.
await pin.set(high="true")
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `Context` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `high` [(bool)](https://pkg.go.dev/builtin#bool): If `true`, set the state of the pin to high.
If `false`, set the state of the pin to low.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- `error` [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#GPIOPin).

```go
myBoard, err := board.FromRobot(robot, "my_board")

// Get the GPIOPin with Pin Number 15 (GPIO 22 on Raspberry Pi 4).
pin, err := myBoard.GPIOPinByName("15")

// Set the pin to high.
err := pin.Set(context.Background(), "true", nil)
```

{{% /tab %}}
{{< /tabs >}}

### Get

Get if it's `true` that the digital signal output of this pin is set to high (active, >0V).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional[Dict[str, Any]])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional[float])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- `high` [(bool)](https://docs.python.org/3/library/stdtypes.html#bltin-boolean-values): If `true`, the state of the pin is set to high.
If `false`, the state of the pin is set to low.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/index.html#viam.components.board.Board.GPIOPin.get).

```python
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the GPIOPin with Pin Number 15 (GPIO 22 on Raspberry Pi 4).
pin = await my_board.GPIO_pin_by_name(name="15")

# Get if it is true or false that the pin is set to high.
high = await pin.get()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `Context` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- `high` [(bool)](https://pkg.go.dev/builtin#bool): If `true`, the state of the pin is set to high.
If `false`, the state of the pin is set to low.
- `error` [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#GPIOPin).

```go
myBoard, err := board.FromRobot(robot, "my_board")

// Get the GPIOPin with Pin Number 15 (GPIO 22 on Raspberry Pi 4).
pin, err := myBoard.GPIOPinByName("15")

// Get if it is true or false that the pin is set to high.
high := pin.Get(context.Background(), nil)
```

{{% /tab %}}
{{< /tabs >}}

### PWM

{{% alert title="Note" color="note" %}}

[Pulse Width Modulation (PWM)](https://www.digikey.com/en/blog/pulse-width-modulation) is a method where of transmitting a digital signal in the form of pulses to control analog circuits.
With PWM on a *board*, the continuous digital signal output by a GPIO pin is sampled at regular intervals and transmitted to any [hardware components](/components) wired to the pin that read analog signals.
This enables the board to communicate with these components.

{{% /alert %}}

Get the pin's [Pulse Width Modulation (PWM) duty cycle](https://learn.sparkfun.com/tutorials/pulse-width-modulation/duty-cycle): a float [`0.0`, `1.0`] representing the percentage of time the digital signal output by this pin is in the "high" state (active, >0V) relative to the interval period of the PWM signal [(interval period being the mathematical inverse of the PWM frequency)](https://learn.adafruit.com/improve-brushed-dc-motor-performance/pwm-frequency).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional[Dict[str, Any]])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional[float])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- `duty_cycle` [(float)](https://docs.python.org/3/library/functions.html#float): A float [`0.0`, `1.0`] representing the percentage of time the digital signal output by this pin is in the "high" state relative to the interval period of the PWM signal.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/index.html#viam.components.board.Board.GPIOPin.get_pwm).

```python
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the GPIOPin with Pin Number 15 (GPIO 22 on Raspberry Pi 4).
pin = await my_board.GPIO_pin_by_name(name="15")

# Get if it is true or false that the pin is set to high.
duty_cycle = await pin.get_pwm()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `Context` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- `duty_cycle` [(float64)](https://pkg.go.dev/builtin#float64): A float [`0.0`, `1.0`] representing the percentage of time the digital signal output by this pin is in the "high" state relative to the interval period of the PWM signal.
- `error` [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#GPIOPin).

```go
myBoard, err := board.FromRobot(robot, "my_board")

// Get the GPIOPin with Pin Number 15 (GPIO 22 on Raspberry Pi 4).
pin, err := myBoard.GPIOPinByName("15")

// Get if it is true or false that the pin is set to high.
duty_cycle := pin.PWM(context.Background(), nil)
```

{{% /tab %}}
{{< /tabs >}}

### SetPWM

Set the pin's [Pulse Width Modulation (PWM) duty cycle](https://learn.sparkfun.com/tutorials/pulse-width-modulation/duty-cycle): a float [`0.0`, `1.0`] indicating the percentage of time the digital signal output of this pin is in the "high" state (active, >0V) relative to the interval period of the PWM signal [(interval period being the mathematical inverse of the PWM frequency)](https://learn.adafruit.com/improve-brushed-dc-motor-performance/pwm-frequency).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `cycle` [(float64)](https://pkg.go.dev/builtin#float64): A float [`0.0`, `1.0`] representing the percentage of time the digital signal output by this pin is in the "high" state relative to the interval period of the PWM signal.
- `extra` [(Optional[Dict[str, Any]])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional[float])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- `high` [(bool)](https://docs.python.org/3/library/stdtypes.html#bltin-boolean-values): If `true`, the state of the pin is set to high.
If `false`, the state of the pin is set to low.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/index.html#viam.components.board.Board.GPIOPin.set_pwm).

```python
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the GPIOPin with Pin Number 15 (GPIO 22 on Raspberry Pi 4).
pin = await my_board.GPIO_pin_by_name(name="15")

# Set the duty cycle to .6, meaning that this pin will be set to high for 60% of the duration of the PWM interval period.
await pin.set_pwm(cycle=.6)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `Context` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `cycle` [(float64)](https://pkg.go.dev/builtin#float64): A float [`0.0`, `1.0`] representing the percentage of time the digital signal output by this pin is in the "high" state relative to the interval period of the PWM signal.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- `error` [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#GPIOPin).

```go
myBoard, err := board.FromRobot(robot, "my_board")

// Get the GPIOPin with Pin Number 15 (GPIO 22 on Raspberry Pi 4).
pin, err := myBoard.GPIOPinByName("15")

// Set the duty cycle to .6, meaning that this pin will be set to high for 60% of the duration of the PWM interval period.
err := pin.SetPWM(context.Background(), .6, nil)
```

{{% /tab %}}
{{< /tabs >}}

### PWMFreq

Get the [Pulse Width Modulation (PWM) Frequency](https://learn.adafruit.com/improve-brushed-dc-motor-performance/pwm-frequency) in Hertz (Hz) of this pin, the count of PWM interval periods per second.
The optimal value for PWM Frequency depends on the type and model of [component](/components) you control with the signal output by this pin.
Refer to your device's data sheet for PWM Frequency specifications.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional[Dict[str, Any]])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional[float])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- `frequency` [(int)](https://docs.python.org/3/library/functions.html#int): The PWM Frequency in Hertz (Hz) (the count of PWM interval periods per second) the digital signal output by this pin is set to.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/index.html#viam.components.board.Board.GPIOPin.get_pwm_frequency).

```python
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the GPIOPin with Pin Number 15 (GPIO 22 on Raspberry Pi 4).
pin = await my_board.GPIO_pin_by_name(name="15")

# Get the PWM frequency of this pin.
freq = await pin.get_pwm_frequency()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `Context` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- `freqHz` [(unit)](https://pkg.go.dev/builtin#uint): The PWM Frequency in Hertz (Hz) (the count of PWM interval periods per second) the digital signal output by this pin is set to.
- `error` [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#GPIOPin).

```go
myBoard, err := board.FromRobot(robot, "my_board")

// Get the GPIOPin with Pin Number 15 (GPIO 22 on Raspberry Pi 4).
pin, err := myBoard.GPIOPinByName("15")

// Get the PWM frequency of this pin.
freqHz, err := pin.PWMFreq(context.Background(), nil)
```

{{% /tab %}}
{{< /tabs >}}

### SetPWMFreq

Set the [Pulse Width Modulation (PWM) Frequency](https://learn.adafruit.com/improve-brushed-dc-motor-performance/pwm-frequency) in Hertz (Hz) of this pin, the count of PWM interval periods per second.
The optimal value for PWM Frequency depends on the type and model of [component](/components) you control with the PWM signal output by this pin.
Refer to your device's data sheet for PWM Frequency specifications.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional[Dict[str, Any]])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional[float])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- `frequency` [(int)](https://docs.python.org/3/library/functions.html#int)The PWM Frequency in Hertz (Hz), the count of PWM interval periods per second, to set the digital signal output by this pin to.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/index.html#viam.components.board.Board.GPIOPin.set_pwm_frequency).

```python
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the GPIOPin with Pin Number 15 (GPIO 22 on Raspberry Pi 4).
pin = await my_board.GPIO_pin_by_name(name="15")

# Set the PWM frequency of this pin to 1600 Hz.
high = await pin.set_pwm_frequency(frequency=1600)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `Context` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `freqHz` [(unit)](https://pkg.go.dev/builtin#uint): The PWM Frequency in Hertz (Hz), the count of PWM interval periods per second, to set the digital signal output by this pin to.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- `error` [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#GPIOPin).

```go
myBoard, err := board.FromRobot(robot, "my_board")

// Get the GPIOPin with Pin Number 15 (GPIO 22 on Raspberry Pi 4).
pin, err := myBoard.GPIOPinByName("15")

// Set the PWM frequency of this pin to 1600 Hz.
high := pin.SetPWMFreq(context.Background(), 1600, nil)
```

{{% /tab %}}
{{< /tabs >}}

## `AnalogReader` API

### Read

Read the current integer value of the digital signal output by the [AnalogReader](#analogs).

## `DigitalInterrupt` API

### Value

Get the current value of this interrupt.
If a post processor function has been added with [`AddPostProcessor()`](#addpostprocessor), it will be applied to this value before it is returned.

Calculation of value differs between the `"type"` of interrupt [configured](#digital_interrupts):

{{< tabs >}}
{{% tab name="Basic" %}}
{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional[Dict[str, Any]])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional[float])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- `count` [(int)](https://docs.python.org/3/library/functions.html#int) The amount of [Ticks](#tick) that have occurred.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/index.html#viam.components.board.Board.DigitalInterrupt.value).

```python
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the DigitalInterrupt "my_example_digital_interrupt".
interrupt = await my_board.digital_interrupt_by_name(name="my_example_digital_interrupt")

# Get the amount of times this DigitalInterrupt has been interrupted with a tick.
count = await interrupt.value()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `Context` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- `count` [(int64)](https://pkg.go.dev/builtin#int64): The amount of [Ticks](#tick) that have occurred.
- `error` [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#BasicDigitalInterrupt).

```go
myBoard, err := board.FromRobot(robot, "my_board")

// Get the DigitalInterrupt "my_example_digital_interrupt".
interrupt, ok := myBoard.DigitalInterruptByName("my_example_digital_interrupt")

// Get the amount of times this DigitalInterrupt has been interrupted with a tick.
count, err := interrupt.Value(context.Background(), nil)
```

{{% /tab %}}
{{< /tabs >}}
{{% /tab %}}
{{% tab name="Servo" %}}
{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional[Dict[str, Any]])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional[float])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- `rolling_avg` [(int)](https://docs.python.org/3/library/functions.html#int) The [RollingAverage](https://pkg.go.dev/go.viam.com/rdk/utils#RollingAverage) of the time in nanoseconds between two successive low signals (pulse width) recorded by [`Tick()`](#tick), computed over a window of size `10`.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/index.html#viam.components.board.Board.DigitalInterrupt.value).

```python
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the DigitalInterrupt "my_example_digital_interrupt".
interrupt = await my_board.digital_interrupt_by_name(name="my_example_digital_interrupt")

# Get the rolling average of the pulse width across each time the DigitalInterrupt is interrupted with a tick.
rolling_avg = await interrupt.value()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `Context` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- `rolling_avg`[(int64)](https://pkg.go.dev/builtin#int64): The [RollingAverage](https://pkg.go.dev/go.viam.com/rdk/utils#RollingAverage) of the time in nanoseconds between two successive low signals (pulse width) recorded by [`Tick()`](#tick), computed over a window of size `10`.
- `error` [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#ServoDigitalInterrupt).

```go
myBoard, err := board.FromRobot(robot, "my_board")

// Get the DigitalInterrupt "my_example_digital_interrupt".
interrupt, ok := myBoard.DigitalInterruptByName("my_example_digital_interrupt")

// Get the rolling average of the pulse width across each time the DigitalInterrupt is interrupted with a tick.
rolling_avg, err := interrupt.Value(context.Background(), nil)
```

{{% /tab %}}
{{< /tabs >}}
{{% /tab %}}
{{< /tabs >}}

### Tick

{{% alert title="Caution" color="caution" %}}
You should only need to integrate this method into your application code for testing purposes, as the handling of `Tick()` should be automated once the interrupt is configured.
{{% /alert %}}

Record an interrupt.

The way `Tick()` is triggered differs between the `type` of interrupt [configured](#digital_interrupts):

{{< tabs >}}
{{% tab name="Basic" %}}
{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `high` [(bool)](https://docs.python.org/3/library/stdtypes.html#bltin-boolean-values): If `true`, the state of the pin is set to high, and the [`Value()`](#value) of the interrupt should increase.
If `false`, the state of the pin is set to low.
- `nanos` [(int)](https://docs.python.org/3/library/functions.html#int): The time that has elapsed in nanoseconds since the last time the interrupt was ticked.

**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/index.html#viam.components.board.Board.DigitalInterrupt.tick).

```python
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the DigitalInterrupt "my_example_digital_interrupt".
interrupt = await my_board.digital_interrupt_by_name(name="my_example_digital_interrupt")

# Record an interrupt and notify any interested callbacks.
await interrupt.tick(high=true, nanos=12345)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `Context` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `high` [(bool)](https://pkg.go.dev/builtin#bool): If `true`, the state of the pin is set to high, and the [`Value()`](#value) of the interrupt should increase.
If `false`, the state of the pin is set to low.
- `now` [(uint64)](https://pkg.go.dev/builtin#uint64): The time that has elapsed in nanoseconds since the last time the interrupt was ticked.

**Returns:**

- `error` [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#BasicDigitalInterrupt).

```go
myBoard, err := board.FromRobot(robot, "my_board")

// Get the DigitalInterrupt "my_example_digital_interrupt".
interrupt, ok := myBoard.DigitalInterruptByName("my_example_digital_interrupt")

// Record an interrupt and notify any interested callbacks.
count, err := interrupt.Tick(context.Background(), true, 12345)
```

{{% /tab %}}
{{< /tabs >}}
{{% /tab %}}
{{% tab name="Servo" %}}
{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `high` [(bool)](https://docs.python.org/3/library/stdtypes.html#bltin-boolean-values): If `true`, the state of the pin is set to high.
If `false`, the state of the pin is set to low.
- `nanos` [(int)](https://docs.python.org/3/library/functions.html#int): The time in nanoseconds between two successive low signals (pulse width).

**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/index.html#viam.components.board.Board.DigitalInterrupt.tick).

```python
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the DigitalInterrupt "my_example_digital_interrupt".
interrupt = await my_board.digital_interrupt_by_name(name="my_example_digital_interrupt")

# Record an interrupt and notify any interested callbacks.
await interrupt.tick(high=true, nanos=12345)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `Context` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `high` [(bool)](https://pkg.go.dev/builtin#bool): If `true`, the state of the pin is set to high.
If `false`, the state of the pin is set to low.
- `nanoseconds` [(uint64)](https://pkg.go.dev/builtin#uint64): The time in nanoseconds between two successive low signals (pulse width).

**Returns:**

- `error` [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#ServoDigitalInterrupt).

```go
myBoard, err := board.FromRobot(robot, "my_board")

// Get the DigitalInterrupt "my_example_digital_interrupt".
interrupt, ok := myBoard.DigitalInterruptByName("my_example_digital_interrupt")

// Record an interrupt and notify any interested callbacks.
err := interrupt.Tick(context.Background(), true, 12345)
```

{{% /tab %}}
{{< /tabs >}}
{{% /tab %}}
{{< /tabs >}}

### AddCallback

Add a callback function to be sent the boolean value `high` returned by a call to `Tick()`.
When interrupted, this interrupt should call all callbacks that have been added with this method.

### AddPostProcessor

<!-- TODO: Will do something with this but not in this format. API documentation may be sufficient. Could make subpage.  -->

<!-- #### GPIO

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
{{< /tabs >}} -->

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}

## Next Steps

{{< cards >}}
  {{% card link="/tutorials/get-started/make-an-led-blink-with-the-viam-app" size="small" %}}
{{< /cards >}}
