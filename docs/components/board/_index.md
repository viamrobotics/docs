---
title: "Board Component"
linkTitle: "Board"
childTitleEndOverwrite: "Board Component"
weight: 20
type: "docs"
no_list: true
description: "The signal wire hub of a machine, with GPIO pins for transmitting signals between the machine's computer and its other components."
tags: ["board", "components"]
icon: true
images: ["/icons/components/board.svg"]
modulescript: true
aliases:
  - "/components/board/"
# SMEs: Gautham, Rand
---

A _board_ component on your machine communicates with the other [components](/components/) of the machine.

A board can be:

- A single-board computer (SBC) with GPIO pins and a CPU capable of running `viam-server`.
- A GPIO peripheral device that must connect to an external computer.
- A PWM peripheral device that must connect to an SBC that has a CPU and GPIO pins.

The board of a machine is also its signal wire hub that provides access to general purpose input/output [(GPIO)](https://www.howtogeek.com/787928/what-is-gpio/) pins: a collection of pins on the motherboard of a computer that can receive electrical signals.

Signaling is overseen by a computer running `viam-server` which allows you to control the flow of electricity to these pins to change their state between "high" (active) and "low" (inactive), and wire them to send [digital signals](https://en.wikipedia.org/wiki/Digital_signal) to and from other hardware.

{{% figure src="/components/board/board-comp-options.png" alt="Image showing two board options: First, running viam-server locally and second, running via a peripheral plugged into the USB port of a computer that is running the viam-server." title="Two different board options: a single-board computer with GPIO pins running `viam-server` locally, or a GPIO peripheral plugged into a desktop computer's USB port, with the computer running `viam-server`." %}}

## Supported models

To use your board with Viam, check whether one of the following [built-in models](#built-in-models) or [modular resources](#modular-resources) supports your board.

{{< alert title="Running viam-server" color="note" >}}

The board component allows you to use the pins on your board.
If there is no board model for your board:

- you can still run `viam-server` if your board [supports it](/get-started/installation/#compatibility)
- you can still access USB ports

{{< /alert >}}

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
| [`pca9685`](pca9685/) | [PCA9685 Arduino I<sup>2</sup>C Interface](https://www.adafruit.com/product/815), a 16-channel I<sup>2</sup>C [PWM](https://docs.arduino.cc/learn/microcontrollers/analog-output)/[servo](/components/servo/) driver peripheral |
| [`odroid`](odroid/) | [Odroid-C4](https://www.hardkernel.com/shop/odroid-c4/) |
| [`customlinux`](customlinux/) | A model for other Linux boards. |
| [`fake`](fake/) | A model used for testing, with no physical hardware |

### Modular resources

{{<modular-resources api="rdk:component:board" type="board">}}

{{< readfile "/static/include/create-your-own-mr.md" >}}

### Micro-RDK

If you are using the micro-RDK, navigate to [Micro-RDK Board](/build/micro-rdk/board/) for supported model information.

## Attribute configuration

Configuring these attributes on your board allows you to integrate [analog-to-digital converters](#analogs) and [digital interrupts](#digital_interrupts) into your machine.

### `analogs`

{{< readfile "/static/include/components/board/board-analogs.md" >}}

### `digital_interrupts`

{{< readfile "/static/include/components/board/board-digital-interrupts.md" >}}

## Control your board with Viam's client SDK libraries

To get started using Viam's SDKs to connect to and control your machine, go to your machine's page on [the Viam app](https://app.viam.com), navigate to the **CONNECT** tab's **Code sample** page, select your preferred programming language, and copy the sample code generated.

{{% snippet "show-secret.md" %}}

When executed, this sample code will create a connection to your machine as a client.
Then control your machine programmatically by getting your `board` component from the machine with `FromRobot` and adding API method calls, as shown in the following examples.

These examples assume you have a board called "my_board" configured as a component of your machine.
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

Additionally, the nested `GPIOPin`, `Analog`, and `DigitalInterrupt` interfaces support the following methods:

[`GPIOPin`](#gpiopin-api) API:

{{< readfile "/static/include/components/apis/gpiopin.md" >}}

<br>

[`Analog`](#analog-api) API:

{{< readfile "/static/include/components/apis/analogreader.md" >}}

<br>

[`DigitalInterrupt`](#digitalinterrupt-api) API:

{{< readfile "/static/include/components/apis/digitalinterrupt.md" >}}

### AnalogByName

Get an [`Analog`](#analogs) pin by `name`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `name` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Name of the analog pin you want to retrieve.

**Returns:**

- [(Analog)](https://python.viam.dev/autoapi/viam/components/board/index.html#viam.components.board.Board.AnalogReader): An interface representing an analog pin configured and residing on the board.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/index.html#viam.components.board.Board.analog_reader_by_name).

```python
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the Analog "my_example_analog_pin".
analog = await my_board.analog_reader_by_name(name="my_example_analog")
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `name` [(string)](https://pkg.go.dev/builtin#string): Name of the analog pin you want to retrieve. Set as the `"name"` property [in configuration](/components/board/#digital_interrupts).

**Returns:**

- [(Analog)](https://pkg.go.dev/go.viam.com/rdk/components/board#AnalogReader): An interface representing an analog pin configured and residing on the board.
- [(bool)](https://pkg.go.dev/builtin#bool): True if there was an analog pin of this `name` found on your board.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#Board).

```go
myBoard, err := board.FromRobot(robot, "my_board")

// Get the Analog pin "my_example_analog".
analog, err := myBoard.AnalogByName("my_example_analog")

// Read the value from the analog pin.
val, err := analog.Read(context.Background, map[string]interface{})
```

{{% /tab %}}
{{< /tabs >}}

### GetDigitalInterruptValue

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

### AnalogNames

Get the name of every [`Analog`](#analogs) pin configured and residing on the board or implemented in the board driver.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- [(List\[str\])](https://docs.python.org/3/library/stdtypes.html#typesseq-list): A list containing the `"name"` of every analog pin [configured](#supported-models) on the board.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/index.html#viam.components.board.Board.analog_reader_names).

```python
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the name of every Analog configured on the board.
names = await my_board.analog_names()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- None

**Returns:**

- [([]string)](https://go.dev/tour/moretypes/7): A slice containing the `"name"` of every analog pin [configured](#supported-models) on the board.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#Board).

```go
myBoard, err := board.FromRobot(robot, "my_board")

// Get the name of every Analog pin configured on the board.
names := myBoard.AnalogNames()
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
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None

```python {class="line-numbers linkable-line-numbers"}
my_board = Board.from_robot(robot=robot, name="my_board")

# Set pin 11 to value 48.
await my_board.write_analog(pin="11", value=48)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/board/index.html#viam.components.board.board.Board.write_analog).

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

### StreamTicks

Start a stream of [`DigitalInterrupt`](/components/board/#digital_interrupts) ticks.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `interrupts` (List[[DigitalInterrupt](https://python.viam.dev/autoapi/viam/components/board/board/index.html#viam.components.board.board.Board.DigitalInterrupt)]): List of digital interrupts to receive ticks from.

**Returns:**

- [(`TickStream`)](https://python.viam.dev/autoapi/viam/components/board/board/index.html#viam.components.board.board.TickStream): [Stream](https://python.viam.dev/autoapi/viam/streams/index.html#viam.streams.Stream) of [Ticks](https://python.viam.dev/autoapi/viam/proto/component/board/index.html#viam.proto.component.board.StreamTicksResponse), objects containing `pin_name`, `time`, and `high` fields.

```python {class="line-numbers linkable-line-numbers"}
my_board = Board.from_robot(robot=robot, name="my_board")

di8 = await my_board.digital_interrupt_by_name(name="8")
di11 = await my_board.digital_interrupt_by_name(name="11")

# Stream ticks from the listed digital interrupts on pins 8 and 11.
ticks = await my_board.stream_ticks([di8, di11])
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.BoardClient.stream_ticks).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `interrupts` [([]DigitalInterrupt)](https://pkg.go.dev/go.viam.com/rdk/components/board#DigitalInterrupt): Slice of digital interrupts to receive ticks from.
- `ch` ([chan](https://go.dev/tour/concurrency/2) [Tick](https://pkg.go.dev/go.viam.com/rdk/components/board#Tick)): The channel to stream Ticks, structs containing `Name`, `High`, and `TimestampNanosec` fields.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#Board).

```go
myBoard, err := board.FromRobot(robot, "my_board")

// Make a channel to stream ticks
ticksChan := make(chan board.Tick)

interrupts := []*DigitalInterrupt{}

if di8, err := myBoard.DigitalInterruptByName("8"); err == nil {
    interrupts = append(interrupts, di8)
}
if di11, err := myBoard.DigitalInterruptByName("11"); err == nil {
    interrupts = append(interrupts, di11)
}

// Stream ticks on ticksChan from the listed digital interrupts on pins 8 and 11.
err = myBoard.StreamTicks(context.Background(), interrupts, ticksChan, nil)
```

{{% /tab %}}
{{< /tabs >}}

### GetGeometries

Get all the geometries associated with the board in its current configuration, in the [frame](/mobility/frame-system/) of the board.
The [motion](/mobility/motion/) and [navigation](/mobility/navigation/) services use the relative position of inherent geometries to configured geometries representing obstacles for collision detection and obstacle avoidance while motion planning.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional\[Dict\[str, Any\]\])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(List[Geometry])](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Geometry): The geometries associated with the board, in any order.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.BoardClient.get_geometries).

```python {class="line-numbers linkable-line-numbers"}
my_board = Board.from_robot(robot=robot, name="my_board")

geometries = await my_board.get_geometries()

if geometries:
    # Get the center of the first geometry
    print(f"Pose of the first geometry's centerpoint: {geometries[0].center}")
```

{{% /tab %}}

<!-- Go tab

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [`[]spatialmath.Geometry`](https://pkg.go.dev/go.viam.com/rdk/spatialmath#Geometry): The geometries associated with the board, in any order.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Shaped).

```go {class="line-numbers linkable-line-numbers"}
myBoard, err := board.FromRobot(robot, "my_board")

geometries, err := my.Geometries(context.Background(), nil)

if len(geometries) > 0 {
    // Get the center of the first geometry
    elem := geometries[0]
    fmt.Println("Pose of the first geometry's center point:", elem.center)
}
```

 -->

{{< /tabs >}}

### DoCommand

Execute model-specific commands that are not otherwise defined by the component API.
For built-in models, model-specific commands are covered with each model's documentation.
If you are implementing your own board and add features that have no built-in API method, you can access them with `DoCommand`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `command` [(Dict[str, Any])](https://docs.python.org/3/library/stdtypes.html#typesmapping): The command to execute.
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

### Close

Safely shut down the resource and prevent further use.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- None

```python {class="line-numbers linkable-line-numbers"}
my_board = Board.from_robot(robot, "my_board")

await my_board.close()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.BoardClient.close).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error) : An error, if one occurred.

```go {class="line-numbers linkable-line-numbers"}
myBoard, err := board.FromRobot(robot, "my_board")

err := myBoard.Close(ctx)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}

## `GPIOPin` API

### SetGPIO

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

### GetGPIO

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

### Close

Safely shut down the resource and prevent further use.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- None

```python {class="line-numbers linkable-line-numbers"}
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the GPIOPin with pin number 15.
pin = await my_board.gpio_pin_by_name(name="15")

# Close the pin.
await pin.close()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.GPIOPinClient.close).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error) : An error, if one occurred.

```go {class="line-numbers linkable-line-numbers"}
myBoard, err := board.FromRobot(robot, "my_board")

// Get the GPIOPin with pin number 15.
pin, err := myBoard.GPIOPinByName("15")

// Close the pin.
err := pin.Close(ctx)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}

## `Analog` API

### Read

Read the current integer value of the digital signal output by the [ADC](#analogs).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional\[Dict\[str, Any\]\])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(int)](https://docs.python.org/3/library/functions.html#int): The value of the digital signal output by the analog pin.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/index.html#viam.components.board.Board.AnalogReader.read).

```python
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the GPIOPin with pin number 15.
pin = await my_board.gpio_pin_by_name(name="15")

# Get if it is true or false that the pin is set to high.
duty_cycle = await pin.get_pwm()

# Get the Analog pin "my_example_analog".
analog = await my_board.analog_by_name(
    name="my_example_analog")

# Get the value of the digital signal "my_example_analog" has most
# recently measured.
reading = analog.read()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(int)](https://pkg.go.dev/builtin#int): The value of the digital signal output by the analog pin.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#GPIOPin).

```go
myBoard, err := board.FromRobot(robot, "my_board")

// Get the Analog pin "my_example_analog".
analog, err := myBoard.AnalogByName("my_example_analog")

// Get the value of the digital signal "my_example_analog" has most recently measured.
reading := analog.Read(context.Background(), nil)
```

{{% /tab %}}
{{< /tabs >}}

### Close

Safely shut down the resource and prevent further use.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- None

```python {class="line-numbers linkable-line-numbers"}
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the Analog pin "my_example_analog".
analog = await my_board.analog_by_name(
    name="my_example_analog")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.AnalogReaderClient.close).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error) : An error, if one occurred.

```go {class="line-numbers linkable-line-numbers"}
myBoard, err := board.FromRobot(robot, "my_board")

// Get the Analog "my_example_analog".
analog, err := myBoard.AnalogByName("my_example_analog")

// Read the current value from the analog pin.
value, err := analog.Read(context.Background(), map[string]interface{})
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}

## `DigitalInterrupt` API

### Value

Get the current value of this interrupt.

Calculation of value differs between the `"type"` of interrupt [configured](#digital_interrupts):

{{< tabs >}}
{{% tab name="Basic" %}}
{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional\[Dict\[str, Any\]\])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(int)](https://docs.python.org/3/library/functions.html#int): The amount of ticks that have occurred.

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

- [(int64)](https://pkg.go.dev/builtin#int64): The amount of ticks that have occurred.
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

- [(int)](https://docs.python.org/3/library/functions.html#int): The [RollingAverage](https://pkg.go.dev/go.viam.com/rdk/utils#RollingAverage) of the time in nanoseconds between two successive low signals (pulse width) recorded by the digital interrupt's ticks, computed over a window of size `10`.

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

- [(int64)](https://pkg.go.dev/builtin#int64): The [RollingAverage](https://pkg.go.dev/go.viam.com/rdk/utils#RollingAverage) of the time in nanoseconds between two successive low signals (pulse width) recorded by the digital interrupt's ticks, computed over a window of size `10`.
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

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}

## Next steps

{{< cards >}}
{{% card link="/tutorials/get-started/blink-an-led" %}}
{{% card link="/tutorials/projects/guardian" %}}
{{< /cards >}}
