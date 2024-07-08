### SetGPIO

Set the digital signal output of this pin to low (0V) or high (active, >0V).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `high` ([bool](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)) (required): When true, sets the pin to high. When false, sets the pin to low.
- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the GPIOPin with pin number 15.
pin = await my_board.gpio_pin_by_name(name="15")

# Set the pin to high.
await pin.set(high="true")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.GPIOPinClient.set).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `high` [(bool)](https://pkg.go.dev/builtin#bool): If `true`, set the state of the pin to high. If `false`, set the state of the pin to low.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myBoard, err := board.FromRobot(robot, "my_board")

// Get the GPIOPin with pin number 15.
pin, err := myBoard.GPIOPinByName("15")

// Set the pin to high.
err := pin.Set(context.Background(), "true", nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#GPIOPin).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `pin` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `high` [bool](https://api.flutter.dev/flutter/dart-core/bool-class.html) (required)
- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<void>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
// Set pin 15 to high
await myBoard.setGpioState('15', true);
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Board/setGpioState.html).

{{% /tab %}}
{{< /tabs >}}

### GetGPIO

Get if the digital signal output of this pin is high (active, >0V).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([bool](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)): Indicates if the state of the pin is high.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the GPIOPin with pin number 15.
pin = await my_board.gpio_pin_by_name(name="15")

# Get if it is true or false that the state of the pin is high.
high = await pin.get()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.GPIOPinClient.get).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(bool)](https://pkg.go.dev/builtin#bool): If `true`, the state of the pin is high. If `false`, the state of the pin is low.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myBoard, err := board.FromRobot(robot, "my_board")

// Get the GPIOPin with pin number 15.
pin, err := myBoard.GPIOPinByName("15")

// Get if it is true or false that the state of the pin is high.
high := pin.Get(context.Background(), nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#GPIOPin).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `pin` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<[bool](https://api.flutter.dev/flutter/dart-core/bool-class.html)>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
// Whether the state of pin 15 is currently high
bool pinStateIsHigh = await myBoard.gpio('15');
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Board/gpio.html).

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

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)): The duty cycle.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the GPIOPin with pin number 15.
pin = await my_board.gpio_pin_by_name(name="15")

# Get if it is true or false that the state of the pin is high.
duty_cycle = await pin.get_pwm()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.GPIOPinClient.get_pwm).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(float64)](https://pkg.go.dev/builtin#float64): A float [`0.0`, `1.0`] representing the percentage of time the digital signal output by this pin is in the high state relative to the interval period of the PWM signal.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myBoard, err := board.FromRobot(robot, "my_board")

// Get the GPIOPin with pin number 15.
pin, err := myBoard.GPIOPinByName("15")

// Returns the duty cycle.
duty_cycle := pin.PWM(context.Background(), nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#GPIOPin).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `pin` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<[double](https://api.flutter.dev/flutter/dart-core/double-class.html)>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
// Get the PWM duty cycle of pin 15
var dutyCycle = await myBoard.pwm('15');
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Board/pwm.html).

{{% /tab %}}
{{< /tabs >}}

### SetPWM

Set the pin's [Pulse-width modulation (PWM) duty cycle](https://learn.sparkfun.com/tutorials/pulse-width-modulation/duty-cycle): a float [`0.0`, `1.0`] indicating the percentage of time the digital signal output of this pin is in the high state (active, >0V) relative to the interval period of the PWM signal [(interval period being the mathematical inverse of the PWM frequency)](https://learn.adafruit.com/improve-brushed-dc-motor-performance/pwm-frequency).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `duty_cycle` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (required): The duty cycle.
- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the GPIOPin with pin number 15.
pin = await my_board.gpio_pin_by_name(name="15")

# Set the duty cycle to .6, meaning that this pin will be in the high state for
# 60% of the duration of the PWM interval period.
await pin.set_pwm(cycle=.6)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.GPIOPinClient.set_pwm).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `dutyCyclePct` [(float64)](https://pkg.go.dev/builtin#float64): A float [`0.0`, `1.0`] representing the percentage of time the digital signal output by this pin is in the high state relative to the interval period of the PWM signal.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myBoard, err := board.FromRobot(robot, "my_board")

// Get the GPIOPin with pin number 15.
pin, err := myBoard.GPIOPinByName("15")

// Set the duty cycle to .6, meaning that this pin will be in the high state for 60% of the duration of the PWM interval period.
err := pin.SetPWM(context.Background(), .6, nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#GPIOPin).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `pin` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `dutyCyclePct` [double](https://api.flutter.dev/flutter/dart-core/double-class.html) (required)
- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<void>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
// Set the PWM duty cycle of pin 13
await myBoard.setPwm('13', 0.6);
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Board/setPwm.html).

{{% /tab %}}
{{< /tabs >}}

### PWMFrequency

Get the PWM frequency of the GPIO pin.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([int](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)): The PWM frequency.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the GPIOPin with pin number 15.
pin = await my_board.gpio_pin_by_name(name="15")

# Get the PWM frequency of this pin.
freq = await pin.get_pwm_frequency()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.GPIOPinClient.get_pwm_frequency).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(uint)](https://pkg.go.dev/builtin#uint): The PWM Frequency in Hertz (Hz) (the count of PWM interval periods per second) the digital signal output by this pin is set to.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myBoard, err := board.FromRobot(robot, "my_board")

// Get the GPIOPin with pin number 15.
pin, err := myBoard.GPIOPinByName("15")

// Get the PWM frequency of this pin.
freqHz, err := pin.PWMFreq(context.Background(), nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#GPIOPin).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `pin` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<[int](https://api.flutter.dev/flutter/dart-core/int-class.html)>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
// Get the PWM frequency of pin 11
var frequency = await myBoard.pwmFrequency('11');
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Board/pwmFrequency.html).

{{% /tab %}}
{{< /tabs >}}

### SetPWMFrequency

Set the pin to the given PWM `frequency` (in Hz). When `frequency` is 0, it will use the board’s default PWM frequency.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `frequency` ([int](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (required): The frequency, in Hz.
- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the GPIOPin with pin number 15.
pin = await my_board.gpio_pin_by_name(name="15")

# Set the PWM frequency of this pin to 1600 Hz.
high = await pin.set_pwm_frequency(frequency=1600)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.GPIOPinClient.set_pwm_frequency).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `freqHz` [(uint)](https://pkg.go.dev/builtin#uint): The PWM Frequency in Hertz (Hz), the count of PWM interval periods per second, to set the digital signal output by this pin to.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myBoard, err := board.FromRobot(robot, "my_board")

// Get the GPIOPin with pin number 15.
pin, err := myBoard.GPIOPinByName("15")

// Set the PWM frequency of this pin to 1600 Hz.
high := pin.SetPWMFreq(context.Background(), 1600, nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#GPIOPin).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `pin` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `frequencyHz` [int](https://api.flutter.dev/flutter/dart-core/int-class.html) (required)
- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<void>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
// Set the PWM frequency of pin 15 to 1600 Hz
await myBoard.setPwmFrequency('15', 1600);
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Board/setPwmFrequency.html).

{{% /tab %}}
{{< /tabs >}}

### AnalogNames

Get the name of every [`Analog`](#analogs) configured and residing on the board.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None.

**Returns:**

- (List[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)]): The list of names of all known analog readers/writers.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the name of every Analog configured on the board.
names = await my_board.analog_names()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.BoardClient.analog_names).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- None.

**Returns:**

- [([]string)](https://pkg.go.dev/builtin#string): A slice containing the `"name"` of every analog pin [configured](#supported-models) on the board.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#Board).

{{% /tab %}}
{{< /tabs >}}

### AnalogByName

Get an [`Analog`](#analogs) by `name`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): Name of the analog reader to be retrieved.

**Returns:**

- ([viam.components.board.board.Board.Analog](https://python.viam.dev/autoapi/viam/components/board/board/index.html#viam.components.board.board.Board.Analog)): The analog reader or writer.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the Analog "my_example_analog_reader".
reader = await my_board.analog_by_name(name="my_example_analog_reader")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.BoardClient.analog_by_name).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `name` [(string)](https://pkg.go.dev/builtin#string): Name of the analog pin you want to retrieve. Set as the `"name"` property [in configuration](/components/board/#digital_interrupts).

**Returns:**

- [(Analog)](https://pkg.go.dev/go.viam.com/rdk/components/board#Analog): An interface representing an analog pin configured and residing on the board.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myBoard, err := board.FromRobot(robot, "my_board")

// Get the Analog pin "my_example_analog".
analog, err := myBoard.AnalogByName("my_example_analog")
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#Board).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `analogReaderName` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<[AnalogValue](https://flutter.viam.dev/viam_sdk/AnalogValue.html)>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
// Get the current value of an analog reader named "my_example_analog"
var analogVal = await myBoard.analogReaderValue('my_example_analog');
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Board/analogReaderValue.html).

{{% /tab %}}
{{< /tabs >}}

### Write

Write an analog value to a pin on the board.

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `value` [(int)](https://pkg.go.dev/builtin#int): Value to write to the pin.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myBoard, err := board.FromRobot(robot, "my_board")

// Get the Analog pin "my_example_analog".
analog, err := myBoard.AnalogByName("my_example_analog")

// Set the pin to value 48.
err := analog.Write(context.Background(), 48, nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#Analog).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `pin` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `value` [int](https://api.flutter.dev/flutter/dart-core/int-class.html) (required)
- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<void>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
// Set pin 11 to value 48
await myBoard.writeAnalog('11', 48);
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Board/writeAnalog.html).

{{% /tab %}}
{{< /tabs >}}

### GetDigitalInterruptValue

Get an [`DigitalInterrupt`](#digital_interrupts) by `name`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): Name of the digital interrupt.

**Returns:**

- ([viam.components.board.board.Board.DigitalInterrupt](https://python.viam.dev/autoapi/viam/components/board/board/index.html#viam.components.board.board.Board.DigitalInterrupt)): The digital interrupt.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the DigitalInterrupt "my_example_digital_interrupt".
interrupt = await my_board.digital_interrupt_by_name(
    name="my_example_digital_interrupt")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.BoardClient.digital_interrupt_by_name).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `name` [(string)](https://pkg.go.dev/builtin#string): Name of the digital interrupt you want to retrieve. Set as the `"name"` property [in configuration](/components/board/#digital_interrupts).

**Returns:**

- [(DigitalInterrupt)](https://pkg.go.dev/go.viam.com/rdk/components/board#DigitalInterrupt): An interface representing a configured interrupt on the board.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myBoard, err := board.FromRobot(robot, "my_board")

// Get the DigitalInterrupt "my_example_digital_interrupt".
interrupt, err := myBoard.DigitalInterruptByName("my_example_digital_interrupt")
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#Board).

{{% /tab %}}
{{< /tabs >}}

### StreamTicks

Start a stream of [`DigitalInterrupt`](/components/board/#digital_interrupts) ticks.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `interrupts` ([List[viam.components.board.board.Board.DigitalInterrupt]](https://python.viam.dev/autoapi/viam/components/board/board/index.html#viam.components.board.board.Board.DigitalInterrupt)) (required): list of digital interrupts to receive ticks from.
- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.

**Returns:**

- (viam.components.board.board.TickStream): stream of ticks.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_board = Board.from_robot(robot=robot, name="my_board")
di8 = await my_board.digital_interrupt_by_name(name="8"))
di11 = await my_board.digital_interrupt_by_name(name="11"))

# Iterate over stream of ticks from pins 8 and 11.
async for tick in my_board.stream_ticks([di8, di11]):
    print(f"Pin {tick.pin_name} changed to {'high' if tick.high else 'low'} at {tick.time}")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.BoardClient.stream_ticks).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `interrupts` [([]DigitalInterrupt)](https://pkg.go.dev/go.viam.com/rdk/components/board#DigitalInterrupt): Slice of digital interrupts to receive ticks from.
- `ch chan` [(Tick)](https://pkg.go.dev/go.viam.com/rdk/components/board#Tick): The channel to stream Ticks, structs containing `Name`, `High`, and `TimestampNanosec` fields.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
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

err = myBoard.StreamTicks(context.Background(), interrupts, ticksChan, nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#Board).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `interrupts` [List](https://api.flutter.dev/flutter/dart-core/List-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)> (required)
- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic>? (optional)

**Returns:**

- [Stream](https://api.flutter.dev/flutter/dart-async/Stream-class.html)<[Tick](https://flutter.viam.dev/viam_sdk/Tick.html)>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
// Stream ticks from digital interrupts on pins 8 and 11
var interrupts = ['8', '11'];
Stream<Tick> tickStream = await myBoard.streamTicks(interrupts);
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Board/streamTicks.html).

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

- `mode` ([viam.proto.component.board.PowerMode.ValueType](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.PowerMode)) (required): The desired power mode.
- `duration` ([datetime.timedelta](https://docs.python.org/3/library/datetime.html#timedelta-objects)) (optional): Requested duration to stay in power mode.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_board = Board.from_robot(robot=robot, name="my_board")

# Set the power mode of the board to OFFLINE_DEEP.
status = await my_board.set_power_mode(mode=PowerMode.POWER_MODE_OFFLINE_DEEP)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.BoardClient.set_power_mode).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `mode` [(pb.PowerMode)](https://pkg.go.dev/go.viam.com/api/component/board/v1#PowerMode): Options to specify power usage of the board: `boardpb.PowerMode_POWER_MODE_UNSPECIFIED`, `boardpb.PowerMode_POWER_MODE_NORMAL`, and `boardpb.PowerMode_POWER_MODE_OFFLINE_DEEP`.
- `duration` [(*time.Duration)](https://pkg.go.dev/time#Duration): If provided, the board will exit the given power mode after the specified duration.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myBoard, err := board.FromRobot(robot, "my_board")

Set the power mode of the board to OFFLINE_DEEP.
myBoard.SetPowerMode(context.Background(), boardpb.PowerMode_POWER_MODE_OFFLINE_DEEP, nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#Board).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `powerMode` [PowerMode](https://flutter.viam.dev/viam_protos.component.board/PowerMode-class.html) (required)
- `seconds` [int](https://api.flutter.dev/flutter/dart-core/int-class.html) (required)
- `nanos` [int](https://api.flutter.dev/flutter/dart-core/int-class.html) (required)
- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<void>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
// Set the power mode of the board to offline deep for 60 seconds
// Requires importing 'package:viam_sdk/protos/component/board.dart'
const powerMode = PowerMode.POWER_MODE_OFFLINE_DEEP;
await myBoard.setPowerMode(powerMode, 60, 0);
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Board/setPowerMode.html).

{{% /tab %}}
{{< /tabs >}}

### GetGeometries

Get all the geometries associated with the board in its current configuration, in the [frame](/services/frame-system/) of the board.
The [motion](/services/motion/) and [navigation](/services/navigation/) services use the relative position of inherent geometries to configured geometries representing obstacles for collision detection and obstacle avoidance while motion planning.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([List[viam.proto.common.Geometry]](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Geometry)): The geometries associated with the Component.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
geometries = await component.get_geometries()

if geometries:
    # Get the center of the first geometry
    print(f"Pose of the first geometry's centerpoint: {geometries[0].center}")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.BoardClient.get_geometries).

{{% /tab %}}
{{< /tabs >}}

### Read

Read the current integer value of the digital signal output by the [ADC](#analogs).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- (viam.components.board.board.Board.Analog.Value): The current value, including the min, max, and step_size of the reader.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the Analog "my_example_analog_reader".
reader = await my_board.analog_reader_by_name(
    name="my_example_analog_reader")

# Get the value of the digital signal "my_example_analog_reader" has most
# recently measured.
reading = await reader.read()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.AnalogClient.read).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(AnalogValue)](https://pkg.go.dev/go.viam.com/rdk/components/board#AnalogValue): The current value, including the integer `Value` of the digital signal output by the analog pin and the `Min`, `Max`, and `StepSize` of the reader.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myBoard, err := board.FromRobot(robot, "my_board")

// Get the analog pin "my_example_analog".
analog, err := myBoard.AnalogByName("my_example_analog")

// Get the value of the analog signal "my_example_analog" has most recently measured.
reading, err := analog.Read(context.Background(), nil)
readingValue := reading.Value
stepSize := reading.StepSize
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#Analog).

{{% /tab %}}
{{< /tabs >}}

### Value

Get the current value of this interrupt.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([int](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)): The current value.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the DigitalInterrupt "my_example_digital_interrupt".
interrupt = await my_board.digital_interrupt_by_name(
    name="my_example_digital_interrupt")

# Get the amount of times this DigitalInterrupt has been interrupted with a
# tick.
count = await interrupt.value()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.DigitalInterruptClient.value).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(int64)](https://pkg.go.dev/builtin#int64): The amount of ticks that have occurred.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myBoard, err := board.FromRobot(robot, "my_board")

// Get the DigitalInterrupt "my_example_digital_interrupt".
interrupt, err := myBoard.DigitalInterruptByName("my_example_digital_interrupt")

// Get the amount of times this DigitalInterrupt has ticked.
count, err := interrupt.Value(context.Background(), nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#DigitalInterrupt).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `digitalInterruptName` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<[int](https://api.flutter.dev/flutter/dart-core/int-class.html)>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
// Get the current value of a digital interrupt named "my_example_digital_interrupt"
var interruptVal = await myBoard.digitalInterruptValue('my_example_digital_interrupt');
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Board/digitalInterruptValue.html).

{{% /tab %}}
{{< /tabs >}}

### DigitalInterruptNames

Get the name of every [`DigitalInterrupt`](#digital_interrupts) configured on the board.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None.

**Returns:**

- (List[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)]): The names of the digital interrupts.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the name of every DigitalInterrupt configured on the board.
names = await my_board.digital_interrupt_names()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.BoardClient.digital_interrupt_names).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- None.

**Returns:**

- [([]string)](https://pkg.go.dev/builtin#string): A slice containing the `"name"` of every interrupt [configured](#supported-models) on the board.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#Board).

{{% /tab %}}
{{< /tabs >}}

### GPIOPinByName

Get a `GPIOPin` by {{< glossary_tooltip term_id="pin-number" text="pin number" >}}.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): Name of the GPIO pin.

**Returns:**

- ([viam.components.board.board.Board.GPIOPin](https://python.viam.dev/autoapi/viam/components/board/board/index.html#viam.components.board.board.Board.GPIOPin)): The pin.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the GPIOPin with pin number 15.
pin = await my_board.gpio_pin_by_name(name="15")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.BoardClient.gpio_pin_by_name).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `name` [(string)](https://pkg.go.dev/builtin#string): Pin number of the GPIO pin you want to retrieve as a `GPIOPin` interface. Refer to the pinout diagram and data sheet of your [board model](#supported-models) for {{< glossary_tooltip term_id="pin-number" text="pin numbers" >}}.

**Returns:**

- [(GPIOPin)](https://pkg.go.dev/go.viam.com/rdk/components/board#GPIOPin): An interface representing an individual GPIO pin on the board.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myBoard, err := board.FromRobot(robot, "my_board")

// Get the GPIOPin with pin number 15.
pin, err := myBoard.GPIOPinByName("15")
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#Board).

{{% /tab %}}
{{< /tabs >}}

### Reconfigure

Reconfigure this resource.
Reconfigure must reconfigure the resource atomically and in place.

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `deps` [(Dependencies)](https://pkg.go.dev/go.viam.com/rdk/resource#Dependencies): The resource dependencies.
- `conf` [(Config)](https://pkg.go.dev/go.viam.com/rdk/resource#Config): The resource configuration.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}

### DoCommand

Execute model-specific commands that are not otherwise defined by the component API.
For built-in models, model-specific commands are covered with each model's documentation.
If you are implementing your own board and add features that have no built-in API method, you can access them with `DoCommand`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `command` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), ValueTypes]) (required): The command to execute.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), viam.utils.ValueTypes]): Result of the executed command.

**Raises:**

- (NotImplementedError): Raised if the Resource does not support arbitrary commands.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
command = {"cmd": "test", "data1": 500}
result = component.do(command)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.BoardClient.do_command).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `cmd` [(map[string]interface{})](https://go.dev/blog/maps): The command to execute.

**Returns:**

- [(map[string]interface{})](https://pkg.go.dev/builtin#string): The command response.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// This example shows using DoCommand with an arm component.
myArm, err := arm.FromRobot(machine, "my_arm")

command := map[string]interface{}{"cmd": "test", "data1": 500}
result, err := myArm.DoCommand(context.Background(), command)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `command` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic> (required)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<[Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic>>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
// Example using doCommand with an arm component
const command = {'cmd': 'test', 'data1': 500};
var result = myArm.doCommand(command);
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Resource/doCommand.html).

{{% /tab %}}
{{< /tabs >}}

### FromRobot

Get the resource from the provided robot with the given name.

{{< tabs >}}
{{% tab name="Flutter" %}}

**Parameters:**

- `robot` [RobotClient](https://flutter.viam.dev/viam_sdk/RobotClient-class.html) (required)
- `name` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)

**Returns:**

- [Board](https://flutter.viam.dev/viam_sdk/Board-class.html)

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Board/fromRobot.html).

{{% /tab %}}
{{< /tabs >}}

### Name

Get the `ResourceName` for this board with the given name.

{{< tabs >}}
{{% tab name="Flutter" %}}

**Parameters:**

- `name` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)

**Returns:**

- [ResourceName](https://flutter.viam.dev/viam_sdk/ResourceName-class.html)

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Board/getResourceName.html).

{{% /tab %}}
{{< /tabs >}}

### Close

Safely shut down the resource and prevent further use.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await component.close()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.BoardClient.close).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// This example shows using Close with an arm component.
myArm, err := arm.FromRobot(machine, "my_arm")

err = myArm.Close(ctx)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}
