### Read

{{< tabs >}}
{{% tab name="Python" %}}

Read the current value.

**Parameters:**

- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Extra options to pass to the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(int)](INSERT RETURN TYPE LINK): The current value.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.AnalogReaderClient.read).

``` python {class="line-numbers linkable-line-numbers"}
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the GPIOPin with pin number 15.
pin = await my_board.gpio_pin_by_name(name="15")

# Get if it is true or false that the pin is set to high.
duty_cycle = await pin.get_pwm()

# Get the AnalogReader "my_example_analog_reader".
reader = await my_board.analog_reader_by_name(
    name="my_example_analog_reader")

# Get the value of the digital signal "my_example_analog_reader" has most
# recently measured.
reading = reader.read()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(int)](https://pkg.go.dev/builtin#int):
- [(error)](https://pkg.go.dev/builtin#error):

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#Analog).

{{% /tab %}}
{{< /tabs >}}
