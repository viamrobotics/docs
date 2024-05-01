### GetPWM

\{\{< tabs >}}
\{\{% tab name="Python" %}\}

Python Method: get_pwm

Get the pin’s given duty cycle.

**Parameters:**

- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional) Extra options to pass to the underlying RPC call.:
- `extra`- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional) An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.:
- `timeout`

**Returns:**

- [(float)](INSERT RETURN TYPE LINK): The duty cycle.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.GPIOPinClient.get_pwm).

``` python {class="line-numbers linkable-line-numbers"}
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the GPIOPin with pin number 15.
pin = await my_board.gpio_pin_by_name(name="15")

# Get if it is true or false that the state of the pin is high.
duty_cycle = await pin.get_pwm()

```

\{\{% /tab %}}

\{\{% tab name="Go" %\}\}

Go Method: PWM

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(float64)](<INSERT PARAM TYPE LINK>)
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#GPIOPin).

\{\{% /tab %}}

\{\{% tab name="Flutter" %}\}

Flutter Method: pWM

**Parameters:**

- `extra` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `extra`- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `name`- `pin` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `pin`

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.board/BoardServiceClient/pWM.html).

\{\{% /tab %}}

\{\{< /tabs >}}

