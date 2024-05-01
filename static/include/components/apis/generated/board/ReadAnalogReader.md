### ReadAnalogReader

\{\{< tabs >}}
\{\{% tab name="Python" %}\}

Python Method: analog_reader_by_name

Get an AnalogReader by name.

**Parameters:**

- `name` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required) Name of the analog reader to be retrieved.:
- `name`

**Returns:**

- [(viam.components.board.board.Board.AnalogReader)](INSERT RETURN TYPE LINK): The analog reader.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.BoardClient.analog_reader_by_name).

``` python {class="line-numbers linkable-line-numbers"}
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the AnalogReader "my_example_analog_reader".
reader = await my_board.analog_reader_by_name(name="my_example_analog_reader")

```

\{\{% /tab %}}

\{\{% tab name="Go" %\}\}

Go Method: AnalogReaderByName

