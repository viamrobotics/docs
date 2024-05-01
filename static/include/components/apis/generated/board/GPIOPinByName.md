### GPIOPinByName

{{< tabs >}}
{{% tab name="Python" %}}

Get a GPIO Pin by name.

**Parameters:**

- `name` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): Name of the GPIO pin.


**Returns:**

- [(viam.components.board.board.Board.GPIOPin)](INSERT RETURN TYPE LINK): The pin.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.BoardClient.gpio_pin_by_name).

``` python {class="line-numbers linkable-line-numbers"}
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the GPIOPin with pin number 15.
pin = await my_board.gpio_pin_by_name(name="15")

```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `name`[(string)](<INSERT PARAM TYPE LINK>)

**Returns:**

- [(GPIOPin)](<INSERT PARAM TYPE LINK>)
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#Board).

{{% /tab %}}
