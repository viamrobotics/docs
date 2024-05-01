### SetGPIO

\{\{< tabs >}}
\{\{% tab name="Python" %}\}

Python Method: set

Set the pin to either low or high.

**Parameters:**

- `high` [(bool)](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool) (required) When true, sets the pin to high. When false, sets the pin to low.:
- `high`- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional) Extra options to pass to the underlying RPC call.:
- `extra`- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional) An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.:
- `timeout`

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.GPIOPinClient.set).

``` python {class="line-numbers linkable-line-numbers"}
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the GPIOPin with pin number 15.
pin = await my_board.gpio_pin_by_name(name="15")

# Set the pin to high.
await pin.set(high="true")

```

\{\{% /tab %}}

\{\{% tab name="Go" %\}\}

Go Method: Set

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `high`[(bool)](<INSERT PARAM TYPE LINK>)
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#GPIOPin).

\{\{% /tab %}}

\{\{% tab name="Flutter" %}\}

Flutter Method: setGPIO

**Parameters:**

- `extra` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `extra`- `high` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `high`- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `name`- `pin` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `pin`

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.board/BoardServiceClient/setGPIO.html).

\{\{% /tab %}}

\{\{< /tabs >}}

