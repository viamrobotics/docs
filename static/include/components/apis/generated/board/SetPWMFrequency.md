### SetPWMFrequency

\{\{< tabs >}}
\{\{% tab name="Python" %}\}

Python Method: set_pwm_frequency

Set the pin to the given PWM frequency (in Hz). When frequency is 0, it will use the board’s default PWM frequency.

**Parameters:**

- `frequency` [(int)](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex) (required) The frequency, in Hz.:
- `frequency`- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional) Extra options to pass to the underlying RPC call.:
- `extra`- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional) An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.:
- `timeout`

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.GPIOPinClient.set_pwm_frequency).

``` python {class="line-numbers linkable-line-numbers"}
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the GPIOPin with pin number 15.
pin = await my_board.gpio_pin_by_name(name="15")

# Set the PWM frequency of this pin to 1600 Hz.
high = await pin.set_pwm_frequency(frequency=1600)

```

\{\{% /tab %}}

\{\{% tab name="Go" %\}\}

Go Method: SetPWMFreq

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `freqHz`[(uint)](<INSERT PARAM TYPE LINK>)
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#GPIOPin).

\{\{% /tab %}}

\{\{% tab name="Flutter" %}\}

Flutter Method: setPWMFrequency

**Parameters:**

- `extra` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `extra`- `frequencyHz` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `frequencyHz`- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `name`- `pin` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `pin`

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.board/BoardServiceClient/setPWMFrequency.html).

\{\{% /tab %}}

\{\{< /tabs >}}

