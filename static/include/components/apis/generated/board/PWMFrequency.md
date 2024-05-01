### PWMFrequency

{{< tabs >}}
{{% tab name="Python" %}}

Get the PWM frequency of the pin.

**Parameters:**

- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Extra options to pass to the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.


**Returns:**

- [(int)](INSERT RETURN TYPE LINK): The PWM frequency.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.GPIOPinClient.get_pwm_frequency).

``` python {class="line-numbers linkable-line-numbers"}
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the GPIOPin with pin number 15.
pin = await my_board.gpio_pin_by_name(name="15")

# Get the PWM frequency of this pin.
freq = await pin.get_pwm_frequency()

```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(uint)](<INSERT PARAM TYPE LINK>)
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#GPIOPin).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `pin` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.board/BoardServiceClient/pWMFrequency.html).

{{% /tab %}}
{{< /tabs >}}
