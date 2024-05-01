### SetPWM

{{< tabs >}}
{{% tab name="Python" %}}

Set the pin to the given duty_cycle.

**Parameters:**

- `duty_cycle` [(float)](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex) (required): The duty cycle.
- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Extra options to pass to the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/board/client/index.html#viam.components.board.client.GPIOPinClient.set_pwm).

``` python {class="line-numbers linkable-line-numbers"}
my_board = Board.from_robot(robot=robot, name="my_board")

# Get the GPIOPin with pin number 15.
pin = await my_board.gpio_pin_by_name(name="15")

# Set the duty cycle to .6, meaning that this pin will be in the high state for
# 60% of the duration of the PWM interval period.
await pin.set_pwm(cycle=.6)

```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `dutyCyclePct`[(float64)](<INSERT PARAM TYPE LINK>)
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/board#GPIOPin).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `dutyCyclePct` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `extra` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `pin` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.board/BoardServiceClient/setPWM.html).

{{% /tab %}}
{{< /tabs >}}
