### DigitalInterruptNames

{{< tabs >}}
{{% tab name="Python" %}}

Get the names of all known digital interrupts.

**Parameters:**

- None.

**Returns:**

- [(List[str])](INSERT RETURN TYPE LINK): The names of the digital interrupts.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.BoardClient.digital_interrupt_names).

``` python {class="line-numbers linkable-line-numbers"}
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the name of every DigitalInterrupt configured on the board.
names = await my_board.digital_interrupt_names()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(string)](https://pkg.go.dev/builtin#string):

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#Board).

{{% /tab %}}
{{< /tabs >}}
