### GetDigitalInterruptValue

{{< tabs >}}
{{% tab name="Python" %}}

Get a DigitalInterrupt by name.

**Parameters:**

- `name` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): Name of the digital interrupt.


**Returns:**

- [(viam.components.board.board.Board.DigitalInterrupt)](INSERT RETURN TYPE LINK): The digital interrupt.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.BoardClient.digital_interrupt_by_name).

``` python {class="line-numbers linkable-line-numbers"}
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the DigitalInterrupt "my_example_digital_interrupt".
interrupt = await my_board.digital_interrupt_by_name(
    name="my_example_digital_interrupt")

```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `name`[(string)](<INSERT PARAM TYPE LINK>)

**Returns:**

- [(DigitalInterrupt)](<INSERT PARAM TYPE LINK>)
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#Board).

{{% /tab %}}
