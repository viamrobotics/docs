### ReadAnalogReader

{{< tabs >}}
{{% tab name="Python" %}}

Get an AnalogReader by name.

**Parameters:**

- `name` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): Name of the analog reader to be retrieved.

**Returns:**

- [(viam.components.board.board.Board.AnalogReader)](INSERT RETURN TYPE LINK): The analog reader.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.BoardClient.analog_reader_by_name).

``` python {class="line-numbers linkable-line-numbers"}
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the AnalogReader "my_example_analog_reader".
reader = await my_board.analog_reader_by_name(name="my_example_analog_reader")
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `name` [(string)](https://pkg.go.dev/builtin#string):

**Returns:**

- [(Analog)](https://pkg.go.dev#Analog):
- [(error)](https://pkg.go.dev/builtin#error):

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#Board).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `analogReaderName` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `boardName` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `extra` [(Struct)](<INSERT PARAM TYPE LINK>) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.board/BoardServiceClient/readAnalogReader.html).

{{% /tab %}}
{{< /tabs >}}
