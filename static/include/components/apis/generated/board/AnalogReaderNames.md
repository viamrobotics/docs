### AnalogReaderNames

{{< tabs >}}
{{% tab name="Python" %}}

Get the names of all known analog readers.


**Returns:**

- [(List[str])](INSERT RETURN TYPE LINK): The list of names of all known analog readers.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.BoardClient.analog_reader_names).

``` python {class="line-numbers linkable-line-numbers"}
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the name of every AnalogReader configured on the board.
names = await my_board.analog_reader_names()

```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(string)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#Board).

{{% /tab %}}
