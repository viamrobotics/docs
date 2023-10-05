---
title: "Board Component"
linkTitle: "Board"
childTitleEndOverwrite: "Board Component"
weight: 20
type: "docs"
no_list: true
description: "The signal wire hub of a robot, with GPIO pins for transmitting signals between the robot's computer and its other components."
tags: ["board", "components"]
icon: "/icons/components/board.svg"
images: ["/icons/components/board.svg"]
# SMEs: Gautham, Rand
---

A _board_ component on your robot communicates with the other [components](/components/) of the robot.

A board can be:

- A single-board computer (SBC) with GPIO pins and a CPU capable of running `viam-server`.
- A GPIO peripheral device that must connect to an external computer.
- A PWM peripheral device that must connect to an SBC that has a CPU and GPIO pins.

The board of a robot is also its signal wire hub that provides access to general purpose input/output [(GPIO)](https://www.howtogeek.com/787928/what-is-gpio/) pins: a collection of pins on the motherboard of a computer that can receive electrical signals.

Signaling is overseen by a computer running `viam-server` which allows you to control the flow of electricity to these pins to change their state between "high" (active) and "low" (inactive), and wire them to send [digital signals](https://en.wikipedia.org/wiki/Digital_signal) to and from other hardware.

{{% figure src="/components/board/board-comp-options.png" alt="Image showing two board options: First, running viam-server locally and second, running via a peripheral plugged into the USB port of a computer that is running the viam-server." title="Two different board options: a single-board computer with GPIO pins running `viam-server` locally, or a GPIO peripheral plugged into a desktop computer's USB port, with the computer running `viam-server`." %}}

## Supported Models

To use your base with Viam, check whether one of the following [built-in models](#built-in-models) or [modular resources](#modular-resources) supports your base.

{{< readfile "/static/include/create-your-own-mr.md" >}}

### Built-in models

For configuration information, click on the model name:

<!-- prettier-ignore -->
| Model | Description |
| ----- | ----------- |
| [`pi`](pi/) | [Raspberry Pi 4](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/), [Raspberry Pi 3](https://www.raspberrypi.com/products/raspberry-pi-3-model-b/) or [Raspberry Pi Zero 2 W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/) |
| [`jetson`](jetson/) | [NVIDIA Jetson AGX Orin](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-orin/), [NVIDIA Jetson Orin Nano](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-orin/), [NVIDIA Jetson Xavier NX](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-xavier-nx/), [NVIDIA Jetson Nano](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-nano/) |
| [`upboard`](upboard/) | An Intel-based board like the [UP4000](https://github.com/up-board/up-community/wiki/Pinout_UP4000) |
| [`ti`](ti/) | [Texas Instruments TDA4VM](https://devices.amazonaws.com/detail/a3G8a00000E2QErEAN/TI-TDA4VM-Starter-Kit-for-Edge-AI-vision-systems) |
| [`beaglebone`](beaglebone/) | [BeagleBoard's BeagleBone AI-64](https://www.beagleboard.org/boards/beaglebone-ai-64) |
| [`numato`](numato/) | [Numato GPIO Modules](https://numato.com/product-category/automation/gpio-modules/), peripherals for adding GPIO pins |
| [`pca9685`](pca9685/) | [PCA9685 Arduino I<sup>2</sup>C Interface](https://www.adafruit.com/product/815), a 16-channel [I<sup>2</sup>C](#i2cs) [PWM](https://docs.arduino.cc/learn/microcontrollers/analog-output)/[servo](/components/servo/) driver peripheral |
| [`customlinux`](customlinux/) | A model for other Linux boards. |
| [`fake`](fake/) | A model used for testing, with no physical hardware |

### Modular Resources

{{<modular-resources api="rdk:component:board" type="board">}}

### Micro-RDK

If you are using the micro-RDK, navigate to [Micro-RDK Board](/micro-rdk/board/) for supported model information.

## Attribute Configuration

Configuring these attributes on your board allows you to integrate [analog-to-digital converters](#analogs), [digital interrupts](#digital_interrupts), and components that must communicate through the [SPI](#spis) and [I<sup>2</sup>C](#i2cs) protocols into your robot.

### `analogs`

{{< readfile "/static/include/components/board/board-analogs.md" >}}

### `digital_interrupts`

{{< readfile "/static/include/components/board/board-digital-interrupts.md" >}}

### `spis`

{{< readfile "/static/include/components/board/board-spis.md" >}}

### `i2cs`

{{< readfile "/static/include/components/board/board-i2cs.md" >}}

## Control your board with Viam's client SDK libraries

To get started using Viam's SDKs to connect to and control your robot, go to your robot's page on [the Viam app](https://app.viam.com), navigate to the **Code sample** tab, select your preferred programming language, and copy the sample code generated.

{{% snippet "show-secret.md" %}}

When executed, this sample code will create a connection to your robot as a client.
Then control your robot programmatically by getting your `board` component from the robot with `FromRobot` and adding API method calls, as shown in the following examples.

These examples assume you have a board called "my_board" configured as a component of your robot.
If your board has a different name, change the `name` in the code.

Be sure to import the board package for the SDK you are using:

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.board import Board
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
  "go.viam.com/rdk/components/board"
)
```

{{% /tab %}}
{{< /tabs >}}

## API

The board component supports the following methods:

{{< readfile "/static/include/components/apis/board.md" >}}

Additionally, the nested `GPIOPin`, `AnalogReader`, and `DigitalInterrupt` interfaces support the following methods:

[`GPIOPin`](#gpiopin-api) API:

{{< readfile "/static/include/components/apis/gpiopin.md" >}}

<br>

[`AnalogReader`](#analogreader-api) API:

{{< readfile "/static/include/components/apis/analogreader.md" >}}

<br>

[`DigitalInterrupt`](#digitalinterrupt-api) API:

{{< readfile "/static/include/components/apis/digitalinterrupt.md" >}}

### AnalogReaderByName

Get an [`AnalogReader`](#analogs) by `name`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `name` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Name of the analog reader you want to retrieve.

**Returns:**

- [(AnalogReader)](https://python.viam.dev/autoapi/viam/components/board/index.html#viam.components.board.Board.AnalogReader): An interface representing an analog reader configured and residing on the board.

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

- [(AnalogReader)](https://pkg.go.dev/go.viam.com/rdk/components/board#AnalogReader): An interface representing an analog reader configured and residing on the board.
- [(bool)](https://pkg.go.dev/builtin#bool): True if there was an analog reader of this `name` found on your board.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#Board).

```go
myBoard, err := board.FromRobot(robot, "my_board")

// Get the AnalogReader "my_example_analog_reader".
reader, err := myBoard.AnalogReaderByName("my_example_analog_reader")
```

{{% /tab %}}
{{< /tabs >}}

### DigitalInterruptByName

Get an [`DigitalInterrupt`](#digital_interrupts) by `name`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `name` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Name of the digital interrupt you want to retrieve. Set as the `"name"` property [in configuration](/components/board/#digital_interrupts).

**Returns:**

- [(DigitalInterrupt)](https://python.viam.dev/_modules/viam/components/board/board.html#Board.DigitalInterrupt): An interface representing a configured interrupt on the board.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/index.html#viam.components.board.Board.digital_interrupt_by_name).

```python
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the DigitalInterrupt "my_example_digital_interrupt".
interrupt = await my_board.digital_interrupt_by_name(
    name="my_example_digital_interrupt")
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `name` [(string)](https://pkg.go.dev/builtin#string): Name of the digital interrupt you want to retrieve. Set as the `"name"` property [in configuration](/components/board/#digital_interrupts).

**Returns:**

- [(DigitalInterrupt)](https://pkg.go.dev/go.viam.com/rdk/components/board#DigitalInterrupt): An interface representing a configured interrupt on the board.
- [(bool)](https://pkg.go.dev/builtin#bool): True if there was a digital interrupt of this `name` found on your board.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#Board).

```go
myBoard, err := board.FromRobot(robot, "my_board")

// Get the DigitalInterrupt "my_example_digital_interrupt".
interrupt, ok := myBoard.DigitalInterruptByName("my_example_digital_interrupt")
```

{{% /tab %}}
{{< /tabs >}}

### GPIOPinByName

Get a `GPIOPin` by {{< glossary_tooltip term_id="pin-number" text="pin number" >}}.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `name` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Pin number of the GPIO pin you want to retrieve as a `GPIOPin` interface.
  Refer to the pinout diagram and data sheet of your [board model](#supported-models) for {{< glossary_tooltip term_id="pin-number" text="pin numbers" >}}.

**Returns:**

- [(GPIOPin)](https://python.viam.dev/_modules/viam/components/board/board.html#Board.GPIOPin): An interface representing an individual GPIO pin on the board.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/index.html#viam.components.board.Board.gpio_pin_by_name).

```python
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the GPIOPin with pin number 15.
pin = await my_board.gpio_pin_by_name(name="15")
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `name` [(string)](https://pkg.go.dev/builtin#string): {{< glossary_tooltip term_id="pin-number" text="pin number" >}} of the GPIO pin you want to retrieve as a `GPIOPin` interface.
  Refer to the pinout diagram and data sheet of your [board model](#supported-models) for {{< glossary_tooltip term_id="pin-number" text="pin numbers" >}}.

**Returns:**

- [(GPIOPin)](https://pkg.go.dev/go.viam.com/rdk/components/board#GPIOPin): An interface representing an individual GPIO pin on the board.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#Board).

```go
myBoard, err := board.FromRobot(robot, "my_board")

// Get the GPIOPin with pin number 15.
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

- [(List\[str\])](https://docs.python.org/3/library/stdtypes.html#typesseq-list): A list containing the `"name"` of every analog reader [configured](#supported-models) on the board.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/index.html#viam.components.board.Board.analog_reader_names).

```python
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the name of every AnalogReader configured on the board.
names = await my_board.analog_reader_names()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- None

**Returns:**

- [([]string)](https://go.dev/tour/moretypes/7): A slice containing the `"name"` of every analog reader [configured](#supported-models) on the board.

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

- [(List\[str\])](https://docs.python.org/3/library/stdtypes.html#typesseq-list): A list containing the `"name"` of every interrupt [configured](#supported-models) on the board.

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

- [([]string)](https://go.dev/tour/moretypes/7): A slice containing the `"name"` of every interrupt [configured](#supported-models) on the board.

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

- `extra` [(Optional\[Dict\[str, Any\]\])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(BoardStatus)](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.BoardStatus): Mappings of the current status of the fields and values of any [AnalogReaders](#analogs) and [DigitalInterrupts](#digital_interrupts) configured on the board.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/index.html#viam.components.board.Board.status).

```python
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the current status of the board.
status = await my_board.status()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.
- [(BoardStatus)](https://pkg.go.dev/go.viam.com/api/common/v1#BoardStatus): Mappings of the current status of the fields and values of any [AnalogReaders](#analogs) and [DigitalInterrupts](#digital_interrupts) configured on the board.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#Board).

```go
myBoard, err := board.FromRobot(robot, "my_board")

// Get the current status of the board.
err := myBoard.Status(context.Background(), nil)
```

{{% /tab %}}
{{< /tabs >}}

### ModelAttributes

Get the attributes related to the model of this board.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- [(Attributes)](https://python.viam.dev/autoapi/viam/components/board/index.html#viam.components.board.Board.Attributes): Attributes related to the model of this board.
  Will include the board's innate `remote` attribute, which is not specified in configuration and is a `bool` indicating whether this model of board is accessed over a remote connection like gRPC.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/index.html#viam.components.board.Board.model_attributes).

```python
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the attributes related to the model of this board.
attributes = await my_board.model_attributes()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- None

**Returns:**

- [(ModelAttributes)](https://pkg.go.dev/go.viam.com/rdk/components/board#ModelAttributes): Attributes related to the model of this board.
  Will include the board's innate `remote` attribute, which is not specified in configuration and is a `bool` indicating whether this model of board is accessed over a remote connection like gRPC.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#ModelAttributes).

```go
myBoard, err := board.FromRobot(robot, "my_board")

// Get the attributes related to the model of this board.
attributes := myBoard.ModelAttributes()
```

{{% /tab %}}
{{< /tabs >}}

### SetPowerMode

Set the board to the indicated `PowerMode`.

{{% alert title="Info" color="info" %}}

This method may not receive a successful response from gRPC when you set the board to the offline power mode `PowerMode.POWER_MODE_OFFLINE_DEEP`.

When this is the case for your board model, the call is returned with an error specifying that the remote procedure call timed out or that the endpoint is no longer available.
This is expected: the board has been successfully powered down and can no longer respond to messages.

{{% /alert %}}

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `mode` [(PowerMode)](https://python.viam.dev/autoapi/viam/proto/component/board/index.html#viam.proto.component.board.PowerMode): Options to specify power usage of the board: `PowerMode.POWER_MODE_UNSPECIFIED`, `PowerMode.POWER_MODE_NORMAL`, and `PowerMode.POWER_MODE_OFFLINE_DEEP`.
- `duration` [(Optional\[datetime.timedelta\])](https://docs.python.org/3/library/typing.html#typing.Optional): If provided, the board will exit the given power mode after the specified duration.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

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

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `mode` [(PowerMode)](https://pkg.go.dev/go.viam.com/api/component/board/v1#PowerMode): Options to specify power usage of the board: `boardpb.PowerMode_POWER_MODE_UNSPECIFIED`, `boardpb.PowerMode_POWER_MODE_NORMAL`, and `boardpb.PowerMode_POWER_MODE_OFFLINE_DEEP`.
- `duration` [(\*time.Duration)](https://pkg.go.dev/time#Duration): If provided, the board will exit the given power mode after the specified duration.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#Board).

```go
myBoard, err := board.FromRobot(robot, "my_board")

// Set the power mode of the board to OFFLINE_DEEP.
err := myBoard.Status(context.Background(), nil)
myBoard.SetPowerMode(context.Background(), boardpb.PowerMode_POWER_MODE_OFFLINE_DEEP, nil)
```

{{% /tab %}}
{{< /tabs >}}

### WriteAnalog

Write an analog value to a pin on the board.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `pin` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Name of the pin ({{< glossary_tooltip term_id="pin-number" text="pin number" >}}).
- `value` [(int)](https://docs.python.org/3/library/functions.html#int): Value to write to the pin.
- `extra` [(Optional\[Dict\[str, Any\]\])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None

```python {class="line-numbers linkable-line-numbers"}
my_board = Board.from_robot(robot=robot, name="my_board")

# Set pin 11 to value 48.
await my_board.write_analog(pin="11", value=48)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.write_analog).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `pin` [(string)](https://pkg.go.dev/builtin#string): Name of the pin ({{< glossary_tooltip term_id="pin-number" text="pin number" >}}).
- `value` [(int)](https://pkg.go.dev/builtin#int32): Value to write to the pin.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#Board).

```go
myBoard, err := board.FromRobot(robot, "my_board")

// Set pin 11 to value 48.
err := myBoard.WriteAnalog(context.Background(), "11", 48, nil)
```

{{% /tab %}}
{{< /tabs >}}

### DoCommand

Execute model-specific commands that are not otherwise defined by the component API.
For built-in models, model-specific commands are covered with each model's documentation.
If you are implementing your own board and add features that have no built-in API method, you can access them with `DoCommand`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `command` [(Dict[str, Any])](https://docs.python.org/3/library/stdtypes.html#typesmapping): The command to execute.\
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(Dict[str, Any])](https://docs.python.org/3/library/stdtypes.html#typesmapping): Result of the executed command.

```python {class="line-numbers linkable-line-numbers"}
my_board = Board.from_robot(robot=robot, name="my_board")

my_command = {
  "command": "dosomething",
  "someparameter": 52
}

await my_board.do_command(my_command)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/index.html#viam.components.board.Board.do_command).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `cmd` [(map\[string\]interface{})](https://go.dev/blog/maps): The command to execute.

**Returns:**

- [(map\[string\]interface{})](https://go.dev/blog/maps): Result of the executed command.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

```go {class="line-numbers linkable-line-numbers"}
myBoard, err := board.FromRobot(robot, "my_board")

resp, err := myBoard.DoCommand(ctx, map[string]interface{}{"command": "dosomething", "someparameter": 52})
```

For more information, see the [Go SDK Code](https://github.com/viamrobotics/rdk/blob/main/resource/resource.go).

{{% /tab %}}
{{< /tabs >}}

## `GPIOPin` API

### Set

Set the digital signal output of this pin to low (0V) or high (active, >0V).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `high` [(bool)](https://docs.python.org/3/library/stdtypes.html#bltin-boolean-values): If `true`, set the state of the pin to high.
  If `false`, set the state of the pin to low.
- `extra` [(Optional\[Dict\[str, Any\]\])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/index.html#viam.components.board.Board.GPIOPin.set).

```python
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the GPIOPin with pin number 15.
pin = await my_board.gpio_pin_by_name(name="15")

# Set the pin to high.
await pin.set(high="true")
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `high` [(bool)](https://pkg.go.dev/builtin#bool): If `true`, set the state of the pin to high.
  If `false`, set the state of the pin to low.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#GPIOPin).

```go
myBoard, err := board.FromRobot(robot, "my_board")

// Get the GPIOPin with pin number 15.
pin, err := myBoard.GPIOPinByName("15")

// Set the pin to high.
err := pin.Set(context.Background(), "true", nil)
```

{{% /tab %}}
{{< /tabs >}}

### Get

Get if the digital signal output of this pin is high (active, >0V).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional\[Dict\[str, Any\]\])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(bool)](https://docs.python.org/3/library/stdtypes.html#bltin-boolean-values): If `true`, the state of the pin is high.
  If `false`, the state of the pin is low.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/index.html#viam.components.board.Board.GPIOPin.get).

```python
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the GPIOPin with pin number 15.
pin = await my_board.gpio_pin_by_name(name="15")

# Get if it is true or false that the state of the pin is high.
high = await pin.get()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(bool)](https://pkg.go.dev/builtin#bool): If `true`, the state of the pin is high.
  If `false`, the state of the pin is low.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#GPIOPin).

```go
myBoard, err := board.FromRobot(robot, "my_board")

// Get the GPIOPin with pin number 15.
pin, err := myBoard.GPIOPinByName("15")

// Get if it is true or false that the state of the pin is high.
high := pin.Get(context.Background(), nil)
```

{{% /tab %}}
{{< /tabs >}}

### GetPWM

{{% alert title="Info" color="info" %}}

[Pulse-width modulation (PWM)](https://www.digikey.com/en/blog/pulse-width-modulation) is a method where of transmitting a digital signal in the form of pulses to control analog circuits.
With PWM on a _board_, the continuous digital signal output by a GPIO pin is sampled at regular intervals and transmitted to any [hardware components](/components/) wired to the pin that read analog signals.
This enables the board to communicate with these components.

{{% /alert %}}

Get the pin's [pulse-width modulation (PWM) duty cycle](https://learn.sparkfun.com/tutorials/pulse-width-modulation/duty-cycle): a float [`0.0`, `1.0`] representing the percentage of time the digital signal output by this pin is in the high state (active, >0V) relative to the interval period of the PWM signal [(interval period being the mathematical inverse of the PWM frequency)](https://learn.adafruit.com/improve-brushed-dc-motor-performance/pwm-frequency).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional\[Dict\[str, Any\]\])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(float)](https://docs.python.org/3/library/functions.html#float): A float [`0.0`, `1.0`] representing the percentage of time the digital signal output by this pin is in the high state relative to the interval period of the PWM signal.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/index.html#viam.components.board.Board.GPIOPin.get_pwm).

```python
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the GPIOPin with pin number 15.
pin = await my_board.gpio_pin_by_name(name="15")

# Get if it is true or false that the state of the pin is high.
duty_cycle = await pin.get_pwm()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(float64)](https://pkg.go.dev/builtin#float64): A float [`0.0`, `1.0`] representing the percentage of time the digital signal output by this pin is in the high state relative to the interval period of the PWM signal.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#GPIOPin).

```go
myBoard, err := board.FromRobot(robot, "my_board")

// Get the GPIOPin with pin number 15.
pin, err := myBoard.GPIOPinByName("15")

// Get if it is true or false that the state of the pin is high.
duty_cycle := pin.PWM(context.Background(), nil)
```

{{% /tab %}}
{{< /tabs >}}

### SetPWM

Set the pin's [Pulse-width modulation (PWM) duty cycle](https://learn.sparkfun.com/tutorials/pulse-width-modulation/duty-cycle): a float [`0.0`, `1.0`] indicating the percentage of time the digital signal output of this pin is in the high state (active, >0V) relative to the interval period of the PWM signal [(interval period being the mathematical inverse of the PWM frequency)](https://learn.adafruit.com/improve-brushed-dc-motor-performance/pwm-frequency).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `cycle` [(float64)](https://pkg.go.dev/builtin#float64): A float [`0.0`, `1.0`] representing the percentage of time the digital signal output by this pin is in the high state relative to the interval period of the PWM signal.
- `extra` [(Optional\[Dict\[str, Any\]\])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(bool)](https://docs.python.org/3/library/stdtypes.html#bltin-boolean-values): If `true`, the state of the pin is high.
  If `false`, the state of the pin is low.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/index.html#viam.components.board.Board.GPIOPin.set_pwm).

```python
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the GPIOPin with pin number 15.
pin = await my_board.gpio_pin_by_name(name="15")

# Set the duty cycle to .6, meaning that this pin will be in the high state for
# 60% of the duration of the PWM interval period.
await pin.set_pwm(cycle=.6)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `cycle` [(float64)](https://pkg.go.dev/builtin#float64): A float [`0.0`, `1.0`] representing the percentage of time the digital signal output by this pin is in the high state relative to the interval period of the PWM signal.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#GPIOPin).

```go
myBoard, err := board.FromRobot(robot, "my_board")

// Get the GPIOPin with pin number 15.
pin, err := myBoard.GPIOPinByName("15")

// Set the duty cycle to .6, meaning that this pin will be in the high state for 60% of the duration of the PWM interval period.
err := pin.SetPWM(context.Background(), .6, nil)
```

{{% /tab %}}
{{< /tabs >}}

### PWMFreq

Get the [Pulse-width modulation (PWM) frequency](https://learn.adafruit.com/improve-brushed-dc-motor-performance/pwm-frequency) in Hertz (Hz) of this pin, the count of PWM interval periods per second.
The optimal value for PWM Frequency depends on the type and model of [component](/components/) you control with the signal output by this pin.
Refer to your device's data sheet for PWM Frequency specifications.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional\[Dict\[str, Any\]\])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(int)](https://docs.python.org/3/library/functions.html#int): The PWM Frequency in Hertz (Hz) (the count of PWM interval periods per second) the digital signal output by this pin is set to.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/index.html#viam.components.board.Board.GPIOPin.get_pwm_frequency).

```python
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the GPIOPin with pin number 15.
pin = await my_board.gpio_pin_by_name(name="15")

# Get the PWM frequency of this pin.
freq = await pin.get_pwm_frequency()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(unit)](https://pkg.go.dev/builtin#uint): The PWM Frequency in Hertz (Hz) (the count of PWM interval periods per second) the digital signal output by this pin is set to.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#GPIOPin).

```go
myBoard, err := board.FromRobot(robot, "my_board")

// Get the GPIOPin with pin number 15.
pin, err := myBoard.GPIOPinByName("15")

// Get the PWM frequency of this pin.
freqHz, err := pin.PWMFreq(context.Background(), nil)
```

{{% /tab %}}
{{< /tabs >}}

### SetPWMFreq

Set the [Pulse-width modulation (PWM) frequency](https://learn.adafruit.com/improve-brushed-dc-motor-performance/pwm-frequency) in Hertz (Hz) of this pin, the count of PWM interval periods per second.
The optimal value for PWM Frequency depends on the type and model of [component](/components/) you control with the PWM signal output by this pin.
Refer to your device's data sheet for PWM Frequency specifications.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional\[Dict\[str, Any\]\])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(int)](https://docs.python.org/3/library/functions.html#int): The PWM Frequency in Hertz (Hz), the count of PWM interval periods per second, to set the digital signal output by this pin to.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/index.html#viam.components.board.Board.GPIOPin.set_pwm_frequency).

```python
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the GPIOPin with pin number 15.
pin = await my_board.gpio_pin_by_name(name="15")

# Set the PWM frequency of this pin to 1600 Hz.
high = await pin.set_pwm_frequency(frequency=1600)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `freqHz` [(unit)](https://pkg.go.dev/builtin#uint): The PWM Frequency in Hertz (Hz), the count of PWM interval periods per second, to set the digital signal output by this pin to.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#GPIOPin).

```go
myBoard, err := board.FromRobot(robot, "my_board")

// Get the GPIOPin with pin number 15.
pin, err := myBoard.GPIOPinByName("15")

// Set the PWM frequency of this pin to 1600 Hz.
high := pin.SetPWMFreq(context.Background(), 1600, nil)
```

{{% /tab %}}
{{< /tabs >}}

## `AnalogReader` API

### Read

Read the current integer value of the digital signal output by the [ADC](#analogs).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional\[Dict\[str, Any\]\])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(int)](https://docs.python.org/3/library/functions.html#int): The value of the digital signal output by the analog reader.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/index.html#viam.components.board.Board.AnalogReader.read).

```python
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the GPIOPin with pin number 15.
pin = await my_board.gpio_pin_by_name(name="15")

# Get if it is true or false that the pin is set to high.
duty_cycle = await pin.get_pwm()

# Get the AnalogReader "my_example_analog_reader".
reader = await my_board.analog_reader_by_name(
    name="my_example_analog_reader")

# Get the value of the digital signal "my_example_analog_reader" has most
# recently measured.
reading = reader.read()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(int)](https://pkg.go.dev/builtin#int): The value of the digital signal output by the analog reader.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#GPIOPin).

```go
myBoard, err := board.FromRobot(robot, "my_board")

// Get the AnalogReader "my_example_analog_reader".
reader, err := myBoard.AnalogReaderByName("my_example_analog_reader")

// Get the value of the digital signal "my_example_analog_reader" has most recently measured.
reading := reader.Read(context.Background(), nil)
```

{{% /tab %}}
{{< /tabs >}}

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

- `extra` [(Optional\[Dict\[str, Any\]\])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(int)](https://docs.python.org/3/library/functions.html#int): The amount of [Ticks](#tick) that have occurred.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/index.html#viam.components.board.Board.DigitalInterrupt.value).

```python
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the DigitalInterrupt "my_example_digital_interrupt".
interrupt = await my_board.digital_interrupt_by_name(
    name="my_example_digital_interrupt")

# Get the amount of times this DigitalInterrupt has been interrupted with a
# tick.
count = await interrupt.value()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(int64)](https://pkg.go.dev/builtin#int64): The amount of [Ticks](#tick) that have occurred.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

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

- `extra` [(Optional\[Dict\[str, Any\]\])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(int)](https://docs.python.org/3/library/functions.html#int): The [RollingAverage](https://pkg.go.dev/go.viam.com/rdk/utils#RollingAverage) of the time in nanoseconds between two successive low signals (pulse width) recorded by [`Tick()`](#tick), computed over a window of size `10`.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/index.html#viam.components.board.Board.DigitalInterrupt.value).

```python
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the DigitalInterrupt "my_example_digital_interrupt".
interrupt = await my_board.digital_interrupt_by_name(
    name="my_example_digital_interrupt")

# Get the rolling average of the pulse width across each time the
# DigitalInterrupt is interrupted with a tick.
rolling_avg = await interrupt.value()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(int64)](https://pkg.go.dev/builtin#int64): The [RollingAverage](https://pkg.go.dev/go.viam.com/rdk/utils#RollingAverage) of the time in nanoseconds between two successive low signals (pulse width) recorded by [`Tick()`](#tick), computed over a window of size `10`.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

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

Record an interrupt and notify any [channels](https://go.dev/tour/concurrency/2) that have been added with [AddCallback()](#addcallback).

{{% alert title="Tip" color="tip" %}}
You should only need to integrate this method into your application code for testing purposes, as the handling of `Tick()` should be automated once the interrupt is configured.

Calling this method is not yet fully implemented with the Viam Python SDK.
{{% /alert %}}

<!-- NOT YET IMPLEMENTED: See https://github.com/viamrobotics/viam-python-sdk/blob/main/src/viam/components/board/client.py#L60

BASIC

**Parameters:**

- `high` [(bool)](https://docs.python.org/3/library/stdtypes.html#bltin-boolean-values): If `true`, the state of the pin is set to high.
If `false`, the state of the pin is set to low.
- `nanos` [(int)](https://docs.python.org/3/library/functions.html#int): The time that has elapsed in nanoseconds since the last time the interrupt was ticked.

**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/index.html#viam.components.board.Board.DigitalInterrupt.tick).

```python
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the DigitalInterrupt "my_example_digital_interrupt".
interrupt = await my_board.digital_interrupt_by_name(
    name="my_example_digital_interrupt")

# Record an interrupt and notify any interested callbacks.
await interrupt.tick(high=true, nanos=12345)
```

SERVO

**Parameters:**

- `high` (https://docs.python.org/3/library/stdtypes.html#bltin-boolean-values): If `true`, the state of the pin is set to high.
If `false`, the state of the pin is set to low.
- `nanos` [(int)](https://docs.python.org/3/library/functions.html#int): The time in nanoseconds between two successive low signals (pulse width).

**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/index.html#viam.components.board.Board.DigitalInterrupt.tick).

```python
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the DigitalInterrupt "my_example_digital_interrupt".
interrupt = await my_board.digital_interrupt_by_name(
    name="my_example_digital_interrupt")

# Record an interrupt and notify any interested callbacks.
await interrupt.tick(high=true, nanos=12345)
```
 -->

{{< tabs >}}
{{% tab name="Basic - Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `high` [(bool)](https://pkg.go.dev/builtin#bool): If `true`, the state of the pin is set to high.
  If `false`, the state of the pin is set to low.
- `now` [(uint64)](https://pkg.go.dev/builtin#uint64): The time that has elapsed in nanoseconds since the last time the interrupt was ticked.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#BasicDigitalInterrupt).

```go
myBoard, err := board.FromRobot(robot, "my_board")

// Get the DigitalInterrupt "my_example_digital_interrupt".
interrupt, ok := myBoard.DigitalInterruptByName("my_example_digital_interrupt")

// Record an interrupt and notify any interested callbacks.
err := interrupt.Tick(context.Background(), true, 12345)
```

{{% /tab %}}
{{% tab name="Servo - Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `high` [(bool)](https://pkg.go.dev/builtin#bool): If `true`, the state of the pin is set to high.
  If `false`, the state of the pin is set to low.
- `nanoseconds` [(uint64)](https://pkg.go.dev/builtin#uint64): The time in nanoseconds between two successive low signals (pulse width).

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

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

### AddCallback

Add a [channel](https://go.dev/tour/concurrency/2) as a listener for when the state of the [configured GPIO pin](#digital_interrupts) changes.
When [Tick()](#tick) is called, callbacks added to an interrupt will be sent the returned value `high`.

{{% alert title="Support Notice" color="note" %}}
This method is not available for digital interrupts [configured](#digital_interrupts) with `"type": "servo"`.
It is also not yet fully implemented with the Viam Python SDK.
{{% /alert %}}

<!-- NOT YET IMPLEMENTED: see https://github.com/viamrobotics/viam-python-sdk/blob/main/src/viam/components/board/client.py#L63

**Parameters:**

- `queue` [(multiprocessing.Queue)](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Queue): The receiving queue.

**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/index.html#viam.components.board.Board.DigitalInterrupt.add_callback).

```python
"""from multiprocessing import Queue"""
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the GPIOPin with pin number 15.
pin = await my_board.gpio_pin_by_name(name="15")

callback_queue = Queue(maxsize=10)

# Get the DigitalInterrupt "my_example_digital_interrupt".
interrupt = await my_board.digital_interrupt_by_name(
    name="my_example_digital_interrupt")

# Add a queue to the interrupt.
interrupt.add_callback(callback_queue)
```
 -->

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `callback` [(chan Tick)](https://go.dev/tour/concurrency/2): The channel to add as a listener for when the state of the GPIO pin this interrupt is [configured for](#digital_interrupts) changes between high and low.

**Returns:**

- None

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#DigitalInterrupt.AddCallback).

```go {class="line-numbers linkable-line-numbers"}
myBoard, err := board.FromRobot(robot, "my_board")

// Get the DigitalInterrupt "my_example_digital_interrupt".
interrupt, ok := myBoard.DigitalInterruptByName("my_example_digital_interrupt")

// Make the channel for Tick().
ch := make(chan Tick)

// Add the channel to "my_example_digital_interrupt" as a callback.
interrupt.AddCallback(ch)
```

{{% /tab %}}
{{< /tabs >}}

### AddPostProcessor

Add a [PostProcessor](https://pkg.go.dev/go.viam.com/rdk/components/board#PostProcessor) function that takes an integer input and transforms it into a new integer value.
Functions added to an interrupt will be used to modify values before they are returned by [Value()](#value).

{{% alert title="Support Notice" color="note" %}}
This method is not yet fully implemented with the Viam Python SDK.
{{% /alert %}}

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `processor` [(PostProcessor)](https://pkg.go.dev/go.viam.com/rdk/components/board#PostProcessor): The post processor function to add.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#DigitalInterrupt).

```go
myBoard, err := board.FromRobot(robot, "my_board")

// Get the GPIOPin with pin number 15.
pin, err := myBoard.GPIOPinByName("15")

// Get the DigitalInterrupt "my_example_digital_interrupt".
interrupt, ok := myBoard.DigitalInterruptByName("my_example_digital_interrupt")

// Create a simple post processing function calculating absolute value of integers.
MySimplePP := int64(math.Abs)

// Add "MySimplePP" as a post processor to "my_example_digital_interrupt".
interrupt.AddPostProcessor(MySimplePP)
```

{{% /tab %}}
{{< /tabs >}}

<!-- NOT IMPLEMENTED: see https://github.com/viamrobotics/viam-python-sdk/blob/main/src/viam/components/board/client.py#L66

**Parameters:**

- `processor` [(Callable[[int], int])](https://docs.python.org/3/library/typing.html#callable): The post processor function to add.

**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/index.html#viam.components.board.Board.DigitalInterrupt.add_post_processor).

```python
"""from collections.abc import Callable"""
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the DigitalInterrupt "my_example_digital_interrupt".
interrupt = await my_board.digital_interrupt_by_name(
    name="my_example_digital_interrupt")
```
``` -->

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}

## Related Services

{{< cards >}}
{{% card link="/services/frame-system/" class="small" %}}
{{</ cards >}}

## Next Steps

{{< cards >}}
{{% card link="/tutorials/get-started/blink-an-led" %}}
{{% card link="/tutorials/projects/guardian" %}}
{{< /cards >}}
