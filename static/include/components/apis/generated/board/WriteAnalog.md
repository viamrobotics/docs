### WriteAnalog

{{< tabs >}}
{{% tab name="Python" %}}

Write an analog value to a pin on the board.

**Parameters:**

- `pin` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): The name of the pin.
- `value` [(int)](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex) (required): The value to write.
- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Extra options to pass to the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.BoardClient.write_analog).

``` python {class="line-numbers linkable-line-numbers"}
my_board = Board.from_robot(robot=robot, name="my_board")

# Set pin 11 to value 48.
await my_board.write_analog(pin="11", value=48)

```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `pin`[(string)](<INSERT PARAM TYPE LINK>)
- `value`[(int32)](<INSERT PARAM TYPE LINK>)
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#Board).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [(int)](https://api.flutter.dev/flutter/dart-core/int-class.html) (required):
- `name` [(int)](https://api.flutter.dev/flutter/dart-core/int-class.html) (required):
- `pin` [(int)](https://api.flutter.dev/flutter/dart-core/int-class.html) (required):
- `value` [(int)](https://api.flutter.dev/flutter/dart-core/int-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.board/BoardServiceClient/writeAnalog.html).

{{% /tab %}}
{{< /tabs >}}
