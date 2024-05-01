### Value

{{< tabs >}}
{{% tab name="Python" %}}

Get the current value of the interrupt, which is based on the type of interrupt.

**Parameters:**

- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Extra options to pass to the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.


**Returns:**

- [(int)](INSERT RETURN TYPE LINK): The current value.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.DigitalInterruptClient.value).

``` python {class="line-numbers linkable-line-numbers"}
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

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(int64)](<INSERT PARAM TYPE LINK>)
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#DigitalInterrupt).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `boardName` [(Struct)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `digitalInterruptName` [(Struct)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `extra` [(Struct)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.board/BoardServiceClient/getDigitalInterruptValue.html).

{{% /tab %}}
{{< /tabs >}}
